#!/usr/bin/perl -wT

# Copyright (C) 1994 - 2001  eXtropia.com
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

use strict;

BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules
               ../Modules/CPAN .);
}

use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

my $APP_NAME = "doc_manager";

my $GLOBAL_DATAFILES_DIRECTORY = "../../Datafiles";
my $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
my $APP_DATAFILES_DIRECTORY    = "../../Datafiles/DocManager";

my @VIEWS_SEARCH_PATH =
    qw(../Modules/Extropia/View/DocManager
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/DocManager
       ../HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to bug in Perl 5.60. Uncomment with Perl 5.61
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");

my $VIEW_LOADER = new Extropia::Core::View
	(\@VIEWS_SEARCH_PATH, \@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        ". Please contact the webmaster.");

foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x/);
}
                
######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60,
    -SESSION_DIR     => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
    -FATAL_TIMEOUT   => 0,
    -FATAL_SESSION_NOT_FOUND => 0
);

######################################################################
#                     SESSION MANAGER SETUP                          #
######################################################################

my @SESSION_MANAGER_CONFIG_PARAMS = (
    -TYPE           => 'FormVar',
    -CGI_OBJECT     => $CGI,
    -SESSION_PARAMS => \@SESSION_CONFIG_PARAMS
);

my $SESSION_MGR = Extropia::Core::SessionManager->create(
    @SESSION_MANAGER_CONFIG_PARAMS
);

my $SESSION     = $SESSION_MGR->createSession();

######################################################################
#                       AUTHENTICATION SETUP                         #
######################################################################

my @AUTH_USER_DATASOURCE_FIELD_NAMES = qw(
    username
    password
    groups
    firstname
    lastname
    email
);

my @AUTH_USER_DATASOURCE_PARAMS = (
    -TYPE                       => 'File',
    -FIELD_DELIMITER            => '|',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.users.dat"
);

my @AUTH_ENCRYPT_PARAMS = (
    -TYPE => 'Crypt'
);

my %USER_FIELDS_TO_DATASOURCE_MAPPING = (
    'auth_username'  => 'username',
    'auth_password'  => 'password',
    'auth_firstname' => 'firstname',
    'auth_lastname'  => 'lastname',
    'auth_groups'    => 'groups',
    'auth_email'     => 'email'
);

my @AUTH_CACHE_PARAMS = (
    -TYPE           => 'Session',
    -SESSION_OBJECT => $SESSION
);

my @AUTH_CONFIG_PARAMS = (
    -TYPE                                => 'DataSource',
    -USER_DATASOURCE_PARAMS              => \@AUTH_USER_DATASOURCE_PARAMS,
    -ENCRYPT_PARAMS                      => \@AUTH_ENCRYPT_PARAMS,
    -ADD_REGISTRATION_TO_USER_DATASOURCE => 1,
    -USER_FIELDS_TO_DATASOURCE_MAPPING   => \%USER_FIELDS_TO_DATASOURCE_MAPPING,
    -AUTH_CACHE_PARAMS                   => \@AUTH_CACHE_PARAMS
);

######################################################################
#                 AUTHENTICATION MANAGER SETUP                       #
######################################################################

my @AUTH_VIEW_DISPLAY_PARAMS = (
    -COLOR_FOR_EVEN_ROWS     => 'E5E5E5',
    -COLOR_FOR_ODD_ROWS      => 'FFFFFF',
    -CSS_VIEW_URL            => $CGI->script_name() . "?display_css_view=on",
    -APPLICATION_LOGO        => 'logo.gif',
    -APPLICATION_LOGO_HEIGHT => '40',
    -APPLICATION_LOGO_WIDTH  => '353',
    -APPLICATION_LOGO_ALT    => 'WebDB Demo',
    -HTTP_HEADER_PARAMS      => [],
    -DOCUMENT_ROOT_URL       => '/',
    -DEFAULT_CHARSET          => 'ISO-8859-1',
    -IMAGE_ROOT_URL          => '/Images/Extropia',
    -LINK_TARGET             => '_self',
    -SCRIPT_DISPLAY_NAME     => 'Doc Manager',
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => 'PageTopView',
    -PAGE_BOTTOM_VIEW        => 'PageBottomView'
);


