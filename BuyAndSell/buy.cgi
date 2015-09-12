#!/usr/bin/perl -wT
# 	$Id: buy.cgi,v 1.8 2002/05/31 14:27:36 shanta Exp $	

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
    # Windows users must set a timezone env!
    $ENV{'TZ'} = 'EST' if ($^O =~ /MSWin32/i);
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
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/BuyAndSell
       ../HTMLTemplates/ECF
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/CSC
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/HE
       ../HTMLTemplates/IM
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Skye
       ../HTMLTemplates/Todo
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
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x$/);
}

######################################################################
#                          SITE SETUP                             #
######################################################################


my $APP_NAME = "buy";

my $APP_NAME_TITLE = "Buy and Sell";
my $SiteName =  $CGI->param('site') || "CSC";
my $site_update;
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
    my $CSS_VIEW_NAME = 'ApisCSSView';
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
    my $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $BuyDBI_DSN ='mysql:database=shanta_forager';
    my $BuyAUTH_MSQL_USER_NAME ='shanta_forager';
    my $BuyMySQLPW ='herbsrox2';
    my $DEFAULT_CHARSET; 
    my $additonalautusernamecomments;
    my $SetupVariables;
    my $TableName;
    my $sitename;
    my $ProjectTableName;
    my $mail_to_user;
    my $mail_to_member;
    my $mail_to_discussion;
    my $mail_list_bcc;
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $last_update = 'January 26, 2006';
    my $listname;
    my $AccountURL;
    my $subscrib;
    my $unsubscrib;
    my $listinfo;
    my $listfaq;
    my $SitedisplyName;
    my $salutaion;
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
my $Affiliate = 001;

    $APP_NAME_TITLE = "Buy and Sell";
    my $HasMembers = 0;


use SiteSetup;
  my $UseModPerl = 1;
   $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-page_left_view};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
    $additonalautusernamecomments  = $SetupVariables->{-ADDITIONALAUTHUSERNAMECOMMENTS};
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
    my $LocalIp            = $SetupVariables->{-LOCAL_IP};
    $Affiliate               = $SetupVariables->{-AFFILIATE};
   $site = $SetupVariables->{-DATASOURCE_TYPE};
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $DATAFILES_DIRECTORY   = $APP_DATAFILES_DIRECTORY;
    $site_session          = $DATAFILES_DIRECTORY.'/Sessions';
    $auth                  = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
    $TableName             = 'buy_sell_tb    ';
    $ProjectTableName      = 'csc_project_tb';
	 my $DropListName       = 'buy_sell_category_tb';
 
#Add sub aplication spacific overrides.
# $GLOBAL_DATAFILES_DIRECTORY = "Datafiles";
# $TEMPLATES_CACHE_DIRECTORY  = "$GLOBAL_DATAFILES_DIRECTORY/TemplatesCache";
# $APP_DATAFILES_DIRECTORY    = "Datafiles/Todo";
$page_top_view    = $CGI->param('page_top_view')||$page_top_view;
$page_bottom_view = $CGI->param('page_bottom_view')||$page_bottom_view;
#$page_left_view   = $CGI->param('page_left_view')||$page_left_view;
$page_left_view = "LeftPageView";
my $target;
my $columnstoview;
my $SortFields;
my $SortField1;
my $SortField2;
my $SortDirection;
my $RecordsToDisplay;
my $version = '1.2';


if ($CGI->param('page_top_view') eq'SBPageTopView'){
$target='_content';
 $columnstoview = [qw(
        category
        item_name
        price
       )];
 $SortFields=[qw(
        category
        item_name
        location
        )];
 $SortField2='due_date';
 $SortField1='priority';
 $SortDirection='DESC' ;
 $RecordsToDisplay=20;
}else{
$target='_self';
 $columnstoview=[qw(
        category
        item_name
        price
        url
        location

        )];
$SortFields=[qw(
        category
        location
        )];
 $SortField1=$CGI->param('sort_field1') ||'priority';
 $SortField2=$CGI->param('sort_field2') ||'due_date';
 $RecordsToDisplay=100;
 $SortDirection='DESC';#ASC
}
my $SESSION_DIR;
$LINK_TARGET = $target;
my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

