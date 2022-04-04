#!/usr/bin/perl -wT
	
# 	$Id: /cgi-bin/apis/palltet.cgi,v 01 2020/03/10 21:26:43 shanta Exp shanta $	
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
my $AppVer = "v .03 April 5, 2022";
use strict;
BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/CSC
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");


foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x/);
}
######################################################################
#                          PORTING SETUP                             #
######################################################################
my $SiteName =  $CGI->param('site') || "Apis";
my $Affiliate = 001;
my $additonalautusernamecomments;

my $allow_mod ='1';
my $allow_del = '1';
my $auth_search = '0';
my $APP_DATAFILES_DIRECTORY;
my $app_logo;
my $app_logo_height;
my $app_logo_width;
my $app_logo_alt;
my $APP_NAME = "pallet";
my $APP_NAME_TITLE = $SiteName." Pallet  Manager";
my $auth;
my $BASIC_DATA_VIEW; 
my $DBI_DSN;
my $AUTH_MSQL_USER_NAME;
my $AUTH_TABLE;
my $CAL_TABLE;
my $CustCode = $CGI->param('custcode') || "BMaster";
my $CSS_VIEW_NAME = '/styles/CSCCSSView';
my $CSS_VIEW_URL = $CSS_VIEW_NAME;
my $DEFAULT_CHARSET;
my $DOCUMENT_ROOT_URL;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $GLOBAL_DATAFILES_DIRECTORY;
my $HeaderImage;
my $Header_height;
my $Header_width;
my $Header_alt;
my $HasMembers = 0;
my $homeviewname ;
my $home_view; 
my $HostName   = $ENV{'SERVER_NAME'};
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_DESCRIPTION;
my $IMAGE_ROOT_URL; 
my $last_update       =  $AppVer|| 'April 04, 2022';
my $LINK_TARGET;
my $left_page_view;
#Mail settings
my $mail_from; 
my $mail_to;
my $mail_replyto;
my $mail_to_user;
my $mail_to_member;
my $mail_to_discussion;
my $match_group_search = 0;
my $match_use_mod = 0;
my $match_user_search = 1;
my $MySQLPW;
my $NEWS_TB;
my $Page           = $CGI->param('page');
my $Page_tb;
my $page_top_view;
my $page_bottom_view;
my $page_left_view;
my $pid        = '15';
my $procedure      = $CGI->param('procedure');
my $project        = $CGI->param('project');
my $require  = '0';
my $reqire_user = '0';
my $require_group = '0';
my $SetupVariables  ;
my $shop = 'cs';
my $site;
my $site_session;
my $style = $CGI->param('pagestyle');
my $title          = $CGI->param('title');
my $View           = $CGI->param('view') ;
my $TEMPLATES_CACHE_DIRECTORY;
my    $DATAFILES_DIRECTORY;
my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");
   
use SiteSetup;
  my $UseModPerl = 1;
   $SetupVariables  = new SiteSetup($UseModPerl);
    $Affiliate           = $SetupVariables->{-AFFILIATE};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $app_logo              = $SetupVariables->{-APP_LOGO};
    $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
    $auth                  = $APP_DATAFILES_DIRECTORY.'/csc.admin.users.dat';
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $BASIC_DATA_VIEW       = 'PalletView'||$SetupVariables->{-BASIC_DATA_VIEW};
    $CAL_TABLE             = $SetupVariables->{-CAL_TABLE};
    $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
    $CSS_VIEW_URL  = $SetupVariables->{-CSS_VIEW_NAME};
    $DATAFILES_DIRECTORY = $APP_DATAFILES_DIRECTORY;
    $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
$FAVICON                 = $SetupVariables->{-FAVICON};
$ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
$FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
$HeaderImage             = $SetupVariables->{-HEADER_IMAGE};
$Header_height           = $SetupVariables->{-HEADER_HEIGHT};
$Header_width            = $SetupVariables->{-HEADER_WIDTH};
$Header_alt              = $SetupVariables->{-HEADER_ALT};
$home_view             = $SetupVariables->{-HOME_VIEW}; 
$homeviewname          = 'PalletView'||$SetupVariables->{-HOME_VIEW_NAME};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $left_page_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
my $LocalIp              = $SetupVariables->{-LOCAL_IP};
#Mail settings
    $mail_from             = $SetupVariables->{-MAIL_FROM}; 
    $mail_to               = $SetupVariables->{-MAIL_TO};
    $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
#MySQL settings
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
$Page_tb             = $SetupVariables->{-PAGE_TB} || 'page_tb';
$pid                     = $SetupVariables->{-PID};
    $site = $SetupVariables->{-DATASOURCE_TYPE};
