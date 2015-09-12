package Default::ProcessModifyRequestAction;

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
use Extropia::Core::DateTime ();
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
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG,
        -MODIFY_EMAIL_BODY_VIEW,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_RETRIEVED,
        -MAX_RECORDS_PER_PAGE,
        -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME,
        -MODIFY_FILE_FIELD_LIST,
        -MODIFY_FORM_VIEW_NAME,
        -MAIL_SEND_PARAMS,
        -MAIL_CONFIG_PARAMS,
        -MODIFY_FORM_VIEW_NAME,
        -REQUIRE_AUTH_FOR_MODIFYING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SEND_EMAIL_ON_MODIFY_FLAG,
        -SESSION_OBJECT,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -VIEW_DISPLAY_PARAMS,
        -VIEW_LOADER,
        -UPLOAD_MANAGER_CONFIG_PARAMS,
        -DATETIME_CONFIG_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -APPLICATION_OBJECT,
            ],
        @_
    );

    my $app     = $params->{-APPLICATION_OBJECT};
    my $session = $params->{-SESSION_OBJECT};
    my $cgi     = $params->{-CGI_OBJECT};

    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};

    if (defined($cgi->param('submit_modify_record')) &&
        $params->{-ALLOW_MODIFICATIONS_FLAG}) {



        my $modification_request_success = 0;
        my $auth_manager;
        if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
            $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object. " .
                       "Please contact the webmaster.");
        }

        my $log_object;
        if ($params->{-LOG_CONFIG_PARAMS}) {
           $log_object = Extropia::Core::Log->create(@{$params->{-LOG_CONFIG_PARAMS}})
               or die("Whoopsy!  I was unable to construct the " .
                      "Log object. Please " .
                      "contact the webmaster.");
       }

        my @dhm_config_params = _rearrange([
           -MODIFY_FORM_DHM_CONFIG_PARAMS
               ],
               [
               ],
            @{$params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS}}
       );

        my $modify_form_dhm_config_params = shift (@dhm_config_params);


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

        my $input_widget_definitions   = shift (@input_widget_config_params);
        my $input_widget_display_order = shift (@input_widget_config_params);

        
        my @config_params = _rearrange([
           -BASIC_DATASOURCE_CONFIG_PARAMS
               ],
               [
           -BASIC_DATASOURCE_CONFIG_PARAMS
               ],
           @{$params->{-DATASOURCE_CONFIG_PARAMS}}
        );

        my $datasource_config_params = shift (@config_params);

        if ($auth_manager && $params->{-REQUIRE_AUTH_FOR_MODIFYING_FLAG}) {
            $auth_manager->authenticate();
        }

        if ($modify_form_dhm_config_params) {

            my $data_handler_success = $app->handleIncomingData
                (
                 -CGI_OBJECT                 => $cgi,
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

                return 1;
            }
        }

        $modification_request_success = $app->modifyRecord((
                    -CGI_OBJECT               => $params->{-CGI_OBJECT},
                    -SESSION_OBJECT           => $params->{-SESSION_OBJECT},
                    -LOG_OBJECT               => $log_object,
                    -KEY_FIELD                => $params->{-KEY_FIELD},
                    -DATASOURCE_CONFIG_PARAMS => $datasource_config_params,
                    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG},
                    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG},
                    -MODIFY_FILE_FIELD_LIST => $params->{-MODIFY_FILE_FIELD_LIST},
                    -UPLOAD_MANAGER_CONFIG_PARAMS => $params->{-UPLOAD_MANAGER_CONFIG_PARAMS}
        ));

        if ($modification_request_success) {
            if ($params->{-SEND_EMAIL_ON_MODIFY_FLAG}) {

                my $view_loader = $params->{-VIEW_LOADER};
                my $body = $view_loader->process_email
                    (
                     $params->{-MODIFY_EMAIL_BODY_VIEW},
                     {
                      -CGI_OBJECT => $params->{-CGI_OBJECT},
                      @_,
                     }
                    );

                my @send_params = _rearrange
                    ([
                      -MODIFY_EVENT_MAIL_SEND_PARAMS
                     ],
                     [
                     ],
                     @{$params->{-MAIL_SEND_PARAMS}}
                    );
                my $mail_send_params = shift @send_params;

                $app->sendMail
                    (
                     -MAIL_CONFIG_PARAMS => $params->{-MAIL_CONFIG_PARAMS},
                     -BODY               => $body,
                     @$mail_send_params
                    );
            }
       }
       
       
        if (!$modification_request_success) {

            $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-MODIFY_FORM_VIEW_NAME}
            );
            
            $app->setAdditionalViewDisplayParam(
                    -PARAM_NAME => '-INPUT_WIDGET_CONFIG',
                    -PARAM_VALUE => $input_widget_definitions
            );

            $app->setAdditionalViewDisplayParam(
                    -PARAM_NAME => '-INPUT_WIDGET_DISPLAY_ORDER',
                    -PARAM_VALUE => $input_widget_display_order
           );
            
            return 1;
          
        }
        elsif ($params->{-DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG}) {
           
             $app->setNextViewToDisplay(
                 -VIEW_NAME => $params->{-MODIFY_ACKNOWLEDGEMENT_VIEW_NAME}
             );
             return 1;
        
	} else {   
	        $cgi->delete('record_id');           	          
                return 2;
               
        }
             
     }
    return 0;
}
