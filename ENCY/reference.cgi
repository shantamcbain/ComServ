#!/usr/bin/perl -wT
# 	$Id: formulas.cgi,v 1.1 2002/01/25 19:21:35 shanta Exp $	

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

my @VIEWS_SEARCH_PATH = 
    qw(Modules/Extropia/View/AddressBook
       Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/AltPower
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/AddressBook
       ../HTMLTemplates/Shanta
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

my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

######################################################################
#                             SITE SETUP                             #
######################################################################
my $SiteName =  $CGI->param('site') || "ENCY";

my $APP_NAME          = "reference";
my $APP_NAME_TITLE    = 'Refrence';
my $Affiliate = 001;
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $site_update;

#ViewNames
my $home_view         = 'BasicDataView'; 
my $page_top_view     = 'PageTopView';
my $page_bottom_view  = 'PageBottomView';
my $left_page_view    = 'LeftPageView';
#Mail settings
my $mail_from         = "$CGI->param('email')||'encyreference\@forager.com'";
my $mail_to           = 'encyreference\@forager.com';
my $mail_replyto      = 'encyadmin\@forager.com';
my $auth_mail_to;


#Style
my $CSS_VIEW_NAME     = "CSSView",
my $app_logo          = '../ency/encyicon.gif';
my $app_logo_height   = '86';
my $app_logo_width    = '108';
my $logo_alt          = "ENCY Logo";
my $image_root_url    = '/images/extropia'; 
my $ColorForEvenRows  = '#009933';
my $ColorForOddRows   = '#A5B3A1';
my $TABLE_BG_COLOR_1  = '6699CC';
my $TABLE_BG_COLOR_2  = 'E5E5E5';
my $TABLE_BG_FONT_COLOR_1   = 'BLACK';
my $TABLE_BG_FONT_COLOR_2   = 'BLACK';
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_DESCRIPTION;
my $HeaderImage;
my $Header_height;
my $Header_width;
my $Header_alt;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;


my $SiteLastUpdate;
my $shop = 'cs';

my $HasMembers = 0;

my $matchuser = 0;
my $matchgroup = 0;
my $last_update = 'January 12, 2020';
    my $LINK_TARGET;
    my $DEFAULT_CHARSET;
 my $LineStatus        = "yes";
my $Page_tb;
my $StoreUrl  = 'countrystores.ca';


use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
     $home_view             = $SetupVariables->{-HOME_VIEW}; 
  my $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
  my $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
     $page_top_view         = 'templatePageTopView';
     $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
  my $page_left_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
  my $MySQLPW               = $SetupVariables->{-MySQLPW};
  my $DBI_DSN               = $SetupVariables->{-DBI_DSN};
  my $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
  my $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
#Mail settings
     $mail_from             = $SetupVariables->{-MAIL_FROM}; 
     $mail_to               = $SetupVariables->{-MAIL_TO};
     $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
     $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
     $app_logo              = $SetupVariables->{-APP_LOGO};
     $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
     $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
  my $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
  my $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
  my $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
   my $site                  = $SetupVariables->{-DATASOURCE_TYPE};
  my $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
  my $LocalIp            = $SetupVariables->{-LOCAL_IP};
  my $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
  my $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};


 # my $GLOBAL_DATAFILES_DIRECTORY = "/home/shanta/Datafiles";       
  #my $site = 'file';
  my $site = 'MySQL';
  
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
my $SetupVariables = new SiteSetup($UseModPerl, $CGI->param('site'));
$SiteName            = $SiteName || $SetupVariables->{-SITE_NAME};
$Affiliate           = $SetupVariables->{-AFFILIATE};
$APP_NAME_TITLE      = $SetupVariables->{-APP_NAME_TITLE};
$home_view           = $SetupVariables->{-HOME_VIEW};
$BASIC_DATA_VIEW     = $SetupVariables->{-BASIC_DATA_VIEW};
$DBI_DSN             = $SetupVariables->{-DBI_DSN};
$AUTH_TABLE          = $SetupVariables->{-AUTH_TABLE};
$AUTH_MSQL_USER_NAME = $SetupVariables->{-AUTH_MSQL_USER_NAME};
$LineStatus          = $SetupVariables->{-Line_Status} || $LineStatus;
$page_top_view       = $SetupVariables->{-PAGE_TOP_VIEW};
$page_bottom_view    = $SetupVariables->{-PAGE_BOTTOM_VIEW};
$page_left_view      = $SetupVariables->{-page_left_view};
$MySQLPW             = $SetupVariables->{-MySQLPW};
$Page_tb             = $SetupVariables->{-PAGE_TB} || 'page_tb';

