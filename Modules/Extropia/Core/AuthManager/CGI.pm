#$Id: CGI.pm,v 1.12 2002/01/10 02:48:31 janet Exp $
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

package Extropia::Core::AuthManager::CGI;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange
                      _rearrangeAsHash 
                      _assignDefaults
                      _dieIfRemainingParamsExist);

use Extropia::Core::Auth;
use Extropia::Core::AuthManager;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::AuthManager);
$VERSION = do { my @r = (q$Revision: 1.12 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -SESSION_OBJECT,
       -LOGON_VIEW,
       -REGISTRATION_VIEW,
       -REGISTRATION_SUCCESS_VIEW,
       -SEARCH_VIEW,
       -SEARCH_RESULTS_VIEW,
       -AUTH_VIEW_PARAMS,
       -VIEW_LOADER,
       -AUTH_PARAMS,
       -CGI_OBJECT,
       -ALLOW_REGISTRATION,
       -ALLOW_USER_SEARCH,
       -USER_SEARCH_FIELD,
       -GENERATE_PASSWORD,
       -PASSWORD_KEYGENERATOR_PARAMS,
       -DEFAULT_GROUPS,
       -EMAIL_REGISTRATION_TO_ADMIN,
       -EMAIL_REGISTRATION_ACKNOWLEDGEMENT_TO_USER,
       -MAIL_PARAMS,
       -USER_ACKNOWLEDGEMENT_MAIL_SEND_PARAMS,
       -ADMIN_MAIL_SEND_PARAMS,
       -ADMIN_MAIL_BODY_VIEW,
       -USER_MAIL_SEND_PARAMS,
       -USER_MAIL_BODY_VIEW,
       -USER_FIELDS,
       -USER_FIELD_TYPES,
       -USER_FIELD_NAME_MAPPINGS,
       -AUTH_REGISTRATION_DH_MANAGER_PARAMS,
       -AUTH_PASSED_SESSION_VAR,
       -DISPLAY_LOGON_AFTER_REGISTRATION,
       -LOGON_USER_AFTER_REGISTRATION,
       -DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE
    ],
    [
       -SESSION_OBJECT,
       -LOGON_VIEW,
       -REGISTRATION_VIEW,
       -REGISTRATION_SUCCESS_VIEW,
       -SEARCH_VIEW,
       -SEARCH_RESULTS_VIEW,
       -VIEW_LOADER,
       -AUTH_PARAMS,
       -CGI_OBJECT
    ],@_);

    if (!$self->{-USER_FIELD_NAME_MAPPINGS}) {
        if ($self->{-USER_FIELDS}) {
            my $field;
            my %mappings = ();
            foreach $field (@{$self->{-USER_FIELDS}}) {
                $mappings{$field} = $field;
            }
            $self->{-USER_FIELD_NAME_MAPPINGS} =
                \%mappings;
        } else {
            $self->{-USER_FIELD_NAME_MAPPINGS} =
                {'auth_username' => 'Username',
                 'auth_password' => 'Password',
                 'auth_groups'   => 'Groups',
                 'auth_email'    => 'EMail'};
        }
    }
    
    $self = _assignDefaults($self,
                   {

#'-AUTH_VIEWS' => 'Extropia::Core::AuthManager::CGI::AuthView',
# stas: I cannot find this module? what's that?
                    '-ALLOW_REGISTRATION' => 1,
                    '-ALLOW_USER_SEARCH' => 1,
                    '-USER_SEARCH_FIELD' => '',
                    '-GENERATE_PASSWORD' => 0,
                    '-PASSWORD_KEYGENERATOR_PARAMS' =>
                        [-TYPE => 'SimplePassword'],
                    '-DEFAULT_GROUPS' => 'normal',
                    '-EMAIL_REGISTRATION_TO_ADMIN' => 0,
# JT: Note that the oldview .pm file will be changed to ttml.
# Note that the ttml file will be placed in the HTMLTemplates/Default/AuthManager/CGI directory.
#  -USER_MAIL_BODY_VIEW, -ADMIN_MAIL_BODY_VIEW are the 2 views affected for the Auth.
                    -USER_MAIL_BODY_VIEW => 
                         'AuthManager/CGI/UserEventEmailView', 
                       # 'Extropia::Core::AuthManager::CGI::UserMailBodyView',
                    -ADMIN_MAIL_BODY_VIEW =>
                         'AuthManager/CGI/AdminEventEmailView',
                        #'Extropia::Core::AuthManager::CGI::AdminMailBodyView',
                    '-USER_FIELDS' => [
                        'auth_username', 
                        'auth_password',
                        'auth_groups'],
                    '-AUTH_PASSED_SESSION_VAR' => '_AUTH_PASSED',
                    '-DISPLAY_LOGON_AFTER_REGISTRATION' => 0,
                    '-DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE' => 1
                   });

    $self = _assignDefaults($self,
                   {'-USER_FIELD_NAME_MAPPINGS' => $self->{'-USER_FIELDS'},
                    '-USER_FIELD_TYPES' => [
                       -USERNAME_FIELD => $self->{-USER_FIELDS}->[0],
                       -PASSWORD_FIELD => $self->{-USER_FIELDS}->[1],
                       -GROUP_FIELD    => $self->{-USER_FIELDS}->[2],
                       -EMAIL_FIELD    => $self->{-USER_FIELDS}->[3]],
                    '-AUTH_REGISTRATION_DH_MANAGER_PARAMS' =>
                      [
                       -TYPE           => 'CGI',
                       -CGI_OBJECT     => $self->{-CGI_OBJECT},
                       -DATAHANDLERS   => [qw(Exists)],
                       -FIELD_MAPPINGS => $self->{-USER_FIELD_NAME_MAPPINGS},
                       -IS_FILLED_IN   => $self->{-USER_FIELDS}
                      ]
                   });
 
    _dieIfRemainingParamsExist(@_);

    return bless $self, $package;

}

