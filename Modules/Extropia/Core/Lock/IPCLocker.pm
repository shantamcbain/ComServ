#$Id: IPCLocker.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Lock::IPCLocker;

use Carp;
use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Error;
use Extropia::Core::Lock;

use IPC::Locker;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Lock);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $lock = new Extropia::Core::Lock(-TYPE => "IPCLocker",
#                   -FILE => "filename",
#                   -TIMEOUT => 10,
#                   -TRIES   => 5);
# $lock->obtainLock();
# $lock->releaseLock();
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash(
            [
             -RESOURCE_NAME,
             -TIMEOUT,
             -REMOVE_LOCK_AFTER_TIMEOUT,
             -HOST, 
             -PORT
            ],
            [
             -RESOURCE_NAME
            ],@_);

    $self = _assignDefaults($self, {-TIMEOUT                   => 120,
                                    -REMOVE_LOCK_AFTER_TIMEOUT => 1,
                                   });

    return bless $self, $package;

}

#
# Using IPC::Locker involves just using the lock object
# created from the IPC::Locker... and that's it!
#
# Very easy. Note: You must be running lockerd on the machine
# that is accepting locks.
#
sub obtainLock {
    my $self = shift;
    
    my @extra_params = ();

    if ($self->{-TIMEOUT}) {
        push(@extra_params, 'timeout', $self->{-TIMEOUT});
    }
    if ($self->{-HOST}) {
        push(@extra_params, 'host', $self->{-HOST});
    }
    if ($self->{-PORT}) {
        push(@extra_params, 'port', $self->{-PORT});
    }

    my $lock = IPC::Locker->lock(
            lock => $self->{-RESOURCE_NAME},
            @extra_params);

    if ($lock) {
        $self->{_lock_object} = $lock;
    } else {
        die("Something went wrong. IPC::Locker could " .
            "not obtain a lock. Perhaps you should " .
            "restart the IPC::Locker demon.");
    }
    return 1;

} # end of obtain lock

sub releaseLock {
    my $self = shift;

    $self->{_lock_object}->unlock();

    return 1;
}

1;

