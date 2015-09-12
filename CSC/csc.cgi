#!/usr/bin/perl -w
# 	$Id: csc.cgi,v 1.4 2011/01/25 03:48:50 shanta Exp $
#on /cgi-bin/CSC
# Copyright (C) 1994 - 2001  eXtropia.com
#
# This program is free software; you can redistribute it and/or
# modify it under t terms of the GNU General Public License
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
    @dirs = qw(  /home/forager/perl/
               ../Modules/
               ../Modules/CPAN .);
}
BEGIN {
    my $homedir = ( getpwuid($>) )[7];
    my @user_include;
    foreach my $path (@INC) {
        if ( -d $homedir . '/perl' . $path ) {
            push @user_include, $homedir . '/perl' . $path;
        }
    }
    unshift @INC, @user_include;
}


use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/AltPower
       ../HTMLTemplates/Apis
       ../HTMLTemplates/BuyAndSell
       ../HTMLTemplates/CS
       ../HTMLTemplates/CSC
       ../HTMLTemplates/Demo      
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Forager
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/GrindrodProject
       ../HTMLTemplates/LT
       ../HTMLTemplates/MW
       ../HTMLTemplates/Organic
       ../HTMLTemplates/SB
       ../HTMLTemplates/SkyeFarm 
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/UrbanFarming       
       ../HTMLTemplates/USBM
       ../HTMLTemplates/WB
       ../HTMLTemplates/WW
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

my $APP_NAME = "csc"; 
my $SiteName =  $CGI->param('site') || "CSC";
my $APP_NAME_TITLE = "Dev.Computer System Consulting.ca";
    my $homeviewname ;
    my $home_view; 
    my $BASIC_DATA_VIEW;
    my $page_top_view;
    my $page_bottom_view;
    my $left_page_view;
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
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
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
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my  $additonalautusernamecomments;
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $last_update  = 'June 22, 2011';
    my $SITE_DISPLAY_NAME = 'No display name defined for this site.';
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
    my $SiteLastUpdate;
    my $site_update;
    my $DeBug = $CGI->param('debug')|| 0;
    my $shop ;
    my $Affiliate = 001;
    
use SiteSetup;
  my $UseModPerl = 1;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view                    = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname                 = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW              = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view                = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view             = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $left_page_view               = $SetupVariables->{-PAGE_LEFT_VIEW};
    $MySQLPW                      = $SetupVariables->{-MySQLPW}||'nvidia2';
#Mail settings  
    $mail_from                    = $SetupVariables->{-MAIL_FROM}; 
    $mail_to                      = $SetupVariables->{-MAIL_TO};
    $mail_replyto                 = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME                = $SetupVariables->{-CSS_VIEW_NAME};
    $app_logo                     = $SetupVariables->{-APP_LOGO};
    $app_logo_height              = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width               = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt                 = $SetupVariables->{-APP_LOGO_ALT};
    $FAVICON                      = $SetupVariables->{-FAVICON};
    $ANI_FAVICON                  = $SetupVariables->{-ANI_FAVICON};
    $FAVICON_TYPE                 = $SetupVariables->{-FAVICON_TYPE};
    $IMAGE_ROOT_URL               = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL            = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET                  = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS           = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS         = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION      = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    my @PRODUCT_DATASET           = $SetupVariables->{-PRODUCT_DATASOURCE_CONFIG_PARAMS};
    $DEFAULT_CHARSET              = $SetupVariables->{-DEFAULT_CHARSET};
    $DBI_DSN                      = $SetupVariables->{-DBI_DSN}||'mysql:host=mysql.computersystemconsulting.ca;database=shanta_forager';
    $AUTH_TABLE                   = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME          = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    my @AUTH_USER_DATASOURCE_CONFIG_PARAMS = $SetupVariables->{-AUTH_USER_DATASOURCE_CONFIG_PARAMS};
    $additonalautusernamecomments = $SetupVariables->{-ADDITIONALAUTHUSERNAMECOMMENTS};
    $site                         = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY   = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY    = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY      = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    my $LocalIp                   = $SetupVariables->{-LOCAL_IP};
    $last_update                  = $SetupVariables->{-LAST_UPDATE};
    $DATAFILES_DIRECTORY          = $APP_DATAFILES_DIRECTORY;
    $site_session                 = $DATAFILES_DIRECTORY.'/Sessions';
    $auth                         = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';


my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => $SetupVariables->{-SESSION_TIME_OUT}||60 * 60,
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
my $CSS_VIEW_URL;# = $CGI->script_name(). "?display_css_view=on&session_id=$SESSION_ID";

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