use constant HAS_CLASS_DATE  => eval { require Class::Date; };

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60 * 2,
    -SESSION_DIR     => $SESSION_DIR,
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
my $username = $SESSION ->getAttribute(-KEY => 'auth_username');
$sitename =$SiteName;
my $GROUP_OF_POSTER = $SESSION -> getAttribute(-KEY => 'auth_groups')||'normal';
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');
if ($SiteName eq "Apis") {
use ApisSetup;
  my $UseModPerl = 1;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_NAME          = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $app_logo               = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height        = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width         = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt           = $SetupVariablesApis->{-APP_LOGO_ALT};
    $homeviewname           = 'HomeView';
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis'; 
#    $TableName              = 'apis_todo_tb';
#    $ProjectTableName       = 'apis_project_tb';
     $CSS_VIEW_URL           = $SetupVariablesApis->{-CSS_VIEW_NAME};
#Mail settings
    $mail_from              = $SetupVariablesApis->{-MAIL_FROM};
    $mail_to                = $SetupVariablesApis->{-MAIL_TO};
    $mail_replyto           = $SetupVariablesApis->{-MAIL_REPLYTO};
	 $mail_to_user           = $SetupVariablesApis->{-MAIL_TO_USER};
	 $mail_to_member         = $SetupVariablesApis->{-MAIL_TO_Member};
	 $mail_to_discussion     = $SetupVariablesApis->{-MAIL_TO_DISCUSSION};
	 $mail_list_bcc          = $SetupVariablesApis->{-MAIL_LIST_BCC};
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
    $mail_from             = $SetupVariablesBMaster->{-MAIL_FROM};
    $mail_to               = $SetupVariablesBMaster->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME      = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
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
    $last_update              = $SetupVariablesDemo->{-LAST_UPDATE};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};

}

elsif ($SiteName eq "ECF" ||
       $SiteName eq "ECFDev" ) {
use ECFSetup;
  my $UseModPerl = 1;
  my $SetupVariablesECF   = new ECFSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesECF->{-APP_LOGO_ALT};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ECF'; 
#    $TableName              = 'ecf_todo_tb';
#    $ProjectTableName       = 'ecf_project_tb';
 #Mail settings
    $mail_from               = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesECF->{-MAIL_REPLYTO};
	 $mail_to_user            = $SetupVariablesECF->{-MAIL_TO_USER};
	 $mail_to_member          = $SetupVariablesECF->{-MAIL_TO_Member};
	 $mail_to_discussion      = $SetupVariablesECF->{-MAIL_TO_DISCUSSION};
	 $mail_list_bcc           = $SetupVariablesECF->{-MAIL_LIST_BCC};
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
     
}

elsif ($SiteName eq "ENCY") {
use ENCYSetup;
  my $UseModPerl = 1;
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
     $home_view            = $SetupVariablesGrindrod->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGrindrod->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesGrindrod->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGrindrod->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGrindrod->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGrindrod->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGrindrod->{-SITE_DISPLAY_NAME};
#     $FAVICON                 = $SetupVariablesGrindrod->{-FAVICON};
#    $ANI_FAVICON             = $SetupVariablesGrindrod->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGrindrod->{-PAGE_TOP_VIEW};
#     $FAVICON_TYPE            = $SetupVariablesGrindrod->{-FAVICON_TYPE};
} 
elsif ($SiteName eq "HE" ) {
use HESetup;
  my $UseModPerl = 1;
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
#     $site_update              = $SetupVariablesIM->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesIM->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesIM->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesIM->{-MAIL_REPLYTO};
#     $shop                     = $SetupVariablesIM->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesIM->{-SITE_DISPLAY_NAME};
     $homeviewname             =$home_view;
     }






