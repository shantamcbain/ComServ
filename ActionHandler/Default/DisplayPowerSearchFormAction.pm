package Default::DisplayPowerSearchFormAction;

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
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -CGI_OBJECT,
        -POWER_SEARCH_VIEW_NAME,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -INPUT_WIDGET_DEFINITIONS
            ],
            [
        -APPLICATION_OBJECT,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    if (defined($cgi->param('display_power_search_form'))) {
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

#
#        foreach my $i (@$input_widget_display_order) {
#            $i = [ $i ] if ref $widget ne "ARRAY";
#            foreach my $j (@$i) {
#                my $values_ref = $input_widget_definitions->{$j};
#                my (@values) = _rearrange([
#                    -DISPLAY_NAME,
#                    -TYPE,
#                    -DESCRIPTION_CELL_COLSPAN,
#                    -INPUT_CELL_COLSPAN,
#                        ],
#                        [
#                    -DISPLAY_NAME,
#                    -TYPE
#                        ],
#                    @$values_ref
#                );
#
#                my $display_name             = shift @values || '';
#                my $type                     = shift @values || '';
#                my $description_cell_colspan = shift @values || "1";
#                my $input_cell_colspan       = shift @values || "1";
#
#                %search_widgets{$j} =  
#        }

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

        my $input_widget_definitions = shift (@input_widget_config_params);
        my $input_widget_display_order = shift (@input_widget_config_params);
        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME => '-INPUT_WIDGET_CONFIG',
            -PARAM_VALUE => $input_widget_definitions
        );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME => '-INPUT_WIDGET_DISPLAY_ORDER',
            -PARAM_VALUE => $input_widget_display_order
        );

        $app->setNextViewToDisplay(
            -VIEW_NAME => $params->{-POWER_SEARCH_VIEW_NAME}
        );

        return 1;
    }
    return 0;
}
