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
        }
        else {
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
 sub setMaxInactiveInterval {
    my $self = shift;
    @_ = _rearrange([-AGE],[-AGE],@_);
     my $age = shift;
     $self->{-MAX_ACCESS_TIME} = $age;
     $self->_checkValidity();
}
 sub getMaxInactiveInterval {
    my $self = shift;
     return $self->{-MAX_ACCESS_TIME};
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
     return $self->{-MAX_MODIFY_TIME};
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
     return $self->{-MAX_CREATION_TIME};
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

=head1 OVERVIEW

HTTP is a stateless protocol. This is something of an inconvenience
from the point of view of the application developer who wants to keep
track of user information from one access of web server to the next.

This framework of modules aims to make that task a little easier. The
basic idea is one of a data repository which is bound to a unique
identifier. The programatic contract that is made between these
objects and the application developer is is that the objects will
always map the same unique ID to the same underlying data store, and
will persist changes made to the state of the object, to that store.

Every effort has been made to abstract the actual type of the data
store from the application logic. Regardless of whether you are using
a Session object that stores data in a database, or in a file, the API
that is presented to the application developer remains unchanged.

To basically sum up all the above, if $session contains a reference to
a session object, then regardless if it is a database based session
object, or a file based session object, the application developer is
ALWAYS going to call $session->methodX to store data or
$session->methodY to retrieve it. This means that design decisions can
be taken regarding where session data is going to be stored [ ie the
type of session object that is going to be used ], and these decisions
can change without affecting the semantics of the application.

Additionally, the application developer can be assured of the fact
that if $session says that it has a unique IDof "xyz", then any use of
this ID in the subsequent creation of a session object will lead to
the reconstitution of the original object, with all its stateful
information as it was left.

The Session objects work hand in hand with the SessionManager range of
objects. The SessionManager objects are responsible for, as the name
suggests, management functions that are outside the ambit of
individual session objects, such as obtaining an enumeration of all
available sessions in a repository, or removing sessions that have
timed out, and so on and so forth. It is also the SessionManager that
is capable of extracting the unique session id from data that it is
passed by the application. It is the SessionManager that
creates/recreates particular session objects. As a result, you will
not find any examples of Session creation in this documentation - see
the SessionManager documentation on information regarding this.

The current range of objects comprises:

=over 4

=item 1 B<Session>

=item 2 B<Session::Base>

=item 3 B<Session::TiedHashRepresentation>

=item 4 B<Session::File>

=item 5 B<Session::ApacheFile>

=item 6 B<Session::ApacheDBI>

=item 7 B<SessionManager>

=item 8 B<SessionManager::Base>

=item 9 B<SessionManager::Cookie>

=item 10 B<SessionManager::FormVar>

=item 11 B<SessionManager::PathInfo>

=item 12 B<SessionManager::Default>

=back

=head1 OBJECT STRUCTURE

The 2 Session objects at the top of the Session object framework are
Session, and Session::Base. These work in the following way:

=over 4

=item 1 B<Session>

Session is an abstract class, which is meant to function as a
template. It defines all the methods that subclasses of Session should
implement if they are to be considered as validly implementing the
Session API.

=back

=over 4

=item 2 B<Session::Base>

Session::Base is a convenience class. A suitable analogy from Java
would be an adapter class. That is to say a class that provides a
range of default functionality, but one that is not intended for use
in its own right, but rather for extension from.

In this case, Session::Base sits under Session, and implements a lot
of the functionality that the Session class dictates as mandatory for
the Session API. The point then is that when you wish to implement a
Session object of a particular flavour, you can extend Session::Base,
and then only worry about implementing those methods from Session that
Session::Base either does not implement at all, or that Session::Base
does implement, but that you want to change.

The alternative would be that every implementation of a new Session
Class would have to re-implement all the functionality dictated by the
root Session class.

Of course the Session::Base class is also free to [ and does ]
implement functionality that is additional to theroot Session class.

The Session::Base object implements an in memory data repository,
stored as a reference to a hash in a private instance variable called
'_data_cache' . Key to the operations of this class is the fact that
operations on data stored in a Session object [ that inherits from
Session::Base ] ONLY alter the data in this cache directly. It is then
the task of the methods in the Session::Base class to check the
data_policy of the object, to see when this in-memory data should be
written to or read from the underlying data repository. This is the
remit of the _policyRead and _policyWrite methods of the Session::Base
object.

The actual reading and writing of Session data is via the
_writeSession and _readSession methods, but these are implemented not
in Session::Base, but polymorphically across all the classes that
derive from it - to represent the fact that Session objects of
different classes persist/read their data in different ways.

=back

The other class that is worth considering in this context is the
Session::TiedHashRepresentation. This is currently only used in
conjunction with the Session::File object. It is essentially a very
thin package that does little except forward all requests for data
access/modification to the Session::File object that it is annexed to,
and which actually does the work of data storage and retrieval. It is
provided as a comfort class for those of you who are used to doing all
Session management through raw tied hash data structures - you can use
the tied hash directly if you want, but all it is going to do is use
the Session object.....

=head1 B<PACKAGE Session>

Instances of Session objects are never created via direct calls to any
object in the Session Heirachy by the application developer. In order
to instantiate a Session object, see the SessionManager documentation.

Documentation on how most of the following methods actually work is to
be found in the documentation for the specific Session subclasses that
actually implement them, which Session itself does not. The methods
are laid out below just to give some idea of the API to which the
classes have been designed

=item 1 B<create PRIVATE METHOD>

This method is called indirectly, via the SessionManager object, in
order to create a session of the appropriate type.

=item 2 B<getAttribute>

=item 3 B<setAttribute>

=item 4 B<removeAttribute>

=item 5 B<_readSession PRIVATE METHOD>

=item 6 B<_writeSession PRIVATE METHOD>

=item 7 B<getAttributeNames>

=item 8 B<getAttributes>

=item 9 B<_getSessions PRIVATE METHOD>

=item 10 B<_invalidateOldSessions>

=item 11 B<getCreationTime>

=item 12 B<_setCreationTime PRIVATE METHOD>

=item 13 B<getLastAccessedTime>

=item 14 B<_setLastAccessedTime PRIVATE METHOD>

=item 15 B<getLastModifiedTime>

=item 16 B<_setLastModifiedTime PRIVATE METHOD>

=item 17 B<getMaxInactiveInterval>

=item 18 B<invalidate>

=item 19 B<setMaxInactiveInterval>

=item 20 B<isNew>

=item 21 B<getId>

=item 21 B<removeAttributes>

=head1 B<PACKAGE Session::Base>

=item 1 B<_init PRIVATE METHOD>

This method is implemented as a convenience for those writing new
Session subclasses. It is responsible for checking whether a given
session has exceeded its timeout period for either the last time it
was accessed, or modified, or from when it was created. It also marks
the Session as having been accessed, and, for new Sessions, marks
their creation time.

It is anticipated that this method will be called by subclasses just
before they return from their constructors.

=item 2 B<_trackAccess PRIVATE METHOD>

returns true or false, to denote whether this Session object is
actually keeping track of the times it is accessed.
  
=item 3 B<_trackModify PRIVATE METHOD>

returns true or false, to denote whether this Session object is
actually keeping track of the times it is modified.

=item 3 B<_trackCreation PRIVATE METHOD>

returns true or false, to denote whether a given NEW session is going
to mark the time of its creation.

=item 4 B<_getSession PRIVATE METHOD>

this method is responsible for creating the Session object, either as
a new Session, or as a reconstitued old Session based on a pre
existing Session ID that it has been handed.

In the case of pre exisiting IDs, it is also responsible for checking
whether the Session alluded to by the ID passed in actually exists.

Again, the workflow provided in this method is provided as a labour
saving device for Session writers. All they have to do is prime the
instance variables of their object as _getSession expects, and write
the methods into their objects that _getSession is going to call.

this method also flags whether the Session is new or not, based on
whether the Session is created from scratch, or from a pre existing,
valid, ID


=item 5 B<setAttribute>

$session->setAttribute("-KEY"=>"firstname","-VALUE"=>"Gunther")

this is the method that sets a particular value in the Session object,
and marks the fact that the Session has been modified/accessed for
those Session objects that are tacking access/modify times.

The Session will only be marled as modified if the name/value pair
that are fed to this method were not already in the Session object

=item 6 B<getAttribute>

my $lastName = $session->getAttribute("-KEY"=>"lastname");

this is the method that pulls values back from the Session object, and
marks the object as accessed, for those objects that are tracking
access times.


=item 7 B<removeAttribute>

$session->removeAttribute("-KEY"=>"firstname");

removes the value specified by the -KEY argument from the Session
object, and marks the object as accessed modified, for those objects
that are tracking access/modification times.

=item 8 B<removeAttributes>

$session->removeAttributes();

clear out all user accessible name value pairs from the Session object

marks the object as accessed and modified, for those objects that are
tracking access/modification times.

=item 9 B<getAttributeNames>

my @names = $session->getAttributeNames();
foreach my $name(@names){
    print "name is $name, value is ",$session->getAttribute("-KEY"=>"$name"),"\n";
}

returns an array of all the publicly accessible keys to values in the
Session object. This class assumes that any key in the Session object
that is preceded by a "_", is a reference to a private value, and as
such, this method will not return it

marks the object as accessed, for those objects that are tracking
access times.

=item 10 B<getAttributes>

my @values = $session->getAttributes();
foreach my $value (@values){
    print "$value\n";
}

returns an array of all publicly accessible values that have been set
in the Session object. A value is considered to be publicly accessible
if the key that indexes it does not start with "_"

marks the object as accessed, for those objects that are tracking access times.

=item 11 B<_policyRead PRIVATE METHOD>

this method is responsible for refreshing the data that is being held
in the Session object, by forcing a read from the object's underlying
data repository [ eg disk,DB and so on ]. The method depends on the
'data_policy' instance variable of the Session object such that:

=over 4

=item 1 

A data policy of 1 means that all reads come from the data repository

=item 2

A data policy of 2 or 3 means that only the first data read is from
the data repository. All subsequent reads are from memory

=back

=item 12 B<_policyWrite PRIVATE METHOD>

acts in a very similar way to the B<_policyWrite> method described
above. This method is responsible for deciding when the Session object
ought to persist its data to an underlying data repository, and when
it should merely hold its state in memory. Again, the method reads the
'data_policy' instance variable of the Session object, so that:

=over 4

=item 1

A data policy of 1 or 2 means that all writes are persisted to the
data repository

=item 2 

a data policy of 3 means that only the the object only persists its
state to the data repository on global destruction. But thats not the
end of the world ;)

=back

=item 13 B<_hasDataChanged PRIVATE METHOD>

this method is used by the Session object in order to determine when
it ought to bother writing itself to the underlying data repository
. The method checks the name/value pairs currently in the Session
object, compared to the name/value pairs that were in the object at
the time it was last written. A discrepancy between these 2 things
means that something has changed, and therefore the object needs to
write itself out.

=item 14 B<DESTROY PRIVATE METHOD>

global destructor - writes the object to its data repository in cases
of a 'data_policy' of 3.

Also checks to see if the Session object has an instance variable
called '_lock'. If it DOES, it assumes that this is a lock object,
which is no longer needed as the object is about to go out of
scope. It therefore calls destoryLock() on the lock object. [ ie
$self->{'_lock'}->destroyLock() ]


=item 15 B<_getHash PRIVATE METHOD>

private method to generate unique session id. Works in conjunction
with method ......


=item 16 B<_hash PRIVATE METHOD>

does the actual work of generating and returning the session id

=item 17 B<_checkValidity PRIVATE METHOD>

this is the method that the Session object uses to check to see if a
given session is still valid, or it has expired on the basis of the
last time it was accessed/modified, or when it was created.

Session objects that have timed out have their invalidate method
invoked. A Session is only checked against a given criteria [ ie
access time, modification time or creation time ] if

=over 4

=item 1

the Session is tracking those actions on it

=item 2

the Session has been set with a maximum value for the category [ ie
max_access_time, and so on ]

=item 3

the Session implements methods that are capable of handing back
defined values in order to determine last accessed time, last modified
time and creation time, and so forth.

=back

=item 18 B<setMaxInactiveInterval>

$session->setMaxInactiveInterval("-AGE"=>"3600")

sets the maximum length of time permissable [ in seconds ] between
accesses to this Session object. Invoking this method will immediately
call _checkValidity, to see if the Session has timed out as a result
of the modification

=item 19 B<_setLastModifiedTime PRIVATE METHOD>

this is the internal method used by the Session object to keep track
of changes to its data. By default this data is written to a value
indexed by "_MODIFY_TIME" in the Session object. The object itself
determines, at various points through its lifecycle, what constitues a
modification, and calls this method accordingly. This is only the case
for Session objects that are tracking modifications though.
 
=item 20 B<getLastModifiedTime>

my $time = $session->getLastModifiedTime();

Returns the time() that the Session had its key/value pairs last
modified. The result of calling this method on a Session object that
is not tracking modification times is that the object will confess()


=item 21 B<_setLastAccessedTime PRIVATE METHOD>

this is the internal method used by the Session object to keep track
of accesses to its data. By default this data is written to a value
indexed by "_ACCESS_TIME" in the Session object. The object itself
determines, at various points through its lifecycle, what constitues
an access, and calls this method accordingly. This is only the case
for Session objects that are tracking accesses though.
 

=item 22 B<getLastAccessedTime PRIVATE METHOD>

my $time = $session->getLastAccessedTime();

Returns the time() that the Session had its key/value pairs last
accessed. The result of calling this method on a Session object that
is not tracking access times is that the object will confess()


=item 23 B<_setCreationTime>

sets the "_CREATION_TIME" private instance variable of new Session
objects. It is important to note the fact that this is for new Session
objects only. If a Session object is created with its 'track_create'
flag set to false, this method will never be called subsequently on
this object, because the object will only ever be considered as new
the first time it is created.

=item 24 B<getCreationTime>

returns the time() that the Session was created, if the Session was
tracking its creation time when it came into existence.


=item 25 B<getMaxInactiveInterval>

my $mii = $session->getMaxInactiveInterval(); returns the maximum
number of seconds permissable between accesses to the Session object


=item 26 B<_obtainLock PRIVATE METHOD>

for those Sessions that are interested in obtaining locks at key
points during their lifecycle [ such as when they persist themselves
to the data repository, or when they invalidate themselves, and are
removed from the data repository ], this method is a convenience.

The Session object sets preferences in the form of instance variables
which determine what type of lock is going to be obtained, and then
this method does all the work as far as obtaining the lock is
concerned.

this method caches the lock object that it creates in an instance
variable in the Session object called '_lock' , to save it creating
new locks all then time. If the '_lock' variable is already defined,
then this method simply returns the lock object that it references,
having first obtained a lock on it.


=item 27 B<isNew>

my $bool = $session->isNew();
 
returns a boolean to signify whether this session is new or not.

=item 28 B<isNew>

my $id = $session->getId();

returns the unique ID that references this Session object

=item 29 B<setMaxModifyInterval>

$session->setMaxModifyInterval("-AGE"=>"3600")

Like setMaxInactiveInterval. This method sets the maximum permitted
time between modifications to the Session object

=item 30 B<getMaxModifyInterval>

my $mmi = $session->getMaxModifyInterval();

returns the maximum length of time permissable between modifications
to the Session object

=item 31 B<setMaxCreationInterval>

$session->setMaxCreationInterval("-AGE"=>"3600")

Like setMaxInactiveInterval. This method sets the maximum permitted
time between when the Session is created, and when it is used

=item 32 B<getMaxCreationInterval>

my $mci = $session->getMaxCreationInterval();

returns the maximum length of time permissable between when the
Session was created, and when it is going to expire.

=head1 B<PACKAGE Session::TiedHashRepresentation>

B<ALL METHODS IN THIS PACKAGE ARE PRIVATE>

=item 1 B<TIEHASH>

the package constructor. It takes a reference to a Session object that
it is going to be used in conjunction with, and to which it is going
to defer all data centric operations.

=item 2 B<FETCH>

defers data access to the getAttribute() method of the Session object,
unless the developer has requested session_id, or the Session object
itself.


=item 2 B<STORE>

defers data storage to the setAttribute() method of the Session object

=item 3 B<DELETE>

defers removal of a key/value pair to the removeAttribute() method of
the Session object

=item 4 B<CLEAR>

defers removal of all public key/value pairs from the Session object
to its removeAttributes()

=item 5 B<EXISTS>

checks to see if the key specified results in the Session object
returning a defined value from its getAttribute() method

=item 6 B<FIRSTKEY>

returns the first key of the Session object's _data_cache

=item 7 B<NEXTKEY>

returns the next key from the Session object's _data_cache

=head1 B<PACKAGE Session::File>

This subclass of Session::Base is responsible for the storage of
Session based information in a File store.

=item 1 B<new PRIVATE METHOD>

The constructor of the Session object. It accepts the following
parameters for Session creation:

=over 4

=item 1 B<-SESSION_ID>

if you have the ID of a pre existing session that you want to use,
then it can be passed as an argument to the constructor, and will be
used to recreate the old Session

=item 2 B<-SESSION_FILE_EXTENSION> 

this is the file extension that Session files are going to be give
when they are stored. The default value is "ses" . The code will
insert the "." in the file extension for you, there is no need to
include it [ ie pass in, for example "session_file" as an extension,
not ".session_file" ]

=item 3 B<-CREATE_NEW_SESSION>

forces the creation of a new Session object. Default is false. If this
is set to true, then any pre-existing session ID that is passed in
will be ignored, and a new Session WILL be created
 
=item 4 B<-ONLY_USE_EXISTING_SESSION>

forces the use of a pre existing Session. Default is false. If this is
set to true, an ID HAS to be passed in to the Session as a
construction parameter - new Sessions will NOT be created

=item 5 B<-SESSION_DIR>

This is the file path to the location where Session objects are going
to be stored. By default, the object looks for a /tmp or a /temp
directory - although this is subject to the parameter that is passed
in by the user. The Session object has to find either /tmp or /temp,
or be passed a valid directory by the user, or it will throw an
Exception

=item 6 B<-SESSION_ID_LENGTH>

This determines the length of the unique ID that is going to be
created as the handle to the Session object. The default is 16 chars

=item 7 B<-SESSION_CREATE_MAX_TRIES>

this is the maximum number of times that the Session object is going
to try to bind to its underlying File data store. The default is 5
attempts, after which the object will confess()

=item 8 B<-SESSION_SECRET_KEY>

the string that is going to be incorporated into the hashing algorithm
that generates the Session object's unique ID. The default
is.....lame.

=item 9 B<-DATA_POLICY>

This is the parameter that determines how the object reads and writes
to and from its data store. How the data policy is used is determined
by functionality in the Session::Base superclass. See ante for
details. The default value for the data policy is 1

=item 10 B<-MAX_ACCESS_TIME>

The maximum length of time the Session is going to allow between
accesses to it. The default is 3600 seconds.


=item 11 B<-MAX_MODIFY_TIME>

The maximum length of time the Session is going to allow between
modifications to it. The default is 3600 seconds.

=item 12 B<-MAX_CREATION_TIME>

this effectively determines the basic lifespan of the Session
object. It specifies how long a Session object remains valid after
creation. The default is 3600 seconds.

=item 13 B<-ENABLE_MD5>

specifies whether the MD5 module's functionality is going to be used
during the creation of the unique ID of the Session object. The
default is false

=item 14 B<-LOCK_PARAMS>

this specifies the parameters that are going to be used if the Session
object ever needs to obtain a lock before operating on its data. The
-LOCK_PARAMS argument needs to be a reference to an array, and can
contain in turn the following values :

=over 8

=item 1 B<-TYPE>

the type of lock that the Session object is going to use. Default is
File.

=item 2 B<-FILE>

the name of the File that the Session object is going to lock on. The
default is <session_id>.<session_file_extension>.lock

=item 3 B<-TIMEOUT>

the maximum length of time that the Session object will attempt to
obtain a lock on the lock file for, before giving up. Default is 120
seconds

=item 4 B<-TRIES>

The maximum number of attempts that the Session object will make at
obtaining the file lock, within the specified -TIMEOUT, above. The
default is 20

=back


=item 15 B<-TRACK_ACCESS_TIME>

whether the Session is interested in marking the times it is accessed,
or timing out on the basis that its MAX_ACCESS_TIME has been
exceeded. The default for this value is true.

=item 16 B<-TRACK_MODIFY_TIME>

whether the Session is interested in marking the times it is modified,
or timing out on the basis that its MAX_MODIFY_TIME has been
exceeded. The default for this value is true.

=item 17 B<-TRACK_CREATION_TIME>

Determines whether a new Session is going to mark the time of its
creation . Please note that setting this flag to false when the
Session is first created means that the Session will NEVER mark its
creation time - only new Sessions can do this. A related effect is
that a Session that has not had its creation time marked can never
time out on the basis of the -MAX_CREATION_TIME specified above - as
there is no creation time for the Session to compare against.

=back

=item 2 B<_doesSessionExist PRIVATE METHOD>

Checks that a pre existing session ID maps to a valid Session file.

=item 3 B<_createSession PRIVATE METHOD>

creates the file that the Session object is going to be bound to as a
datasource. The -SESSION_CREATE_MAX_TRIES parameter [ ante ]
determines how many attempts will be made to create the file before
the method fails


=item 4 B<_writeSession PRIVATE METHOD>

The means by which the object actually persists itself to File.

=item 5 B<_readSession PRIVATE METHOD>

The means by which the file reconstitutes its state from its from file
that it is bound to.


=item 6 B<_makeSessionFileName PRIVATE METHOD>

The method that returns the fully qualified path to the file that is
going to be used to store the Session object's data


=item 7 B<_getSessions PRIVATE METHOD>

this is a static method that is responsible for recreating all the
Session objects that are stored in the session directory, and
returning them as an array of objects

=item 8 B<_invalidateOldSessions PRIVATE METHOD>

this method is responsible for invalidating all Sessions that have
exceeded the maximum length of inactivity according to any of the
access time, modify time or creation time parameters that have been
specified.

=item 9 B<invalidate>

$session->invalidate();

responsible for removing the Session object's underlying file
repository.

=item 10 B<_getLockFileName PRIVATE METHOD>

This method returns the name of the file that the Session object
specifies for use in all locking operations.


=item 11 B<_setLastAccessedTime PRIVATE METHOD>

this method initiates an access of the underlying Session file -
effectively by doing little more than opening and closing it again.


=item 12 B<getLastAccessedTime>

my $lat = $session->getLastAccessedTime();

returns the last time that the file was accessed. Achieved through the
use of perl's file access test operator

=item 13 B<_setLastModifiedTime PRIVATE METHOD>

this method is overidden to do nothing, the reason being that the
filesystem that stores the underlying Session object will keep track
of changes to the file on its own

=item 14 B<getLastModifiedTime>

my $lmt = $session->getLastModifiedTime();

returns the time the Session's underlying file object was last
modifed, through use of perl's file modification test operator

=item 15 B<getTiedHash>

my $hashref = $session->getTiedHash();

returns a reference to the underlying tied hash that the Session
contains on, for those who are more comfortable using a hash data
structure for data storage/retrieval. The object is of type
Session::TiedHashRepresentation. See the documentation above.

=head1 B<PACKAGE Session::ApacheFile>

B<OVERVIEW>

From here onwards, the remaining modules are little more than a
variation on a theme really. Session::File's documentation explained
the methods that were used to persist Session data to an underlying
filestore. The Session::ApacheFile module is a wrapper around an
Apache::Session::File object. Seeing as the latter class already
implements so much of the functionality that we are interested in, all
that the Session::ApacheFile class really has to do is encapsulate it,
add a few things, but in the main, simply massage the
Apache::Session::File's API, to that of the Session class

item 1 B<new PRIVATE METHOD>

The constructor. Takes the following configuration parameters:

-SESSION_ID,
-SESSION_DIR,
-MAX_ACCESS_TIME,
-MAX_MODIFY_TIME,
-MAX_CREATION_TIME,
-TRACK_ACCESS_TIME,
-TRACK_MODIFY_TIME,
-TRACK_CREATION_TIME,
-SESSION_CREATE_MAX_TRIES,
-DATA_POLICY

in all cases, the default values of these parameters, and the effect
that they have on the behaviour of the Session object is as detailed
in the Session::File documentation above

The only other point worth noting is that Session::ApacheFile
constructor does not make use of the Session::Base class _getSession
method in order to create its Session. This is because all the
workflow/functionality involved in the creation of a new Session's
file store is performed by the encapsulated Apache::Session::File's
constructor. This class is just a wrapper.

B<EXCEPT WHERE OTHERWISE STATED, ALL THE FOLLOWING METHODS HAVE THE
SAME FUNCTIONALITY AS THE CORRESPONDING METHODS IN Session::File>

=item 1 B<getLastModifiedTime>

=item 2 B<_setLastModifiedTime PRIVATE METHOD>

=item 3 B<getLastAccessedTime>

=item 4 B<_setLastAccessedTime PRIVATE METHOD>

=item 5 B<getCreationTime>

=item 6 B<_setCreationTime PRIVATE METHOD>

=item 7 B<_makeSessionFileName PRIVATE METHOD>

=item 8 B<invalidate>

=item 9 B<_readSession PRIVATE METHOD>

this method delegates all functionality to the contained Apache::Session::File object

=item 9 B<_writeSession PRIVATE METHOD>

this method delegates all functionality to the contained Apache::Session::File object

=item 10 B<_getSessions PRIVATE METHOD>

=item 11 B<_invalidateOldSessions PRIVATE METHOD>

=item 12 B<getTiedHash>

returns a reference to the underlying tied Apache::Session::File hash

B<PACKAGE Session::ApacheDBI>

Again, in a similar vein to Session::ApacheFile, this class does
little except to massage and complement the API presented by
Apache::Session::DBI, an object of which type is instantiated,
contained, and manipulated within objects of this type

this class is concerned with binding the data in a Session object to
an underlying database data store. Seeing as this class is Database
based, it relies on the methods on the superclass, Session::Base, to
maintain information about when it was accessed/modified/created. This
is in contrast to the preceding 2 Session objects, Session::File and
Session::ApacheFile, which could rely on Perl built in file test
operators for this functionality

=item 1 B<new PRIVATE METHOD>

The constructor. Takes the following configuration parameters:

	-SESSION_ID,
	-DATASOURCE,
	-USERNAME,
	-PASSWORD,
	-SESSION_CREATE_MAX_TRIES,
	-DATA_POLICY,
	-TRACK_ACCESS_TIME,
	-TRACK_MODIFY_TIME,
	-TRACK_CREATION_TIME,
	-MAX_ACCESS_TIME,
	-MAX_MODIFY_TIME,
	-MAX_CREATION_TIME,

in all cases, the default values of these parameters, and the effect
that they have on the behaviour of the Session object is as detailed
in the Session::File documentation above.

B<The Database connection>

the only additional parameters above are B<-DATASOURCE> B<USERNAME>
and B<PASSWORD>. DATASOURCE is the connection string that is going to
be used in order to establish the DB connection. See the perldoc on
DBI for more details. A sample string would be something like:

dbi:[driver name, eg Sybase]:server=[server name];database=[database name].

USERNAME and PASSWORD, predictably enough are going to be used to
perform validation at the Database with

There is a problem with using Sybase DBs in conjunction with the
Apache::Session::DBI class, as it relies in certain cases, on the
preparation of cached statements in the DB. Sybase will not allow this
for certain column data types. If the Session::ApacheDBI class detects
an attempt to connect to a sybase datasource, it will make use of the
Apache::Session::DBI::Sybase module instead. This was kindly sent to
me by B<Mark Landry (mdlandry@lincoln.midcoast.com)>, thus saving MUCH
headache.

for details of what columns and datatypes you need to set up in your
DB to use this module, please see the documentation for
Apache::Session::DBI and Apache::Session::DBI::Sybase

Like Session::ApacheFile, the constructor of Session::ApacheDBI does
make use of its superclass's [ Session::Base] _getSession method in
order to create the actual Sessions's data representation.

B<EXCEPT WHERE OTHERWISE STATED, ALL THE FOLLOWING METHODS HAVE THE
SAME FUNCTIONALITY AS THE CORRESPONDING METHODS IN Session::File>

=item 2 B<invalidate>

=item 3 B<_readSession PRIVATE METHOD>

Delegates all functionality to the Apache::Session::DBI object that it wraps

=item 4 B<_writeSession PRIVATE METHOD>

Delegates all functionality to the Apache::Session::DBI object that it wraps

=item 5 B<_getSessions PRIVATE METHOD>

=item 6 B<_invalidateOldSessions PRIVATE METHOD>

=item 7 B<getTiedHash>

returns a reference to the underlying tied Apache::Session::DBI object. 

=cut
