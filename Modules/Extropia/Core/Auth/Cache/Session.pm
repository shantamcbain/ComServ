#$Id: Session.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Auth::Cache::Session;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);

use Extropia::Core::Auth::Cache;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth::Cache);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# new Auth Cache Session
#
sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -SESSION_OBJECT
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -SESSION_OBJECT
    ],@_);

    return bless $self, $package;

} # end of new

#
# _getSession is a protected method used to 
# get the session object for the other methods
# to implement session specific caching behavior
#
sub _getSession {
    my $self = shift;

    return $self->{-SESSION_OBJECT};

} # end of _getSession

#
# clearCache clears the cache out...
#
sub clearCache {
    my $self = shift;

    my $session = $self->_getSession();
    my $field;
    foreach $field (@{$self->{-USER_FIELDS}}) {
        $session->removeAttribute(-KEY => $field);
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

    my $user_value = 
        $self->_getSession()->getAttribute(-KEY => $user_field);
    if ($user_field eq $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD} &&
        $user_value =~ /^#/) {
        return undef;
    }

    if (defined($user_value)) {
        $user_value =~ s/^\\#/#/;
        $user_value =~ s/^\\\\#/\\#/;
    }

    return $user_value; 

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

    if ($user_value) {
        $user_value =~ s/^\\#/\\\\#/;
        $user_value =~ s/^#/\\#/;

        $self->_getSession()->setAttribute(-KEY => $user_field, 
                                           -VALUE => $user_value);
    }

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

    my $group_list = 
        $self->_getSession()->getAttribute(
                -KEY => $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD});
# remove incomplete group list marker...
    $group_list =~ s/^#//;
    my @groups = split(",", $group_list);
    my $group;
    foreach $group (@groups) {
        if ($group_to_check eq $group) {
            return 1;
        }
    }
    if ($self->isFullGroupListCached()) {
        return 0;
    }
    return undef;

} # end of isMemberOfGroup

#
# if isFullGroupListCached is true, it means that
# all the groups have been read...
# 
sub isFullGroupListCached {
    my $self = shift;

    my $group_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $group_value = $self->_getSession()->getAttribute(-KEY => $group_field);
  
    if (!$group_value ||
        $group_value =~ /^#/) {
        return undef;
    } else {
        return 1;
    }

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

    my $group_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $group_value = $self->getUserField(-USER_FIELD => $group_field);

    $group_value .= $group;
    if ($group_value !~ /^#/) {
        $group_value = "#" . $group_value;
    }
    $self->_getSession()->setAttribute(-KEY   => $group_field,
                                       -VALUE => $group_value);

} # end of addGroupToCache

1;