my @AUTH_REGISTRATION_DH_MANAGER_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,
    -DATAHANDLERS => [qw(
        Email
        Exists
    )],
    
    -FIELD_MAPPINGS => {
                'auth_username'     => 'Username',
                'auth_password'     => 'Password',
                'auth_password2'    => 'Confirm Password',
                'auth_firstname'    => 'First Name',
                'auth_lastname'     => 'Last Name',
                'auth_email'        => 'E-Mail Address'
        },
  
        -IS_FILLED_IN => [qw(
                auth_username
                auth_firstname
                auth_lastname
                auth_email
        )],
    
        -IS_EMAIL => [qw(
                auth_email
        )]
);
    
my @USER_FIELDS = (qw(
    auth_username
    auth_password
    auth_groups
    auth_firstname
    auth_lastname
    auth_email
));

my %USER_FIELD_NAME_MAPPINGS = (
    'auth_username'  => 'Username',
    'auth_password'  => 'Password',
    'auth_groups'     => 'Groups',
    'auth_firstname' => 'First Name',
    'auth_lastname'  => 'Last Name',
    'auth_email'     => 'E-Mail'
);

my %USER_FIELD_TYPES = (
    -USERNAME_FIELD => 'auth_username',
    -PASSWORD_FIELD => 'auth_password',
    -GROUP_FIELD    => 'auth_groups',
    -EMAIL_FIELD    => 'auth_email'
);

my @MAIL_PARAMS = (
    -TYPE         => 'Sendmail',
);

my @USER_MAIL_SEND_PARAMS = (
    -FROM    => 'you@yourdomain.com',
    -SUBJECT => 'Password Generated'
);
                
my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => 'you@yourdomain.com',
    -TO      => 'you@yourdomain.com',
    -SUBJECT => 'Registration Notification'
);

my @AUTH_MANAGER_CONFIG_PARAMS = (
    -TYPE                        => 'CGI',
    -ADMIN_MAIL_SEND_PARAMS      => \@ADMIN_MAIL_SEND_PARAMS,
    -AUTH_VIEW_PARAMS            => \@AUTH_VIEW_DISPLAY_PARAMS,
    -MAIL_PARAMS                 => \@MAIL_PARAMS,
    -USER_MAIL_SEND_PARAMS       => \@USER_MAIL_SEND_PARAMS,
    -SESSION_OBJECT              => $SESSION,
   # -AUTH_VIEWS                  => 'CGIViews.pm',
    -LOGON_VIEW                  => 'AuthManager/CGI/LogonScreen',
    -REGISTRATION_VIEW           => 'AuthManager/CGI/RegistrationScreen',
    -REGISTRATION_SUCCESS_VIEW   => 'AuthManager/CGI/RegistrationSuccessScreen',
    -SEARCH_VIEW                 => 'AuthManager/CGI/SearchScreen',
    -SEARCH_RESULTS_VIEW         => 'AuthManager/CGI/SearchResultsScreen',
    -VIEW_LOADER                 => $VIEW_LOADER,
    -AUTH_PARAMS                 => \@AUTH_CONFIG_PARAMS,
    -CGI_OBJECT                  => $CGI,
    -ALLOW_REGISTRATION          => 1,   
    -ALLOW_USER_SEARCH           => 1,
    -USER_SEARCH_FIELD           => 'auth_email',
    -GENERATE_PASSWORD           => 0,
    -DEFAULT_GROUPS              => 'normal',
    -EMAIL_REGISTRATION_TO_ADMIN => 0,
    -USER_FIELDS                 => \@USER_FIELDS,
    -USER_FIELD_TYPES            => \%USER_FIELD_TYPES,
    -USER_FIELD_NAME_MAPPINGS    => \%USER_FIELD_NAME_MAPPINGS,
    -DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE => 1,
    -AUTH_REGISTRATION_DH_MANAGER_PARAMS => \@AUTH_REGISTRATION_DH_MANAGER_PARAMS,
    
);

######################################################################
#                      UPLOAD MANAGER SETUP                          #
######################################################################

