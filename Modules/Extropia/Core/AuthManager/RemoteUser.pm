#$Id: RemoteUser.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
# Copyright (C) 1996  eXtropia.com
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

package Extropia::Core::AuthManager::RemoteUser;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);

use Extropia::Core::Auth;
use Extropia::Core::AuthManager;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::AuthManager);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -AUTH_PARAMS,
       -REMOTE_USER,
       -USER_FIELDS,
       -USER_FIELD_TYPES
    ],
    [
       -AUTH_PARAMS
    ],@_);

    bless $self, ref($package) || $package;
    my $auth = $self->getAuthObject();
    $auth->setUsername($self->_getRemoteUser());

    return $self;

}

#
# isAuthenticated lets the script know if the user
# has already authenticated. For RemoteUser, the 
# user has authenticated if the REMOTE_USER env variable
# has a value.
#

sub isAuthenticated {
    my $self = shift;

    if ($ENV{REMOTE_USER}) {
        return 1;
    }
    return 0;
}

#
# Authenticate.  In AuthManager::RemoteUser
# we authenticate against a REMOTE_USER environment variable.
# This variable has been set if the Web Server has already
# figured out who the user is.
#
# We still use the AuthManager module set though
# in order to get information out of the Auth
# module about the user other than the username.
#
sub authenticate {
    my $self = shift;

#my $remote_user = $self->_getRemoteUser();
    return 1;
      #  $self->getAuthObject()->authenticate(-USERNAME => $remote_user);
  
} # end of authenticate

#
# _getRemoteUser obtains the remote user information (the user
# logged in via a server side authentication
#
sub _getRemoteUser {
    my $self = shift;

    my $remote_user = $self->{-REMOTE_USER};
    if (!$remote_user) {
        $remote_user = $ENV{REMOTE_USER};
    }
    return $remote_user;

} # end of _getRemoteUser

1;
