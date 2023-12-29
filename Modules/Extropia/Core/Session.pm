#$Id: Session.pm,v 1.4 2001/05/21 10:33:08 gunther Exp $
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

package Extropia::Core::Session;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver);

use vars qw(@ISA $VERSION @EXPORT_OK);
@EXPORT_OK = qw(CACHE_NOTHING CACHE_READS CACHE_READS_AND_WRITES
                NO_LOCK DATA_STORE_LOCK ATTRIBUTE_LOCK);
@ISA       = qw(Extropia::Core::Base);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.4 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# declare data policy constants
sub CACHE_NOTHING          () { 1; }
sub CACHE_READS            () { 2; }
sub CACHE_READS_AND_WRITES () { 3; }

# declare locking constants for -LOCK_POLICY
sub NO_LOCK         () { 1; }
sub DATA_STORE_LOCK () { 2; }
sub ATTRIBUTE_LOCK  () { 3; }

# declare error constants for the session time out errors
sub MISC_ERROR             () { 0; }
sub ACCESS_TIME_EXCEEDED   () { 1; }
sub MODIFY_TIME_EXCEEDED   () { 2; }
sub CREATION_TIME_EXCEEDED () { 3; }
sub SESSION_NOT_FOUND      () { 4; }

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $session_class = 
        Extropia::Core::Base::_getDriver("Extropia::Core::Session", $type) or
        Carp::croak("Extropia::Core::Session type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $session_class->new(@fields);
}

#
# Drivers must implement the following methods
#
# getLastModifiedTime
# _setLastModifiedTime
# getCreationTime
# _setCreationTime
# getLastAccessedTime
# _setLastAccessedTime
# removeAttributes
# _readSession
# _writeSession
# _getSessions
# _invalidateOldSessions
# forceSessionRead
# forceSessionWrite
#
# Plus the following Java servlet compatible methods
#
# getAttribute
# setAttribute
# removeAttribute
# getAttributeNames
# getAttributes
# getCreationTime
# getLastAccessedTime
# getMaxInactiveInterval
# invalidate
# setMaxInactiveInterval
# isNew
# getId

sub _init {
    my $self = shift;

    if((defined $self->{-MAX_ACCESS_TIME}) or 
       (defined $self->{-MAX_MODIFY_TIME}) or
       (defined $self->{-MAX_CREATION_TIME})) {
        $self->_checkValidity();
    }

    if ($self->_trackAccess()) {
        $self->_policyRead();
        $self->_setLastAccessedTime();
        $self->_policyWrite();
    }

    if (($self->_trackCreation()) and 
        ($self->isNew())) {
        $self->_policyRead();
        $self->_setCreationTime();
        $self->_policyWrite();
    }

    if (!$self->{-LOCK_POLICY}) {
        $self->{-LOCK_POLICY} = NO_LOCK;
    }

    if (!defined($self->{-FATAL_TIMEOUT})) {
        $self->{-FATAL_TIMEOUT} = 1;
    }

    if (!defined($self->{-FATAL_SESSION_NOT_FOUND})) {
        $self->{-FATAL_SESSION_NOT_FOUND} = 1;
    }
}

sub _trackAccess {
    my $self = shift;

    return ($self->{-TRACK_ACCESS_TIME});
}

sub _trackModify{
    my $self = shift;

    return ($self->{-TRACK_MODIFY_TIME});
}

sub _trackCreation{
    my $self = shift;

    return ($self->{-TRACK_CREATION_TIME});
}

sub _generateSessionNotFoundError {
    my $self = shift;

    my $remote_addr = $ENV{"REMOTE_ADDR"} || "No Remote Addr";
    my $session_id = $self->{-SESSION_ID} || '';
    $self->{-SESSION_ID} = undef;

    if ($self->{-FATAL_SESSION_NOT_FOUND}) {
        confess("Passed Session ID: $session_id from " .
        $remote_addr . " does not exist. " .
        "Possible hack attempt.");
    } else {
        require Extropia::Core::Error;
        my $error = new Extropia::Core::Error(
                -CODE => SESSION_NOT_FOUND,
                -MESSAGE => 
                    "Passed Session ID: $session_id from " .
                    $remote_addr . " does not exist. " .
                    "Possible hack attempt."
           );
        $self->addError($error);
    }

} # end of _generateSessionNotFoundError

sub _getSession {
    my $self = shift;

    my $session_id = $self->{-SESSION_ID} || '';

# META: check that the session is valid
#    unless ($session_id && $self->_checkValidity()) {
    unless ($session_id) {
        $self->{_is_new} = 1;
        # META: need to reuse the upgrade to the same session id
        return $self->_createSession();
    }

    unless ($self->_doesSessionExist($session_id) or $self->getErrorCount()) {
        $self->_generateSessionNotFoundError();
        $self->{_invalid_session_at_construction_time} = 1;
    }

    return $session_id;

} # end of _getSession


