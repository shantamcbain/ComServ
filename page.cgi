#!/usr/bin/perl -wT
# 	$Id: page.cgi,v 1.01 2015/08/30 14:27:36 shanta Exp $	

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
my $allow_add = 0;
my $allow_mod = 0;
my $allow_del = 0;  
my $HasMembers = 0;   

use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
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


 if ($SiteName eq "ECF" ||
     $SiteName eq "DarmaFarms"||
     $SiteName eq "ECFDev") {
use ECFSetup;
  my $SetupVariablesECF    = new  ECFSetup($UseModPerl);
     $shop                     = $SetupVariablesECF->{-SHOP};
     $StoreUrl                = $SetupVariablesECF->{-STORE_URL};
     $site_update              = $SetupVariablesECF->{-SITE_LAST_UPDATE};
     $CSS_VIEW_NAME           = $SetupVariablesECF->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesECF->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesECF->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesECF->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesECF->{-APP_LOGO_ALT};
     $FAVICON                = $SetupVariablesECF->{-FAVICON};
     $ANI_FAVICON            = $SetupVariablesECF->{-ANI_FAVICON};
     $FAVICON_TYPE          = $SetupVariablesECF->{-FAVICON_TYPE};
 #    $home_view               = $SetupVariablesECF->{-HOME_VIEW};
#Mail settings 
    $mail_from               = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS      = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
    $last_update             = $SetupVariablesECF->{-LAST_UPDATE}; 
 }
 elsif ($SiteName eq "AltPower") {
use AltPowerSetup;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
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
     $home_view               = 'HomeView'||$SetupVariablesAltPower->{-HOME_VIEW_NAME};
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
elsif ($SiteName eq "Apis") {
use ApisSetup;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesApis->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesApis->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesApis->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesApis->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesApis->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesApis->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesApis->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesApis->{-APP_LOGO_ALT};
 #    $home_view               = $SetupVariablesApis->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesApis->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesApis->{-LAST_UPDATE}; 
 #Mail settings
     $site_update             = $SetupVariablesApis->{-SITE_LAST_UPDATE};
     $mail_from               = $SetupVariablesApis->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesApis->{-MAIL_TO};
     $mail_replyto           = $SetupVariablesApis->{-MAIL_REPLYTO};
 }

elsif ($SiteName eq "BMastBreeder") {
use BMasterSetup;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesBMaster->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesBMaster->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesBMaster->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesBMaster->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesBMaster->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesBMaster->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesBMaster->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesBMaster->{-APP_LOGO_ALT};
 #    $home_view            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
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

elsif ($SiteName eq "BeeCoop") {
use BMasterSetup;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesBMaster->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesBMaster->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesBMaster->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesBMaster->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesBMaster->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesBMaster->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesBMaster->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesBMaster->{-APP_LOGO_ALT};
 #    $home_view            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
 #    $home_view               = 'CoopHomeView'||$SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from               = $SetupVariablesBMaster->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBMaster->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBMaster->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = 'BeeMaster.ca Co-Op';
     $FAVICON                 = $SetupVariablesBMaster->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesBMaster->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBMaster->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesBMaster->{-FAVICON_TYPE};
}

elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
#    $home_view          = $SetupVariablesBrew->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesBrew->{-HOME_VIEW}; 
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
    $last_update           = $SetupVariablesBrew->{-LAST_UPDATE}; 
    $site_update           = $SetupVariablesBrew->{-SITE_LAST_UPDATE};
}

elsif($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk") {
use CSSetup;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
 #   $APP_NAME_TITLE        = "Country Stores Client.";
#    $home_view          = $SetupVariablesCS->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesCS->{-HOME_VIEW}; 
  $page_top_view            = $SetupVariablesCS->{-PAGE_TOP_VIEW};
  $page_bottom_view         = $SetupVariablesCS->{-PAGE_BOTTOM_VIEW};
  $page_left_view           = $SetupVariablesCS->{-LEFT_PAGE_VIEW};
#  $home_view             = $SetupVariablesCS->{-HOME_VIEW_NAME};
  $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
  $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};
  $last_update              = $SetupVariablesCS->{-LAST_UPDATE}; 
  $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
  $shop                     = $SetupVariablesCS->{-SHOP};
  $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
  $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
  $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
  $FAVICON                  = $SetupVariablesCS>{-FAVICON};
  $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
  $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};
  $CSS_VIEW_URL             = $SetupVariablesCS->{-CSS_VIEW_NAME};
