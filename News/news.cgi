#!/usr/bin/perl -wT
# 	$Id: news_manager.cgi,v 1.3 2002/10/28 22:21:00 shanta Exp $	

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
    qw(../Modules/Extropia/View/News
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/Organic
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/News
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Default);
    
#my @ACTION_HANDLER_SEARCH_PATH =
#    qw(Modules/ActionHandler/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::SessionManager;



my $CGI = new CGI() or
    die("Unable to construct the CGI object. " .
        ". Please contact the webmaster.");

######################################################################
#                          SITE SETUP                             #
######################################################################

my $APP_NAME                = "news_manager"; 
my $SiteName                =  $CGI->param('site') || "CSC";
my $APP_NAME_TITLE          = "CSC News Manager";
    my $homeviewname ;
    my $home_view; 
    my $BASIC_DATA_VIEW; 
    my $site_update;
    my $page_top_view;
    my $page_bottom_view;
    my $page_left_view;
#Mail settings
    my $mail_from; 
    my $mail_to;
    my $mail_replyto;
    my $CSS_VIEW_NAME;
    my $app_logo;
    my $app_logo_height;
    my $app_logo_width;
    my $app_logo_alt;
    my $IMAGE_ROOT_URL; 
    my $DOCUMENT_ROOT_URL;
    my $datamode;
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
    my $DEFAULT_CHARSET;
    my $news_tb;
    my $last_update = 'January 26, 2006';
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
    my $HasMembers = 0;

use SiteSetup;

  my $UseModPerl            = 0;
  my $SetupVariables        = new SiteSetup($UseModPerl);

   $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
   $home_view             = $SetupVariables->{-HOME_VIEW}; 
   $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
   $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
   $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
   $page_left_view        = $SetupVariables->{-PAGE_LEFT_VIEW};
   $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
   $DBI_DSN               = $SetupVariables->{-DBI_DSN};
   $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
   $MySQLPW               = $SetupVariables->{-MySQLPW};
   $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
   $news_tb               = 'csc_news_tb';
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
   $datamode              = $SetupVariables->{-DATASOURCE_TYPE}||"CSC";
   $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
   $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
   $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
   $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
  $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
     #$page_top_view = 'NewsPageTopView';

my $VIEW_LOADER = new Extropia::Core::View(\@VIEWS_SEARCH_PATH, \@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object" .
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
my $SESSION_ID = $SESSION->getId();
my $CSS_VIEW_URL;

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


if ($SiteName eq "Apis") {
use ApisSetup;
  my $SetupVariablesApis  = new  ApisSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesApis->{-AUTH_TABLE};
    $news_tb                 = 'apis_news_tb';
    $page_top_view           = $SetupVariablesApis->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesApis->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesApis->{-PAGE_LEFT_VIEW};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesApis->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesApis->{-HTTP_HEADER_DESCRIPTION};
    $homeviewname            = 'ApisHomeView';
    $home_view               = $SetupVariablesApis ->{-HOME_VIEW}; 
    $APP_DATAFILES_DIRECTORY = $SetupVariablesApis->{-APP_DATAFILES_DIRECTORY};
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
} 
 
elsif ($SiteName eq "BMaster") {
use BMasterSetup;
  my $UseModPerl = 0;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
     $HasMembers              = $SetupVariablesBMaster->{-HAS_MEMBERS};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesBMaster->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesBMaster->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesBMaster->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesBMaster->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesBMaster->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesBMaster->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesBMaster->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesBMaster->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
 #Mail settings
     $mail_from               = $SetupVariablesBMaster->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBMaster->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBMaster->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
     $news_tb                 = $SetupVariablesBMaster->{ -NEWS_TB};
}

elsif ($SiteName eq "Shanta"){
use ShantaSetup;
  my $UseModPerl = 0;
  my $SetupVariablesShanta = new ShantaSetup($UseModPerl);
    $CSS_VIEW_URL           = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesShanta->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesShanta->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesShanta->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesShanta->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesShanta->{-APP_LOGO_ALT};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesShanta->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesShanta->{-HTTP_HEADER_DESCRIPTION};
    $homeviewname            = 'HelpDeskHomeView';
    $news_tb                 = 'shanta_news_tb';
    $home_view               = $SetupVariablesShanta->{-HOME_VIEW}; 
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SITE_DISPLAY_NAME       = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
  }
elsif ($SiteName eq "CSC") {
use CSCSetup;
  my $SetupVariablesCSC       = new  CSCSetup($UseModPerl);
    $AUTH_TABLE              = $SetupVariablesCSC ->{-AUTH_TABLE};
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $page_top_view           = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CSC'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
}
elsif ($SiteName eq "Demo") {
use DEMOSetup;
  my $SetupVariablesDemo   = new  DEMOSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesDemo ->{-AUTH_TABLE};
    $HasMembers               = $SetupVariablesDemo->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesDemo->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesDemo->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesDemo->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME            = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $mail_from                = $SetupVariablesDemo->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesDemo->{-MAIL_TO};
    $page_top_view            = $SetupVariablesDemo->{-PAGE_TOP_VIEW};
    $page_bottom_view         = $SetupVariablesDemo->{-PAGE_BOTTOM_VIEW};
    $page_left_view           = $SetupVariablesDemo->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
    $homeviewname             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-LAST_UPDATE};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};

}

