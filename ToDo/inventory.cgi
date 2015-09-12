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
#Good For Tracing Error/Warning.
#use Carp ();
#local $SIG{__WARN__} = \&Carp::cluck;

BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules/
               ../Modules/CPAN .);
}

use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH =
    qw(../../lib/Extropia/View/BugTracker
       ../../lib/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Organic
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/d2earth
       ../HTMLTemplates/BugTracker
       ../HTMLTemplates/rv
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Default);

use CGI qw(-debug);

# Carp commented out to avoid Perl 5.60 problems. Uncomment if you use
# Perl 5.61
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
            ". Please contact the webmaster.");

foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x/);
}

######################################################################
#                          SITE SETUP                             #
######################################################################

my $APP_NAME = "";
my $MOD_NAME = "inventory";

my $APP_NAME_TITLE = "CSC.ca Inventor Modual";
my $SiteName =  $CGI->param('site') || "Inventory";

    my $homeviewname ;
    my $home_view; 
    my $BASIC_DATA_VIEW; 
    my $page_top_view;
    my $page_bottom_view;
    my $left_page_view;
#Mail settings
    my $mail_from; 
    my $mail_to;
    my $mail_replyto;
    my $CSS_VIEW_NAME = 'CSCCSSView';
    my $app_logo;
    my $app_logo_height;
    my $app_logo_width;
    my $app_logo_alt;
    my $IMAGE_ROOT_URL; 
    my $DOCUMENT_ROOT_URL;
    my $site;
    my $GLOBAL_DATAFILES_DIRECTORY;
    my $TEMPLATES_CACHE_DIRECTORY;
    my $APP_DATAFILES_DIRECTORY;
    my $DATAFILES_DIRECTORY;
    my $site_session;
    my $auth;
    my $MySQLPW;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $DBI_DSN;
    my $AUTH_TABLE;
    my $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $DataFile;
    my $ProductTable;
use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $APP_NAME_TITLE        = "CSC.ca Inventory Manager";
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $left_page_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
#Mail settings
    $mail_from             = $SetupVariables->{-MAIL_FROM}; 
    $mail_to               = $SetupVariables->{-MAIL_TO};
    $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME}||'blank';
    $app_logo              = $SetupVariables->{-APP_LOGO};
    $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE                 = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME        = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $DEFAULT_CHARSET            = $SetupVariables->{-DEFAULT_CHARSET};
    $site                       = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
 
#Add sub aplication spacific overrides.
 $GLOBAL_DATAFILES_DIRECTORY = "../../Datafiles";
 $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
 $APP_DATAFILES_DIRECTORY    = "../../Datafiles/Apps/Todo";
$page_top_view    = $CGI->param('page_top_view')||$page_top_view;
$page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
$left_page_view   = $CGI->param('page_view_left')||$left_page_view;
# $GLOBAL_DATAFILES_DIRECTORY = "../../Datafiles";
# $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
 $APP_DATAFILES_DIRECTORY    = "../../Datafiles/CSC/CSR";
    my $LocalIp            = $SetupVariables->{-LOCAL_IP};

my $VIEW_LOADER = new Extropia::Core::View
     (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        ". Please contact the webmaster.");

use constant HAS_CLASS_DATE  => eval { require Class::Date; };

                
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

my $SESSION    = $SESSION_MGR->createSession();
my $SESSION_ID = $SESSION->getId();
my $CSS_VIEW_URL ;

