#$Id: Flock.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Lock::Flock;

use Carp;
use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Lock;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Lock);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# The following has the same effect as
# use constant but is compatible with Perl 5.003
#
sub LOCK_SHARED       () { 1; };
sub LOCK_EXCLUSIVE    () { 2; };
sub LOCK_NON_BLOCKING () { 4; };
sub LOCK_RELEASE      () { 8; };

# $lock = new Extropia::Core::Lock(-TYPE => "flock",
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
             -CLEAN_UP_AFTER_RELEASE,
             -DO_NOT_RENAME_FILE],
            [-FILE],@_);

    $self = _assignDefaults($self, {-TIMEOUT                   => 120,
                                    -TRIES                     => 0,
                                    -DO_NOT_RENAME_FILE        => 0,
                                    _filehandle                => undef});

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
    if ($directory =~ /^(.*)(\/|\\)/) {
        $directory = $1;
    } else {
        $directory = ".";
    }
    if (!-e $directory) {
        die("$directory does not exist!");
    }
    if (!-w $directory) {
        die("$directory is not writable!");
    }

    return bless $self, $package;
}

sub obtainLock {
    my $self = shift;
    @_ = _rearrange([-SHARED],[],@_);

    my $shared_lock = shift || 0;
    
    my $max_tries  = $self->{-TRIES};
    my $timeout    = $self->{-TIMEOUT};
    my $file       = $self->{-FILE};
    my $start_time = time();
    my $tries      = 0;

    my $lock_failed = 0;

    # If the file exists, it will be opened normally. If it does
    # not exist, it will be created.
    local *FH;
    open(FH, ">>$file") || 
        die("Could not open lock file: $file: $!\n");


    my $lock_type = LOCK_EXCLUSIVE;
    $lock_type = LOCK_SHARED if ($shared_lock);
    if ($max_tries) {
        while (!flock(FH, $lock_type | LOCK_NON_BLOCKING)) {
            sleep($timeout/$max_tries);
            if (time() - $start_time > $timeout) {
            $lock_failed = 1;
            last;
            } 
        }
        if ($lock_failed) {
            my ($cpkg, $cfile, $cline, $csub) = caller(0);
            die("The lock on " . $file 
                . " failed, in $cfile $cpkg\:\:$csub at line $cline.");
        }
    } else {
        local $SIG{ALRM} = 
            sub { die("The lock on $file failed to be acquired.") };
        alarm($timeout);
        flock(FH, $lock_type);
        alarm 0;
    }

    $self->{_filehandle} = *FH;
    return 1;

} # end of obtainLock

sub releaseLock {
    my $self = shift;

    # normally we should flush output before unlocking, but since we don't
    # care so much about the lockfile contents, we just release the lock
    # explicitly first.
    my $fh = $self->{-FILEHANDLE} || 0;
    if ($fh) {
# taken from Perl Cookbook to flush data before unlocking...
        if ($] < 5.004) {
            my $old_fh = select($fh);
            local $| = 1;
            local $\ = '';
            print "";
            select ($old_fh);
        }
        flock($fh, LOCK_RELEASE);
        close($fh);
    }

    return 1;

} # end of releaseLock

# clean up by calling ancestor method and then unlinking the
# lock file that we generally keep lying around between 
# locks.
sub cleanUpLock {
    my $self = shift;

    $self->SUPER::cleanUpLock();
    unlink($self->{-FILE});
}

1;

