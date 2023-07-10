#$Id: File.pm,v 1.7 2001/09/09 14:52:57 gunther Exp $
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

package Extropia::Core::Session::File;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Session qw(CACHE_NOTHING CACHE_READS CACHE_READS_AND_WRITES
                         NO_LOCK DATA_STORE_LOCK ATTRIBUTE_LOCK);
use Extropia::Core::UniqueFile;

use Carp;
use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Session);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.7 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self,@_) = _rearrangeAsHash(
               [
                    -SESSION_ID,
                    -SESSION_FILE_EXTENSION,
                    -SESSION_DIR,
                    -KEY_GENERATOR_PARAMS,
                    -SESSION_ID_LENGTH,
                    -SESSION_CREATE_MAX_TRIES,
                    -DATA_POLICY,
                    -MAX_ACCESS_TIME,
                    -MAX_MODIFY_TIME,
                    -MAX_CREATION_TIME,
                    -LOCK_PARAMS,
                    -LOCK_POLICY,
                    -TRACK_ACCESS_TIME,
                    -TRACK_MODIFY_TIME,
                    -TRACK_CREATION_TIME,
                    -FATAL_TIMEOUT,
                    -FATAL_SESSION_NOT_FOUND
             ],
            [],@_
                    );

    $self = __assignSessionFileDefaults($self);

    bless $self, ref($package) || $package;

    if (!$self->{-LOCK_PARAMS}) {
        $self->{-LOCK_PARAMS} = [
            -TYPE => 'File',
            -LOCK_DIR => $self->{-SESSION_DIR}
            ];
    }

    $self->{-SESSION_ID} = $self->_getSession();
    if (!defined($self->{-SESSION_ID})) {
        return (undef);
    }

    $self->_init();
    return $self;
}

sub __assignSessionFileDefaults {
    my $original = shift;

    $original = _assignDefaults($original, {-SESSION_ID_LENGTH => 0});

#
# NOTE: The default is ACCESS TIME and MODIFY TIME tracking for
# the session timeout tracking...
# But the only Win98/95 systems, access time tracking does not
# work at all...
#
# Therefore Win95/Win98 users may need to change it so that
# Tracking access time is turned off. Note that WinNT/2000
# users should not have a problem.
#
# Basically what seems to occur on Win95/Win98 is that
# accessed time actually behaves more like creation time 
# but doesn't seem to be very logical.
#
# Setting this tracking to on probably won't affect anything
# too badly on Win98, but if there are problems email
# support@extropia.com and let us know the behavior. You
# likely should just turn off track access time if it is
# causing an issue.
#
    return _assignDefaults($original,{
      -SESSION_DIR               => Extropia::Core::UniqueFile::findTempDirectory(),
      -KEY_GENERATOR_PARAMS      => [
                 -TYPE           => 'Random',
                 -SECRET_ELEMENT => '42lifetheuniverseandeverything',
                 -LENGTH         => $original->{-SESSION_ID_LENGTH}
                                     ],
      -SESSION_CREATE_MAX_TRIES  => 5,
      -DATA_POLICY               => CACHE_NOTHING,
      -MAX_ACCESS_TIME           => 60*60, # 1 hr
      -MAX_MODIFY_TIME           => 60*60, # 1 hr
      -MAX_CREATION_TIME         => 60*60, # 1 hr
      # Access time is off if we are in win32 because FAT32 can't
      # handle access time
      -TRACK_ACCESS_TIME         => ($^O =~ /MSWin32/i ? 0 : 1),
      -TRACK_MODIFY_TIME         => 1,
      -TRACK_CREATION_TIME       => 0,
      -LOCK_POLICY               => DATA_STORE_LOCK,
      -SESSION_FILE_EXTENSION    => 'ses',
      -FATAL_SESSION_NOT_FOUND   => 1
    });
}

sub _doesSessionExist {
    my $self = shift;

    my $session_file = $self->_getSessionFilename();
    return (-e $session_file);
}