#Deal with site setup in session files. This code need taint checking.
if ($CGI->param('site')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'SiteName') ){
      $SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $CGI->param('site')) ;
       $SiteName = $CGI->param('site');
    }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'SiteName')) {
    $SiteName = $SESSION ->getAttribute(-KEY => 'SiteName');
  }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
      }
}
my $username =  $SESSION ->getAttribute(-KEY => 'auth_username')||'none';
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group')||'none';
my $BasicDataView = 'BasicDataView';


 if ($SiteName eq "Inventory") {
    $BasicDataView        =  'BasicDataView'||'InventroyHomeView';
    $CSS_VIEW_URL         = $SetupVariables->{-CSS_VIEW_NAME};
    $DataFile             = '../../cgi-bin/store/shops/city/Data_files/product.db';
 }
 elsif ($SiteName eq "Apis") {
use ApisSetup;
  my $UseModPerl = 0;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_URL         = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesApis->{-APP_LOGO_ALT};
    $APP_NAME_TITLE        = "Apis HelpDesk";
    $homeviewname          = 'HelpDeskHomeView';
     $DataFile             = '../../cgi-bin/store/shops/cs/Data_files/product.db';
  }
elsif ($SiteName eq "BCHPA") { 
use BCHPASetup;
  my $SetupVariablesBCHPA = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $APP_NAME_TITLE        = "British Columbia Honey Producers Customer Service Request";
    $homeviewname          = 'HelpDeskHomeView';
}  
elsif ($SiteName eq "Brew") { 
use BrewSetup;
  my $SetupVariablesBrew   = new  BrewSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesBrew->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBrew->{-AUTH_TABLE};
    $APP_NAME_TITLE        = "Brewing HelpDesk";
    $homeviewname          = 'HelpDeskHomeView';
}  
elsif ($SiteName eq "VitalVic") { 
use VitalVicSetup;
  my $SetupVariablesVitalVic   = new  VitalVicSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesVitalVic ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesVitalVic ->{-AUTH_TABLE};
    $APP_NAME_TITLE        = " VitalVic HelpDesk";
    $homeviewname          = 'HelpDeskHomeView';
     $DataFile             = '../../cgi-bin/store/shops/vitalvic/Data_files/product.db';
}  
elsif($SiteName eq "CS") {
    $APP_NAME_TITLE        = "Country Stores Helpdesk.";
    $homeviewname          = 'HelpDeskHomeView';
     $DataFile             = '../../cgi-bin/store/shops/cs/Data_files/product.db';
}
elsif ($SiteName eq "CSC"){
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC  = new CSCSetup($UseModPerl);
    $APP_NAME_TITLE        = "Computer System Consulting.ca";
    $homeviewname          = 'HelpDeskHomeView';
    $CSS_VIEW_NAME         = $SetupVariablesCSC->{-CSS_VIEW_NAME};
     $DataFile             = '../../cgi-bin/store/shops/csc/Data_files/product.db';

}
elsif ($SiteName eq "d2earth") {
use d2earthSetup;
  my $UseModPerl = 0;
  my $SetupVariablesd2earth   = new d2earthSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesd2earth->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesd2earth->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariablesd2earth->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesd2earth->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesd2earth->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesd2earth->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesd2earth->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesd2earth->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesd2earth->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesd2earth->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesd2earth->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesd2earth->{-HOME_VIEW};

 }
elsif ($SiteName eq "rv") {
use RVSetup;
  my $SetupVariablesRV       = new  RVSetup($UseModPerl);
    $AUTH_TABLE              = $SetupVariablesRV ->{-AUTH_TABLE};
    $APP_NAME_TITLE          = "Rancho Vignola ToDo";
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesRV->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesRV->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesRV->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesRV->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/rv'; 
    $app_logo                = $SetupVariablesRV->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesRV->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesRV->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesRV->{-APP_LOGO_ALT};
    $mail_from               = $SetupVariablesRV->{-MAIL_FROM}; 
    $mail_to                 = $SetupVariablesRV->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesRV->{-MAIL_REPLYTO};
    $DataFile                = '../../cgi-bin/store/shops/rv/Data_files/product.db';  
   $ProductTable         = 'rv_product';
}

   $left_page_view        = $CGI->param('page_left_view')||$left_page_view;
my $modify = '1';
my $delete = '1';

 if ($username eq "Shanta"  ) {
    $modify = '0';
    $delete = '0';
}
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
    developer_status
);

#CSC comversion to auth swiching from SiteSetup.pm At momet this is only set to switch from
# file to MySQL

