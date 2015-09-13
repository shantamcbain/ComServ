#$Id: Cache.pm,v 1.2 2002/03/06 08:11:32 janet Exp $
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

package Extropia::Core::Auth::Cache;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create Auth::Cache object
#
sub create {
    my $package = shift;
    @_ = _rearrange(
            [-TYPE],
            [-TYPE],@_);

    my $type = shift;
    my @fields = @_;

    my $cache_class = 
      Extropia::Core::Base::_getDriver("Extropia::Core::Auth::Cache", 
                                 $type) or
        confess("Extropia::Core::Auth::Cache type " . 
                    "'$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $cache_class->new(@fields);

} # end of create

#
# Interface to Auth Cache
#
#sub getUserField          {  }
#sub setCachedUserField    {  }
#sub isMemberOfGroup       {  }
#sub getGroups             {  }
#sub clearCache            {  }
#sub isFullGroupListCached {  }
#sub addGroupToCache       {  }

####################################################
#
# EXTERNAL AUTH CACHE DRIVERS
#
####################################################

#
# getGroups gets a list of groups and returns
# them...
#
sub getGroups {
    my $self = shift;

    my $group_field = 
        $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};

    my $group_value =
        $self->getUserField(-USER_FIELD => $group_field);

# This additional conditional check for defined value is added 
# to avoid uninitialized value warning.
    if(defined($group_value)){
    	return split(/,/,$group_value);
    } else {
    	return;	
    }              
} # end of getGroups

1;
