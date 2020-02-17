#!/usr/bin/perl -wT
# 	$Id: procedure_tracker.cgi,v 1.7 2019/05/09 21:22:07 shanta Exp $
# 	$Id: project_tracker.cgi,v 1.7 2004/02/02 21:22:07 shanta Exp $

# Copyright (C) 1994 - 2001  eXtropia.com
#

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theuse CGI ':standard';use CGI ':standard';
use strict; use warnings;

use strict; use warnings;

# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.

use strict;

BEGIN
{
 use vars qw(@dirs);
 @dirs = qw(../Modules
   ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

my @VIEWS_SEARCH_PATH = qw(../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = qw(../HTMLTemplates/Apis
  ../HTMLTemplates/AltPower
  ../HTMLTemplates/Brew
  ../HTMLTemplates/CS
  ../HTMLTemplates/CSC
  ../HTMLTemplates/CSPS
  ../HTMLTemplates/Demo
  ../HTMLTemplates/ECF
  ../HTMLTemplates/ENCY
  ../HTMLTemplates/Forager
  ../HTMLTemplates/HE
  ../HTMLTemplates/HelpDesk
  ../HTMLTemplates/Organic
  ../HTMLTemplates/Shanta
  ../HTMLTemplates/SkyeFarm
  ../HTMLTemplates/TelMark
  ../HTMLTemplates/VitalVic
  ../HTMLTemplates/WW
  ../HTMLTemplates/Default);

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
 $CGI->param( $1, $CGI->param($_) ) if (/(.*)\.x/);
}
######################################################################
#                          PORTING SETUP                             #
######################################################################
my $SiteName          = $CGI->param('site') || "CSC";
my $APP_NAME          = "procdure_tracker";
my $SITE_DISPLAY_NAME = 'Site not added to session setup.';
my $APP_NAME_TITLE    = "Procedure Manager";
my $homeviewname;
my $home_view;
my $BASIC_DATA_VIEW;
my $page_top_view;
my $page_bottom_view;
my $page_left_view;

#Mail settings
my $mail_from;
my $mail_to;
my $mail_replyto;
my $mail_bcc;
my $CSS_VIEW_NAME;
my $app_logo;
my $app_logo_height;
my $app_logo_width;
my $app_logo_alt;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $IMAGE_ROOT_URL;
my $DOCUMENT_ROOT_URL;
my $GLOBAL_DATAFILES_DIRECTORY ;
my $TEMPLATES_CACHE_DIRECTORY;
my $APP_DATAFILES_DIRECTORY;
my $DATAFILES_DIRECTORY;
my $site_session;
my $auth;
my $site;
my $SiteLastUpdate;
my $MySQLPW;
my $LINK_TARGET;
my $HTTP_HEADER_PARAMS;
my $DBI_DSN;
my $AUTH_TABLE;
my $AUTH_MSQL_USER_NAME;
my $DEFAULT_CHARSET;
my $additonalautusernamecomments;
my $SetupVariables;
my $page_left_view;
my $TableName;
my $records;
my $StoreUrl;
my $site_update;
my $frame;
my $last_update = 'May 9, 2019';
my $DeBug       = $CGI->param('debug') || 0;
my $project     = $CGI->param('project')||'none';
my $title       = $CGI->param('title');
my $client_tb   = 'csc_client_tb';
my $Affiliate   = 001;
my $HasMembers  = 0;
my $HostName    = $ENV{'SERVER_NAME'};
my $OffLine     = 'yes';
my $shop        = 'cs';

if ($HostName eq 'computersystemconsulting.ca'||
    $HostName eq 'brew.computersystemconsulting.ca'||
    $HostName eq 'dev.computersystemconsulting.ca'||
    $HostName eq 'dev.altpower.usbm.ca'||
    $HostName eq 'dev.beemaster.ca'||
    $HostName eq 'dev.ecf.beemaster.ca'){
   $GLOBAL_DATAFILES_DIRECTORY ="/home/shanta/Datafiles";
}

if ($HostName eq 'usbm.ca' ||
    $HostName eq 'altpower.usbm.ca' ||
    $HostName eq 'brew.usbm.ca'||
    $HostName eq 'ency.usbm.ca'){
   $GLOBAL_DATAFILES_DIRECTORY ="/home/usbmca/Datafiles";
}

if ($HostName eq 'beemaster.ca' ||
    $HostName eq 'ecf.beemaster.ca' ||
    $HostName eq 'hivemanagment.beemaster.ca' ||
    $HostName eq 'anucollective.beemaster.ca' ||
    $HostName eq 'jennabee.beemaster.ca'){
   $GLOBAL_DATAFILES_DIRECTORY ="/home/beemast/Datafiles";
}


my $VIEW_LOADER =
  new Extropia::Core::View( \@VIEWS_SEARCH_PATH, \@TEMPLATES_SEARCH_PATH )
  or die(   "Unable to construct the VIEW LOADER object in "
          . $CGI->script_name()
          . " Please contact the webmaster." );

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
                         -TYPE            => 'File',
                         -MAX_MODIFY_TIME => 60 * 60,
                         -SESSION_DIR => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
                         -FATAL_TIMEOUT           => 0,
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

my $SESSION_MGR =
  Extropia::Core::SessionManager->create( @SESSION_MANAGER_CONFIG_PARAMS );

my $SESSION    = $SESSION_MGR->createSession();
my $SESSION_ID = $SESSION->getId();
my $CSS_VIEW_URL ;

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

my $username = $SESSION->getAttribute( -KEY => 'auth_username' );
my $group    = $SESSION->getAttribute( -KEY => 'auth_group' );
use SiteSetup;
my $UseModPerl = 1;
my $SetupVariables = new SiteSetup( $UseModPerl, $SiteName );
$Affiliate                  = $SetupVariables->{-AFFILIATE};
$home_view                  = 'ProjectHomeView';
$APP_NAME_TITLE             = $SetupVariables->{-APP_NAME_TITLE};
$homeviewname               = 'ProjectHomeView';
$BASIC_DATA_VIEW            = $SetupVariables->{-BASIC_DATA_VIEW};
$page_top_view              = $SetupVariables->{-PAGE_TOP_VIEW} || 'PageTopView';
$page_bottom_view           = $SetupVariables->{-PAGE_BOTTOM_VIEW};
$page_left_view             = $SetupVariables->{-page_left_view};
$AUTH_MSQL_USER_NAME        = $SetupVariables->{-AUTH_MSQL_USER_NAME};
$MySQLPW                    = $SetupVariables->{-MySQLPW};

#Mail settings
$mail_from                  = $SetupVariables->{-MAIL_FROM};
$mail_to                    = $SetupVariables->{-MAIL_TO};
$mail_replyto               = $SetupVariables->{-MAIL_REPLYTO};
$CSS_VIEW_NAME              = $SetupVariables->{-CSS_VIEW_NAME};
$app_logo                   = $SetupVariables->{-APP_LOGO};
$app_logo_height            = $SetupVariables->{-APP_LOGO_HEIGHT};
$app_logo_width             = $SetupVariables->{-APP_LOGO_WIDTH};
$app_logo_alt               = $SetupVariables->{-APP_LOGO_ALT};
$IMAGE_ROOT_URL             = $SetupVariables->{-IMAGE_ROOT_URL};
$DOCUMENT_ROOT_URL          = $SetupVariables->{-DOCUMENT_ROOT_URL};
$LINK_TARGET                = $SetupVariables->{-LINK_TARGET};
$HTTP_HEADER_PARAMS         = $SetupVariables->{-HTTP_HEADER_PARAMS};
my $HTTP_HEADER_KEYWORDS    = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
my $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
my $LocalIp                 = $SetupVariables->{-LOCAL_IP};
$site                       = $SetupVariables->{-DATASOURCE_TYPE};
$SITE_DISPLAY_NAME          = $SetupVariables->{-SITE_DISPLAY_NAME};
$GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY} || 'BLANK';
$TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY . $SetupVariables->{ -TEMPLATES_CACHE_DIRECTORY, };
$APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
$DATAFILES_DIRECTORY        = $APP_DATAFILES_DIRECTORY;
$site_session               = $DATAFILES_DIRECTORY . '/Sessions';
$auth                       = $DATAFILES_DIRECTORY . '/csc.admin.users.dat';
$TableName                  = 'procedures_tb';
$DBI_DSN                    = $SetupVariables->{-DBI_DSN};
my $LocalIp                 = $SetupVariables->{-LOCAL_IP};
$shop                       = $SetupVariables->{-SHOP};
$StoreUrl                   = $SetupVariables->{-STORE_URL};
$site_update                = $SetupVariables->{-SITE_LAST_UPDATE};
$last_update                = $SetupVariables->{-LAST_UPDATE};
$HasMembers                 = $SetupVariables->{-HAS_MEMBERS};
$CSS_VIEW_NAME              = $SetupVariables->{-CSS_VIEW_NAME};
$CSS_VIEW_URL               = $SetupVariables->{-CSS_VIEW_NAME};

my $modify       = '1';
my $delete       = '1';
my $add          = '1';
my $group_search = '1';

if ( $username eq "Shanta" )
{
 $modify       = '1';
 $delete       = '1';
 $group_search = '0';
 $add          = '1';
}

if ( $CGI->param('embed') )
{
 $page_top_view    = "EmbedPageTopView";
 $records          = 30;
 $page_bottom_view = '';
}
if ( $CGI->param('frame') )
{
 $frame = "1";
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
if ( $site eq "file" )
{

 @AUTH_USER_DATASOURCE_PARAMS = (
                         -TYPE                       => 'File',
                         -FIELD_DELIMITER            => '|',
                         -CREATE_FILE_IF_NONE_EXISTS => 1,
                         -FIELD_NAMES => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
                         -FILE => "$APP_DATAFILES_DIRECTORY/$APP_NAME.users.dat"
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
      -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
      -SCRIPT_NAME             => $CGI->script_name(),
      -PAGE_TOP_VIEW           => $CGI->param('page_top_view') || $page_top_view,
      -PAGE_BOTTOM_VIEW        => $CGI->param('page_bottom_view') || $page_bottom_view,
      -page_left_view          => $CGI->param('page_left_view')   || $page_left_view,
      -LINK_TARGET             => $LINK_TARGET
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

my @MAIL_PARAMS = ( -TYPE => 'Sendmail', );

my @USER_MAIL_SEND_PARAMS = (
                             -FROM    => $mail_from,
                             -TO      => $mail_to,
                             -SUBJECT => $APP_NAME_TITLE . ' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
                      -FROM    => $mail_from,
                      -TO      => $mail_to,
                      -SUBJECT => $APP_NAME_TITLE . ' Registration Notification'
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
 -DATAHANDLERS => [
  qw(
    Email
    Exists
    HTML
    String
    )
 ],

 -FIELD_MAPPINGS => {
                      'status'              => 'Status',
                      'project_name'        => 'Project Name',
                      'project_size'        => 'Project Size',
                      'estimated_man_hours' => 'Estimated Man Hours',
                      'developer_name'      => 'Developer Name',
                      'client_name'         => 'Client Name',
                      'comments'            => 'Comments'
 },

 -RULES => [
  -ESCAPE_HTML_TAGS => [
   -FIELDS => [
    qw(
      *
      )
   ],
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
      status
      project_name
      project_size
      estimated_man_hours
      developer_name
      client_name
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
                      'status'              => 'Status',
                      'project_name'        => 'procedure Name',
                      'project_size'        => 'Project Size',
                      'estimated_man_hours' => 'Estimated Man Hours',
                      'developer_name'      => 'Developer Name',
                      'client_name'         => 'Client Name',
                      'comments'            => 'Comments'
 },

 -RULES => [
  -ESCAPE_HTML_TAGS => [
   -FIELDS => [
    qw(
      *
      )
   ],
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
      status
      project_name
      project_size
      estimated_man_hours
      developer_name
      client_name
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
  status
  project_code
  project_name
  project_size
  estimated_man_hours
  developer_name
  client_name
  sitename
  comments
  username_of_poster
  group_of_poster
  date_time_posted
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
 status => [
             -DISPLAY_NAME => 'Status',
             -TYPE         => 'popup_menu',
             -NAME         => 'status',
             -VALUES => [qw(Requested Public In-Process Testing Delivered)]
 ],

 project_name => [
                   -DISPLAY_NAME => 'Procedure Name',
                   -TYPE         => 'textfield',
                   -NAME         => 'project_name',
                   -SIZE         => 30,
                   -MAXLENGTH    => 80
 ],

 project_code => [
                   -DISPLAY_NAME => 'ProView name Code',
                   -TYPE         => 'textfield',
                   -NAME         => 'project_code',
                   -SIZE         => 30,
                   -MAXLENGTH    => 80
 ],

 project_size => [
                   -DISPLAY_NAME => 'Project Size',
                   -TYPE         => 'popup_menu',
                   -NAME         => 'project_size',
                   -VALUES       => [ 'Large', 'Med', 'Small', '' ]
 ],

 estimated_man_hours => [
                          -DISPLAY_NAME => 'Est. Man Hours',
                          -TYPE         => 'textfield',
                          -NAME         => 'estimated_man_hours',
                          -SIZE         => 30,
                          -MAXLENGTH    => 80
 ],

 developer_name => [
                     -DISPLAY_NAME => 'Developer',
                     -TYPE         => 'textfield',
                     -NAME         => 'developer_name',
                     -VALUE        => $username,
                     -SIZE         => 30,
                     -MAXLENGTH    => 80
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
 ],

#    sitename => [
#        -DISPLAY_NAME => 'Site',
#        -TYPE         => 'popup_menu',
#       -NAME         => 'sitename',
#       -VALUES       => [qw(All Alegro AltPower Apis BCHPA BeeMaster CSC CS DarmaFarms ECF ENCY Forager Fly 	Marts Organic RV Shanta Skye TelMark USBM VitalVic )]
#   ],
);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
  status
  project_code
  project_name
  project_size
  estimated_man_hours
  developer_name
  sitename
  client_name
  comments
);

my @INPUT_WIDGET_DEFINITIONS = (
         -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
         -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ( $site eq "file" )
{
 @BASIC_DATASOURCE_CONFIG_PARAMS = (
                             -TYPE => 'File',
                             -FILE => "$APP_DATAFILES_DIRECTORY/$TableName.dat",
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
                                     -TYPE    => 'DBI',
                                     -DBI_DSN => $DBI_DSN,
                                     -TABLE   => $TableName || 'csc_project_tb',
                                     -USERNAME    => $AUTH_MSQL_USER_NAME,
                                     -PASSWORD    => $MySQLPW,
                                     -FIELD_NAMES => \@DATASOURCE_FIELD_NAMES,
                                     -KEY_FIELDS  => ['project_code'],
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
my @DROPLIST_DATASOURCE_FIELD_NAMES = qw(
  record_id
  status
  category
  sitename
  app_name
  list_name
  display_value
  client_name
  comments
  username_of_poster
  group_of_poster
  date_time_posted
);

my @DROPLIST_DATASOURCE_CONFIG_PARAMS = (
                              -TYPE        => 'DBI',
                              -DBI_DSN     => $DBI_DSN,
                              -TABLE       => 'csc_droplist_tb',
                              -USERNAME    => $AUTH_MSQL_USER_NAME,
                              -PASSWORD    => $MySQLPW,
                              -FIELD_NAMES => \@DROPLIST_DATASOURCE_FIELD_NAMES,
                              -KEY_FIELDS  => ['project_code'],
                              -FIELD_TYPES => {
                                                record_id => 'Autoincrement',
                                                datetime  => [
                                                      -TYPE    => "Date",
                                                      -STORAGE => 'y-m-d H:M:S',
                                                      -DISPLAY => 'y-m-d H:M:S',
                                                ],
                              },
);

my @CLIENT_DATASOURCE_FIELD_NAMES = qw(
  category
  record_id
  sitename
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

my @CLIENT_DATASOURCE_CONFIG_PARAMS = (
                                -TYPE        => 'DBI',
                                -DBI_DSN     => $DBI_DSN,
                                -TABLE       => $client_tb,
                                -USERNAME    => $AUTH_MSQL_USER_NAME,
                                -PASSWORD    => $MySQLPW,
                                -FIELD_NAMES => \@CLIENT_DATASOURCE_FIELD_NAMES,
                                -KEY_FIELDS  => ['username'],
                                -FIELD_TYPES => {
                                                  record_id => 'Autoincrement'
                                },
);

my @DATASOURCE_CONFIG_PARAMS = (
      -BASIC_DATASOURCE_CONFIG_PARAMS    => \@BASIC_DATASOURCE_CONFIG_PARAMS,
      -CLIENT_DATASOURCE_CONFIG_PARAMS   => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
      -DROPLIST_DATASOURCE_CONFIG_PARAMS => \@DROPLIST_DATASOURCE_CONFIG_PARAMS,
      -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################

my @MAIL_CONFIG_PARAMS = ( -TYPE => 'Sendmail' );

my @EMAIL_DISPLAY_FIELDS = qw(
  status
  project_code
  project_name
  project_size
  estimated_man_hours
  developer_name
  client_name
  comments
);

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
          -SUBJECT  => $APP_NAME_TITLE . ' Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
          -SUBJECT  => $APP_NAME_TITLE . ' Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
          -FROM => $SESSION->getAttribute( -KEY => 'auth_email' ) || $mail_from,
          -TO => $mail_to,
          -REPLY_TO => $mail_replyto,
          -SUBJECT  => $APP_NAME_TITLE . ' Modification'
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
                      -LOG_ENTRY_PREFIX => '$APP_NAME_TITLE|'
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
  CSPSCSSView
  CSCCSSView
  VitalVicCSSView
  ApisCSSView
  ECFCSSView
  ENCYCSSView
  BCHPACSSView
  AddAcknowledgementView
  AddRecordConfirmationView
  DeleteRecordConfirmationView
  DeleteAcknowledgementView
  ModifyAcknowledgementView
  ModifyRecordConfirmationView
  SessionTimeoutErrorView
  AddRecordView
  PowerSearchFormView
  ProjectsView
  BasicDataView
  DetailsRecordView
  ModifyRecordView
  LogoffView
  OptionsView
  InventoryProjectionView
  ProductView
  ProjectHomeView
  MailView
);

my @ROW_COLOR_RULES = (
                        { 'status' => [qw(Requested 99CC99)] },
                        { 'status' => [qw(In-Process CC9999)] },
                        { 'status' => [qw(Delivered CC9999)] }
);

my @FIELD_COLOR_RULES = (
                          { 'project_size' => [qw(Large BLUE)] },
                          { 'project_size' => [qw(Small ORANGE)] }
);

my @VIEW_DISPLAY_PARAMS = (
 -ROW_COLOR_RULES                       => \@ROW_COLOR_RULES,
 -FIELD_COLOR_RULES                     => \@FIELD_COLOR_RULES,
 -APPLICATION_LOGO                      => $app_logo,
 -APPLICATION_LOGO_HEIGHT               => $app_logo_height,
 -APPLICATION_LOGO_WIDTH                => $app_logo_width,
 -APPLICATION_LOGO_ALT                  => $app_logo_alt,
 -FAVICON                               => $FAVICON,
 -ANI_FAVICON                           => $ANI_FAVICON,
 -FAVICON_TYPE                          => $FAVICON_TYPE,
 -DOCUMENT_ROOT_URL                     => $DOCUMENT_ROOT_URL,
 -IMAGE_ROOT_URL                        => $IMAGE_ROOT_URL,
 -HTTP_HEADER_PARAMS                    => $HTTP_HEADER_PARAMS,
 -LINK_TARGET                           => $LINK_TARGET,
 -APP_NAME                              => $APP_NAME,
 -SCRIPT_DISPLAY_NAME                   => $APP_NAME_TITLE,
 -SITE_DISPLAY_NAME                     => $SITE_DISPLAY_NAME,
 -SCRIPT_NAME                           => $CGI->script_name(),
 -EMAIL_DISPLAY_FIELDS                  => \@EMAIL_DISPLAY_FIELDS,
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
 -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [
  qw(
    body
    )
 ],
 -HOME_VIEW           => $homeviewname,
 -FIELD_NAME_MAPPINGS => {
                           status              => 'Status',
                           project_code        => 'Project Code',
                           sitename            => 'Site',
                           project_name        => 'Project Name',
                           project_size        => 'Project Size',
                           estimated_man_hours => 'Est. Man Hours',
                           developer_name      => 'Developer',
                           client_name         => 'Client',
                           comments            => 'Comments'
 },
 -DISPLAY_FIELDS => [
  qw(
    sitename
    project_code
    project_name
    project_size
    estimated_man_hours
    status
    developer_name
    client_name
    comments
    )
 ],
 -SORT_FIELDS => [
  qw(
    status
    projectcode
    project_name
    project_size
    estimated_man_hours
    developer_name
    client_name
    comments
    )
 ],
 -SELECTED_DISPLAY_FIELDS => [
  qw(
    sitename
    project_code
    project_name
    developer_name
    client_name
    status
    )
 ],
);

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
                                   -ENABLE => $CGI->param('embed') || 0
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
  CSC::PopulateInputWidgetDefinitionListWithClientWidgetAction
  CSC::PopulateInputWidgetDefinitionListWithDropListSiteNameWidgetAction

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
    -ACTION_HANDLER_LIST                  => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME        => 'AddAcknowledgementView',
    -AFFILIATE_NUMBER                     => $Affiliate,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME     => 'DeleteAcknowledgementView',
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME     => 'ModifyAcknowledgementView',
    -POWER_SEARCH_VIEW_NAME               => 'PowerSearchFormView',
    -ADD_RECORD_CONFIRMATION_VIEW_NAME    => 'AddRecordConfirmationView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME => 'ModifyRecordConfirmationView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME => 'DeleteRecordConfirmationView',
    -ALLOW_ADDITIONS_FLAG                 => 1,
    -ALLOW_DELETIONS_FLAG                 => 1,
    -ALLOW_MODIFICATIONS_FLAG             => 1,
    -ALLOW_DUPLICATE_ENTRIES              => 0,
    -ADD_EMAIL_BODY_VIEW                  => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                   => 'AddRecordView',
    -AUTH_MANAGER_CONFIG_PARAMS           => \@AUTH_MANAGER_CONFIG_PARAMS,
    -APPLICATION_SUB_MENU_VIEW_NAME       => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME               => 'OptionsView',
    -BASIC_DATA_VIEW_NAME                 => 'ProjectHomeView',
    -CGI_OBJECT                           => $CGI,
    -CSS_VIEW_URL                         => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                        => $CSS_VIEW_NAME,
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS           => \@DATASOURCE_CONFIG_PARAMS,
    -DEBUG                              => $DeBug,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 0,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 0,
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DEFAULT_SORT_FIELD1                    => 'project_code',
    -DEFAULT_SORT_FIELD2                    => 'project_name',
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOCAL_IP                               => $LocalIp,
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => $group_search,
    -SEND_EMAIL_ON_DELETE_FLAG                        => $delete,
    -SEND_EMAIL_ON_MODIFY_FLAG                        => $modify,
    -SEND_EMAIL_ON_ADD_FLAG                           => $add,
    -SESSION_OBJECT                                   => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME   => 'SessionTimeoutErrorView',
    -SIMPLE_SEARCH_BOX_VIEW_NAME => 'SimpleSearchBoxView',
    -TITAL                       => $title,
    -VIEW_FILTERS_CONFIG_PARAMS  => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS         => \@VIEW_DISPLAY_PARAMS,
    -TEMPLATES_CACHE_DIRECTORY   => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                 => \@VALID_VIEWS,
    -VIEW_LOADER                 => $VIEW_LOADER,
    -RECORDS_PER_PAGE_OPTS       => [ 5, 10, 25, 50, 100 ],
    -MAX_RECORDS_PER_PAGE => $CGI->param('records_per_page') || $records || 500,
    -SORT_FIELD1    => $CGI->param('sort_field1')    || 'project_code',
    -SORT_FIELD2    => $CGI->param('sort_field2')    || 'status',
    -SORT_DIRECTION => $CGI->param('sort_direction') || 'ASC',
    -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string')    || "",
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
    -KEY_FIELD            => 'record_id',
    -SITE_NAME            => $SiteName,
    -PROJECT              => $project,
    -PAGE_TOP_VIEW    => $CGI->param('page_top_view')    || $page_top_view,
    -PAGE_BOTTOM_VIEW => $CGI->param('page_bottom_view') || $page_bottom_view,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN => 2,
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = new Extropia::Core::App::DBApp(
                -ROOT_ACTION_HANDLER_DIRECTORY => "../ActionHandler",
                -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
                -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
                -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
  )
  or die(   "Unable to construct the application object in "
          . $CGI->script_name()
          . ". Please contact the webmaster." );

print $APP->execute();