# 
# isAuthenticated lets the programmer know if the 
# user has already logged on using the AuthManager::CGI
# driver. There is a flag in session that reveals whether
# the user authenticated
#

sub isAuthenticated {
    my $self = shift;

    my $session     = $self->{'-SESSION_OBJECT'};
    my $auth_passed = $self->{'-AUTH_PASSED_SESSION_VAR'};

    if ($session->getAttribute(-KEY => $auth_passed)) {
        my $auth = $self->getAuthObject();
        return 1;
    }

    return 0;
}

#
# logoff() reverses the authentication and overrides the
# default empty logoff method in the main class
#
sub logoff {
    my $self = shift;

    my $session     = $self->{'-SESSION_OBJECT'};
    my $auth_passed = $self->{'-AUTH_PASSED_SESSION_VAR'};

    $session->removeAttribute(-KEY => $auth_passed);
    return 1;

} # end of logff

#
# Authenticate.  In AuthManager::CGI
# we authenticate against a session variable. If the session
# variable says we have validated, then we can safely assume
# that the user has logged on.
#
sub authenticate {
    my $self   = shift;
    my $params;
    ($params,@_) = _rearrangeAsHash([-USERNAME,-PASSWORD],[],@_);

    if ($params->{-USERNAME}) {
        $self->_validateUser(-USERNAME => $params->{-USERNAME},
                             -PASSWORD => $params->{-PASSWORD});
        return 1;
    }

    my $session     = $self->{'-SESSION_OBJECT'};
    my $auth_passed = $self->{'-AUTH_PASSED_SESSION_VAR'};

    # 
    # If we have already logged on, then we want to
    # pass this info onto the authentication object right away
    # instead of going the CGI route.
    #
    if ($session->getAttribute(-KEY => $auth_passed)) {
        my $auth = $self->getAuthObject();
        return 1;
    } else {
        if ($self->_authenticateUsingCGI()) {
            my $username_field = 
                $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
            my $username = $self->getUserField(
                        -USER_FIELD => $username_field);
            $session->setAttribute(-KEY => $auth_passed,
                                   -VALUE => $username);
            return 1;
        } else { 
            return 0;
        }
    }
  
} # end of authenticate