my @UPLOAD_MANAGER_CONFIG_PARAMS = ( 
                -TYPE         => 'Simple',
                # Session is added as it will be required in storeUploadedFile in Simple.pm 
                # to store the info of uploaded file into the session.
                -SESSION_OBJECT => $SESSION,
                -CGI_OBJECT   => $CGI,
                -UPLOAD_FIELD => 'file',
                -UPLOAD_DIRECTORY => "$APP_DATAFILES_DIRECTORY/Uploads",
                -FIELD_TO_SET_UPLOAD_FILENAME => "filename",
                -FIELD_TO_SET_UPLOAD_SIZE     => "size",
                -ADD_SESSION_ID_TO_URL_AS_GET_PARAMETER => 0,
                -KEY_GENERATOR_PARAMS => [
                    -TYPE               => 'Random',
                    -SECRET_ELEMENT     => 'RECRUIT',
                    -LENGTH             => 0
                ],
                );

######################################################################
#                      DATA HANDLER SETUP                            #
######################################################################
                       
my @ADD_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Email 
        Exists
        HTML
        String
        Upload
        )],

    -FIELD_MAPPINGS => {
        'folder'         => 'Folder',
        'file'           => 'File',
        'filename'       => 'Filename',
        'description'    => 'Description',
        'size'           => 'Size',
        'username'       => 'Username'
    },

    -RULES => [
    
    # ESCAPE_HTML_TAGS has to be removed else the email received will be with the escaped HTML Tag.
    
    #    -ESCAPE_HTML_TAGS => [
    #        -FIELDS => [qw(
    #            *
    #        )]
    #    ],

        -UPLOAD_FILE => [
            -FIELDS => [qw(
                file
                )],
            -UPLOAD_MANAGER_PARAMS => \@UPLOAD_MANAGER_CONFIG_PARAMS,
            -ADD_SESSION_ID_AS_GET_PARAM => 1

        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\\',
            -ERROR_MESSAGE => "You may not have a '\\' character in the " .
                              "%FIELD_NAME% field."
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\"',
            -ERROR_MESSAGE => "You may not have a '\"' character in the " .
                              "%FIELD_NAME% field."
        ],


        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
            -FIELDS => [qw(
                *
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                    folder
                    file
                    description
            )]
        ]
    ]
);

my @MODIFY_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Email 
        Exists
        HTML
        String
        Upload
        )],

    -FIELD_MAPPINGS => {
        'folder'         => 'Folder',
        'file'           => 'File',
        'filename'       => 'Filename',
        'description'    => 'Description',
        'size'           => 'Size',
        'username'       => 'Username'
    },

    -RULES => [
      # ESCAPE_HTML_TAGS has to be removed else the email received will be with the escaped HTML Tag.
      #  -ESCAPE_HTML_TAGS => [
      #      -FIELDS => [qw(
      #          *
      #      )]
      #  ],

        -UPLOAD_FILE => [
            -FIELDS => [qw(
                file
                )],
            -UPLOAD_MANAGER_PARAMS => \@UPLOAD_MANAGER_CONFIG_PARAMS,
            -ADD_SESSION_ID_AS_GET_PARAM => 1
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\\',
            -ERROR_MESSAGE => "You may not have a '\\' character in the " .
                              "%FIELD_NAME% field."
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\"',
            -ERROR_MESSAGE => "You may not have a '\"' character in the " .
                              "%FIELD_NAME% field."
        ],

        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
            -FIELDS => [qw(
                *
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                folder
                description
            )]
        ]
    ]
);

my @DATA_HANDLER_MANAGER_CONFIG_PARAMS = (
    -ADD_FORM_DHM_CONFIG_PARAMS    => \@ADD_FORM_DHM_CONFIG_PARAMS,
    -MODIFY_FORM_DHM_CONFIG_PARAMS => \@MODIFY_FORM_DHM_CONFIG_PARAMS,
);

######################################################################
#                      DATASOURCE SETUP                              #
######################################################################

