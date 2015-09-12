#$Id: ApacheFile.pm,v 1.2 2001/05/21 08:45:31 gunther Exp $
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

package Extropia::Core::Session::ApacheFile;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Session qw(CACHE_NOTHING CACHE_READS CACHE_READS_AND_WRITES
                         NO_LOCK DATA_STORE_LOCK ATTRIBUTE_LOCK);
use Extropia::Core::UniqueFile;

use Carp;
use strict;

use Apache::Session::File;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Session);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self; 
    ($self,@_) = _rearrangeAsHash (
        [
            -SESSION_ID,
            -SESSION_DIR,
            -MAX_ACCESS_TIME,
            -MAX_MODIFY_TIME,
            -MAX_CREATION_TIME,
            -TRACK_ACCESS_TIME,
            -TRACK_MODIFY_TIME,
            -TRACK_CREATION_TIME,
            -LOCK_PARAMS,
            -LOCK_POLICY,
            -DATA_POLICY,
            -FATAL_TIMEOUT,
            -FATAL_SESSION_NOT_FOUND
        ],[],@_); 

    $self = _assignDefaults($self,{
                    -MAX_ACCESS_TIME          => 3600, # 1 hr
                    -MAX_MODIFY_TIME          => 3600, # 1 hr
                    -MAX_CREATION_TIME        => 3600, # 1 hr
                    -TRACK_ACCESS_TIME        => 1,
                    -TRACK_MODIFY_TIME        => 1,
                    -TRACK_CREATION_TIME      => 0,
                    -LOCK_POLICY              => DATA_STORE_LOCK,
                    -SESSION_DIR              => Extropia::Core::UniqueFile::findTempDirectory(),
                    -DATA_POLICY              => CACHE_NOTHING
                   },@_);
    
    my %tied_hash;
    tie %tied_hash, 'Apache::Session::File',
        $self->{-SESSION_ID},{Directory => $self->{-SESSION_DIR}};

    if (!$self->{-LOCK_PARAMS}) {
        $self->{-LOCK_PARAMS} = [
            -TYPE => 'File',
            -LOCK_DIR => $self->{-SESSION_DIR}
            ];
    }

    if (defined %tied_hash) {
        $self->{_session_hash}=\%tied_hash;
    } else {
        die("Failed to create a tied hash for ApacheFile " . 
            "session to use. Error was $@");
    }

    if (!defined $self->{-SESSION_ID}) {
        $self->{-SESSION_ID}=$self->{_session_hash}->{_session_id};
        $self->{_is_new}=1;
    }

    bless $self, ref($package) || $package;
    $self->_init();
    return($self);
}

sub getLastModifiedTime {
    my $self = shift;

    my $mt;
    if($self->_trackModify()){
        $mt = -M $self->_getSessionFilename();
        $mt = $^T-($mt*24*60*60);
        return($mt);
    }
    else {
        die("attempt to call getLastModifiedTime for a session " . 
            "object that is not tracking modifications");
    }
}

sub _setLastModifiedTime {
    # empty subroutine
}

sub getLastAccessedTime {
    my $self = shift;

    my $lat;
    if($self->_trackAccess()){
        $lat = -A $self->_getSessionFilename();
        $lat = $^T-($lat*24*60*60);
        return($lat);
    }
    else {
        die("attempt to call getLastAccessedTime for a session " . 
            "object that is not tracking accesses");
    }
}

sub _setLastAccessedTime {
    # empty subroutine
}

sub _getSessionFilename {
    my $self = shift;

    return ($self->{-SESSION_DIR} . '/' . $self->{-SESSION_ID});
}

sub invalidate {
    my $self = shift;

    eval {
        tied(%{$self->{_session_hash}})->delete();
    };
    if ($@) {
        die("Unable to invalidate ApacheFile session object: Error $@");
    }
}

sub _readSession {
    my $self = shift;

    return(\%{$self->{_session_hash}});
}

sub _writeSession {
    my $self = shift;

    %{$self->{_session_hash}}=%{$self->{_data_cache}};    
}

#
# STATIC METHOD
#
sub _getSessions {
    my $package = shift;

    my ($session_params, @other_args) = 
        _rearrangeAsHash([-SESSION_DIR], [], @_);

    my $session_dir = $session_params->{-SESSION_DIR} || 
        Extropia::Core::UniqueFile::findTempDirectory();


    local *SESSIONDIR;
    opendir(SESSIONDIR, $session_dir) ||
        confess("File Session Package could not open $session_dir " .
                "to getSessions.");
    my @session_file_list = grep(!/^\.+$/, readdir(SESSIONDIR));
    closedir (SESSIONDIR);
    
    my @sessions;
    my $session_file;
    foreach $session_file (@session_file_list) {
        eval {
            my $new_session = Extropia::Core::Session->create(
                                    -SESSION_ID => $session_file,
                                    -SESSION_DIR => $session_dir,
                                    @other_args
                                    );
            push(@sessions, $new_session);
        };
        if (($@) && ($@ !~ /^TIMEOUT/i)) {
            confess("Unknown error in _getSessions " .
                    "for session $session_file. Error: $@");
        }
    }
    return (@sessions);
}

1;