elsif ($SiteName eq "GrindrodBC") {
use GrindrodSetup;
  my $SetupVariablesGrindrod   = new GrindrodSetup($UseModPerl);
     $APP_NAME_TITLE          = "Grindrod";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGrindrod->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGrindrod->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGrindrod->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGrindrod->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGrindrod->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGrindrod->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGrindrod->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGrindrod->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesGrindrod->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGrindrod->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGrindrod->{-LAST_UPDATE}; 
#      $site_update            = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGrindrod->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGrindrod->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGrindrod->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGrindrod->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGrindrod->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGrindrod->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGrindrod->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGrindrod->{-FAVICON_TYPE};
} 

 elsif ($SiteName eq "USBM") {
use USBMSetup;
  my $SetupVariablesUSBM   = new USBMSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesUSBM->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesUSBM->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesUSBM->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesUSBM->{-AUTH_TABLE};
     $APP_NAME_TITLE          = $SetupVariablesUSBM->{-APP_NAME_TITLE};
     $app_logo                = $SetupVariablesUSBM->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesUSBM->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesUSBM->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesUSBM->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesUSBM->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesUSBM->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesUSBM->{-LAST_UPDATE};
     $site_update             = $SetupVariablesUSBM->{-SITE_LAST_UPDATE};
 
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
if ($datamode eq "file") {

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
    -SITE_NAME            => $SiteName,
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
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
    -LEFT_PAGE_VIEW          => $page_left_view,
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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      => $mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
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
#    -AUTH_VIEWS                  => 'CGIViews.pm',
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
    -AUTH_REGISTRATION_DH_MANAGER_PARAMS => \@AUTH_REGISTRATION_DH_MANAGER_PARAMS
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
        String
        )],

    -FIELD_MAPPINGS => {
        'subject'   => 'Subject',
        'abstract'  => 'Abstract',
        'full_text' => 'Full Text'
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
                subject
                abstract
                full_text
            )]
        ]
    ]
);