my @DATASOURCE_FIELD_NAMES = qw(
        folder
        record_id
        file
        filename
        description
        size
        username
        username_of_poster
        group_of_poster
        date_time_posted
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    folder => [
        -DISPLAY_NAME => 'Folder',
        -TYPE         => 'popup_menu',
        -NAME         => 'folder',
        -VALUES       => [qw(Business Misc Personal)]
    ],

    file => [
        -DISPLAY_NAME => 'File',
        -TYPE         => 'filefield',
        -NAME         => 'file',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    filename => [
        -DISPLAY_NAME => 'Filename',
        -TYPE         => 'textfield',
        -NAME         => 'filename',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    size => [
        -DISPLAY_NAME => 'Size',
        -TYPE         => 'textfield',
        -NAME         => 'size',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    description => [
        -DISPLAY_NAME => 'Description',
        -TYPE         => 'textfield',
        -NAME         => 'description',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ]

);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
        folder
        file   
        description   
);

my @SEARCH_INPUT_WIDGET_DISPLAY_ORDER = qw(
        folder
        filename   
        description   
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);

my @SEARCH_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@SEARCH_INPUT_WIDGET_DISPLAY_ORDER
);

my @BASIC_DATASOURCE_CONFIG_PARAMS = (
    -TYPE                       => 'File', 
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
    -COMMENT_PREFIX             => '#',
    -FIELD_DELIMITER            => '|',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['record_id'],
    -FIELD_TYPES                => {
        record_id        => 'Autoincrement'
    },
);

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################
           
my @MAIL_CONFIG_PARAMS = (     
    -TYPE         => 'Sendmail'
);

my @EMAIL_DISPLAY_FIELDS = qw(
        folder
        file
        filename
        size
        description
);

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => 'you@yourdomain.com',
    -TO       => 'you@yourdomain.com',
    -REPLY_TO => 'you@yourdomain.com',
    -SUBJECT  => 'Document Manager Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => 'you@yourdomain.com',
    -TO       => 'you@yourdomain.com',
    -REPLY_TO => 'you@yourdomain.com',
    -SUBJECT  => 'Document Manager Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => 'you@yourdomain.com',
    -TO       => 'you@yourdomain.com',
    -REPLY_TO => 'you@yourdomain.com',
    -SUBJECT  => 'Document Manager Modification'
);

my @MAIL_SEND_PARAMS = (
    -DELETE_EVENT_MAIL_SEND_PARAMS => \@DELETE_EVENT_MAIL_SEND_PARAMS,
    -ADD_EVENT_MAIL_SEND_PARAMS    => \@ADD_EVENT_MAIL_SEND_PARAMS,
    -MODIFY_EVENT_MAIL_SEND_PARAMS => \@MODIFY_EVENT_MAIL_SEND_PARAMS
);

##################################################################
#                         LOGGING SETUP                          #
##################################################################

my @LOG_CONFIG_PARAMS = (
    -TYPE             => 'File',
    -LOG_FILE         => "$APP_DATAFILES_DIRECTORY/$APP_NAME.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX => 'DocumentManager|'
);

sub _generateEnvVarsString {
    my @env_values;
    
    my $key;
    foreach $key (keys %ENV) {
        push (@env_values, "$key=" . $ENV{$key});
    }   
    return join ("\|", @env_values);
}   
   
######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = qw(
    CSSView
    AddAcknowledgementView
    AddRecordConfirmationView
    DeleteRecordConfirmationView
    DeleteAcknowledgementView
    ModifyAcknowledgementView
    ModifyRecordConfirmationView
    SessionTimeoutErrorView
    AddRecordView
    BasicDataView
    BasicDataFastView
    PowerSearchFormView
    DetailsRecordView
    ModifyRecordView
    LogoffView
    OptionsView
);

my @ROW_COLOR_RULES = (
   {'folder' => [qw(Business 99CC99)]},
   {'folder' => [qw(Personal CC9999)]}
);

my @VIEW_DISPLAY_PARAMS = (
    
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -COLOR_FOR_EVEN_ROWS     => 'E5E5E5',
    -COLOR_FOR_ODD_ROWS      => 'FFFFFF',
    -DOCUMENT_ROOT_URL       => '/',
    -APPLICATION_LOGO               => 'logo.gif',
    -APPLICATION_LOGO_HEIGHT        => '40',
    -APPLICATION_LOGO_WIDTH         => '353',
    -APPLICATION_LOGO_ALT    => 'WebDB Demo',
    -HTTP_HEADER_PARAMS      => [-EXPIRES => '-1d'],
    -IMAGE_ROOT_URL          => '/Images/Extropia',
    -LINK_TARGET             => '_self',
    -SCRIPT_DISPLAY_NAME     => 'DocumentManager',
    -SCRIPT_NAME             => $CGI->script_name(),
    -DEFAULT_CHARSET          => 'ISO-8859-1',
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -HOME_VIEW               => 'BasicDataView',
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FORM_ENCTYPE => "MULTIPART/FORM-DATA",
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [
           [ "file" , "filename" ]
    ],
    -FIELD_NAME_MAPPINGS     => {
        folder	    => 'Folder',
        record_id	=> 'Record ID',
        file		=> 'File',
        filename    => 'Filename',
        description	=> 'Description',
        size		=> 'Size',
        username	=> 'Username'
        },
    -DISPLAY_FIELDS         => [qw(
            folder
            file
            description
            size
        )],
    -SORT_FIELDS         => [qw(
            folder
            file
            description
            size
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
            folder
            file
            description
            size
        )]
);  

