#$Id: DataSource.pm,v 1.2 2001/07/13 09:35:58 janet Exp $
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

package Extropia::Core::Auth::DataSource;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults _dieIfError);

use Extropia::Core::DataSource;
use Extropia::Core::Auth;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# new Auth::DataSource
#
sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -USER_DATASOURCE_PARAMS,
       -DEFAULT_GROUPS,
       -ENCRYPT_PARAMS,
       -ADD_REGISTRATION_TO_USER_DATASOURCE,
       -USER_FIELDS_TO_DATASOURCE_MAPPING,
       -AUTH_CACHE_PARAMS,
       -USERNAME_NOT_FOUND_ERROR,
       -PASSWORD_NOT_MATCHED_ERROR,
       -DUPLICATE_USERNAME_ERROR,
       -AUTH_CASE_SENSITIVE_SEARCH
    ],
    [
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -USER_DATASOURCE_PARAMS
    ],@_);

    $self = _assignDefaults($self,
                   {
                    '-ENCRYPT_PARAMS' => [-TYPE => 'Crypt'],
                    '-ADD_REGISTRATION_TO_USER_DATASOURCE' => 1,
                    '-USER_FIELDS_TO_DATASOURCE_MAPPING' =>
                      {'auth_username' => 'username',
                       'auth_password' => 'password'},
                    '-AUTH_CACHE_PARAMS' => [-TYPE => 'None']
                   });

    bless $self, ref($package) || $package;

    $self->_init();

    return $self;
}

sub _retrieveAuthDataStore {
    my $self = shift;
    @_ = _rearrange([-USERNAME],[-USERNAME],@_);

    my $username = shift;

    if ((defined($self->{_username_parameter}) &&
        $username eq $self->{_username_parameter}) &&
        $self->{_data_store}) {
        return $self->{_data_store};
    }

    my @ds_params =
      @{$self->{-USER_DATASOURCE_PARAMS}};

    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
    my $field_map      = $self->{'-USER_FIELDS_TO_DATASOURCE_MAPPING'};
    my $ds_username    = $field_map->{$username_field};

    my $ds = Extropia::Core::DataSource->create(@ds_params);
    _dieIfError($ds);

    my $search_term;
    if($self->{-AUTH_CASE_SENSITIVE_SEARCH}) {
      $search_term = $ds_username .
                                " == " . qq!"$username"!;

    } else {
      $search_term = $ds_username .
                                " =i " . qq!"$username"!;
    }


    my $record_set = $ds->search($search_term);
    _dieIfError($ds);

    $record_set->moveFirst();
    if ($record_set->endOfRecords()) {
        $self->addError(
                sprintf($self->{-USERNAME_NOT_FOUND_ERROR},$username));
        return undef;
    }

    my $rh_record = $record_set->getRecordAsHash();
    $self->{_data_store} = $rh_record;

    return $rh_record;

} # end of retrieveAuthDataStore

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
                  [-USERNAME],@_
                 );

    # local params
    my $username       = $params->{-USERNAME};
    my $password       = $params->{-PASSWORD};

#################################################
#
# DATASOURCE RELATED VARIABLES
#
#################################################

    my $password_field = $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD};
    my $field_map = $self->{'-USER_FIELDS_TO_DATASOURCE_MAPPING'};
    my $ds_password = $field_map->{$password_field};

#################################################
#
# ENCRYPT RELATED VARIABLES
#
#################################################

    my @encrypt_params =
      @{$self->{"-ENCRYPT_PARAMS"}};

    require Extropia::Core::Encrypt;
    my $encrypt = Extropia::Core::Encrypt->create(@encrypt_params);
    _dieIfError($encrypt);

    my $rh_record = $self->retrieveAuthDataStore(-USERNAME => $username);
    return undef if (!$rh_record);

    if (defined($password) &&
            (!$encrypt->compare(
                        -ENCRYPTED_CONTENT  => $rh_record->{
                           $ds_password},
                        -CONTENT_TO_COMPARE => $password))) {

        $self->addError(
                sprintf($self->{-PASSWORD_NOT_MATCHED_ERROR},$username));
        return undef;
    } # end compare password

    # OK, now we know that the user passed....
    $self->{"_user_authenticated"} = 1;

    $self->_prePopulateCache();

    return 1;

} # end of authenticate

#
# _prePopulateCache prepopulates the cache with the
# information passed to it.
#
sub _prePopulateCache {
    my $self = shift;

    my $auth_cache = $self->getAuthCacheObject();
    my $rh_user_ds_record = $self->retrieveAuthDataStore();

    my $field;
    foreach $field (@{$self->{-USER_FIELDS}}) {
        my $user_field =
            $self->{-USER_FIELDS_TO_DATASOURCE_MAPPING}->{$field};
#die($user_field);
        my $user_value =
            $rh_user_ds_record->{$user_field};
        $auth_cache->setCachedUserField(-USER_FIELD => $field,
                                  -USER_VALUE => $user_value);
    }

} # end of _prePopulateCache

