#!/usr/bin/perl -wT
# 	$Id: apis.cgi,v 1.6 2002/05/31 14:27:36 shanta Exp $	

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
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/CSC       
       ../HTMLTemplates/Brew
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/ECF
       ../HTMLTemplates/GRA
       ../HTMLTemplates/GrindrodProject
       ../HTMLTemplates/HE
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/SB
       ../HTMLTemplates/Todo
       ../HTMLTemplates/Default);

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

my $APP_NAME = "apis"; 
my $APP_NAME_TITLE = "Apis, Bees and Beekeeping ";
my $SiteName =  $CGI->param('site')||"SLT";
my $site_update;
my $username;
my $group;
my $CustCode =  $CGI->param('custcode') || "BMaster";
my $homeviewname ;
my $home_view; 
my $BASIC_DATA_VIEW; 
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
my $DEFAULT_CHARSET;
my $mail_to_user;
my $mail_to_member;
my $mail_to_discussion;
my $last_update = 'Sept 8, 2010';
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $SiteLastUpdate;
my $shop = 'cs';
      
use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
     $site                 = $SetupVariables->{-DATASOURCE_TYPE};
#    $SiteName 		   = $SetupVariables->{-SITE_NAME};
    $APP_NAME_TITLE        = "Apis: A beekeepers Resource";
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariables->{-HOME_VIEW};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN}||'mysql:database=shanta_forager';
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-page_left_view};
    $MySQLPW               = $SetupVariables->{-MySQLPW}||'nvidia2';
#Mail settings
    $mail_from             = $SetupVariables->{-MAIL_FROM};
    $mail_to               = $SetupVariables->{-MAIL_TO};
    $auth_mail_to          = $SetupVariables->{-MAIL_TO_AUTH};
    $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
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
    $FAVICON                = $SetupVariables->{-FAVICON};
    $ANI_FAVICON            = $SetupVariables->{-ANI_FAVICON};
    $FAVICON_TYPE          = $SetupVariables->{-FAVICON_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    my $LocalIp            = $SetupVariables->{-LOCAL_IP};
    my $site_for_search = 0;





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
     $homeviewname            = $SetupVariablesECF->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesECF->{-HOME_VIEW};
#Mail settings 
    $mail_from               = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS      = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
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
     $homeviewname            = $SetupVariablesApis->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesApis->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesApis->{-LAST_UPDATE}; 
 #Mail settings
     $site_update              = $SetupVariablesApis->{-SITE_LAST_UPDATE};
    $mail_from             = $SetupVariablesApis->{-MAIL_FROM};
    $mail_to               = $SetupVariablesApis->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesApis->{-MAIL_REPLYTO};
 }

elsif ($SiteName eq "BMaster") {
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
     $homeviewname            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = 'CoopHomeView'||$SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from               = $SetupVariablesBMaster->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBMaster->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBMaster->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = 'BeeMaster.ca Co-Op';
     $FAVICON                = $SetupVariablesBMaster->{-FAVICON};
     $ANI_FAVICON            = $SetupVariablesBMaster->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBMaster->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE          = $SetupVariablesBMaster->{-FAVICON_TYPE};
}

elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
    $homeviewname          = $SetupVariablesBrew->{-HOME_VIEW_NAME};
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
    $last_update           = $SetupVariablesBrew->{-LAST_UPDATE}; 
    $site_update           = $SetupVariablesBrew->{-SITE_LAST_UPDATE};
}
elsif ($SiteName eq "Kamasket") {
use KamasketSetup;
  my $SetupVariablesKamasket   = new KamasketSetup($UseModPerl);
     $APP_NAME_TITLE          = "Kamasket";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesKamasket->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesKamasket->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesKamasket->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesKamasket->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesKamasket->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesKamasket->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesKamasket->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesKamasket->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesKamasket->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesKamasket->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesKamasket->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesKamasket->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesKamasket->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesKamasket->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesKamasket->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesKamasket->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesKamasket->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesKamasket->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesKamasket->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesKamasket->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesKamasket->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesKamasket->{-FAVICON_TYPE};
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
elsif ($SiteName eq "GPMarket") {
use GPMSetup;
  my $SetupVariablesGRMarket   = new GRMSetup($UseModPerl);
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
      $site_update            = $SetupVariablesGRMarket->{-SITE_LAST_UPDATE};
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
} 
 
elsif ($SiteName eq "HoneyDo" or
       $SiteName eq "HoneyDoDev") {
use HoneyDoSetup;
  my $UseModPerl = 1;
  my $SetupVariablesHoneyDo   = new HoneyDoSetup($UseModPerl);
     $APP_NAME_TITLE          = "Honey Do Small Engine ";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesHoneyDo->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesHoneyDo->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesHoneyDo->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesHoneyDo->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesHoneyDo->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesHoneyDo->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesHoneyDo->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesHoneyDo->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesHoneyDo->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesHoneyDo->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesHoneyDo->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesHoneyDo->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHoneyDo->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesHoneyDo->{-MAIL_TO};
    $SITE_DISPLAY_NAME        = $SetupVariablesHoneyDo->{-SITE_DISPLAY_NAME};
    $mail_replyto             = $SetupVariablesHoneyDo->{-MAIL_REPLYTO};
 }

elsif ($SiteName eq "CertBee" or
       $SiteName eq "CertBeeDev" ) {
use CertBeeSetup;
  my $SetupVariablesCertBee   = new CertBeeSetup($UseModPerl);
     $APP_NAME_TITLE          = $SetupVariablesCertBee->{-APP_NAME_TITLE};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesCertBee->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesCertBee->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesCertBee->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesCertBee->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesCertBee->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesCertBee->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesCertBee->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesCertBee->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesCertBee->{-APP_LOGO_ALT};
     if ($group eq "Mentoring"){
     $home_view               = 'MentoringHomeView';
     $homeviewname            = $home_view;
    }else{
     $homeviewname            = $SetupVariablesCertBee->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesCertBee->{-HOME_VIEW};
     }
     $CSS_VIEW_URL            = $SetupVariablesCertBee->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesCertBee->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesCertBee->{-SITE_LAST_UPDATE};
 #Mail settings
    $mail_from                = $SetupVariablesCertBee->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesCertBee->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesCertBee->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesCertBee->{-SITE_DISPLAY_NAME};
    $FAVICON                  = '/images/apis/favicon.ico'||$SetupVariablesCertBee->{-FAVICON}||'/images/apis/favicon.ico';
    $ANI_FAVICON              = $SetupVariablesCertBee->{-ANI_FAVICON};
    $page_top_view            = $SetupVariablesCertBee->{-PAGE_TOP_VIEW};
}

elsif ($SiteName eq "WB" or
       $SiteName eq "WBDev" ) {
use WBSetup;
  my $SetupVariablesWB   = new WBSetup($UseModPerl);
     $APP_NAME_TITLE          = "Geniology";
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
     $home_view               = 'MentoringHomeView';
     $homeviewname            = $home_view;
    }else{
     $homeviewname            = $SetupVariablesWB->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesWB->{-HOME_VIEW};
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
     $APP_NAME_TITLE           = " ";
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
     $site_update              = $SetupVariablesHE->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
     $shop                     = $SetupVariablesHE->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
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
    $homeviewname          = $SetupVariablesShanta->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesShanta->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SiteLastUpdate        = $SetupVariablesShanta->{-Site_Last_Update}; 
    $SITE_DISPLAY_NAME     = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
  }

elsif ($SiteName eq "SLT") {
use SLTSetup;
  my $SetupVariablesSLT   = new SLTSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSLT->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSLT->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSLT->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSLT->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSLT->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSLT->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSLT->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSLT->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSLT->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesSLT->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSLT->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSLT->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSLT->{-LAST_UPDATE}; 
 #Mail settings
     $site_update              = $SetupVariablesSLT->{-SITE_LAST_UPDATE};
    $mail_from             = $SetupVariablesSLT->{-MAIL_FROM};
    $mail_to               = $SetupVariablesSLT->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesSLT->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME     = $SetupVariablesSLT->{-SITE_DISPLAY_NAME};
 }


elsif ($SiteName eq "OKB" or
       $SiteName eq "OKBDev" 
       ) {
use OKbeekeeperSetup;
  my $SetupVariablesOKB   = new OKbeekeeperSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesOKB->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesOKB->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesOKB->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesOKB->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesOKB->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesOKB->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesOKB->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesOKB->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesOKB->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesOKB->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesOKB->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOKB->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesOKB->{-LAST_UPDATE};   
     $site_update             = $SetupVariablesOKB->{-SITE_LAST_UPDATE};
#Mail settings
    $mail_from                = $SetupVariablesOKB->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesOKB->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesOKB->{-MAIL_REPLYTO};
	 $mail_to_user             = $SetupVariablesOKB->{-MAIL_TO_USER};
	 $mail_to_member           = $SetupVariablesOKB->{-MAIL_TO_Member};
	 $mail_to_discussion       = $SetupVariablesOKB->{-MAIL_TO_DISCUSSION};
}

 
elsif ($SiteName eq "Noop") {
use NoopSetup;
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
     $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
     $site_update             = $SetupVariablesNoop->{-SITE_LAST_UPDATE};
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
     $homeviewname            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
     $site_update             = $SetupVariablesOrganic-> {-SITE_LAST_UPDATE};
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
     $homeviewname            = $SetupVariablesSky->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesSky->{-LAST_UPDATE};
     $site_update             = $SetupVariablesSky->{-SITE_LAST_UPDATE};
 }

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
       project_code	      	=> 'Project Code',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       owner            => 'Owner',
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       abstract          => 'Subject',
       details      => 'Description',
       status           => 'Status',
       priority         => 'Priority',
       last_mod_by      => 'Last Modified By',
       last_mod_date    => 'Last Modified Date',
       comments            => 'Comments',
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
    -DATAHANDLERS => [qw(
        Email 
        Exists
        HTML
        String
        )],

    -FIELD_MAPPINGS => {
       project_code	      	=> 'Project Code',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       start_date               => 'Start Date',
       due_date                 => 'Due Date',
       abstract                 => 'Subject',
       details                  => 'Description',
       status                   => 'Status',
       priority                 => 'Priority',
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

my @DATASOURCE_FIELD_NAMES = 
    qw(
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



my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
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

    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

     details  => [
                 -DISPLAY_NAME => 'Description',
                 -TYPE         => 'textarea',
                 -NAME         => 'details',
                 -ROWS         => 8,
                 -COLS         => 42,
                 -WRAP         => 'VIRTUAL',
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
                 -VALUES       => [1..31],
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

     priority => [
                 -DISPLAY_NAME => 'Priority',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'priority',
                 -VALUES       => [sort {$a <=> $b} keys %priority],
                 -LABELS       => \%priority,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    project_code => [
        -DISPLAY_NAME => 'Project Code',
        -TYPE         => 'popup_menu',
        -NAME         => 'project_code',
        -VALUES  => [
            '',		
            'MITEGONE',
            'MITEGONE_admin',
            'MITEGONE_ProjectTraker',
            'MITEGONE_ToDo',
            'MITEGONE_ToDo',
            'ECF',
            'Extropia',
            'Extropia_HelpDesk',
            'MiteGone',
            'Mite_HelpDesk',
            'WebCT',
            'WebCT_Internal',
            '(None)',
        ]
    ],

     status => [
                 -DISPLAY_NAME => 'Status',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'status',
                 -VALUES       => [sort {$a <=> $b} keys %status],
	          	  -LABELS       => \%status,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    );


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (
      qw(project_code),
      qw(abstract ),
     [qw(start_day start_mon start_year)],
     [qw(due_day due_mon due_year)],
      qw(details),
      qw(priority),
     [qw(status)],
     qw(estimated_man_hours),
     qw(accumulative_time),
     qw(comments),
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
           -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'todo_tb',
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
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => '$APP_NAME_TITLE Delete'
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')|| $mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => '$APP_NAME_TITLE Addition'
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
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
       MiteGoneDocsView
       ApisHoneyView
       CertifiedOrganicView
       AssociateView
       MGWaverView 
       ForumsView
       ContactView
       ProductView
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
       ShantaLaptopHomeView
       GPMRulesView
       WorkShopsView

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
        abstract
        details
        start_date
        due_date
        status
        priority
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
        'project_code' => 'Project Code',
        'abstract'     => 'Subject',
        'details'      => 'Description',
        'start_date'   => 'Start Date',
        'due_date'     => 'Due Date',
        'status'       => 'Status',
        'priority'     => 'Priority',
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
        project_code
        abstract
        start_date
        due_date
        status
        priority
        )],
    -SORT_FIELDS             => [qw(
        due_date
        abstract
        start_date
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
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => '',
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
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'start_date',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'abstract',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'DESC',
	 -Debug                                  => $CGI->param('debug')||0,
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
    -HTTP_HEADER_PARAMS                     => $HTTP_HEADER_PARAMS||'test',
    -HTTP_HEADER_KEYWORDS                   => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION                => $HTTP_HEADER_DESCRIPTION,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
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
    -SITE_NAME                              => $SiteName,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -SHOP                                   =>  $shop,
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
    -ROOT_ACTION_HANDLER_DIRECTORY => "../ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() .  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();