my @AUTH_USER_DATASOURCE_PARAMS;
if ($site eq "file") {

	@AUTH_USER_DATASOURCE_PARAMS = (
	    -TYPE                       => 'File',
	    -FIELD_DELIMITER            => '|',
	    -CREATE_FILE_IF_NONE_EXISTS => 1,
	    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
	    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.users.dat"
	);
}
else {

   @AUTH_USER_DATASOURCE_PARAMS = (
        -TYPE         => 'DBI',
        -DBI_DSN      => $DBI_DSN,
        -TABLE        => $AUTH_TABLE,
        -USERNAME     => $AUTH_MSQL_USER_NAME,
        -PASSWORD     => $MySQLPW,
        -FIELD_NAMES  => \@AUTH_USER_DATASOURCE_FIELD_NAMES
    );
}

# mysql database
#my @AUTH_USER_DATASOURCE_PARAMS = (
#    -TYPE                       => 'DBI',
#    -DBI_DSN                    => 'mysql:host=127.0.0.1;database=foo',
#    -TABLE                      => 'bugz_auth',
#    -USERNAME                   => 'foo',
#    -PASSWORD                   => 'foo',
#    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
#    -KEY_FIELDS                 => ['username']
#);



my @AUTH_ENCRYPT_PARAMS = (
    -TYPE => 'Crypt'
);

my %USER_FIELDS_TO_DATASOURCE_MAPPING = (
    'auth_username'  => 'username',
    'auth_password'  => 'password',
    'auth_firstname' => 'firstname',
    'auth_lastname'  => 'lastname',
    'auth_groups'    => 'groups',
    'auth_email'     => 'email',
    'auth_developer_status' => 'developer_status'
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
    -SITE_NAME            => $SiteName,
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $APP_NAME_TITLE,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -LINK_TARGET             => $LINK_TARGET,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -LEFT_PAGE_VIEW          => $left_page_view,
    -LINK_TARGET             => $LINK_TARGET,
    -DEFAULT_CHARSET         => $DEFAULT_CHARSET,
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
                'auth_email'        => 'E-Mail Address',
                'auth_developer_status' => 'Are you a developer?'

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
    auth_developer_status
));

my %USER_FIELD_NAME_MAPPINGS = (
    'auth_username'  => 'Username',
    'auth_password'  => 'Password',
    'auth_groups'    => 'Groups',
    'auth_firstname' => 'First Name',
    'auth_lastname'  => 'Last Name',
    'auth_email'     => 'E-Mail',
    'auth_developer_status'     => 'Developer?'
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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Registration Notification'
);

my @AUTH_MANAGER_CONFIG_PARAMS = (
    -TYPE                        => 'CGI',
    -ADMIN_MAIL_SEND_PARAMS      => \@ADMIN_MAIL_SEND_PARAMS,
    -AUTH_VIEW_PARAMS            => \@AUTH_VIEW_DISPLAY_PARAMS,
    -MAIL_PARAMS                 => \@MAIL_PARAMS,
    -USER_MAIL_SEND_PARAMS       => \@USER_MAIL_SEND_PARAMS,
    -SESSION_OBJECT              => $SESSION,
    -VIEW_LOADER                 => $VIEW_LOADER,
    -AUTH_PARAMS                 => \@AUTH_CONFIG_PARAMS,
    -CGI_OBJECT                  => $CGI,
    -ALLOW_REGISTRATION          => 1,   
    -ALLOW_USER_SEARCH           => 0,
    -USER_SEARCH_FIELD           => 'auth_email',
    -GENERATE_PASSWORD           => 0,
    -DEFAULT_GROUPS              => 'normal',
    -EMAIL_REGISTRATION_TO_ADMIN => 1,
    -USER_FIELDS                 => \@USER_FIELDS,
    -USER_FIELD_TYPES            => \%USER_FIELD_TYPES,
    -USER_FIELD_NAME_MAPPINGS    => \%USER_FIELD_NAME_MAPPINGS,
    -DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE => 1,
    -AUTH_REGISTRATION_DH_MANAGER_PARAMS => \@AUTH_REGISTRATION_DH_MANAGER_PARAMS,
    -LOGON_VIEW                  => 'AuthManager/CGI/LogonScreen',
    -REGISTRATION_VIEW           => 'RegistrationScreen',
    -REGISTRATION_SUCCESS_VIEW   => 'AuthManager/CGI/RegistrationSuccessScreen',
    -SEARCH_VIEW                 => 'AuthManager/CGI/SearchScreen',
    -SEARCH_RESULTS_VIEW         => 'AuthManager/CGI/SearchResultsScreen',

);

