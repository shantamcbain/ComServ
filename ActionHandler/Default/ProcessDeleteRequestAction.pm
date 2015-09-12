package Default::ProcessDeleteRequestAction;

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
        -ALLOW_DELETIONS_FLAG,
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -DELETE_ACKNOWLEDGEMENT_VIEW_NAME,
        -DELETE_FORM_VIEW_NAME,
        -DELETE_FILE_FIELD_LIST,
        -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG,
        -ENABLE_SORTING_FLAG,
        -DELETE_EMAIL_BODY_VIEW,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -MAIL_CONFIG_PARAMS,
        -MAIL_SEND_PARAMS,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_DELETING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SEND_EMAIL_ON_DELETE_FLAG,
        -SESSION_OBJECT,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -UPLOAD_MANAGER_CONFIG_PARAMS,
        -VIEW_DISPLAY_PARAMS,
        -VIEW_LOADER,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
        -MAIL_SEND_PARAMS,
            ],
        @_
    );

    my $app                    = $params->{-APPLICATION_OBJECT};;
    my $session                = $params->{-SESSION_OBJECT};
    my $cgi                    = $params->{-CGI_OBJECT};
    my $data_handler_manager_config_params = $params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS};

    if (defined($cgi->param('submit_delete_record')) &&
        $params->{-ALLOW_DELETIONS_FLAG} ) {

#        if (!$params->{-ALLOW_DELETIONS_FLAG}) {
#            die ('Sorry, but you are not allowed to perform additions. ' .
#                 'To enable additions, you must set -ALLOW_DELETIONS_FLAG ' .
#                 'in the @ACTION_HANDLER_ACTION_PARAMS array ' .
#                 'in the application executable to 1'
#            );
#        }

        if ($params->{-REQUIRE_AUTH_FOR_DELETING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                    or die("Whoopsy!  I was unable to construct the " .
                           "Authentication object. " .
                           "Please contact the webmaster.");
                $auth_manager->authenticate();
            }
            else {
                die('You have set -REQUIRE_AUTH_FOR_DELETING_FLAG to 1 ' .
                    ' in the application executable, but you have not ' .
                    ' defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                    '@ACTION_HANDLER_ACTION_PARAMS array ' .
                    'in the application executable. This action ' .
                    ' cannot procede unless you do both.'
                );
            }
        }

        my $log_object;
        if ($params->{-LOG_CONFIG_PARAMS}) {
            $log_object = Extropia::Core::Log->create(@{$params->{-LOG_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Log object. Please " .
                       "contact the webmaster.");
        }

        my @dhm_config_params = _rearrange([
            -DELETE_FORM_DHM_CONFIG_PARAMS
               ],
               [
               ],
            @{$params->{-DATA_HANDLER_MANAGER_CONFIG_PARAMS}}
        );

        my $delete_form_dhm_config_params = shift (@dhm_config_params);

        if ($delete_form_dhm_config_params) {
            my $data_handler_success = $app->handleIncomingData
                (
                 -CGI_OBJECT                 => $cgi,
                 -LOG_OBJECT                 => $log_object,
                 -DATA_HANDLER_CONFIG_PARAMS => $delete_form_dhm_config_params
                 -ACTION_HANDLER_PLUGINS     => $params->{-ACTION_HANDLER_PLUGINS},
                );

            if (!$data_handler_success) {
                $app->setNextViewToDisplay(
                    -VIEW_NAME => $params->{-DELETE_FORM_VIEW_NAME}
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

        my $deletion_request_success = $app->deleteRecord((
            -CGI_OBJECT               => $cgi,
            -SESSION_OBJECT           => $params->{-SESSION_OBJECT},
            -KEY_FIELD                => $params->{-KEY_FIELD},
            -LOG_OBJECT               => $log_object,
            -DATASOURCE_CONFIG_PARAMS => $datasource_config_params,
            -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG},
            -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG},
            -DELETE_FILE_FIELD_LIST   => $params->{-DELETE_FILE_FIELD_LIST},
            -UPLOAD_MANAGER_CONFIG_PARAMS => $params->{-UPLOAD_MANAGER_CONFIG_PARAMS}
        ));

        if ($deletion_request_success) {

            # don't propogate the id, its gone now!
            $cgi->delete('record_id');

            if ($params->{-SEND_EMAIL_ON_DELETE_FLAG}) {
                my @send_params = _rearrange([
                    -DELETE_EVENT_MAIL_SEND_PARAMS
                        ],
                        [
                        ],
                    @{$params->{-MAIL_SEND_PARAMS}}
                );

                my $mail_send_params = shift (@send_params);

		my $view_loader = $params->{-VIEW_LOADER};
		my $body = $view_loader->process_email
		    (
		    	$params->{-DELETE_EMAIL_BODY_VIEW},
		    	{
		    		-CGI_OBJECT => $params->{-CGI_OBJECT},
		    		@_,
		    	}
		    );
		
                $app->sendMail((
                    -MAIL_CONFIG_PARAMS => $params->{-MAIL_CONFIG_PARAMS},
                    -BODY               => $body,
                    @$mail_send_params
                ));
            }
        }


        if (!$deletion_request_success) {
            $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-DELETE_FORM_VIEW_NAME}
            );

            my ($total_records,$ra_records) = $app->loadData
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

            $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-TOTAL_RECORDS",
                 -PARAM_VALUE => $total_records,
                );

            return 1;
        }

        elsif ($params->{-DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG}) {
            $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-DELETE_ACKNOWLEDGEMENT_VIEW_NAME}
            );
            return 1;
        }

        else {
            return 2;
        }
    }

    return 0;
}
