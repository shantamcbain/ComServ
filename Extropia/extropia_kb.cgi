#!/usr/bin/perl -wT
# 	$Id: extropia_kb.cgi,v 1.2 2002/02/02 18:23:21 shanta Exp shanta $	
#CSC file location /cgi-bin/CSC
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
    @dirs = qw(../Modules/
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Extropia
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
        ../HTMLTemplates/ENCY
      ../HTMLTemplates/Todo
        ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/BugTracker
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
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x$/);
}
######################################################################
#                          SITE SETUP                             #
######################################################################

my $APP_NAME = "extropia_methouds"; 
my $SiteName =  $CGI->param('site') || "eXtropia";
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';

my $APP_NAME_TITLE = "CSC Extropia Knowlage Base";
my $applogo = '../csc/cscsmall.gif';
my $applogoalt = 'CSC Logo';
my $imagerooturl ='http://forager.com/images/extropia';
my $HomePageViewName ='BasicDataView';
my $leftpageviewname ='ExtropiaHelpDeskLeftPageView';
my $css_view_name = "CSSView";
    my $ColorForEvenRows      = 'FFFFFF';
    my $ColorForOddRows       = 'E5E5E5';
    my $homeviewname          = 'CSCHome';
    my $home_view             = 'BasicDataView'; 
    my $BASIC_DATA_VIEW       = $home_view; 
    my $page_top_view         ;
    my $page_bottom_view      = 'PageBottomView';
    my $page_left_view        = 'LeftPageView';
#Mail settings
    my $mail_from             = 'csc@computersystemconsulting.ca'; 
    my $mail_to               = 'csc_user_list@computersystemconsulting.ca';
    my $mail_replyto          = 'csc@computersystemconsulting.ca';
    my $CSS_VIEW_NAME         = "CSSView";
    my $app_logo              = '../csc/cscsmall.gif';
    my $app_logo_height       = '63';
    my $app_logo_width        = '225';
    my $logo_alt              = 'CSC Logo';
    my $IMAGE_ROOT_URL        = 'http://forager.com/images/extropia'; 
    my $DOCUMENT_ROOT_URL     = '/';
    my $TABLE_BG_COLOR_1      = '66909CC';
    my $TABLE_BG_COLOR_2      = 'E5E5E5';
    my $TABLE_BG_FONT_COLOR_1 = 'BLACK';
    my $TABLE_BG_FONT_COLOR_2 = 'BLACK';
    my $MySQLPW;
    my $last_update = 'January 26, 2006';

my $GLOBAL_DATAFILES_DIRECTORY = "../../Datafiles";
my $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
my $APP_DATAFILES_DIRECTORY    = "../../Datafiles/Todo";
#my $site = 'file';
my $site = 'MySQL';
my $DATAFILES_DIRECTORY = "../../Datafiles";
my $site_session = $DATAFILES_DIRECTORY.'/Sessions';
my $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
my $datafile = $DATAFILES_DIRECTORY.'/csc_todo_tracker.dat';
my $DBI_DSN;
my $AUTH_TABLE;
my $AUTH_MSQL_USER_NAME;
my $app_logo_alt;
my $LINK_TARGET;
my $DEFAULT_CHARSET;	
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_DESCRIPTION;
    my $HasMembers = 0;

use SiteSetup;
my $UseModPerl = 1;
 my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
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
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $DATAFILES_DIRECTORY = $APP_DATAFILES_DIRECTORY;
    $site_session = $DATAFILES_DIRECTORY.'/Sessions';
    $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
    $page_top_view    = $CGI->param('page_top_view')||$page_top_view;
    $page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
    $page_left_view   = $CGI->param('left_page_view')||$page_left_view;
    my $HomePageViewName = $BASIC_DATA_VIEW;

my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60,
    -SESSION_DIR     => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
    -FATAL_TIMEOUT   => 0,
    -FATAL_SESSION_NOT_FOUND => 1
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

