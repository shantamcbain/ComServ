#$Id: LDAP.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Auth::LDAP;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Auth;
use Extropia::Core::Encrypt;
use Mozilla::LDAP::Conn;
use Mozilla::LDAP::Entry;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -DEFAULT_GROUPS,
       -ENCRYPT_PARAMS,
       -ADD_REGISTRATION_TO_LDAP,
       -USER_FIELDS_TO_LDAP_MAPPING,
       -MEMBER_FIELD_TO_LDAP_MAPPING,
       -AUTH_CACHE_PARAMS,
       -LDAP_SERVER_NAME,
       -LDAP_SERVER_PORT,
       -LDAP_SERVER_BASE,
       -LDAP_SERVER_SCOPE,
       -LDAP_BIND_DN,
       -LDAP_BIND_PASSWORD,
       -LDAP_CERT,
       -CACHE_LDAP_CONNECTION,
       -USERNAME_NOT_FOUND_ERROR,
       -PASSWORD_NOT_MATCHED_ERROR,
       -DUPLICATE_USERNAME_ERROR
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -LDAP_SERVER_NAME
    ],
    @_);

    $self = _assignDefaults($self,
                   {
                    -ADD_REGISTRATION_TO_LDAP    => 0,
                    -USER_FIELDS_TO_LDAP_MAPPING => 
                      {'auth_username' => 'uid',
                       'auth_password' => 'password'},
                    -MEMBER_FIELD_TO_LDAP_MAPPING =>
                      'member', # could be uniqueMember for Netscape
                    -AUTH_CACHE_PARAMS  => [-TYPE => 'None'],
                    -LDAP_SERVER_PORT   => '389',
                    -LDAP_SERVER_BASE   => '',
                    -LDAP_SERVER_SCOPE  => 'sub',
                    -LDAP_BIND_DN       => '',
                    -LDAP_BIND_PASSWORD => '',
                    -LDAP_CERT          => '',
                    -CACHE_LDAP_CONNECTION => 1
                   });

    bless $self, ref($package) || $package;

    $self->_init();

    return $self;
}


sub _connectToLDAP {
    my $self = shift;

    my $ldap_server_name   = $self->{'-LDAP_SERVER_NAME'};
    my $ldap_server_port   = $self->{'-LDAP_SERVER_PORT'};
    my $ldap_bind_dn       = $self->{'-LDAP_BIND_DN'};
    my $ldap_bind_password = $self->{'-LDAP_BIND_PASSWORD'};
    my $ldap_cert          = $self->{'-LDAP_CERT'};

    my $conn = new Mozilla::LDAP::Conn ($ldap_server_name,
                                        $ldap_server_port,
                                        $ldap_bind_dn,
                                        $ldap_bind_password,
                                        $ldap_cert);
    if (!$conn) {
        die("LDAP Server: $ldap_server_name could not connect");
    }
    return $conn;

} # end of _connectToLDAP

sub _closeLDAP {
    my $self = shift;

    if ($self->{_ldap_connection} &&
        !$self->{-CACHE_LDAP_CONNECTION}) {
        $self->{_ldap_connection}->close();
        $self->{_ldap_connection} = undef;
    }
}

sub DESTROY {
    my $self = shift;

    if ($self->{_ldap_connection}) {
        $self->{_ldap_connection}->close();
        $self->{_ldap_connection} = undef;
    }
} 

sub _retrieveAuthDataStore {
    my $self = shift;
    @_ = _rearrange([-USERNAME],[-USERNAME],@_);

    my $username = shift;

    if ($username eq $self->{_username_parameter}) {
        return $self->{_data_store};
    }
    
    my $ldap_server_base  = $self->{-LDAP_SERVER_BASE};
    my $ldap_server_scope = $self->{-LDAP_SERVER_SCOPE};

    my $field_map = $self->{-USER_FIELDS_TO_LDAP_MAPPING};
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
    my $ldap_username = $field_map->{$username_field};
    my @attr_list = ("dn");
    my $field;
    foreach $field (@{$self->{-USER_FIELDS}}) {
        if ($field ne $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD}) {
            push @attr_list, $field_map->{$field};
        }
    }
    
    my $conn = $self->_connectToLDAP();
    my $search_term = $ldap_username . "=" . $username; 

    my $entry = $conn->search ($ldap_server_base,
                               $ldap_server_scope,
                               $search_term,
                               0,
                               @attr_list);

    $self->_closeLDAP();

    if (!$entry) {
        $self->addError(
                sprintf($self->{-USERNAME_NOT_FOUND_ERROR},$username));
        return undef;
    }

    $self->{_data_store} = $entry;
    return $entry;
}