#Mail settings
$mail_from               = $SetupVariables->{-MAIL_FROM};
$mail_to                 = $SetupVariables->{-MAIL_TO};
$auth_mail_to            = $SetupVariables->{-MAIL_TO_AUTH};
$mail_replyto            = $SetupVariables->{-MAIL_REPLYTO};
$app_logo                = $SetupVariables->{-APP_LOGO};
$app_logo_height         = $SetupVariables->{-APP_LOGO_HEIGHT};
$app_logo_width          = $SetupVariables->{-APP_LOGO_WIDTH};
$app_logo_alt            = $SetupVariables->{-APP_LOGO_ALT};
$HeaderImage             = $SetupVariables->{-HEADER_IMAGE};
$Header_height           = $SetupVariables->{-HEADER_HEIGHT};
$Header_width            = $SetupVariables->{-HEADER_WIDTH};
$Header_alt              = $SetupVariables->{-HEADER_ALT};
$IMAGE_ROOT_URL          = $SetupVariables->{-IMAGE_ROOT_URL};
$DOCUMENT_ROOT_URL       = $SetupVariables->{-DOCUMENT_ROOT_URL};
$LINK_TARGET             = $SetupVariables->{-LINK_TARGET};
$HTTP_HEADER_PARAMS      = $SetupVariables->{-HTTP_HEADER_PARAMS};
$HTTP_HEADER_KEYWORDS    = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
$HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
$FAVICON                 = $SetupVariables->{-FAVICON};
$ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
$FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
$site                    = $SetupVariables->{-DATASOURCE_TYPE};
$SITE_DISPLAY_NAME       = $SetupVariables->{-SITE_DISPLAY_NAME};

$GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY};
$TEMPLATES_CACHE_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY . $SetupVariables->{ -TEMPLATES_CACHE_DIRECTORY, };
$APP_DATAFILES_DIRECTORY = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
my $LocalIp = $SetupVariables->{-LOCAL_IP};
$shop          = $SetupVariables->{-SHOP};
$StoreUrl      = $SetupVariables->{-STORE_URL};
$site_update   = $SetupVariables->{-SITE_LAST_UPDATE};
$last_update   = $SetupVariables->{-LAST_UPDATE};
$HasMembers    = $SetupVariables->{-HAS_MEMBERS};
$CSS_VIEW_NAME = $SetupVariables->{-CSS_VIEW_NAME};
$CSS_VIEW_URL  = $SetupVariables->{-CSS_VIEW_NAME};

