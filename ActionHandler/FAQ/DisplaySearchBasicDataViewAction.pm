package FAQ::DisplaySearchBasicDataViewAction;

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
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -DEFAULT_VIEW_NAME,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG,
        -SIMPLE_SEARCH_STRING,
        -SITE_NAME,
        -SESSION_OBJECT,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -APPLICATION_OBJECT
            ],
        @_
    );

    my $app     = $params->{-APPLICATION_OBJECT};
    my $cgi     = $params->{-CGI_OBJECT};
    my $session = $params->{-SESSION_OBJECT};

#    if (defined($cgi->param('display_data_view')) ||
#        defined($cgi->param('return_to_main')) ||
#        (defined $params->{-BASIC_DATA_VIEW_NAME} and defined $params->{-DEFAULT_VIEW_NAME} 
#         and $params->{-BASIC_DATA_VIEW_NAME} eq $params->{-DEFAULT_VIEW_NAME}) ) {


        if (defined($cgi->param('display_simple_search_results'))) {
            if ($params->{-REQUIRE_AUTH_FOR_SEARCHING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                 or die("Whoopsy!  I was unable to construct the " .
                        "Authentication object in the DefaultAction ActionHandler. " . 
                        "Please contact the webmaster.");
                $auth_manager->authenticate();
            }

            else {
                die('You have set -REQUIRE_AUTH_FOR_SEARCHING_FLAG to 1 ' .
                    ' in the application executable, but you have not ' .
                    ' defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                    '@ACTION_HANDLER_ACTION_PARAMS array ' .
                    'in the application executable. This action ' .
                    ' cannot procede unless you do both.'
                );
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
        
	    my $inc_category  = $cgi->param('category');
	    my $inc_keywords  = $cgi->param('search_answers');
	    my $inc_site      = $cgi-> param('require_matching_site_for_searching_flag');
	    my $inc_site_name = $cgi-> param('site_name');

        if ($inc_category eq 'null') {
                $inc_category = undef;
            };

        if ($inc_keywords eq '') {
                $inc_keywords = undef;
            };
         if ($inc_site eq '0') {
                $inc_site = undef;
            };
           
        if (defined($inc_category) && defined($inc_keywords)){
            $cgi->param(
             		-NAME => 'raw_search',
             		-VALUE => "category=='$inc_category' AND answer=='$inc_keywords'"
        	);
	  }elsif (defined($inc_category) && !defined($inc_keywords) && defined($inc_site)){
             $cgi->param(
             		-NAME => 'raw_search',
             		-VALUE => "category='$inc_category' AND site='$inc_site_name'");

        }elsif (defined($inc_category) && !defined($inc_keywords)){
             $cgi->param(
             		-NAME => 'raw_search',
             		-VALUE => "category='$inc_category'"
        	);
        }else{
             $cgi->param(
             		-NAME => 'simple_search_string',
             		-VALUE => $inc_keywords
        	);
        };
    
        if ($datasource_config_params) {
            my ($ra_records,$total_records) = $app->loadData
                (
                 -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
                 -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
                 -KEY_FIELD                   => $params->{-KEY_FIELD},
                 -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
                 -RECORD_ID                   => $cgi->param($params->{-KEY_FIELD} || 'record_id' ) || "",
                 -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
                 -SORT_FIELD1                 => $params->{-SORT_FIELD1},
                 -SORT_FIELD2                 => $params->{-SORT_FIELD2},
                 # Maximum records per page and last record on page are not passed in as 
                 # no limit of retrieve is required.
                 #-MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
                 #-LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
                 -SIMPLE_SEARCH_STRING        => $cgi->param('simple_search_string')  || "",
                 -CGI_OBJECT                  => $params->{-CGI_OBJECT},
                 -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
                 -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
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
    
            if ($total_records == 1 && ($cgi->param('display_simple_search_results') ||
                $cgi->param('submit_power_search'))) {
                $app->setNextViewToDisplay(
                   -VIEW_NAME => $params->{-BASIC_DATA_VIEW_NAME}
               );
            }

            else {
               $app->setNextViewToDisplay(
                   -VIEW_NAME => $params->{-BASIC_DATA_VIEW_NAME}
                );
            }
       }

        else {
            die('You must specify a configuration for ' .
                '-BASIC_DATASOURCE_CONFIG_PARAMS in order to ' .
                'use loadData(). You may do so in the ' .
                '@ACTION_HANDLER_ACTION_PARAMS array ' .
               'in the application executable');
        }

        return 1;
    }

    return 0;
}