#
# This is the heart of the CGI based authentication
# The logic here entails putting out the right form
# passed on previously passed form variables.
#
sub _authenticateUsingCGI {
    my $self = shift;

    my $cgi = $self->{'-CGI_OBJECT'};

    # First we add some code in case to set normalize
    # submit button logic in case someone wants to use
    # image buttons instead of normal submit buttons.
    #
    # We do this by taking form vars with a .x suffix
    # and creating the same thing without.
    #
    foreach ($cgi->param()) {
        $cgi->param($1,$cgi->param($_)) if (/(.*)\.x/);
    }

    # We can look at the CGI Based authentication
    # as a series of scenarios...
    #
    ###########################################
    # SCENARIO 1: SEARCH FOR USER             #
    ###########################################
    if ($cgi->param("auth_submit_search") &&
        $self->{'-ALLOW_USER_SEARCH'}) {
        my $auth = $self->getAuthObject();
	my @user_list = $auth->search(
        -USER_SEARCH_FIELD => $self->{-USER_SEARCH_FIELD},
        -USER_SEARCH_VALUE => $cgi->param($self->{-USER_SEARCH_FIELD})
        );
        $self->_loadViewAndDisplay(
            $self->{-SEARCH_RESULTS_VIEW},
	         -CGI_OBJECT => $cgi,
    		 -USER_LIST => \@user_list); 
    ###########################################
    # SCENARIO 2: DISPLAY SEARCH SCREEN       #
    ###########################################
    } elsif ($cgi->param("auth_submit_search_request") &&
            $self->{'-ALLOW_USER_SEARCH'}) {
            $self->_loadViewAndDisplay(
                $self->{-SEARCH_VIEW},
	            -CGI_OBJECT => $cgi); 
    ###########################################
    # SCENARIO 3: LOGON 
    ###########################################
    } elsif ($cgi->param("auth_submit_logon")) {
        return $self->_CGIValidateUser();
    ###########################################
    # SCENARIO 4: REGISTER USER SCREEN        #
    ###########################################
    } elsif ($cgi->param("auth_submit_registration_request") &&
             $self->{'-ALLOW_REGISTRATION'}) {
        my $password_field = $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD}; 
        my $group_field    = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};

        $self->_loadViewAndDisplay(
                 $self->{-REGISTRATION_VIEW},
		-ERROR_LIST => [],
        -CGI_OBJECT => $cgi,
		-USER_FIELDS => $self->{'-USER_FIELDS'},
		-USER_FIELD_NAME_MAPPINGS =>
		    $self->{'-USER_FIELD_NAME_MAPPINGS'},
		-GENERATE_PASSWORD => 
		    $self->{'-GENERATE_PASSWORD'},
        -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
        -PASSWORD_FIELD =>
            $password_field,
        -GROUP_FIELD =>
            $group_field);
    ###########################################
    # SCENARIO 5: REGISTER USER               #
    ###########################################
    } elsif ($cgi->param("auth_submit_registration") &&
             $self->{'-ALLOW_REGISTRATION'}) {
        if ($self->_register()) {
            return 1;
        }
    ##############################################
    # SCENARIO 6: (DEFAULT) DISPLAY LOGON SCREEN #
    ##############################################
    } else {
        $self->_loadViewAndDisplay(
            $self->{'-LOGON_VIEW'},
            -ERROR_LIST => [],
	        -CGI_OBJECT => $cgi,
            -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
    		-ALLOW_REGISTRATION => $self->{'-ALLOW_REGISTRATION'},
            -ALLOW_USER_SEARCH  =>
		    $self->{'-ALLOW_USER_SEARCH'});
    }

    exit();
} # end of _authenticateUserCGI


