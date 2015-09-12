package Default::SimpleForm::ProcessFormAction;

# Copyright (C) 1994 - 2001 eXtropia.com
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
use Extropia::Core::Log;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([
        -APPLICATION_OBJECT,
        -ACKNOWLEDGEMENT_VIEW_NAME,
        -CGI_OBJECT,
        -LOG_OBJECT,
        -SEND_ADMIN_EMAIL_FLAG,
        -SEND_USER_EMAIL_FLAG,
        -FORM_VIEW_NAME,
        -DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -DISPLAY_ACKNOWLEDGEMENT_FLAG,
        -LOG_FORM_SUBMISSION_FLAG,
        -DATASOURCE_CONFIG_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
        -SEND_ADMIN_RECEIPT_FLAG,
        -SEND_USER_RECEIPT_FLAG,
        -USER_EMAIL_BODY_VIEW,
        -ADMIN_EMAIL_BODY_VIEW,
        -VIEW_DISPLAY_PARAMS,
        -MAIL_CONFIG_PARAMS,
        -MAIL_SEND_PARAMS,
        -USER_MAIL_SEND_PARAMS,
        -ADMIN_MAIL_SEND_PARAMS,
        -ENCRYPT_MAIL_FLAG,
        -ENCRYPT_CONFIG_PARAMS,
        -VIEW_LOADER,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -VIEW_DISPLAY_PARAMS,
        -VIEW_LOADER
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    if (defined($cgi->param('submit_form'))) {

        my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};
        my @input_widget_config_params = _rearrange
            ([
              -BASIC_INPUT_WIDGET_DEFINITIONS,
              -BASIC_INPUT_WIDGET_DISPLAY_ORDER
             ],
             [
              -BASIC_INPUT_WIDGET_DEFINITIONS,
              -BASIC_INPUT_WIDGET_DISPLAY_ORDER
             ],
             @$input_widget_config
            );

        my $input_widget_definitions = shift (@input_widget_config_params);
        my $input_widget_display_order = shift (@input_widget_config_params);
      
        my $log_object;
        if ($params->{-LOG_CONFIG_PARAMS}) {
            $log_object = Extropia::Core::Log->create(@{$params->{-LOG_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Log object. Please " .
                       "contact the webmaster.");
        }

        my $addition_request_success = 0;

        my @dhm_config_params = _rearrange([
            -BASIC_FORM_DHM_CONFIG_PARAMS
                ],
                [
                ],
            @{$params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS}}
        );

        my $dhm_config_params = shift (@dhm_config_params);

        if ($dhm_config_params) {
            my $data_handler_success = $app->handleIncomingData
                (
                 -CGI_OBJECT                 => $params->{-CGI_OBJECT},
                 -LOG_OBJECT                 => $log_object,
                 -DATA_HANDLER_CONFIG_PARAMS => $dhm_config_params,
                 -ACTION_HANDLER_PLUGINS      => $params->{-ACTION_HANDLER_PLUGINS},
            );

            if (!$data_handler_success) {
                $app->setAdditionalViewDisplayParam(
                    -PARAM_NAME => '-INPUT_WIDGET_CONFIG',
                    -PARAM_VALUE => $input_widget_definitions
                );

                $app->setAdditionalViewDisplayParam(
                    -PARAM_NAME => '-INPUT_WIDGET_DISPLAY_ORDER',
                    -PARAM_VALUE => $input_widget_display_order
                );	

                $app->setNextViewToDisplay(
                    -VIEW_NAME => $params->{-FORM_VIEW_NAME}
                );

                my $error;
                foreach $error ($app->getDataHandlerErrors()) {
                    $app->addError($error);
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

        $addition_request_success = $app->addRecord((
            -CGI_OBJECT               => $params->{-CGI_OBJECT},
            -SESSION_OBJECT           => $params->{-SESSION_OBJECT},
            -KEY_FIELD                => $params->{-KEY_FIELD},
            -LOG_OBJECT               => $log_object,
            -DATASOURCE_CONFIG_PARAMS => $datasource_config_params,
            -ALLOW_DUPLICATE_ENTRIES  => $params->{-ALLOW_DUPLICATE_ENTRIES}
        ));

        if ($addition_request_success) {
            if ($params->{'-SEND_ADMIN_EMAIL_FLAG'}) {
                my @send_params = _rearrange([
                    -SUBMIT_EVENT_MAIL_SEND_PARAMS_FOR_ADMIN,
                        ],
                        [
                    -SUBMIT_EVENT_MAIL_SEND_PARAMS_FOR_ADMIN,
                        ],
                    @{$params->{-MAIL_SEND_PARAMS}}
                );

                my $admin_mail_send_params = shift (@send_params);
                my $view_loader = $params->{-VIEW_LOADER};
		my $body = $view_loader->process_email
		    (
		    	$params->{-ADMIN_EMAIL_BODY_VIEW},
		    	{
		    		-CGI_OBJECT => $params->{-CGI_OBJECT},
		    		@{$params->{-VIEW_DISPLAY_PARAMS}}
		    	}
		    );

                $app->sendMail((
                    -MAIL_CONFIG_PARAMS => $params->{-MAIL_CONFIG_PARAMS},
                    -BODY               => $body,
                    @$admin_mail_send_params
                ));
            }

            if ($params->{'-SEND_USER_EMAIL_FLAG'}) {
                my @send_params = _rearrange([
                    -SUBMIT_EVENT_MAIL_SEND_PARAMS_FOR_USER
                        ],
                        [
                    -SUBMIT_EVENT_MAIL_SEND_PARAMS_FOR_USER
                        ],
                    @{$params->{-MAIL_SEND_PARAMS}}
                );

                my $user_mail_send_params = shift (@send_params);

                my $view_loader = $params->{-VIEW_LOADER};
		my $body = $view_loader->process_email
		    (
		    	$params->{-USER_EMAIL_BODY_VIEW},
		    	{
		    		-CGI_OBJECT => $params->{-CGI_OBJECT},
		    		@{$params->{-VIEW_DISPLAY_PARAMS}}
		    	}
		    );
                $app->sendMail((
                    -MAIL_CONFIG_PARAMS => $params->{-MAIL_CONFIG_PARAMS},
                    -BODY               => $body,
                    @$user_mail_send_params
                ));
            }
        }

        if (!$addition_request_success) {
           $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-FORM_VIEW_NAME}
            );
        }

        elsif ($params->{-DISPLAY_ACKNOWLEDGEMENT_FLAG}) {
           $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-ACKNOWLEDGEMENT_VIEW_NAME}
            );
        }

        else {
           $app->setAdditionalViewDisplayParam(
                   -PARAM_NAME => '-INPUT_WIDGET_CONFIG',
                   -PARAM_VALUE => $input_widget_definitions
               );

           $app->setAdditionalViewDisplayParam(
                   -PARAM_NAME => '-INPUT_WIDGET_DISPLAY_ORDER',
                   -PARAM_VALUE => $input_widget_display_order
               );	
        	
           $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-FORM_VIEW_NAME}
           );
       }



        return 1;
    }

    return 0;
}