#    $left_page_view = 'CSCLeftPageView';
}


elsif ($SiteName eq "CSC" or
       $SiteName eq "CSCDev"
       ) {
use CSCSetup;
  my $SetupVariablesCSC   = new  CSCSetup($UseModPerl);
if ($SiteName eq "CSCDev"
       ) {     
    $SITE_DISPLAY_NAME        = "Dev.".$SetupVariablesCSC->{-SITE_DISPLAY_NAME};
   #    $APP_NAME_TITLE           = "CSC";
$AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
       } else {
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
  #  $APP_NAME_TITLE           = "Computer System Consulting.ca";
         $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
       }
    $StoreUrl                = $SetupVariablesCSC->{-STORE_URL};
    $site_update             = $SetupVariablesCSC->{-SITE_LAST_UPDATE};
    $last_update             = $SetupVariablesCSC->{-LAST_UPDATE}; 
    $HasMembers              = $SetupVariablesCSC->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
#    $home_view               = $SetupVariablesCSC->{-HOME_VIEW};
    $page_top_view           = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CSC'; 

}
elsif ($SiteName eq "Demo" or
      $SiteName eq "DemoHelpDesk") {
use DEMOSetup;
  my $UseModPerl = 1;
  my $SetupVariablesDemo   = new  DEMOSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesDemo ->{-AUTH_TABLE};
    $StoreUrl                 = $SetupVariablesDemo->{-STORE_URL};
 #   $APP_NAME_TITLE           = "Computer System Consulting.ca Demo Application";
    $HasMembers               = $SetupVariablesDemo->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesDemo->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesDemo->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesDemo->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME            = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $page_top_view            = $SetupVariablesDemo->{-PAGE_TOP_VIEW};
    $page_bottom_view         = $SetupVariablesDemo->{-PAGE_BOTTOM_VIEW};
    $page_left_view           = $SetupVariablesDemo->{-LEFT_PAGE_VIEW};
    $app_logo                 = $SetupVariablesDemo->{-APP_LOGO};
    $shop                     = $SetupVariablesDemo->{-SHOP};
    $app_logo_height          = $SetupVariablesDemo->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesDemo->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesDemo->{-APP_LOGO_ALT};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
#    $home_view             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-SITE_LAST_UPDATE};
    $FAVICON                  = $SetupVariablesDemo->{-FAVICON};
    $ANI_FAVICON              = $SetupVariablesDemo->{-ANI_FAVICON};
    $FAVICON_TYPE             = $SetupVariablesDemo->{-FAVICON_TYPE};

}elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $SetupVariablesENCY   = new ENCYSetup($UseModPerl);
      $HTTP_HEADER_KEYWORDS    = $SetupVariablesENCY->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesENCY->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesENCY->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesENCY->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesENCY->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesENCY->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesENCY->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesENCY->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesENCY->{-APP_LOGO_ALT};
 #    $home_view            = $SetupVariablesENCY->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesENCY->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesENCY->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesENCY->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesENCY->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesENCY->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesENCY->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesENCY->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesENCY->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesENCY->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesENCY->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesENCY->{-FAVICON_TYPE};
} 

elsif ($SiteName eq "FeedBees") {
use FeedBeesSetup;
  my $SetupVariablesFeedBees   = new FeedBeesSetup($UseModPerl);
     $StoreUrl                = $SetupVariablesFeedBees->{-STORE_URL};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesFeedBees->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesFeedBees->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesFeedBees->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesFeedBees->{-CSS_VIEW_NAME};
     $Affiliate               = $SetupVariablesFeedBees->{-AFFILIATE};
     $AUTH_TABLE              = $SetupVariablesFeedBees->{-AUTH_TABLE};
     $MySQLPW                 = $SetupVariablesFeedBees>{-MySQLPW};
     $AUTH_MSQL_USER_NAME     = $SetupVariablesFeedBees->{-AUTH_MSQL_USER_NAME};
     $app_logo                = $SetupVariablesFeedBees->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesFeedBees->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesFeedBees->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesFeedBees->{-APP_LOGO_ALT};
     $home_view               = 'HomeView'||$SetupVariablesFeedBees->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesFeedBees->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesFeedBees->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesFeedBees->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesFeedBees->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesFeedBees->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesFeedBees->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesFeedBees->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesFeedBees->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesFeedBees->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesFeedBees->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesFeedBees->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesFeedBees->{-FAVICON_TYPE};
}
if ($SiteName eq "Forager") {
use ForagerSetup;
  my $SetupVariablesForager    = new  ForagerSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesForager->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesForager->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesForager->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesForager->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesForager->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesForager->{-APP_LOGO_ALT};
    $home_view               = $SetupVariablesForager->{-HOME_VIEW};
#Mail settings
    $mail_from               = $SetupVariablesForager->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesForager->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesForager->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS      = $SetupVariablesForager->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesForager->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesForager->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesForager->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesForager->{-SITE_DISPLAY_NAME}||'test';
    $last_update             = $SetupVariablesForager->{-SITE_LAST_UPDATE}; 
 }



