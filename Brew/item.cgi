#!/usr/bin/perl -wT
my $AppVer = "ver 1.01, Dec 13, 2006";
# 	$Id: url.cgi,v 1.7 2004/01/25 20:11:35 shanta Exp $	
#CSC file location /cgi-bin/CSC
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


# not Email for ECF cc to nother has been disabled. enable before upload.
use strict;

BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules/
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

#my $site = 'file';
my $site = 'MySQL';

my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/Brew
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/ECF
       ../HTMLTemplates/Extropia
       ../HTMLTemplates/Forager
       ../HTMLTemplates/Fly
       ../HTMLTemplates/HE
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/IM
       ../HTMLTemplates/Organic
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HoneyDo
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/Todo
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
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x$/);
}

######################################################################
#                          SITE SETUP                             #
######################################################################

my $APP_NAME = "url"; 
my $SiteName =  $CGI->param('site') || "Apis";
my $APP_NAME_TITLE = "Links Database";
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
    my $mail_cc;
    my $app_logo;
    my $app_logo_height;
    my $app_logo_width;
    my $app_logo_alt;
    my $IMAGE_ROOT_URL; 
    my $DOCUMENT_ROOT_URL;
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
    my $mail_to_admin;
    my $mail_to_discussion;
    my $last_update;
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $site_update;
    my $shop ;
    my $url_tb;
    my $HasMembers = 0;
    
use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
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
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $DATAFILES_DIRECTORY = $APP_DATAFILES_DIRECTORY;
    $site_session = $DATAFILES_DIRECTORY.'/Sessions';
    $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
    my $LocalIp            = $SetupVariables->{-LOCAL_IP};
    my  $FAVICON                = $SetupVariables->{-FAVICON};
    my $ANI_FAVICON            = $SetupVariables->{-ANI_FAVICON};
    my $FAVICON_TYPE          = $SetupVariables->{-FAVICON_TYPE};

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
my $CSS_VIEW_URL ;

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
#$CGI->param('Nav_link')||
my $Nav_link =   '0';
    $url_tb = "item_tb";
my $Nav_link = $CGI->param('Nav_link')|| '0';


if ($Nav_link = "1"){
    $url_tb = "brew_item_list_tb";
}else{
    $url_tb = "url_tb";
}


my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');


######################################################################
#                          SITE SETUP                                #
######################################################################

if ($SiteName eq "BCHPA") { 
use BCHPASetup;
  my $SetupVariablesBCHPA  = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesBCHPA->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesBCHPA->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBCHPA->{-LEFT_PAGE_VIEW};
    $APP_NAME_TITLE        = "British Columbia Honey Producers Association";
    $homeviewname          = 'BCHPAHomeView';
    $home_view             = $SetupVariablesBCHPA ->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesBCHPA->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "Aktiv" or
       $SiteName eq "AktivDev") {
use AktivSetup;
  my $UseModPerl = 0;
  my $SetupVariablesAktiv   = new AktivSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS      = $SetupVariablesAktiv->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS        = $SetupVariablesAktiv->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION   = $SetupVariablesAktiv->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME             = $SetupVariablesAktiv->{-CSS_VIEW_NAME};
     $AUTH_TABLE                = $SetupVariablesAktiv->{-AUTH_TABLE};
     $mail_from                 = $SetupVariablesAktiv->{-MAIL_FROM};
     $mail_to                   = $SetupVariablesAktiv->{-MAIL_TO};
     $mail_to_admin             = $SetupVariablesAktiv->{-MAIL_TO_AMIN};
     $mail_replyto              = $SetupVariablesAktiv->{-MAIL_REPLYTO};
     $app_logo                  = $SetupVariablesAktiv->{-APP_LOGO};
     $app_logo_height           = $SetupVariablesAktiv->{-APP_LOGO_HEIGHT};
     $app_logo_width            = $SetupVariablesAktiv->{-APP_LOGO_WIDTH};
     $app_logo_alt              = $SetupVariablesAktiv->{-APP_LOGO_ALT};
     $homeviewname              = $SetupVariablesAktiv->{-HOME_VIEW_NAME};
     $home_view                 = $SetupVariablesAktiv->{-HOME_VIEW};
     $CSS_VIEW_URL              = $SetupVariablesAktiv->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY   = $SetupVariablesAktiv->{-APP_DATAFILES_DIRECTORY};
     $SITE_DISPLAY_NAME         = $SetupVariablesAktiv->{-SITE_DISPLAY_NAME};
     $last_update               = $SetupVariablesAktiv->{-LAST_UPDATE}; 
     $last_update          = $SetupVariablesAktiv->{-SITE_LAST_UPDATE}; 
     $APP_NAME_TITLE            ='Adventures';
 }

 
