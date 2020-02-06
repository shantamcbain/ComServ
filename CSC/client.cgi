#!/usr/bin/perl -wT
# 	$Id: client.cgi,v 1.2 2004/02/02 21:22:45 shanta Exp $
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
# Boston, MA  02111-1307, USA.state

use strict;
BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/AddressBook
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/CSC
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Forager
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/AddressBook
       ../HTMLTemplates/Organic
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


my $APP_NAME = "client";
my $SiteName =  $CGI->param('site') || "CSC";
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $APP_NAME_TITLE = "Computer System Consulting.ca";
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
    my $site;
    my $MySQLPW;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $additonalautusernamecomments;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
    my $SetupVariables  ;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $last_update = 'Sept 8, 2010';
my $site_update;
my $Affiliate = 001;
my $client_tb = 'csc_client_tb';
    my $HasMembers = 0;

use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view                    = $SetupVariables->{-HOME_VIEW};
    $homeviewname                 = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW              = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view                = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view             = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view               = $SetupVariables->{-PAGE_LEFT_VIEW};
    $MySQLPW                      = $SetupVariables->{-MySQLPW};
#Mail settings
    $mail_from                    = $SetupVariables->{-MAIL_FROM};
    $mail_to                      = $SetupVariables->{-MAIL_TO};
    $mail_replyto                 = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME                = $SetupVariables->{-CSS_VIEW_NAME};
    $app_logo                     = $SetupVariables->{-APP_LOGO};
    $app_logo_height              = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width               = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt                 = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL               = $SetupVariables->{-IMAGE_ROOT_URL};
    $DOCUMENT_ROOT_URL            = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET                  = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS           = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS         = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION      = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    my @PRODUCT_DATASET           = $SetupVariables->{-PRODUCT_DATASOURCE_CONFIG_PARAMS};
    $DEFAULT_CHARSET              = $SetupVariables->{-DEFAULT_CHARSET};
    $DBI_DSN                      = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE                   = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME          = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    my @AUTH_USER_DATASOURCE_CONFIG_PARAMS = $SetupVariables->{-AUTH_USER_DATASOURCE_CONFIG_PARAMS};
    $additonalautusernamecomments = $SetupVariables->{-ADDITIONALAUTHUSERNAMECOMMENTS};
    $site                         = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY   = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY    = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY      = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $DATAFILES_DIRECTORY          = $APP_DATAFILES_DIRECTORY;
    $site_session                 = $DATAFILES_DIRECTORY.'/Sessions';
    $auth                         = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
   my $LocalIp            = $SetupVariables->{-LOCAL_IP};

#Add
# $GLOBAL_DATAFILES_DIRECTORY = "Datafiles";
# $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
# $APP_DATAFILES_DIRECTORY    = "Datafiles/AddressBook";
#$page_top_view    = $CGI->param('page_top_view')||$page_top_view;
#$page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
#$left_page_view   = $CGI->param('left_page_view')||$left_page_view;

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
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');
my $username    =  $SESSION ->getAttribute(-KEY => 'auth_username');

 if ($SiteName eq "ECF") {
use ECFSetup;
  my $SetupVariablesECF    = new  ECFSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesECF->{-APP_LOGO_ALT};
    $APP_NAME_TITLE        = "Eagle Creek Farms: Apis";
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
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ECF'; 
}
elsif ($SiteName eq "AltPower") {
use AltPowerSetup;
  my $UseModPerl = 0;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesAltPower->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesAltPower->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesAltPower->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesAltPower=>{-CSS_VIEW_NAME};
     $CSS_VIEW_URL            = $SetupVariablesAltPower->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesAltPower->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesAltPower->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesAltPower->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesAltPower->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesAltPower->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesAltPower->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesAltPower->{-HOME_VIEW};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
 }

elsif ($SiteName eq "BMaster") {
use BMasterSetup;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
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
     $homeviewname            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
      $site_update              = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesBMaster->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBMaster->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBMaster->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesBMaster->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesBMaster->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBMaster->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesBMaster->{-FAVICON_TYPE};
}

