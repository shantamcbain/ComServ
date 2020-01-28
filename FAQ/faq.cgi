#!/usr/bin/perl -wT
# 	$Id: faq.cgi,v 1.2 2014/03/17 06:42:22 shanta Exp shanta $	

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
          # The following is only of interest to mod_perl, PerlEx,
          # and other Perl acceleration users
unshift @INC, @dirs if $ENV{MOD_PERL};


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/FAQ
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/FAQ
       ../HTMLTemplates/Apis
       ../HTMLTemplates/BCHPA
       ../HTMLTemplates/Brew
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Fly
       ../HTMLTemplates/CS
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Extropia
       ../HTMLTemplates/Forager
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/VitalVic
       ../HTMLTemplates/FAQ/SSI
       ../HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");

# turn the autoescaping off here
$CGI->autoEscape(undef);

my $VIEW_LOADER = new Extropia::Core::View
     (\@VIEWS_SEARCH_PATH, \@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        ". Please contact the webmaster.");


foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x/);
}
my $APP_NAME = "faq";
my $APP_NAME_TITLE = " FAQ";
my $SiteName =  $CGI->param('site') || "Grindrod";

   my $homeviewname ;
    my $home_view; 
    my $BASIC_DATA_VIEW; 
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
    my $site;
    my $GLOBAL_DATAFILES_DIRECTORY;
    my $TEMPLATES_CACHE_DIRECTORY;
    my $APP_DATAFILES_DIRECTORY;
    my $DATAFILES_DIRECTORY;
    my $site_session;
    my $auth;
    my $MySQLPW;\
    my $AUTH_TABLE;
    my $HTTP_HEADER_PARAMS;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $last_update;
    my $site_update;
    my $SITE_DISPLAY_NAME = 'No display name defined for this site.';
    my $FAVICON;
    my $ANI_FAVICON;
my $FAVICON_TYPE;
my $Affiliate = 001;
    my $HasMembers = 0;

use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $homeviewname          = 'HelpDeskHomeView';
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view           = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariables->{-LEFT_PAGE_VIEW};
    my $DBI_DSN              = $SetupVariables->{-DBI_DSN};
    my $AUTH_MSQL_USER_NAME  = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $MySQLPW                 = $SetupVariables->{-MySQLPW};
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
    $FAVICON                = $SetupVariables->{-FAVICON};
    $ANI_FAVICON            = $SetupVariables->{-ANI_FAVICON};
    $FAVICON_TYPE          = $SetupVariables->{-FAVICON_TYPE};
    $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    my $TableName          = 'csc_faq_tb';
    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};

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
my $CSS_VIEW_URL = $CGI->script_name(). "?display_css_view=on&session_id=$SESSION_ID";

if ($CGI->param('site')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'SiteName') ){
      $SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $CGI->param('site')) ;
       $SiteName = $CGI->param('site');
    }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE =>  $SiteName );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'SiteName')) {
   $SiteName = $SESSION ->getAttribute(-KEY => 'SiteName');
  }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE =>  $SiteName );
      }
}

my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');



if ($SiteName eq "Apis") {
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
    $APP_NAME                = "apis";
    $APP_NAME_TITLE          = "Apis FAQ";
    $homeviewname            = 'ApisHomeView';
    $home_view               = $SetupVariablesApis ->{-HOME_VIEW}; 
    $TableName               = 'apis_faq_tb';
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
}  
elsif ($SiteName eq "AltPower") {
use AltPowerSetup;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
     $APP_NAME_TITLE          = $SetupVariablesAltPower->{-APP_NAME_TITLE}||"index";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesAltPower->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesAltPower->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesAltPower->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesAltPower->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesAltPower->{-AUTH_TABLE};
     $Affiliate               = $SetupVariablesAltPower->{-AFFILIATE};
     $app_logo                = $SetupVariablesAltPower->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesAltPower->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesAltPower->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesAltPower->{-APP_LOGO_ALT};
      $home_view               = $SetupVariablesAltPower->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesAltPower->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesAltPower->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesAltPower->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesAltPower->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesAltPower->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesAltPower->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesAltPower->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesAltPower->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesAltPower->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesAltPower->{-FAVICON_TYPE};
}