elsif ($SiteName eq "CSC" or
       $SiteName eq "CSCDev"
       ) {
use CSCSetup;
  my $SetupVariablesCSC   = new  CSCSetup($UseModPerl);
if ($SiteName eq "CSCDev"
       ) {     
    $SITE_DISPLAY_NAME        = "Dev.".$SetupVariablesCSC->{-SITE_DISPLAY_NAME};
       $APP_NAME_TITLE           = "CSC";
$AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
       } else {
    $SITE_DISPLAY_NAME        = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
    $APP_NAME_TITLE           = "Computer System Consulting.ca";
         $AUTH_TABLE               = $SetupVariablesCSC ->{-AUTH_TABLE};
       }
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

}
elsif ($SiteName eq "Shanta"){
use ShantaSetup;
  my $UseModPerl = 1;
  my $SetupVariablesShanta = new ShantaSetup($UseModPerl);
    $CSS_VIEW_URL           = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesShanta->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesShanta->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesShanta->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesShanta->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesShanta->{-APP_LOGO_ALT};
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesShanta->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesShanta->{-HTTP_HEADER_DESCRIPTION};
    $home_view               = $SetupVariablesShanta->{-HOME_VIEW}; 
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SITE_DISPLAY_NAME       = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
  }


 elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $UseModPerl = 1;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
    $homeviewname            = 'BrewHomeView';
    $home_view               = $SetupVariablesBrew->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW         = $SetupVariablesBrew->{-BASIC_DATA_VIEW};
    $page_top_view           = $SetupVariablesBrew->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesBrew->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesBrew->{-LEFT_PAGE_VIEW};
#Mail settings
    $mail_from               = $SetupVariablesBrew->{-MAIL_FROM}; 
    $mail_to                 = $SetupVariablesBrew->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesBrew->{-MAIL_REPLYTO};
    $CSS_VIEW_URL            = $SetupVariablesBrew->{-CSS_VIEW_NAME}||'blank';
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesBrew->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesBrew->{-HTTP_HEADER_DESCRIPTION};
    $IMAGE_ROOT_URL          = $SetupVariablesBrew->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL       = $SetupVariablesBrew->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET             = $SetupVariablesBrew->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS      = $SetupVariablesBrew->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET         = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $AUTH_TABLE              = $SetupVariablesBrew->{-AUTH_TABLE};
    $DEFAULT_CHARSET         = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $APP_DATAFILES_DIRECTORY =  $GLOBAL_DATAFILES_DIRECTORY."/Brew";
#    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $SITE_DISPLAY_NAME       = $SetupVariablesBrew->{-SITE_DISPLAY_NAME};
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
     $app_logo                = $SetupVariablesAltPower->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesAltPower->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesAltPower->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesAltPower->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesAltPower->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesAltPower->{-HOME_VIEW};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
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
     $site_update              = $SetupVariablesLumbyThrift->{-SITE_LAST_UPDATE};
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
elsif ($SiteName eq "Skye") {
use SkySetup;
  my $UseModPerl = 1;
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
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Sky'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
}