my @MODIFY_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Exists
        HTML
        String
        )],

    -FIELD_MAPPINGS => {
        'subject'   => 'Subject',
        'abstract'  => 'Abstract',
        'full_text' => 'Full Text'
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
                subject
                abstract
                full_text
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
        subject
        abstract
        sitename
        full_text
        username_of_poster
        group_of_poster
        date_time_posted
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    subject => [
        -DISPLAY_NAME => 'Subject',
        -TYPE         => 'textfield',
        -NAME         => 'subject',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    abstract => [
        -DISPLAY_NAME => 'Abstract',
        -TYPE         => 'textarea',
        -NAME         => 'abstract',
        -ROWS         => 4,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

    full_text => [
        -DISPLAY_NAME => 'Full Text',
        -TYPE         => 'textarea',
        -NAME         => 'full_text',
        -ROWS         => 12,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],
    
    
     sitename => [
        -DISPLAY_NAME => 'sitename',
        -TYPE         => 'textfield',
        -NAME         => 'sitename',
        -SIZE         => 30,
	     -VALUE        => $SiteName,
        -MAXLENGTH    => 80
    ],
);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
        sitename
        subject
        abstract
        full_text
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);

my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($datamode eq "file"){
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
	        -TABLE        => $news_tb,
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
           
my @MAIL_CONFIG_PARAMS = (     
    -TYPE         => 'Sendmail'
);

my @EMAIL_DISPLAY_FIELDS = qw(
        subject
        abstract
        full_text
);

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $SetupVariables->{-MAIL_TO_USER}||$mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $SetupVariables->{-MAIL_TO_USER}||$mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       =>$SetupVariables->{-MAIL_TO_USER}|| $mail_to,
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
    -LOG_FILE         => "$APP_DATAFILES_DIRECTORY/news.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX => 'News|'
);



sub _generateEnvVarsString {
    my @env_values;

    my $key;
    foreach $key (keys %ENV) {
        push (@env_values, "$key=" . $ENV{$key});
    }
    return join ("\|", @env_values);
    # or just
    #  return join "\|", map {"$_=$ENV{$_}"} keys %ENV;
}

######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = qw(
       ShantaCSSView
       ApisCSSView
       BCHPACSSView
    CSCCSSView
    SubTopFrameView
    AddAcknowledgementView
    AddRecordConfirmationView
    DeleteRecordConfirmationView
    DeleteAcknowledgementView
    ModifyAcknowledgementView
    ModifyRecordConfirmationView
    SessionTimeoutErrorView
    AddRecordView
    PowerSearchFormView
    NewsManagerBasicDataView
    DetailsRecordView
    ModifyRecordView
    LogoffView
    OptionsView
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
    -FAVICON                 => $FAVICON || '/images/apis/favicon.ico',
    -ANI_FAVICON             => $ANI_FAVICON,
    -FAVICON_TYPE            => $FAVICON_TYPE,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -APP_NAME                => $APP_NAME,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -HOME_VIEW               => 'PowerSearchFormView',
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        subject
        abstract
        full_text
        )],
    -FIELD_NAME_MAPPINGS     => {
        subject   => "Subject",
        abstract  => "Abstract",
        full_text => "Full Text"
        },
    -DISPLAY_FIELDS        => [qw(
        subject
        abstract
        full_text
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
        subject
        abstract
        )],
    -SORT_FIELDS             => [qw(
        subject
        abstract
        full_text
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
    Default::PerformPowerSearchAction
    Default::DisplayBasicDataViewAction
    Default::DefaultAction
);

my @ACTION_HANDLER_ACTION_PARAMS =
    (
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
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -BASIC_DATA_VIEW_NAME                   => 'NewsManagerBasicDataView',
    -CGI_OBJECT                             =>  $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
	 -Debug                                  => $CGI->param('debug')||0,
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DELETE_FORM_VIEW_NAME                  => 'NewsManagerBasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DEFAULT_SORT_FIELD1                    => 'date_time_posted',
    -DEFAULT_SORT_FIELD2                    => 'abstract',
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
    -SEND_EMAIL_ON_DELETE_FLAG              => 1,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -SIMPLE_SEARCH_BOX_VIEW_NAME            => 'SimpleSearchBoxView',
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 10,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'record_id',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'subject',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'DESC',
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -KEY_FIELD                              => 'record_id',
    -SITE_LAST_UPDATE                       => $site_update,
    -SITE_NAME               => $SiteName,
    -PAGE_TOP_VIEW           =>  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $page_left_view,
    -PAGE_BOTTOM_VIEW        =>  $page_bottom_view,
    -INPUT_WIDGET_DEFINITIONS => \@INPUT_WIDGET_DEFINITIONS,
     -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 2,
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
