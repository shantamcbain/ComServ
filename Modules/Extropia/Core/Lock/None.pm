#$Id: None.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Lock::None;

#
# The Extropia::Core::Lock::None driver is supposed to be used for testing
# in environments where resource locking is not an issue or to 
# narrow down whether one of the lock drivers is causing a problem
#
# Note that we do NOT recommend using Extropia::Core::Lock::None in a 
# production environment
#
use Carp;
use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Lock;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Lock);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $lock = new Extropia::Core::Lock(-TYPE => "None");

sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([], [], @_);

    return bless $self, $package;
}

sub obtainLock {
    my $self = shift;

    return 1;

} # end of obtainLock

sub releaseLock {
    my $self = shift;

    return 1;

} # end of releaseLock

1;