sub _createSession {
    my $self = shift;

    my $session_ext    = $self->{-SESSION_FILE_EXTENSION};
    my $session_length = $self->{-SESSION_ID_LENGTH};

    my $unique_file = new Extropia::Core::UniqueFile(
            -KEY_GENERATOR_PARAMS => $self->{-KEY_GENERATOR_PARAMS},
            -EXTENSION            => $session_ext,
            -DIRECTORY            => $self->{-SESSION_DIR},
            -NUMBER_OF_TRIES      => $self->{-SESSION_CREATE_MAX_TRIES}
            );

    $unique_file->createFile();
    my $session_file = $unique_file->getFilename();
    
    my $session_id;
    if ($session_file =~ /(.*)\.${session_ext}$/) {
        $session_id = $1;
    } else {
        die("Session ID could not be extracted from ${session_file}.");
    }
    
    if ($session_length) {
        $session_id = substr($session_id,0,$session_length);
    }
    return $session_id;
}

sub _setLastAccessedTime {
    # empty since file system does it for us...
}

sub getLastAccessedTime {
    my $self = shift;

    my $lat;
    if ($self->_trackAccess()) {
        $lat = -A $self->_getSessionFilename();
        return undef if (!defined($lat));
        $lat = -$lat * 24 * 60 * 60;
        return($lat);
    } else {
        confess("attempt to call getLastAccessedTime for a session " .
                "object that is not tracking accesses");
    }
}

sub getLastModifiedTime {
    my $self = shift;

    my $mt;
    if ($self->_trackModify()) {
        $mt = -M $self->_getSessionFilename();
        return undef if (!defined($mt));
        $mt = -($mt * 24 * 60 * 60);
        return $mt;
    } else {
        confess("attempt to call getLastModifiedTime for a session " .
            "object that is not tracking modifications");
    }
}


sub _getSessionFilename {
    my $self = shift;

    return '' unless $self->{-SESSION_ID};

    my $session_file = $self->{-SESSION_DIR} . 
                        "/" . $self->{-SESSION_ID} .
                        "." . $self->{-SESSION_FILE_EXTENSION};

    return $session_file;
}

sub _writeSession {
    my $self = shift;

    my $path = $self->_getSessionFilename();
    if ($path) {
        if ($self->{-LOCK_POLICY} == DATA_STORE_LOCK) {
            $self->obtainLock();
        }
        local *FILE;
        open (FILE, ">$path") ||
            confess("File session object failed to open $path " .
                    "to write session. Error was $@.");
        my $key;
        my $value;
        while (($key,$value) = each(%{$self->{_data_cache}})) {
            $value =~ s/\\/\\\\/g;
            $value =~ s/\n/\\n/g;
            print FILE "$key\n$value\n";
        }
        close(FILE);
        if ($self->{-LOCK_POLICY} == DATA_STORE_LOCK) {
            $self->releaseLock();
        }
    }
}

sub _readSession {
    my $self = shift;

    my $path = $self->_getSessionFilename();
    unless ($path && -e $path) {
# If at first we don't succeed... try again after recreating the session
        $self->_writeSession();
        unless ($path && -e $path) {
            $self->_generateSessionNotFoundError();
            return $self->{_data_cache} || {};
        }
    }

    my $should_lock = ($self->{-LOCK_POLICY} == DATA_STORE_LOCK) ? 1 : 0;

    my @lines = ();
    local *FILE;
    $self->obtainLock() if $should_lock;
    # !!! start critical section
    open FILE, "<$path" 
        or confess("File session object failed to open $path to read session: $!");
    @lines = <FILE>;
    close FILE;
    # !!! end critical section
    $self->releaseLock() if $should_lock; # unlock asap
    chomp @lines;

    my %data_cache = @lines;
    foreach my $key (keys %data_cache) {
        $data_cache{$key} =~ s/(^|[^\\])\\n/$1\n/g;
        $data_cache{$key} =~ s/\\\\/\\/g;
    } # end of foreach

    return \%data_cache;
}

