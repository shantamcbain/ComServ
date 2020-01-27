94 - 2001  eXtropia.com
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

my @VIEWS_SEARCH_PATH = 
    qw(Modules/Extropia/View/AddressBook
       Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/ENCY
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/AddressBook
       ../HTMLTemplates/Default);

use CGI qw(-debug);
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");

######################################################################
#                          SITE SETUP                             #
######################################################################

my $SiteName =  $CGI->param('site') || "ENCY";
my $APP_NAME = "diseases_admin";
my $APP_NAME_TITLE = 'ENCY Diseases';
my $SITE_DISPLAY_NAME = 'None Defined for this site.';

    my $homeviewname         ;
    my $home_view            ;
    my $BASIC_DATA_VIEW      ;
    my $page_top_view        ;
    my $page_bottom_view     ;
    my $left_page_view       ;
    my $MySQLPW;
#Mail settings
    my $mail_from            ;
    my $mail_to              ;
    my $mail_replyto         ;
    my $CSS_VIEW_NAME        ;
    my $app_logo             ;
    my $app_logo_height      ;
    my $app_logo_width       ;
    my $app_logo_alt             ;
    my $IMAGE_ROOT_URL       ;
    my $DOCUMENT_ROOT_URL    ;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $GLOBAL_DATAFILES_DIRECTORY ;
    my $TEMPLATES_CACHE_DIRECTORY;
    my $APP_DATAFILES_DIRECTORY;
    my $site;
    my $DATAFILES_DIRECTORY;
    my $site_session;
    my $auth;
    my $datafile;
    my $HasMembers = 0;

  my $UseModPerl = 0;
  my $SiteNameSetup = $SiteName."Setup";
  use ENCYSetup;
  my $SetupVariables  = new ENCYSetup($UseModPerl);
  $APP_NAME_TITLE        = $SiteName.": ". $APP_NAME_TITLE;


  $home_view             = $SetupVariables->{-HOME_VIEW}; 
  $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
  $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
  $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
  $left_page_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
  #Mail settings
 $mail_from             = $SetupVariables->{-MAIL_FROM}; 
  $mail_to               = $SetupVariables->{-MAIL_TO};
  $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
  $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
  $app_logo              = $SetupVariables->{-APP_LOGO};
  $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
  $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
  $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
  $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
  $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};

  $site = $SetupVariables->{-DATASOURCE_TYPE};
  $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
  $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
  $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};

#script override Variables
  $mail_from        = "$CGI->param('email')||$mail_from"; 
  $homeviewname     = 'BasicDataView';
my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60 * 8,
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
my $CSS_VIEW_URL = $CGI->script_name(). "?display_css_view=on&session_id=$SESSION_ID";
  $CSS_VIEW_URL          = $SetupVariables->{-CSS_VIEW_NAME};
 
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