{-HAS_MEMBERS};
 
elsif ($SiteName eq "BMaster" or
       $SiteName eq "BMasterDev" ) {
use BMasterSetup;
  my $UseModPerl = 0;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
     $APP_NAME_TITLE          = "Beemaster.ca ";
     $HasMembers               = $SetupVariablesBMaster->{-HAS_MEMBERS};
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
    $mail_from                = $SetupVariablesBMaster->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesBMaster->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
    $FAVICON                  = '/images/apis/favicon.ico'||$SetupVariablesBMaster->{-FAVICON}||'/images/apis/favicon.ico';
    $ANI_FAVICON              = $SetupVariablesBMaster->{-ANI_FAVICON};
    $page_top_view            = $SetupVariablesBMaster->{-PAGE_TOP_VIEW};
    $TableName              = 'apis_faq_tb';
}
elsif ($SiteName eq "BeeSafe") {
use BeeSafeSetup;
  my $SetupVariablesBeeSafe   = new BeeSafeSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesBeeSafe->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesBeeSafe->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesBeeSafe->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesBeeSafe->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesBeeSafe->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesBeeSafe->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesBeeSafe->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesBeeSafe->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesBeeSafe->{-APP_LOGO_ALT};
     $home_view            = 'HomeView'||$SetupVariablesBeeSafe->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBeeSafe->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBeeSafe->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBeeSafe->{-LAST_UPDATE}; 
#Mail settings
     $mail_from               = $SetupVariablesBeeSafe->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBeeSafe->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBeeSafe->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesBeeSafe->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesBeeSafe->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesBeeSafe->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBeeSafe->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesBeeSafe->{-FAVICON_TYPE};
}
elsif($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk") {
use CSSetup;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
    $APP_NAME_TITLE        = "Country Stores Client.";
    $home_view          = $SetupVariablesCS->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesCS->{-HOME_VIEW}; 
  $page_top_view            = $SetupVariablesCS->{-PAGE_TOP_VIEW};
  $page_bottom_view         = $SetupVariablesCS->{-PAGE_BOTTOM_VIEW};
  $page_left_view           = $SetupVariablesCS->{-LEFT_PAGE_VIEW};
#  $home_view             = $SetupVariablesCS->{-HOME_VIEW_NAME};
  $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
  $last_update              = $SetupVariablesCS->{-LAST_UPDATE}; 
  $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
  $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
  $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
  $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
  $FAVICON                  = $SetupVariablesCS>{-FAVICON};
  $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
  $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};
  $CSS_VIEW_URL             = $SetupVariablesCS->{-CSS_VIEW_NAME};
#    $left_page_view = 'CSCLeftPageView';
}

elsif ($SiteName eq "Demo") {
use DEMOSetup;
  my $SetupVariablesDemo   = new  DEMOSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesDemo ->{-AUTH_TABLE};
    $APP_NAME_TITLE           = "Computer System Consulting.ca Demo Application";
    $HasMembers               = $SetupVariablesDemo->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesDemo->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesDemo->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesDemo->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME            = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $page_top_view            = $SetupVariablesDemo->{-PAGE_TOP_VIEW};
    $page_bottom_view         = $SetupVariablesDemo->{-PAGE_BOTTOM_VIEW};
    $page_left_view           = $SetupVariablesDemo->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
    $homeviewname             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-LAST_UPDATE};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};

}

