package Default::PerformLogonAction;

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
        -AUTH_MANAGER_CONFIG_PARAMS,
        -APPLICATION_OBJECT,
        -CGI_OBJECT
            ],
            [
        -APPLICATION_OBJECT,
        -CGI_OBJECT
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};

    if ($cgi->param('submit_logon')) {
        if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
            my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object. " .
                       "Please contact the webmaster.");
            $auth_manager->authenticate();
        }
        else {
            die('You have requested to logon using submit_logon ' .
                'However, you have not ' .
                'defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                '@ACTION_HANDLER_ACTION_PARAMS array ' .
                'in the application executable. This action ' .
                'cannot procede unless you do so.'
            );
        }
    }
    return 2;
}