if ($SiteName eq "Organic") {
use OrganicSetup;
  my $UseModPerl = 0;
  my $SetupVariablesOrganic   = new OrganicSetup($UseModPerl);
    $page_top_view         = $SetupVariablesOrganic->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesOrganic->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesOrganic->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesOrganic->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesOrganic->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesOrganic->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesOrganic->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesOrganic->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesOrganic->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
 }
 elsif ($SiteName eq "ECF") {
use ECFSetup;
  my $SetupVariablesECF    = new  ECFSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesECF->{-APP_LOGO_ALT};
    $homeviewname            = $SetupVariablesECF->{-HOME_VIEW_NAME};
    $home_view               = $SetupVariablesECF->{-HOME_VIEW};
#Mail settings
    $mail_from               = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS      = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
 }
 elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $SetupVariablesENCY    = new  ENCYSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesENCY->{-SITE_DISPLAY_NAME};
 }

 elsif ($SiteName eq "SB") {
use SBSetup;
  my $SetupVariablesSB    = new  SBSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesSB->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesSB->{-AUTH_TABLE};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesSB->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesSB->{-HTTP_HEADER_DESCRIPTION};
    $APP_NAME                = "vitavic";
    $mail_to                 = $SetupVariablesSB->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesSB->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/VitalVic'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesSB->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "VitalVic") {
use VitalVicSetup;
  my $SetupVariablesVitalVic     = new  VitalVicSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesVitalVic->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesVitalVic->{-AUTH_TABLE};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesVitalVic->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesVitalVic->{-HTTP_HEADER_DESCRIPTION};
    $mail_to                 = $SetupVariablesVitalVic->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesVitalVic->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/VitalVic'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesVitalVic->{-SITE_DISPLAY_NAME};
}
elsif ($SiteName eq "Apis") {
use ApisSetup;
  my $SetupVariablesApis  = new  ApisSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesApis->{-AUTH_TABLE};
    $page_top_view           = $SetupVariablesApis->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesApis->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesApis->{-PAGE_LEFT_VIEW};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesApis->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesApis->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $homeviewname            = 'ApisHomeView';
    $home_view               = $SetupVariablesApis ->{-HOME_VIEW}; 
    $matchuser               = '1';
    $matchgroup              =1;
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
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
);
my @AUTH_USER_DATASOURCE_PARAMS;
if ($site eq "file") {

	@AUTH_USER_DATASOURCE_PARAMS = (
	    -TYPE                       => 'File',
	    -FIELD_DELIMITER            => '|',
	    -CREATE_FILE_IF_NONE_EXISTS => 1,
	    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
	    -FILE                       => $auth
	);
}
else {

   @AUTH_USER_DATASOURCE_PARAMS = (
        -TYPE         => 'DBI',
        -DBI_DSN      => 'mysql:host=localhost;database=forager',
        -TABLE        => 'ency_user_auth_tb',
        -USERNAME     => 'forager',
        -PASSWORD     => $MySQLPW,
        -FIELD_NAMES  => \@AUTH_USER_DATASOURCE_FIELD_NAMES
    );
}


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
    -SITE_NAME            => $SiteName,
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $APP_NAME_TITLE,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW                          => $CGI->param('page_top_view')||$page_top_view,
    -PAGE_BOTTOM_VIEW                       => $CGI->param('page_bottom_view')||$page_bottom_view,
    -LEFT_PAGE_VIEW                         => $CGI->param('left_page_view')||$left_page_view,
    -LINK_TARGET             => '_self'
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
    
my @USER_FIELDS = 
    qw(
       auth_username
       auth_password
       auth_groups
       auth_firstname
       auth_lastname
       auth_email
      );

my %USER_FIELD_NAME_MAPPINGS = (
    'auth_username'  => 'Username',
    'auth_password'  => 'Password',
    'auth_groups'    => 'Groups',
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
    -TO      => '$mail_to',
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO      => '$mail_to',
    -SUBJECT => $APP_NAME_TITLE.' Registration Notification'
);
                
