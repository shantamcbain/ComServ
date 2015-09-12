#$Id: AuthManager.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::AuthManager;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    @_ = _rearrange(
            [-TYPE],
             [-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $auth_class = 
      Extropia::Core::Base::_getDriver("Extropia::Core::AuthManager", 
                                 $type) or
        confess("Extropia::Core::AuthManager type " . 
                    "'$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $auth_class->new(@fields);

}

#######################################################
# Base object methods for use by objects that inherit
# from the base AuthManager.pm file.
#######################################################

#
# logoff simply logs the user off... most auth managers
# do not have a concept of logging off so the default
# implementation is blank. Basically this reverses
# the process of authentication...
#
sub logoff {
    my $self = shift;
    return 1;
} # end of logoff

#
# getAuthObject returns the auth object
# associated with the AuthManager.
#
# If none is associated, then the auth object
# is created
#
sub getAuthObject {
    my $self = shift;

    if (!$self->{-AUTH_OBJECT}) {
        my @params = @{$self->{-AUTH_PARAMS}};

        # if we use named parameters we insert some defaults...
        if (defined($params[0]) && $params[0] =~ /^-/) {
            my %param_hash = (@params,
                -USER_FIELDS      => $self->{-USER_FIELDS},
                -USER_FIELD_TYPES => $self->{-USER_FIELD_TYPES});
            @params = %param_hash;
        }

        $self->{-AUTH_OBJECT} =
            Extropia::Core::Auth->create(@params);
    }
    return $self->{-AUTH_OBJECT};

} # end of getAuthObject

#
# Manually refresh authentication state... generally
# will force an already authenticated object to redownload
# it's information into a cache or at least clear it's cache
# of info.
#
sub refresh {
    my $self = shift;

    my $auth = $self->getAuthObject();

    my $username = $auth->getUserField(-USER_FIELD => 
                       $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD});
    if ($username) {
        $auth->setUsername(
            -USERNAME => $username
        );
    }

    $self->getAuthObject()->refresh();

} # end of refresh

#
# getGroups will get the groups from the auth module...
#
sub getGroups {
    my $self = shift;

    return
      $self->getAuthObject()->getGroups();

} # end of getGroups

#
# isMemberOfGroup will check if we are a member of a group
# this method passes through to the auth object.
#
sub isMemberOfGroup {
    my $self = shift;
    @_ = _rearrange([-GROUP],[-GROUP],@_);

    my $group_to_check = shift;

    return $self->getAuthObject()->isMemberOfGroup($group_to_check);

} # end of isMemberOfGroup

#
# getUserField gets the value of a user field. It passes through
# to the authentication module.
#
sub getUserField {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD],[-USER_FIELD],@_);

    my $user_field = shift;

    return $self->getAuthObject()->getUserField(-USER_FIELD =>
                                               $user_field);

} # end of getUserField

#
# getUserFields simply enumerates a list of valid user fields
# for the client...
#
sub getUserFields {
    my $self = shift;

    return (@{$self->{-USER_FIELDS}});
} # end of getUserFields

#
# setCachedUserField passes through to the auth module which selectively
# makes a decision whether to update the permenent datatore, the
# auth cache, none, or both.
#
# Bottomline is that the authmanager does not have to know the
# implementation of this.
#
sub setCachedUserField {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD, -USER_VALUE],
                    [-USER_FIELD, -USER_VALUE], @_);

    my $user_field = shift;
    my $user_value = shift;

    $self->getAuthObject()->setCachedUserField(-USER_FIELD => $user_field,
                                          -USER_VALUE => $user_value);
} # end of setCachedUserField

# 
# isAuthenticated lets the programmer know if the 
# user has already logged on 
#
# Most drivers have already logged a user on, so
# no extra auth step is truly needed.
#

sub isAuthenticated {
    my $self = shift;

    return 1;

}

1;