#
# _loadViewAndDisplay is a helper method to allow 
# us to load and display views easily for the CGI
# based authentication module
#
sub _loadViewAndDisplay {
    my $self = shift;

    my $view_name = shift;

    my @view_params = ();
    if ($self->{-AUTH_VIEW_PARAMS}) {
        @view_params = @{$self->{-AUTH_VIEW_PARAMS}};
    }

#print STDERR "process Auth: $view_name\n";

    print $self->{-VIEW_LOADER}->process
            (
             $view_name,
             {@{$self->{"-AUTH_VIEWS"}||[]},
              @view_params,
              @_}
            );

} # END OF LoadViewAndDisplay

# _register() checks the form variables from the
# registration screen makes makes sure that they are OK.
#
# If they are, then it calls the register() method on
# the core authentication object. 
#
# Then, success or failure is reported. 
# 
sub _register {
    my $self = shift;

    # global params
    my $cgi = $self->{'-CGI_OBJECT'};
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};

    my $generate_password = $self->{-GENERATE_PASSWORD};
    my $password_field = $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD};

    my $ra_user_field_names = $self->{-USER_FIELDS};
    my $group_field = $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD};
    my $default_groups = $self->{-DEFAULT_GROUPS};

    # derived params
    my $auth = $self->getAuthObject();

    my $field_map = $self->{-AUTH_FIELDS_TO_DATASOURCE_MAPPING};

    # main variables
    my $register_success = 0;

    my @error_list = ();

    ###################################################
    # 
    # CHECK THAT THE FORM PASSED DATAHANDLER VALIDATION
    #
    ###################################################
    require Extropia::Core::DataHandlerManager;
    my $dhm_params = $self->{'-AUTH_REGISTRATION_DH_MANAGER_PARAMS'};
    my $dhm = Extropia::Core::DataHandlerManager->create(@$dhm_params);

    my $datahandler_croaked = 0;

    # VALIDATE FORM
    $dhm->validate();
    if ($dhm->getErrorCount()) {
        my $errors = $dhm->getErrors();
        my $error;
        foreach $error (@$errors) {
            push(@error_list, $error->getMessage()); 
        }
        $datahandler_croaked = 1;
    } 
    # UNTAINT FORM
    $dhm->untaint($cgi);
    if ($dhm->getErrorCount()) {
        my $errors = $dhm->getErrors();
        my $error;
        foreach $error (@$errors) {
            push(@error_list, $error->getMessage()); 
        }
        $datahandler_croaked = 1;
    } 
    # TRANSFORM FORM
    $dhm->transform($cgi);
    if ($dhm->getErrorCount()) {
        my $errors = $dhm->getErrors();
        my $error;
        foreach $error (@$errors) {
            push(@error_list, $error->getMessage()); 
        }
        $datahandler_croaked = 1;
    } 

    my %user_field_name_to_value_mapping = ();
    my $field;
    foreach $field (@{$ra_user_field_names}) {
        if ($field ne $group_field) {
            $user_field_name_to_value_mapping{$field} = 
                $cgi->param($field);
        } else {
            $user_field_name_to_value_mapping{$field} =
                $default_groups;
        }	
    }

    my $generated_password = "";
    if (!$datahandler_croaked) { # everything validated fine...

        ##########################################################
        #
        # GENERATE OR OBTAIN PASSWORD...
        #
        # If password is obtained, then it is checked against
        # the user entering it twice... once in the specified
        # password field and a second time in the same field name
        # with a "2" appended to the name. 
        #
        ##########################################################

        if (!$generate_password) {
            if (!$cgi->param($password_field) ||
	            !$cgi->param($password_field . "2")) {
	            push(@error_list, "One of the password fields was missing!");
	        } else {
                if ($cgi->param($password_field) ne 
                $cgi->param($password_field . "2")) {
                    push(@error_list, "Entered Passwords Did Not Match!");
                } 
	        }
        } else { # GENERATE PASSWORD! 
            require Extropia::Core::KeyGenerator;
            my $kg = Extropia::Core::KeyGenerator->create(
                           @{$self->{-PASSWORD_KEYGENERATOR_PARAMS}});
            $generated_password = $kg->createKey();
            $user_field_name_to_value_mapping{$password_field} =
                $generated_password;
        } # end of generate password

        #########################################################
        #
        # CALL THE Extropia::Core::Auth's register() METHOD
        #
        #########################################################
    
        if (@error_list < 1) {
            $register_success = $auth->register(
                            -USER_FIELD_NAME_TO_VALUE_MAPPING =>
                            \%user_field_name_to_value_mapping
                            );

            if (!$register_success) {
                my $errors = $auth->getErrors();
                my $error;
                foreach $error (@$errors) {
                    push(@error_list, $error->getMessage()); 
                }
            }
        }
    } # if datahandler croaked...


    ################################################################
    #
    # DISPLAY NEW SCREEN NOW THAT REGISTRATION FAILED OR SUCCEEDED
    #
    ################################################################
    if ($register_success) {
        if ($self->{-EMAIL_REGISTRATION_TO_ADMIN}) {
            $self->_sendAdminMail(
                    -USER_FIELD_NAME_TO_VALUE_MAPPING =>
                    \%user_field_name_to_value_mapping);
        }

        if ($self->{-EMAIL_REGISTRATION_ACKNOWLEDGEMENT_TO_USER}) {
            $self->_sendUserAcknowledgementMail(
                    -USER_FIELD_NAME_TO_VALUE_MAPPING =>
                    \%user_field_name_to_value_mapping);
        }
        if ($generate_password) {
            $self->_sendUserMail(-USERNAME => 
               $user_field_name_to_value_mapping{$username_field},
               -PASSWORD => $generated_password,
               -USER_MAIL_ADDRESS => 
               $user_field_name_to_value_mapping{
                 $self->{-USER_FIELD_TYPES}->{-EMAIL_FIELD}}
               ); 
        }

        if ($self->{'-DISPLAY_LOGON_AFTER_REGISTRATION'}) {
        $self->_loadViewAndDisplay($self->{'-LOGON_VIEW'},
		 -ERROR_LIST => [""],
	         -CGI_OBJECT => $cgi,
                 -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
		 -ALLOW_REGISTRATION => $self->{'-ALLOW_REGISTRATION'},
		 -ALLOW_USER_SEARCH  =>
		     $self->{'-ALLOW_USER_SEARCH'},
                 -USERNAME =>
                   $user_field_name_to_value_mapping{
                     $username_field
                   });
        } elsif ($self->{-LOGON_USER_AFTER_REGISTRATION}) {
            return $self->authenticate(-USERNAME => 
                         $user_field_name_to_value_mapping{$username_field},
                       -PASSWORD =>
                         $user_field_name_to_value_mapping{$password_field},
                       );
        } else {
            $self->_loadViewAndDisplay(
                                 $self->{'-REGISTRATION_SUCCESS_VIEW'},      
                        -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
	                -CGI_OBJECT     => $cgi);
            exit;
        }
     } else {
         if ($self->{'-DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE'}) {
            $self->_loadViewAndDisplay(
                                   $self->{'-REGISTRATION_VIEW'},     
		        -ERROR_LIST => \@error_list,
                    -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
	            -CGI_OBJECT => $cgi,
		        -USER_FIELDS => 
                     $self->{'-USER_FIELDS'},
		        -USER_FIELD_NAME_MAPPINGS =>
		            $self->{'-USER_FIELD_NAME_MAPPINGS'},
		        -GENERATE_PASSWORD =>
		            $self->{'-GENERATE_PASSWORD'},
                 -PASSWORD_FIELD =>
                     $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD},
                 -GROUP_FIELD =>
                     $self->{-USER_FIELD_TYPES}->{-GROUP_FIELD},
                 -USER_FIELD_NAME_TO_VALUE_MAPPING =>
                     \%user_field_name_to_value_mapping
                     ); 
        } else {
	        unshift(@error_list, 'Registration Unsuccessful.');
            $self->_loadViewAndDisplay(
                                $self->{'-LOGON_VIEW'},       
		        -ERROR_LIST => \@error_list,
                    -SESSION_OBJECT => $self->{'-SESSION_OBJECT'},
	            -CGI_OBJECT => $cgi,
		        -ALLOW_REGISTRATION => 
                     $self->{'-ALLOW_REGISTRATION'},
		        -ALLOW_USER_SEARCH =>
		            $self->{'-ALLOW_USER_SEARCH'});
         }
     }

     return 0;

} # end of _register