my @AUTH_MANAGER_CONFIG_PARAMS = (
    -TYPE                        => 'CGI',
    -ADMIN_MAIL_SEND_PARAMS      => \@ADMIN_MAIL_SEND_PARAMS,
    -AUTH_VIEW_PARAMS            => \@AUTH_VIEW_DISPLAY_PARAMS,
    -MAIL_PARAMS                 => \@MAIL_PARAMS,
    -USER_MAIL_SEND_PARAMS       => \@USER_MAIL_SEND_PARAMS,
    -SESSION_OBJECT              => $SESSION,
    -LOGON_VIEW                  => 'AuthManager/CGI/LogonScreen',
    -REGISTRATION_VIEW           => 'AuthManager/CGI/RegistrationScreen',
    -REGISTRATION_SUCCESS_VIEW   => 'AuthManager/CGI/RegistrationSuccessScreen',
    -SEARCH_VIEW                 => 'AuthManager/CGI/SearchScreen',
    -SEARCH_RESULTS_VIEW         => 'AuthManager/CGI/SearchResultsScreen',
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
    -AUTH_REGISTRATION_DH_MANAGER_PARAMS => \@AUTH_REGISTRATION_DH_MANAGER_PARAMS
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
        )],

    -FIELD_MAPPINGS => {
        'disease_code    '   => 'Disease Code',
        'name'               => 'Names if Disease',
        'description'        => 'Description',
        'category'           => 'Medical name',
        'key_name'           => 'Key_Name',
        'active'             => 'Active',
        'visibility'         => 'Visibility',
        'comments'           => 'Comments'
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                
            )]
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\\',
            -ERROR_MESSAGE => "You may not have a '\\' character in the " .
                              "%FIELD_NAME% field."
        ],

        -IS_EMAIL => [
            -FIELDS => [qw(
                email
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
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
                name
                desease_code
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
        )],

    -FIELD_MAPPINGS => {
        'desease_code    '   => 'Desease Code',
        'name'               => 'Names if Desease',
        'description'        => 'Description',
        'category'           => 'Medical name',
        'key_name'           => 'Key_Name',
        'active'             => 'Active',
        'visibility'         => 'Visibility',
        'comments'           => 'Comments'
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                
            )]
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                
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

        -IS_EMAIL => [
            -FIELDS => [qw(
                email
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
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
                name
                desease_code
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
        record_id
        desease_code
        name
        display_name
        description
        comments
        medical_uses
        active
        visibility
        url
        contra_indications
        history
        reference
        username_of_poster
        group_of_poster
        date_time_posted
);


my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    therapeutic_action => [
        -DISPLAY_NAME => 'Therapeutic Action',
        -TYPE         => 'checkbox_group',
        -NAME         => 'therapeutic_action',
        -VALUES       => [qw(alterative Antipyretic Antiseptic Antispasmodic Aromatic Astringent Carminative Cholagogue Cordial Demulcent Diaphoretic Diuretic Emmenagogue Expectorant Hemostatic  Hypotensive Mucilaginous Nervine Pungent Stimulant Stomatic Sudforific Tonic Urinary Vulinary)]
    ],

    preparation => [
        -DISPLAY_NAME => 'Preparation',
        -TYPE         => 'checkbox_group',
        -NAME         => 'preparation',
        -VALUES       => [qw(Decoction Fluid_extract Infusion Oil Ointment Poltice Powder Tincutre)]
    ],

    desease_code => [
        -DISPLAY_NAME => 'Disease Code',
        -TYPE         => 'textfield',
        -NAME         => 'desease_code',
        -SIZE         => 50,
        -MAXLENGTH    => 500
    ],

    solvents => [
        -DISPLAY_NAME => 'Solvents',
        -TYPE         => 'textfield',
        -NAME         => 'solvents',
        -SIZE         => 50,
        -MAXLENGTH    => 500
    ],

    name => [
        -DISPLAY_NAME => 'Disease  Name',
        -TYPE         => 'textarea',
        -NAME         => 'name',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    chinese => [
        -DISPLAY_NAME => 'Chinese',
        -TYPE         => 'textarea',
        -NAME         => 'chinese',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],
    contra_indications => [
        -DISPLAY_NAME => 'Contra Indications',
        -TYPE         => 'textarea',
        -NAME         => 'contra_indications',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    cultivation => [
        -DISPLAY_NAME => 'Cultivation',
        -TYPE         => 'textarea',
        -NAME         => 'cultivation',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    dosage => [
        -DISPLAY_NAME => 'Dosage',
        -TYPE         => 'textarea',
        -NAME         => 'dosage',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    formulas => [
        -DISPLAY_NAME => 'formulas',
        -TYPE         => 'textarea',
        -NAME         => 'formulas',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    non_med => [
        -DISPLAY_NAME => 'non_med',
        -TYPE         => 'textarea',
        -NAME         => 'non_med',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    description => [
        -DISPLAY_NAME => 'Description',
        -TYPE         => 'textarea',
        -NAME         => 'description',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
     ],

    harvest => [
        -DISPLAY_NAME => 'Harvest',
        -TYPE         => 'textarea',
        -NAME         => 'harvest',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    history => [
        -DISPLAY_NAME => 'History',
        -TYPE         => 'textarea',
        -NAME         => 'history',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    display_name => [
        -DISPLAY_NAME => 'Display Name',
        -TYPE         => 'textfield',
        -NAME         => 'display_name',
        -SIZE         => 50,
        -MAXLENGTH    => 80
    ],

    reference => [
        -DISPLAY_NAME => 'reference',
        -TYPE         => 'scrolling_list',
        -NAME         => 'reference',
        -VALUES       => [
            '6.  Back to Eden, Jethro Kloss.',
            '10. Dominion Herbal Collage.',
            '1.  The Encyclopedia of Herbs and Herbalism. Stuart.',
            '2.  The Herb Book. John Lust.',
            '24. The Herbalist. Joseph E Meyer.',
            '3.  Indian Herbology of North America. Alma Hutchens.',
            '27. Kings Dispensary',
            '22. Natural Healing With Herbs. Humbart Santillo.',
            '4.  Modern Encyclopedia of herbs. Joseph Kadans.',
            '11. Normay Myers Course',
            '21. Peoples Desk Reference. E. Joseph Montagna.',
            '22. School of Natural Healng. Dr. John Christopher',
            '25. Shanta McBain Personal use and experiance', #/12-Count',
         ], 
        -SIZE         => 5,
        -MULTIPLE     => 1
    ],

    flowers => [
        -DISPLAY_NAME => 'Flowers',
        -TYPE         => 'textfield',
        -NAME         => 'flowers',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    root => [
        -DISPLAY_NAME => 'Root',
        -TYPE         => 'textfield',
        -NAME         => 'root',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    constituents => [
        -DISPLAY_NAME => 'Constituents',
        -TYPE         => 'textarea',
        -NAME         => 'constituents',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    medical_uses => [
        -DISPLAY_NAME => 'Etiology',
        -TYPE         => 'textarea',
        -NAME         => 'medical_uses',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    active => [
        -DISPLAY_NAME => 'Active Yes/No',
        -TYPE         => 'popup_menu',
        -NAME         => 'active',
        -VALUES  => [
                   '0',
                   '1',
       ],
        -LABELS  => { 
               '0' 	=> 'No',
               '1'	=> 'Yes',
      }
    ],

    sister_plants => [
        -DISPLAY_NAME => 'Sister Plants',
        -TYPE         => 'textfield',
        -NAME         => 'sister_plants',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    visibility => [
        -DISPLAY_NAME => 'Visibility',
        -TYPE         => 'popup_menu',
        -NAME         => 'visibility',
        -VALUES  => [
                   '1',
                   '0',
                   '2',
       ],
        -LABELS  => { 
               '1'	=> 'Public',
               '0' 	=> 'Private',
               '2'	=> 'Paid',
      }
    ],

    leaves => [
        -DISPLAY_NAME => 'Leaves',
        -TYPE         => 'textfield',
        -NAME         => 'leaves',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    fruit => [
        -DISPLAY_NAME => 'Fruit',
        -TYPE         => 'textfield',
        -NAME         => 'fruit',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    taste => [
        -DISPLAY_NAME => 'Taste',
        -TYPE         => 'textfield',
        -NAME         => 'taste',
        -SIZE         => 50,
        -MAXLENGTH    => 250
    ],

    odour => [
        -DISPLAY_NAME => 'Odour',
        -TYPE         => 'textfield',
        -NAME         => 'odour',
        -SIZE         => 50,
        -MAXLENGTH    => 150
    ],

    distribution => [
        -DISPLAY_NAME => 'Distribution',
        -TYPE         => 'textarea',
        -NAME         => 'distribution',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
   ],

    administration    => [
        -DISPLAY_NAME => 'Administration',
        -TYPE         => 'textarea',
        -NAME         => 'administration',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
   ],
    url => [
        -DISPLAY_NAME => 'Url',
        -TYPE         => 'textfield',
        -NAME         => 'url',
        -SIZE         => 50,
        -MAXLENGTH    => 80
    ],

    vetrinary => [
        -DISPLAY_NAME => 'vetrinary',
        -TYPE         => 'textarea',
        -NAME         => 'vetrinary',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ],

    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL'
    ]
);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
        desease_code   
        name   
        display_name   
        active
        visibility
        description   
        medical_uses
        chinese
        history
        url
        comments
        reference
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (
    -TYPE                       => 'File', 
    -FILE                       => $APP_DATAFILES_DIRECTORY/$APP_NAME,
    -FIELD_DELIMITER            => '|',
    -COMMENT_PREFIX             => '#',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -COMMENT_PREFIX             => '#',
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['record_id'],
    -FIELD_TYPES                => {
        record_id        => 'Autoincrement'
    },
);
}
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => 'mysql:host=localhost;database=forager',
	        -TABLE        => 'ency_deseases_tb',
	        -USERNAME     => 'forager',
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

}
#my @BASIC_DATASOURCE_CONFIG_PARAMS = (
#    -TYPE                       => 'File', 
#    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
#    -FIELD_DELIMITER            => '|',
#    -COMMENT_PREFIX             => '#',
#    -CREATE_FILE_IF_NONE_EXISTS => 1,
#    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
#    -KEY_FIELDS                 => ['record_id'],
#    -FIELD_TYPES                => {
#        record_id        => 'Autoincrement'
#    },
#);

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
        therapeutic_action
        desease_code
        name
        display_name
        description
        comments
);


my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Modification"
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
    -LOG_FILE         => "../DataFiles/ENCY/$APP_NAME.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX =>  '$APP_NAME_TITLE |'
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
    AddRecordView
    BasicDataView
    DetailsRecordView
    AddAcknowledgementView
    AddRecordConfirmationView
    DeleteRecordConfirmationView
    DeleteAcknowledgementView
    ModifyAcknowledgementView
    ModifyRecordConfirmationView
    ModifyRecordView
    PowerSearchFormView
    SessionTimeoutErrorView
    LogoffView
    OptionsView
);

my @ROW_COLOR_RULES = (
   {'therapeutic_action' => [qw(Business 99CC99)]},
   {'therapeutic_action' => [qw(Personal CC9999)]}
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
    -DISPLAY_FIELDS                 => [qw(
        therapeutic_action
        desease_code
        name
        display_name
        description
        comments
        medical_uses
        active
        visibility
        leaves
        fruit
        taste
        flowers
        root
        constituents
        odour
        distribution
        solvents
        contra_indications
        preparation
        administration
        dosage
        formulas
        vetrinary
        cultivation
        non_med
        history
        sister_plants
        harvest
        url
        )],
    -DOCUMENT_ROOT_URL       => '/',
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        taste
        comments
                 )],
    -FIELD_NAME_MAPPINGS     => {
        therapeutic_action	=> 'Therapeutic Action',
        non_med                	=> 'Non Medical Uses',
        history	                => 'History',
        cultivation          	=> 'Cultivation',
        harvest          	=> 'Harvest',
        sister_plants          	=> 'Sister Plants',
        preparation	        => 'Preparation',
        vetrinary	        => 'Vetrinary',
        record_id	        => 'Record ID',
        administration	        => 'Administration',
        formulas	        => 'Formulas',
        contra_indications      => 'Contra Indications',
        desease_code	        => 'Disease Code',
        name		        => 'Disease Name',
        display_name		=> 'Disease',
        description		=> 'Description',
        comments	        => 'Comments',
        medical_uses            => 'Etiology',
        active                  => 'Active',
        visibility              => 'Visibility',
        leaves                  => 'Leaves',
        fruit                   => 'Fruit',
        taste                   => 'Taste',
        flowers                 => 'Flowers',
        solvents                => 'Solvents',
        root                    => 'Root',
        constituents            => 'Constituents',
        odour                   => 'Odour',
        distribution            => 'Distribution',
        dosage                  => 'Dosage',
        url                     => 'URL'
        },
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        desease_code
        name
        display_name
        therapeutic_action
        description
        comments
        medical_uses
        active
        visibility
        leaves
        fruit
        taste
        flowers
        root
        constituents
        odour
        distribution
        solvents
        chinese
        contra_indications
        preparation
        dosage
        administration
        formulas
        vetrinary
        history
        non-med
        cultivation
        sister_plants
        harvest
    )],
    -HOME_VIEW               => $homeviewname,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
         display_name
         medical_uses
        )],
    -SORT_FIELDS             => [qw(
        desease_code
        name
        display_name
        therapeutic_action
        description
        comments
        medical_uses
        active
        visibility
        leaves
        fruit
        taste
        flowers
        root
        constituents
        odour
        distribution
        solvents
        chinese
        contra_indications
        preparation
        dosage
        administration
        formulas
        vetrinary
        history
        non-med
        cultivation
        sister_plants
        harvest
        url
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

my @ACTION_HANDLER_LIST = 
    qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction
       Default::ProcessConfigurationAction
       Default::CheckForLogicalConfigurationErrorsAction
       Default::DisplaySessionTimeoutErrorAction
       Default::PerformLogoffAction
       Default::PerformLogonAction
       Default::DisplayOptionsFormAction
       Default::DownloadFileAction
       Default::DisplayAddFormAction
       Default::DisplayAddRecordConfirmationAction
       Default::ProcessAddRequestAction
       Default::DisplayDeleteFormAction
       Default::DisplayDeleteRecordConfirmationAction
       Default::ProcessDeleteRequestAction
       Default::DisplayModifyFormAction
       Default::DisplayModifyRecordConfirmationAction
       Default::ProcessModifyRequestAction
       Default::DisplayPowerSearchFormAction
       Default::DisplayDetailsRecordViewAction
       Default::DisplayViewAllRecordsAction
       Default::DisplaySimpleSearchResultsAction
       Default::PerformPowerSearchAction
       Default::HandleSearchByUserAction
       Default::DisplayBasicDataViewAction
       Default::DefaultAction
      );

# add plugins here if any
my %ACTION_HANDLER_PLUGINS =
    (
    );


my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_DELETIONS_FLAG                   => 0,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => 'BasicDataView',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 5,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'desease_code',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'name',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
    -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -KEY_FIELD                              => 'record_id',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
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
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
    -SITE_NAME            => $SiteName,
    -PAGE_TOP_VIEW           =>  $CGI->param('page_top_view') ||  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $CGI->param('left_page_view') || $left_page_view,
    -PAGE_BOTTOM_VIEW        =>  $CGI->param('$page_bottom_view') || $page_bottom_view,
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
             $CGI->script_name() .  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();
  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();