if ($SiteName eq "CSC"||
       $SiteName eq "CSCDev" ){
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC  = new CSCSetup($UseModPerl);
  my $SetupVariablesCSC       = new  CSCSetup($UseModPerl);
if ($SiteName eq "CSCDev"
       ) { $AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
    $SITE_DISPLAY_NAME        = "Dev.".$SetupVariablesCSC->{-SITE_DISPLAY_NAME};
       } else {
         $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
     $SITE_DISPLAY_NAME       = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
  }
    $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $homeviewname            = 'HelpDeskHomeView';
    $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $page_top_view           = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};

}
elsif ($SiteName eq "eXtropia") {
use eXtropiaSetup;
  my $UseModPerl = 0;
  my $SetupVariableseXtropia   = new eXtropiaSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariableseXtropia->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariableseXtropia->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariableseXtropia->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariableseXtropia->{-HTTP_HEADER_DESCRIPTION};
     $AUTH_TABLE              = $SetupVariableseXtropia->{-AUTH_TABLE};
     $app_logo                = $SetupVariableseXtropia->{-APP_LOGO};
     $app_logo_height         = $SetupVariableseXtropia->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariableseXtropia->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariableseXtropia->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariableseXtropia->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariableseXtropia->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariableseXtropia->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariableseXtropia->{-SITE_DISPLAY_NAME};
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
    -COLOR_FOR_EVEN_ROWS     => 'E5E5E5',
    -COLOR_FOR_ODD_ROWS      => 'FFFFFF',
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $applogo,
    -APPLICATION_LOGO_HEIGHT => '50',
    -APPLICATION_LOGO_WIDTH  => '353',
    -APPLICATION_LOGO_ALT    => $applogoalt,
    -HTTP_HEADER_PARAMS      => [-EXPIRES => '-1d'],
    -DOCUMENT_ROOT_URL       => '/',
    -IMAGE_ROOT_URL          => $imagerooturl,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -LEFT_PAGE_VIEW          => $page_left_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
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
    -FROM     => $CGI->param('email')||'computersystemconsulting.ca',
    -SUBJECT => '$APP_NAME_TITLE Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM     => $CGI->param('email')||'todologin@computersystemconsulting.ca',
    -TO      => 'shanta@computersystemconsulting.ca',
    -SUBJECT => '$APP_NAME_TITLE Registration Notification'
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

    -FIELD_MAPPINGS =>
      {
        'status'              => 'Status',
        'kb_type'	      => 'Knowledge Base Type',
        'questions'            => 'Questions',
        'summary'     => 'Summery',
        'user_type'             => 'User Type',
        'solution'             => 'Solution',
        'workaround'             => 'Workaround',
        'browser'	      => 'Browser',
        'category_1'	      => 'category_1',
        'submitted_by'        => 'Submitted by',
        'user_name_of_poster'        => 'First Posted by',
        'category_2'          => 'Category 2',
        'priority'	      => 'Priority',
        'comments'            => 'Comments'
      },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
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
            -FIELDS => [
                        qw(
                          )
                       ]
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
        'kb_type'	      => 'Knowledge Base Type',
        'questions'           => 'Questions',
        'summary'             => 'Summery',
        'user_type'           => 'User Type',
        'solution'            => 'Solution',
        'workaround'          => 'Workaround',
        'browser'	      => 'Browser',
        'category_1'	      => 'category_1',
        'submitted_by'        => 'Submitted by',
        'user_name_of_poster' => 'First Posted by',
        'category_2'          => 'Category 2',
        'priority'	      => 'Priority',
         comments                 => 'Comments',
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
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
                *
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                          )
                       ]
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

my @DATASOURCE_FIELD_NAMES = 
    qw(
      record_id
        status
        company_code
        kb_type
        questions
        summary
        solution
        workaround
        user_type
        category_1
        category_2
        audience
        submitted_by
        internal_notes
        comments        
        count
        username_of_poster
        group_of_poster
        date_time_posted
);
# prepare the data then used in the form input definition
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (2001..2005);
my %days  = ();
$days{$_} = $_ for (1..31);

my %priority =
    (
      1 => 'LOW',
      2 => 'MIDDLE',
      3 => 'HIGH',
    );

my %status =
    (
      1 => 'NEW',
      2 => 'IN PROGRESS',
      3 => 'DONE',
    );