######################################################################
#                        Calling site  SETUP                         #
######################################################################
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');

if ($SiteName eq "Apis" or
    $SiteName eq "HelpDeskApis") {
use ApisSetup;
  my $UseModPerl = 1;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $AUTH_TABLE            = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesApis->{-APP_LOGO_ALT};
    $APP_NAME_TITLE        = "Apis Client";
#    $left_page_view       = 'CSCLeftPageView';
    $CSS_VIEW_URL          = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME     = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
 }
 
elsif ($SiteName eq "BMaster" or
    $SiteName eq "HelpDeskBMaster") {
use BMasterSetup;
  my $UseModPerl = 1;
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
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
 }
 

elsif ($SiteName eq "BCHPA" or
    $SiteName eq "HelpDeskBMaster") {
use BCHPASetup;
   my $UseModPerl = 1;
 my $SetupVariablesBCHPA  = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_URL         = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesBCHPA->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesBCHPA->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBCHPA->{-LEFT_PAGE_VIEW};
    $APP_NAME_TITLE        = "British Columbia Honey Producers Assoiation";
#Mail settings
    $mail_from             = $SetupVariablesBCHPA->{-MAIL_FROM};
    $mail_to               = $SetupVariablesBCHPA->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBCHPA->{-MAIL_REPLYTO};
 $APP_DATAFILES_DIRECTORY    = "../../Datafiles/Apis";
if ($group eq "BCHPA_admin") {
    $home_view             = 'BCHPAAdminHomeView';
    $homeviewname          = 'BCHPAAdminHomeView';
 $left_page_view =$page_left_view;
 }
if ($CGI->param('view') eq "HelpDeskView") {
 $left_page_view = 'CSCLeftPageView';
 }
  }

elsif ($SiteName eq "eXtropia" or
    $SiteName eq "eXtropiaHelpDesk") {
use eXtropiaSetup;
  my $UseModPerl = 1;
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
}

elsif ($SiteName eq "VitalVic" or
      $SiteName eq "VitalVicHelpDesk") { 
use VitalVicSetup;
  my $UseModPerl = 1;
  my $SetupVariablesVitalVic   = new  VitalVicSetup;
    $CSS_VIEW_URL         = $SetupVariablesVitalVic ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesVitalVic ->{-AUTH_TABLE};
    $APP_NAME_TITLE        = " VitalVic Clien";
$left_page_view = 'CSCLeftPageView';
}
elsif($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk") {
use CSSetup;
  my $SetupVariablesCS   = new CSSetup($UseModPerl);
    $APP_NAME_TITLE        = "Country Stores Client.";
#    $left_page_view = 'CSCLeftPageView';
  $page_top_view            = $SetupVariablesCS->{-PAGE_TOP_VIEW};
  $page_bottom_view         = $SetupVariablesCS->{-PAGE_BOTTOM_VIEW};
  $page_left_view           = $SetupVariablesCS->{-LEFT_PAGE_VIEW};
  $homeviewname             = $SetupVariablesCS->{-HOME_VIEW_NAME};
  $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};
  $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
  $shop                     = $SetupVariablesCS->{-SHOP};
  $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
  $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
  $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
  $FAVICON                  = $SetupVariablesCS>{-FAVICON};
  $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
  $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};

}