# In the context of the Auth Module
# authenticate takes a username and password and checks to
# see if a problem has occurred
# 
# If the logon is successful, then that information is
# cached for further querying by the AuthManager object
#
# If the logon fails it is either because the username does
# not match an existing one or because the password failed to match
# 
# If password is undef, then it is assumed that the authentication
# is merely trying to get the user information for passing back to
# the authentication manager which may be managing security issues
#
# returns a true if successful, false if not.
# 

sub authenticate {
    my $self = shift;
    my ($params) = _rearrangeAsHash(
                  [-USERNAME,-PASSWORD],
                  [-USERNAME,-PASSWORD],
                  @_
                 );

    # local params
    my $username       = $params->{-USERNAME};
    my $password       = $params->{-PASSWORD};
    
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};

    # global params

    my $field_map     = $self->{-USER_FIELDS_TO_LDAP_MAPPING};

    my $ldap_entry = $self->retrieveAuthDataStore(-USERNAME => $username);
    my $dn         = $ldap_entry->getDN();
    
    my $conn = $self->_connectToLDAP();
    if ((defined ($password)) && (($password eq '') || 
        (!$conn->simpleAuth ($dn, $password)))) {
        $self->addError(
                sprintf($self->{-PASSWORD_NOT_MATCHED_ERROR},$username));
        return undef;
    }
    $self->_closeLDAP();
    
    # OK, now we know that the user passed....
    $self->{"_user_authenticated"} = 1;
    
    $self->_prePopulateCache ();

    return 1;

} # end of authenticate

sub _rawIsMemberOfGroup {
    my $self = shift;
    @_ = _rearrange([-GROUP],[-GROUP],@_);

    my $group = shift;
    
    my $ldap_entry = $self->retrieveAuthDataStore();
    my $dn         = $ldap_entry->getDN();
    my $conn       = $self->_connectToLDAP();

    my $ldap_server_base  = $self->{-LDAP_SERVER_BASE};
    my $ldap_server_scope = $self->{-LDAP_SERVER_SCOPE};
    my $member            = $self->{-MEMBER_FIELD_TO_LDAP_MAPPING};

    my $field_map     = $self->{-USER_FIELDS_TO_LDAP_MAPPING};

    my $field = $field_map->{$self->{-USER_FIELD_TYPES}->{-GROUP_FIELD}};
    my $search_term = "(&(objectClass=$field)($member=$dn)(cn=$group))";
    my $group_entry = $conn->search ($ldap_server_base,
                                     $ldap_server_scope,    
                                     $search_term,
                                     0,
                                     ('cn'));

    my $is_member = 0;
    $is_member = 1 if ($group_entry);

    return $is_member;

} # end of # _rawIsMemberOfGroup

sub _getRawGroupList {
    my $self = shift;

    my $ldap_entry = $self->retrieveAuthDataStore();
    my $dn         = $ldap_entry->getDN();
    my $conn       = $self->_connectToLDAP();

    my $ldap_server_base  = $self->{-LDAP_SERVER_BASE};
    my $ldap_server_scope = $self->{-LDAP_SERVER_SCOPE};
    my $member            = $self->{-MEMBER_FIELD_TO_LDAP_MAPPING};

    my $field_map     = $self->{-USER_FIELDS_TO_LDAP_MAPPING};

    my $field = $field_map->{$self->{-USER_FIELD_TYPES}->{-GROUP_FIELD}};
    my $search_term = "(&(objectclass=$field)($member=$dn))";
    my $group_entry = $conn->search ($ldap_server_base,
                                     $ldap_server_scope,    
                                     $search_term,
                                     0,
                                     ('cn'));

    my @groups = ();

    while ($group_entry) {
        my %group_hash = %$group_entry;
        my @group_array = %group_hash;

        push(@groups, @{$group_entry->{'cn'}});
        $group_entry = $conn->nextEntry();
    }
    $self->_closeLDAP();

    return @groups;

} # end of _getRawGroupList