elsif ($SiteName eq "Sustainable" or
       $SiteName eq "SustainableDev" 
       ) {
use SustainableSetup;
  my $SetupVariablesSustainable   = new SustainableSetup($UseModPerl);
     $Affiliate               = $SetupVariablesSustainable->{-AFFILIATE};
     $APP_NAME_TITLE          = $SetupVariablesSustainable->{-APP_NAME_TITLE};
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
elsif ($SiteName eq "TelMark") {
use TelMarkSetup;
  my $UseModPerl = 1;
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
     $mail_from               = 'telmark@shanta.org'; 
     $mail_to                 = 'csc_user_list@computersystemconsulting.ca';
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
 }
elsif ($SiteName eq "WiseWoman") {
use WWSetup;
  my $SetupVariablesWiseWoman   = new WWSetup($UseModPerl);
     $APP_NAME_TITLE          = "WiseWoman";
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesWiseWoman->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesWiseWoman->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesWiseWoman->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesWiseWoman->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesWiseWoman->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesWiseWoman->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesWiseWoman->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesWiseWoman->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesWiseWoman->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablesWiseWoman->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesWiseWoman->{-LAST_UPDATE}; 
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
     $homeviewname            = $SetupVariablesUSBM->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesUSBM->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesUSBM->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesUSBM->{-LAST_UPDATE};
     $site_update             = $SetupVariablesUSBM->{-SITE_LAST_UPDATE};
 }
my $apsubmenu = 'BuyApplicationSubMenuView';
if  ($CGI->param('view') eq 'ContactView'){
 $apsubmenu ='' ;
}
my $footer           = " ----------------------------------------
You received this email because you requested a subscription to ."
.$listname
." We apologise if you received it in error or if your information is incorrect.
Please follow the instructions below to unsubcribe or change your settings:

Point your browser at  " .$AccountURL." to manage your account.

Alternatively, use the email commands:

Subscribe To " .$listname."
Send email to " .$subscrib."
 Unsubscribe From " .$listname." : Send email to
  " .$unsubscrib ."


Send mail to the following for info and FAQ for this list:
".$listinfo ." ". $listfaq ."

The ".$SitedisplyName ." respects your privacy. We do not sell our mailing list information nor do we release your information to anyone, except as required by law.

Thanks,"
.$salutaion;
    $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
if ($CGI->param('embed')){
   $page_top_view = "EmbedPageTopView";
   $page_bottom_view = "";
   $RecordsToDisplay = 10;
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
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -page_left_view          => $page_left_view,
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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||$mail_from,
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
       owner            => 'Owner',
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       subject          => 'Subject',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       category	      	=> 'Project Code',
       description      => 'Description',
       status           => 'Status',
       priority         => 'Priority',
       last_mod_by      => 'Last Modified By',
       last_mod_date    => 'Last Modified Date',
      },

    -RULES => [
      #  -ESCAPE_HTML_TAGS => [
      #      -FIELDS => [qw(
      #          *
      #      )]
      #  ],

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
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       subject          => 'Subject',
       description      => 'Description',
       category	      	=> 'Project Code',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       status           => 'Status',
       priority         => 'Priority',
    },

    -RULES => [
      #  -ESCAPE_HTML_TAGS => [
      #      -FIELDS => [qw(
      #          *
      #      )]
      #  ],

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
       owner
       start_date
       due_date
       price
       location
       item_name
       description
       url
       email
       phone
       category
       status
       priority
       share
       last_mod_by
       last_mod_date
       username_of_poster
       group_of_poster
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
      1 => 'NEW',
      2 => 'On hand',
      3 => 'Sold',
    );



my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     subject => [
                 -DISPLAY_NAME => 'Name of item',
                 -TYPE         => 'textfield',
                 -NAME         => 'subject',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
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

     start_day => [
                 -DISPLAY_NAME => 'Date add to start',
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

  share => [
        -DISPLAY_NAME => 'What level of sharing do you want? ',
        -TYPE         => 'popup_menu',
        -NAME         => 'share',
        -LABELS  => { 
               '' 	=> "I'm not sure",
               'pub'		=> 'All sites.',
               'priv'		=> 'Only This Site.',
        },
        -VALUES       => [
                      '',
                      'pub',
                      'priv',
        ]
    ],

     priority => [
                 -DISPLAY_NAME => 'Priority',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'priority',
                 -VALUES       => [sort {$a cmp $b} keys %priority],
                 -LABELS       => \%priority,
                 -INPUT_CELL_COLSPAN => 3,
                ],

     status => [
                 -DISPLAY_NAME => 'Status',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'status',
                 -VALUES       => [sort {$a cmp $b} keys %status],
		 -LABELS       => \%status,
                 -INPUT_CELL_COLSPAN => 3,
                ],
     owner => [
        -DISPLAY_NAME => 'Owner',
        -TYPE         => 'textfield',
        -NAME         => 'owner',
        -SIZE         => 30,
	     -VALUE        => $username,
        -MAXLENGTH    => 80
    ],

     sitename => [
        -DISPLAY_NAME => 'Site Name',
        -TYPE         => 'textfield',
        -NAME         => 'sitename',
        -SIZE         => 30,
	-VALUE        => $SiteName,
        -MAXLENGTH    => 80
    ],

     price => [
        -DISPLAY_NAME => 'Item price',
        -TYPE         => 'textfield',
        -NAME         => 'price',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     url => [
        -DISPLAY_NAME => "Web Site do not add HTTP://",
        -TYPE         => 'textfield',
        -NAME         => 'url',
        -SIZE         => 80,
        -MAXLENGTH    => 150
    ],
    
     email => [
        -DISPLAY_NAME => 'Email address',
        -TYPE         => 'textfield',
        -NAME         => 'email',
        -SIZE         => 30,
        -MAXLENGTH    => 75
    ],
 
     number => [
        -DISPLAY_NAME => 'Number on offer.',
        -TYPE         => 'textfield',
        -NAME         => 'phone',
        -VALUE        => '1',
        -SIZE         => 3,
        -MAXLENGTH    => 80
    ],
     phone => [
        -DISPLAY_NAME => 'Phone number',
        -TYPE         => 'textfield',
        -NAME         => 'phone',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
     item_name => [
        -DISPLAY_NAME => 'Name of product or service',
        -TYPE         => 'textfield',
        -NAME         => 'item_name',
        -SIZE         => 30,
        -MAXLENGTH    => 250
    ],

    location => [
        -DISPLAY_NAME => 'Location of item.',
        -TYPE         => 'textfield',
        -NAME         => 'location',
        -SIZE         => 30,
        -MAXLENGTH    => 100
    ],

    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],
   );
#      [qw(due_day due_mon due_year)]


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER =  (
     qw(category),
     qw(sitename),     
     qw(owner),
     [qw(start_day start_mon start_year)],
      qw(item_name),
      qw(description),
      qw(number),
      qw(price),
     qw(email),
     qw(url),
      qw(phone),
     [qw(location)],
     qw(comments),
     [qw(status)],
     qw(share),
    );


my %ACTION_HANDLER_PLUGINS =
    (

 #    'Default::DisplayAddFormAction' =>
 #    {
 #     -DisplayAddFormAction     => [qw(Plugin::Todo::DisplayAddFormAction)],
 #    },

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

 #    'Default::DefaultAction' => 
 #    {
 #     -loadData_END             => [qw(Plugin::Todo::Records2Display)],
 #     -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
 #    },

 #    'Default::DisplayViewAllRecordsAction' => 
 #    {
 #     -loadData_END             => [qw(Plugin::Todo::Records2Display)],
 #     -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
 #    },

 #    'Default::DisplaySimpleSearchResultsAction' => 
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

#     'Default::PerformPowerSearchAction' => 
#     {
#      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
#      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
#     },



    );


my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
#$site = 'file';
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (    -TYPE                       => 'File',
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$TableName.dat",
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
	        -TABLE        => $TableName,
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
        username_of_poster
        group_of_poster
        date_time_posted
);

my	@PROJ_DATASOURCE_CONFIG_PARAMS;

if ($site eq "file"){
	@PROJ_DATASOURCE_CONFIG_PARAMS = (
    -TYPE                       => 'File',
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$SiteName._project_tb.dat",
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
);#$SiteName.
}else{
	@PROJ_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => $ProjectTableName,
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@PROJECT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);
}

my @BUYCAT_DATASOURCE_FIELD_NAMES = qw(
        record_id
        status
        category
        subcategory
        sitename
        display_value
        client_name
        comments        
        username_of_poster
        group_of_poster
        date_time_posted
);

my  @BUYCAT_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => $DropListName,
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@BUYCAT_DATASOURCE_FIELD_NAMES,
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


my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -BUYCAT_DATASOURCE_CONFIG_PARAMS  => \@BUYCAT_DATASOURCE_CONFIG_PARAMS,
    -PROJECT_DATASOURCE_CONFIG_PARAMS   => \@PROJ_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

my @PROJECT_DATASOURCE_CONFIG_PARAMS = (
    -PROJECT_DATASOURCE_CONFIG_PARAMS     => \@PROJ_DATASOURCE_CONFIG_PARAMS,
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
       category
       start_date
       end_date
       description
       estimated_man_hours 
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
    -TO       => $mail_to.','.$mail_to_discussion,
    -BCC      => $mail_list_bcc,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION->getAttribute(-KEY =>
'auth_email')||$mail_from,
    -TO       => $mail_to.','.$mail_to_discussion,
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
    -LOG_ENTRY_PREFIX =>  $APP_NAME_TITLE.' |'
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
       BCHPACSSView
       ECFCSSView
       ApisCSSView
       CSPSCSSView
       CSCCSSView

       DetailsRecordView
       BasicDataView
       ContactView
       BuySellHomeView

       AddRecordView
       AddRecordConfirmationView
       AddAcknowledgementView

       DeleteRecordConfirmationView
       DeleteAcknowledgementView

       ModifyRecordView
       ModifyRecordConfirmationView
       ModifyAcknowledgementView

       ProductView
       PowerSearchFormView
       OptionsView
       LogoffView
       PrivacyView
       BeeDiseaseView
       BuyCatagoryView
       JobView
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
    -DEFAULT_CHARSET                => $DEFAULT_CHARSET,
    -DISPLAY_FIELDS                 => [qw(
        category
        item_name
        price
        url
        location
        )],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        description
	     item_name
	     comments
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        description
	     item_name
 	comments
   )],
    -FIELD_NAME_MAPPINGS     => {
        'category'=> 'Catagory',
        'description' => 'Description',
        'item_name'   => 'Item for sale',
        'location'    => 'location',
        'url'         => 'Web Site',
        'status'      => 'Status',
        'price'       => 'Price',
        'priority'    => 'Priority',
        },
    -HOME_VIEW               => 'BasicDataView',
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => $columnstoview,
    -SORT_FIELDS             => $SortFields,
    -VERSION                 => $version,
);  

