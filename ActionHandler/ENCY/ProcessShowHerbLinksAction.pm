package ENCY::ProcessShowHerbLinksAction;

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
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -URL_DATA_HANDLER_MANAGER_CONFIG_PARAMS,
        -SESSION_OBJECT,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2
            ],
            [
        -APPLICATION_OBJECT
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    my $auth_manager;
    if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
        $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
            or die("Whoopsy!  I was unable to construct the " .
                   "Authentication object in the DefaultAction ActionHandler. " .
                   "Please contact the webmaster.");
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


    if (defined($cgi->param('show_herb_urls'))) {
        if ($params->{-REQUIRE_AUTH_FOR_SEARCHING_FLAG}) {
            if ($auth_manager) {
                $auth_manager->authenticate();
            }
        }
        my $viewname = $cgi->param('view') ||'BasicDataView';
 
       $app->setNextViewToDisplay(
				  -VIEW_NAME => $viewname
        );


        my $username = $cgi->param('user');
        my $searchvalue1 = $cgi->param('search1')||'*';
        my $searchfield = $cgi->param('searchfield')||'fname';
        my $display_field2 = $cgi->param('display_2');
        my $visibility = $cgi->param('visibility')||'priv';
 
        $cgi->param(
            -NAME  => 'raw_search',
            -VALUE => "$searchfield == $searchvalue1 "
        );

        my ($ra_records,$total_records) = $app->loadData
            (
             -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
             -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
             -KEY_FIELD                   => $params->{-KEY_FIELD},
             -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
	     -SORT_DIRECTION              => $cgi->param('sort_direction')||"ASC",
	     -RECORD_ID                   => $cgi->param('record_id') || "",
	     -SORT_FIELD1                 => $cgi->param('sort_field1')|| $params->{-SORT_FIELD1},
	     -SORT_FIELD2                 => $cgi->param('sort_field2')|| $params->{-SORT_FIELD2},
             -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
             -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
             -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING},
             -CGI_OBJECT                  => $params->{-CGI_OBJECT},
             -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
             -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
             -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG}
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

    return 2;
}
