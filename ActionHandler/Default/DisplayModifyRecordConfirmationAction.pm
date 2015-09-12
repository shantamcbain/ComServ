package Default::DisplayModifyRecordConfirmationAction;

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
        -ALLOW_MODIFICATIONS_FLAG,
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -CGI_OBJECT,
        -DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -LOG_CONFIG_PARAMS,
        -MAX_RECORDS_PER_PAGE,
        -MODIFY_RECORD_CONFIRMATION_VIEW_NAME,
        -MODIFY_FORM_VIEW_NAME,
        -REQUIRE_AUTH_FOR_MODIFYING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SESSION_OBJECT,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -DATETIME_CONFIG_PARAMS,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -APPLICATION_OBJECT,
        -INPUT_WIDGET_DEFINITIONS,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};
    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};

    if (defined($cgi->param('display_modify_record_confirmation'))) {

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


        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME => '-DISPLAY_TYPE',
            -PARAM_VALUE => 'CONFIRM'
        );



        if (!$params->{-ALLOW_MODIFICATIONS_FLAG}) {
            die ('Sorry, but you are not allowed to perform additions. ' .
                 'To enable additions, you must set -ALLOW_MODIFICATIONS_FLAG ' .
                 'in the @ACTION_HANDLER_ACTION_PARAMS array ' .
                 'in the application executable to 1'
            );
        }

        elsif ($params->{-REQUIRE_AUTH_FOR_MODIFYING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                    or die("Whoopsy!  I was unable to construct the " .
                           "Authentication object. " .
                           "Please contact the webmaster.");
                $auth_manager->authenticate();
            }

            else {
                die('You have set -REQUIRE_AUTH_FOR_MODIFYING_FLAG to 1 ' .
                    ' in the application executable, but you have not ' .
                    ' defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                    '@ACTION_HANDLER_ACTION_PARAMS array ' .
                    'in the application executable. This action ' .
                    ' cannot procede unless you do both.'
               );
           }
        }

        my $data_handler_manager_config_params = $params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS};

        my @dhm_config_params = _rearrange([
            -MODIFY_FORM_DHM_CONFIG_PARAMS
                ],
                [
                ],
            @{$params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS}}
        );

        my $modify_form_dhm_config_params = shift (@dhm_config_params);

        if ($modify_form_dhm_config_params) {
            my $log_object;
            if ($params->{-LOG_CONFIG_PARAMS}) {
                $log_object = Extropia::Core::Log->create(@{$params->{-LOG_CONFIG_PARAMS}})
                    or die("Whoopsy!  I was unable to construct the " .
                           "Log object. Please " .
                           "contact the webmaster."
                );
            }

            my $data_handler_success = $app->handleIncomingData(
                -CGI_OBJECT                 => $params->{-CGI_OBJECT},
                -LOG_OBJECT                 => $log_object,
                -DATA_HANDLER_CONFIG_PARAMS => $modify_form_dhm_config_params,
                -ACTION_HANDLER_PLUGINS     => $params->{-ACTION_HANDLER_PLUGINS},
            );

            if (!$data_handler_success) {
                $app->setNextViewToDisplay(
                    -VIEW_NAME => $params->{-MODIFY_FORM_VIEW_NAME}
                );
                my $error;
                foreach $error ($app->getDataHandlerErrors()) {
                    $app->addError($error);
                }

                my @config_params = _rearrange([
                    -BASIC_DATASOURCE_CONFIG_PARAMS
                        ],
                        [
                    -BASIC_DATASOURCE_CONFIG_PARAMS
                        ],
                    @{$params->{-DATASOURCE_CONFIG_PARAMS}}
                );

                my $datasource_config_params = shift (@config_params);

                if ($datasource_config_params) {
                    my $ra_records = $app->loadData
                        (
                         -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
                         -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
                         -KEY_FIELD                   => $params->{-KEY_FIELD},
                         -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
                         -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
                         -RECORD_ID                   => $cgi->param('record_id') || "",
                         -SORT_FIELD1                 => $params->{-SORT_FIELD1},
                         -SORT_FIELD2                 => $params->{-SORT_FIELD2},
                         -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
                         -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
                         -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING},
                         -CGI_OBJECT                  => $params->{-CGI_OBJECT},
                         -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
                         -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
                         -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG},
                         -ACTION_HANDLER_PLUGINS      => $params->{-ACTION_HANDLER_PLUGINS},
                        );

                    $app->setAdditionalViewDisplayParam
                        (
                         -PARAM_NAME  => "-RECORDS",
                         -PARAM_VALUE => $ra_records,
                        );

                }

                else {
                    die('You must specify a configuration for ' .
                        '-BASIC_DATASOURCE_CONFIG_PARAMS in order to ' .
                        'use loadData(). You may do so in the ' .
                        '@ACTION_HANDLER_ACTION_PARAMS array ' .
                        'in the application executable'
                    );
                }
                return 1;
            }
        }

        my @config_params = _rearrange([
            -BASIC_DATASOURCE_CONFIG_PARAMS
                ],
                [
            -BASIC_DATASOURCE_CONFIG_PARAMS
                ],
            @{$params->{-DATASOURCE_CONFIG_PARAMS}}
        );

        my $datasource_config_params = shift (@config_params);

        if ($datasource_config_params) {
            my $ra_records = $app->loadData
                (
                 -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
                 -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
                 -KEY_FIELD                   => $params->{-KEY_FIELD},
                 -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
                 -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
                 -RECORD_ID                   => $cgi->param('record_id') || "",
                 -SORT_FIELD1                 => $params->{-SORT_FIELD1},
                 -SORT_FIELD2                 => $params->{-SORT_FIELD2},
                 -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
                 -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
                 -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING},
                 -CGI_OBJECT                  => $params->{-CGI_OBJECT},
                 -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
                 -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
                 -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG},
                 -ACTION_HANDLER_PLUGINS      => $params->{-ACTION_HANDLER_PLUGINS},
                );

            $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-RECORDS",
                 -PARAM_VALUE => $ra_records,
                );
        }

        else {
            die('You must specify a configuration for ' .
                '-BASIC_DATASOURCE_CONFIG_PARAMS in order to ' .
                'use loadData(). You may do so in the ' .
                '@ACTION_HANDLER_ACTION_PARAMS array ' .
               'in the application executable');
        }

        $app->setNextViewToDisplay(
            -VIEW_NAME => $params->{-MODIFY_RECORD_CONFIRMATION_VIEW_NAME}
        );

        return 1;
    }

    return 0;
}
