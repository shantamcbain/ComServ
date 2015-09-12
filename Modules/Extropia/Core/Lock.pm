# $Id: Lock.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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
#
# Implements both flock and file based locking depending on the system 
# you have.  For file based locking, the O'Reilly Perl Cookbook's approach
# to locking over a network using a mkdir command as an atomic operation
# is used for safety.  Checking the existence of a file and then creating it
# is two operations and provides yet another hole.
#
# Note: use flock based locking as the primary means of locking.
#
# Also, with flock, a file is created to lock on. This file contains
# the process ID that created the file to help troubleshoot bad locks.
# For the file based locking (using mkdir), an owner.dat file is
# created in the lock-directory.
#
package Extropia::Core::Lock;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _notImplemented);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $lock = Extropia::Core::Lock->create(-TYPE => "file",
#                   -FILE => "filename",
#                   -TIMEOUT => 10,
#                   -TRIES   => 5);
# $lock->obtainLock();
# $lock->releaseLock();

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $lock_class = Extropia::Core::Base::_getDriver("Extropia::Core::Lock", $type) or
        Carp::croak("Extropia::Core::Lock type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $lock_class->new(@fields);
}

# default resource clean up method. 
sub cleanUpLock {
    my $self = shift;

    $self->releaseLock(); 
} # end of cleanUpLock

# needs to implement releaseLock() and obtainLock()
#
# helper method to destroy lock on destruction...
#
sub DESTROY {
    my $self = shift;
    $self->releaseLock();
}

1;