my %BASIC_INPUT_WIDGET_DEFINITIONS =     (

    status => [
        -DISPLAY_NAME => 'Status',
        -TYPE         => 'popup_menu',
        -NAME         => 'status',
        -VALUES       => [
                 'draft',
                 'Verified', 
                 ''
                 ]
    ],

    kb_type => [
        -DISPLAY_NAME => 'Bug',
        -TYPE         => 'popup_menu',
        -NAME         => 'kb_type',
        -VALUES       => [
                 '',
                 'No',
                 'Yes', 
                 ''
                 ]
    ],
    

    questions => [
        -DISPLAY_NAME => 'Question',
        -TYPE         => 'textarea',
        -NAME         => 'questions',
        -ROWS         => 1,
        -COLS         => 100,
        -WRAP         => 'VIRTUAL'
    ],

    summary => [
        -DISPLAY_NAME => 'Summary',
        -TYPE         => 'textarea',
        -NAME         => 'summary',
        -ROWS         => 3,
        -COLS         => 100,
        -WRAP         => 'VIRTUAL'
    ],
    
    rep_description => [
        -DISPLAY_NAME => 'Steps to Reproduce',
        -TYPE         => 'textarea',
        -NAME         => 'rep_description',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],



    user_type => [
        -DISPLAY_NAME => '<b>User Type</b> ',
        -TYPE         => 'popup_menu',
        -NAME         => 'user_type',
        -VALUES  => [
            '',
            'My_SQL_admin',
            '---Extropia---',
            'Developer',
        ]
    ],
    
    category_2 => [
        -DISPLAY_NAME => '<b>Category 2</b> ',
        -TYPE         => 'popup_menu',
        -NAME         => 'category_2',
        -VALUES  => [
                'DropList',
                'Setup',
                'Site Porting',
                'Widgets',
        	]
    ],

    submitted_by => [
        -DISPLAY_NAME => 'Submitted by (Required)',
        -TYPE         => 'textfield',
        -NAME         => 'submitted_by',
        -DEFAULT      => $SESSION->getAttribute(
 		-KEY => 'auth_username'),
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
    server_os => [
        -DISPLAY_NAME => 'Server Operating System. ',
        -TYPE         => 'popup_menu',
        -NAME         => 'server_os',
        -VALUES  => [    
                    '',
			'AIX',
			'Unix',
			'FreeBSD 2.x',
			'FreeBSD 3.x',
			'HPUX',
			'IRIX 5.3',
			'IRIX 6.2',
			'Linux (libc5 i.e.. old RedHat 4) (Intel)',
			'Linux (libc6)',
			'OSF1/DEC Unix',
			'Solaris x86 (Intel)',
			'Sparc Solaris 2.5/2.6',
			'Sparc Solaris 7 (2.7)',
			'Sparc Solaris 8 (2.8)',
			'Solaris 5.6',
			'Solaris',
			'Sun Solaris',
			'Sun 450 /Solaris 2.6',
			'Windows NT (Apache)',
			'Windows NT (IIS)',
			'Windows NT',
			'Windows 2000 (Intel)',
        ]
    ],

    build => [
        -DISPLAY_NAME => '<b>Build</b> ',
        -TYPE         => 'popup_menu',
        -NAME         => 'build',
        -VALUES  => [
            '',		
            '6',
            '(None)',
            '1',
            '2',
            '3',
            '4',
            '5',
            '7',
        ]
    ],
    
    workaround => [
        -DISPLAY_NAME => 'Workaround',
        -TYPE         => 'textarea',
        -NAME         => 'workaround',
        -ROWS         => 3,
        -COLS         => 100,
        -WRAP         => 'VIRTUAL'
    ],

    internal_notes => [
        -DISPLAY_NAME => 'Internal Information',
        -TYPE         => 'textarea',
        -NAME         => 'internal_notes',
        -ROWS         => 3,
        -COLS         => 100,
        -WRAP         => 'VIRTUAL'
    ],

    solution => [
        -DISPLAY_NAME => 'Solution',
        -TYPE         => 'textarea',
        -NAME         => 'solution',
        -ROWS         => 6,
        -COLS         => 100,
        -WRAP         => 'VIRTUAL'
    ],

    estimated_man_hours => [
        -DISPLAY_NAME => 'Est. Man Hours',
        -TYPE         => 'textfield',
        -NAME         => 'estimated_man_hours',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

        
    accumulative_time => [
        -DISPLAY_NAME => 'Accumulated time in seconds.',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
    
    category_1 => [
        -DISPLAY_NAME => 'Category 1',
        -TYPE         => 'popup_menu',
        -NAME         => 'category_1',
        -VALUES  => [
                      '',		
               	      'ActionHandler',
                      'HTMLTemplates',
                      'Setup files',
               	      'Methoud',
               	      'Widgets',
        ]
    ],
    browser => [
        -DISPLAY_NAME => '<b>Client Browser</b> ',
        -TYPE         => 'popup_menu',
        -NAME         => 'browser',
        -VALUES  => [
                      '',		
                      'Netscape Navigator',
                      'Netscape Communicator',
                      'Internet Explorer',
                      'AOL',
                      'Opera',
                      'Neoplanet',
                      'NetCaptor',
                      'Netpositive',
        ]
    ],

    issue_type => [
        -DISPLAY_NAME => '<b>Issue Type</b> ',
        -TYPE         => 'popup_menu',
        -NAME         => 'issue_type',
        -VALUES  => [
                      '',		
                      'Bug Report',
                      'Cosmetic',
                      'Feature Request',
                      'Information',
                      'Language',
        ]
    ],
    
    
    audience	 => [
        -DISPLAY_NAME => 'Audience ',
        -TYPE         => 'popup_menu',
        -NAME         => 'audience',
        -VALUES  => [  
                      '',
                      'Public',
        	      'Internal',
        ]
    ],




    record_id => [
        -DISPLAY_NAME => 'Record Id',
        -TYPE         => 'textfield',
        -NAME         => 'record_id',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    count => [
        -DISPLAY_NAME => 'Count',
        -TYPE         => 'textfield',
        -NAME         => 'count',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
    username_of_poster => [
        -DISPLAY_NAME => 'username_of_poster',
        -TYPE         => 'textfield',
        -NAME         => 'username_of_poster',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],


    group_of_poster => [
        -DISPLAY_NAME => 'group_of_poster',
        -TYPE         => 'textfield',
        -NAME         => 'group_of_poster',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    date_time_posted => [
        -DISPLAY_NAME => 'date_time_posted',
        -TYPE         => 'textfield',
        -NAME         => 'date_time_posted',
        -SIZE         => 30,
        -MAXLENGTH    => 80
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
        status
        company_code
	kb_type
        audience
        user_type
        category_1
        category_2
        questions
        summary
        solution
        workaround
        browser
        internal_notes
        submitted_by
        comments        
        count
 
    );


#my %ACTION_HANDLER_PLUGINS =
#    (

#     'Default::DisplayAddFormAction' =>
#     {
#      -DisplayAddFormAction     => [qw(Plugin::Todo::DisplayAddFormAction)],
#     },
#
#     'Default::DisplayDetailsRecordViewAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayDeleteRecordConfirmationAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayModifyFormAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayModifyRecordConfirmationAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::ProcessModifyRequestAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayAddRecordConfirmationAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },
#
#     'Default::ProcessAddRequestAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },
#
#     'Default::DefaultAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayViewAllRecordsAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplaySimpleSearchResultsAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayOptionsFormAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayPowerSearchFormAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },
#
#     'Default::PerformPowerSearchAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },



#    );


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
	        -TABLE        => 'csc_kb_tb',
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
my @CLIENT_DATASOURCE_FIELD_NAMES = qw(
        category
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


my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -CLIENT_DATASOURCE_CONFIG_PARAMS    => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
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
       abstract
       location
       start_date
       end_date
       recur_interval
       recur_until_date
       details
       estimated_man_hours
       accumulative_time
       comments        
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $CGI->param('email')||'todologin@computersystemconsulting.ca',
    -TO       => 'kb@computersystemconsulting.ca',
    -REPLY_TO => 'csc@computersystemconsulting.ca',
    -SUBJECT  => "$APP_NAME_TITLE Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $CGI->param('email')||'todologin@forager.com',
    -TO       => 'kb@computersystemconsulting.ca',
    -REPLY_TO => 'kb@computersystemconsulting.ca',
    -SUBJECT  => "$APP_NAME_TITLE Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $CGI->param('email')||'todologin@forager.com',
    -TO       => 'kb@computersystemconsulting.ca',
    -REPLY_TO => 'kb@computersystemconsulting.ca',
    -SUBJECT  => "$APP_NAME_TITLE Modification"
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
    -LOG_ENTRY_PREFIX => 'Todo|'
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

my @VALID_VIEWS = 
    qw(
       CSSView

       DetailsRecordView
       BasicDataView

       AddRecordView
       AddRecordConfirmationView
       AddAcknowledgementView

       DeleteRecordConfirmationView
       DeleteAcknowledgementView

       ModifyRecordView
       ModifyRecordConfirmationView
       ModifyAcknowledgementView

       PowerSearchFormView
       OptionsView
       LogoffView
       CSCHome
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $applogo,
    -APPLICATION_LOGO_HEIGHT        => '50',
    -APPLICATION_LOGO_WIDTH         => '353',
    -APPLICATION_LOGO_ALT           => $applogoalt,
    -COLOR_FOR_EVEN_ROWS            => 'E5E5E5',
    -COLOR_FOR_ODD_ROWS             => 'FFFFFF',
    -DISPLAY_FIELDS        => [qw(
        kb_type
        questions
         )],
    -DOCUMENT_ROOT_URL       => '/',
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_TRUNCATED =>      [qw(
        questions 
        summary
        workaround 
        solution 
      )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        body
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
	questions 
        summary
        workaround 
        solution 
    )],
    -FIELD_NAME_MAPPINGS   => {
      'record_id'             => 'KB ID ',
      'status'                => 'Status ',
        'kb_type'	            => 'Bug ',
        'questions'           => 'Questions ',
        'summary'             => 'Summary ',
        'workaround'          => 'Workaround ',
        'solution'            => 'Solution ',
        'user_type'           => 'User Type ',
        'browser'	      => 'Browser ',
        'category_1'	      => 'Category 1 ',
        'submitted_by'        => 'Submitted by  ',
        'user_name_of_poster'        => 'First Posted by',
        'category_2'          => 'Category 2 ',
        'comments'            => 'Comments '
        },
      
    -HOME_VIEW               => $HomePageViewName,
    -IMAGE_ROOT_URL          => $imagerooturl,
    -LINK_TARGET             => '_self',
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SORT_FIELDS        => [qw(
      record_id
        questions
        user_type
        submitted_by
         comments        
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
        kb_type
        questions
        summary
	  )],
  
    -TABLE_BG_COLOR_1        => '6699CC',
    -TABLE_BG_COLOR_2        => 'E5E5E5',
    -TABLE_BG_FONT_COLOR_1   => 'BLACK',
    -TABLE_BG_FONT_COLOR_2   => 'BLACK'
);  

######################################################################
#                           DATE TIME SETUP                             #
######################################################################

my @DATETIME_CONFIG_PARAMS = 
    (
     -TYPE => 'ClassDate',
    );

######################################################################
#                           FILTER SETUP                             #
######################################################################

my @HTMLIZE_FILTER_CONFIG_PARAMS = (
    -TYPE                          => 'HTMLize',
    -CONVERT_DOUBLE_LINEBREAK_TO_P => 1,
    -CONVERT_LINEBREAK_TO_BR       => 1,
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

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST = 
    qw(
       CSC::ProcessShowKBAction
       CSC::PopulateInputWidgetDefinitionListWithCompanyCodeWidgetAction

       Default::SetSessionData
       Default::DisplayCSSViewAction

       Default::DisplayDetailsRecordViewAction

       Default::DisplayDeleteFormAction
       Default::ProcessDeleteRequestAction
       Default::DisplayDeleteRecordConfirmationAction

       Default::DisplayModifyFormAction
       Default::ProcessModifyRequestAction
       Default::DisplayModifyRecordConfirmationAction

       Default::DisplayAddFormAction
       Default::ProcessAddRequestAction
       Default::DisplayAddRecordConfirmationAction

       Default::DisplaySimpleSearchResultsAction
       Default::DisplayOptionsFormAction
       Default::DisplayPowerSearchFormAction
       Default::PerformPowerSearchAction

       Default::PerformLogonAction
       Default::PerformLogoffAction

       Default::DisplayViewAllRecordsAction
       Default::DefaultAction

      );


my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'BugTrackerApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => 'BasicDataView',
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $css_view_name,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'status',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'developer',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
#    -SORT_DIRECTION                         => 'DESC',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
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
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
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
    -PAGE_TOP_VIEW                          => $page_top_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -PAGE_LIST_VIEW                         => 'CSCSubscribeListView',
    -LEFT_PAGE_VIEW                         => $page_left_view,
    -DATETIME_CONFIG_PARAMS                 => \@DATETIME_CONFIG_PARAMS,
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = Extropia::Core::App::DBApp->new(
    -ROOT_ACTION_HANDLER_DIRECTORY => "../ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() .  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();
