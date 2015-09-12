package Default::DisplayAddRecordConfirmationAction;

# Copyright (C) 1994 - 2001  eXtropia.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::Action;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
        
    my ($params) = _rearrangeAsHash([
        -ADD_FORM_VIEW_NAME,
        -ADD_RECORD_CONFIRMATION_VIEW_NAME,
        -ALLOW_ADDITIONS_FLAG,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -CGI_OBJECT,        
        -DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
        -LOG_CONFIG_PARAMS,
        -REQUIRE_AUTH_FOR_ADDING_FLAG,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -ADD_FORM_VIEW_NAME,
        -ADD_RECORD_CONFIRMATION_VIEW_NAME,
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
        -INPUT_WIDGET_DEFINITIONS,
            ],
        @_
    );

    my $app          = $params->{-APPLICATION_OBJECT};
    my $cgi          = $params->{-CGI_OBJECT};
    my $data_handler_manager_config_params = $params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS};
    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};

    if (defined($cgi->param('display_add_record_confirmation'))) {
        if (!$params->{-ALLOW_ADDITIONS_FLAG}) {
            die ('Sorry, but you are not allowed to perform additions. ' .
                 'To enable additions, you must set -ALLOW_ADDITIONS_FLAG ' .
                 'in the @ACTION_HANDLER_ACTION_PARAMS array ' .
                 'in the application executable to 1'
            );
        }

        if ($params->{-REQUIRE_AUTH_FOR_ADDING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                    or die("Whoopsy!  I was unable to construct the " .
                           "Authentication object. " .
                           "Please contact the webmaster.");
                $auth_manager->authenticate();
            }
            else {
                die('You have set -REQUIRE_AUTH_FOR_ADDING_FLAG to 1 ' .
                    ' in the application executable, but you have not ' .
                    ' defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                    '@ACTION_HANDLER_ACTION_PARAMS array ' .
                    'in the application executable. This action ' .
                    ' cannot procede unless you do both.'
                );
            }
        }
 
        my @input_widget_config_params = _rearrange([
            -BASIC_INPUT_WIDGET_DEFINITIONS,
            -BASIC_INPUT_WIDGET_DISPLAY_ORDER
                ],
                [
            -BASIC_INPUT_WIDGET_DEFINITIONS,
            -BASIC_INPUT_WIDGET_DISPLAY_ORDER
                ],
            @$input_widget_config
       );

        my $input_widget_definitions   = shift (@input_widget_config_params);
        my $input_widget_display_order = shift (@input_widget_config_params);

        if (!$input_widget_display_order){
            die('You have not defined -BASIC_INPUT_WIDGET_DISPLAY_ORDER ' .
                'in the  @ACTION_HANDLER_ACTION_PARAMS array ' .
                'in the application executable. This action ' .
                'cannot procede unless you do so.'
            );
        }

        if (!$input_widget_definitions){
            die('You have not defined -BASIC_INPUT_WIDGET_DEFINITIONS ' .
                'in the  @ACTION_HANDLER_ACTION_PARAMS array ' .
                'in the application executable. This action ' .
                'cannot procede unless you do so.'
            );
        }

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME => '-INPUT_WIDGET_CONFIG',
            -PARAM_VALUE => $input_widget_definitions
        );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME => '-INPUT_WIDGET_DISPLAY_ORDER',
            -PARAM_VALUE => $input_widget_display_order
        );

        if ($data_handler_manager_config_params) {
            my @dhm_config_params = _rearrange([
                -ADD_FORM_DHM_CONFIG_PARAMS
                    ],
                    [
                    ],
                @$data_handler_manager_config_params
            );

            my $add_form_dhm_config_params = shift (@dhm_config_params);

            if ($add_form_dhm_config_params) {
                my $log_object;
                if ($params->{-LOG_CONFIG_PARAMS}) {
                    $log_object = Extropia::Core::Log->create(@{$params->{-LOG_CONFIG_PARAMS}})
                        or die("Whoopsy!  I was unable to construct the " .
                               "Log object. Please contact the webmaster.");
                }

                my $data_handler_success = $app->handleIncomingData
                    (
                     -CGI_OBJECT                 => $params->{-CGI_OBJECT},
                     -LOG_OBJECT                 => $log_object,
                     -DATA_HANDLER_CONFIG_PARAMS => $add_form_dhm_config_params,
                     -ACTION_HANDLER_PLUGINS     => $params->{-ACTION_HANDLER_PLUGINS},
                );

                if (!$data_handler_success) {
                    $app->setNextViewToDisplay(
                        -VIEW_NAME => $params->{-ADD_FORM_VIEW_NAME}
                    );
                    my $error;
                    foreach $error ($app->getDataHandlerErrors()) {
                        $app->addError($error);
                    }
                    return 1;
                }

                


            }
        }

        $app->setNextViewToDisplay(
            -VIEW_NAME => $params->{-ADD_RECORD_CONFIRMATION_VIEW_NAME}
        );

        return 1;
    }

    return 0;
}