# for whatever reason, to enable a session to kill itself, and remove its
# persistent repository.
sub invalidate {
    my $self = shift;

    my $session_file = $self->_getSessionFilename();
    my $lock_policy = $self->{-LOCK_POLICY};
    if ($lock_policy != NO_LOCK) {
        $self->obtainLock();
    }
    unlink $session_file ||
       confess("session file $session_file has cannot be removed\n");
    if ($lock_policy != NO_LOCK) {
        $self->releaseLock();
    }
# eval in case clean up fails... clean up could fail if no
# locks were ever obtained so we do not really care about
# more errors at this point
    eval {
        # clean up any resources required by the lock...
        my $lock = $self->_getLockObject();
        $lock->cleanUpLock() if ($lock);
    }
}

#
# Static (package-level) method 
#
# Note that if this sub changes, you should consider
# also looking at _invalidateOldSessions since their
# algorithms are different.
#
sub _getSessions {
    my $package = shift;

    my ($session_params, @other_args) =
       _rearrangeAsHash([-SESSION_DIR,-SESSION_FILE_EXTENSION], [], @_);
                    
    my $session_dir = $session_params->{-SESSION_DIR} ||
                        Extropia::Core::UniqueFile::findTempDirectory();
    my $session_ext = $session_params->{-SESSION_FILE_EXTENSION} || 'ses';

    my $ra_session_files = $package->__getSessionFileList($session_dir, 
                                                          $session_ext);
    
    my $session_file;
    my @sessions;
    foreach $session_file (@$ra_session_files) {
        eval {
            $session_file =~ /(.*)\.${session_ext}$/;
            my $session_id = $1;
            my $new_session = Extropia::Core::Session->create(
                                    -SESSION_ID             => $session_id,
                                    -SESSION_DIR            => $session_dir,
                                    -SESSION_FILE_EXTENSION => $session_ext,
                                    @other_args);
            push(@sessions,$new_session);
        };
        if (($@) && ($@ !~ /^TIMEOUT/i)) {
            confess("Unknown error in _getSessions " .
                    "for session $session_file. Error: $@");
        }
    }
    return(@sessions);
}

#
# _invalidateOldSessions() overrides the default one that merely
# called _getSessions(). _getSessions() is a bit of a heavyweight
# method as it has to instantiate an entire list of session objects
# in order to determine if they can be deleted or not.
#
sub _invalidateOldSessions {
    my $package = shift;

    my ($session_params, @other_args) =
       _rearrangeAsHash([   
                            -SESSION_DIR,
                            -SESSION_FILE_EXTENSION,
                            -DATA_POLICY,
                            -MAX_ACCESS_TIME,
                            -MAX_MODIFY_TIME,
                            -MAX_CREATION_TIME,
                            -LOCK_PARAMS,
                            -LOCK_POLICY,
                            -TRACK_ACCESS_TIME,
                            -TRACK_MODIFY_TIME,
                            -TRACK_CREATION_TIME
                        ], [], @_);
                    
    $session_params = __assignSessionFileDefaults($session_params);

    my $session_dir = $session_params->{-SESSION_DIR} ||
                        Extropia::Core::UniqueFile::findTempDirectory();
    my $session_ext = $session_params->{-SESSION_FILE_EXTENSION} || 'ses';

    my $ra_session_files = $package->__getSessionFileList($session_dir, 
                                                   $session_ext);

    my $session_file;
    foreach $session_file (@$ra_session_files) {
        $session_file =~ /(.*)\.${session_ext}$/;
        my $session_id = $1;
        $session_params->{-SESSION_ID} = $session_id;
        bless $session_params, $package;
# we eval to avoid dying when the session does not pass the
# validity check...
        eval {
            $session_params->_checkValidity();
        }
    } # end of foreach session file...

} # end of _invalidateOldSessions

#
# __getSessionFileList is a private helper method that
# _getSessions and _invalidateOldSessions uses to determine
# the list of session files that exists.
#
sub __getSessionFileList {
    my $package     = shift;

    my $session_dir = shift;
    my $session_ext = shift;

    local *SESSIONDIR;
    opendir(SESSIONDIR,$session_dir) ||
        confess("File Session Object could not open $session_dir ".
                "to get a list of sessions.");
    my @session_file_list = grep(/\.$session_ext$/, readdir(SESSIONDIR));
    closedir(SESSIONDIR);

    return \@session_file_list;

} # end of __getSessionFileList

1;