my $DATAFILES_DIRECTORY = "$GLOBAL_DATAFILES_DIRECTORY/Datafiles";  
my $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
my $site_session = $DATAFILES_DIRECTORY.'/Sessions';
my $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
my $datafile = $DATAFILES_DIRECTORY.'/csc_todo_tracker.dat';


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
        -DBI_DSN      => $DBI_DSN,
        -TABLE        => $AUTH_TABLE,
        -USERNAME     => $AUTH_MSQL_USER_NAME,
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
    -SITE_NAME               => $SiteName,
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $APP_NAME_TITLE,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -LINK_TARGET             => $LINK_TARGET,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -LEFT_PAGE_VIEW          => $page_left_view,
    -LINK_TARGET             => $LINK_TARGET,
    -DEFAULT_CHARSET         =>  $DEFAULT_CHARSET,
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
    -FROM    => '$mail_from',
    -SUBJECT => 'Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    =>  '$mail_from',
    -TO      =>  '$mail_to',
    -SUBJECT => 'Registration Notification'
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
        'reference_code'    => 'Reference Code',
        'title'             => 'Title',
        'share'             => 'Share',
        'pages'             => 'Page numbers',
        'date_of_publication'    => 'Date of Pubication',
        'location'    => 'Location of Book',
        'comments' => 'Comments'
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

        -IS_EMAIL => [
            -FIELDS => [qw(
                email
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
        ],

        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
            -FIELDS => [qw(
                
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                title
                share
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
        'fname'    => 'Botanica Names',
        'title'    => 'Title',
        'share'    => 'Sharing',
        'pages'             => 'Page numbers',
        'therapeutic_action' => 'Therapeutic_Action',
        'date_of_publication'    => 'Date_Of_Publication',
        'comments' => 'Comments'
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
                
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                title
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
        reference_code
        title
        share
        pages
        date_of_publication
        location
        isbn
	     url
        comments
        username_of_poster
        group_of_poster
        date_time_posted
);


my %BASIC_INPUT_WIDGET_DEFINITIONS = (
   
reference_code => [
        -DISPLAY_NAME => 'Reference code, used by Herbs etc to trak references',
        -TYPE         => 'textfield',
        -NAME         => 'reference_code',
        -SIZE         => 30,
        -MAXLENGTH    => 500
    ],

    pages => [
        -DISPLAY_NAME => 'Page Numbers',
        -TYPE         => 'textfield',
        -NAME         => 'pages',
        -SIZE         => 30,
        -MAXLENGTH    => 500
    ],

    title => [
        -DISPLAY_NAME => 'Title of reference',
        -TYPE         => 'textarea',
        -NAME         => 'title',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

    isbn => [
        -DISPLAY_NAME => 'Book refrence number. use isbn',
        -TYPE         => 'textfield',
       -NAME         => 'isbm',
        -SIZE         => 30,
        -MAXLENGTH    => 15
    ],

    date_of_publication => [
        -DISPLAY_NAME => 'Date of publication',
        -TYPE         => 'textfield',
        -NAME         => 'date_of_publication',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    location => [
        -DISPLAY_NAME => 'location',
        -TYPE         => 'textfield',
        -NAME         => 'location',
        -SIZE         => 30,
        -MAXLENGTH    => 250
    ],

    url => [
        -DISPLAY_NAME => 'Url',
        -TYPE         => 'textfield',
        -NAME         => 'url',
       -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
 
     share => [
        -DISPLAY_NAME => 'Share Level',
        -TYPE         => 'popup_menu',
        -NAME         => 'share',
        -VALUES       => [qw(
            public
            priv
        )], 
        -LABELS       => { 
            'public'  => 'Seen by all users',
            'priv'    => 'Private only I  can see.',
             },
    ],

   
    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ]
);
        

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
        reference_code
        title
        isbn
        url
        share
        pages
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
    -KEY_FIELDS                 => ['formulat_code'],
    -FIELD_TYPES                => {
    },
);
}
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'ency_reference_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
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


my @BOOK_BOOKDATASOURCE_FIELD_NAMES = qw(
        record_id
        reference_code
        title
        author_code
        publisher_code
        date_of_publication
        location
        isbn
	     url
        comments
        username_of_poster
        group_of_poster
        date_time_posted
);
	
my @BOOK_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'books_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@BOOK_BOOKDATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -BOOK_DATASOURCE_CONFIG_PARAMS      => \@BOOK_DATASOURCE_CONFIG_PARAMS,
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
        fname
        title
        date_of_publication
        share
        comments
);
my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => '$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => '$APP_NAME_TITLE Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => '$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => '$APP_NAME_TITLE Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => '$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => '$APP_NAME_TITLE Modification'
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
    -LOG_ENTRY_PREFIX => '$APP_NAME_TITLE|'
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
    -APPLICATION_LOGO_ALT           => $logo_alt,
    -COLOR_FOR_EVEN_ROWS            => $ColorForEvenRows,
    -COLOR_FOR_ODD_ROWS             => $ColorForOddRows,
    -DISPLAY_FIELDS                 => [qw(
        therapeutic_action
        formula_name
        title
        date_of_publication
        share
        comments
        medical_uses
        ident_character
        stem
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
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        title
       )],
    -FIELD_NAME_MAPPINGS     => {
        title           	  => 'Title of publication',
        date_of_publication  => 'Date of Publiction',
        share		           => 'Share',
        comments	           => 'Comments',
        url                  => 'URL'
        },
    -HOME_VIEW               => 'BasicDataView',
    -IMAGE_ROOT_URL          => $image_root_url,
    -LINK_TARGET             => '_self',
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
         title
         share      )],
    -SORT_FIELDS             => [qw(
        formula_name
        title
        date_of_publication
        therapeutic_action
        share
        comments
        medical_uses
        ident_character
        stem
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
    -TABLE_BG_COLOR_1        => $TABLE_BG_COLOR_1,
    -TABLE_BG_COLOR_2        => $TABLE_BG_COLOR_2,
    -TABLE_BG_FONT_COLOR_1   => $TABLE_BG_FONT_COLOR_1,
    -TABLE_BG_FONT_COLOR_2   => $TABLE_BG_FONT_COLOR_2
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
#       ENCY::PopulateInputWidgetDefinitionListWithBookWidgetAction

######################################################################
#                      ACTION/WORKFLOW SETUP                         #
######################################################################
#ENCY::PopulateInputWidgetDefinitionListWithBookISBMWidgetAction
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
    -ALLOW_DELETIONS_FLAG                   => 1,
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
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'title',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || '',
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
    -SEND_EMAIL_ON_MODIFY_FLAG              => 0,
    -SEND_EMAIL_ON_ADD_FLAG                 => 0,
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
    -PAGE_TOP_VIEW                          => $page_top_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -LEFT_PAGE_VIEW                         => $left_page_view,
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