elsif ($SiteName eq "Organic") {
use OrganicSetup;
  my $SetupVariablesOrganic  = new  OrganicSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesOrganic->{-AUTH_TABLE};
    $page_top_view           = $SetupVariablesOrganic->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesOrganic->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesOrganic->{-PAGE_LEFT_VIEW};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesOrganic->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesOrganic->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $homeviewname            = 'ApisHomeView';
    $home_view               = $SetupVariablesOrganic ->{-HOME_VIEW}; 
    $TableName              = 'organcic_faq_tb';
    $SITE_DISPLAY_NAME      = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
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
elsif ($SiteName eq "GPMarket") {
use GPMSetup;
  my $SetupVariablesGRMarket   = new GPMSetup($UseModPerl);
     $APP_NAME_TITLE          = "Sustainable";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGRMarket->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGRMarket->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGRMarket->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGRMarket->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGRMarket->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGRMarket->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGRMarket->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGRMarket->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGRMarket->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesGRMarket->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGRMarket->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGRMarket->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGRMarket->{-LAST_UPDATE}; 
 #     $site_update            = $SetupVariablesGRMarket->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGRMarket->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGRMarket->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGRMarket->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGRMarket->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGRMarket->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGRMarket->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGRMarket->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGRMarket->{-FAVICON_TYPE};
} 
 
elsif ($SiteName eq "GRA") {
use GRASetup;
  my $SetupVariablesGRA   = new GRASetup($UseModPerl);
     $APP_NAME_TITLE          = "Grindrod Recreation  Assosiation";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGRA->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGRA->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGRA->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGRA->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGRA->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGRA->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGRA->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGRA->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGRA->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesGRA->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGRA->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGRA->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGRA->{-LAST_UPDATE}; 
#      $site_update            = $SetupVariablesGRA->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGRA->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGRA->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGRA->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGRA->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGRA->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGRA->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGRA->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGRA->{-FAVICON_TYPE};
} 
elsif ($SiteName eq "GrindrodProject") {
use GRProjectSetup;
  my $SetupVariablesGRProject   = new GRProjectSetup($UseModPerl);
     $APP_NAME_TITLE          = "Sustainable";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGRProject->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGRProject->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGRProject->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGRProject->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGRProject->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGRProject->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGRProject->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGRProject->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGRProject->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesGRProject->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGRProject->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGRProject->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGRProject->{-LAST_UPDATE}; 
#      $site_update            = $SetupVariablesGRProject->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGRProject->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGRProject->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGRProject->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGRProject->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGRProject->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGRProject->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGRProject->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGRProject->{-FAVICON_TYPE};
} 

elsif ($SiteName eq "Noop") {

use NoopSetup;
  my $UseModPerl = 0;
  my $SetupVariablesNoop   = new NoopSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesNoop->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesNoop->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesNoop->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesNoop->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesNoop->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesNoop->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesNoop->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesNoop->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesNoop->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesNoop->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesNoop->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesNoop->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic'; 
     $TableName               = 'organcic_faq_tb';
     $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "ECF") {
use ECFSetup;
  my $SetupVariablesECF    = new  ECFSetup($UseModPerl);
    $APP_NAME_TITLE          = "ECF FAQ";
    $CSS_VIEW_NAME         = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesECF->{-APP_LOGO_ALT};
    $homeviewname          = $SetupVariablesECF->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesECF->{-HOME_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to               = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS    = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.'/ECF';
    $TableName              = 'apis_faq_tb';
    $SITE_DISPLAY_NAME      = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
    $homeviewname          = 'BrewHomeView';
    $home_view             = $SetupVariablesBrew->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariablesBrew->{-BASIC_DATA_VIEW};
    $page_bottom_view      = $SetupVariablesBrew->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBrew->{-LEFT_PAGE_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesBrew->{-MAIL_FROM}; 
    $mail_to               = $SetupVariablesBrew->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBrew->{-MAIL_REPLYTO};
    $CSS_VIEW_URL          = $SetupVariablesBrew->{-CSS_VIEW_NAME}||'blank';
    $app_logo              = $SetupVariablesBrew->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesBrew->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesBrew->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesBrew->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL        = $SetupVariablesBrew->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL     = $SetupVariablesBrew->{-DOCUMENT_ROOT_URL};
    my $LINK_TARGET        = $SetupVariablesBrew->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariablesBrew->{-HTTP_HEADER_PARAMS};
    my $DEFAULT_CHARSET    = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $AUTH_TABLE            = $SetupVariablesBrew->{-AUTH_TABLE};
    $DEFAULT_CHARSET       = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $SITE_DISPLAY_NAME     = $SetupVariablesBrew->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "CSC" or
       $SiteName eq "CSCDev"){
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC   = new CSCSetup($UseModPerl);
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $AUTH_TABLE               = $SetupVariablesCSC->{-AUTH_TABLE};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL             = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME      = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
}
  elsif ($SiteName eq "SQL_Ledger"){
use SQLSetup;
  my $UseModPerl = 0;
  my $SetupVariablesSQL   = new SQLSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesSQL->{-AUTH_TABLE};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesSQL->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesSQL->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesSQL->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL             = $SetupVariablesSQL->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesSQL->{-SITE_DISPLAY_NAME};
 }
  
elsif ($SiteName eq "eXtropia") {
use eXtropiaSetup;
  my $UseModPerl = 0;
  my $SetupVariableseXtropia   = new eXtropiaSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariableseXtropia->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariableseXtropia->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariableseXtropia->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariableseXtropia->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariableseXtropia->{-CSS_VIEW_NAME};
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
 elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $SetupVariablesENCY    = new  ENCYSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
 }
 elsif ($SiteName eq "Fly") {
use FlySetup;
  my $SetupVariablesFly    = new  FlySetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesFly->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesFly->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesFly->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesFly->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesFly->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesFly->{-APP_LOGO_ALT};
    $homeviewname          = $SetupVariablesFly->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesFly->{-HOME_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesFly->{-MAIL_FROM};
    $mail_to               = $SetupVariablesFly->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesFly->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS    = $SetupVariablesFly->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariablesFly->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesFly->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesFly->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME      = $SetupVariablesFly->{-SITE_DISPLAY_NAME};
}
elsif ($SiteName eq "TelMark") {
use TelMarkSetup;
  my $UseModPerl = 0;
  my $SetupVariablesTelMark   = new TelMarkSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesTelMark->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesTelMark->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesTelMark->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesTelMark->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesTelMark->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesTelMark->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesTelMark->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesTelMark->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesTelMark->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesTelMark->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesTelMark->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesTelMark->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "VitalVic") {
use VitalVicSetup;
  my $SetupVariablesVitalVic     = new  VitalVicSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesVitalVic->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesVitalVic->{-AUTH_TABLE};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesVitalVic->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesVitalVic->{-HTTP_HEADER_DESCRIPTION};
    $APP_NAME                = "vitavic";
    $mail_to                 = $SetupVariablesVitalVic->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesVitalVic->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/VitalVic'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesVitalVic->{-SITE_DISPLAY_NAME};
}
elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $UseModPerl = 0;
  my $SetupVariablesENCY   = new ENCYSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesENCY->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesENCY->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariablesENCY->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesENCY->{-HTTP_HEADER_DESCRIPTION};
     $mail_from               = $SetupVariablesENCY->{-MAIL_FROM}; 
     $mail_to                 = $SetupVariablesENCY->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesENCY->{-MAIL_REPLYTO};
     $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesENCY->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesENCY->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesENCY->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesENCY->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesENCY->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesENCY->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesENCY->{-HOME_VIEW};
     $SITE_DISPLAY_NAME       = $SetupVariablesENCY->{-SITE_DISPLAY_NAME};
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
        -TABLE        =>  $AUTH_TABLE ,
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
    -HTTP_HEADER_PARAMS      => [-EXPIRES => '-1d'],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => '_self',
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -LEFT_PAGE_VIEW          => $page_left_view,
    -PAGE_LEFT_VIEW          => $page_left_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view
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
    -FROM     => $CGI->param('email')||$mail_from,
    -SUBJECT => 'Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM     => $CGI->param('email')||$mail_from,
    -TO      => $mail_to ,
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
#                      DATASOURCE SETUP                              #
######################################################################

my @DATASOURCE_FIELD_NAMES = qw(
        record_id
        category
        question
        answer
        sitename
        username_of_poster
        date_time_posted
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    category => [
        -DISPLAY_NAME => 'Category',
        -TYPE         => 'popup_menu',
        -NAME         => 'category',
        -VALUES  => [qw(
            		beebreeding
            		beekeeping
            		disease
            		honey
                        mitegone
                        wintering     
                    )],
        -LABELS => {
	    'beebreeding'       => 'Bee breeding',
	    'beekeeping'        => 'General Bee keeping',
	    'disease' 	        => 'Disease and Pest',
	    'honey'             => 'Honey',
            'mitegone' 	        => 'MiteGone ',
	    'wintering'         => 'Wintering',
        },
         -INPUT_CELL_COLSPAN => 2,
    ],

    question => [
        -DISPLAY_NAME => 'Question',
        -TYPE         => 'textarea',
        -NAME         => 'question',
        -ROWS         => 2,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL',
        -INPUT_CELL_COLSPAN => 2,
    ],

    answer => [
        -DISPLAY_NAME => 'Answer',
        -TYPE         => 'textarea',
        -NAME         => 'answer',
        -ROWS         => 20,
        -COLS         => 50,
        -WRAP         => 'VIRTUAL',
        -INPUT_CELL_COLSPAN => 2,
    ]
);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = qw(
        category
        question
        answer
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);


my @BASIC_DATASOURCE_CONFIG_PARAMS = ( 
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        =>  $TableName,
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

    

my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = qw(
		     ApisCSSView
		     BCHPACSSView
		     ECFCSSView
		     OrganicCSSView
		     CSSView
		     BasicFAQView
		     BasicDataView
		     DetailsRecordView
    
		     meta_tags
		     style_sheet_basic
    
		     navigation_template_top
		     freesupportnav
		     page_header_with_search_top
		     page_header_with_search_bottom
    
		     navigation_template_bottom
		     SearchView
		     ContactView
           PrivacyView
           GrowersView
           MembersView
           MissionView
           AltPowerProductsView
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
	 -FLAVICON                       => '/images/apis/favicon.ico',
	 -ANI_FLAVICON                   => $ANI_FAVICON,
 	 -FAVICON_TYPE                   => $FAVICON_TYPE,
    -HTTP_HEADER_PARAMS      => [-EXPIRES => '-1d'],
    -LINK_TARGET             => '_self',
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       =>  $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -HOME_VIEW               => 'BasicFAQView',
    -FIELD_NAME_MAPPINGS     => {
        category    => "Category",
        question    => "Question",
        answer      => "Answer"
        },
    -DISPLAY_FIELDS        => [qw(
        category
        question
        answer
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
        category
        question
        )],
    -SORT_FIELDS             => [qw(
        category
        question
        answer
        )],
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
    	question
    	answer
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
    -ENABLE          => $CGI->param('embed') || 0
);

my @VIEW_FILTERS_CONFIG_PARAMS = (
     \@HTMLIZE_FILTER_CONFIG_PARAMS,
     \@CHARSET_FILTER_CONFIG_PARAMS,
     \@EMBED_FILTER_CONFIG_PARAMS
);


######################################################################
#                      ACTION/WORKFLOW SETUP                         #
######################################################################
 #   FAQ::DisplayFAQDetailsRecordViewAction

my @ACTION_HANDLER_LIST = qw(
    Default::DisplayCSSViewAction
    Default::DownloadFileAction

   Default::DisplayDetailsRecordViewAction
     FAQ::DisplayFAQBasicDataViewAction
    FAQ::DisplaySearchBasicDataViewAction

   
    Default::DefaultAction
);

my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -BASIC_DATA_VIEW_NAME                   => 'BasicFAQView',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => "CSSView",
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DEFAULT_SORT_FIELD1                    => 'date_time_posted',
    -DEFAULT_SORT_FIELD2                    => 'question',
    -DEFAULT_VIEW_NAME                      => 'BasicDataView',
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -SIMPLE_SEARCH_BOX_VIEW_NAME            => 'SimpleSearchBoxView',
    -SORT_DIRECTION                         => 'DESC',
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 3,
    -DOCUMENT_ROOT_URL                      => $DOCUMENT_ROOT_URL,
    -IMAGE_ROOT_URL                         => $IMAGE_ROOT_URL,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'category',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'fname',
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG => 1,
    -LAST_UPDATE                            => $last_update,
    -KEY_FIELD                              => 'record_id',
    -SITE_NAME                              => $SiteName,
    -PAGE_TOP_VIEW                          => $page_top_view,
    -LEFT_PAGE_VIEW                         => $page_left_view,
    -PAGE_LEFT_VIEW                         => $page_left_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
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