elsif ($SiteName eq "GrindrodBC") {
use GrindrodSetup;
  my $SetupVariablesGrindrod   = new GrindrodSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGrindrod->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGrindrod->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGrindrod->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGrindrod->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGrindrod->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGrindrod->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGrindrod->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGrindrod->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGrindrod->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
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
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGRProject->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGRProject->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGRProject->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGRProject->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGRProject->{-AUTH_TABLE};
     $MySQLPW                 = $SetupVariablesGRProject->{-MySQLPW};
     $AUTH_MSQL_USER_NAME     = $SetupVariablesGRProject->{-AUTH_MSQL_USER_NAME};
     $app_logo                = $SetupVariablesGRProject->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGRProject->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGRProject->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGRProject->{-APP_LOGO_ALT};
 #    $home_view             = $SetupVariablesGRProject->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesGRProject->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGRProject->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGRProject->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesGRProject->{-SITE_LAST_UPDATE};
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
 
elsif ($SiteName eq "HoneyDo" or
       $SiteName eq "HoneyDoDev") {
use HoneyDoSetup;
  my $UseModPerl = 1;
  my $SetupVariablesHoneyDo   = new HoneyDoSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesHoneyDo->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesHoneyDo->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesHoneyDo->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesHoneyDo->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesHoneyDo->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesHoneyDo->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesHoneyDo->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesHoneyDo->{-APP_LOGO_ALT};
 #    $home_view            = $SetupVariablesHoneyDo->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesHoneyDo->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesHoneyDo->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesHoneyDo->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from               = $SetupVariablesHoneyDo->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesHoneyDo->{-MAIL_TO};
     $SITE_DISPLAY_NAME       = $SetupVariablesHoneyDo->{-SITE_DISPLAY_NAME};
     $mail_replyto            = $SetupVariablesHoneyDo->{-MAIL_REPLYTO};
 }


elsif ($SiteName eq "WB" or
       $SiteName eq "WBDev" ) {
use WBSetup;
  my $SetupVariablesWB   = new WBSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesWB->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesWB->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesWB->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesWB->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesWB->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesWB->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesWB->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesWB->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesWB->{-APP_LOGO_ALT};
     if ($group eq "Mentoring"){
 #    $home_view               = 'MentoringHomeView';
 #    $home_view            = $home_view;
    }else{
 #    $home_view            = $SetupVariablesWB->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesWB->{-HOME_VIEW};
     }
     $CSS_VIEW_URL            = $SetupVariablesWB->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesWB->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesWB->{-SITE_LAST_UPDATE};
 #Mail settings
    $mail_from                = $SetupVariablesWB->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesWB->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesWB->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesWB->{-SITE_DISPLAY_NAME};
    $FAVICON                  = $SetupVariablesWB->{-FAVICON}||'/images/apis/favicon.ico';
    $ANI_FAVICON              = $SetupVariablesWB->{-ANI_FAVICON};
    $page_top_view            = $SetupVariablesWB->{-PAGE_TOP_VIEW};
}

elsif ($SiteName eq "HE" or
       $SiteName eq "HEDev") {
use HESetup;
  my $SetupVariablesHE   = new HESetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS     = $SetupVariablesHE->{-HTTP_HEADER_KEYWORDS};
     $StoreUrl                = $SetupVariablesHE->{-STORE_URL};
     $HTTP_HEADER_PARAMS       = $SetupVariablesHE->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION  = $SetupVariablesHE->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME            = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $AUTH_TABLE               = $SetupVariablesHE->{-AUTH_TABLE};
     $app_logo                 = $SetupVariablesHE->{-APP_LOGO};
     $app_logo_height          = $SetupVariablesHE->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesHE->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesHE->{-APP_LOGO_ALT};
 #    $home_view             = $SetupVariablesHE->{-HOME_VIEW_NAME};
 #    $home_view                = $SetupVariablesHE->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesHE->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesHE->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
     $shop                     = $SetupVariablesHE->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
}
 
elsif ($SiteName eq "IM" or
       $SiteName eq "IMDEV") {
use IMSetup;
  my $SetupVariablesIM   = new IMSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS     = $SetupVariablesIM->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS       = $SetupVariablesIM->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION  = $SetupVariablesIM->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME            = $SetupVariablesIM->{-CSS_VIEW_NAME};
     $AUTH_TABLE               = $SetupVariablesIM->{-AUTH_TABLE};
     $app_logo                 = $SetupVariablesIM->{-APP_LOGO};
     $app_logo_height          = $SetupVariablesIM->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesIM->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesIM->{-APP_LOGO_ALT};
 #    $home_view             = $SetupVariablesIM->{-HOME_VIEW_NAME};
 #    $home_view                = $SetupVariablesIM->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesIM->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesIM->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesIM->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesIM->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesIM->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesIM->{-MAIL_REPLYTO};
     $shop                     = $SetupVariablesIM->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesIM->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "LandTrust"){
use LTrustSetup;
  my $UseModPerl = 1;
  my $SetupVariablesLandTrust   = new LTrustSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesLandTrust->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesLandTrust->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesLandTrust->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesLandTrust->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesLandTrust->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesLandTrust->{-APP_LOGO_ALT};
#    $home_view          = $SetupVariablesLandTrust->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesLandTrust->{-HOME_VIEW}; 
    $CSS_VIEW_URL            = $SetupVariablesLandTrust->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/LandTrust';
    $SiteLastUpdate          = $SetupVariablesLandTrust->{-Site_Last_Update}; 
    $SITE_DISPLAY_NAME       = $SetupVariablesLandTrust->{-SITE_DISPLAY_NAME};
    $NEWS_TB                 = $SetupVariablesLandTrust->{-NEWS_TB};
  }
elsif ($SiteName eq "LumbyThrift") {
use LumbyThriftSetup;
  my $SetupVariablesLumbyThrift   = new LumbyThriftSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesLumbyThrift->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesLumbyThrift->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesLumbyThrift->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesLumbyThrift->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesLumbyThrift->{-AUTH_TABLE};
     $Affiliate               = $SetupVariablesLumbyThrift->{-AFFILIATE};
     $app_logo                = $SetupVariablesLumbyThrift->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesLumbyThrift->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesLumbyThrift->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesLumbyThrift->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesLumbyThrift->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesLumbyThrift->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesLumbyThrift->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesLumbyThrift->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesLumbyThrift->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesLumbyThrift->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesLumbyThrift->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesLumbyThrift->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesLumbyThrift->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesLumbyThrift->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesLumbyThrift->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesLumbyThrift->{-FAVICON_TYPE};
}

elsif (
      $SiteName eq "JennaBee") {
use JennaBeeSetup;
  my $SetupVariablesJennaBee    = new  JennaBeeSetup($UseModPerl);
     $shop                    = $SetupVariablesJennaBee->{-SHOP};
     $StoreUrl                = $SetupVariablesJennaBee->{-STORE_URL};
     $Affiliate               = $SetupVariablesJennaBee->{-AFFILIATE};
#     $HeaderImage             = $SetupVariablesJennaBee->{-HEADER_IMAGE};
#     $Header_height           = $SetupVariablesJennaBee->{-HEADER_HEIGHT};
#     $Header_width            = $SetupVariablesJennaBee->{-HEADER_WIDTH};
#     $Header_alt              = $SetupVariablesJennaBee->{-HEADER_ALT};
     $site_update             = $SetupVariablesJennaBee->{-SITE_LAST_UPDATE};
     $CSS_VIEW_NAME           = $SetupVariablesJennaBee->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesJennaBee->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesJennaBee->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesJennaBee->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesJennaBee->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesJennaBee->{-APP_LOGO_ALT};
     $FAVICON                 = $SetupVariablesJennaBee->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesJennaBee->{-ANI_FAVICON};
     $FAVICON_TYPE            = $SetupVariablesJennaBee->{-FAVICON_TYPE};
     $home_view               = $SetupVariablesJennaBee->{-HOME_VIEW};
#Mail settings 
     $mail_from               = $SetupVariablesJennaBee->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesJennaBee->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesJennaBee->{-MAIL_REPLYTO};
     $HTTP_HEADER_PARAMS      = $SetupVariablesJennaBee->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesJennaBee->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesJennaBee->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_URL            = $SetupVariablesJennaBee->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesJennaBee->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesJennaBee->{-LAST_UPDATE}; 
 }
elsif ($SiteName eq "MW" or
       $SiteName eq "MWDev" ) {
use MWSetup;
  my $SetupVariablesMW   = new MWSetup($UseModPerl);
     $StoreUrl                = $SetupVariablesMW->{-STORE_URL};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesMW->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesMW->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesMW->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesMW->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesMW->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesMW->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesMW->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesMW->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesMW->{-APP_LOGO_ALT};
     if ($group eq "Mentoring"){
     $home_view               = 'MentoringHomeView';
       }else{
     $home_view               = $SetupVariablesMW->{-HOME_VIEW};
     }
     $CSS_VIEW_URL            = $SetupVariablesMW->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesMW->{-LAST_UPDATE}; 
     $site_update             = $SetupVariablesMW->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from               = $SetupVariablesMW->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesMW->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesMW->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesMW->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesMW->{-FAVICON}||'/images/apis/favicon.ico';
     $ANI_FAVICON             = $SetupVariablesMW->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesMW->{-PAGE_TOP_VIEW};
}

elsif ($SiteName eq "Shanta"){
use ShantaSetup;
  my $UseModPerl = 1;
  my $SetupVariablesShanta   = new ShantaSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesShanta->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesShanta->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesShanta->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesShanta->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesShanta->{-APP_LOGO_ALT};
#    $home_view          = $SetupVariablesShanta->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesShanta->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SiteLastUpdate        = $SetupVariablesShanta->{-Site_Last_Update}; 
    $SITE_DISPLAY_NAME     = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
  }
  
elsif ($SiteName eq "ShantaWorkShop"){
use ShantaWorkShopSetup;
  my $UseModPerl = 1;
  my $SetupVariablesShantaWorkShop   = new ShantaWorkShopSetup($UseModPerl);
     $StoreUrl                = $SetupVariablesShantaWorkShop->{-STORE_URL};
     $CSS_VIEW_NAME           = $SetupVariablesShantaWorkShop->{-CSS_VIEW_NAME};
 #    $home_view            = $SetupVariablesShantaWorkShop->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesShantaWorkShop->{-HOME_VIEW};
     $AUTH_TABLE              = $SetupVariablesShantaWorkShop->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesShantaWorkShop->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesShantaWorkShop->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesShantaWorkShop->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesShantaWorkShop->{-APP_LOGO_ALT};
#    $home_view          = $SetupVariablesShantaWorkShop->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesShantaWorkShop->{-HOME_VIEW}; 
     $CSS_VIEW_URL            = $SetupVariablesShantaWorkShop->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ShantasWorkShop';
     $site_update             = $SetupVariablesShantaWorkShop>{-Site_Last_Update};
     $SiteLastUpdate          = $SetupVariablesShantaWorkShop->{-Site_Last_Update}; 
     $SITE_DISPLAY_NAME       = $SetupVariablesShantaWorkShop->{-SITE_DISPLAY_NAME};
  }
  
elsif ($SiteName eq "Skye" or
       $SiteName eq "SkyeStore") {
use SkyeFarmSetup;
  my $SetupVariablesSkyeFarm   = new SkyeFarmSetup($UseModPerl);
     $StoreUrl                = $SetupVariablesSkyeFarm->{-STORE_URL};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSkyeFarm->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSkyeFarm->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSkyeFarm->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSkyeFarm->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSkyeFarm->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSkyeFarm->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSkyeFarm->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSkyeFarm->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSkyeFarm->{-APP_LOGO_ALT};
 #    $home_view               = $SetupVariablesSkyeFarm->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesSkyeFarm->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSkyeFarm->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSkyeFarm->{-LAST_UPDATE}; 
 #Mail settings
     $site_update             = $SetupVariablesSkyeFarm->{-SITE_LAST_UPDATE};
     $mail_from               = $SetupVariablesSkyeFarm->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesSkyeFarm->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesSkyeFarm->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesSkyeFarm->{-SITE_DISPLAY_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/SkyeFarm';
  }



elsif ($SiteName eq "Organic") {
use OrganicSetup;
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
 #    $home_view            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
     $site_update             = $SetupVariablesOrganic-> {-SITE_LAST_UPDATE};
 }
elsif ($SiteName eq "SSeedSavers" or
       $SiteName eq "SSeedSaversDev" 
       ) {
use SSeedSaversSetup;
  my $SetupVariablesSSeedSavers   = new SSeedSaversSetup($UseModPerl);
     $Affiliate               = $SetupVariablesSSeedSavers->{-AFFILIATE};
     $StoreUrl                = $SetupVariablesSSeedSavers->{-STORE_URL};
     $SITE_DISPLAY_NAME       = $SetupVariablesSSeedSavers->{-SITE_DISPLAY_NAME};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSSeedSavers->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSSeedSavers->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSSeedSavers->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSSeedSavers->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSSeedSavers->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSSeedSavers->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSSeedSavers->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSSeedSavers->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSSeedSavers->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesSSeedSavers->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSSeedSavers->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSSeedSavers->{-LAST_UPDATE};   
     $site_update             = $SetupVariablesSSeedSavers->{-SITE_LAST_UPDATE};
#Mail settings
    $mail_from                = $SetupVariablesSSeedSavers->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesSSeedSavers->{-MAIL_TO};
    $mail_replyto             = $SetupVariables->{-MAIL_REPLYTO};
	  $mail_to_user             = $SetupVariablesSSeedSavers->{-MAIL_TO_USER};
	  $mail_to_member           = $SetupVariablesSSeedSavers->{-MAIL_TO_Member};
	  $mail_to_discussion       = $SetupVariablesSSeedSavers->{-MAIL_TO_DISCUSSION};
 }
elsif ($SiteName eq "Sky") {
use SkySetup;
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
 #    $home_view            = $SetupVariablesSky->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesSky->{-LAST_UPDATE};
     $site_update             = $SetupVariablesSky->{-SITE_LAST_UPDATE};
 }elsif ($SiteName eq "Sustainable" or
       $SiteName eq "SustainableDev" 
       ) {
use SustainableSetup;
  my $SetupVariablesSustainable   = new SustainableSetup($UseModPerl);
     $Affiliate               = $SetupVariablesSustainable->{-AFFILIATE};
     $SITE_DISPLAY_NAME       = $SetupVariablesSustainable->{-SITE_DISPLAY_NAME};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSustainable->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSustainable->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSustainable->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSustainable->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSustainable->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSustainable->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSustainable->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSustainable->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSustainable->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesSustainable->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSustainable->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSustainable->{-LAST_UPDATE};   
     $site_update             = $SetupVariablesSustainable->{-SITE_LAST_UPDATE};
#Mail settings
    $mail_from                = $SetupVariablesSustainable->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesSustainable->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesSustainable->{-MAIL_REPLYTO};
    $mail_to_user             = $SetupVariablesSustainable->{-MAIL_TO_USER};
    $mail_to_member           = $SetupVariablesSustainable->{-MAIL_TO_Member};
    $mail_to_discussion       = $SetupVariablesSustainable->{-MAIL_TO_DISCUSSION};
 }
 elsif ($SiteName eq "USBM") {
use USBMSetup;
  my $SetupVariablesUSBM   = new USBMSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesUSBM->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesUSBM->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesUSBM->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesUSBM->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesUSBM->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesUSBM->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesUSBM->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesUSBM->{-APP_LOGO_ALT};
 #    $home_view            = $SetupVariablesUSBM->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesUSBM->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesUSBM->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesUSBM->{-LAST_UPDATE};
     $site_update             = $SetupVariablesUSBM->{-SITE_LAST_UPDATE};
 }
elsif ($SiteName eq "WiseWoman") {
use WWSetup;
  my $SetupVariablesWiseWoman   = new WWSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesWiseWoman->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesWiseWoman->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesWiseWoman->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesWiseWoman->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesWiseWoman->{-AUTH_TABLE};
     $Affiliate               = $SetupVariablesWiseWoman->{-AFFILIATE};
     $app_logo                = $SetupVariablesWiseWoman->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesWiseWoman->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesWiseWoman->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesWiseWoman->{-APP_LOGO_ALT};
     $home_view               = $SetupVariablesWiseWoman->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesWiseWoman->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesWiseWoman->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesWiseWoman->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesWiseWoman->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesWiseWoman->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesWiseWoman->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesWiseWoman->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesWiseWoman->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesWiseWoman->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesWiseWoman->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesWiseWoman->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesWiseWoman->{-FAVICON_TYPE};
} 

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
        )],
    -SORT_FIELDS             => [qw(
        sitename
        view_name
        status
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