elsif ($SiteName eq "BeeTalk") {
use BeeTalkSetup;
  my $SetupVariablesBeeTalk   = new BeeTalkSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesBeeTalk->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesBeeTalk->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesBeeTalk->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesBeeTalk->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesBeeTalk->{-AUTH_TABLE};
     $Affiliate               = $SetupVariablesBeeTalk->{-AFFILIATE};
     $app_logo                = $SetupVariablesBeeTalk->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesBeeTalk->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesBeeTalk->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesBeeTalk->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesBeeTalk->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBeeTalk->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBeeTalk->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBeeTalk->{-LAST_UPDATE}; 
#Mail settings
     $mail_from               = $SetupVariablesBeeTalk->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBeeTalk->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBeeTalk->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesBeeTalk->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesBeeTalk->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesBeeTalk->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBeeTalk->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesBeeTalk->{-FAVICON_TYPE};
}


elsif ($SiteName eq "SQL_Ledger") {
use SQLSetup;
  my $SetupVariablesSQL       = new  SQLSetup($UseModPerl);
    $AUTH_TABLE              = $SetupVariablesSQL ->{-AUTH_TABLE};
    $APP_NAME_TITLE          = "Computer System Consulting.ca";
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesSQL->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesSQL->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesSQL->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME           = $SetupVariablesSQL->{-CSS_VIEW_NAME};
    $page_top_view           = $SetupVariablesSQL->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesSQL->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesSQL->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL            = $SetupVariablesSQL->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CSC'; 
}

elsif ($SiteName eq "CSC"){
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC  = new CSCSetup($UseModPerl);
    $APP_NAME_TITLE        = "CSC Clients";
    $homeviewname          = 'HelpDeskHomeView';
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $home_view             = $SetupVariablesCSC->{-HOME_VIEW};
    $BASIC_DATA_VIEW       = $SetupVariablesCSC->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesCSC->{-MAIL_FROM};
    $mail_to               = $SetupVariablesCSC->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesCSC->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME         = $SetupVariablesCSC->{-CSS_VIEW_NAME}||'blank';
    $app_logo              = $SetupVariablesCSC->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesCSC->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesCSC->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesCSC->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL        = $SetupVariablesCSC->{-IMAGE_ROOT_URL};
    $DOCUMENT_ROOT_URL     = $SetupVariablesCSC->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET           = $SetupVariablesCSC->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET       = $SetupVariablesCSC->{-DEFAULT_CHARSET};
#    $DBI_DSN               = $SetupVariablesCSC->{-DBI_DSN};
#    $AUTH_TABLE            = $SetupVariablesCSC->{-AUTH_TABLE};
    $DEFAULT_CHARSET       = $SetupVariablesCSC->{-DEFAULT_CHARSET};
    $site = $SetupVariablesCSC->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariablesCSC->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariablesCSC->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariablesCSC->{-APP_DATAFILES_DIRECTORY};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
     
}
elsif ($SiteName eq "Demo" or
      $SiteName eq "DemoHelpDesk") {
use DEMOSetup;
  my $UseModPerl = 1;
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
    $app_logo                 = $SetupVariablesDemo->{-APP_LOGO};
    $app_logo_height          = $SetupVariablesDemo->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesDemo->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesDemo->{-APP_LOGO_ALT};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
    $homeviewname             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-SITE_LAST_UPDATE};
    $FAVICON                  = $SetupVariablesDemo->{-FAVICON};
    $ANI_FAVICON              = $SetupVariablesDemo->{-ANI_FAVICON};
    $FAVICON_TYPE             = $SetupVariablesDemo->{-FAVICON_TYPE};

}

elsif ($SiteName eq "Forager") {
use ForagerSetup;
  my $UseModPerl = 1;
  my $SetupVariablesForager  = new ForagerSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesForager->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesForager->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesForager->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesForager->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesForager->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesForager->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesForager->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesForager->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesForager->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesForager->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesForager->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesForager->{-CSS_VIEW_NAME};
     $APP_NAME_TITLE          = "Forager Clients";
     $mail_to                 = $SetupVariablesForager->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesForager->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Forager'; 
 }
