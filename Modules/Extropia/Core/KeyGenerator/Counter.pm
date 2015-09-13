#$Id: Counter.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::KeyGenerator::Counter;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::KeyGenerator;
use Extropia::Core::Lock;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::KeyGenerator);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new KeyGenerator Object 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([
            -COUNTER_FILE,
            -LOCK_PARAMS,
            -INITIAL_KEY_SOURCE
        ],
        [-COUNTER_FILE], @_);

    my $lock_params = $self->{-LOCK_PARAMS};

    if ($lock_params) {
        my @new_lock_params = @$lock_params;
        push(@new_lock_params, '-FILE', $self->{-COUNTER_FILE});
        $self->{_lock_object} = Extropia::Core::Lock->create(
            @new_lock_params);
    } else {
        $self->{_lock_object} = Extropia::Core::Lock->create(
            -TYPE => 'File',
            -FILE => $self->{-COUNTER_FILE});
    }

    return bless $self, $package;

} # end of new

sub createKey {
    my $self = shift;
    @_ = _rearrange([-EXTRA_ELEMENT],[],@_);

    my $extra_element = shift || "";
    my $lock          = $self->{_lock_object};
    my $counter_file  = $self->{-COUNTER_FILE};

    local(*COUNTER);
    my $key;

    $lock->obtainLock();
    if (!(-e $counter_file)) {
        $key = 1;
        if ($self->{-INITIAL_KEY_SOURCE}) {
            $key = $self->{-INITIAL_KEY_SOURCE}->getInitialKey();
        }
        open (COUNTER,">$counter_file") ||
            die ("Could not open counter file for writing: " .
                 "$counter_file: $!");
    } else {
        open (COUNTER, "+<$counter_file") ||
            die("Could not open counter file for update: " .
                "$counter_file: $!");
        $key = <COUNTER> || "";
        chomp($key);
        if (!$key && $self->{-INITIAL_KEY_SOURCE}) {
            $key = $self->{-INITIAL_KEY_SOURCE}->getInitialKey();
        }
        $key++;
        seek(COUNTER,0,0);
    } 
    print COUNTER "$key\n";
    close (COUNTER);
    $lock->releaseLock();

# untaint the key... since it was read from a file...
# taintmode thinks it could be a hacked element which of course
# is not true...
    if ($key =~ /(\d*)/) {
        $key = $1;
    } else {
        die("Well, whaddya know, KeyGenerator::Counter could not 
             untaint the generated counter afterall...weird");
    }

    return $key . $extra_element;
    
} # end of createKey

1;