#
# _getRawUserField is a metho that is called
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

    # global params
    my $field_map = $self->{'-USER_FIELDS_TO_DATASOURCE_MAPPING'};
    my $ds_fieldname = $field_map->{$user_field};

    my $username = $self->{_username_parameter};
    if (!defined($username)) {
# we haven't logged on yet...we may want to get/set session cache
# data anyway...
        return undef;
    }
    my $rh_user_ds_record =
        $self->retrieveAuthDataStore(-USERNAME => $username);

    if (!defined($rh_user_ds_record)) {
        die("$username\'s record could not be found in the datasource.");
    }
    my $user_value = $rh_user_ds_record->{$ds_fieldname};
    if (!exists($rh_user_ds_record->{$ds_fieldname}) &&
        ($user_field eq $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD} ||
        $user_field eq $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD} ||
        $user_field eq $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD})
        ) {
        confess(
            "$user_field could not be translated into an expected user value");
    }

    return $user_value;

} # end of _getRawUserField


#
# register
#
# Allows a user to register into the authenticaton source...
#

sub register {
    my $self = shift;
    @_ = _rearrange(
          [-USER_FIELD_NAME_TO_VALUE_MAPPING],
          [-USER_FIELD_NAME_TO_VALUE_MAPPING],
          @_);

    # local params
    my $rh_user_field_name_to_value_mapping = shift;

    # global params
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
    my $password_field = $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD};
    my $ra_user_field_names  = $self->{-USER_FIELDS};

    my $field_map = $self->{'-USER_FIELDS_TO_DATASOURCE_MAPPING'};

    my @ds_params =
      @{$self->{"-USER_DATASOURCE_PARAMS"}};

    # derived...
    my $ds = Extropia::Core::DataSource->create(@ds_params);
    _dieIfError($ds);

    my $username_value =
          $rh_user_field_name_to_value_mapping->{$username_field};

    # Check whether user is already in the datasource..
    # raise an error if this is so and make the register()
    # method fail...
    #

    my $search_term;
    if($self->{-AUTH_CASE_SENSITIVE_SEARCH}) {
      $search_term = $field_map->{$username_field} .
                                  " == " . qq{"$username_value"};

    } else {
      $search_term = $field_map->{$username_field} .
                                  " =i " . qq{"$username_value"};
    }

    my $record_set = $ds->search($search_term);

    $record_set->moveFirst();

    if (!$record_set->endOfRecords()) {
        $self->addError(
                sprintf($self->{-DUPLICATE_USERNAME_ERROR},$username_value));
        return undef;
    }

    # OK so now we passed the duplicate username check
    # so let's add the user to the datasource..

    require Extropia::Core::Encrypt;

    my @encrypt_params =
      @{$self->{"-ENCRYPT_PARAMS"}};
    my $encrypt = Extropia::Core::Encrypt->create(@encrypt_params);
    _dieIfError($encrypt);

    my $password_value =
        $rh_user_field_name_to_value_mapping->{$password_field};
    if (defined($password_value)) {
        $rh_user_field_name_to_value_mapping->{$password_field} =
            $encrypt->encrypt(
                -CONTENT_TO_ENCRYPT => $password_value
            );
    }


    #
    # set up the fields for adding to the datasource...
    #
    my %fields = ();

    my $field;
    foreach $field (@{$ra_user_field_names}) {
      $fields{$field_map->{$field}} =
        $rh_user_field_name_to_value_mapping->{$field};
    }

    if ($self->{'-ADD_REGISTRATION_TO_USER_DATASOURCE'}) {
        $ds->add(\%fields);
        _dieIfError($ds);
    }

    return 1; #success

} # end of register
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

    # globals used in this method
    my @ds_params =
        @{$self->{-USER_DATASOURCE_PARAMS}};
    my $field_map = $self->{-USER_FIELDS_TO_DATASOURCE_MAPPING};
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};

    my @user_list = ();
    if (!$user_search_field) {
        return @user_list;
    }

    my $ds = Extropia::Core::DataSource->create(@ds_params);
    _dieIfError($ds);

    my $search_term;
    if($self->{-AUTH_CASE_SENSITIVE_SEARCH}) {
       $search_term = $field_map->{$user_search_field} .
                    " == " . qq`"$user_search_value"`;

    } else {
       $search_term = $field_map->{$user_search_field} .
                    " =i " . qq`"$user_search_value"`;
    }


    my $record_set = $ds->search($search_term);
    _dieIfError($ds);

    my $ra_records = $record_set->getAllRecordsAsHash();
    my $ra_record;
    foreach $ra_record (@$ra_records) {
        my $user = $ra_record->{$field_map->{$username_field}};
        push (@user_list, $user);
    }

    return @user_list;

} # end of search

1;
