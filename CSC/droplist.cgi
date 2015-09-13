#!/usr/bin/perl -wT
# 	$Id: droplist.cgi,v 1.3 2004/01/25 03:48:50 shanta Exp $	

#location /cgi-bin/CSC
#Canged view url
#changed templates root

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
    qw(../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/CSC
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Extropia
       ../HTMLTemplates/Forager
       ../HTMLTemplates/Fly
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/VitalVic
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
#                          SITE SETUP                             #
######################################################################

my $APP_NAME = "droplist";
my $MOD_NAME = "droplist";
my $SiteName =  $CGI->param('site') || "CSC";
my $APP_NAME_TITLE = $SiteName." droplist manager";
my $AppVer = "ver 1.01, Dec 13, 2006";

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
    my $MySQLPW;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $DBI_DSN;
    my $AUTH_TABLE;
    my $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $last_update = 'September 16, 2010';
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $mail_cc;
    my $TableName;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
    my $HasMembers = 0;

use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
#Mail settings
    $mail_from             = $SetupVariables->{-MAIL_FROM}; 
    $mail_to               = $SetupVariables->{-MAIL_TO};
    $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME}||'blank';
    $app_logo              = $SetupVariables->{-APP_LOGO};
    $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
    $site                  = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
     my $LocalIp            = $SetupVariables->{-LOCAL_IP};

#Add sub aplication spacific overrides.
$page_top_view    = $CGI->param('page_top_view')||$page_top_view;
$page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
$page_left_view   = $CGI->param('left_page_view')||$page_left_view;



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
my $CSS_VIEW_URL ;
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
if ($SiteName eq "Apis") {
use ApisSetup;
  my $UseModPerl = 0;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesApis->{-APP_LOGO_ALT};
    $APP_NAME              = "apis";
    $homeviewname          = 'HelpDeskHomeView';
    $CSS_VIEW_URL          = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis'; 
    $SITE_DISPLAY_NAME      = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
  }
elsif ($SiteName eq "BCHPA") { 
use BCHPASetup;
  my $SetupVariablesBCHPA  = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesBCHPA->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesBCHPA->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBCHPA->{-LEFT_PAGE_VIEW};
    $homeviewname          = 'BCHPAHomeView';
    $home_view             = $SetupVariablesBCHPA ->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/BCHPA'; 
    $SITE_DISPLAY_NAME      = $SetupVariablesBCHPA->{-SITE_DISPLAY_NAME};
}  