######################################################################
#                           DATE TIME SETUP                          #
######################################################################

my @DATETIME_CONFIG_PARAMS = 
    (
     -TYPE => (HAS_CLASS_DATE ? 'ClassDate' : 'DateManip'),
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

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST =
    qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction

       Default::PopulateInputWidgetDefinitionListWithBuyCategoryWidgetAction
       CSC::ProcessShowAllOpenToDosAction
       Apis::ProcessShowBillsRecordsAction
       Default::DisplayDetailsRecordViewAction

       Default::DisplayDeleteFormAction
       Default::ProcessDeleteRequestAction
       Default::DisplayDeleteRecordConfirmationAction

       Default::DisplayModifyFormAction
       BuyAndSell::ProcessModifyRequestAction
       Default::DisplayModifyRecordConfirmationAction

       Default::DisplayAddFormAction
       BuyAndSell::ProcessAddRequestAction
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
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APP_NAME                               => $APP_NAME,
    -APPLICATION_SUB_MENU_VIEW_NAME         => $apsubmenu,
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => 'BuySellHomeView',
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $RecordsToDisplay || 10,
    -SORT_FIELD1                            => $SortField1,
    -SORT_FIELD2                            => $SortField2,
    -SORT_DIRECTION                         => $SortDirection|| 'DESC',
#   -SORT_DIRECTION                         => 'DESC',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -GROUP_OF_POSTER                        => $GROUP_OF_POSTER,
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
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LAST_UPDATE                            => $last_update,
    -LOCAL_IP                               => $LocalIp,
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MESSAGE_FOOTER                         => $footer,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 1,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 1,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
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
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -SITE_NAME                              => $SiteName,
    -SITE_LAST_UPDATE                       => $site_update,
    -PAGE_TOP_VIEW                          =>  $page_top_view ,
    -PAGE_LEFT_VIEW                         =>  $page_left_view,
    -PAGE_BOTTOM_VIEW                       =>  $page_bottom_view,
    -SELECT_FORUM_VIEW		            => 'SelectForumView',
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
