#!/usr/bin/perl -wT
# 	$Id: helpdesk.cgi,v 1.4 2003/12/05 04:40:16 shanta Exp shanta $	
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

use strict;

BEGIN{
    use vars qw(@dirs);
    @dirs = qw(  /home/shanta/perl/
               ../Modules/
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

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


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Fly
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS    use vars qw(@dirs);
    @dirs = qw(/home/shanta/public_html/cgi-bin/Modules/
               /home/shanta/public_html/cgi-bin/Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/Brew
       ../HTMLTemplates/Extropia
       ../HTMLTemplates/Apis
       ../HTMLTemplates/Brew
       ../HTMLTemplates/BuyAndSell
       ../HTMLTemplates/CS
       ../HTMLTemplates/CSC       
       ../HTMLTemplates/CSC       
       ../HTMLTemplates/Demo      
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/ECF
       ../HTMLTemplates/Forager
       ../HTMLTemplates/GrindrodProject
       ../HTMLTemplates/HE
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/LT
       ../HTMLTemplates/MW
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta 
       ../HTMLTemplates/SB
       ../HTMLTemplates/SkyeFarm 
       ../HTMLTemplates/Todo
       ../HTMLTemplates/UrbanFarming       
       ../HTMLTemplates/USBM
       ../HTMLTemplates/WB
       ../HTMLTemplates/WW
       ../HTMLTemplates/HoneyDo
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

my $APP_NAME = "helpdesk"; 
   my $VirtualServerName = $ENV{'SERVER_NAME'}||'test';
 my $SiteName =  $CGI->param('site') || "CSC";
my $APP_NAME_TITLE = "HelpDesk";
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
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
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
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $additonalautusernamecomments;
    my $DBI_DSN;
    my $AUTH_TABLE;
    my $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET;
    my $mail_to_user;
    my $mail_to_member;
    my $mail_to_discussion;
    my $last_update;
    my $site_update;
    my $SITE_DISPLAY_NAME = 'No display name defined for this site.';
    my $mail_to_admin;
    my $mail_from_helpdesk;    
     my $HasMembers = 0;
   
    
use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view                    = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname                 = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW              = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view                = 'templatePageTopView';
    $page_bottom_view             = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view               = $SetupVariables->{-PAGE_LEFT_VIEW};
    $MySQLPW                      = $SetupVariables->{-MySQLPW}||'nvidia2';
#Mail settings  
    $mail_from                    = $SetupVariables->{-MAIL_FROM}; 
    $mail_to                      = $SetupVariables->{-MAIL_TO};
    $mail_from_helpdesk           = $SetupVariables->{-MAIL_FROM_HELPDESK}; 
    $mail_replyto                 = $SetupVariables->{-MAIL_REPLYTO};
    $CSS_VIEW_NAME                = $SetupVariables->{-CSS_VIEW_NAME};
    $app_logo                     = $SetupVariables->{-APP_LOGO};
    $app_logo_height              = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width               = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt                 = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL               = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $FAVICON                      = $SetupVariables->{-FAVICON};
    $ANI_FAVICON                  = $SetupVariables->{-ANI_FAVICON};
    $FAVICON_TYPE                 = $SetupVariables->{-FAVICON_TYPE};
     $DOCUMENT_ROOT_URL            = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET                  = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS           = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS         = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION      = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    my @PRODUCT_DATASET           = $SetupVariables->{-PRODUCT_DATASOURCE_CONFIG_PARAMS};
    $DEFAULT_CHARSET              = $SetupVariables->{-DEFAULT_CHARSET};
    $DBI_DSN                      = $SetupVariables->{-DBI_DSN}||'mysql:database=shanta_forager';
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
#my $CSS_VIEW_URL = $CGI->script_name()."?display_css_view=on&session_id=$SESSION_ID";
my $CSS_VIEW_URL = "/styles/apis.css";

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
    $page_left_view        = $CGI->param('page_left_view')||$page_left_view;

if ($CGI->param('page_left_view')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'page_left_view') ){
      $SESSION ->setAttribute(-KEY => 'page_left_view', -VALUE => $CGI->param('page_left_view')) ;
       $page_left_view = $CGI->param('page_left_view');
    }else {
	$SESSION ->setAttribute(-KEY => 'page_left_view', -VALUE => $page_left_view );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'page_left_view')) {
    $page_left_view = $SESSION ->getAttribute(-KEY => 'page_left_view');
  }else {
	$SESSION ->setAttribute(-KEY => 'page_left_view', -VALUE => $page_left_view );
      }
}
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');