elsif ($SiteName eq "BMaster" or
       $SiteName eq "BMasterDev") {
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
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $site_update              = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesBMaster->{-SHOP};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis'; 
 }
 
 
elsif ($SiteName eq "BeeCoop") {
use BMasterSetup;
  my $UseModPerl = 0;
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
     $last_update             = $SetupVariablesBMaster->{-SITE_LAST_UPDATE}; 
 #Mail settings
     $mail_from               = $SetupVariablesBMaster->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesBMaster->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesBMaster->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = 'BeeMaster.ca Co-Op';
     $FAVICON                = $SetupVariablesBMaster->{-FAVICON};
     $ANI_FAVICON            = $SetupVariablesBMaster->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesBMaster->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE          = $SetupVariablesBMaster->{-FAVICON_TYPE};
    $site_update              = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesBMaster->{-SHOP};
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
     $url_tb               = 'brew_item_list_tb';
}

 elsif ($SiteName eq "CS") {
use CSSetup;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesCS->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesCS->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesCS->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesCS->{-AUTH_TABLE};
     $APP_NAME_TITLE           = "Country Stores";
     $app_logo                = $SetupVariablesCS->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesCS->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesCS->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesCS->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesCS->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesCS->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesCS->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesCS->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesCS->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesCS->{-ANI_FAVICON};
     $FAVICON_TYPE            = $SetupVariablesCS->{-FAVICON_TYPE};
} 
 elsif ($SiteName eq "CertBee" or
       $SiteName eq "CertBeeDev" ) {
use CertBeeSetup;
  my $UseModPerl = 0;
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
    $site_update              = $SetupVariablesCertBee->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesCertBee->{-SHOP};
     }
     $CSS_VIEW_URL            = $SetupVariablesCertBee->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesCertBee->{-LAST_UPDATE}; 
 #Mail settings
    $mail_from                = $SetupVariablesCertBee->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesCertBee->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesCertBee->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesCertBee->{-SITE_DISPLAY_NAME};
    $FAVICON                  = '/images/apis/favicon.ico'||$SetupVariablesCertBee->{-FAVICON}||'/images/apis/favicon.ico';
    $ANI_FAVICON              = $SetupVariablesCertBee->{-ANI_FAVICON};
    $page_top_view            = $SetupVariablesCertBee->{-PAGE_TOP_VIEW};
}

elsif ($SiteName eq "ECF"||
     $SiteName eq "ECFDev") { 
use ECFSetup;
  my $SetupVariablesECF  = new  ECFSetup($UseModPerl);
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
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
#    $mail_cc               = 'Norlandbeekeepers@yahoogroups.com';
    $CSS_VIEW_URL          = $SetupVariablesECF->{-CSS_VIEW_NAME};
	if ($CGI->param('droplist')                                                                   ){
	$mail_cc = '' ;
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ECF'; 
}
    $site_update              = $SetupVariablesECF->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesECF->{-SHOP};
}
elsif ($SiteName eq "Apis" ||
     $SiteName eq "ApisDev") {
use ApisSetup;
  my $UseModPerl = 0;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesApis->{-APP_LOGO_ALT};
    $mail_from             = $SetupVariablesApis->{-MAIL_FROM};
    $mail_to               = $SetupVariablesApis->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesApis->{-MAIL_REPLYTO};
 #   $mail_cc               = 'Norlandbeekeepers@yahoogroups.com';
    $homeviewname          =  $SetupVariablesApis->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesApis->{-HOME_VIEW};
    $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis'; 

	if ($CGI->param('droplist')){
	$mail_cc = 'shanta@forager.com' ;
	}
   if  ($CGI->param('Nav_link')){
	$mail_cc = 'shanta2shanta.org' ;
	}
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesApis->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesApis->{-SHOP};
}
 elsif ($SiteName eq "CS") {
use CSSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesCS->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesCS->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesCS->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesCS->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesCS->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesCS->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesCS->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesCS->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesCS->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesCS->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesCS->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesCS->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesCS->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesCS->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesCS->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesCS->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesCS->{-PAGE_TOP_VIEW};
     $page_left_view          = $SetupVariablesCS->{-page_left_view};
     $FAVICON_TYPE            = $SetupVariablesCS->{-FAVICON_TYPE};
	if ($CGI->param('droplist')){
	$mail_cc = 'shanta@countrystores.ca' ;
	}
   if  ($CGI->param('Nav_link')){
	$mail_cc = 'csc@computersystemconsulting.ca' ;
	}
} 

