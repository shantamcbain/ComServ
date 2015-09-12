#$Id: Auth.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Auth;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _assignDefaults);
use Extropia::Core::Auth::Cache;

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

    my $auth_class = Extropia::Core::Base::_getDriver("Extropia::Core::Auth", $type) or
        Carp::croak("Extropia::Core::Auth type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $auth_class->new(@fields);

} # end of create

#
# Interface to Auth
#
#sub authenticate        {  }
#sub register            {  }
#sub search              {  }
#sub getAuthCacheObject  {  }
#sub getUserField        {  }
#sub setCachedUserField        {  }
#sub isMemberOfGroup     {  }
#sub getGroups           {  }
#sub refresh             {  }
#sub setUsername         {  }

####################################################
#
# EXTERNAL AUTH DRIVERS
#
####################################################

#
# getAuthCacheObject gets an auth cache
# object if one exits. If not, an auth cache
# object is created an stored in the auth object
# for future use.
#
sub getAuthCacheObject {
    my $self = shift;

    if (!$self->{-AUTH_CACHE_OBJECT}) {
        my @params = @{$self->{-AUTH_CACHE_PARAMS}};

        # if we use named parameters we insert some defaults...
        if (defined($params[0]) && $params[0] =~ /^-/) {
            push (@params,
                -USER_FIELDS      => $self->{-USER_FIELDS},
                -USER_FIELD_TYPES => $self->{-USER_FIELD_TYPES});
        } 
      
        $self->{-AUTH_CACHE_OBJECT} = 
        Extropia::Core::Auth::Cache->create(@params);
    }
    return $self->{-AUTH_CACHE_OBJECT};

} # end of getAuthCacheObject

#
# getUserField
#
# Returns information about the user...
# generally called as a passthrough to the authentication manager
#
# Note: the cache is used to obtain data in case obtaining it
# from the raw data source is expensive.
#
# The algorithm is this...
# 1. First check the cache. If the cache has the info then
#    we can assume all is right with the world and hand back
#    the cached result.
#
# 2. Second, if there is no cache info, then look up the info
#    and submit it to the cache.
#
# Exception: the Auth module reserves the right to prepopulate
# the cache for efficiency. For example, in the case of the
#
# The cache should also reserve the right to be partially populated.
# for example, certain operations may be hierarchical and cause
# multiple lookups. For example, looking up all the groups associated
# with a user may result in multiple calls. Group is the only field
# that benefits from this because of the isMemberOfGroup function.
#
# Instead we might wish to read in only one group at a time...
# and slowly populate the cache.
#
sub getUserField {
    my $self = shift;
    @_ = _rearrange(
          [-USER_FIELD],[-USER_FIELD],@_);

    # local params
    my $user_field = shift;

    if ($user_field eq $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD}) {
        return undef;
    }

    my $auth_cache = $self->getAuthCacheObject();
    my $user_value = $auth_cache->getUserField(-USER_FIELD => $user_field);

    if (!$user_value) {
        $user_value = $self->_getRawUserField(-USER_FIELD => $user_field);
        $auth_cache->setCachedUserField(-USER_FIELD => $user_field,
                                  -USER_VALUE => $user_value);
    }
    return $user_value;

} # end of getUserField

#
# setCachedUserField sets the user field... an authentication
# module should be able to set its own logic as to whether the
# user field is set directly in the auth or is done as a pass
# through to the cache.
#
# Note: the user is NOT guaranteed to have setCachedUserField actually
# do anything. It's a convenience for auth modules that may support it.
#
# The recommended minimum implementation is to pass through the
# value to the underlying cache.
#
sub setCachedUserField {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD, -USER_VALUE],
                    [-USER_FIELD, -USER_VALUE],@_);

    my $user_field = shift;
    my $user_value = shift;

    $self->getAuthCacheObject()->setCachedUserField(-USER_FIELD => $user_field,
                                               -USER_VALUE => $user_value);

} # end of setCachedUserField

#
# isMemberOfGroup  checks the groups in the cache first...
# if the group has not been seen in the cache before
# then it looks it up in the raw low level interface to the
# auth module
#
sub isMemberOfGroup {
    my $self = shift;
    @_ = _rearrange([-GROUP],[-GROUP],@_);

    my $group_to_check = shift;

    my $auth_cache = $self->getAuthCacheObject();
    my $is_in_group = 
    $auth_cache->isMemberOfGroup(-GROUP => $group_to_check);

    if (!defined($is_in_group)) {
        $is_in_group = $self->_rawIsMemberOfGroup(-GROUP => $group_to_check);
        if ($is_in_group) {
            $auth_cache->addGroupToCache(-GROUP => $group_to_check);
        }
    }

    return $is_in_group;

} # end of isMemberOfGroup

#
# getGroups gets a list of groups and returns
# them...
#
sub getGroups {
    my $self = shift;

    my $group_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};

    my @groups =
    $self->getAuthCacheObject()->getGroups();

    if (!@groups) {
        my $group_value = $self->_getRawUserField(-USER_FIELD => $group_field);
        @groups =  split(/,/,$group_value);
    }
    return @groups;

} # end of getGroups

#
# The default implementation of refresh simply
# clears the AuthCache. At this point any subsequent
# call to an authentication routine will require
# a call to the auth object itself to get to its own
# date.
#
sub refresh {
    my $self = shift;

    $self->getAuthCacheObject()->clearCache();

} # end of refresh

#
# setUsername primes the authentication module
# for automatically looking up information based
# on a previously known username.
#
sub setUsername {
    my $self = shift;
    @_ = _rearrange([-USERNAME],[-USERNAME],@_);

    my $username = shift;

    $self->{_username_parameter} = {-USERNAME => $username};

} # end of setUsername

# 
# _rawIsMemberOfGroup implements actually getting
# the group information from the datasource...
#
# Luckily for most Auth modules, we just have to
# call the getGroups function to actually check if
# we are a member of the group.
#
# For another type of Auth module such as LDAP,
# we might decide to do some performance enhancements
# so that only the individual group is looked up 
# at a time.
#
sub _rawIsMemberOfGroup {
    my $self = shift;
    @_ = _rearrange([-GROUP],[-GROUP],@_);

    my $group_to_check = shift;

    my @groups = $self->getGroups();
    my $group;
    foreach $group (@groups) {
        if ($group_to_check eq $group) {
            return 1;
        }
    }

return 0;

} # end of _rawIsMemberOfGroup

# eventually will move this out to Auth.pm
sub _init {
    my $self = shift;

    $self = _assignDefaults($self,
                {-USERNAME_NOT_FOUND_ERROR =>
                   "Username or password did not match existing entries.",
                 -PASSWORD_NOT_MATCHED_ERROR =>
                   "Username or password did not match existing entries.",
                 -DUPLICATE_USERNAME_ERROR =>
                   "The Username: %s already exists in the user database."
                });

} # end of _init

sub retrieveAuthDataStore {
    my $self = shift;
    @_ = _rearrange([-USERNAME],[],@_);

    my $username = shift;

    if (!defined($username)) {
        if (defined($self->{_username_parameter})) {
            $username = $self->{_username_parameter};
        } else {
            confess("retrieveAuthDataStore() did not have a username.");
        }
    } 

    my $data_store =  
         $self->_retrieveAuthDataStore(-USERNAME => $username);
    $self->{_username_parameter} = $username;
    return $data_store;
}

1;