#
# _validateUser authenticates a user using the Extropia::Core::Auth
# API. If the authentication is successful, the user is considered to
# be logged on and then this module takes the session info and populates
# it with new logon information...
#
sub _validateUser {
    my $self = shift;
    my ($username, $password)
        = _rearrange([-USERNAME,-PASSWORD],[-USERNAME,-PASSWORD],@_);

    #
    # do the authentication...
    #
    my $auth = $self->getAuthObject();

    my $success = $auth->authenticate(
               -USERNAME => $username,
               -PASSWORD => $password
              );

    my $error_message = "";
    if (!$success) {
        my $errors = $auth->getErrors();
        my $error;
        foreach $error (@$errors) {
            $error_message .= $error->getMessage() . "\n"; 
        }
    }

    ##############################################################
    #
    # POPULATE AUTHENTICATION INFORMATION
    #
    ##############################################################

    if ($success) {
        my $session = $self->{-SESSION_OBJECT};
        my $auth_passed = $self->{-AUTH_PASSED_SESSION_VAR};

        $session->{$auth_passed} = $username;

        return 1;
    } else { # logon unsuccessful
        $self->_loadViewAndDisplay(
                            $self->{-LOGON_VIEW},
		        -ERROR_LIST         => [$error_message],
                -SESSION_OBJECT     => $self->{'-SESSION_OBJECT'},
	            -CGI_OBJECT         => $self->{-CGI_OBJECT},
		        -ALLOW_REGISTRATION => 
                    $self->{'-ALLOW_REGISTRATION'},
		        -ALLOW_USER_SEARCH  =>
		            $self->{'-ALLOW_USER_SEARCH'},
                -USERNAME           =>
                    $username);
    }

    exit();

} # end of _validateUser