######################################################################
#                      UPLOAD MANAGER SETUP                          #
######################################################################

my @UPLOAD_MANAGER_CONFIG_PARAMS = (
                -TYPE         => 'Simple',
                # Session is required as storeUploadedFile in Simple.pm require to get and set attribute into Session.
                -SESSION_OBJECT => $SESSION,
                -CGI_OBJECT   => $CGI,
                -UPLOAD_FIELD => 'attach',
                -FIELD_TO_SET_UPLOAD_FILENAME => 'attach_filename',
                -KEY_GENERATOR_PARAMS => [
                    -TYPE               => 'Random',
                    -SECRET_ELEMENT     => 'RECRUIT',
                    -LENGTH             => 0
                ],
                -UPLOAD_DIRECTORY => "$APP_DATAFILES_DIRECTORY/Uploads",
);



######################################################################
#                      DATA HANDLER SETUP                            #
######################################################################

my @ADD_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Exists
        HTML
        Email
        Number
        String
        Upload
        )],

    -FIELD_MAPPINGS => {
        abstract        => 'Abstract',
        priority        => 'Priority',
        reporter        => 'Reporter',
        developer       => 'Developer',
        details         => 'Details',
        status          => 'Status',
        attach          => 'Attachment',
        resolution_text => 'Problem Resolution',
    },

    -RULES => [
 #       -ESCAPE_HTML_TAGS => [
 #           -FIELDS => [qw(
 #               *
 #           )],
 #       ],

        -UPLOAD_FILE => [
            -FIELDS => [qw(
                attach
                )],
            -UPLOAD_MANAGER_PARAMS => \@UPLOAD_MANAGER_CONFIG_PARAMS,
            -ADD_SESSION_ID_AS_GET_PARAM => 1,

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
                abstract
            )],
        ],
    ]
);

my @MODIFY_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Exists
        HTML
        Email
        Number
        String
        Upload
        )],

    -FIELD_MAPPINGS => {
        'abstract'        => 'Abstract',
        'priority'        => 'Priority',
        'reporter'        => 'Reporter',
        'developer'       => 'Developer',
        'details'         => 'Details',
        'status'          => 'Status',
        'attach'          => 'Attachment',
        'resolution_text' => 'Problem Resolution',
    },

    -RULES => [
#        -ESCAPE_HTML_TAGS => [
#            -FIELDS => [qw(
#                *
#            )],
#        ],

        -UPLOAD_FILE => [
            -FIELDS => [qw(
                attach
                )],
            -UPLOAD_MANAGER_PARAMS => \@UPLOAD_MANAGER_CONFIG_PARAMS,
            -ADD_SESSION_ID_AS_GET_PARAM => 1

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
                abstract
            )],
        ],

    ]
);

my @DATA_HANDLER_MANAGER_CONFIG_PARAMS = (
    -ADD_FORM_DHM_CONFIG_PARAMS    => \@ADD_FORM_DHM_CONFIG_PARAMS,
    -MODIFY_FORM_DHM_CONFIG_PARAMS => \@MODIFY_FORM_DHM_CONFIG_PARAMS,
);

######################################################################
#                      DATASOURCE SETUP                              #
######################################################################