#
# _prePopulateCache prepopulates the cache with the 
# information passed to it.
#
sub _prePopulateCache {
    my $self = shift;
  
    my $auth_cache = $self->getAuthCacheObject();
    my $ldap_entry = $self->retrieveAuthDataStore();

    my $field_map     = $self->{-USER_FIELDS_TO_LDAP_MAPPING};

    my $field;
    foreach $field (@{$self->{-USER_FIELDS}}) {
        if ($field ne $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD} &&
            $field ne $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD}) {
            my $user_field = 
                $self->{-USER_FIELDS_TO_LDAP_MAPPING}->{$field};
            my $user_value = 
                ($ldap_entry->{$user_field}[0]);
            $auth_cache->setCachedUserField(-USER_FIELD => $field,
                                      -USER_VALUE => $user_value);
        }
    } 
} # end of _prePopulateCache

#
# _getRawUserField is a method that is called
# from getUserField(). It performs the raw work
# of getting to the authentication data lookup (eg DataSource
# or LDAP).
#
sub _getRawUserField {
    my $self = shift;
    @_ = _rearrange(
              [-USER_FIELD],[-USER_FIELD],@_);

    # local params
    my $user_field = shift;
    
    if ($user_field eq 
            $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD}) {
        return join(",",$self->_getRawGroupList());
    }

    # global params
    my $field_map = $self->{-USER_FIELDS_TO_LDAP_MAPPING};
    my $ldap_field_name = $field_map->{$user_field};

    my $username = $self->{_username_parameter};
    if (!defined($username)) {
# we haven't logged on yet...we may want to get/set session cache 
# data anyway...
        return undef;
    }
    my $rh_user_ldap_record = 
        $self->retrieveAuthDataStore(-USERNAME => $username);

    my $user_value = $rh_user_ldap_record->{$ldap_field_name}->[0];
    if (!$user_value) {
        confess(
            "$user_field could not be translated into an expected user value");
    }

    return $user_value;

} # end of _getRawUserField

#
# search
#
# search takes a user field and a value to search on
# and returns a list of usernames that satisfy this search
#
sub search {
    my $self = shift;
    @_ = _rearrange(
                [-USER_SEARCH_FIELD,
                 -USER_SEARCH_VALUE],
                [-USER_SEARCH_FIELD,
                 -USER_SEARCH_VALUE],@_);

    # params
    my $user_search_field    = shift;
    my $user_search_value    = shift;

    my $ldap_server_base  = $self->{-LDAP_SERVER_BASE};
    my $ldap_server_scope = $self->{-LDAP_SERVER_SCOPE};

    my $field_map = $self->{-USER_FIELDS_TO_LDAP_MAPPING};
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
    my $ldap_field = $field_map->{$user_search_field};

    my @attr_list = ("dn");
    my $field;
    foreach $field (@{$self->{-USER_FIELDS}}) {
        if ($field ne $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD}) {
            push @attr_list, $field_map->{$field};
        }
    }
    
    my $conn = $self->_connectToLDAP();
    my $search_term = $ldap_field . "=" . $user_search_value; 

    my $entry = $conn->search ($ldap_server_base,
                               $ldap_server_scope,
                               $search_term,
                               0,
                               @attr_list);

    $self->_closeLDAP();

    my @user_list = ();
    while ($entry) {
        push(@user_list,
                ($entry->{$field_map->{$username_field}}[0]));
        $entry = $conn->nextEntry();
    }

    return @user_list;

} # end of search

#
# register
#
# Allows a user to register into the authenticaton source...
#

sub register {

    die("User registration is not implemented yet.");

} # end of register

1;
