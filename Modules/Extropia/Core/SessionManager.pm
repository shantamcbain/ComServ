#$Id: SessionManager.pm,v 1.7 2001/05/23 01:46:23 gunther Exp $
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

package Extropia::Core::SessionManager;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrange _getDriver _rearrangeAsHash);
use Extropia::Core::Session;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.7 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $session_manager_class = 
        Extropia::Core::Base::_getDriver("Extropia::Core::SessionManager", $type) or
        Carp::croak("Extropia::Core::SessionManager type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $session_manager_class->new(@fields);
}

#
# Drivers must implement the following methods
#
# createSession
# _extractSessionID
# invalidateOldSessions
# getSessions
#

sub createSession {
    my $self = shift;
    my $session_id = $self->_extractSessionId();

    my $session;
    my $untaint;

# the session id itself must be untainted...
# 
# It is OK to untaint based on just word characters as this will not
# allow different files to be written (eg no file extensions are 
# designated as part of the session id... and no shell meta characters
# for traversing directory structures.
#
    if ($session_id) {
        if($session_id =~ /^([\w\-]+)$/){
            $session_id = $1;
        } else {
            confess ("Session ID: $session_id could not be untainted!");
        }
    }

    if ($session_id) {
# Invalidation of sessions that occurs before the attempt
# to get an existing session.
        if ($self->{-INVALIDATE_OLD_SESSIONS_AT_GET_SESSION}) {
            $self->invalidateOldSessionsByProbability();
        }
        eval {
            $session = 
                Extropia::Core::Session->create(-SESSION_ID=>$session_id,
                                    @{$self->{-SESSION_PARAMS}});
        };
        my $error;
        if ($@) {
            $error = 1;
        } else {
            $error = $session->getLastError();
        }
# Let's create a brand new session from scratch if it failed to create one with an existing session id...
        if (defined($error)) {
            $session = 
                Extropia::Core::Session->create(@{$self->{-SESSION_PARAMS}});
            $self->_changeSessionId($session->getId());
# set up a meta data related to session handling
            $self->{_previous_session_id_was_invalid} = 1;
        }
          
    } else {
# Invalidation of sessions that only occurs if a session is created from scratch
        if ($self->{-INVALIDATE_OLD_SESSIONS} ||
            $self->{-INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION}) {
            $self->invalidateOldSessionsByProbability();
        }
        $session = Extropia::Core::Session->create(@{$self->{-SESSION_PARAMS}});
    }

    return($session);
}

#
# Uses the probability setting to determine
# whether to invalidate old sessions...
#
sub invalidateOldSessionsByProbability {
    my $self = shift;

# Get probability of when session invalidation will
# be run. The default is to run session cleanup
# 1% of the time.
    my $probability = $self->{-INVALIDATE_OLD_SESSIONS_PROBABILITY};
    $probability = 1 unless defined $probability;
    
#
# If the probability falls outside of the random
# generated percent, then do nothing and
# return immediately without garbage collecting
# any sessions
#
    my $rand_percent = int(rand(100)) - 1;
    if ($rand_percent > $probability) {
        return undef;
    }

#
# Garbage collection the sessions since we 
# passed the probability test.
#
    return $self->invalidateOldSessions();

} # end of invalidateOldSessionsByProbability

sub invalidateOldSessions {
    my $self = shift;

    my $hash_ref;
    ($hash_ref) = _rearrangeAsHash([-TYPE], [-TYPE], 
                         @{$self->{-SESSION_PARAMS}});
    my $type = $hash_ref->{-TYPE};
    my $package = "Extropia::Core::Session::$type";

    require "Extropia/Core/Session/$type.pm";
    return ($package->_invalidateOldSessions(@{$self->{-SESSION_PARAMS}}));
} 

sub getSessions {
    my $self = shift;

    my $hash_ref;
    ($hash_ref) = _rearrangeAsHash([-TYPE], [-TYPE], 
                         @{$self->{-SESSION_PARAMS}});
    my $type = $hash_ref->{-TYPE};
    my $package = "Extropia::Core::Session::$type";

    require "Extropia/Core/Session/$type.pm";
    return ($package->_getSessions(@{$self->{-SESSION_PARAMS}}));
}

# Adding API to allow someone to query the session manager and find
# out whether the originally created session was invalid.
sub wasPreviouslyCreatedSessionInvalid {
    my $self = shift;

    return 1 if ($self->{_previous_session_id_was_invalid});

    return 0;

} # end of wasPreviousSessionIdInvalid