my @DATASOURCE_FIELD_NAMES = 
    qw(
       ProductID 
       CategoryID
       DiscountID
       ProductPrice
       ProductTaxable 
       ManufacturerID 
       AuthorID 
       ManufacturerPID
       ProductShortDescriptionENG 
       ProductShortDescriptionGER 
       ProductLongDescriptionENG 
       ProductLongDescriptionGER
       ProductImageURL 
       ProductImageThmbURL 
       ProductAssociateLink 
       ProductOptions 
       ProductDeliveryMethod 
       ProductDownloadData
       ProductShipsIndividually  
       ProductPackingFactor 
       ProductMinimumOrder  
       ProductMaximumOrder 
       ProductExpires 
       ProductDisabled 
       ProductWeight 
       ReleaseDate
      );

my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     priority => [
                  -DISPLAY_NAME => 'Priority',
                  -TYPE         => 'popup_menu',
                  -NAME         => 'priority',
                  -VALUES       => [qw(1 2 3 4 5)]
                 ],

     ProductDisabled => [
                -DISPLAY_NAME => 'Check this box if you want to disable the item from the active database',
                -TYPE         => 'checkbox',
                -NAME         => 'ProductDisabled',
 #               -VALUES       => [qw(Reported Requested In-Progress Fixed Not-A-Bug)]
               ],

            ProductID => [
                  -DISPLAY_NAME => 'Product ID',
                  -TYPE         => 'textfield',
                  -NAME         => 'ProductID',
                  -SIZE         => 30,
                  -MAXLENGTH    => 80
                 ],

     details => [
                 -DISPLAY_NAME => 'Details. Tell us about your problem, Past error messages,
                                    any other details that will help us solve your problem. ',
                 -TYPE         => 'textarea',
                 -NAME         => 'details',
                 -ROWS         => 6,
                 -COLS         => 30,
                 -WRAP         => 'VIRTUAL'
                ],

     attach => [
                -DISPLAY_NAME => 'Attachment',
                -TYPE         => 'filefield',
                -NAME         => 'attach',
                -SIZE         => 30,
                -MAXLENGTH    => 80
               ],

     reporter => [
                -DISPLAY_NAME => 'Reporter',
                -TYPE         => 'textfield',
                -NAME         => 'reporter',
		-VALUE        => $username,
                -SIZE         => 30,
                -MAXLENGTH    => 80
               ],

     attach_filename => [
                -DISPLAY_NAME => 'Attachment filename',
                -TYPE         => 'textfield',
                -NAME         => 'attach_filename',
                -SIZE         => 30,
               ],

     resolution_text => [
                 -DISPLAY_NAME => 'Problem Resolution',
                 -TYPE         => 'textarea',
                 -NAME         => 'resolution_text',
                 -ROWS         => 6,
                 -COLS         => 30,
                 -WRAP         => 'VIRTUAL'
                ],
     resolution => [
                 -DISPLAY_NAME => 'Problem Resolution',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'resolution_text',
                ],

    accepted_date  => [
                  -DISPLAY_NAME => 'Accepted Date',
                  -TYPE         => 'textfield',
                  -NAME         => 'accepted_date',
                  -SIZE         => 10,
                  -MAXLENGTH    => 10
                 ],

     accepted_by => [
                  -DISPLAY_NAME => 'Accepted By',
                  -TYPE         => 'textfield',
                  -NAME         => 'accepted_by',
                  -SIZE         => 20,
                  -MAXLENGTH    => 50
                 ],

            CategoryID => [
                  -DISPLAY_NAME => 'CategoryID',
                  -TYPE         => 'textfield',
                  -NAME         => 'CategoryID',
                  -SIZE         => 10,
                  -MAXLENGTH    => 10
                 ],


    );

