package Default::PerformGracefulSessionTimeoutAction;

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
        -SESSION_OBJECT,
        -SESSION_TIMEOUT_VIEW_NAME
            ],
            [
        -APPLICATION_OBJECT,
            ],
        @_
    );

    my $session = $params->{'-SESSION_OBJECT'};
    my $app     = $params->{'-APPLICATION_OBJECT'};

    if (defined ($session) && $session->getErrorCount()) {
       $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-VIEW_NAME",
            -PARAM_VALUE => $params->{'-SESSION_TIMEOUT_VIEW_NAME'}
        );

        return 1;
    }
	
    return 0;
}