sub setAttribute {
    my $self = shift;
    @_ = _rearrange([-KEY,-VALUE],[-KEY,-VALUE],@_);

    my $key   = shift;
    my $value = shift;
    
    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->obtainLock();
    }
    $self->_policyRead();
    my $old_value = $self->{_data_cache}->{$key};
    if (!defined($old_value) || $value ne $old_value) {
        $self->_setDataCacheAttribute(-KEY => $key,-VALUE => $value);
        $self->_setLastAccessedTime();
        $self->_setLastModifiedTime();
        $self->_policyWrite();
    }

    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->releaseLock();
    }
}

sub getAttribute {
    my $self = shift;
    @_ = _rearrange([-KEY],[-KEY],@_);

    my $key = shift;

    $self->_policyRead();
    my $return_value = $self->{_data_cache}->{$key};

    if ($key ne "_ACCESS_TIME") {
        $self->_setLastAccessedTime();
    }
    return($return_value);
}

sub removeAttribute {
    my $self = shift;
    @_ = _rearrange([-KEY],[-KEY],@_);

    my $key = shift;

    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->obtainLock();
    }
    $self->_policyRead();
    $self->_deleteDataCacheAttribute(-KEY => $key);

    $self->_setLastAccessedTime();
    $self->_setLastModifiedTime();
    $self->_policyWrite();
    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->releaseLock();
    }
}

sub removeAttributes {
    my $self = shift;

    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->obtainLock();
    }
    foreach ($self->getAttributeNames()) {
        $self->_deleteDataCacheAttribute(-KEY => $_);
    }
    $self->_setLastAccessedTime();
    $self->_setLastModifiedTime();
    $self->_policyWrite();
    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK) {
        $self->releaseLock();
    }
}

sub getAttributeNames {
    my $self = shift;

    $self->_policyRead();
    $self->_setLastAccessedTime();
    $self->_policyWrite();
    my @names = grep { !/^_/; } (keys %{$self->{_data_cache}});
    return @names;
}

sub getAttributes {
    my $self = shift;

    $self->_policyRead();
    $self->_setLastAccessedTime();
    $self->_policyWrite();
    my @keys = (grep !/^_/,(keys %{$self->{_data_cache}}));

    my @return_list;
    foreach (@keys) {
        push(@return_list, $self->{_data_cache}->{$_});
    }
    return(@return_list);
}

sub _setDataCacheAttribute {
    my $self = shift;
    @_ = _rearrange([-KEY,-VALUE],[-KEY,-VALUE],@_);

    my $key   = shift;
    my $value = shift;

    $self->{_has_changed}        = 1;
    $self->{_data_cache}->{$key} = $value;
}

sub _deleteDataCacheAttribute {
    my $self = shift;
    @_ = _rearrange([-KEY],[-KEY],@_);

    my $key = shift;

    $self->{_has_changed} = 1;
    delete $self->{_data_cache}->{$key};
}

sub _policyRead{
    my $self = shift;

    return if ($self->{_invalid_session_at_construction_time});
        
    my $session_data;

# read data if either we dont cache anything or
# we have not read the session before...
    if ($self->{-DATA_POLICY} == CACHE_NOTHING ||
        !$self->{_has_read_session}) {
        $session_data = $self->_readSession();
        $self->{_data_cache} = {%$session_data};
    }
    $self->{_has_read_session} = 1;
}

sub _policyWrite {
    my $self = shift;

    return if ($self->{_invalid_session_at_construction_time});

    if ((($self->{-DATA_POLICY} == CACHE_NOTHING) ||
        ($self->{-DATA_POLICY} == CACHE_READS)) &&
        ($self->_hasDataChanged())){
        $self->{_last_written_data_cache} = {%{$self->{_data_cache}}};
        $self->_writeSession($self->{_data_cache});
        $self->{_has_changed} = 0;
    }
}

sub _hasDataChanged {
    my $self = shift;

    return $self->{_has_changed};
}

sub DESTROY {
    my $self = shift;

    if (($self->{-DATA_POLICY} == CACHE_READS_AND_WRITES) && 
        ($self->_hasDataChanged()) &&
        ($self->getErrorCount() < 1)) {
        $self->_writeSession($self->{_data_cache});
    }
    if (defined $self->{_lock_object}) {
        $self->releaseLock();
    }
}