#
# _CGIValidateUser is the low level call that _authenticateUsingCGI calls
#

sub _CGIValidateUser {
    my $self = shift;

    # global params

    my $cgi            = $self->{'-CGI_OBJECT'};
    my $ra_user_fields = $self->{'-USER_FIELDS'};

    #
    # Derived params
    #
    my $username_field = $self->{-USER_FIELD_TYPES}->{-USERNAME_FIELD};
    my $password_field = $self->{-USER_FIELD_TYPES}->{-PASSWORD_FIELD};

    my $username = $cgi->param($username_field) || "";
    my $password = $cgi->param($password_field) || "";

    return $self->_validateUser(-USERNAME => $username,
                                -PASSWORD => $password);

} # end of _CGIValidateUser

sub _sendUserMail {
    my $self = shift;
    @_ = _rearrange([-USERNAME,-PASSWORD,-USER_MAIL_ADDRESS],
                    [-USERNAME,-PASSWORD],@_);

    my $username  = shift;
    my $password  = shift;
    my $user_mail = shift;

    my $mail = $self->_getMailObject();

    # This is commented and stas' method of process_email is being implemented.
    #my $view =
    #      $self->{-VIEW_LOADER}->create($self->{-USER_MAIL_BODY_VIEW});

    #my $body = $view->display(-USERNAME => $username, 
    #                          -PASSWORD => $password);

    my $body = $self->{-VIEW_LOADER}->process_email(
          	$self->{-USER_MAIL_BODY_VIEW},
          	{
          		-CGI_OBJECT =>$self->{-CGI_OBJECT},
                -USERNAME=>$username,
                -PASSWORD=>$password,
          		@_,
          	}
          
    );


    if (!defined($self->{-USER_MAIL_SEND_PARAMS})) {
        die("You forgot to define -USER_MAIL_SEND_PARAMS in the " . 
                "Auth Manager configuration. Suggestion parameters " .
                "include -FROM and -TO.");
    }
    my @mail_send_params = @{$self->{-USER_MAIL_SEND_PARAMS}};
    push(@mail_send_params,-TO => $user_mail);
    $mail->send(@mail_send_params,-BODY => $body);

} # end of _sendUserMail


