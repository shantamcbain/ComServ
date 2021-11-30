#!/usr/bin/perl -wT
# 	$Id: address_book.cgi,v 1.6 2006/01/11 22:10:33 shanta Exp $	

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

my $AppVer = "ver 0.01, October 12, 2021";
use strict;
BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules
               ../Modules/CPAN .);
}
use lib @dirs; 
unshift @INC, @dirs unless $INC[0] eq $dirs[0];
my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Forager
       ../HTMLTemplates/Apis
       ../HTMLTemplates/CS
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/Brew
       ../HTMLTemplates/HE
       ../HTMLTemplates/IM
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/HoneyDo
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Telemark
       ../HTMLTemplates/VitalVic              
       ../HTMLTemplates/Todo
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
#                      Application SETUP                             #
######################################################################

my $APP_NAME = "address_book";
my $APP_NAME_TITLE = "Address book";
my $SiteName =  $CGI->param('site') || "Computer System Consulting.ca";
my $SITE_DISPLAY_NAME = 'None Defined for this site.';
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
    my $MySQLPW;
    my $HTTP_HEADER_PARAMS;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $LINK_TARGET;
    my  $additonalautusernamecomments;
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $auth_search = '0';
    my $allow_mod ='1';
    my $allow_del = '1';
    my $require  = '1';
    my $require_user = '0';
    my $require_group = '0';
    my $require_user_list = '0';
    my $require_group_list = '0';
    my $last_update;
    my $site_for_search = '1';
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
    my $SiteLastUpdate;
    my $shop = 'cs';
    my $site_update;
    my $HasMembers = 0;

###############################################################################
#                                                                             #
#                            Pull valuables for global Application             #
#                                                                             #
###############################################################################
use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $APP_NAME_TITLE        = "Apis: A beekeepers Resource";
    $homeviewname          =  $SetupVariables->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN}||'mysql:database=shanta_forager';
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME}||'shanta';
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW}||'nvidia2';
#Mail settings
    my $address_book_tb    = 'address_book_tb';
    my $mail_from          = $SetupVariables->{-MAIL_FROM}; 
    my $mail_to_admin      = $SetupVariables->{-MAIL_TO_AMIN};
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
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    my $LocalIp            = $SetupVariables->{-LOCAL_IP};


my @VIEWS_SEARCH_PATH = 
    qw(Modules/Extropia/View/AddressBook
       Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/AltPower
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/Apis
       ../HTMLTemplates/AddressBook
       ../HTMLTemplates/CSC
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HE
       ../HTMLTemplates/IM
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/VitalVic
       ../HTMLTemplates/Default);

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
my $CSS_VIEW_URL;
######################################################################
#                      SET SITENAME IN SESSION                       #
######################################################################

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
my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_groups');
my $simple_search_string = $CGI->param('simple_search_string');