if ($SiteName eq "Apis") {
use ApisSetup;
  my $UseModPerl = 0;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_URL           = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE             = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo               = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height        = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width         = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt           = $SetupVariablesApis->{-APP_LOGO_ALT};
    $SITE_DISPLAY_NAME      = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
    $homeviewname           = 'HelpDeskHomeView';
    $SITE_DISPLAY_NAME      = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
  }
  
elsif ($SiteName eq "BMaster") {
use BMasterSetup;
  my $UseModPerl = 1;
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
    $mail_from                = $SetupVariablesBMaster->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesBMaster->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
 }
 



elsif ($SiteName eq "CS" or
      $SiteName eq "CSHelpDesk" ) {
use CSSetup;
  my $SetupVariablesCS   = new  CSSetup($UseModPerl);
     $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
     $HTTP_HEADER_KEYWORDS     = $SetupVariablesCS->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS       = $SetupVariablesCS->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCS->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_URL             = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $CSS_VIEW_NAME            = $SetupVariablesCS->{-CSS_VIEW_NAME};
     $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};
     $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
     $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
     $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
     $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
#     $FAVICON                  = $SetupVariablesCS->{-FAVICON};
#     $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
#     $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};
}

elsif ($SiteName eq "CSC"or
      $SiteName eq "HelpDesk" ) {
use CSCSetup;
  my $SetupVariablesCSC   = new  CSCSetup($UseModPerl);
    $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
    $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
    $HTTP_HEADER_KEYWORDS     = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS       = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION  = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $page_top_view            = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view         = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view           = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL             = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $app_logo                 = $SetupVariablesCSC->{-APP_LOGO};
    $app_logo_height          = $SetupVariablesCSC->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesCSC->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesCSC->{-APP_LOGO_ALT};
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
    $homeviewname             = $SetupVariablesCSC->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesCSC->{-LAST_UPDATE};
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};

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
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};cgi
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
    $homeviewname             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-LAST_UPDATE};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};

}

elsif ($SiteName eq "VitalVic") {
use VitalVicSetup;
  my $SetupVariablesVitalVic   = new  VitalVicSetup($UseModPerl);
    $CSS_VIEW_URL          = $SetupVariablesVitalVic ->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesVitalVic ->{-AUTH_TABLE};
    $homeviewname          = 'HelpDeskHomeView';
    $SITE_DISPLAY_NAME     = $SetupVariablesVitalVic->{-SITE_DISPLAY_NAME};
}  
elsif($SiteName eq "CS") {
    $homeviewname          = 'HelpDeskHomeView';
}

elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $UseModPerl = 0;
  my $SetupVariablesENCY   = new ENCYSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesENCY->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesENCY->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariablesENCY->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesENCY->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesENCY->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesENCY->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesENCY->{-APP_};
     $app_logo_height         = $SetupVariablesENCY->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesENCY->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesENCY->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablesENCY->{-CSS_VIEW_NAME};
#     $homeviewname            = $SetupVariablesENCY->{-HOME_VIEW_NAME};
#     $home_view               = $SetupVariablesENCY->{-HOME_VIEW};
     $SITE_DISPLAY_NAME       = $SetupVariablesENCY->{-SITE_DISPLAY_NAME};
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
    $SITE_DISPLAY_NAME        = $SetupVariableseXtropia->{-SITE_DISPLAY_NAME};
}

 elsif ($SiteName eq "ECF"||
        $SiteName eq "ECFDev") {
use ECFSetup;
  my $SetupVariablesECF    = new  ECFSetup($UseModPerl);
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesECF->{-AUTH_TABLE};
    $homeviewname            = $SetupVariablesECF->{-HOME_VIEW_NAME};
    $home_view               = $SetupVariablesECF->{-HOME_VIEW};
#Mail settings
    $mail_from               = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesECF->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS      = $SetupVariablesECF->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesECF->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesECF->{-HTTP_HEADER_DESCRIPTION};
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "Fly") {
use FlySetup;
  my $UseModPerl = 0;
  my $SetupVariablesFly   = new FlySetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesFly->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesFly->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesFly->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesFly->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesFly->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesFly->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesFly->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesFly->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesFly->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesFly->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesFly->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesFly->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesFly->{-SITE_DISPLAY_NAME};
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
     $app_logo                = $SetupVariablesHoneyDo->{-APP_LOGO};cgi
     $app_logo_height         = $SetupVariablesHoneyDo->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesHoneyDo->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesHoneyDo->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesHoneyDo->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesHoneyDo->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesHoneyDo->{-LAST_UPDATE}; 
#     $site_update              = $SetupVariablesHoneyDo->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHoneyDo->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesHoneyDo->{-MAIL_TO};
    $SITE_DISPLAY_NAME        = $SetupVariablesHoneyDo->{-SITE_DISPLAY_NAME};
    $mail_replyto             = $SetupVariablesHoneyDo->{-MAIL_REPLYTO};
 }