sub _sendUserAcknowledgementMail {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD_NAME_TO_VALUE_MAPPING],
                    [-USER_FIELD_NAME_TO_VALUE_MAPPING],@_);

    my $field_name_to_value = shift;

    my $mail = $self->_getMailObject();

   # This is commented and stas' method of process_email is being implemented.
   # my $view =
   #       $self->{-VIEW_LOADER}->create($self->{-ADMIN_MAIL_BODY_VIEW});

     my $body = $self->{-VIEW_LOADER}->process_email(
          	$self->{-ADMIN_MAIL_BODY_VIEW},
          	{
          		-CGI_OBJECT =>$self->{-CGI_OBJECT},
          		@_,
          	}
          
          );

    if (!defined($self->{-USER_ACKNOWLEDGEMENT_MAIL_SEND_PARAMS})) {
        die("You forgot to define -USER_ACKNOWLEDGEMENT_MAIL_SEND_PARAMS in  AuthManager::CGI.");
    }
    my @mail_send_params = @{$self->{-USER_ACKNOWLEDGEMENT_MAIL_SEND_PARAMS}};
    $mail->send(@mail_send_params);
} # end of _sendAdminMail

sub _sendAdminMail {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD_NAME_TO_VALUE_MAPPING],
                    [-USER_FIELD_NAME_TO_VALUE_MAPPING],@_);

    my $field_name_to_value = shift;

    my $mail = $self->_getMailObject();

   # my $view =
    	      #$self->{-VIEW_LOADER}->create($self->{-ADMIN_MAIL_BODY_VIEW});
   
    #my $body = $view->display(-USER_FIELD_NAME_TO_VALUE_MAPPING =>
    #                          $field_name_to_value,
    #                          -USER_FIELD_TYPES => 
    #                          $self->{-USER_FIELD_TYPES});

    my $body = $self->{-VIEW_LOADER}->process_email(
          	$self->{-ADMIN_MAIL_BODY_VIEW},
          	{
          		-CGI_OBJECT =>$self->{-CGI_OBJECT},
          		@_,
          	}
          
    );
    
    if (!defined($self->{-ADMIN_MAIL_SEND_PARAMS})) {
        die("You forgot to define -ADMIN_MAIL_SEND_PARAMS in AuthManager::CGI.");
    }
    my @mail_send_params = @{$self->{-ADMIN_MAIL_SEND_PARAMS}};
    $mail->send(@mail_send_params,-BODY => $body);
     
    

} # end of _sendAdminMail

sub _getMailObject {
    my $self = shift;

    if (!$self->{_mail_object}) {
        if (!$self->{-MAIL_PARAMS}) {
            confess("You must specify mail parameters when creating
                    this auth manager. You must be attempting to 
                    send mail without having set this up.");
        }
        my $mail = Extropia::Core::Mail->create(@{$self->{-MAIL_PARAMS}});
        $self->{_mail_object} = $mail;
    }

    return $self->{_mail_object};

} # end of _getMailObject

1;