######################################################################
#                          SITE SETUP                                #
######################################################################

 if ($SiteName eq "ECF") {
use ECFSetup;
  my $SetupVariablesECF   = new ECFSetup($UseModPerl);
    $CSS_VIEW_URL             = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE               = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo                 = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height          = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesECF->{-APP_LOGO_ALT};
    $APP_NAME                 = $SetupVariablesECF->{-APP_NAME}||$APP_NAME;
    $homeviewname             = $SetupVariablesECF->{-HOME_VIEW_NAME};
    $home_view                = $SetupVariablesECF->{-HOME_VIEW};
    $APP_DATAFILES_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.'/ECF';
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL             = $SetupVariablesECF->{-CSS_VIEW_NAME};
#Mail settings
    $mail_from                = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesECF->{-MAIL_TO};
    $mail_to_admin            = $SetupVariablesECF->{-MAIL_TO_AMIN};
    $mail_replyto             = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS       = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $APP_NAME                 = 'ECF Client Profile' ||$APP_NAME;
    $SITE_DISPLAY_NAME        = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
     $shop                     = $SetupVariablesECF->{-SHOP};
  }
 elsif ($SiteName eq "Apis"){
use ApisSetup;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesApis->{-AUTH_TABLE};
    $mail_from               = $SetupVariablesApis->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesApis->{-MAIL_TO};
    $mail_to_admin           = $SetupVariablesApis->{-MAIL_TO_AMIN};
    $mail_replyto            = $SetupVariablesApis->{-MAIL_REPLYTO};
    $app_logo                = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesApis->{-APP_LOGO_ALT};
    $APP_NAME                = 'Apis Client Profile' ||$APP_NAME;
    $homeviewname            = 'Apis Member Profile';
    $home_view               = $SetupVariables->{-HOME_VIEW}; 
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesApis->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesApis->{-HTTP_HEADER_DESCRIPTION};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis';
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "BCHPA") { 
use BCHPASetup;
  my $SetupVariablesBCHPA  = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $page_top_view           = $SetupVariablesBCHPA->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesBCHPA->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesBCHPA->{-LEFT_PAGE_VIEW};
    $mail_from               = $SetupVariablesBCHPA->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesBCHPA->{-MAIL_TO};
    $mail_to_admin           = $SetupVariablesBCHPA->{-MAIL_TO_AMIN};
    $mail_replyto            = $SetupVariablesBCHPA->{-MAIL_REPLYTO};
    $address_book_tb         = 'bchpa_member_tb';
    $APP_NAME                = $SetupVariablesBCHPA>{-APP_NAME}||$APP_NAME;
    $APP_NAME_TITLE          = "BCHPA Members";
    $homeviewname            = 'BCHPAHomeView';
    $home_view               = $SetupVariablesBCHPA ->{-HOME_VIEW}; 
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesBCHPA->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesBCHPA->{-HTTP_HEADER_DESCRIPTION};
}  

 
elsif ($SiteName eq "BeeCoop") {
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
     $homeviewname            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = 'CoopHomeView'||$SetupVariablesBMaster->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
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

 
elsif ($SiteName eq "BMaster" or
       $SiteName eq "BMasterDev") {
use BMasterSetup;
  my $UseModPerl = 0;
  my $SetupVariablesBMaster   = new BMasterSetup($UseModPerl);
     $APP_NAME_TITLE          = "Beemaster.ca ";
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
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.'/BMaster';
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
     $APP_DATAFILES_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.'\GRMarket';
} 
 
elsif ($SiteName eq "Organic") {
use OrganicSetup;
  my $UseModPerl = 0;
  my $SetupVariablesOrganic   = new OrganicSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesOrganic->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesOrganic->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesOrganic->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $mail_from               = $SetupVariablesOrganic->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesOrganic->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesOrganic->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesOrganic->{-MAIL_REPLYTO};
     $AUTH_TABLE              = $SetupVariablesOrganic->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesOrganic->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesOrganic->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesOrganic->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesOrganic->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $APP_NAME                = 'OrganicFarming Member Profile' ||$APP_NAME;
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic';
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $SetupVariablesENCY     = new  ENCYSetup($UseModPerl);
     $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesENCY->{-AUTH_TABLE};
     $mail_from               = $SetupVariablesENCY->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesENCY->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesENCY->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesENCY->{-MAIL_REPLYTO};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesENCY->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesENCY->{-HTTP_HEADER_DESCRIPTION};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ENCY';
     $APP_NAME                = 'ENCY Member Profile' ||$APP_NAME;
     $SITE_DISPLAY_NAME       = $SetupVariablesENCY->{-SITE_DISPLAY_NAME};
    
 }
elsif ($SiteName eq "AltPower") {
use AltPowerSetup;
  my $UseModPerl = 1;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesAltPower->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesAltPower->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesAltPower->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesAltPower=>{-CSS_VIEW_NAME};
     $CSS_VIEW_URL            = $SetupVariablesAltPower->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesAltPower->{-AUTH_TABLE};
     $mail_from               = $SetupVariablesAltPower->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesAltPower->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesAltPower->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesAltPower->{-MAIL_REPLYTO};
     $app_logo                = $SetupVariablesAltPower->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesAltPower->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesAltPower->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesAltPower->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesAltPower->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesAltPower->{-HOME_VIEW};
     $APP_NAME                = 'AltPower Member Profile' ||$APP_NAME;
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "AltPowerDev") {
use AltPowerSetup;
  my $UseModPerl = 1;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesAltPower->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesAltPower->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesAltPower->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesAltPower=>{-CSS_VIEW_NAME};
     $CSS_VIEW_URL            = $SetupVariablesAltPower->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesAltPower->{-AUTH_TABLE};
     $mail_from               = $SetupVariablesAltPower->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesAltPower->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesAltPower->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesAltPower->{-MAIL_REPLYTO};
     $app_logo                = $SetupVariablesAltPower->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesAltPower->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesAltPower->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesAltPower->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesAltPower->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesAltPower->{-HOME_VIEW};
     $APP_NAME                = 'AltPower Member Profile' ||$APP_NAME;
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
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
elsif ($SiteName eq "CSC"or
       $SiteName eq "CSCDev"){
use CSCSetup;
  my $UseModPerl = 1;
  my $SetupVariablesCSC  = new CSCSetup($UseModPerl);
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $homeviewname               = 'HelpDeskHomeView';
    $home_view                  = $SetupVariablesCSC->{-HOME_VIEW};
    $BASIC_DATA_VIEW            = $SetupVariablesCSC->{-BASIC_DATA_VIEW};
    $page_top_view              = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view           = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view             = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
 #Mail settings 
    $mail_to_admin              = $SetupVariablesCSC->{-MAIL_TO_AMIN};
    $mail_from                  = $SetupVariablesCSC->{-MAIL_FROM};
    $mail_to                    = $SetupVariablesCSC->{-MAIL_TO};
    $mail_replyto               = $SetupVariablesCSC->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME              = $SetupVariablesCSC->{-CSS_VIEW_NAME}||'blank';
    $app_logo                   = $SetupVariablesCSC->{-APP_LOGO};
    $app_logo_height            = $SetupVariablesCSC->{-APP_LOGO_HEIGHT};
    $app_logo_width             = $SetupVariablesCSC->{-APP_LOGO_WIDTH};
    $app_logo_alt               = $SetupVariablesCSC->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL             = $SetupVariablesCSC->{-IMAGE_ROOT_URL};
    $DOCUMENT_ROOT_URL          = $SetupVariablesCSC->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET                = $SetupVariablesCSC->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS         = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET            = $SetupVariablesCSC->{-DEFAULT_CHARSET};
if ($SiteName eq "CSCDev"
       ) { $AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
$address_book_tb    = 'csc_client_tb';
       } else {
         $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
       }
    $DEFAULT_CHARSET            = $SetupVariablesCSC->{-DEFAULT_CHARSET};
    $site                       = $SetupVariablesCSC->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariablesCSC->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariablesCSC->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariablesCSC->{-APP_DATAFILES_DIRECTORY};
    $HTTP_HEADER_KEYWORDS       = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS         = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION    = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL               = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME          = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
    $APP_NAME                   = 'CSC Client Profile' ||$APP_NAME;
     
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
    $shop                     = $SetupVariablesDemo->{-SHOP};
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
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariablesDemo->{-GLOBAL_DATAFILES_DIRECTORY};

}

elsif ($SiteName eq "IM" or
       $SiteName eq "IMDev") {
use HESetup;
  my $SetupVariablesIM   = new HESetup($UseModPerl);
     $APP_NAME_TITLE           = " ";
     $HTTP_HEADER_KEYWORDS     = $SetupVariablesIM->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS       = $SetupVariablesIM->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION  = $SetupVariablesIM->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME            = $SetupVariablesIM->{-CSS_VIEW_NAME};
     $AUTH_TABLE               = $SetupVariablesIM->{-AUTH_TABLE};
     $app_logo                 = $SetupVariablesIM->{-APP_LOGO};
     $app_logo_height          = $SetupVariablesIM->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesIM->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesIM->{-APP_LOGO_ALT};
     $homeviewname             = $SetupVariablesIM->{-HOME_VIEW_NAME};
     $home_view                = $SetupVariablesIM->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesIM->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesIM->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesIM->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesIM->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesIM->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesIM->{-MAIL_REPLYTO};
     $shop                     = $SetupVariablesIM->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesIM->{-SITE_DISPLAY_NAME};
     $homeviewname             =$home_view;
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
     $mail_from               = $SetupVariablesNoop->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesNoop->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesNoop->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesNoop->{-MAIL_REPLYTO};
     $app_logo                = $SetupVariablesNoop->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesNoop->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesNoop->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesNoop->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesNoop->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesNoop->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesNoop->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
     $APP_NAME                = 'Orgnaic Co-op Member Profile' ||$APP_NAME;
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
     $mail_to_admin           = $SetupVariablesSky->{-MAIL_TO_AMIN};
     $mail_from               = $SetupVariablesSky->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesSky->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesSky->{-MAIL_REPLYTO};
     $homeviewname            = $SetupVariablesSky->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Sky'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $APP_NAME                = 'Skye Farm Client' ||$APP_NAME;
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
     $mail_from               = $SetupVariablesTelMark->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesTelMark->{-MAIL_TO};
     $mail_to_admin           = $SetupVariablesTelMark->{-MAIL_TO_AMIN};
     $mail_replyto            = $SetupVariablesTelMark->{-MAIL_REPLYTO};
     $app_logo                = $SetupVariablesTelMark->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesTelMark->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesTelMark->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesTelMark->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesTelMark->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesTelMark->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesTelMark->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
     $APP_NAME                = 'TelMark_Member_Profile' ||$APP_NAME;
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
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
#     $site_update              = $SetupVariablesSLT->{-SITE_LAST_UPDATE};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/SLT';
    $mail_from             = $SetupVariablesSLT->{-MAIL_FROM};
    $mail_to               = $SetupVariablesSLT->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesSLT->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME     = $SetupVariablesSLT->{-SITE_DISPLAY_NAME};
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
     $home_view            = $SetupVariablesUSBM->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesUSBM->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesUSBM->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesUSBM->{-LAST_UPDATE};
     $site_update             = $SetupVariablesUSBM->{-SITE_LAST_UPDATE};
 
}
if ($username = 'Shanta'){
   $allow_mod     ='1';
   $allow_del     = '1';
   $auth_search   = '0';
   $require       = '0';
   $require_user   = '0';
   $require_group = '0';
}

if ($CGI->param('embed')==1){
   $page_top_view    = "EmbedPageTopView";
   $page_bottom_view = "";
   $allow_mod        ='0';
   $allow_del        = '0';
   $auth_search      = '0';
   $require          = '0';
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
	    -FILE                       => $auth
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
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -SUBJECT => 'Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to_admin,
    -SUBJECT  => 'Registration Notification'
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
                lname
                fname
                email
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
                lname
                fname
                email
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
        sitename
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
        chat
        url
        products
        username
        company_name
        title
        department
        username_of_poster
        group_of_poster
        date_time_posted
);

my %products;
 if  ( $group eq "ECF_admin"  ||
       $group eq "Apis_admin" ||
       $group eq "OKB_admin"
       ){   
     %products = (
      Extraction  => 'Custom Extraction',
      Honey       => 'Honey',
      None        => 'No products',
      Retired     => 'Retired',
      Hobby       => 'Back Yard Hobbyist',
      Nukes       => 'Nucs',
      Package     => 'Custom Packaging',
      Pollinator  => 'Pollination Products',
      Pollen      => 'Pollen',
      Queens      => 'Queens',
      Wax         => 'Wax',
    );
}elsif ( $group eq "CSC_admin" ||
         $SiteName eq "CSC" 
       ){
      %products = (
        hosting   => 'Web Hosting',
        app_host  => 'Application Hosting',
        Perl      => 'Perl programing',
        );
        
}else{
    %products = (
       None => 'None',
       );
}
my %site_code;
if ( $group eq "CSC_admin" ||
         $SiteName eq "CSC" 
       ){
      %site_code = (
       $SiteName  => $SiteName,
        Altpower  => 'Alternat Power',
        Apis      => 'Apis beekeepig',
        Brew      => 'Brewing',
        CSC       => 'Computer System Consultin.ca',
        CS        => 'Country Stores',
        Demo      => " Demo",
        Forager   => 'Forager.com',
        OKB       => 'Okanagan Beekeepers',
        Organic   => 'Organic Farming',
        Stawns    => "Stawn's Honey",
        VitalVic  => 'Vital Victoria',
        );
        
}else{
    %site_code = (
       $SiteName => $SiteName,
       );
}
my $years_as;

if  ( $SiteName eq "ECF"  || 
      $SiteName eq "Apis" ||
      $SiteName eq "OKB" 
      ){
     $years_as  = 'Active years as a bee keeper';
}elsif( $SiteName eq "CSC" 
        ){
       
     $years_as  = 'Active years as a Programer';

}else{
      $years_as = 'Active years as a Member';
}

my %category;
if  ( $group eq "ECF_admin" || 
      $group eq "Apis_admin"
     ) {
%category =   (
       Guest      => 'Guest',
       Cust       => 'Customer',
       HCust      => 'Honey Customer',
       PCust      => 'Pollination Customer',
       supplier   => 'Supplier',
       Cust       => 'Customer',
       Beekeeper  => 'Bee Keeper',
    );
}elsif( $group eq "AltPower_admin" ||
        $SiteName eq "AltPower" ){
  (
       Guest                       => 'Guest',
       Member                      => 'Member',
       Supplier                    => 'Suppler',
       Publisher                   => 'Publisher',       
  );

}elsif( $group eq "CSC_admin" ||
        $SiteName eq "CSC" ){
        %category =
        (
          Guest                       => 'Guest',
          Member                      => 'Member',
          Supplier                    => 'Suppler',
          CSC_admin                   => 'CSC_Admin',       
        );
}else{%category =   (
       author                    => 'Author',
       Guest                       => 'Guest',
       Member                      => 'Member',
       Supplier                    => 'Suppler',
       Publisher                   => 'Publisher',       
       Customer                    => 'Customer',
       Site_Contact                    => 'Contact',
       Doc                         => 'Physician',
      );
}
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (1900..2025);
my %days  = ();
$days{$_} = $_ for (1..31);

my %BASIC_INPUT_WIDGET_DEFINITIONS = (
    category => [
        -DISPLAY_NAME => 'Category',
        -TYPE         => 'popup_menu',
        -NAME         => 'category',
                 -VALUES       => [sort {$a <=> $b} keys %category],
                 -LABELS       => \%category,
                 -INPUT_CELL_COLSPAN => 3, 
    ],

     sitename => [
        -DISPLAY_NAME => 'Site Name *',
        -TYPE         => 'popup_menu',
        -NAME         => 'sitename',
                 -VALUES       => [sort {$a <=> $b} keys %site_code],
                 -LABELS       => \%site_code,
                 -INPUT_CELL_COLSPAN => 3, 
    ],

    products => [
                 -DISPLAY_NAME => 'Products You Produce',
                 -TYPE         => 'checkbox_group',
                 -NAME         => 'products',
                 -VALUES       => [sort {$a <=> $b} keys %products],
                 -LABELS       => \%products,
                 -INPUT_CELL_COLSPAN => 3,
                ],
    fname => [
        -DISPLAY_NAME => 'First Name *',
        -TYPE         => 'textfield',
        -NAME         => 'fname',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    lname => [
        -DISPLAY_NAME => 'Last Name *',
        -TYPE         => 'textfield',
        -NAME         => 'lname',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     birth_day => [
                 -DISPLAY_NAME => 'Birth Date',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'birth_day',
                 -VALUES       => [1..31],
                ],

     birth_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'birth_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     birth_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'birth_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],
    years => [
        -DISPLAY_NAME => $years_as,
        -TYPE         => 'textfield',
        -NAME         => 'years',
        -SIZE         => 4,
        -MAXLENGTH    => 4
    ],

    email => [
        -DISPLAY_NAME => 'Email *',
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
        -DISPLAY_NAME => 'Postal Code',
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

     chat => [
        -DISPLAY_NAME => 'Chat links',
        -TYPE         => 'textfield',
        -NAME         => 'chat',
        -SIZE         => 30,
        -MAXLENGTH    => 150
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
if ($username eq 'Shanta'){
     }
else {
 %BASIC_INPUT_WIDGET_DEFINITIONS."   username => [
        -DISPLAY_NAME => 'username',
        -TYPE         => 'popup_menu',
        -NAME         => 'username',
        -VALUES       => $username,
    ],"
     }
 
my @BASIC_INPUT_WIDGET_DISPLAY_ORDER;

if ($group eq 'BCHPA_admin'){
 
 @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
       qw(fname),
       qw(lname),
       qw(username),
#      [qw(birth_day birth_mon birth_year)],
       qw(company_name),   
       qw(phone),   
       qw(email),   
       qw(address1),
       qw(address2),
       qw(city),
       qw(prov),
       qw(zip),
       qw(country),
       qw(fax),
       qw(mobile),
       qw(url),
       qw(years),
       qw(category),
       qw(products),
       qw(comments),
);
}elsif ($group eq 'CSC_admin'
         ){

 @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
       qw(sitename),   
       qw(username),
       qw(category),
       qw(fname),
       qw(lname),
       [qw(birth_day birth_mon birth_year)],
       qw(company_name),   
       qw(phone),   
       qw(email),
       qw(chat),   
       qw(address1),
       qw(address2),
       qw(city),
       qw(prov),
       qw(zip),
       qw(country),
       qw(fax),
       qw(mobile),
       qw(url),
       qw(years),
       qw(products),
       qw(comments),
);  

}elsif ($simple_search_string eq 'BCHPA_contact' ||
        $simple_search_string eq 'OBC_contact'||
        $simple_search_string eq 'ECF_contact'||
        $simple_search_string eq 'Apis_contact'||
        $simple_search_string eq 'BMaster_contact'||
        $simple_search_string eq 'Brew_contact'||
        $simple_search_string eq 'ENCY_contact'||
        $simple_search_string eq 'Marts_contact'||
        $simple_search_string eq 'CSPS_contact'
         ){

 @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
       qw(fname),
       qw(lname),
       qw(company_name),   
       qw(phone),   
       qw(email),   
       qw(address1),
       qw(address2),
       qw(city),
       qw(prov),
       qw(zip),
       qw(country),
);
}elsif ($simple_search_string eq 'CSC_contact'){     
 @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (      
       qw(fname),
       qw(lname),
       qw(company_name),   
       qw(phone),   
       qw(email),   
       qw(chat),   
       qw(address1),
       qw(address2),
       qw(city),
       qw(prov),
       qw(zip),
       qw(country),
      );
 
}else{
 @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
       qw(sitename),   
       qw(username),
       qw(category),
       qw(fname),
       qw(lname),
       [qw(birth_day birth_mon birth_year)],
       qw(company_name),   
       qw(phone),   
       qw(email),   
       qw(chat),   
       qw(address1),
       qw(address2),
       qw(city),
       qw(prov),
       qw(zip),
       qw(country),
       qw(fax),
       qw(mobile),
       qw(url),
       qw(years),
       qw(products),
       qw(comments),
);
}

my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS   => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (
    -TYPE                       => 'File', 
    -FILE                       => $APP_DATAFILES_DIRECTORY/$APP_NAME,
    -FIELD_DELIMITER            => '|',
    -COMMENT_PREFIX             => '#',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -COMMENT_PREFIX             => '#',
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['record_id'],
    -FIELD_TYPES                => {
        record_id        => 'Autoincrement'
    },
);
}
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => $address_book_tb,
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);

}
#my @BASIC_DATASOURCE_CONFIG_PARAMS = (
#    -TYPE                       => 'File', 
#    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
#    -FIELD_DELIMITER            => '|',
#    -COMMENT_PREFIX             => '#',
#    -CREATE_FILE_IF_NONE_EXISTS => 1,
#    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
#    -KEY_FIELDS                 => ['record_id'],
#    -FIELD_TYPES                => {
#        record_id        => 'Autoincrement'
#    },
#);

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
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => "$APP_NAME_TITLE Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')|| $mail_from,
    -TO       => $mail_to_admin || $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => "$SiteName $APP_NAME_TITLE Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to_admin || $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => "$SiteName $APP_NAME_TITLE Modification"
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