sub forceSessionWrite {
    my $self = shift;

    if ($self->_hasDataChanged()) {
        $self->_writeSession();
        $self->{_has_changed} = 0;
    }
}

sub forceSessionRead {
    my $self = shift;

    my $session_data = $self->_readSession();
    $self->{_data_cache} = {%$session_data};
    $self->{_has_changed} = 0;
}

sub _checkValidity {
    my $self = shift;

    my $max_interval;
    my $last_time;

    if ($self->_trackAccess() &&
        defined($max_interval = $self->{-MAX_ACCESS_TIME}) && 
        defined($last_time = $self->getLastAccessedTime()) &&
        ($max_interval + $last_time) < time()) {
        $self->invalidate();
        if ($self->{-FATAL_TIMEOUT}) {
            confess("TIMEOUT: session with id " . $self->getId() . 
            "has exceeded max_access_time: $max_interval.");
        } else {
            require Extropia::Core::Error;
            my $error = new Extropia::Core::Error(
                    -MESSAGE => "TIMEOUT: session with id " . $self->getId() . 
                                "has exceeded max_access_time: $max_interval.",
                    -CODE    => Extropia::Core::Session::ACCESS_TIME_EXCEEDED);
            $self->addError($error);
        }
    }

#print "TrackModify:" . $self->_trackModify() . "\n";
#   print "Current time: " . time() . "\n";
#   print "Last Mod Time: " . $self->getLastModifiedTime() . "\n";
   
    if ($self->_trackModify() &&
        defined($max_interval = $self->{-MAX_MODIFY_TIME}) && 
        defined($last_time = $self->getLastModifiedTime()) &&
        ($max_interval + $last_time) < time()) {
        $self->invalidate();
        if ($self->{-FATAL_TIMEOUT}) {
            confess("TIMEOUT: session with id " . $self->getId() . 
            "has exceeded max_modify_time: $max_interval.");
        } else {
            require Extropia::Core::Error;
            my $error = new Extropia::Core::Error(
                    -MESSAGE => "TIMEOUT: session with id " . $self->getId() . 
                                "has exceeded max_modify_time: $max_interval.",
                    -CODE    => Extropia::Core::Session::MODIFY_TIME_EXCEEDED);
            $self->addError($error);
        }
    }

    if ($self->_trackCreation() &&
        defined($max_interval = $self->{-MAX_CREATION_TIME}) && 
        defined($last_time = $self->getCreationTime()) &&
        ($max_interval + $last_time) < time()) {
        $self->invalidate();
        if ($self->{-FATAL_TIMEOUT}) {
            confess("TIMEOUT: session with id " . $self->getId() . 
            "has exceeded max_creation_time: $max_interval.");
        } else {
            require Extropia::Core::Error;
            my $error = new Extropia::Core::Error(
                    -MESSAGE => "TIMEOUT: session with id " . $self->getId() . 
                                "has exceeded max_creation_time: $max_interval.",
                    -CODE    => Extropia::Core::Session::CREATION_TIME_EXCEEDED);
            $self->addError($error);
        }
    }

}

sub setMaxInactiveInterval {
    my $self = shift;
    @_ = _rearrange([-AGE],[-AGE],@_);

    my $age = shift;

    $self->{-MAX_ACCESS_TIME} = $age;
    
    $self->_checkValidity();
}

sub getMaxInactiveInterval {
    my $self = shift;

    return($self->{-MAX_ACCESS_TIME});
}

sub setMaxModifyInterval {
    my $self = shift;
    @_ = _rearrange([-AGE],[-AGE],@_);

    my $age = shift;

    $self->{-MAX_MODIFY_TIME} = $age;
    
    $self->_checkValidity();
}

sub getMaxModifyInterval {
    my $self = shift;

    return($self->{-MAX_MODIFY_TIME});
}


sub setMaxCreationInterval {
    my $self = shift;
    @_ = _rearrange([-AGE],[-AGE],@_);

    my $age = shift;

    $self->{-MAX_CREATION_TIME} = $age;
    
    $self->_checkValidity();
}

sub getMaxCreationInterval {
    my $self = shift;

    return($self->{-MAX_CREATION_TIME});
}


sub _setLastModifiedTime {
    my $self = shift;

    if ($self->_trackModify()) {
        $self->_policyRead();
        $self->_setDataCacheAttribute(-KEY   => '_MODIFY_TIME',
                                      -VALUE => time());
        $self->_policyWrite();
    }
}

sub getLastModifiedTime {
    my $self = shift;

    if ($self->_trackModify()) {
        return($self->getAttribute(-KEY => '_MODIFY_TIME'));
    } else {
        confess("Attempt to getLastModifiedTime for an object that " . 
            "it not tracking modifications");
    }
}

