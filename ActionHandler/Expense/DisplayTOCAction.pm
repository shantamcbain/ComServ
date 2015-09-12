package Expense::DisplayTOCAction;

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
        -TOC_VIEW_NAME,
        -CGI_OBJECT,
        -KEY_FIELD,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -INPUT_WIDGET_DEFINITIONS
            ],
            [
        -APPLICATION_OBJECT,
        -TOC_VIEW_NAME,
        -CGI_OBJECT,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    if ($cgi->param('display_toc_view')) {
        my $auth_manager;
        if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
            $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object. " .
                       "Please contact the webmaster.");
        }

        if ($params->{-REQUIRE_AUTH_FOR_SEARCHING_FLAG}) {
            if ($auth_manager) {
                $auth_manager->authenticate();
            }
        }
        
        $app->setNextViewToDisplay(
            -VIEW_NAME => $cgi->param('view') ||
                           $params->{-TOC_VIEW_NAME}
        );

# Below are the codes that are shifted from the view to action handler
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
            -PARAM_NAME  => "-INPUT_WIDGET_CONFIG",
            -PARAM_VALUE => $input_widget_definitions
        );

	$app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-INPUT_WIDGET_DISPLAY_ORDER",
            -PARAM_VALUE => $input_widget_display_order
        );

         
   	my (@project_types) = _rearrange([
        	-TYPE,
        	-NAME,
        	-VALUES,
            ],
            [
            ],
        	@{$input_widget_definitions->{'project_code'}}
        );

       my $project_type = shift (@project_types);	
       my $project_name = shift (@project_types);
       my $project_value = shift (@project_types);
       
       my %project = (
       		'type'	  => $project_type,
       		'name'	  => $project_name,
       		);
      
       $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-PROJECT",
            -PARAM_VALUE => \%project
        );
      
       $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-PROJECT_VALUE",
            -PARAM_VALUE => $project_value
        );
        
          
       my (@expense_types) = _rearrange([
        	-TYPE,
        	-NAME,
        	-VALUES
            ],
            [
            ],
       		 @{$input_widget_definitions->{'expense_type'}}
       );

       my $expense_type = shift (@expense_types);
       my $expense_name = shift (@expense_types);	
       my $expense_value = shift (@expense_types);		
  
       my %expense = (
       		'type' => $expense_type,
       		'name' => $expense_name,
       		);
  
       $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-EXPENSE",
            -PARAM_VALUE => \%expense
        );
     
       $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-EXPENSE_VALUE",
            -PARAM_VALUE => $expense_value
        );
     
     
# End of code shifted from view     

        return 1;
    }
    return 2;
}
