package Default::ProcessConfigurationAction;

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

#
# This action handler runs various configuration processing and other
# code that need to be executed for *all* kind of requests
#

use strict;
use Extropia::Core::Base qw(_rearrangeAsHash);
use base qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
        -INPUT_WIDGET_DEFINITIONS,
            ],
            [
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
        -INPUT_WIDGET_DEFINITIONS,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    # handle the image buttons (strip .x)
    foreach ($cgi->param()) {
        if (/^(.*)\.x$/){
            $cgi->param($1,$cgi->param($_));
            $cgi->delete("$1.y");
        }
    }

    # calculate the colspan of the details view table
    my %input_widget_definitions = (@{$params->{-INPUT_WIDGET_DEFINITIONS} || []});
    my $input_widget_display_order = $input_widget_definitions{-BASIC_INPUT_WIDGET_DISPLAY_ORDER} || [];
    my $max_input_widgets_in_row = 1;
    for (@$input_widget_display_order) {
        my $input_widgets_in_row = ref $_ eq "ARRAY" ? scalar @$_ : 1;
        $max_input_widgets_in_row = $input_widgets_in_row
            if $input_widgets_in_row > $max_input_widgets_in_row;
    }
    my $colspan = $max_input_widgets_in_row*2;
    $app->setAdditionalViewDisplayParam
        (
         -PARAM_NAME  => "-BASIC_INPUT_WIDGET_DISPLAY_COLSPAN",
         -PARAM_VALUE => $colspan,
        );

    return 2;
}

1;
__END__