elsif ($SiteName eq "BMaster") {
use BMasterSetup;
  my $UseModPerl = 0;
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
     $homeviewname            = $SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
 #Mail settings
    $mail_from             = $SetupVariablesBMaster->{-MAIL_FROM};
    $mail_to               = $SetupVariablesBMaster->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME      = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $UseModPerl = 0;
  my $SetupVariablesBrew   = new BrewSetup($UseModPerl);
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
elsif($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk") {
use CSSetup;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
    $APP_NAME_TITLE        = "Country Stores Client.";
    $homeviewname          = $SetupVariablesCS->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesCS->{-HOME_VIEW}; 
  $page_top_view            = $SetupVariablesCS->{-PAGE_TOP_VIEW};
  $page_bottom_view         = $SetupVariablesCS->{-PAGE_BOTTOM_VIEW};
  $page_left_view           = $SetupVariablesCS->{-LEFT_PAGE_VIEW};
#  $homeviewname             = $SetupVariablesCS->{-HOME_VIEW_NAME};
  $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
#  $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};#
#  $last_update              = $SetupVariablesCS->{-LAST_UPDATE}; 
  $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
#  $shop                     = $SetupVariablesCS->{-SHOP};
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

}


elsif ($SiteName eq "CSC" or	
       $SiteName eq "CSCDev"){
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC   = new CSCSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesCSC->{-AUTH_TABLE};
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL             = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.'/CSC'; 
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "ECF" or
       $SiteName eq "ECFDev") { 
use ECFSetup;
  my $SetupVariablesECF  = new  ECFSetup($UseModPerl);
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
    $CSS_VIEW_URL          = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME     = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
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
	if ($CGI->param('droplist')){
	$mail_cc = 'shanta@forager.com' ;
	}
   if  ($CGI->param('Nav_link')){
	$mail_cc = 'shanta2shanta.org' ;
	}
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
 
elsif ($SiteName eq "HE" ) {
use HESetup;
  my $UseModPerl = 0;
  my $SetupVariablesHE   = new HESetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS     = $SetupVariablesHE->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS       = $SetupVariablesHE->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION  = $SetupVariablesHE->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME            = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $AUTH_TABLE               = $SetupVariablesHE->{-AUTH_TABLE};
     $app_logo                 = $SetupVariablesHE->{-APP_LOGO};
     $app_logo_height          = $SetupVariablesHE->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesHE->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesHE->{-APP_LOGO_ALT};
     $homeviewname             = $SetupVariablesHE->{-HOME_VIEW_NAME};
     $home_view                = $SetupVariablesHE->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesHE->{-LAST_UPDATE}; 
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
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
 #     $site_update            = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
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
#      $site_update            = $SetupVariablesGRMarket->{-SITE_LAST_UPDATE};
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
 
 elsif ($SiteName eq "SQL_Ledger") {
  use SQLSetup;
	  my $SetupVariablesSQL       = new  SQLSetup($UseModPerl);
	    $AUTH_TABLE              = $SetupVariablesSQL ->{-AUTH_TABLE};
	    $HTTP_HEADER_KEYWORDS    = $SetupVariablesSQL->{-HTTP_HEADER_KEYWORDS};
	    $HTTP_HEADER_PARAMS      = $SetupVariablesSQL->{-HTTP_HEADER_PARAMS};
	    $HTTP_HEADER_DESCRIPTION = $SetupVariablesSQL->{-HTTP_HEADER_DESCRIPTION};
	    $CSS_VIEW_NAME           = $SetupVariablesSQL->{-CSS_VIEW_NAME};
	    $page_top_view           = $SetupVariablesSQL->{-PAGE_TOP_VIEW};
	    $page_bottom_view        = $SetupVariablesSQL->{-PAGE_BOTTOM_VIEW};
	    $page_left_view          = $SetupVariablesSQL->{-LEFT_PAGE_VIEW};
	    $CSS_VIEW_URL            = $SetupVariablesSQL->{-CSS_VIEW_NAME};
	    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CSC'; 
	    $SITE_DISPLAY_NAME       = $SetupVariablesSQL->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "Genealogy"){
use GenSetup;
  my $UseModPerl = 0;
  my $SetupVariablesGen   = new GenSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesGen->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesGen->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesGen->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesGen->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesGen->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesGen->{-APP_LOGO_ALT};
    $homeviewname          = $SetupVariablesGen->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesGen->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesGen->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SITE_DISPLAY_NAME      = $SetupVariablesGen->{-SITE_DISPLAY_NAME};
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
     $mail_to                 = $SetupVariablesForager->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesForager->{-MAIL_REPLYTO};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Forager'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesForager->{-SITE_DISPLAY_NAME};
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
    $APP_NAME_TITLE        = "Fly Fishing: A Flyfishrmans resource";
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
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Fly'; 
    $SITE_DISPLAY_NAME      = $SetupVariablesFly->{-SITE_DISPLAY_NAME};
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
     $SITE_DISPLAY_NAME      = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "AltPowerDev") {
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
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
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

elsif ($SiteName eq "Sky") {
use SkySetup;
  my $UseModPerl = 0;
  my $SetupVariablesSky   = new SkySetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSky->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSky->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSky->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSky->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSky->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSky->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSky->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSky->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesSky->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesSky=>{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesSky->{-LAST_UPDATE};
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
     $APP_NAME_TITLE          = "Organic Farming Droplist Manager.";
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic'; 
     $SITE_DISPLAY_NAME        = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
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
    $APP_DATAFILES_DIRECTORY  = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
    $SITE_DISPLAY_NAME        = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
 }

my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');

 
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
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $IMAGE_ROOT_URL,
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
    -LEFT_PAGE_VIEW          => $page_left_view,
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

my @MAIL_PARAMS = (
    -TYPE         => 'Sendmail',
);

my @USER_MAIL_SEND_PARAMS = (
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
        'category'             => 'Category',
        'project_name'        => 'Project Name',
        'project_size'        => 'Project Size',
        'estimated_man_hours' => 'Estimated Man Hours',
        'display_value'      => 'Display Value',
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
        'category'             => 'Category',
        'project_name'        => 'Project Name',
        'project_size'        => 'Project Size',
        'estimated_man_hours' => 'Estimated Man Hours',
        'display_value'      => 'Display Value',
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
 #       estimated_man_hours
my @app_name =qw(address_book slfaq faq faq_manager apis todo url  );
 my %sitenames;

if ($group eq 'CSC_admin') {
 %sitenames =
    ( All  => 'All Sites',
      AltPower => 'AltPower',
      Apis => 'Apis',
      CSC  => 'Computer System Consulting.ca',
      CS   => 'Country Stores',
      Demo => 'Demo site',
      ECF  => 'Eagle Creek Farms',
      Forager => 'Forager.com',
      Fly  => 'Fly Fishing',
      Marts => 'Marts',
      Organic => 'Organicfarming.ca',
      Shanta  => 'Shanta.org',
      Sky   => 'Skye Farm',
      SQL_Leger => 'SQL_Ledger Support',
      Stawns    => "Stawn's Honey farm",
      TelMark   => 'Telmark Skiing application',
      USBM      => 'Universal School of Biological Life',
      VitaVic   => 'Vital Victoria',
  
    );
    }
else{
      %sitenames =
    (
     All       => 'All Sites',
     $SiteName => $SiteName
    );
}
my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    status => [
        -DISPLAY_NAME => 'Status',
        -TYPE         => 'popup_menu',
        -NAME         => 'status',
        -VALUES       => [qw(active inactive)]
    ],  

#    project_name => [
#        -DISPLAY_NAME => 'Project Name',
#        -TYPE         => 'textfield',
#        -NAME         => 'project_name',
#        -SIZE         => 30,
#        -MAXLENGTH    => 80
#    ],

    category => [
        -DISPLAY_NAME => 'Stored Value  no spaces',
        -TYPE         => 'textfield',
        -NAME         => 'category',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    project_size => [
        -DISPLAY_NAME => 'Project Size',
        -TYPE         => 'popup_menu',
        -NAME         => 'project_size',
        -VALUES       => [
			  'Large', 
			  'Med', 
			  'Small', 
			  ''
			  ]
    ],

    estimated_man_hours => [
        -DISPLAY_NAME => 'Est. Man Hours',
        -TYPE         => 'textfield',
        -NAME         => 'estimated_man_hours',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    display_value => [
        -DISPLAY_NAME => 'Display Value',
        -TYPE         => 'textfield',
        -NAME         => 'display_value',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
 
    sitename => [
        -DISPLAY_NAME => 'Site',
        -TYPE         => 'popup_menu',
        -NAME         => 'sitename',
        -VALUES       => [sort {$a <=> $b} keys %sitenames ], 
 		  -LABELS       => \%sitenames,
         ],
#    app_name => [
#        -DISPLAY_NAME => 'Application Name',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'app_name',
#        -VALUES       => /@app_name,
#    ],

#    client_name => [
#        -DISPLAY_NAME => 'Client',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'client_name',
#        -VALUES       => [qw(ALL AltPower Apis BCHPA BuyAndSell CS CSC CAP ECF ENCY Organic VitalVic sl )]
#    ],

#     list_name => [
#        -DISPLAY_NAME => 'Drop list name',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'list_name',
#        -VALUES       => [qw(category client subject app_name )]
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
        app_name
        list_name
        category
        display_value
        client_name
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
	        -TABLE        => $CGI->param('DropListName')||'csc_droplist_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['category'],
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
######################################################################
#                          project db  SETUP                              #
######################################################################

my @PROJECT_DATASOURCE_FIELD_NAMES = qw(
        record_id
        status
        project_code
        project_name
        project_size
        estimated_man_hours
        developer_name
        client_name
        comments 
        sitename       
        username_of_poster
        group_of_poster
        date_time_posted
);

my	@PROJ_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'csc_project_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@PROJECT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

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
    -PROJECT_DATASOURCE_CONFIG_PARAMS     => \@PROJ_DATASOURCE_CONFIG_PARAMS,
    -CLIENT_DATASOURCE_CONFIG_PARAMS    => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
    -DROPLIST_DATASOURCE_CONFIG_PARAMS   => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################
           
my @MAIL_CONFIG_PARAMS = (     
    -TYPE         => 'Sendmail'
);

my @EMAIL_DISPLAY_FIELDS = qw(
        status
        category
        project_name
        project_size
        estimated_man_hours
        display_value
        client_name
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
    -FROM     =>  $SESSION->getAttribute(-KEY =>
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
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -LOG_FILE         => "$APP_DATAFILES_DIRECTORY/$APP_NAME.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX => "$APP_NAME_TITLE|"
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
    ApisCSSView
    CSCSSView
    CSPSCSSView
    VitalVicCSSView
    ENCYCSSView
    BCAFCSSView
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
    BasicDataView
    DetailsRecordView
    ModifyRecordView
    LogoffView
    OptionsView
);

my @ROW_COLOR_RULES = (
   {'status' => [qw(Requested 99CC99)]},
   {'status' => [qw(In-Process CC9999)]},
   {'status' => [qw(Delivered CC9999)]}
);

my @FIELD_COLOR_RULES = (
   {'project_size' => [qw(Large BLUE)]},
   {'project_size' => [qw(Small ORANGE)]}
);


my @VIEW_DISPLAY_PARAMS = (
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -FIELD_COLOR_RULES       => \@FIELD_COLOR_RULES,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
    -FAVICON                 => $FAVICON || '/images/apis/favicon.ico',
    -ANI_FAVICON             => $ANI_FAVICON,
    -FAVICON_TYPE            => $FAVICON_TYPE,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -HOME_VIEW               => $homeviewname,
    -SITE_DISPLAY_NAME       =>  $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELD_NAME_MAPPINGS   => {
        status              => 'Status',
        category             => 'Category',
        app_name        => 'Application Name',
        project_size        => 'Project Size',
        estimated_man_hours => 'Est. Man Hours',
        display_value      => 'Display Value',
        client_name         => 'Client',
        comments            => 'Comments'
        },
    -DISPLAY_FIELDS        => [qw(
        category
        project_name
        project_size
        estimated_man_hours
        status
        display_value
        client_name
        comments        
        )],
    -SORT_FIELDS        => [qw(
        status
        project_name
        project_size
        estimated_man_hours
        display_value
        client_name
        comments        
        )],
    -SELECTED_DISPLAY_FIELDS        => [qw(
        category
        app_name
        display_value
        client_name
        status
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

       CSC::PopulateInputWidgetDefinitionListWithProjectCodeWidgetAction
       CSC::ProcessShowAllOpenToDosAction
       CSC::PopulateInputWidgetDefinitionListWithClientWidgetAction
       Default::PopulateInputWidgetDefinitionListWithAppNameWidgetAction
       Default::PopulateInputWidgetDefinitionListWithListWidgetAction
       
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
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -MOD_NAME                               => $MOD_NAME,
    -APP_NAME                               => $APP_NAME,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -BASIC_DATA_VIEW_NAME                   => 'BasicDataView',
    -CGI_OBJECT                             =>  $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DELETE_FORM_VIEW_NAME                  => 'BasicDataView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DEFAULT_SORT_FIELD1                    => 'status',
    -DEFAULT_SORT_FIELD2                    => 'project_name',
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LAST_UPDATE                            => $last_update,
  	 -APP_VER                                => $AppVer,
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
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 1,
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG         => 1,
    -SEND_EMAIL_ON_DELETE_FLAG             => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG             => 0,
    -SEND_EMAIL_ON_ADD_FLAG                => 0,
    -SESSION_OBJECT                        => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME             => 'SessionTimeoutErrorView',
    -SIMPLE_SEARCH_BOX_VIEW_NAME           => 'SimpleSearchBoxView',
    -VIEW_FILTERS_CONFIG_PARAMS            => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_DISPLAY_PARAMS                   => \@VIEW_DISPLAY_PARAMS,
    -TEMPLATES_CACHE_DIRECTORY             => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                           => \@VALID_VIEWS,
    -VIEW_LOADER                           => $VIEW_LOADER,
    -RECORDS_PER_PAGE_OPTS                 => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                  => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                           => $CGI->param('sort_field1') || 'category',
    -SORT_FIELD2                           => $CGI->param('sort_field2') || '',
    -SORT_DIRECTION                        => $CGI->param('sort_direction') || 'ASC',
    -SIMPLE_SEARCH_STRING                  => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                  => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || "0",
    -KEY_FIELD                             => 'record_id',
    -SITE_NAME                             => $SiteName,
    -PAGE_TOP_VIEW                         => $page_top_view ,
    -LEFT_PAGE_VIEW                        => $page_left_view,
    -PAGE_BOTTOM_VIEW                      => $page_bottom_view,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN    => 2,
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

