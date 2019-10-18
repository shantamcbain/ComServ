#!/usr/bin/perl -wT

# 	$Id: page.cgi,v 1.02 2018/12/20
#  1.01 2015/08/30 14:27:36 shanta Exp $	

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
    @dirs = qw(Modules/
               Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(Modules/Extropia/View/Todo
       Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(HTMLTemplates/AltPower
       HTMLTemplates/Apis
       HTMLTemplates/CSPS
       HTMLTemplates/CSC       
       HTMLTemplates/CS
       HTMLTemplates/Demo
       HTMLTemplates/Brew
       HTMLTemplates/ENCY
       HTMLTemplates/ECF
       HTMLTemplates/HelpDesk
       HTMLTemplates/HE
       HTMLTemplates/LT
       HTMLTemplates/MW       
       HTMLTemplates/Organic
       HTMLTemplates/Shanta 
       HTMLTemplates/SB
       HTMLTemplates/SkyeFarm 
       HTMLTemplates/Todo
       HTMLTemplates/USBM
       HTMLTemplates/WW       
       HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
use CGI::Carp qw(fatalsToBrowser);

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

my $APP_NAME = "page"; 
my $APP_NAME_TITLE ;
my $SiteName =  $CGI->param('site')||'CSC';
my $site_update;
my $username;
my $group;
my $CustCode =  $CGI->param('custcode') || "BMaster";
my $home_view; 
my $BASIC_DATA_VIEW; 
my $View     = $CGI->param('view')||'PageView';
my $Page     = $CGI->param('page')||'HomeView';
my $page_top_view;
my $page_bottom_view;
my $page_left_view;
#Mail settings
my $mail_from; 
my $mail_to;
my $auth_mail_to;
my $mail_replyto;
my $CSS_VIEW_NAME;
my $app_logo;
my $app_logo_height;
my $app_logo_width;
my $app_logo_alt;
my $IMAGE_ROOT_URL; 
my $apsubmenu ='' ;

my $DOCUMENT_ROOT_URL;
my $site;
my $GLOBAL_DATAFILES_DIRECTORY;
my $TEMPLATES_CACHE_DIRECTORY;
my $APP_DATAFILES_DIRECTORY;
my $DATAFILES_DIRECTORY;
my $site_session;
my $auth;
my $MySQLPW;
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_DESCRIPTION;
my $LINK_TARGET;
my $additonalautusernamecomments;
my $DBI_DSN;
my $AUTH_TABLE;
my $AUTH_MSQL_USER_NAME;
my $PAGE_DBI; 
my $PAGE_MySQLPW;
my $PAGE_MSQL_USER_NAME;
my $pageMySQLPW ;
my $DEFAULT_CHARSET;
my $mail_to_user;
my $mail_to_member;
my $mail_to_discussion;
my $LineStatus = "yes";
my $last_update = 'Febuary 5, 2015';
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $SiteLastUpdate;
my $shop = 'cs';
my $NEWS_TB;
my $search = 0;
my $Affiliate = 001;
my $StoreUrl = 'countrystores.ca';
my $allow_add;
my $allow_mod;
my $allow_del;
my $HasMembers;
use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl, $SiteName);
#    $SiteName 		   = $SetupVariables->{-SITE_NAME};
    $APP_NAME_TITLE        = "LiveEdit";
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $home_view             = $BASIC_DATA_VIEW||$SetupVariables->{-HOME_VIEW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-page_left_view};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
#Mail settings
    $mail_from              = $SetupVariables->{-MAIL_FROM};
    $mail_to                = $SetupVariables->{-MAIL_TO};
    $auth_mail_to           = $SetupVariables->{-MAIL_TO_AUTH};
    $mail_replyto           = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME          = $SetupVariables->{-CSS_VIEW_NAME};
    $app_logo               = $SetupVariables->{-APP_LOGO};
    $app_logo_height        = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width         = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt           = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL         = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL      = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET            = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS     = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS   = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    $FAVICON                 = $SetupVariables->{-FAVICON};
    $ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
    $FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
    $SiteName                =  $CGI->param('site')|| $SetupVariables->{-FAVICON_TYPE};
    $site                    = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'/home/grindrod/Datafiles/';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    my $LocalIp                 = $SetupVariables->{-LOCAL_IP};
    my $site_for_search         = 0;
    $PAGE_DBI                   = $SetupVariables ->{-PAGE_DBI};
    $PAGE_MySQLPW               = $SetupVariables ->{-PAGE_MySQLPW};
    $PAGE_MSQL_USER_NAME        = $SetupVariables ->{-PAGE_MSQL_USER_NAME};





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

if ($SiteName eq "DarmaFarms") {
   $group    = 'ECF_Client';
   $SiteName = 'ECF';
	if ( $username eq 'gardenboy') {
	 $group    = 'DarmaFarms_Admin';
	};
};

if ($CGI->param('site')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'SiteName')){
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

 $username =  $SESSION ->getAttribute(-KEY => 'auth_username');
 $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');


  




if ($username eq "Shanta") {$search = 1;
  $allow_add = 1;
  $allow_mod = 1;
  $allow_del = 1;  
}
 if ($group eq "CSC_Admin" or
     $group eq "Apis_admin" or
     $group eq "BMast_Admin" or
     $group eq "BeeTalk_Admin" or
     $group eq "CSCDev_Admin" or
     $group eq "Brew_Admin" or
     $group eq "ECF_Admin" or
     $group eq "Aikikai_Admin" ) {$search = 1;
  $allow_add = 1;
  $allow_mod = 1;
  $allow_del = 1;  
}
$apsubmenu = 'ApplicationSubMenuView';




#$page_top_view    = $CGI->param('page_top_view')||$page_top_view;
#$page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
#$page_left_view   = $CGI->param('page_left_view')||$page_left_view;
#$page_left_view = "LeftPageView";


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
my @AUTH_USER_DATASOURCE_PARAMS;
if ($site eq "file") {

	@AUTH_USER_DATASOURCE_PARAMS = (
	    -TYPE                       => 'File',
	    -FIELD_DELIMITER            => '|',
	    -CREATE_FILE_IF_NONE_EXISTS => 1,
	    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
	    -FILE                       => "$APP_DATAFILES_DIRECTORY/$AUTH_TABLE.dat"
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
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -page_left_view          => $page_left_view,
    -PAGE_LEFT_VIEW          => $page_left_view,
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
    'auth_username'  => 'Username no spaces',
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
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -SUBJECT => 'Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      => $mail_to,
    -SUBJECT => "$SiteName Registration Notification"
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
       sitename	      	=> 'SiteName',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       owner            => 'Owner',
       lastupdate       => 'Last update',
       due_date         => 'Due Date',
       abstract         => 'Subject',
       details          => 'Description',
       status           => 'Status',
       priority         => 'Priority',
       last_mod_by      => 'Last Modified By',
       last_mod_date    => 'Last Modified Date',
       comments         => 'Comments',
       pageheader       => 'Page Header',
      },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
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
            -NEW_STRING => "'"
        ],

        -IS_EMAIL => [
            -FIELDS => [qw(
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
        ],

 
        -IS_FILLED_IN => [
            -FIELDS => [
                        qw(
                           sitename                           
                           page_code
                           body
                           status
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
       sitename	      	=> 'Site Name',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       lastupdate           => 'Last update',
       due_date             => 'Due Date',
       abstract             => 'Subject',
       details              => 'Description',
       status               => 'Status',
       priority             => 'Priority',
       comments             => 'Comments',
       pageheader           => 'Page Header',
   },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
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
            -NEW_STRING => "'"
        ],

        -IS_EMAIL => [
            -FIELDS => [qw(
                email
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
        ],


        -IS_FILLED_IN => [
            -FIELDS => [qw(
                          sitename
                          view_name
                          page_code           
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
       sitename
       menu
       page_code
       page_site
       app_title
       view_name
       body
       facebook
       linkedin
       description
       keywords
       link_order
       news
       status
       share
       mailchimp
       lastupdate
       last_mod_by
       last_mod_date
       comments        
      );

# prepare the data then used in the form input definition
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (2012..2015);
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
      1 => 'Archive',
      2 => 'Active',
    );

my %share =
    (
      1 => 'Private',
      2 => 'Public',
    );
    
my %news = (

      0 => 'None', 
      1 => 'One', 
      2 => 'Two', 
      3 => 'Three', 
      4 => 'Four', 
      5 => 'five', 
      6 => 'Six', 
      7 => 'Seven', 
      8 => 'Eight', 
      9 => 'Nine', 
      10 => 'Ten',
    );

my %menu =
    (
      none => 'None', 
      admin => 'Admin', 
      main => 'Main', 
      bottom => 'Bottom', 
      member => 'Members', 
      cust => 'Customers', 
      top => 'Top', 
      helpdesk => 'HelpDesk', 
    );

my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     sitename => [
        -DISPLAY_NAME => 'Site name code',
        -TYPE         => 'textfield',
        -NAME         => 'sitename',
        -VALUE        => $SiteName,
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],


   abstract => [
                 -DISPLAY_NAME => 'Subject',
                 -TYPE         => 'textfield',
                 -NAME         => 'abstract',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
                ],
    accumulative_time => [
        -DISPLAY_NAME => 'Accumulated Please Add time to entry',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
    
   page_site => [
                 -DISPLAY_NAME => 'This is the first group of words In the browser top bar. Leave blank for default.',
                 -TYPE         => 'textfield',
                 -NAME         => 'page_site',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
                ],
   app_title=> [
                 -DISPLAY_NAME => 'The midle group of words in the browser top bar.',
                 -TYPE         => 'textfield',
                 -NAME         => 'app_title',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

     body  => [
                 -DISPLAY_NAME => 'Page Content here',
                 -TYPE         => 'textarea',
                 -NAME         => 'body',
                 -ROWS         => 100,
                 -COLS         => 80,
                 -WRAP         => 'VIRTUAL',
                 -INPUT_CELL_COLSPAN => 3,
               ],
    facebook => [
        -DISPLAY_NAME => 'Your face book link for this page',
        -TYPE         => 'textfield',
        -NAME         => 'facebook',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    linkedin => [
        -DISPLAY_NAME => 'Your Linked in link for this page',
        -TYPE         => 'textfield',
        -NAME         => 'linkedin',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     link_order => [
                 -DISPLAY_NAME => 'Order of dispaly',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'link_order',
                 -VALUES       => [0..12],
               ],
    menu => [
      -DISPLAY_NAME => 'Link Menu.',
    -TYPE         => 'popup_menu',
   -NAME         => 'menu',
   -VALUES       => [sort {$a <=> $b} keys %menu],
   -LABES        => \%menu,
   -INPUT_CELL_COLSPAN => 3,
    ],

     page_code => [
        -DISPLAY_NAME => 'Page Code.',
        -TYPE         => 'textfield',
        -NAME         => 'page_code',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
   view_name => [
        -DISPLAY_NAME => 'Name of your page',
        -TYPE         => 'textfield',
        -NAME         => 'view_name',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     lastupdate => [
        -DISPLAY_NAME => 'Last Update, Leave blank if not wanted',
        -TYPE         => 'textfield',
        -NAME         => 'lastupdate',
        -SIZE         => 30,
        -MAXLENGTH    => 80
     ],
     mailchimp => [
        -DISPLAY_NAME => 'MailChimp url.',
        -TYPE         => 'textfield',
        -NAME         => 'mailchimp',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     start_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     start_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],

     due_day => [
                 -DISPLAY_NAME => 'Due Date',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_day',
                 -VALUES       => [1..31],
                ],

     due_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     due_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],
                
                
   news => [
   -DISPLAY_NAME => 'Number of News pages',
   -TYPE         => 'popup_menu',
   -NAME         => 'news',
   -VALUES         => [sort {$a <=> $b} keys %news],
   -LABELS       =>\%news,
   -INPUT_CELL_COLSPAN => 3,
   ],
   
 keywords   => [
   -DISPLAY_NAME => 'Header Keywords, max 12 Not supported',              
   -TYPE         => 'textarea',
   -NAME         => 'keywords',
   -ROWS         => 4,
   -COLS         => 80,
   -WRAP         => 'VIRTUAL',
   -INPUT_CELL_COLSPAN => 3,
               ],
description   => [
   -DISPLAY_NAME => 'Header discription max lingth 150',              
   -TYPE         => 'textfield',
   -NAME         => 'description',
   -SIZE         => 60,
   -MAXLENGTH    => 150
               ],

   priority => [
   -DISPLAY_NAME => 'priority',
   -TYPE         => 'popup_menu',
   -NAME         => 'priority',
   -VALUES       => [sort {$a <=> $b} keys %priority],
   -LABES        => \%priority,
   -INPUT_CELL_COLSPAN => 3,
               ],

     status => [
                 -DISPLAY_NAME => 'Status',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'status',
                 -VALUES       => [sort {$a <=> $b} keys %status],
	          	  -LABELS       => \%status,
                 -INPUT_CELL_COLSPAN => 3,
                ],

     share => [
                 -DISPLAY_NAME => 'Share',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'share',
                 -VALUES       => [sort {$a <=> $b} keys %share],
	          	  -LABELS       => \%share,
                 -INPUT_CELL_COLSPAN => 3,
                ],
   );


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (
      qw(sitename),      
      qw(page_code),      
      qw(keywords),
      qw(description),
      qw(link_order),
      qw(app_title),
      qw(page_site),
      qw(menu),      
      qw(view_name),
      qw(body), 
      qw(status),
      qw(facebook),
      qw(linkedin),
      qw(mailchimp),
      qw(news),
      qw(lastupdate),   
      qw(comments),
      qw(share),
   );

my %ACTION_HANDLER_PLUGINS ;




    


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
          -DBI_DSN      => $PAGE_DBI,
	        -TABLE        => 'page_tb',
	        -USERNAME     => $PAGE_MSQL_USER_NAME,
	        -PASSWORD     => $PAGE_MySQLPW,
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
    -PAGE_DATASOURCE_CONFIG_PARAMS      => \@BASIC_DATASOURCE_CONFIG_PARAMS,
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
       status
       sitename
       page_code
       view_name
       body
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE. ' Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')|| $mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE. ' Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE. ' Modification'
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
    -LOG_ENTRY_PREFIX => $APP_NAME.' |'
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
       ApisCSSView
       BCHPACSSView
       ECFCSSView
       OrganicCSSView

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
       
       HomeView
       AboutUsView

       ApisHomeView
       ApisProductView
       ApisPolinatorsView
       ApisPollenView
       ApisWaxView
       ApisBeesView
       ApisQueensView
       ApisWholesaleView
       ApisManagementView
       ApisMentoringView
       ApisSwarmsView
       MiteGoneDocsView
       ApisHoneyView
       CertifiedOrganicView
       AssociateView
       MGWaverView 
       ForumsView
       ContactView
       ProductView
       ProjectsView
       BeeTrailerView

       BCHPAHomeView
       BCHPAAdminHomeView
       BeeTrustView
       BCHPAByLawsView
       BCHPAContactView
       BCHPABoardView
       BCHPAMemberView
       BCHPAPolinatorsView
       
       OkBeekeepersHomeView

       ECFHomeView
       ECFSideBarHomeView
       PrintView
       AppToolsView
       ForageIndicatorView
       PollinatorSQLView
       InventoryProjectionView
       InventoryView
       InventorySQLView
       OfficeView
       SQLView
       PrivacyView
       BeeDiseaseView
       BudgetView
       FeedView
       HoneyDoHomeView 
       HostingView
       InventoryHomeView
       ListJoinView
       MembersView
       MentorHomeView
       MentoringHomeView
       MailView
       SwarmControlView
       ShantaHome
       CertificationView
       ChickensView
       CalendarView
       GrindRodBreaderHomeView
       ECFBreederProjectView
       BMasterBreederHomeView
       BMasterBreederView
       ReUseAblesView
       ReCyclingView
       ShantaLaptopHomeView
       ShopManagerView
       StoreView
       GPMRulesView
       LtrustHomeView
       NucView
       SiteLogView
       WorkShopsView
       RegistrationView
       MailListView
       BotanicalNameView
       ForumulaView
       JobView
       PageView
       PowerUsageView
       BeeTalk
     );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
     -APPLICATION_LOGO               => $app_logo,
     -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
     -APPLICATION_LOGO_WIDTH         => $app_logo_width,
     -APPLICATION_LOGO_ALT           => $app_logo_alt,
	 -FAVICON                        => $FAVICON || '/images/apis/favicon.ico',
	 -ANI_FAVICON                    => $ANI_FAVICON,
	 -FAVICON_TYPE                   => $FAVICON_TYPE,
     -DISPLAY_FIELDS                 => [qw(
        sitename
        page_code
        pageheader
        view_name
        pageheader
        body
        status
        )],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        body
    )],
    -FIELD_NAME_MAPPINGS     => {
        'sitename'     => 'Site Code',
        'body'         => 'Page content',
        'pageheader'   => 'Area above toplinks',
        'page_code'    => 'Page code',
        'view_name'    => 'Page Name',
        'lastupdate'   => 'Last update',
        'status'       => 'Status',
        'share'        => 'Share',
        'priority'     => 'Priority',
        'pageheader'   => 'Page Header',
       },
    -HOME_VIEW               => $home_view,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -CUST_CODE               => $CustCode,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
        sitename
        page_code
        pageheader
        view_name
        body
        lastupdate
        status
        share
        )],
    -SORT_FIELDS             => [qw(
        sitename
        view_name
        status
        share
        )],
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
    -AFFILIATE_NUMBER                       => $Affiliate,
    -ALLOW_ADDITIONS_FLAG                   => $allow_add,
    -ALLOW_MODIFICATIONS_FLAG               => $allow_mod,
    -ALLOW_DELETIONS_FLAG                   => $allow_del,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => $apsubmenu,
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => $home_view,
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 5,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'sitename',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'abstract',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'DESC',
    -Debug                                  => $CGI->param('debug')||0,
    -MOBILE                                 => $CGI->param('m')||0,
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
    -GROUP                                  => $group,
    -HAS_MEMBERS                            => $HasMembers,
    -HTTP_HEADER_PARAMS                     => $HTTP_HEADER_PARAMS||'test',
    -HTTP_HEADER_KEYWORDS                   => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION                => $HTTP_HEADER_DESCRIPTION,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -LineStatus                             => $LineStatus,
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LAST_UPDATE                            => $last_update,
    -SITE_LAST_UPDATE                       => $site_update,
    -LOCAL_IP                               => $LocalIp,
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
    -PAGE_NAME                              => $Page,
    -NEWS_TB                                => $NEWS_TB,
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => $search,
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
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG         => $site_for_search,
    -SEND_EMAIL_ON_DELETE_FLAG              => 1,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -SITE_NAME                              => $SiteName,
    -STORE_URL                              => $StoreUrl,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -SHOP                                   => $shop,
    -USERNAME                               => $username,
    -PAGE_TOP_VIEW                          => $page_top_view,
    -PAGE_LEFT_VIEW                         => $page_left_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -DATETIME_CONFIG_PARAMS                 => \@DATETIME_CONFIG_PARAMS,
    -ACTION_HANDLER_PLUGINS                 => \%ACTION_HANDLER_PLUGINS,
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = Extropia::Core::App::DBApp->new(
    -ROOT_ACTION_HANDLER_DIRECTORY => "ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() .  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();