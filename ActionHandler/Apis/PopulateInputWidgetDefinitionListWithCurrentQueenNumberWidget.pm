package Apis::PopulateInputWidgetDefinitionListWithCurrentQueenNumberWidget;


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

#This action handler will quriey queens table for active queens in #a given yard and return the sum to Current field in yard table.

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
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -MAX_RECORDS_PER_PAGE,
        -RECORD_ID,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SIMPLE_SEARCH_STRING,
        -SESSION_OBJECT,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -VIEW_DISPLAY_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
            ],
            [
        -APPLICATION_OBJECT,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};
    my $session = $params->{-SESSION_OBJECT};
    my $yard_code = $cgi->param('yard_code');
#$yard_code = 'Berry';
    $cgi->param(
        -NAME  => 'raw_search',
        -VALUE => "( yard_code == 'Home' )
                    
         "
    );  
 #                   yard_code == $yard_code AND
 #AND
 #                    status != 'Dead' OR 
 #                    status != 'Sold'
 
    my @config_params = _rearrange([
        -QUEENS_DATASOURCE_CONFIG_PARAMS
            ],
            [
        -QUEENS_DATASOURCE_CONFIG_PARAMS
            ],
        @{$params->{-DATASOURCE_CONFIG_PARAMS}}
    );

#define tb to pick up info from

my $GroupBoolion ;
my $user_group = $session->getAttribute(-KEY => 'auth_groups')||'normal';

if ($user_group eq 'CSC_admin'){
$GroupBoolion = 0;
}else{ 
$GroupBoolion = $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG}||1;
}

    my $datasource_config_params = shift (@config_params);

 #   my $datasource_config_params = shift @DATASOURCE_CONFIG_PARAMS;

    my $ra_records = $app->loadData((
        -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
        -KEY_FIELD                   => $params->{-KEY_FIELD},
        -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
        -SORT_DIRECTION              => 'ASC',
        -SORT_FIELD1                 => 'queen_code',
        -SORT_FIELD2                 => '',
        -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
        -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING},
        -CGI_OBJECT                  => $params->{-CGI_OBJECT},
        -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
        -MAX_RECORDS_PER_PAGE        => 200 || $cgi->param('records_per_page'),
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG =>  $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $GroupBoolion,
    ));
my $count = 0;

    my @queen_code;
    foreach my $record (@$ra_records) {
        my $username = $record->{'current'};
        push (@queen_code, $username);
        $count + 1;
    }

    my @view_display_params = @{$params->{-VIEW_DISPLAY_PARAMS}};

    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};
    my @input_widget_config_params = _rearrange([
        -BASIC_INPUT_WIDGET_DEFINITIONS,
            ],
            [
        -BASIC_INPUT_WIDGET_DEFINITIONS,
            ],
        @$input_widget_config
    );

    my $input_widget_definitions = shift (@input_widget_config_params);

    my @queen_count_widget = (
        -DISPLAY_NAME => 'Current Number of queens',
        -TYPE         => 'textfield',
        -NAME         => 'current',
        -VALUE        =>  $count   );
 
    $$input_widget_definitions{'current'} = \@queen_count_widget;

    my @new_value = (
        -BASIC_INPUT_WIDGET_DEFINITIONS => $input_widget_definitions
    );

    push (@input_widget_config_params, @new_value);

    $app->{-VIEW_DISPLAY_PARAMS}= $params->{-VIEW_DISPLAY_PARAMS};    

    $cgi->param(
        -NAME  => 'raw_search',
        -VALUE => ""
    );

    return 2;
}
