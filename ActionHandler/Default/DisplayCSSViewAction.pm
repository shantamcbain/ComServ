package Default::DisplayCSSViewAction;

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
        -CSS_VIEW_NAME,
        -CGI_OBJECT,
            ],
            [
        -APPLICATION_OBJECT,
        -CGI_OBJECT,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    if (defined($cgi->param('display_css_view'))) {
        if ($params->{-CSS_VIEW_NAME}) {
            $app->setNextViewToDisplay(
                -VIEW_NAME => $params->{-CSS_VIEW_NAME}
            );
        }
        else {
            die('You have requested a cascading style sheet by ' .
                'calling this applicaiton with display_css_view. ' .
                'However, you have not specified a value for ' .
                '-CSS_VIEW_NAME in @ACTION_HANDLER_ACTION_PARAMS ' .
                'in the applicaiton executable. Please correct ' .
                'this problem.');
        }

        return 1;
    }

    return 0;
}
