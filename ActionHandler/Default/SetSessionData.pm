package Default::SetSessionData;

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
use Extropia::Core::Base qw(_rearrangeAsHash);
use Extropia::Core::Action;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash
        (
         [
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
         ],
         [
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
         ],
         @_,
        );

    my $session  = $params->{-SESSION_OBJECT};

    if (!$session) {
        return 0;
    }

    my $app      = $params->{-APPLICATION_OBJECT};

    $app->setAdditionalViewDisplayParam
        (
         -PARAM_NAME => '-SESSION_ID',
         -PARAM_VALUE => $session->getId() || '',
        );

    $app->setAdditionalViewDisplayParam
        (
         -PARAM_NAME  => "-AUTH_USERNAME",
         -PARAM_VALUE => $session->getAttribute(-KEY => 'auth_username') || '',
        );

    $app->setAdditionalViewDisplayParam
        (
         -PARAM_NAME  => "-AUTH_GROUPS",
         -PARAM_VALUE => $session->getAttribute(-KEY => 'auth_groups') || '',
        );

#    print STDERR "session id: ",$session->getId(),"\n";

    return 2;
}