elsif ($SiteName eq "eXtropia") {
use eXtropiaSetup;
  my $UseModPerl = 0;
  my $SetupVariableseXtropia   = new eXtropiaSetup($UseModPerl);
     $APP_NAME_TITLE          = "URL";
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
	if ($CGI->param('droplist')){
	$mail_cc = 'shanta@forager.com' ;
	}
   if  ($CGI->param('Nav_link')){
	$mail_cc = 'shanta2shanta.org' ;
	}
    $SITE_DISPLAY_NAME       = $SetupVariableseXtropia->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariableseXtropia->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariableseXtropia->{-SHOP};
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
    $SITE_DISPLAY_NAME       = $SetupVariablesFly->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesFly->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesFly->{-SHOP};
}

elsif ($SiteName eq "HE" or
       $SiteName eq "HEDev") {
use HESetup;
  my $UseModPerl = 0;
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
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesHE->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesHE->{-SHOP};
}

elsif ($SiteName eq "IM" or
       $SiteName eq "IMDev") {
use IMSetup;
  my $SetupVariablesIM   = new IMSetup($UseModPerl);
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
     $mail_from               = $SetupVariablesOrganic->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesOrganic->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesOrganic->{-MAIL_REPLYTO};
     $mail_cc                 = 'organic@organicfarming.ca';
     $homeviewname            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $APP_NAME_TITLE          = "Organic Farming";
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesOrganic->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesOrganic->{-SHOP};
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
    $APP_NAME_TITLE          = "Shanta's URLS";
    $home_view               = $SetupVariablesShanta->{-HOME_VIEW}; 
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SITE_DISPLAY_NAME       = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesShanta->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesShanta->{-SHOP};
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
     $mail_from               = $SetupVariablesSky->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesSky->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesSky->{-MAIL_REPLYTO};
     $homeviewname            = $SetupVariablesSky->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $APP_NAME_TITLE          = "Sky Farms";
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Sky'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesSky->{-LAST_UPDATE};
    $site_update              = $SetupVariablesSky->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesSky->{-SHOP};
}
elsif ($SiteName eq "TelMark") {
use TelMarkSetup;
  my $UseModPerl = 0;
  my $SetupVariablesTelMark   = new TelMarkSetup($UseModPerl);
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
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
    $APP_DATAFILES_DIRECTORY    = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
 	if ($CGI->param('droplist')){
	$mail_cc = '' ;
   }
    $site_update              = $SetupVariablesTelMark->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesTelMark->{-SHOP};
}

elsif ($SiteName eq "CSC" or	
       $SiteName eq "CSCDev") {
use CSCSetup;
  my $SetupVariablesCSC       = new  CSCSetup($UseModPerl);
    $AUTH_TABLE              = $SetupVariablesCSC ->{-AUTH_TABLE};
    $APP_NAME_TITLE          = "Computer System Consulting.ca";
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
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesCSC->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesCSC->{-SHOP};
}