my $SITE_DISPLAY_NAME       = $SetupVariables->{-SITE_DISPLAY_NAME};
    $site_session = $DATAFILES_DIRECTORY.'/Sessions';
my $site_update   = $SetupVariables->{-SITE_LAST_UPDATE};
$shop          = $SetupVariables->{-SHOP};
my $StoreUrl      = $SetupVariables->{-STORE_URL};
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};



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
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_groups');
my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');

 
if ($username = 'Shanta'){
    $match_use_mod = 1;
    $match_user_search = 0;
   $allow_mod ='1';
   $allow_del = '1';
   $auth_search = '0';
   $require  = '0';
   $reqire_user = '0';
   $require_group = '0';
}

if ($CGI->param('embed')){
   $page_top_view = "EmbedPageTopView";
   $page_bottom_view = "";
   $allow_mod ='0';
   $allow_del = '0';
   $auth_search = '0';
   $require  = '0';
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
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => 'pallet.cgi'||$CGI->script_name(),
    -PAGE_TOP_VIEW           => $CGI->param('page_top_view')||$page_top_view,
    -PAGE_BOTTOM_VIEW        => $CGI->param('page_bottom_view')||$page_bottom_view,
    -LEFT_PAGE_VIEW          => $CGI->param('left_page_view')||$left_page_view,
    -LINK_TARGET             => $LINK_TARGET
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
    
my @USER_FIELDS = qw(
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
my @ADMIN_EMAIL_DISPLAY_FIELDS = qw(
  username
  password
  groups
  firstname
  lastname
  email
);
my @MAIL_PARAMS = (
    -TYPE         => 'Sendmail',
);

my @USER_MAIL_SEND_PARAMS = (
    -FROM    => $mail_from,
    -TO      => $mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $mail_from,
    -TO      => $mail_to,
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
    -ALLOW_REGISTRATION          => 0,   
    -ALLOW_USER_SEARCH           => 0,
    -USER_SEARCH_FIELD           => 'auth_email',
    -GENERATE_PASSWORD           => 0,
    -DEFAULT_GROUPS              => 'normal',
    -EMAIL_REGISTRATION_TO_ADMIN => 0,
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
        'status'              => 'Status',
        'yard_name'           => 'Yard Name',
        'pallet_code'         => 'Pallet code',
        'pallet_name'         => 'Pallet name',
        'hivetype'            => 'Hive Type',
        'developer_name'      => 'Developer Name',
        'client_name'         => 'Client Name',
        'comments'            => 'Comments'
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
            )],
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
                status
                
                pallet_code
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
        'status'              => 'Status',
        'yard_name'           => 'Yard Name',
        'yard_size'           => 'Yard Size',
        'total_yard_size'     => 'Max Yard Size',
        'hivetype'            => 'Hive Type',
        'developer_name'      => 'Developer Name',
        'client_name'         => 'Client Name',
        'comments'            => 'Comments'
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
            )],
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
                status
                yard_code
                pallet_code
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
        sitename
        status
        pallet_code
        yard_code
        hivetype
        pallet_name
        pallet_size
        queen_code
        client_name
        comments        
        username_of_poster
        group_of_poster
        date_time_posted
);
 my    %type_code = (
        BNuc      => 'Bob nuc',
        KNuc      => 'Knuc',
        GNnuc     => 'Gates double bottom',
        TNuc      => 'top nuc 5framer',
        EightF    => '8 Framer',
        Single    => "Single hive",
        PSingle   => 'Pots single',
        Main      => 'Main hive',
        PMain     => 'Pots Main',
        TBox      => 'Top Box',
        BTop      => 'B top box split',
        B4Top     => 'B top 4 hives',
        Cross     => 'Cross ways',
        );
        
        
my %site_code = (
       $SiteName => $SiteName,
       );
