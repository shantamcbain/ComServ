#$Id: File.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Lock::File;

use Carp;
use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Error;
use Extropia::Core::Lock;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Lock);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $lock = new Extropia::Core::Lock(-TYPE => "file",
#                   -FILE => "filename",
#                   -TIMEOUT => 10,
#                   -TRIES   => 5);
# $lock->obtainLock();
# $lock->releaseLock();
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash(
            [-FILE,
             -RESOURCE_NAME,
             -LOCK_DIR,
             -TIMEOUT,
             -TRIES,
             -REMOVE_LOCK_AFTER_TIMEOUT,
             -DO_NOT_RENAME_FILE,
             -DEBUG],
            [],@_);

    $self = _assignDefaults($self, {-TIMEOUT                   => 120,
                                    -REMOVE_LOCK_AFTER_TIMEOUT => 1,
                                    -DO_NOT_RENAME_FILE        => 0,
                                    _filehandle                => undef,
                                    });

    $self = _assignDefaults($self, {-TRIES => $self->{-TIMEOUT}});

    unless ($self->{-FILE} ||
            ($self->{-RESOURCE_NAME} && $self->{-LOCK_DIR})) {
        die("Must pass either -FILE or " .
            "-RESOURCE_NAME and -LOCK_DIR as params.");
    }
    if (!$self->{-FILE}) {
        $self->{-FILE} = $self->{-LOCK_DIR};
        if ($self->{-FILE} !~ /\/$/) {
            $self->{-FILE} .= "/";
        }
        $self->{-FILE} .= $self->{-RESOURCE_NAME};
    }
    if (!$self->{-DO_NOT_RENAME_FILE}) {
        $self->{-FILE} .= ".lck";
    }

# check for directory existence ...
    my $directory = $self->{-FILE};
    if ($directory =~ /^(.*)(\/|\\)?$/) {
        $directory = $1;
    } else {
        die("No -FILE or -LOCK_DIR Parameter was passed!");
    }
    if (-e $directory && !-d $directory) {
        die("Directory $directory is not a directory!");
    }
    if (-e $directory && !-w $directory) {
        die("Directory $directory is not writable!");
    }

# check parent directory ...
    my $parent;
    if ($directory =~ /^(.*)(\/|\\)/) {
        $parent = $1;
    } else {
        $parent = "."; # Then its the current directory...
    }
    if (!-e $parent) {
        confess("Parent directory $parent does not exist!");
    }
    if (!-w $parent) {
        die("Parent directory $parent is not writable!");
    }

    if ($self->{-DEBUG}) {
        require Extropia::Core::KeyGenerator;
        my $kg = Extropia::Core::KeyGenerator->create(-TYPE => 'Random');
        $self->{_debug_key} = $kg->createKey();
    }

    return bless $self, $package;

}

#
# The way the file based locking works is through
# emulation of the flock locking scheme...
#
# The reason this works is the mkdir is an atomic operation
# 
# If mkdir fails, then we know someone has the lock, if it
# passes, we know that the lock is ours and no one else could
# get it.
#
sub obtainLock {
    my $self = shift;
    
    my $max_tries  = $self->{-TRIES};
    my $tries      = 0;
    my $timeout    = $self->{-TIMEOUT};
    my $start_time = time();
    my $file       = $self->{-FILE};

    my $lock_failed = 0;
    while (1) {
       last if (mkdir($file,0777));
       if (time() - $start_time > $timeout) {
           $lock_failed = 1;
           last;
       } 
       sleep($timeout/$max_tries);
    }
    if ($lock_failed) {
        my ($cpkg, $cfile, $cline, $csub) = caller(0);
        $self->addError(
          new Extropia::Core::Error(-MESSAGE => "The lock on " . $file 
            . " failed, in $cfile $cpkg\:\:$csub at line $cline.")
          );
        if (!$self->{-REMOVE_LOCK_AFTER_TIMEOUT}) {
            die($self->getLastError()->getMessage());
        }
        if ($self->{-DEBUG}) {
            my $dbg = "Lock::File DEBUG $self->{_debug_key}:";
            local *OWNER;
            open (OWNER, "<$file/owner.dat") ||
                warn "$dbg can't read existing $file/owner.dat\n";
            my $line = <OWNER>;
            chomp $line;
            if ($line =~ /^DEBUG: (.*)$/) {
                warn "$dbg overriding lock on $file created by $1\n";
            }
            elsif ($line) {
                warn "$dbg overriding lock on $file created by unknown "
                    ."Lock object (not in DEBUG mode)\n"
            }
            close OWNER;
        }
        # no error detection is used because another process 
        # may have removed the file or directory.
        unlink("$file/owner.dat");
        rmdir($file);
        return $self->obtainLock();
    } else {
        local *OWNER;
        open (OWNER, ">$file/owner.dat") ||
            die("Error creating file $file/owner.dat: $!");
        if ($self->{-DEBUG}) {
            print OWNER "DEBUG: ", $self->{_debug_key}, "\n";
        }
        print OWNER "OWNER: $$\n";
        close OWNER;
    }
    return 1;

} # end of obtain lock

sub releaseLock {
    my $self = shift;

    my $file = $self->{-FILE};

# no error detection is used because another process 
# may have removed the file or directory.
    if (-e "$file/owner.dat") {
        if ($self->{-DEBUG}) {
            my $dbg = "Lock::File DEBUG $self->{_debug_key}:";
            local *OWNER;
            open (OWNER, "<$file/owner.dat") ||
                warn "$dbg can't read existing $file/owner.dat\n";
            my $line = <OWNER>;
            chomp $line;
            if ($line =~ /^DEBUG: (.*)$/) {
                warn "$dbg releasing lock on $file created by $1\n";
            }
            elsif ($line) {
                warn "$dbg releasing lock on $file created by unknown "
                    ."Lock object (not in DEBUG mode)\n"
            }
            close OWNER;
        }
        unlink("$file/owner.dat") ||
            die("Could not remove $file/owner.dat. " .
                "Lock may have been previously released!");
    }
    elsif ($self->{-DEBUG}) {
        warn "Lock::File DEBUG $self->{_debug_key}: $file/owner.dat missing.\n"
    }
    if (-e $file) {
        rmdir($file) ||
            die("Could not remove $file directory. " .
                "Lock may have been previously released!");
    }

    return 1;

}

1;

