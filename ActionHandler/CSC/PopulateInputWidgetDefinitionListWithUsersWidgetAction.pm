package BugTracker::PopulateInputWidgetDefinitionListWithUsersWidgetAction;

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
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -LAST_RECORD_ON_PAGE,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SIMPLE_SEARCH_STRING,
        -SESSION_OBJECT,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -VIEW_DISPLAY_PARAMS,
        -INPUT_WIDGET_DEFINITIONS
            ],
            [
        -APPLICATION_OBJECT
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    $cgi->param(
        -NAME  => 'raw_search',
        -VALUE => "developer_status=='Requested' OR developer_status=='In-Process' OR developer_status=='Testing"
    );

    my @BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => 'mysql:host=localhost;database=forager',
	        -TABLE        => 'csc_project_tb',
	        -USERNAME     => 'forager',
	        -PASSWORD     => 'herbsrox2',
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

}

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

    my @config_params = _rearrange([
        -AUTH_USER_DATASOURCE_CONFIG_PARAMS
            ],
            [
        -AUTH_USER_DATASOURCE_CONFIG_PARAMS
            ],
        @{$params->{-DATASOURCE_CONFIG_PARAMS}}
    );

    my $datasource_config_params = shift (@config_params);

    my $ra_records = $app->loadData((
        -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
        -KEY_FIELD                   => $params->{-KEY_FIELD},
        -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
        -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
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

    my @project_code;
    foreach my $record (@$ra_records) {
        my $project_code_name = $record->{'project_code'};
        push (@project_code, $project_code_name);
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

    my @project_code_widget = (
        -DISPLAY_NAME => 'Project Code:',
        -TYPE         => 'popup_menu',
        -NAME         => 'project_code',
        -VALUES       => \@users
    );

    $$input_widget_definitions{'reporter'} = \@project_code_widget;

    my @new_value = (
        -BASIC_INPUT_WIDGET_DEFINITIONS => $input_widget_definitions
    );

    push (@input_widget_config_params, @new_value);

    $app->{-VIEW_DISPLAY_PARAMS} = $params->{-VIEW_DISPLAY_PARAMS};

    $cgi->param(
        -NAME  => 'raw_search',
        -VALUE => ""
    );

    return 2;
}