elsif ($SiteName eq "CSC" or
       $SiteName eq "CSCDev" or
       $SiteName eq "BMasterDev" or
       $SiteName eq "HelpDesk" or
       $SiteName eq "CSCHelpDesk"
       ){
      
use CSCSetup;
 my $UseModPerl = 1;
  my $SetupVariablesCSC   = new  CSCSetup($UseModPerl);
  
  $page_top_view            = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
  $page_bottom_view         = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
  $page_left_view           = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
  $homeviewname             = $SetupVariablesCSC->{-HOME_VIEW_NAME};
  $site_update              = $SetupVariablesCSC->{-SITE_LAST_UPDATE};
  $app_logo                 = $SetupVariablesCSC->{-APP_LOGO};
  $shop                     = $SetupVariablesCSC->{-SHOP};
  $app_logo_height          = $SetupVariablesCSC->{-APP_LOGO_HEIGHT};
  $app_logo_width           = $SetupVariablesCSC->{-APP_LOGO_WIDTH};
  $app_logo_alt             = $SetupVariablesCSC->{-APP_LOGO_ALT};
  $FAVICON                  = $SetupVariablesCSC->{-FAVICON};
  $ANI_FAVICON              = $SetupVariablesCSC->{-ANI_FAVICON};
  $FAVICON_TYPE             = $SetupVariablesCSC->{-FAVICON_TYPE};

  if ($SiteName eq "CSCDev" or $SiteName eq "CSC"
       ) {     
    $SITE_DISPLAY_NAME        = "Dev.".$SetupVariablesCSC->{-SITE_DISPLAY_NAME};
       $APP_NAME_TITLE           = "CSC";
       $AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
       } 
    elsif ($SiteName eq "CSCHelpDesk"
       ) {
     $SITE_DISPLAY_NAME        = "HelpDesk.".$SetupVariablesCSC->{-SITE_DISPLAY_NAME};
       $APP_NAME_TITLE           = "CSC";
#      $AUTH_TABLE               = $SetupVariablesCSC ->{-$SiteName _AUTH_TABLE}; 
      }
    else {
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
    $APP_NAME_TITLE           = "Computer System Consulting.ca";
    $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
      }
       
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
	    
	if ($SiteName eq "BMasterDev"
	       ) {     
	    $CSS_VIEW_NAME            = "/styles/apis.css";
	    $CSS_VIEW_URL             = "/styles/apis.css";
	           } else {
	    $CSS_VIEW_URL             = $SetupVariablesCSC->{-CSS_VIEW_NAME};
	    $CSS_VIEW_NAME            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
	    }
 
	     
}


elsif ($SiteName eq "CSCRecy"or
      $SiteName eq "CSCRecyHelpDesk" ) {
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


elsif ($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk" ) {
use CSSetup;
  my $SetupVariablesCS   = new  CSSetup($UseModPerl);
     $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
     $APP_NAME_TITLE           = "Country Stores";
	  $HTTP_HEADER_KEYWORDS     = $SetupVariablesCS->{-HTTP_HEADER_KEYWORDS};
	  $HTTP_HEADER_PARAMS       = $SetupVariablesCS->{-HTTP_HEADER_PARAMS};
	  $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCS->{-HTTP_HEADER_DESCRIPTION};
	  $CSS_VIEW_URL             = $SetupVariablesCS->{-CSS_VIEW_NAME};
	  $CSS_VIEW_NAME            = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};
     $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
     $shop                     = $SetupVariablesCS->{-SHOP};
     $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
     $FAVICON                  = $SetupVariablesCS->{-FAVICON};
     $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
     $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};
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

elsif ($SiteName eq "Noop" or
      $SiteName eq "NoopHelpDesk") {

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
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Organic'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
}



elsif ($SiteName eq "Demo" or
      $SiteName eq "DemoHelpDesk") {
use DEMOSetup;
  my $UseModPerl = 1;
  my $SetupVariablesDemo   = new  DEMOSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesDemo ->{-AUTH_TABLE};
    $APP_NAME_TITLE           = "Computer System Consulting.ca Demo Application";
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

}