elsif ($SiteName eq "Genealogy"){
use GenSetup;
  my $UseModPerl = 0;
  my $SetupVariablesGen   = new GenSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesGen->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesGen->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesGen->{-APP_LOGO};
    $app_logo_alt          = $SetupVariablesGen->{-APP_LOGO_ALT};
    $app_logo_height       = $SetupVariablesGen->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesGen->{-APP_LOGO_WIDTH};
    $homeviewname          = $SetupVariablesGen->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesGen->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesGen->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
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
      $site_update            = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
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
      $site_update            = $SetupVariablesGRProject->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGRProject->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGRProject->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGRProject->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGRProject->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGRProject->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGRProject->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGRProject->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGRProject->{-FAVICON_TYPE};
} elsif ($SiteName eq "MW") {
use MWSetup;
  my $SetupVariablesMW   = new MWSetup($UseModPerl);
     $APP_NAME_TITLE          = "MacDonald water products.";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesMW->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesMW->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesMW->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesMW->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesMW->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesMW->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesMW->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesMW->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesMW->{-APP_LOGO_ALT};
     $home_view            = $SetupVariablesMW->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesMW->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesMW->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesMW->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesMW->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesMW->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesMW->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesMW->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesMW->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesMW->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesMW->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesMW->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesMW->{-FAVICON_TYPE};
 #    $TableName               = $SetupVariablesMW->{-PROJECT_TB};
     $client_tb               = $SetupVariablesMW->{-CLIENT_TB};
}

elsif ($SiteName eq "Organic") {
use OrganicSetup;
  my $UseModPerl = 0;
  my $SetupVariablesOrganic   = new OrganicSetup($UseModPerl);
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
 }