sub _changeSessionId {
    my $self = shift;

# By default this is empty... a subclass such as formvar needs to clear the
# session id from the list of values that CGI.pm has so that they do not remain
# sticky in external modules such as AuthManager::CGI

}

1;

__END__

=head1 OVERVIEW

If you want to know the motivation for writing these classes, and how they all fit together, then please read the Session object's POD first, as this lays this all out.

If you have already done that, then the question that is probably at the forefront of your mind is how to actually CREATE a Session object, seeing as so many objects in the Session class itself are marked as private.

This, as the Session documentation states, is the role of the SessionManager object. The basic workflow that you are looking at is:

=over 4

=item 1 

create a SessionManager object

=item 2 

use the SessionManager object to create a new, or recreate an old, Session B<OR>

=item 3

use it to perform admin functions such as creating an enumeration of all Sessions, or invalidate old sessions.

The Classes work out essentially as follows:


=head1 B<PACKAGE SessionManager>

the abstract superclass of all the Session objects. It has the following methods:

=item 1 B<create>

my $sessionmanager = Extropia::Core::SessionManager->create ("-TYPE"=>"session manager type","-SESSION_PARAMS"=>["-TYPE"=>"session type"]);

the first TYPE argument above specifies the type of SessionManager that you need to create. The currently supported categories are:

=over 4

=item 1 B<Cookie>

=item 2 B<PathInfo>

=item 3 B<Default>

=item 4 B<FormVar>

=back

the list of parameters that the Session object is going to be fed is contained in the array reference indexed by -SESSION_PARAMS. The only thing that has to be contained in this list is the -TYPE flag, so as to inform the SessionManager what type of Session it is going to have to create.

As far as the other members of the -SESSION_PARAMS array is concerned, please see the documentation on the Session class, and all its subclasses, as this will tell you what parameters ease particular type of session expects to receive

=item 2 B<createSession>

=item 3 B<_extractSessionId PRIVATE METHOD>

=item 4 B<invalidateOldSessions>

=item 5 B<getSessions>

=item 6 B<printSession>

=head1 B<PACKAGE SessionManager::Base>

a concrete implementation of the Session class

=item 1 B<createSession>

my $manager = Extropia::Core::SessionManager->create
        (
                "-TYPE"                 =>      "Default",
                "-SESSION_PARAMS"       =>
                [
                        "-TYPE"         =>      "File",
                ]
        );

my $session = $manager->createSession()

the method to actually create a Session object. Again, please see the Session documentation for a list of the paramters that a Session of a given type can accept. This method works in conjunction with the _extract_session_id that is mentioned next, because the SessionManager object may be asked to recreate an old Session, as well as create a new one. If it is asked to recreate an old Session, it has to have some way of extracting the Session id that it is passed.

the other function that this method fulfils is to call the the method _printSession in the SessionManager object, after the Session is created, and before it is handed back, but ONLY if the instance variable 'print_session' has been set to true in the SessionManager object. Sessting this instance variable is the responsibility of the subclass that extends SessionManager::Base. Currently, the use of this functionality is only used by SessionManager::Cookie [ see post ]

=item 2 B<_extractSessionId PRIVATE METHOD>

This method is responsible for parsing the construction parameters passed to the SessionManager object upon creation, and pulling out the Session ID, if one has been passed in. SessionManagers of different types, [ eg Cookie, FormVar and so on ] perform this function differently. Further documentation about each of these classes is given further on.

=item 3 B<invalidateOldSessions>

my $manager = Extropia::Core::SessionManager->create
        (
                "-TYPE"                 =>      "Default",
                "-SESSION_PARAMS"       =>
                [
                        "-TYPE"         	=>      "File",
			"-MAX_ACCESS_TIME"	=>	1800
                ]
        );
$manager->invalidateOldSessions();

remove all Session objects of a particular type that have not been accessed/modified for a certain length of time, or that were created more than a certain length of time ago - depending on -SESSION_PARAMS .

The above example removes all File based Session objects that were last accessed over 1800 seconds ago.


=item 4 B<getSessions>

my $manager = Extropia::Core::SessionManager->create
        (
                "-TYPE"                 =>      "Default",
                "-SESSION_PARAMS"       =>
                [
                        "-TYPE"         	=>      "File",
			"-MAX_ACCESS_TIME"	=>	1800
                ]
        );
my @sessions = $manager->getSessions();
foreach(@sessions)
{
	print $_->getId(),"\n";
}