my @VALID_VIEWS = qw(
       ApisCSSView
       BCHPACSSView
       ContactView
    CSSView
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
    FooterPubNavView
       ApisHomeView
       ApisProductView
       AssociateView
       MGWaverView
       ForumsView
       BCHPAHomeView
       ApisHoneyView
       ECFProductView
       PrivacyView
       ProfileHomeView
       ProductView
       BrewRecipeView
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
    -HOME_VIEW               => 'ProfileHomeView'|| $home_view,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
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
    -ENABLE          => $CGI->param('embed') || 0
);

my @VIEW_FILTERS_CONFIG_PARAMS = (
     \@HTMLIZE_FILTER_CONFIG_PARAMS,
     \@CHARSET_FILTER_CONFIG_PARAMS,
     \@EMBED_FILTER_CONFIG_PARAMS
); 

######################################################################
#                      ACTION/WORK-FLOW SETUP                         #
######################################################################

my @ACTION_HANDLER_LIST; 
 if ($username eq 'Shanta'){
  @ACTION_HANDLER_LIST =   qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction
       Default::ProcessConfigurationAction
       Default::CheckForLogicalConfigurationErrorsAction
       Default::DisplaySessionTimeoutErrorAction
       Default::PerformLogoffAction
       Default::PerformLogonAction
       CSC::PopulateInputWidgetDefinitionListWithUsernameWidgetAction

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
       	
      );}
      else{
    @ACTION_HANDLER_LIST =   qw(
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
}
# add plug ins here if any
my %ACTION_HANDLER_PLUGINS =
    (
    );


my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_DELETIONS_FLAG                   => $allow_del,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 0,
    -ALLOW_MODIFICATIONS_FLAG               => $allow_mod,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ProfileSubMenuView',
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
    -DOMAIN_NAME                            => $HostName,
    -GROUP                                  => $group,
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
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -KEY_FIELD                              => 'record_id',
    -LAST_UPDATE                            => $last_update,
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
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => $auth_search,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => $auth_search,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $require_user,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => $require_group,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => $allow_del,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => $allow_del,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => $require_user_list,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => $require_group_list,
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG        => $site_for_search,
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -SITENAME                               => $SiteName,
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
    -SHOP                                   =>  $shop,
    -PAGE_TOP_VIEW           => $page_top_view ,
    -LEFT_PAGE_VIEW          => $page_left_view,
    -PAGE_LEFT_VIEW          => $page_left_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
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
 