elsif ($SiteName eq "CSCRecy" ) {
use CSCSetup;
 my $UseModPerl = 1;
  my $SetupVariablesCSCRecy   = new  CSCSetup($UseModPerl);
     $SITE_DISPLAY_NAME        = $SetupVariablesCSCRecy->{-SITE_DISPLAY_NAME};
   $APP_NAME_TITLE           = "CSC Recycling";
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesCSCRecy->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesCSCRecy->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCSCRecy->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL             = $SetupVariablesCSCRecy->{-CSS_VIEW_NAME};
    $CSS_VIEW_NAME            = $SetupVariablesCSCRecy->{-CSS_VIEW_NAME};
    $page_top_view            = $SetupVariablesCSCRecy->{-PAGE_TOP_VIEW};
    $page_bottom_view         = $SetupVariablesCSCRecy->{-PAGE_BOTTOM_VIEW};
    $page_left_view           = $SetupVariablesCSCRecy->{-LEFT_PAGE_VIEW};
    $homeviewname             = $SetupVariablesCSCRecy->{-HOME_VIEW_NAME};
    $site_update              = $SetupVariablesCSCRecy->{-SITE_LAST_UPDATE};
    $app_logo                 = $SetupVariablesCSCRecy->{-APP_LOGO};
    $shop                     = $SetupVariablesCSCRecy->{-SHOP};
    $app_logo_height          = $SetupVariablesCSCRecy->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesCSCRecy->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesCSCRecy->{-APP_LOGO_ALT};
     $FAVICON                = $SetupVariablesCSCRecy->{-FAVICON};
     $ANI_FAVICON            = $SetupVariablesCSCRecy->{-ANI_FAVICON};
     $FAVICON_TYPE          = $SetupVariablesCSCRecy->{-FAVICON_TYPE};
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
    $SITE_DISPLAY_NAME       = $SetupVariablesSQL->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesSQL->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesSQL->{-SHOP};
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
     $APP_NAME_TITLE          = "Forager ToDo's";
     $mail_to                 = $SetupVariablesForager->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesForager->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Forager'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesForager->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesForager->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesForager->{-SHOP};
 }


 
elsif ($SiteName eq "CSPS") {
use CSPSSetup;
  my $SetupVariablesCSPS   = new  CSPSSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesCSPS->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesCSPS->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesCSPS->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesCSPS->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesCSPS->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesCSPS->{-APP_LOGO_ALT};
    $CSS_VIEW_URL          = $SetupVariablesCSPS->{-CSS_VIEW_NAME};
    $APP_NAME_TITLE        = "Shanta's CSPS Calendar.";
    $HTTP_HEADER_KEYWORDS  = $SetupVariablesCSPS->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSPS->{-HTTP_HEADER_DESCRIPTION};
   $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CSPS'; 
    $SITE_DISPLAY_NAME       = $SetupVariablesCSPS->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesCSPS->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesCSPS->{-SHOP};
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
    $SITE_DISPLAY_NAME       = $SetupVariablesGen->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesGen->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesGen->{-SHOP};
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
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
    $site_update              = $SetupVariablesAltPower->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesAltPower->{-SHOP};
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
    $site_update              = $SetupVariablesDemo->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesDemo->{-SHOP};

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
    $site_update              = $SetupVariablesENCY->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesENCY->{-SHOP};
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
 #Mail settings
     $mail_from                = $SetupVariablesHoneyDo->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesHoneyDo->{-MAIL_TO};
    $SITE_DISPLAY_NAME        = $SetupVariablesHoneyDo->{-SITE_DISPLAY_NAME};
    $mail_replyto             = $SetupVariablesHoneyDo->{-MAIL_REPLYTO};
    $site_update              = $SetupVariablesHoneyDo->{-SITE_LAST_UPDATE};
    $shop                     = $SetupVariablesHoneyDo->{-SHOP};
 }




#$page_left_view = "LeftPageView";
my $allowmod;