sub _setLastAccessedTime{
    my $self = shift;

    if ($self->_trackAccess()) {
        $self->_policyRead();
        $self->_setDataCacheAttribute(-KEY   => '_ACCESS_TIME',
                                      -VALUE => time());
        $self->_policyWrite();
    }
}

sub getLastAccessedTime {
    my $self = shift;

    if ($self->_trackAccess()) {    
        return($self->getAttribute(-KEY => '_ACCESS_TIME'));
    } else {
        confess("Attempt to getLastAccessedTime for an object that " .
            "is not tracking access time");
    }
}

sub _setCreationTime {
    my $self = shift;

    if ($self->_trackCreation()) {
        $self->setAttribute(-KEY   => '_CREATION_TIME',
                            -VALUE => time());
    }
}

sub getCreationTime {
    my $self = shift;

    if ($self->_trackCreation()) {
        return($self->getAttribute(-KEY => '_CREATION_TIME'));
    } else {
        confess("Attempt to getCreationTime for an object that " .
            "is not tracking creationTime");
    }
}

sub _getLockObject {
    my $self = shift;

	my $lock        = $self->{_lock_object};
	
    if (!$lock && $self->{-LOCK_PARAMS}) {
        my @lock_params = @{$self->{-LOCK_PARAMS}};
        my $resource_name = $self->getId();
        push(@lock_params, -RESOURCE_NAME, $resource_name);
        require Extropia::Core::Lock;
        $lock = Extropia::Core::Lock->create(@lock_params);
		$self->{_lock_object} = $lock;
	}
    return($lock);
}

sub obtainLock {
    my $self = shift;

    my $lock = $self->_getLockObject();
    if ($lock && !$self->{_lock_obtained}) {
        $lock->obtainLock();
        $self->{_lock_obtained} = 1;
    }
}

sub releaseLock {
    my $self = shift;

    my $lock = $self->_getLockObject();
    if ($lock && $self->{_lock_obtained}) {
        $lock->releaseLock();
        $self->{_lock_obtained} = 0;
    }
}

sub isNew{
    my $self = shift;
    return($self->{_is_new});
}

sub getId{
    my $self = shift;

    return($self->{-SESSION_ID});
}

sub getTiedHash{
    my $self = shift;

    if (!$self->{_session_hash}) {
        my %hash;
        tie %hash, 'Extropia::Core::Session::TiedHashRepresentation',
            $self;
        $self->{_session_hash} = \%hash;
    }

    return($self->{_session_hash});
}

# default implementation of _invalidateOldSessions
sub _invalidateOldSessions {
    my $package = shift;

    $package->_getSessions(@_);
    return 1;
}

#
# Tied Hash representation of a raw session object
#
package Extropia::Core::Session::TiedHashRepresentation;

use strict;

sub TIEHASH {
    my $self = shift;

    my $session = shift;
    
    my $node ={
        _session_object => $session
    };
    return bless $node, $self;
}

sub FETCH {
    my $self = shift;

    my $key = shift;

    my $session = $self->{_session_object};

    # Take care of "private" variables
    if ($key =~ /^_ID$/i || $key =~ /^_SESSION_ID$/i) {
      return $session->getId();
    } elsif ($key =~ /^_SESSION_OBJECT$/i) {
      return $session;
    }
    return($session->getAttribute("-KEY" => $key));
}

sub STORE {
    my $self = shift;

    my $key   = shift;
    my $value = shift;

    return if ($value =~ /^_/);
    my $session = $self->{_session_object};

    $session->setAttribute(-KEY => $key,-VALUE => $value);
}

sub DELETE {
    my $self = shift;

    my $key = shift;

    my $session = $self->{_session_object};
    $session->removeAttribute(-KEY => $key);
}

sub CLEAR {
    my $self = shift;

    my $session = $self->{_session_object};
    $session->removeAttributes();
}

sub EXISTS{
    my $self = shift;

    my $key = shift;

    my $session = $self->{_session_object};
    return defined($session->getAttribute(-KEY => $key));
}

sub FIRSTKEY {
    my $self = shift;

    my $session = $self->{_session_object};

    $self->{_data_cache_hash} = {};
    my @keys = $session->getAttributes();
    foreach (@keys) {
        $self->{_data_cache_hash}->{$_} = 
            $session->getAttribute(-KEY => $_);
    }
    return each %{$session->{_data_cache_hash}};
}

sub NEXTKEY {
    my $self = shift;

    return each %{$self->{_data_cache_hash}};
}

1;

__END__