the method by which an array of Session objects in existence is returned


=item 5 B<_callStaticSessionMethod>

The fact of the matter is that a SessionManager does not have any knowledge of the the mechanism by which a Session object of a particular type [ eg File, DBI ] ought to be removed, or how to search for all Sessions of a particular type, and recreating them. SessionManagers have no concept of referencing the File system, or a Database. As a result, when a Session Manager is asked to perform admin functions such as invalidateOldSessions() or getSessions(), what it actually does is to delegate the work to the Session class's matching static methods.

In order to do this, the SessionManager has to have a method by which it can call the static methods in the class of Session object for which it is being asked to carry out the function, for example the Session::DBI's _invalidateOldSessions method, for example. 

This method provides the functionality by which this class can make those calls


=head1 B<PACKAGE SessionManager::Cookie>

B<OVERVIEW>

this package provides the ability for the application developer to pass in a CGI object that contains a Session object's ID in a cookie, and this class will extract that ID and recreate the old Session.

=item 1 B<new>

The object constructor. Accepts the following parameters [ those marked with an * are mandatory ]

-CGI_OBJECT *
-COOKIE_VAR_NAME [ by default set to 'session_id']
-SESSION_PARAMS
-COOKIE_DOMAIN
-COOKIE_PATH
-COOKIE_EXPIRES
-PRINT_SESSION

so, to create a SessionManager::Cookie object, 

my $manager = Extropia::Core::SessionManager->create
		(
			-TYPE		=>	"Cookie",
			-CGI_OBJECT	=>	$CGI,
			-SESSION_PARAMS	=>
			[
			]
		);

The SessionManager::Cookie class also deals with the functionality of printing the Session object to STDOUT
as a cookie, thereby setting the session id in the browser without the application develper having to write the cookie code.

The role that the constructor plays in this process is to set the instance variable 'print_session' to true if the CGI_OBJECT that has been passed in does not contain a valid session_id [ in which case it is assumed that  a new session is being created ].

This is subject to whatever value the user passes in with the -PRINT_SESSION flag. If the object sets 'print_session' to true, then the superclass, Session::Base, within its createSession method, will detect this, and call the SessionManager::Cookie's _printSession method.

All the "-COOKIE" preceded options are going to be passed straight through as is to the CGI module for the creation of a cookie. See the CGI docs for details.

The only "-COOKIE..." parameter that is given a default parameter is -COOKIE_PATH. If this is not specified by the user, it is taken to be $ENV{'SCRIPT_NAME'}, minus the actual name of the script. This is proabaly going to resolve to your cgi-bin directory by default. 

=item 2 B<_extractSessionId>

this is the method that is going to search the cookie contained in the -CGI_OBJECT [ ante ] for a session id that is referenced by the key -COOKIE_VAR_NAME.

The _extractSessionId method is going to be called when someone actually uses the SessionManager object's createSession() method.

It is perfectly acceptable for this method to return undef [ is there is no session_id in the CGI_OBJECT's cookie's COOKIE_VAR_NAME field ]. This will result in the createSession method creating a new Session object

=item 3 B<_printSession>

this method creates a cookie from the parameters passed in during the construction of the SessionManager object, and prints it out. It extracts the id of the Session from the Session object that it is passed.

=head2 B<PACKAGES SessionManager::PathInfo,SessionManager::FormVar, SessionManager::Default>

Once you have understood how SessionManager::Cookie works, then the rest of these classes become easy. As SessionManager::Cookie is responsible for extracting session ids from Cookies in CGI objects, SessionManager::FormVar extracts them from FormVariables, SessionManager::PathInfo from the path information contained in the CGI object, and Default does not have to perform any extraction at all, because it is passed the session id as plain text.

So, where SessionManager::Cookie takes -CGI_OBJECT,-COOKIE_VAR_NAME and -SESSION_PARAMS,

=over 4

=item 1

SessionManager::FormVar takes -FORM_VAR_NAME instead of -COOKIE_VAR_NAME. This determines the name of the form field within the -CGI_OBJECT that it is going to extract session id from. By default it is set to 'session_id'

=item 2

SessionManager::PathInfo takes -PATH_INFO_FIELD, which specifies the field within the path info of the CGI_OBJECT that it is going to try and extract the session id from. The default value is 1

=item 3 

SessionManager::Default does not take any construction params except -SESSION_PARAMS and -SESSION_ID. When asked to extract the session id, in its _extractSessionId method, all it does is hand back this latter value.