elsif ($SiteName eq "OKB" ) {
use OKbeekeeperSetup;
  my $UseModPerl = 0;
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
#Mail settings
    $mail_from                = $SetupVariablesOKB->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesOKB->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesOKB->{-MAIL_REPLYTO};
	 $mail_to_user             = $SetupVariablesOKB->{-MAIL_TO_USER};
	 $mail_to_member           = $SetupVariablesOKB->{-MAIL_TO_Member};
	 $mail_to_discussion       = $SetupVariablesOKB->{-MAIL_TO_DISCUSSION};
    $SITE_DISPLAY_NAME        = $SetupVariablesOKB->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "Organic") {
use OrganicSetup;
  my $SetupVariablesOrganic  = new  OrganicSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesOrganic->{-AUTH_TABLE};
    $page_top_view           = $SetupVariablesOrganic->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesOrganic->{-PAGE_BOTTOM_VIEW};
#Mail settings
    $mail_from               = $SetupVariablesOrganic->{-MAIL_FROM};cgi
    $mail_to                 = $SetupVariablesOrganic->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesOrganic->{-MAIL_REPLYTO};
    $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
    $homeviewname            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
    $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
    $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/Organic"; 
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
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
 }
 elsif ($SiteName eq "TelMark" or
       $SiteName eq "TelMarkDev") {
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
     $APP_DATAFILES_DIRECTORY    = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
 }
 if ( $VirtualServerName = "helpdesk.computersystemconsulting.ca") {
    $homeviewname   = 'HelpDeskHomeView';
    $page_top_view  = "PageTopView";
    $page_left_view = "HelpDeskLeftPageView";} 
 
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
    -LEFT_PAGE_VIEW          => $page_left_view,
    -PAGE_LEFT_VIEW          => $page_left_view,
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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||'$mail_from_helpdesk',
    -TO      =>  $SetupVariables->{-MAIL_TO_ADMIN}||$mail_to,
    -SUBJECT => $APP_NAME_TITLE.' Registration Notification'
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

#################################################  #####################
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
                           owner
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
                           owner
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
       owner                    => 'Owner',
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
       owner
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

#my %ACTION_HANDLER_PLUGINS;
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

     'Default::DefaultAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayViewAllRecordsAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplaySimpleSearchResultsAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayOptionsFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayPowerSearchFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::PerformPowerSearchAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },



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
       owner
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
'auth_email') || $mail_from_helpdesk,
    -TO       => $mail_from_helpdesk,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_from_helpdesk,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_from_helpdesk,
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
       CSCSSView
       CSPSCSSView
       d2earthCSSView
       VitalVicCSSView
       CSSView
       ENCYCSSView
       BCHPACSSView

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
       CSCHomeView
       CSCHome
       CityShopAdminView
       HelpDeskHomeView
       SideBarHomeView
       AppToolsView
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -VIRTUAL_SERVER_NAME            => $VirtualServerName,
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
        body
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
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SITE_DISPLAY_NAME       =>  $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
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
#       CSC::ProcessShowCSCDevelLinksAction

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST = 
    qw(
       CSC::ProcessShowCSCAdminLinksAction
       CSC::ProcessShowCSCDevelLinksAction
       CSC::DisplaySideBarViewAction

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
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'start_date',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'priority',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'DESC',
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
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -SITE_LAST_UPDATE                       => $site_update,
    -LAST_UPDATE                            => $last_update,
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
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 1,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 1,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
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
    -LEFT_PAGE_VIEW          =>  $page_left_view,
    -PAGE_BOTTOM_VIEW        =>  $page_bottom_view,
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