my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    status => [
        -DISPLAY_NAME => 'Status',
        -TYPE         => 'popup_menu',
        -NAME         => 'status',
        -VALUES       => [qw(Requested In-Use Inactive defunc)]
    ],

    pallet_name => [
        -DISPLAY_NAME => 'Pallet Name',
        -TYPE         => 'textfield',
        -NAME         => 'pallet_name',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    pallet_code => [
        -DISPLAY_NAME => 'Pallet Code',
        -TYPE         => 'textfield',
        -NAME         => 'pallet_code',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
      hivetype => [
        -DISPLAY_NAME => 'Hive Type',
        -TYPE         => 'popup_menu',
        -NAME         => 'hivetype',
                 -VALUES       => [sort {$a <=> $b}keys %type_code],
                 -LABELS       => \%type_code,
                 -INPUT_CELL_COLSPAN => 3, 
    ],

#    yard_code => [
#        -DISPLAY_NAME => 'Yard Code',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'yard_code',
#     ],

       sitename => [
        -DISPLAY_NAME => 'Site Name *',
        -TYPE         => 'popup_menu',
        -NAME         => 'sitename',
                 -VALUES       => [sort {$a <=> $b} keys %site_code],
                 -LABELS       => \%site_code,
                 -INPUT_CELL_COLSPAN => 3, 
    ],
  pallet_size => [
        -DISPLAY_NAME => 'Total Number of Hives',
        -TYPE         => 'textfield',
        -NAME         => 'pallet_size',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    developer_name => [
        -DISPLAY_NAME => 'Developer',
        -TYPE         => 'textfield',
        -NAME         => 'developer_name',
        -VALUE        => 'Shanta', 
        -SIZE         => 30,
        -MAXLENGTH    => 
    ],

#    client_name => [
#        -DISPLAY_NAME => 'Client',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'client_name',
#        -VALUES       => [qw(CSC BCAF MiteGone )]
#    ],

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
        status
        sitename
        yard_code
        pallet_code
        pallet_name
        hivetype
        queen_code
        pallet_size
        comments 
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (    -TYPE                       => 'File', 
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
    -FIELD_DELIMITER            => '|',
    -COMMENT_PREFIX             => '#',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['record_id'],
    -FIELD_TYPES                => {
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
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_pallet_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['yard_code'],
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

my @CLIENT_DATASOURCE_FIELD_NAMES = qw(
        category
        sitename
        record_id
        fname
        lname
        phone
        email
        comments
        address1
        address2
        city
        prov
        zip
        country
        fax
        mobile
        url
        company_code
        company_name
        title
        department
        username_of_poster
        group_of_poster
        date_time_posted
);

my	@CLIENT_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'csc_client_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@CLIENT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);
my @YARD_DATASOURCE_FIELD_NAMES = qw(
       yard_code
       yard_name
       sitename
       status
       username_of_poster
       group_of_poster
);

my	@YARD_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_yards_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@YARD_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

my @PALLET_DATASOURCE_FIELD_NAMES = qw(
       pallet_code
       hivetype
       sitename
       status
       username_of_poster
       group_of_poster
 );
my	@PALLET_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_pallet_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@PALLET_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);
my @QUEENS_DATASOURCE_FIELD_NAMES = qw(
        status
        sitename
        queen_code
        queen_name
        pallet_code
        box_number
        parent
        queen_colour
        date
        client_name
        comments
        username_of_poster
        group_of_poster
);
my @QUEENS_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_queens_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@QUEENS_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['queen_code'],
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

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -CLIENT_DATASOURCE_CONFIG_PARAMS    => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
    -PALLET_DATASOURCE_CONFIG_PARAMS    => \@PALLET_DATASOURCE_CONFIG_PARAMS,
    -QUEENS_DATASOURCE_CONFIG_PARAMS    => \@QUEENS_DATASOURCE_CONFIG_PARAMS,
    -YARD_DATASOURCE_CONFIG_PARAMS      => \@YARD_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################v 01 
           
my @MAIL_CONFIG_PARAMS = (     
    -TYPE         => 'Sendmail'
);

my @EMAIL_DISPLAY_FIELDS = qw(
        status
        yard_code
        yard_name
        queen_code
        yard_size
        total_yard_size
        developer_name
        client_name
        comments        
);

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE.' Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE.' Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE.' Modification'
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
       CSPSCSSView
       CSCCSSView
       CAPCSSView
       VitalVicCSSView
       ApisCSSView
       ENCYCSSView
       BCAFCSSView
       AddAcknowledgementView
       AddRecordConfirmationView
       DeleteRecordConfirmationView
       DeleteAcknowledgementView
       ModifyAcknowledgementView
       ModifyRecordConfirmationView
       SessionTimeoutErrorView
       AddRecordView
       PalletView
       PowerSearchFormView
       BasicDataView
       DetailsRecordView
       ModifyRecordView
       LogoffView
       OptionsView
       InventoryProjectionView
       YardsView
       FeedingView
       InventoryView      
);	


my @ROW_COLOR_RULES = (
   {'status' => [qw(Requested 99CC99)]},
   {'status' => [qw(In-Process CC9999)]},
   {'status' => [qw(Delivered CC9999)]}
);

my @FIELD_COLOR_RULES = (
   {'yard_size' => [qw(Large BLUE)]},
   {'yard_size' => [qw(Small ORANGE)]}
);


my @VIEW_DISPLAY_PARAMS = (
 -ADMIN_EMAIL_DISPLAY_FIELDS            => \@ADMIN_EMAIL_DISPLAY_FIELDS,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -FIELD_COLOR_RULES       => \@FIELD_COLOR_RULES,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
 -CUST_CODE               => $CustCode,
   -DISPLAY_FIELDS        => [qw(
        pallet_code
        pallet_name
        hivetype
        yard_code
        status
        )],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
 -FAVICON                 => $FAVICON || '/images/apis/favicon.ico',
 -ANI_FAVICON             => $ANI_FAVICON,
 -FAVICON_TYPE            => $FAVICON_TYPE,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        body
    )],
    -FIELD_NAME_MAPPINGS   => {
        status             => 'Status',
        pallet_code        => 'Pallet Code',
        yard_code          => 'Yard Code',
        pallet_name        => 'Pallet Name',
        hivetype           => 'Hive Type',
        queen_code         => 'Queen_code',
        yard_size          => 'Yard Size',
        total_yard_size    => 'Total Number of Hive',
        developer_name     => 'Developer',
        client_name        => 'Client',
        comments           => 'Comments'
        },
 -HEADER_IMAGE            => $HeaderImage || 'none',
 -HEADER_HEIGHT           => $Header_height,
 -HEADER_WIDTH            => $Header_width,
 -HEADER_ALT              => $Header_alt,
   -HOME_VIEW               => $homeviewname,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => 'pallet.cgi'||$CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS        => [qw(
        yard_code
        pallet_code
        queen_code
        hivetype
        pallet_name
        status
        )],        
  -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
   -SORT_FIELDS        => [qw(
        pallet_code
        yard_code
        status
        hivetype
        total_yard_size
        comments        
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
#Apis::PopulateInputWidgetDefinitionListWithCurrentQueenCodeWidgetAction

my @ACTION_HANDLER_LIST = 
    qw(
       CSC::PopulateInputWidgetDefinitionListWithClientWidgetAction
       Apis::PopulateInputWidgetDefinitionListWithQueenCodeWidgetAction
       Apis::PopulateInputWidgetDefinitionListWithYardCodeWidgetAction
       Default::SetSessionData
       Default::DisplayCSSViewAction
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
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -AFFILIATE_NUMBER                     => $Affiliate,
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -APP_VER                              => $AppVer,
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -BASIC_DATA_VIEW_NAME                   => $BASIC_DATA_VIEW,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 2,
    -CGI_OBJECT                             =>  $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
 -Debug                               => $CGI->param('debug') || 0,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 0,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 0,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 0,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 0,
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DEFAULT_SORT_FIELD1                    => 'status',
    -DEFAULT_SORT_FIELD2                    => 'yard_name',
  -DOMAIN_NAME                            => $HostName,
    -ENABLE_SORTING_FLAG                    => 1,
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
 -GROUP                                  => $group,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -KEY_FIELD                              => 'record_id',
     -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
 -LAST_UPDATE                            => $last_update,
 -LOCAL_IP                               => $LocalIp,
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 100,
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
 -MOBILE                              => $CGI->param('m') || 0,  -PID                                  => $pid,
 -NEWS_TB                                => $NEWS_TB,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',    
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -PAGE_TOP_VIEW           =>  $CGI->param('page_top_view') ||  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $CGI->param('left_page_view') || $left_page_view,
    -PAGE_BOTTOM_VIEW        =>  $CGI->param('$page_bottom_view') || $page_bottom_view,
 -PAGE_NAME                              => $Page,
 -PROCEDURE                  => $procedure,
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $match_use_mod,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => $match_user_search,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        =>
$match_group_search,
    -SEND_EMAIL_ON_DELETE_FLAG             => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG             => 0,
    -SEND_EMAIL_ON_ADD_FLAG                => 0,
    -SESSION_OBJECT                        => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME             => 'SessionTimeoutErrorView',
-SHOP                       => $shop,
     -SIMPLE_SEARCH_BOX_VIEW_NAME            => 'SimpleSearchBoxView',
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -SITE_NAME                              => $SiteName,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'yard_code',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'pallet_code',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
 -STORE_URL                              => $StoreUrl,
 -STYLE                                            => $style,
     -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
  -TITLE                      => $title,
 -VIEW                       => $View,
 -VIEW_FILTERS_CONFIG_PARAMS            => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS                   => \@VIEW_DISPLAY_PARAMS,
    -VALID_VIEWS                           => \@VALID_VIEWS,
    -VIEW_LOADER                           => $VIEW_LOADER,
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
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

