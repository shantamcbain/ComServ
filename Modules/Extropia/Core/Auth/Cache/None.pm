#$Id: None.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Auth::Cache::None;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);

use Extropia::Core::Auth;
use Extropia::Core::Auth::Cache;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth::Cache);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# new Auth Cache None
#
sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
    ],@_);

    return bless $self, $package;

} # end of new

#
# clearCache clears the cache out...
#
sub clearCache {
    my $self = shift;

} # clearCache

#
# getUserField gets the user field out of the
# cache. undef should be returned if the cache
# has not been filled yet.
#
sub getUserField {
    my $self = shift;

    return undef;

} # end of getUserField

#
# setCachedUserField sets the user field value in the cache.
#
sub setCachedUserField {
    my $self = shift;

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

    return undef;

} # end of isMemberOfGroup

#
# if isFullGroupListCached is true, it means that
# all the groups have been read...
# 
sub isFullGroupListCached {
    my $self = shift;

    return 0;

} # end of isFullGroupListCached 

#
# addGroupToCache adds an individual group to 
# the cache list so another overhead does not have
# to be dealt with...
#
sub addGroupToCache {
    my $self = shift;

} # end of addGroupToCache

1;

