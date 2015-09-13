package Default::DefaultAction;

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
        -SESSION_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG,
        -LAST_RECORD_ON_PAGE,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -INPUT_WIDGET_DEFINITIONS,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -APPLICATION_OBJECT,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
            ],
        @_
    );

    my $app     = $params->{-APPLICATION_OBJECT};
    my $cgi     = $params->{-CGI_OBJECT};
 
    if($params->{-INPUT_WIDGET_DEFINITIONS}) {
        my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};
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
   }	


    if ($params->{-REQUIRE_AUTH_FOR_SEARCHING_FLAG}) {
        if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
            my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object. " .
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

    $app->setNextViewToDisplay(
        -VIEW_NAME => $cgi->param('view') || $params->{-BASIC_DATA_VIEW_NAME}
    );

    if ($params->{'-DATASOURCE_CONFIG_PARAMS'}) {
        my @config_params = _rearrange([
            -BASIC_DATASOURCE_CONFIG_PARAMS
                ],
                [
                ],
            @{$params->{'-DATASOURCE_CONFIG_PARAMS'}}
        );

        my $datasource_config_params = shift (@config_params);

        if ($datasource_config_params) {
            my $key_field_value = $cgi->param($params->{-KEY_FIELD} || 'record_id' ) || "" ;   
            my ($ra_records,$total_records) = $app->loadData
                (
                 -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
                 -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
                 -KEY_FIELD                   => $params->{-KEY_FIELD},
                 -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
                 -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
                 -RECORD_ID                   => $key_field_value,                 
                 -SORT_FIELD1                 => $params->{-SORT_FIELD1},
                 -SORT_FIELD2                 => $params->{-SORT_FIELD2},
                 -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
                 -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
                 -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING}, 
                 -CGI_OBJECT                  => $params->{-CGI_OBJECT},
                 -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
                 -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
                 -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG},
                 -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
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

             $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-RECORD_ID",
                 -PARAM_VALUE => $key_field_value,
                );
        }

        else {
            die('You must specify a configuration for ' .
                '-BASIC_DATASOURCE_CONFIG_PARAMS in order to ' .
                'use loadData(). You may do so in the ' .
                '@ACTION_HANDLER_ACTION_PARAMS array ' .
                'in the application executable');
        }
    }    
    return 1;
}