elsif ($SiteName eq "ECF" || 
       $SiteName eq "ECFDev" or
      $SiteName eq "ECFHelpDesk" ) {
use ECFSetup;
  my $UseModPerl = 1;
  my $SetupVariablesECF   = new  ECFSetup($UseModPerl);
    $CSS_VIEW_URL         = $SetupVariablesECF ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesECF ->{-AUTH_TABLE};
    $APP_NAME_TITLE        = "CSC.ca's ECF customer support";
    $last_update              = $SetupVariablesECF->{-Site_LAST_UPDATE};
    $site_update              = $SetupVariablesECF->{-Site_LAST_UPDATE};
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

elsif ($SiteName eq "Organic" or
      $SiteName eq "OrganicHelpDesk") {
use OrganicSetup;
  my $UseModPerl = 1;
  my $SetupVariablesOrganic   = new  OrganicSetup($UseModPerl);
    $CSS_VIEW_URL         = $SetupVariablesOrganic ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesOrganic ->{-AUTH_TABLE};
    $APP_NAME_TITLE        = "CSC.ca's Orgnic Farming customer support";
 $left_page_view = 'LeftPageView';

}
elsif ($SiteName eq "SQL_Ledger" or
      $SiteName eq "SQL_LedgerHelpDesk") {
use SQLSetup;
  my $UseModPerl = 1;
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
elsif ($SiteName eq "HE" or
       $SiteName eq "HEDev" or
      $SiteName eq "HEHelpDesk") {
use HESetup;
  my $UseModPerl = 1;
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
      $site_update            = $SetupVariablesGRA->{-SITE_LAST_UPDATE};
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

elsif ($SiteName eq "BCAF" or
      $SiteName eq "BCAFHelpDesk") {
use OrganicSetup;
  my $UseModPerl = 1;
  my $SetupVariablesOrganic   = new  OrganicSetup($UseModPerl);
    $CSS_VIEW_URL         = $SetupVariablesOrganic ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesOrganic ->{-AUTH_TABLE};
    $APP_NAME_TITLE        = "CSC.ca's Orgnic Farming customer support";
 $left_page_view = 'LeftPageView';
$SiteName = 'Organic';
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
 }


#if ( $homeviewname eq 'CSCHome' ||
 #    $home_view eq  'CSCHome'
#   ){
#				    $homeviewname = "CSCHomeView";
#				    $home_view = "CSCHomeView";
#				   }
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
    'auth_email'     => 'email',
    'auth_developer_status' => 'developer_status'
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
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -LINK_TARGET             => $LINK_TARGET,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -LEFT_PAGE_VIEW          => $left_page_view,
    -PAGE_LEFT_VIEW          => $left_page_view,
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
                'auth_email'        => 'E-Mail Address',
                'auth_developer_status' => 'Are you a developer?'
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
    'auth_username'  => 'Username '.$additonalautusernamecomments,
    'auth_password'  => 'Password',
    'auth_groups'    => 'Groups',
    'auth_firstname' => 'First Name',
    'auth_lastname'  => 'Last Name',
    'auth_email'     => 'E-Mail',
    'auth_developer_status'     => 'Developer?'
);

my %USER_FIELD_TYPES = (
    -USERNAME_FIELD => 'auth_username',
    -PASSWORD_FIELD => 'auth_password',
    -GROUP_FIELD    => 'auth_groups',
    -EMAIL_FIELD    => 'auth_email'
);

my @USER_MAIL_SEND_PARAMS = (
    -TO      =>  $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO      =>  $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE." Registration Notification"
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
       sitename            => 'sitename',
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       subject          => 'Subject',
       description      => 'Description',
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
                           sitename
                           start_date
                           due_date
                           subject
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
       subject                 => 'Subject',
       description                  => 'Description',
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
                           sitename
                           start_date
                           due_date
                           subject
                           status
                           priority
                           last_mod_by
                           last_mod_date
                          )
                       ]
        ]
    ]
);

my @URL_FORM_DHM_CONFIG_PARAMS = (
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
       sitename                    => 'sitename',
       category                 => 'Category If not in list select other and place your suggestion in comments',
       subject                  => 'Subject category  If not in list select other and place your suggestion in comments',
       share    	      	=> 'Share level',
       name                     => 'Name of resource',
       description              => 'Description of resource',
       url                      => 'URL',
       start_date               => 'Start Date',
       due_date                 => 'Due Date',
       subject                 => 'Subject',
       description                  => 'Description',
       status                   => 'Status',
       priority                 => 'Priority',
       last_mod_by              => 'Last Modified By',
       last_mod_date            => 'Last Modified Date',
       comments                 => 'Comments',
   },
				  );
#    -MODIFY_FORM_DHM_CONFIG_PARAMS => \@URL_FORM_DHM_CONFIG_PARAMS,

my @URL_DATA_HANDLER_MANAGER_CONFIG_PARAMS = (
    -ADD_FORM_DHM_CONFIG_PARAMS            => \@URL_FORM_DHM_CONFIG_PARAMS,
    -MODIFY_FORM_DHM_CONFIG_PARAMS         => \@URL_FORM_DHM_CONFIG_PARAMS,
);

my @DATA_HANDLER_MANAGER_CONFIG_PARAMS = (
    -ADD_FORM_DHM_CONFIG_PARAMS        => \@ADD_FORM_DHM_CONFIG_PARAMS,
    -MODIFY_FORM_DHM_CONFIG_PARAMS     => \@MODIFY_FORM_DHM_CONFIG_PARAMS,
);

######################################################################
#                      DATASOURCE SETUP                              #
######################################################################

