package Default::SimpleForm::DisplaySimpleFormAction;

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
        -FORM_VIEW_NAME,
        -REQUIRE_AUTH_FOR_VIEWING_FORM_FLAG,
        -INPUT_WIDGET_DEFINITIONS
            ],
            [
        -APPLICATION_OBJECT,
        -FORM_VIEW_NAME,
            ],
        @_
    );
    
    my $app = $params->{-APPLICATION_OBJECT};
    my $input_widget_config = $params->{-INPUT_WIDGET_DEFINITIONS};
    
    my $auth_manager;
    if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
        $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
            or die("Whoopsy!  I was unable to construct the " .
                   "Authentication object. " .
                   "Please contact the webmaster.");
    }

    if ($auth_manager && $params->{-REQUIRE_AUTH_FOR_VIEWING_FORM_FLAG}) {
        $auth_manager->authenticate();
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

    $app->setNextViewToDisplay(
        -VIEW_NAME => $params->{-FORM_VIEW_NAME}
    );
    return 1;
}