my %ACTION_HANDLER_PLUGINS =
    (

     'Default::ProcessAddRequestAction' =>
     {
      -BeforeEmail     => [qw(Plugin::BugTracker::BeforeEmail)],
     },
    );


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER;
 if ( $group eq "CSC_Admin" ||  $username eq "Shanta") {
@BASIC_INPUT_WIDGET_DISPLAY_ORDER =
    qw(
       ProductID
       CategoryID
       ProductDisabled
      );

}else{
@BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    qw(
       ProductID
       CategoryID
       ProductPrice
      );
}
#       ProductShortDescriptionENG
#       ProductLongDescriptionENG

my @SEARCH_INPUT_WIDGET_DISPLAY_ORDER = 
    qw(
     );

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);

my @SEARCH_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@SEARCH_INPUT_WIDGET_DISPLAY_ORDER
);
#$site = 'file';

my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (    -TYPE                       => 'File', 
    -FILE                       => $DataFile||'../../Datafiles/CSC/product.db',
    -FIELD_DELIMITER            => '|',
    -COMMENT_PREFIX             => '#',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['ProductID'],
    -FIELD_TYPES                => {
                                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
                                   },
);
}
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => 'mysql:host=localhost;database=forager_stores',
	        -TABLE        => $ProductTable,
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
	        },
	);

    }

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################

my @MAIL_CONFIG_PARAMS = 
    (
     -TYPE         => 'Sendmail'
    );

my @EMAIL_DISPLAY_FIELDS = 
    qw(
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE."Sevice request Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE."Sevice request Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE."Sevice request Modification"
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
    -LOG_ENTRY_PREFIX => 'Bug Tracker|'
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
       ENCYCSSView
       CSPSCSSView
       CSCCSSView
       VitalVicCSSView
       ECFCSSView
       d2earthCSSView
       BCHPACSSView
       ApisCSSView
       ContactView

    AddAcknowledgementView
    AddRecordConfirmationView
    DeleteRecordConfirmationView
    DeleteAcknowledgementView
    ModifyAcknowledgementView
    ModifyRecordConfirmationView
    SessionTimeoutErrorView
    AddRecordView
    PowerSearchFormView
    BasicDataView
    DetailsRecordView
    ModifyRecordView
    LogoffView
    OptionsView
    InventroyHomeView
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
    -DEFAULT_CHARSET                => $DEFAULT_CHARSET,
    -APPLICATION_SUB_MENU_VIEW_NAME => 'ApplicationSubMenuView',
    -IMAGE_ROOT_URL     => $IMAGE_ROOT_URL,
    -LINK_TARGET        => $LINK_TARGET,
    -HTTP_HEADER_PARAMS => $HTTP_HEADER_PARAMS,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -SCRIPT_NAME              => $CGI->script_name(),
    -SCRIPT_DISPLAY_NAME=> $APP_NAME_TITLE,
    -EMAIL_DISPLAY_FIELDS     => \@EMAIL_DISPLAY_FIELDS,
    -HOME_VIEW                => 'BasicDataView',
    -FIELD_NAME_MAPPINGS      => {
        'ProductID'  => 'Product ID',
        'CategoryID'  => 'Category ID',
        'ProductPrice'  => 'ProductPrice',
        'ProductShortDescriptionENG' => 'Product Short Description ENG',
        'ProductLongDescriptionENG'   => 'Product Long Description ENG',
        },
    -DISPLAY_FIELDS        => [qw(
				  ProductID
				  CategoryID
				  ProductPrice
				  ProductShortDescriptionENG 
        )],
    -SORT_FIELDS        => [qw(
			       CategoryID 
			       ProductID 
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
					   ProductID
					   CategoryID
					   ProductPrice
					   ProductShortDescriptionENG 
        )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [
        ['attach','attach_filename'],
    ],
    -FORM_ENCTYPE => "MULTIPART/FORM-DATA",
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
            ProductShortDescriptionENG 
	    ProductLongDescriptionENG
     )],
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
#       BugTracker::PopulateInputWidgetDefinitionListWithUsersWidgetAction