######################################################################
#                           FILTER SETUP                             #
######################################################################

my @HTMLIZE_FILTER_CONFIG_PARAMS = (
    -TYPE            => 'HTMLize',
    -CONVERT_DOUBLE_LINEBREAK_TO_P => 1,
    -CONVERT_LINEBREAK_TO_BR => 1,
);

my @CHARSET_FILTER_CONFIG_PARAMS = (
    -TYPE            => 'CharSet'
);

my @EMBED_FILTER_CONFIG_PARAMS = (
    -TYPE            => 'Embed',
    -ENABLE          => 0
);

my @VIEW_FILTERS_CONFIG_PARAMS = (
     \@HTMLIZE_FILTER_CONFIG_PARAMS,
     \@CHARSET_FILTER_CONFIG_PARAMS,
     \@EMBED_FILTER_CONFIG_PARAMS
);


######################################################################
#                      ACTION/WORKFLOW SETUP                         #
######################################################################

my @ACTION_HANDLER_LIST = qw(
    Default::DisplayCSSViewAction
    Default::DisplaySessionTimeoutErrorAction
    Default::DownloadFileAction
    Default::PerformLogoffAction
    Default::PerformLogonAction
    Default::DisplayOptionsFormAction
    Default::DisplayAddFormAction
    Default::DisplayAddRecordConfirmationAction
    Default::ProcessAddRequestAction
    Default::DisplayDeleteFormAction
    Default::DisplayDeleteRecordConfirmationAction
    Default::ProcessDeleteRequestAction
    Default::DisplayModifyFormAction
    Default::ProcessModifyRequestAction
    Default::DisplayModifyRecordConfirmationAction
    Default::DisplayPowerSearchFormAction
    Default::DisplayDetailsRecordViewAction
    Default::DisplayViewAllRecordsAction
    Default::DisplaySimpleSearchResultsAction
    Default::PerformPowerSearchAction
    Default::HandleSearchByUserAction
    Default::DisplayBasicDataViewAction
    Default::DefaultAction
);

my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -BASIC_DATA_VIEW_NAME                   => 'BasicDataView',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL   => $CGI->script_name() . "?display_css_view=on",
    -CSS_VIEW_NAME  => "CSSView",
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_FILE_FIELD_LIST                 => [qw( file )],
    -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DEFAULT_SORT_FIELD1                    => 'folder',
    -DEFAULT_SORT_FIELD2                    => 'file',
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -ENABLE_SORTING_FLAG                    => 1,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FILE_FIELD_LIST                 => [qw( file )],
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 0,
    -SEND_EMAIL_ON_ADD_FLAG                 => 0,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -SIMPLE_SEARCH_BOX_VIEW_NAME            => 'SimpleSearchBoxView',
    -UPLOAD_MANAGER_CONFIG_PARAMS           => \@UPLOAD_MANAGER_CONFIG_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 10,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'folder',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'fname',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
    -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
    -KEY_FIELD               => 'record_id',
    -PAGE_TOP_VIEW           => 'PageTopView',
    -PAGE_BOTTOM_VIEW           => 'PageBottomView',
    -INPUT_WIDGET_DEFINITIONS   => \@INPUT_WIDGET_DEFINITIONS,
    -SEARCH_WIDGET_DEFINITIONS   => \@SEARCH_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 2,
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = new Extropia::Core::App::DBApp(
    -ROOT_ACTION_HANDLER_DIRECTORY => "ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() . ". Please contact the webmaster.");

print $APP->execute();