my @DATASOURCE_FIELD_NAMES = 
    qw(
       record_id
       sitename
       start_date
       project_code
       estimated_man_hours 
       accumulative_time
       due_date
       subject
       description
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
     subject => [
                 -DISPLAY_NAME => 'Subject',
                 -TYPE         => 'textfield',
                 -NAME         => 'subject',
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

     description  => [
                 -DISPLAY_NAME => 'Description',
                 -TYPE         => 'textarea',
                 -NAME         => 'description',
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
            'CSC',
            'CSC_admin',
            'CSC_Adress_Book',
            'CSC_Expence',
            'CSC_Expence_Admin',
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
      qw(subject ),
     [qw(start_day start_mon start_year)],
     [qw(due_day due_mon due_year)],
      qw(description),
      qw(priority),
     [qw(status)],
     qw(estimated_man_hours),
     qw(accumulative_time),
     qw(comments),
    );


my %ACTION_HANDLER_PLUGINS =
    (

     'Default::DisplayAddFormAction' =>
     {
      -DisplayAddFormAction     => [qw(Plugin::Todo::DisplayAddFormAction)],
     },

     'Default::DisplayDetailsRecordViewAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayDeleteRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayModifyFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayModifyRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::ProcessModifyRequestAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayAddRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::ProcessAddRequestAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

#     'Default::DefaultAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayViewAllRecordsAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplaySimpleSearchResultsAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayOptionsFormAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

#     'Default::DisplayPowerSearchFormAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },

 #    'Default::PerformPowerSearchAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },



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
	        -TABLE        => 'csc_todo_tb',
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
my @URL_DATASOURCE_FIELD_NAMES = 
    qw(
       record_id
       sitename
       category
       subject
       share
       name 
       description
       url
       last_mod_by
       last_mod_date
       comments        
      );

my @URL_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'url_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@URL_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
	        },
	);


my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -URL_DATASOURCE_CONFIG_PARAMS       => \@URL_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_CONFIG_PARAMS
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
       subject
       location
       start_date
       end_date
       recur_interval
       recur_until_date
       description
       estimated_man_hours
       accumulative_time
       comments        
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>   $SESSION->getAttribute(-KEY =>
'auth_email') || $mail_from,
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

my @VALID_VIEWS = 
    qw(
       CSCCSSView
       ApisCSSView
       BCHPACSSView
       d2earthCSSView
       rvSSView
       VitalVicCSSView
       ENCYCSSView
       ContactView

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
       AppearanceView
       OptionsView
       LogoffView
       HomeView
       PrivacyView
       OpensourceView
       ProductView
       CityShopAdminView
       CSCHomeView
       CSCHome
       DeveloperView
       DevHomeView
       ECFHome
       HelpDeskHomeView
       HostingView
       ECFHomeView
       KamasketHome
       SideBarHomeViewContactView
       ForagerHomeView
       MailView
       ServicesView
       WebSiteAdminView
       SQL_Ledger_Support_View
       GrindrodParkMarketHome
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
	 -FAVICON                        => $FAVICON,
	 -ANI_FAVICON                    => $ANI_FAVICON,
	 -FAVICON_TYPE                   => $FAVICON_TYPE,
    -DISPLAY_FIELDS                 => [qw(
        subject
        description
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
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        description
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        bodyContactView
    )],
    -FIELD_NAME_MAPPINGS     => {
        'project_code' => 'Project Code',
        'subject'     => 'Subject',
        'description'      => 'Description',
        'start_date'   => 'Start Date',
        'due_date'     => 'Due Date',
        'status'       => 'Status',
        'priority'     => 'Priority',
        },
    -HOME_VIEW               => $homeviewname,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -APP_NAME                => $APP_NAME,
    -SELECTED_DISPLAY_FIELDS => [qw(
        project_code
        subject
        start_date
        due_date
        status
        priority
        )],
    -SORT_FIELDS             => [qw(
        due_date
        subject
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
#      CSC::ProcessShowCSCDevelLinksAction
#      CSC::ProcessShowCSCAdminLinksAction

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
    -BASIC_DATA_VIEW_NAME                   => $homeviewname,
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_URL,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
	 -DEBUG                                  => $DeBug,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'start_date',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'priority',
    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASC',
#    -SORT_DIRECTION                         => 'DESC',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -URL_DATA_HANDLER_MANAGER_CONFIG_PARAMS => \@URL_DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -ENABLE_SORTING_FLAG                    => 1,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS||'test',
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -LAST_UPDATE                            => $last_update,
    -SITE_LAST_UPDATE                       => $site_update,
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
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
    -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG         => 0,
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
    -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
    -SITE_NAME            => $SiteName,
    -PAGE_TOP_VIEW           =>  $page_top_view ,
    -LEFT_PAGE_VIEW          =>  $left_page_view,
    -PAGE_BOTTOM_VIEW        =>  $page_bottom_view,
    -SHOP                    =>  $shop,
    -SELECT_FORUM_VIEW		=> 'SelectForumView',
    -PAGE_LIST_VIEW                         => 'CSCSubscribeListView',
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