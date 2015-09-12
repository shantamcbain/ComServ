package Default::DisplayDeleteFormAction;

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
        -INPUT_WIDGET_DEFINITIONS,
        -DELETE_FORM_VIEW_NAME,
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
            ],
            [
        -APPLICATION_OBJECT,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -INPUT_WIDGET_DEFINITIONS,
        -DELETE_FORM_VIEW_NAME,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};
    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};

    if (defined($cgi->param('display_delete_form'))) {
        if (!$params->{-ALLOW_DELETIONS_FLAG}) {
            die ('Sorry, but you are not allowed to perform additions. ' .
                 'To enable additions, you must set -ALLOW_DELETIONS_FLAG ' .
                 'in the @ACTION_HANDLER_ACTION_PARAMS array ' .
                 'in the application executable to 1'
            );
        }

        elsif ($params->{-REQUIRE_AUTH_FOR_DELETING_FLAG}) {
            if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
                my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object." .
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

        $app->setNextViewDisplay(
            -VIEW_NAME => $params->{-DELETE_FORM_VIEW_NAME}
        );

        return 1;
    }

    return 0;
}