my $modify = '1';
my $delete = '1';
my $require = '1';
 if ($username eq "Shanta"  ) {
    $modify = '0';
    $delete = '0';
    $require = '0';
}
if ($group = 'member'){
 $require = '1';
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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      => $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||'$mail_from',
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
        'fname'    => 'First Name',
        'lname'    => 'Last Name',
        'email'    => 'E-Mail',
        'category' => 'Category',
        'phone'    => 'Phone',
        'comments' => 'Comments'
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
                category
                fname
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
        'fname'    => 'First Name',
        'lname'    => 'Last Name',
        'email'    => 'E-Mail',
        'category' => 'Category',
        'phone'    => 'Phone',
        'comments' => 'Comments'
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
                category
                fname
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


my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    category => [
        -DISPLAY_NAME => 'Category',
        -TYPE         => 'popup_menu',
        -NAME         => 'category',
        -VALUES       => [qw(Alliance Business-General Client Misc Personal Staff)]
    ],

    fname => [
        -DISPLAY_NAME => 'First Name',
        -TYPE         => 'textfield',
        -NAME         => 'fname',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    lname => [
        -DISPLAY_NAME => 'Last Name',
        -TYPE         => 'textfield',
        -NAME         => 'lname',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    email => [
        -DISPLAY_NAME => 'Email',
        -TYPE         => 'textfield',
        -NAME         => 'email',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    phone => [
        -DISPLAY_NAME => 'Phone',
        -TYPE         => 'textfield',
        -NAME         => 'phone',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

      company_code => [
        -DISPLAY_NAME => 'Company Code',
        -TYPE         => 'textfield',
        -NAME         => 'company_code',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

  company_name => [
        -DISPLAY_NAME => 'Company',
        -TYPE         => 'textfield',
        -NAME         => 'company_name',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    title => [
        -DISPLAY_NAME => 'Title',
        -TYPE         => 'textfield',
        -NAME         => 'title',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    department => [
        -DISPLAY_NAME => 'Department',
        -TYPE         => 'textfield',
        -NAME         => 'department',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    address1 => [
        -DISPLAY_NAME => 'Address 1',
        -TYPE         => 'textfield',
        -NAME         => 'address1',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    address2 => [
        -DISPLAY_NAME => 'Address2',
        -TYPE         => 'textfield',
        -NAME         => 'address2',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    city => [
        -DISPLAY_NAME => 'City',
        -TYPE         => 'textfield',
        -NAME         => 'city',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    prov => [
        -DISPLAY_NAME => 'Prov',
        -TYPE         => 'textfield',
        -NAME         => 'prov',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    zip => [
        -DISPLAY_NAME => 'Zip',
        -TYPE         => 'textfield',
        -NAME         => 'zip',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    country => [
        -DISPLAY_NAME => 'Country',
        -TYPE         => 'textfield',
        -NAME         => 'country',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    fax => [
        -DISPLAY_NAME => 'Fax',
        -TYPE         => 'textfield',
        -NAME         => 'fax',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    mobile => [
        -DISPLAY_NAME => 'Mobile',
        -TYPE         => 'textfield',
        -NAME         => 'mobile',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    url => [
        -DISPLAY_NAME => 'Url',
        -TYPE         => 'textfield',
        -NAME         => 'url',
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
        category
        fname   
        lname   
        phone   
        email   
        company_code
        company_name
        title
        department
        address1
        address2
        city
        prov
        zip
        country
        fax
        mobile
        url
        comments
);

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
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
	        -TABLE        => $client_tb,
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
        category
        fname
        lname
        phone
        email
        comments
);

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
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
    -LOG_FILE         => "$APP_DATAFILES_DIRECTORY/$APP_NAME.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX => $APP_NAME_TITLE.' |'
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
    CSCCSSView
    CSPSCSSView
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
    ECFHomeView
);

my @ROW_COLOR_RULES = (
   {'category' => [qw(Business 99CC99)]},
   {'category' => [qw(Personal CC9999)]}
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
	 -FAVICON                        => $FAVICON || '/images/apis/favicon.ico',
	 -ANI_FAVICON                    => $ANI_FAVICON,
	 -FAVICON_TYPE                   => $FAVICON_TYPE,
    -DEFAULT_CHARSET                => $DEFAULT_CHARSET,
    -DISPLAY_FIELDS                 => [qw(
        category
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
        company_name
        title
        department
        fax
        mobile
        url
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
        comments
                 )],
    -FIELD_NAME_MAPPINGS     => {
        category	=> 'Category',
        record_id	=> 'Record ID',
        fname		=> 'First Name',
        lname		=> 'Last Name',
        group_of_poster => 'Group',
        phone		=> 'Phone',
       email		=> 'E-mail',
        comments	=> 'Comments',
        address1        => 'Address1',
        address2        => 'Address2',
        city            => 'City',
        prov           => 'Prov',
        zip             => 'Zip',
        country         => 'Country',
        company_name    => 'Company Name',
        title           => 'Title',
        department      => 'Department',
        fax             => 'Fax',
        mobile          => 'Mobile',
        url             => 'URL'
        },
    -IMAGE_ROOT_URL     => $IMAGE_ROOT_URL,
    -LINK_TARGET        => $LINK_TARGET,
    -HTTP_HEADER_PARAMS => $HTTP_HEADER_PARAMS,
    -ROW_COLOR_RULES    => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME=> $APP_NAME_TITLE,
    -SCRIPT_NAME        => $CGI->script_name(),
    -APP_NAME           => $APP_NAME,
    -SELECTED_DISPLAY_FIELDS => [qw(
        category
        fname
        lname
        email
        )],
    -SORT_FIELDS             => [qw(
        category
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
        company_name
        title
        department
        fax
        mobile
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
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 5,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'category',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'fname',
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
    -LAST_UPDATE                            => $last_update,
    -SITE_LAST_UPDATE                       => $site_update,
    -KEY_FIELD                              => 'record_id',
    -LOCAL_IP                               => $LocalIp,
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
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $modify,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => $modify,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => $delete,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => $delete,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => $require,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => $require,
    -SEND_EMAIL_ON_DELETE_FLAG              => 1,
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
    -SITE_DISPLAY_NAME       =>  $SITE_DISPLAY_NAME,
    -PAGE_TOP_VIEW           =>  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $page_left_view,
    -PAGE_BOTTOM_VIEW        =>  $page_bottom_view,
    -SELECT_FORUM_VIEW		=> 'SelectForumView',
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