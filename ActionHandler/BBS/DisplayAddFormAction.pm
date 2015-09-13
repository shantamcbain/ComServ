package BBS::DisplayAddFormAction;

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
        -ALLOW_ADDITIONS_FLAG,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -CGI_OBJECT,
        -INPUT_WIDGET_DEFINITIONS,
        -REQUIRE_AUTH_FOR_ADDING_FLAG,
        -VIEW_DISPLAY_PARAMS,
        -DATASOURCE_CONFIG_PARAMS,
        -KEY_FIELD,
        -SESSION_OBJECT,
        -POSTED_DATE,
    ],
            [
        -ADD_FORM_VIEW_NAME,
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
            ],
        @_
    );

    my $cgi = $params->{-CGI_OBJECT};
    my $app = $params->{-APPLICATION_OBJECT};
    my $session = $params->{-SESSION_OBJECT};
    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};
    my $posted_date = $params->{-POSTED_DATE} || 'date_time_posted';
 
    if (defined($cgi->param('display_add_form'))) {

        if (!$params->{-ALLOW_ADDITIONS_FLAG}) {
            die ('Sorry, but you are not allowed to perform additions. ' .
                 'To enable additions, you must set -ALLOW_ADDITIONS_FLAG ' .
                 'in the @ACTION_HANDLER_ACTION_PARAMS array ' .
                 'in the application executable to 1'
            );
        }

        elsif ($params->{-REQUIRE_AUTH_FOR_ADDING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                    or die("Whoopsy!  I was unable to construct the " .
                           "Authentication object in the new() method of WebDB.pm. " .
                           "Please contact the webmaster."
                    );
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
            -PARAM_VALUE => 'INPUT'
        );


        # set the user's data that we know from his profile (overridable by user)
        my $auth_firstname = $session->getAttribute(-KEY => 'auth_firstname');
        my $auth_lastname  = $session->getAttribute(-KEY => 'auth_lastname');
        my $auth_username  = $session->getAttribute(-KEY => 'auth_username');
        my $auth_email     = $session->getAttribute(-KEY => 'auth_email');
	$cgi->param('name',"$auth_username");
	$cgi->param('email',$auth_email);  
        
     

        my $record_id = $cgi->param('record_id') || '';
        if ($record_id) {

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
                my $ra_records = $app->loadData((
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
                    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG}
                ));
    
                $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-RECORDS",
                 -PARAM_VALUE => $ra_records,
                );

                
		my $rh_record = @$ra_records[0];
                my $datetime = $rh_record->{$posted_date};
                my $name = $rh_record->{'name'};
                my $forum = $rh_record->{'forum'};
                my $body = $rh_record->{'body'}||'';
                my $subject = $rh_record->{'subject'};

                $body =~ s/^([^>])/ $1/mg; # add space if a line wasn't started with '>'
                $body =~ s/^/>/mg; # add ':' for reply
#                # Quick hack
#                $body =~ s/&GT;/>/mg; 
                
                # add new line:
                $body .= "\n\n";

                $body = "On $datetime $name said:\n\n".$body;
                $cgi->param('body',$body);
                
		$cgi->param('subject',$subject);
		
                # adjust the parental connections
		$cgi->param('parent_id',$rh_record->{'record_id'});
                $cgi->param('thread_id',$rh_record->{'thread_id'});
                $cgi->param('forum',$rh_record->{'forum'});
            }
        }

        $app->setNextViewToDisplay(
            -VIEW_NAME => $params->{-ADD_FORM_VIEW_NAME}
        );

        return 1;
    }

    return 0;
}