if ($username eq "Shanta"){
$allowmod = 0;
}else{
$allowmod = 1;
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
    -PAGE_TOP_VIEW                          => $CGI->param('page_top_view')||$page_top_view,
    -PAGE_BOTTOM_VIEW                       => $CGI->param('page_bottom_view')||$page_bottom_view,
    -LEFT_PAGE_VIEW                         => $CGI->param('left_page_view')||$page_left_view,
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

my @USER_MAIL_SEND_PARAMS = (
    -TO      => '$mail_to',
    -SUBJECT => "$APP_NAME_TITLE Password Generated"
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => '$mail_from',
    -TO      => '$mail_to',
    -SUBJECT => "$APP_NAME_TITLE Registration Notification"
);
my @MAIL_PARAMS = (
    -TYPE         => 'Sendmail',
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

    -FIELD_MAPPINGS =>
      {
       project_code	      	=> 'Project Code',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       site_name                => 'Owner',
       item_code                 => 'Code for item',
       subject                  => 'Subject category  If not in list select other and place your suggestion in comments',
       share    	      	=> 'Share level',
       name                     => 'Name of resource',
       description              => 'Description of resource',
       url                      => 'URL',
       start_date               => 'Start Date',
       due_date                 => 'Due Date',
       abstract                 => 'Subject',
       details                  => 'Description',
       status                   => 'Status',
       priority                 => 'Priority',
       last_mod_by              => 'Last Modified By',
       last_mod_date            => 'Last Modified Date',
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
       site_name                => 'Owner',
       item_code                 => 'Item code',
       subject                  => 'Subject category <br> If not in list select other and place your suggestion in comments',
       share    	      	=> 'Share level',
       name                     => 'Name of resource',
       description              => 'Description of resource',
       url                      => 'URL',
       start_date               => 'Start Date',
       due_date                 => 'Due Date',
       abstract                 => 'Subject',
       details                  => 'Description',
       status                   => 'Status',
       priority                 => 'Priority',
       last_mod_by              => 'Last Modified By',
       last_mod_date            => 'Last Modified Date',
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
       item_code
       name 
       description
       stock
       username_of_poster
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
$years{$_} = $_ for (2014..2025);
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
      1 => 'IN Stock',
      2 => 'Out of Stock',
      3 => 'Not stocked',
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

     sitename => [
        -DISPLAY_NAME => 'Site',
        -TYPE         => 'textfield',
        -NAME         => 'site_name',
        -VALUE        => $SiteName,
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

   accumulative_time => [
        -DISPLAY_NAME => 'Accumulated Please Add time to entry',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
        -TYPE         => '',


   keywords => [
        -DISPLAY_NAME => "Keywords, help search. bees, bee breeding, programming, separate each word or  by a comma ",
        -TYPE         => 'textarea',
        -NAME         => 'keywords',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],
   comments => [
        -DISPLAY_NAME => 'Comments, please include country and province/state if known.',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

    description => [
        -DISPLAY_NAME => 'Description',
        -TYPE         => 'textarea',
        -NAME         => 'description',
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

    name => [        
        -DISPLAY_NAME => 'Name',        
        -TYPE         => 'textfield',        
        -NAME         => 'name',        
        -SIZE         => 30,        
        -MAXLENGTH    => 80    
        ],
    item_code => [        
        -DISPLAY_NAME => 'Item Code',        
        -TYPE         => 'textfield',        
        -NAME         => 'item_codeview_name',        
        -SIZE         => 30,        
        -MAXLENGTH    => 80    
        ],

        


      share => [
        -DISPLAY_NAME => 'Who can see this',
        -TYPE         => 'popup_menu',
        -NAME         => 'share',
        -VALUES       => [qw(
            public
            priv
            member
        )], 
        -LABELS       => { 
            'priv'    => 'Private only owner can see.',
            'public'  => 'Seen by all users',
            'member'  => 'Paid Member',
            },
    ],


    url => [        
        -DISPLAY_NAME => 'Link to resource Do not include HTTP://',        
        -TYPE         => 'textfield',        
        -NAME         => 'url',        
        -SIZE         => 30,        
        -MAXLENGTH    => 200    
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
            'CSC',
            'CSC_admin',
            'CSC_Address_Book',
            'CSC_Expense',
            'CSC_Expense_Admin',
            'CSC_Inventory_Tracker',
            'CSC_MLM',
            'CSC_ProjectTraker',
            'CSC_ToDo',
            'CSC_URL',
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

     target => [
                 -DISPLAY_NAME => 'target',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'target',
                 -VALUES       => [
				   '_self',
				   '_blank',
				   '_parent',
				   '_top',

                                    ]
               ],
     link_order => [
                 -DISPLAY_NAME => 'Order of dispaly',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'link_order',
                 -VALUES       => [0..12],
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

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER;


if ($group eq "CSC_admin" || 
    $group eq "ECF_admin" || 
    $group eq "HoneyDo_admin" || 
	 $username eq "Shanta"
	) {
  if  ($Nav_link = '1'){
  @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
	   (  
	   qw(sitename),
      qw(item_code),
      qw(share),
      qw(name),
      qw(url),
      qw(view_name),
      qw(link_order),
      qw(target),
    );
  }else{
  @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
      (
      qw(sitename),
      qw(item_code),
      qw(subject),
      qw(share),
      qw(name),
      qw(url),
      qw(view_name),
      [qw(description)],
      qw(link_order),
      qw(target),
      qw(keywords),
       qw(comments),
    );}

}else{
  @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (
      qw(sitename),
      qw(item_code),
      qw(subject),
      qw(share),
      qw(name),
     [qw(description)],
      qw(keywords),
      qw(url),
      qw(comments),
    );
}

my %ACTION_HANDLER_PLUGINS =
    (




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
}else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'brew_item_list_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
	        },
	);

    }
my @SUBJECT_DATASOURCE_FIELD_NAMES = qw(
        record_id
        status
        subject
        project_name
        project_size
        estimated_man_hours
	     display_value
        client_name
        comments        
        username_of_poster
        group_of_poster
        date_time_posted
);

my	@SUBJECT_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'csc_url_sub_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@SUBJECT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['project_code'],
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
my @DROPLIST_DATASOURCE_FIELD_NAMES = qw(
        record_id
        status
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

my  @DROPLIST_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'csc_droplist_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DROPLIST_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['project_code'],
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
	        -KEY_FIELDS   => ['project_code'],
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
    -CLIENT_DATASOURCE_CONFIG_PARAMS    => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
    -SUBJECT_DATASOURCE_CONFIG_PARAMS   => \@SUBJECT_DATASOURCE_CONFIG_PARAMS,
    -URL_DATASOURCE_CONFIG_PARAMS       => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -DROPLIST_DATASOURCE_CONFIG_PARAMS  => \@DROPLIST_DATASOURCE_CONFIG_PARAMS,
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
        site_name              
        item_code           
        subject            
        name               
        description        
        url                
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
'auth_email')|| $mail_from,
    -TO       => $mail_to,
    -BC       => $mail_cc,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to,
    -CC       => $mail_cc,
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
    -LOG_ENTRY_PREFIX => $APP_NAME.' URL|'
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
       OrganicCSSView
       ApisCSSView
       BCHPACSSView
       ECFCSSView
       OkBeekeepersHomeView

       DetailsRecordView
       BasicDataView
       HomeView
       OfficeView
       BudgetView
       ContactView
       PrivacyView
       ProductView
       PrintView
       HostingView
       MembersView
       ForumsView
       MailView
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

       ApisHomeView
       ApisProductView
       MiteGoneDocsView
       AssociateView
       MGWaverView 
        
    

       BCHPAHomeView
       BCHPAAdminHomeView
       BeeTrustView
       BCHPAByLawsView

       ECFHomeView
       OrganicHomeView
       OrganicProductView
       AppToolsView
       WebAppView
       NoopHomeView

       SkyHomeView
       JavaCartView
       COABCAdminHomeView
       GrowersView
       BeeDiseaseView
       AltPowerProductsView
       MentoringHomeView
       BrewRecipeView
      );



my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $APP_NAME_TITLE,
	 -FAVICON                        => $FAVICON || '/images/apis/favicon.ico',
	 -ANI_FAVICON                    => $ANI_FAVICON,
	 -FAVICON_TYPE                   => $FAVICON_TYPE,
    -DISPLAY_FIELDS        => [qw(
        item_code
        comment
        name 
        description
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
        body
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        description
        name
    )],
    -FIELD_NAME_MAPPINGS     => {
        'record _id'         => 'record _id',
        'site_name'              => 'Owner',
        'item_code'           => 'item_code',
        'subject'            => 'Subject category ',
        'name'               => 'Name of resource',
        'description'        => 'Description of resource',
        'url'                => 'URL',
        'comments'           => 'Comments'
        },
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             =>  $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       =>  $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -HOME_VIEW               => 'BasicDataView',
    -SELECTED_DISPLAY_FIELDS => [qw(
        name 
        description
        url
        )],
    -SORT_FIELDS             => [qw(
        item_code
        subject
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
#       CSC::ProcessShowCSCDevelLinksAction

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST = 
    qw(
       Default::PopulateInputWidgetDefinitionListWithSubjectWidgetAction
       Default::PopulateInputWidgetDefinitionListWithCategoryWidgetAction
       Default::PopulateInputWidgetDefinitionListWithClientWidgetAction
       CSC::ProcessShowCSCDevelLinksAction

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
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => 'BasicDataView',
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'item_code',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'name',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'ASC',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -URL_DATA_HANDLER_MANAGER_CONFIG_PARAMS => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 0,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 0,
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LAST_UPDATE                            => $last_update,
    -SITE_LAST_UPDATE                       => $site_update,
  	 -APP_VER                                => $AppVer,
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
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => $allowmod,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 1,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG         => 1,
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -SITE_NAME                              => $SiteName,
    -SHOP                    =>  $shop,
    -APP_NAME                               => 'url',
    -PAGE_TOP_VIEW                          => $page_top_view ,
    -LEFT_PAGE_VIEW                         => $page_left_view,
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