my @ACTION_HANDLER_LIST = 
    qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction
       Default::DisplaySessionTimeoutErrorAction
       BugTracker::PopulateInputWidgetDefinitionListWithDevelopersWidgetAction
       Default::PerformLogoffAction
       Default::PerformLogonAction
       Default::DownloadFileAction
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
       BugTracker::ProcessShowAllOpenBugsAction
       BugTracker::ProcessShowAllOpenBugsPostedToUserAction
       BugTracker::ProcessShowAllOpenBugsPostedByUserAction
       BugTracker::ProcessShowAllBugsPostedToUserAction
       BugTracker::ProcessShowAllBugsPostedByUserAction
       BugTracker::ProcessShowAllBugsAction
       Default::PerformPowerSearchAction
       Default::HandleSearchByUserAction
       Default::DisplayBasicDataViewAction
       Default::DefaultAction
      );

my @ACTION_HANDLER_ACTION_PARAMS = 
    (
     -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
     -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
     -AUTH_USER_DATASOURCE_PARAMS            => \@AUTH_USER_DATASOURCE_PARAMS,
     -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
     -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
     -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
     -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
     -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
     -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
     -ALLOW_ADDITIONS_FLAG                   => 0,
     -ALLOW_DELETIONS_FLAG                   => 0,
     -ALLOW_MODIFICATIONS_FLAG               => 1,
     -ALLOW_DUPLICATE_ENTRIES                => 0,
     -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
     -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
     -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
     -BASIC_DATA_VIEW_NAME                   => $BasicDataView,
     -CGI_OBJECT                             =>  $CGI,
     -CSS_VIEW_URL                           => $CSS_VIEW_URL,
     -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
     -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
     -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
     -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
     -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
     -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
     -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1, 
     -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
     -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1, 
     -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
     -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
     -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
     -DEFAULT_SORT_FIELD1                    => 'title',
     -DEFAULT_SORT_FIELD2                    => 'abstract',
     -ENABLE_SORTING_FLAG                    => 0,
     -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'BugTrackerHiddenAdminFieldsView',
    -LOCAL_IP                               => $LocalIp,
     -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'BugTrackerURLEncodedAdminFieldsView',
     -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
     -LOGOFF_VIEW_NAME                       => 'LogoffView',
     -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
     -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
     -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
     -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
     -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
     -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0, 
     -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
     -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
     -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
     -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 1,
     -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $modify,
     -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => $delete,
     -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
     -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
     -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
     -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
     -SEND_EMAIL_ON_DELETE_FLAG              => 1,
     -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
     -SEND_EMAIL_ON_ADD_FLAG                 => 1,
     -SESSION_OBJECT                         => $SESSION,
     -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
     -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
     -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
     -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
     -VALID_VIEWS                            => \@VALID_VIEWS,
     -VIEW_LOADER                            => $VIEW_LOADER,
     -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
     -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 25,
     -SORT_FIELD1                            => $CGI->param('sort_field1') || 'category',
     -SORT_FIELD2                            => $CGI->param('sort_field2') || 'fname',
     -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
     -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
     -UPLOAD_MANAGER_CONFIG_PARAMS           => \@UPLOAD_MANAGER_CONFIG_PARAMS,
     -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
     -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
     -KEY_FIELD                              => 'record_id',
    -SITE_NAME            => $SiteName,
    -PAGE_TOP_VIEW           =>  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $left_page_view,
    -PAGE_LEFT_VIEW          =>  $left_page_view,
    -PAGE_BOTTOM_VIEW        =>  $page_bottom_view,
    -SELECT_FORUM_VIEW		=> 'SelectForumView',
     -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
     -SEARCH_WIDGET_DEFINITIONS              => \@SEARCH_WIDGET_DEFINITIONS,
     -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 2,
     -MODIFY_FILE_FIELD_LIST                 => [qw(attach)],
     -ACTION_HANDLER_PLUGINS                 => \%ACTION_HANDLER_PLUGINS,
    );

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = new Extropia::Core::App::DBApp(
    -ROOT_ACTION_HANDLER_DIRECTORY => "../ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() . ". Please contact the webmaster.");

print $APP->execute();
