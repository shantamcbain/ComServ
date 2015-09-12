#$Id: Composite.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Auth::Composite;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Auth;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -LIST_OF_AUTH_PARAMS,
       -AUTHENTICATE_MAPPING,
       -REGISTER_MAPPING,
       -SEARCH_MAPPING, 
       -USER_FIELDS_TO_COMPOSITE_AUTH_MAPPING,
       -AUTH_CACHE_PARAMS
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -LIST_OF_AUTH_PARAMS
    ],
    @_);

    $self = _assignDefaults($self,
                   {
                    -AUTHENTICATE_MAPPING => 0,
                    -REGISTER_MAPPING     => 0,
                    -SEARCH_MAPPING       => 0,
                    -AUTH_CACHE_PARAMS  => [-TYPE => 'None'],
                   });

    my %new_mapping = 
        map { ($_, 0) } @{$self->{-USER_FIELDS}};
    $self->{-USER_FIELDS_TO_COMPOSITE_AUTH_MAPPING} =
        _assignDefaults(
                $self->{-USER_FIELDS_TO_COMPOSITE_AUTH_MAPPING},
                \%new_mapping);

    bless $self, ref($package) || $package;

    $self->_init();

    return $self;
}

sub _retrieveAuthDataStore {
    my $self = shift;
# nothing here...
};

sub _getAuthObject {
    my $self = shift;
    @_ = _rearrange([-INDEX],[-INDEX],@_);

    my $index = shift;

    my $auth_object = $self->{_auth_object_list}->[$index];
    if (!$auth_object) {
        my @params = @{$self->{-LIST_OF_AUTH_PARAMS}->[$index]};
        if (!@params) {
            die("No Auth Parameters Exist for $index index.");
        }

        # if we use named parameters we insert some defaults...
        if (defined($params[0]) && $params[0] =~ /^-/) {
            my %param_hash = (@params,
                -USER_FIELDS      => $self->{-USER_FIELDS},
                -USER_FIELD_TYPES => $self->{-USER_FIELD_TYPES});
            @params = %param_hash;
        }

        $auth_object = Extropia::Core::Auth->create(@params);
        $self->{_auth_object_list}->[$index] = $auth_object;
        $auth_object->{_username_parameter} = $self->{_username_parameter};
    }
    return $auth_object;
}

# In the context of the Auth Module
# authenticate takes a username and password and checks to
# see if a problem has occurred
# 
# If the logon is successful, then that information is
# cached for further querying by the AuthManager object
#
# If the logon fails it is either because the username does
# not match an existing one or because the password failed to match
# 
# If password is undef, then it is assumed that the authentication
# is merely trying to get the user information for passing back to
# the authentication manager which may be managing security issues
#
# returns a true if successful, false if not.
# 

sub authenticate {
    my $self = shift;

    my $index = $self->{-AUTHENTICATE_MAPPING};
    my $auth  = $self->_getAuthObject(-INDEX => $index);

    my $status = $auth->authenticate(@_);

    if (!$status) {
        my @error_list = $auth->getErrors();
        my $error;
        foreach $error (@error_list) {
            $self->addError($error);
        }
        return undef;
    }
    $self->{_username_parameter} = $auth->{_username_parameter};
    return 1;

} # end of authenticate

#
# _getRawUserField is a method that is called
# from getUserField(). It performs the raw work
# of getting to the authentication data lookup (eg DataSource
# or LDAP).
#
sub _getRawUserField {
    my $self = shift;
    @_ = _rearrange(
              [-USER_FIELD],[-USER_FIELD],@_);

    # local params
    my $user_field = shift;
    
    my $field_mapping = $self->{-USER_FIELDS_TO_COMPOSITE_AUTH_MAPPING};
    my $index = $field_mapping->{$user_field};

# get _username_parameter if none exists... it is possible that an
# old session may have cached the username previously without
# having explicitly authenticated...
    if (!$self->{_username_parameter}) {
        my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
        $self->{_username_parameter} = 
            $self->getUserField($username_field);
    }
    my $auth = $self->_getAuthObject(-INDEX => $index);

    return $auth->getUserField(-USER_FIELD => $user_field);

} # end of _getRawUserField

#
# search
#
# search takes a user field and a value to search on
# and returns a list of usernames that satisfy this search
#
sub search {
    my $self = shift;

    my $index = $self->{-LIST_OF_AUTH_PARAMS};
    my $auth  = $self->_getAuthObject(-INDEX => $index);

    my @user_list = $auth->search(@_);

    if (!@user_list) {
        my @error_list = $auth->getErrors();
        my $error;
        foreach $error (@error_list) {
            $self->addError($error);
        }
        return undef;
    }
    return @user_list;

} # end of search

#
# register
#
# Allows a user to register into the authenticaton source...
#

sub register {
    my $self = shift;

    my $index = $self->{-LIST_OF_AUTH_PARAMS};
    my $auth  = $self->_getAuthObject(-INDEX => $index);

    my $status = $auth->register(@_);

    if (!$status) {
        my @error_list = $auth->getErrors();
        my $error;
        foreach $error (@error_list) {
            $self->addError($error);
        }
        return undef;
    }
    return 1;

} # end of register

1;
