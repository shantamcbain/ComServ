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

package Extropia::Core::Auth::Cache::Composite;

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
       -LIST_OF_AUTH_CACHE_PARAMS,
       -USER_FIELDS_TO_COMPOSITE_MAPPING
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -LIST_OF_AUTH_CACHE_PARAMS
    ],
    @_);

    my %new_mapping = 
        map { ($_, 0) } @{$self->{-USER_FIELDS}};
    $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING} =
        _assignDefaults(
                $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING},
                \%new_mapping);

    bless $self, ref($package) || $package;

    $self->_init();

    return $self;
}

sub _getAuthCacheObject {
    my $self = shift;
    @_ = _rearrange([-INDEX],[-INDEX],@_);

    my $index = shift;

    my $auth_cache_object = $self->{_auth_cache_object_list}->[$index];
    if (!$auth_cache_object) {
        my @params = @{$self->{-LIST_OF_AUTH_CACHE_PARAMS}->[$index]};
        if (!@params) {
            die("No Auth::Cache Parameters Exist for $index index.");
        }

        # if we use named parameters we insert some defaults...
        if (defined($params[0]) && $params[0] =~ /^-/) {
            my %param_hash = (@params,
                -USER_FIELDS      => $self->{-USER_FIELDS},
                -USER_FIELD_TYPES => $self->{-USER_FIELD_TYPES});
            @params = %param_hash;
        }

        $auth_cache_object = Extropia::Core::Auth::Cache->create(@params);
        $self->{_auth_cache_object_list}->[$index] = $auth_cache_object;
    }
    return $auth_cache_object;
}

sub _getAuthCacheObjects {
    my $self = shift;

    my @auth_cache_objects = ();
    my $list_of_params = $self->{-LIST_OF_AUTH_CACHE_PARAMS};
    my $high_index     = @$list_of_params - 1;

    my $index;
    for $index (0..$high_index) {
        push(@auth_cache_objects,
                $self->_getAuthCacheObject(-INDEX => $index));
    }

    return \@auth_cache_objects;
}

#
# clearCache clears the cache out...
#
sub clearCache {
    my $self = shift;

    my $ac;
    foreach $ac (@{$self->_getAuthCacheObjects()}) {
        $ac->clearCache();
    }

} # clearCache

#
# getUserField gets the user field out of the
# cache. undef should be returned if the cache
# has not been filled yet.
#
sub getUserField {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD],[-USER_FIELD],@_);

    my $user_field = shift;
    my $index      = $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING}->{$user_field};
    my $ac         = $self->_getAuthCacheObject(-INDEX => $index);

    return $ac->getUserField(-USER_FIELD => $user_field);

} # end of getUserField

#
# setCachedUserField sets the user field value in the cache.
#
sub setCachedUserField {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD,-USER_VALUE],
                    [-USER_FIELD],@_);

    my $user_field = shift;
    my $user_value = shift;
    my $index      = $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING}->{$user_field};
    my $ac         = $self->_getAuthCacheObject(-INDEX => $index);

    $ac->setCachedUserField(-USER_FIELD => $user_field,
                                   -USER_VALUE => $user_value);

} # end of setCachedUserField

#
# isMemberOfGroup gets the group info out of the
# cache...
#
# if undef is returned it means the group is not
# defined yet in the cache... If 0, it means all
# the groups have been defined in the cache
# and so it definately doesn't exist.
#
sub isMemberOfGroup {
    my $self = shift;
    @_ = _rearrange([-GROUP],
                    [-GROUP],@_);

    my $group_to_check = shift;

    my $user_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $index      = $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING}->{$user_field};
    my $ac         = $self->_getAuthCacheObject(-INDEX => $index);

    return $ac->isMemberOfGroup(-GROUP => $group_to_check);

} # end of isMemberOfGroup

#
# if isFullGroupListCached is true, it means that
# all the groups have been read...
# 
sub isFullGroupListCached {
    my $self = shift;

    my $user_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $index      = $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING}->{$user_field};
    my $ac         = $self->_getAuthCacheObject(-INDEX => $index);

    return $ac->isFullGroupListCached();

} # end of isFullGroupListCached 

#
# addGroupToCache adds an individual group to 
# the cache list so another overhead does not have
# to be dealt with...
#
sub addGroupToCache {
    my $self = shift;
    @_ = _rearrange([-GROUP],
                    [-GROUP],@_);

    my $group = shift;

    my $user_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $index      = $self->{-USER_FIELDS_TO_COMPOSITE_MAPPING}->{$user_field};
    my $ac         = $self->_getAuthCacheObject(-INDEX => $index);

    return $ac->addGroupToCachek(-GROUP => $group);

} # end of addGroupToCache

1;
