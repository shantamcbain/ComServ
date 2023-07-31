#!/usr/bin/perl -wT
# 	$Id: index.cgi,v 1.15 2020/01/13 14:27:36 shanta Exp $
# 	$Id: index.cgi,v 1.14 2019/04/08 14:27:36 shanta Exp $
# 	$Id: index.cgi,v 1.13 2019/03/215 14:27:36 shanta Exp $
# 	$Id: index.cgi,v 1.12 2014/03/20 14:27:36 shanta Exp $

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
my $AppVer = "ver 1.15, Dec 02, 2021";

BEGIN
{
 use vars qw(@dirs);
 @dirs = qw(Modules/
   Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

my @VIEWS_SEARCH_PATH = qw(Modules/Extropia/View/Todo
  Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = qw(HTMLTemplates/AltPower
  HTMLTemplates/Apis
  HTMLTemplates/Aikikai
  HTMLTemplates/Brew
  HTMLTemplates/BuyAndSell
  HTMLTemplates/CS
  HTMLTemplates/CSC
  HTMLTemplates/Demo
  HTMLTemplates/ENCY
  HTMLTemplates/ECF
  HTMLTemplates/Forager
  HTMLTemplates/GrindrodProject
  HTMLTemplates/HE
  HTMLTemplates/HelpDesk
  HTMLTemplates/LT
  HTMLTemplates/MonasheeCoop
  HTMLTemplates/MW  
  HTMLTemplates/News
  HTMLTemplates/Organic
  HTMLTemplates/PSP
  HTMLTemplates/Shanta
  HTMLTemplates/SB
  HTMLTemplates/SkyeFarm
  HTMLTemplates/Todo
  HTMLTemplates/UrbanFarming
  HTMLTemplates/USBM
  HTMLTemplates/WB
  HTMLTemplates/WW
  HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI()
  or die(
     "Unable to construct the CGI object" . ". Please contact the webmaster." );

foreach ( $CGI->param() )
{
 $CGI->param( $1, $CGI->param($_) ) if (/(.*)\.x$/);
}

######################################################################
#                          SITE SETUP                             #
######################################################################
my $SiteName       = $CGI->param('site');
my $Affiliate = 001;
my $additonalautusernamecomments;
my $APP_DATAFILES_DIRECTORY;
my $app_logo;
my $app_logo_height;
my $app_logo_width;
my $app_logo_alt;
my $APP_NAME       = "apis";
my $APP_NAME_TITLE = "Apis, Bees and Beekeeping ";
my $auth;
my $AUTH_TABLE;
my $AUTH_MSQL_USER_NAME;
my $BASIC_DATA_VIEW;
my $CustCode = $CGI->param('custcode') || "BMaster";
my $CSS_VIEW_NAME = '/styles/CSCCSSView';
my $CSS_VIEW_URL = $CSS_VIEW_NAME;
my $DBI_DSN;
my $DATAFILES_DIRECTORY;
my $DEFAULT_CHARSET;
my $DOCUMENT_ROOT_URL;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $GLOBAL_DATAFILES_DIRECTORY;
my $home_view ;
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_DESCRIPTION;
my $group  ;
my $HasMembers = 0;
my $HeaderImage;
my $Header_height;
my $Header_width;
my $Header_alt;
my $HostName   = $ENV{'SERVER_NAME'};
my $IMAGE_ROOT_URL;
my $last_update       =  $AppVer|| 'March 15, 2022';
my $LineStatus        = "yes";
my $LINK_TARGET;
#Mail settings
my $mail_from;
my $mail_to;
my $auth_mail_to;
my $mail_replyto;
my $NEWS_TB;
my $OffLine    = 'yes';
my $Page           = $CGI->param('page');
my $Page_tb;
my $page_top_view;
my $page_bottom_view;
my $page_left_view;
my $pid        = '15';
my $procedure      = $CGI->param('procedure');
my $project        = $CGI->param('project');
my $shop = 'cs';
my $site_session;
my $site;
my $SiteLastUpdate;
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $site_for_search = 0;
my $site_update;
my $StoreUrl  = 'countrystores.ca';
my $style = $CGI->param('pagestyle');
my $TEMPLATES_CACHE_DIRECTORY;
my $title          = $CGI->param('title');
my $username;
my $View           = $CGI->param('view') ;



my $VIEW_LOADER =
  new Extropia::Core::View( \@VIEWS_SEARCH_PATH, \@TEMPLATES_SEARCH_PATH )
  or die(   "Unable to construct the VIEW LOADER object in "
          . $CGI->script_name()
          . " Please contact the webmaster." );
#my $HostName    = $ENV{'SERVER_NAME'};

use SiteSetup;
my $UseModPerl     = 1;
my $SetupVariables = new SiteSetup($UseModPerl, 
$CGI->param('site'), $HostName);
$SiteName            = $SiteName || $SetupVariables->{-SITE_NAME};
$Affiliate               = $SetupVariables->{-AFFILIATE};
$APP_DATAFILES_DIRECTORY = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
$app_logo                = $SetupVariables->{-APP_LOGO};
$app_logo_height         = $SetupVariables->{-APP_LOGO_HEIGHT};
$app_logo_width          = $SetupVariables->{-APP_LOGO_WIDTH};
$app_logo_alt            = $SetupVariables->{-APP_LOGO_ALT};
$APP_NAME_TITLE          = $SetupVariables->{-APP_NAME_TITLE};
$AUTH_TABLE              = $SetupVariables->{-AUTH_TABLE};
$AUTH_MSQL_USER_NAME     = $SetupVariables->{-AUTH_MSQL_USER_NAME};
$BASIC_DATA_VIEW         = $SetupVariables->{-HOME_VIEW}  || $SetupVariables->{-BASIC_DATA_VIEW};
$CSS_VIEW_NAME           = $SetupVariables->{-CSS_VIEW_NAME};
$CSS_VIEW_URL            = $SetupVariables->{-CSS_VIEW_NAME};
$DBI_DSN                 = $SetupVariables->{-DBI_DSN};
$DOCUMENT_ROOT_URL       = $SetupVariables->{-DOCUMENT_ROOT_URL};
$FAVICON                 = $SetupVariables->{-FAVICON};
$ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
$FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
$GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'/home/shanta/Datafiles';
$HeaderImage             = $SetupVariables->{-HEADER_IMAGE};
$Header_height           = $SetupVariables->{-HEADER_HEIGHT};
$Header_width            = $SetupVariables->{-HEADER_WIDTH};
$Header_alt              = $SetupVariables->{-HEADER_ALT};
$HasMembers              = $SetupVariables->{-HAS_MEMBERS};
$home_view               = $SetupVariables->{-HOME_VIEW}||'HomeView';
$HTTP_HEADER_PARAMS      = $SetupVariables->{-HTTP_HEADER_PARAMS};
$HTTP_HEADER_KEYWORDS    = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
$HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
$IMAGE_ROOT_URL          = $SetupVariables->{-IMAGE_ROOT_URL};
$last_update             = $SetupVariables->{-LAST_UPDATE};
$LineStatus              = $SetupVariables->{-Line_Status} || $LineStatus;
$LINK_TARGET             = $SetupVariables->{-LINK_TARGET};
my $LocalIp              = $SetupVariables->{-LOCAL_IP};
#Mail settings
$mail_from               = $SetupVariables->{-MAIL_FROM}; 
$mail_to                 = $SetupVariables->{-MAIL_TO};
$mail_replyto            = $SetupVariables->{-MAIL_REPLYTO};
$auth_mail_to            = $SetupVariables->{-MAIL_TO_AUTH};
$mail_replyto            = $SetupVariables->{-MAIL_REPLYTO};
my $mail_to_user         = $SetupVariables->{-MAIL_USER};
my $mail_to_member       = $SetupVariables->{-MAIL_MEMBER};
my $mail_to_discussion   = $SetupVariables->{-MAIL_DISCUSSION};
my $MySQLPW                 = $SetupVariables->{-MySQLPW};
$NEWS_TB                 = $SetupVariables->{-NewsTable};
$page_top_view           = $SetupVariables->{-PAGE_TOP_VIEW};
$page_bottom_view        = $SetupVariables->{-PAGE_BOTTOM_VIEW};
$page_left_view          = $SetupVariables->{-page_left_view};
$Page_tb                 = $SetupVariables->{-PAGE_TB} || 'page_tb';
$pid                     = $SetupVariables->{-PID};
$site                    = $SetupVariables->{-DATASOURCE_TYPE};
$SITE_DISPLAY_NAME       = $SetupVariables->{-SITE_DISPLAY_NAME};
$site_update             = $SetupVariables->{-SITE_LAST_UPDATE};
$shop                    = $SetupVariables->{-SHOP};
$StoreUrl                = $SetupVariables->{-STORE_URL};
$TEMPLATES_CACHE_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY . $SetupVariables->{ -TEMPLATES_CACHE_DIRECTORY, };



######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
                         -TYPE            => 'File',
                         -MAX_MODIFY_TIME => 60 * 60 * 60,
                         -SESSION_DIR => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
                         -FATAL_TIMEOUT           => 0,
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

my $SESSION_MGR =
  Extropia::Core::SessionManager->create( @SESSION_MANAGER_CONFIG_PARAMS );

my $SESSION    = $SESSION_MGR->createSession();
my $SESSION_ID = $SESSION->getId();
#my $CSS_VIEW_URL =

#  $CGI->script_name() . "?display_css_view=on&session_id=$SESSION_ID";

if ( $CGI->param('site') )
{
 if ( $CGI->param('site') ne $SESSION->getAttribute( -KEY => 'SiteName' ) )
 {
  $SESSION->setAttribute( -KEY => 'SiteName', -VALUE => $CGI->param('site') );
  $SiteName = $CGI->param('site');
 }
 else
 {
  $SESSION->setAttribute( -KEY => 'SiteName', -VALUE => $SiteName );
 }

}
else
{
 if ( $SESSION->getAttribute( -KEY => 'SiteName' ) )
 {
  $SiteName = $SESSION->getAttribute( -KEY => 'SiteName' );
 }
 else
 {
  $SESSION->setAttribute( -KEY => 'SiteName', -VALUE => $SiteName );
 }
}

$username =  $SESSION ->getAttribute(-KEY => 'auth_username');
 $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');


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

if ( $site eq "file" )
{

 @AUTH_USER_DATASOURCE_PARAMS = (
                             -TYPE                       => 'File',
                             -FIELD_DELIMITER            => '|',
                             -CREATE_FILE_IF_NONE_EXISTS => 1,
                             -FIELD_NAMES => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
                             -FILE => "$APP_DATAFILES_DIRECTORY/$AUTH_TABLE.dat"
 );
}
else
{

 @AUTH_USER_DATASOURCE_PARAMS = (
                              -TYPE        => 'DBI',
                              -DBI_DSN     => $DBI_DSN,
                              -TABLE       => $AUTH_TABLE,
                              -USERNAME    => $AUTH_MSQL_USER_NAME,
                              -PASSWORD    => $MySQLPW,
                              -FIELD_NAMES => \@AUTH_USER_DATASOURCE_FIELD_NAMES
 );
}

my @AUTH_ENCRYPT_PARAMS = ( -TYPE => 'Crypt' );

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
      -USER_FIELDS_TO_DATASOURCE_MAPPING => \%USER_FIELDS_TO_DATASOURCE_MAPPING,
      -AUTH_CACHE_PARAMS                 => \@AUTH_CACHE_PARAMS
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
 -DATAHANDLERS => [
  qw(
    Email
    Exists
    )
 ],

 -FIELD_MAPPINGS => {
                      'auth_username'  => 'Username',
                      'auth_password'  => 'Password',
                      'auth_password2' => 'Confirm Password',
                      'auth_firstname' => 'First Name',
                      'auth_lastname'  => 'Last Name',
                      'auth_email'     => 'E-Mail Address'
 },

 -IS_FILLED_IN => [
  qw(
    auth_username
    auth_firstname
    auth_lastname
    auth_email
    )
 ],

 -IS_EMAIL => [
  qw(
    auth_email
    )
 ]
);

my @USER_FIELDS = (
 qw( 
   auth_username
   auth_password
   auth_groups
   auth_firstname
   auth_lastname
   auth_email
   )
);
my @ADMIN_EMAIL_DISPLAY_FIELDS = qw(
  username
  password
  groups
  firstname
  lastname
  email
);
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

my @MAIL_PARAMS = ( -TYPE => 'Sendmail', );

my @USER_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -SUBJECT => 'Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
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
 -DATAHANDLERS => [
  qw(
    Email
    Exists
    HTML
    String
    )
 ],

 -FIELD_MAPPINGS => {
                      project_code        => 'Project Code',
                      estimated_man_hours => 'Estimated Man Hours',
                      accumulative_time   => 'Accumulated time',
                      owner               => 'Owner',
                      start_date          => 'Start Date',
                      due_date            => 'Due Date',
                      abstract            => 'Subject',
                      details             => 'Description',
                      status              => 'Status',
                      priority            => 'Priority',
                      last_mod_by         => 'Last Modified By',
                      last_mod_date       => 'Last Modified Date',
                      comments            => 'Comments',
 },


   -RULES => [
  -ESCAPE_HTML_TAGS => [
   -FIELDS => [
    qw(
      *
      )
   ]
  ],

  -DOES_NOT_CONTAIN => [
   -FIELDS => [
    qw(
      *
      )
   ],

   -CONTENT_TO_DISALLOW => '\\',
   -ERROR_MESSAGE       => "You may not have a '\\' character in the "
     . "%FIELD_NAME% field."
  ],

  -DOES_NOT_CONTAIN => [
   -FIELDS => [
    qw(
      *
      )
   ],

   -CONTENT_TO_DISALLOW => '\"',
   -ERROR_MESSAGE       => "You may not have a '\"' character in the "
     . "%FIELD_NAME% field."
  ],

  -IS_EMAIL => [
   -FIELDS => [
    qw(
      )
   ],

   -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value '
     . 'for %FIELD_NAME%.'
  ],

  -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
   -FIELDS => [
    qw(
      *
      )
   ],
   -ORIGINAL_STRING => '"',
   -NEW_STRING      => "''"
  ],

  -IS_FILLED_IN => [
   -FIELDS => [
    qw(
      owner
      start_date
      due_date
      abstract
      status
      priority
      last_mod_by
      last_mod_date
      )
   ]
  ]
   ]
);

my @MODIFY_FORM_DHM_CONFIG_PARAMS = (
 -TYPE         => 'CGI',
 -CGI_OBJECT   => $CGI,
 -DATAHANDLERS => [
  qw(
    Email
    Exists
    HTML
    String
    )
 ],

 -FIELD_MAPPINGS => {
                      project_code        => 'Project Code',
                      estimated_man_hours => 'Estimated Man Hours',
                      accumulative_time   => 'Accumulated time',
                      start_date          => 'Start Date',
                      due_date            => 'Due Date',
                      abstract            => 'Subject',
                      details             => 'Description',
                      status              => 'Status',
                      priority            => 'Priority',
                      comments            => 'Comments',
 },

 -RULES => [
  -ESCAPE_HTML_TAGS => [
   -FIELDS => [
    qw(
      *
      )
   ]
  ],

  -DOES_NOT_CONTAIN => [
   -FIELDS => [
    qw(
      *
      )
   ],

   -CONTENT_TO_DISALLOW => '\\',
   -ERROR_MESSAGE       => "You may not have a '\\' character in the "
     . "%FIELD_NAME% field."
  ],

  -DOES_NOT_CONTAIN => [
   -FIELDS => [
    qw(
      *
      )
   ],

   -CONTENT_TO_DISALLOW => '\"',
   -ERROR_MESSAGE       => "You may not have a '\"' character in the "
     . "%FIELD_NAME% field."
  ],

  -IS_EMAIL => [
   -FIELDS => [
    qw(
      email
      )
   ],

   -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value '
     . 'for %FIELD_NAME%.'
  ],

  -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
   -FIELDS => [
    qw(
      *
      )
   ],
   -ORIGINAL_STRING => '"',
   -NEW_STRING      => "''"
  ],

  -IS_FILLED_IN => [
   -FIELDS => [
    qw(
      owner
      start_date
      due_date
      abstract
      status
      priority
      last_mod_by
      last_mod_date
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

my @DATASOURCE_FIELD_NAMES = qw(
  record_id
  owner
  start_date
  project_code
  estimated_man_hours
  accumulative_time
  due_date
  abstract
  details
  status
  priority
  last_mod_by
  last_mod_date
  comments
);

# prepare the data then used in the form input definition
my @months = qw(January February March April May June July August
  September October November December);
my %months;
@months{ 1 .. @months } = @months;
my %years = ();
$years{$_} = $_ for ( 2001 .. 2005 );
my %days = ();
$days{$_} = $_ for ( 1 .. 31 );

my %priority = (
                 1 => 'LOW',
                 2 => 'MIDDLE',
                 3 => 'HIGH',
);

my %status = (
               1 => 'NEW',
               2 => 'IN PROGRESS',
               3 => 'DONE',
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
 abstract => [
               -DISPLAY_NAME       => 'Subject',
               -TYPE               => 'textfield',
               -NAME               => 'abstract',
               -SIZE               => 44,
               -MAXLENGTH          => 200,
               -INPUT_CELL_COLSPAN => 3,
 ],

 accumulative_time => [
                        -DISPLAY_NAME => 'Accumulated Please Add time to entry',
                        -TYPE         => 'textfield',
                        -NAME         => 'accumulative_time',
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
 ],

 details => [
              -DISPLAY_NAME       => 'Description',
              -TYPE               => 'textarea',
              -NAME               => 'details',
              -ROWS               => 8,
              -COLS               => 42,
              -WRAP               => 'VIRTUAL',
              -INPUT_CELL_COLSPAN => 3,
 ],

 estimated_man_hours => [
                          -DISPLAY_NAME => 'Est. Man Hours',
                          -TYPE         => 'textfield',
                          -NAME         => 'estimated_man_hours',
                          -SIZE         => 30,
                          -MAXLENGTH    => 80
 ],

 start_day => [
                -DISPLAY_NAME => 'Start Date',
                -TYPE         => 'popup_menu',
                -NAME         => 'start_day',
                -VALUES       => [ 1 .. 31 ],
 ],

 start_mon => [
                -DISPLAY_NAME => '',
                -TYPE         => 'popup_menu',
                -NAME         => 'start_mon',
                -VALUES       => [ 1 .. 12 ],
                -LABELS       => \%months,
 ],

 start_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_year',
                 -VALUES       => [ sort { $a <=> $b } keys %years ],
 ],

 due_day => [
              -DISPLAY_NAME => 'Due Date',
              -TYPE         => 'popup_menu',
              -NAME         => 'due_day',
              -VALUES       => [ 1 .. 31 ],
 ],

 due_mon => [
              -DISPLAY_NAME => '',
              -TYPE         => 'popup_menu',
              -NAME         => 'due_mon',
              -VALUES       => [ 1 .. 12 ],
              -LABELS       => \%months,
 ],

 due_year => [
               -DISPLAY_NAME => '',
               -TYPE         => 'popup_menu',
               -NAME         => 'due_year',
               -VALUES       => [ sort { $a <=> $b } keys %years ],
 ],

 priority => [
               -DISPLAY_NAME       => 'Priority',
               -TYPE               => 'popup_menu',
               -NAME               => 'priority',
               -VALUES             => [ sort { $a <=> $b } keys %priority ],
               -LABELS             => \%priority,
               -INPUT_CELL_COLSPAN => 3,
 ],

 project_code => [
                   -DISPLAY_NAME => 'Project Code',
                   -TYPE         => 'popup_menu',
                   -NAME         => 'project_code',
                   -VALUES       => [
                                '',                  'MITEGONE',
                                'MITEGONE_admin',    'MITEGONE_ProjectTraker',
                                'MITEGONE_ToDo',     'MITEGONE_ToDo',
                                'ECF',               'Extropia',
                                'Extropia_HelpDesk', 'MiteGone',
                                'Mite_HelpDesk',     'WebCT',
                                'WebCT_Internal',    '(None)',
                   ]
 ],

 status => [
             -DISPLAY_NAME       => 'Status',
             -TYPE               => 'popup_menu',
             -NAME               => 'status',
             -VALUES             => [ sort { $a <=> $b } keys %status ],
             -LABELS             => \%status,
             -INPUT_CELL_COLSPAN => 3,
 ],

);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
    qw(project_code), qw(abstract ),
    [qw(start_day start_mon start_year)], [qw(due_day due_mon due_year)],
    qw(details),           qw(priority),
    [qw(status)],          qw(estimated_man_hours),
    qw(accumulative_time), qw(comments),
);

my %ACTION_HANDLER_PLUGINS;

my @INPUT_WIDGET_DEFINITIONS = (
         -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
         -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ( $site eq "file" )
{
 @BASIC_DATASOURCE_CONFIG_PARAMS = (
                              -TYPE => 'File',
                              -FILE => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
                              -FIELD_DELIMITER            => '|',
                              -COMMENT_PREFIX             => '#',
                              -CREATE_FILE_IF_NONE_EXISTS => 1,
                              -FIELD_NAMES => \@DATASOURCE_FIELD_NAMES,
                              -KEY_FIELDS  => ['record_id'],
                              -FIELD_TYPES => {
                                                record_id => 'Autoincrement',
                                                datetime  => [
                                                      -TYPE    => "Date",
                                                      -STORAGE => 'y-m-d H:M:S',
                                                      -DISPLAY => 'y-m-d H:M:S',
                                                ],
                              },
 );
}
else
{
 @BASIC_DATASOURCE_CONFIG_PARAMS = (
                                     -TYPE        => 'DBI',
                                     -DBI_DSN     => $DBI_DSN,
                                     -TABLE       => 'todo_tb',
                                     -USERNAME    => $AUTH_MSQL_USER_NAME,
                                     -PASSWORD    => $MySQLPW,
                                     -FIELD_NAMES => \@DATASOURCE_FIELD_NAMES,
                                     -KEY_FIELDS  => ['username'],
                                     -FIELD_TYPES => {
                                                   record_id => 'Autoincrement',
                                                   datetime  => [
                                                      -TYPE    => "Date",
                                                      -STORAGE => 'y-m-d H:M:S',
                                                      -DISPLAY => 'y-m-d H:M:S',
                                                   ],
                                     },
 );

}

my @PAGE_DATASOURCE_FIELD_NAMES = (
                  qw(sitename),  qw(page_code),  qw(pageheader), qw(link_order),
                  qw(app_title), qw(page_site),  qw(menu),       qw(view_name),
                  qw(body),      qw(status),     qw(facebook),   qw(linkedin),
                  qw(news),      qw(lastupdate), qw(comments),
);
my @PAGE_DATASOURCE_CONFIG_PARAMS = (
                                  -TYPE        => 'DBI',
                                  -DBI_DSN     => $DBI_DSN,
                                  -TABLE       => $Page_tb,
                                  -USERNAME    => $AUTH_MSQL_USER_NAME,
                                  -PASSWORD    => $MySQLPW,
                                  -FIELD_NAMES => \@PAGE_DATASOURCE_FIELD_NAMES,
                                  -KEY_FIELDS  => ['username'],
                                  -FIELD_TYPES => {
                                                    record_id => 'Autoincrement'
                                  },
);

my @DATASOURCE_CONFIG_PARAMS = (
            -BASIC_DATASOURCE_CONFIG_PARAMS => \@BASIC_DATASOURCE_CONFIG_PARAMS,
            -PAGE_DATASOURCE_CONFIG_PARAMS  => \@PAGE_DATASOURCE_CONFIG_PARAMS,
            -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################
my @MAIL_CONFIG_PARAMS = ( -TYPE => 'Sendmail' );

my @EMAIL_DISPLAY_FIELDS = qw(
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
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
          -SUBJECT  => '$APP_NAME_TITLE Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
          -SUBJECT  => '$APP_NAME_TITLE Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
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
                      -TYPE     => 'File',
                      -LOG_FILE => "$APP_DATAFILES_DIRECTORY/$APP_NAME.log",
                      -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
                      -LOG_ENTRY_PREFIX => $APP_NAME . ' |'
);

sub _generateEnvVarsString
{
 my @env_values;

 my $key;
 foreach $key ( keys %ENV )
 {
  push( @env_values, "$key=" . $ENV{$key} );
 }
 return join( "\|", @env_values );
}

######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = qw(
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
  NonTableHomeView
  AdminHomeView
  AboutUsView
  LiveEdit
  CSCCSSView
  DailyWorkSheetView

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
  BeeTalk
  BMasterProcedures
  BCHPAHomeView
  BCHPAAdminHomeView
  BeeTrustView
  BCHPAByLawsView
  BCHPAContactView
  BCHPABoardView
  BCHPAMemberView
  BCHPAPolinatorsView

  EVHomeView
  AppearanceView
  ECFHomeView
  ECFSideBarHomeView
  BrewHomeView
  BrewRecipeView
  BatchLogView
  ItemsView
  PrintView
  AppToolsView
  ForageIndicatorView
  PlanningView
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
  WorkshopsView
  HostingView
  InventoryHomeView
  LtrustLeasesView
  LTrustPurchaceLeaseView
  PolicyStatmentView
  ListJoinView
  MembersView
  MentorView
  MentoringHomeView
  MailView
  NewsLetterView
  SwarmControlView
  ShantaHome
  CertificationView
  ChickensView
  CalendarView
  GrindRodBreaderHomeView
  ECFBreederProjectView
  BMasterBreederHomeView
  BMasterBreederView
  HiveManHomeView
  ReUseAblesView
  ReCyclingView
  ShantaLaptopHomeView
  ShopManagerView
  StoreView
  GPMRulesView
  LtrustHomeView
  NucView
  SiteLogView
  Resources
  WorkShopsView
  RegistrationView
  MailListView
  BotanicalNameView
  BeePastureView 
  FeedTheBeesView
  ForumulaView
  JobView
  PageView
  BuySellHomeView
  HelpDeskHomeView
  AltpowerLogHomePage
  VoltSensorDevelopment
  PowerUsageView
  SolarPowerView
  ProceduresView
  AltpowerNodeView
  SustainableView
  UrbanBeekeepingView
  UrbanFarmingView
  ModulesView
  ToDoHomeView
  ENCYHomeView PAGE = 
  MonitoringView
  ResourcesView
  HerbDetailView
  BrewLogView
  ProceduresView
);

my @ROW_COLOR_RULES = ();

my @VIEW_DISPLAY_PARAMS = (
 -ADMIN_EMAIL_DISPLAY_FIELDS            => \@ADMIN_EMAIL_DISPLAY_FIELDS,
 -APPLICATION_LOGO        => $app_logo,
 -APPLICATION_LOGO_HEIGHT => $app_logo_height,
 -APPLICATION_LOGO_WIDTH  => $app_logo_width,
 -APPLICATION_LOGO_ALT    => $app_logo_alt,
 -CUST_CODE               => $CustCode,
-DISPLAY_FIELDS          => [
  qw(
    abstract
    details
    start_date
    due_date
    status
    priority
    )
 ],
 -DOCUMENT_ROOT_URL                     => $DOCUMENT_ROOT_URL,
 -EMAIL_DISPLAY_FIELDS                  => \@EMAIL_DISPLAY_FIELDS,
 -FAVICON                 => $FAVICON || '/images/apis/favicon.ico',
 -ANI_FAVICON             => $ANI_FAVICON,
 -FAVICON_TYPE            => $FAVICON_TYPE,
 -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [
  qw(
    email
    )
 ],
 -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [
  qw(
    url
    )
 ],
 -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [
  qw(
    url
    )
 ],
 -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [
  qw(
    body
    )
 ],
 -FIELD_NAME_MAPPINGS => {
                           'project_code' => 'Project Code',
                           'abstract'     => 'Subject',
                           'details'      => 'Description',
                           'start_date'   => 'Start Date',
                           'due_date'     => 'Due Date',
                           'status'       => 'Status',
                           'priority'     => 'Priority',
 },
 -HEADER_IMAGE            => $HeaderImage || 'none',
 -HEADER_HEIGHT           => $Header_height,
 -HEADER_WIDTH            => $Header_width,
 -HEADER_ALT              => $Header_alt,
 -HOME_VIEW               => $home_view||'HomeView',
 -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
 -LINK_TARGET             => $LINK_TARGET,
 -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
 -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
 -SCRIPT_NAME             => $CGI->script_name(),
 -SELECTED_DISPLAY_FIELDS => [
  qw(
    project_code
    abstract
    start_date
    due_date
    status

    priority
    )
 ],
 -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
 -SORT_FIELDS => [
  qw(
    due_date
    abstract
    start_date
    )
 ],
 );

######################################################################
#                           DATE TIME SETUP                             #
######################################################################

my @DATETIME_CONFIG_PARAMS = ( -TYPE => 'ClassDate', );

######################################################################
#                           FILTER SETUP                             #
######################################################################

my @HTMLIZE_FILTER_CONFIG_PARAMS = (
                                     -TYPE => 'HTMLize',
                                     -CONVERT_DOUBLE_LINEBREAK_TO_P => 1,
                                     -CONVERT_LINEBREAK_TO_BR       => 1,
);

my @CHARSET_FILTER_CONFIG_PARAMS = ( -TYPE => 'CharSet' );

my @EMBED_FILTER_CONFIG_PARAMS = (
                                   -TYPE   => 'Embed',
                                   -ENABLE => 0
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
my @ACTION_HANDLER_LIST = qw(
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
 -ACTION_HANDLER_PLUGINS                 => \%ACTION_HANDLER_PLUGINS,
 -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
 -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
 -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
 -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
 -AFFILIATE_NUMBER                       => $Affiliate,
 -ALLOW_ADDITIONS_FLAG                   => 1,
 -ALLOW_MODIFICATIONS_FLAG               => 1,
 -ALLOW_DELETIONS_FLAG                   => 1,
 -ALLOW_DUPLICATE_ENTRIES                => 0,
 -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
 -APPLICATION_SUB_MENU_VIEW_NAME         => '',
 -APP_NAME                               => 'index',
 -APP_VER                                => $AppVer,
 -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
 -BASIC_DATA_VIEW_NAME                   => $BASIC_DATA_VIEW,
 -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
 -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
 -CGI_OBJECT                             => $CGI,
 -CSS_VIEW_URL                           => $CSS_VIEW_URL||'empty',
 -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
 -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
 -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
 -DATETIME_CONFIG_PARAMS                 => \@DATETIME_CONFIG_PARAMS,
 -Debug                                  => $CGI->param('debug') || 0,
 -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
 -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
 -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
 -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
 -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
 -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
 -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
 -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
 -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
 -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
 -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
 -DOMAIN_NAME                            => $HostName,
 -ENABLE_SORTING_FLAG                    => 1,
 -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
 -GLOBAL_DATAFILES_DIRECTORY             => $GLOBAL_DATAFILES_DIRECTORY,
 -GROUP                                  => $group,
 -HAS_MEMBERS                            => $HasMembers,
 -HTTP_HEADER_PARAMS                     => $HTTP_HEADER_PARAMS ,
 -HTTP_HEADER_KEYWORDS                   => $HTTP_HEADER_KEYWORDS,
 -HTTP_HEADER_DESCRIPTION                => $HTTP_HEADER_DESCRIPTION,
 -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
 -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
 -KEY_FIELD                              => 'record_id',
 -LOGOFF_VIEW_NAME                       => 'LogoffView',
 -LAST_UPDATE                            => $last_update,
 -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
 -LineStatus                             => $LineStatus,
 -LOCAL_IP                               => $LocalIp,
 -MAIL_USER                              => $mail_to_user,
 -MAIL_MEMBER                            => $mail_to_member,
 -MAIL_DISCUSSION                        => $mail_to_discussion ,
 -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
 -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
 -MOBILE                                 => $CGI->param('m') || 0,  
 -PID                                  => $pid,
 -NEWS_TB                                => $NEWS_TB,
 -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
 -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
 -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
 -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
 -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
 -MYSQLPW                                => $MySQLPW,
 -OFF_LINE                               => $OffLine,
 -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
 -PROCEDURE                              => $procedure,
 -PAGE_TOP_VIEW                          => $page_top_view,
 -PAGE_LEFT_VIEW                         => $page_left_view,
 -PROJECT                                => $project,
 -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
 -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
 -PAGE_NAME                              => $Page,
 -RECORDS_PER_PAGE_OPTS                  => [ 5, 10, 25, 50, 100 ],
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
 -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG         => $site_for_search,
 -SEND_EMAIL_ON_DELETE_FLAG              => 0,
 -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
 -SEND_EMAIL_ON_ADD_FLAG                 => 1,
 -SESSION_OBJECT                         => $SESSION,
 -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
 -SHOP                                   => $shop,
 -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
 -SITE_LAST_UPDATE                       => $site_update,
 -SITE_NAME                              => $SiteName,
 -SORT_FIELD1                            => $CGI->param('sort_field1')      || 'start_date',
 -SORT_FIELD2                            => $CGI->param('sort_field2')      || 'abstract',

#    -SORT_DIRECTION                     => $CGI->param('sort_direction') || 'ASEN',
 -SORT_DIRECTION                         => 'DESC',
 -STORE_URL                              => $StoreUrl,
 -STYLE                                  => $style,
 -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
 -TITLE                                  => $title,
 -VIEW                                   => $View,
 -VALID_VIEWS                            => \@VALID_VIEWS,
 -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
 -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
 -VIEW_LOADER                            => $VIEW_LOADER,
 -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP =
  Extropia::Core::App::DBApp->new(
                -ROOT_ACTION_HANDLER_DIRECTORY => "ActionHandler",
                -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
                -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
                -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
  )
  or die(   "Unable to construct the application object in "
          . $CGI->script_name()
          . ". Please contact the webmaster." );

#print "Content-type: text/html\n\n";
print $APP->execute();
