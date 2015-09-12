#!/usr/bin/perl -wT
# 	$Id: todo.cgi,v 1.5 2004/02/04 19:36:17 shanta Exp shanta $	

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
       ../HTMLTemplates/Brew
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CS
       ../HTMLTemplates/CS
       ../HTMLTemplates/Demo
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/ECF
       ../HTMLTemplates/HE
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/SkyeFarm
       ../HTMLTemplates/Todo
       ../HTMLTemplates/VitalVic
       ../HTMLTemplates/WW
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

    my $debug = 0;

my $APP_NAME = "todo";
my $Affiliate = 001;

my $APP_NAME_TITLE = "Todo Manager";
my $SiteName =  $CGI->param('site');
my $site_update;
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $last_update  = 'Febuary 17	, 2015';

    my $homeviewname ;
    my $home_view = 'ToDoHomeView'; 
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
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $DEFAULT_CHARSET; 
    my $additonalautusernamecomments;
    my $SetupVariables;
	  my $TableName;
 	  my $sitename;
    my $site;
    my $ProjectTableName;
    my $records;
    my $frame;
    my $droplist_tb = 'csc_droplist_tb';
    my $log_tb      = 'csc_log-tb';
    my $client_tb   = 'csc_client_tb';
    my $UseModPerl = 1;
    my $HasMembers = 0;


use SiteSetup;
   $SetupVariables  = new SiteSetup($UseModPerl);
#    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $Affiliate                = $SetupVariables->{-AFFILIATE};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-page_left_view};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_KEYWORDS  = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
   $AUTH_TABLE             = $SetupVariables->{-AUTH_TABLE};
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
    $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
    $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
    $DATAFILES_DIRECTORY = $APP_DATAFILES_DIRECTORY;
    $site_session = $DATAFILES_DIRECTORY.'/Sessions';
    $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';
    $TableName             = 'csc_todo_tb';
    $ProjectTableName      = 'csc_project_tb';
    

 
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


if ($CGI->param('page_top_view') eq'SBPageTopView'){
$target='_content';
 $columnstoview = [qw(
        project_code
        subject
        priority
        due_date
        )];
 $SortFields=[qw(
        project_code
        due_date
        priority
        )];
 $SortField2='due_date';
 $SortField1='priority';
 $SortDirection='DESC' ;
 $RecordsToDisplay=150;
}else{
$target='_self';
 $columnstoview=[qw(
        record_id
        project_code
        subject
        abstract
        start_date
        status
        priority

        )];
$SortFields=[qw(
        due_date
        start_date
        abstract
        project_code
        status
        priority
        )];
 $SortField1=$CGI->param('sort_field1') ||'priority';
 $SortField2=$CGI->param('sort_field2') ||'due_date';
 $RecordsToDisplay=250;
 $SortDirection='DESC';#ASC
}
my $SESSION_DIR;
#if ($SiteName eq "rv") {
#  $SESSION_DIR ="../store/shops/rv/Sessions";
#}else{
  $SESSION_DIR = "$GLOBAL_DATAFILES_DIRECTORY/Sessions";
#}
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
$sitename =$SiteName;
my $GROUP_OF_POSTER = $SESSION -> getAttribute(-KEY => 'auth_groups')||'normal';
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');
my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');


if ($SiteName eq "Apis") {
use ApisSetup;
  my $SetupVariablesApis   = new ApisSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesApis->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesApis->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesApis->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesApis->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesApis->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesApis->{-APP_LOGO_ALT};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Apis'; 
#    $TableName             = 'apis_todo_tb';
#    $ProjectTableName      = 'apis_project_tb';
     $CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
 }

elsif ($SiteName eq "AltPowerDev" or
       $SiteName eq "AltPower" ) {
use AltPowerSetup;
  my $SetupVariablesAltPower   = new AltPowerSetup($UseModPerl);
      $Affiliate               = $SetupVariablesAltPower->{-AFFILIATE};
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
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/AltPower'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
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
#     $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
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

 elsif ($SiteName eq "Brew") {

use  BrewSetup;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
    $homeviewname          = 'BrewHomeView';
#    $home_view             = $SetupVariablesBrew->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariablesBrew->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariablesBrew->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesBrew->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBrew->{-LEFT_PAGE_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesBrew->{-MAIL_FROM}; 
    $mail_to               = $SetupVariablesBrew->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBrew->{-MAIL_REPLYTO};
    $CSS_VIEW_URL          = $SetupVariablesBrew->{-CSS_VIEW_NAME}||'blank';
    $HTTP_HEADER_KEYWORDS  = $SetupVariablesBrew->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesBrew->{-HTTP_HEADER_DESCRIPTION};
    $IMAGE_ROOT_URL        = $SetupVariablesBrew->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL     = $SetupVariablesBrew->{-DOCUMENT_ROOT_URL};
    $LINK_TARGET           = $SetupVariablesBrew->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariablesBrew->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET       = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $AUTH_TABLE            = $SetupVariablesBrew->{-AUTH_TABLE};
    $DEFAULT_CHARSET       = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $APP_DATAFILES_DIRECTORY    =  $GLOBAL_DATAFILES_DIRECTORY."/Brew";
#    $site = $SetupVariables->{-DATASOURCE_TYPE};
    $SITE_DISPLAY_NAME     = $SetupVariablesBrew->{-SITE_DISPLAY_NAME};
}


 
elsif($SiteName eq "CS") {
use CSSetup;
  my $SetupVariablesCS  = new  CSSetup($UseModPerl);
    $homeviewname          = 'TodoHomeView';
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/CS'; 
    $SITE_DISPLAY_NAME       = 'Country Stores';
    $HTTP_HEADER_KEYWORDS    = $SetupVariablesCS->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesCS->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCS->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME           = $SetupVariablesCS->{-CSS_VIEW_NAME};
    $CSS_VIEW_URL            = $SetupVariablesCS->{-CSS_VIEW_NAME};
}

elsif ($SiteName eq "CSC" ||
       $SiteName eq "CSCDev") 
       {
use CSCSetup;
  my $SetupVariablesCSC   = new  CSCSetup($UseModPerl);
 if ($SiteName eq "CSCDev"
       ) { $AUTH_TABLE               = $SetupVariablesCSC ->{-ADMIN_AUTH_TABLE}; 
       } else {
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
    $SITE_DISPLAY_NAME       = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};

}

elsif ($SiteName eq "Demo" or
      $SiteName eq "DemoHelpDesk") {
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
    $app_logo                 = $SetupVariablesDemo->{-APP_LOGO};
    $app_logo_height          = $SetupVariablesDemo->{-APP_LOGO_HEIGHT};
    $app_logo_width           = $SetupVariablesDemo->{-APP_LOGO_WIDTH};
    $app_logo_alt             = $SetupVariablesDemo->{-APP_LOGO_ALT};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
#    $homeviewname             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-SITE_LAST_UPDATE};
    $FAVICON                  = $SetupVariablesDemo->{-FAVICON};
    $ANI_FAVICON              = $SetupVariablesDemo->{-ANI_FAVICON};
    $FAVICON_TYPE             = $SetupVariablesDemo->{-FAVICON_TYPE};

}

elsif ($SiteName eq "ECF" || 
       $SiteName eq "ECFDev") {
use ECFSetup;
  my $SetupVariablesECF   = new ECFSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesECF->{-CSS_VIEW_NAME};
     $Affiliate               = $SetupVariablesECF->{-AFFILIATE};
    $AUTH_TABLE              = $SetupVariablesECF->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesECF->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesECF->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesECF->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesECF->{-APP_LOGO_ALT};
    $CSS_VIEW_URL            = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ECF'; 
#    $TableName              = 'ecf_todo_tb';
 #   $ProjectTableName       = 'ecf_project_tb';
     $SITE_DISPLAY_NAME      = $SetupVariablesECF->{-SITE_DISPLAY_NAME};
    
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
     $CSS_VIEW_URL             = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesHE->{-LAST_UPDATE}; 
#     $site_update              = $SetupVariablesHE->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
#     $shop                     = $SetupVariablesHE->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
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
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $mail_to                 = $SetupVariablesOrganic->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesOrganic->{-MAIL_REPLYTO};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/Orgnaic'; 
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
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
     $CSS_VIEW_URL            = $SetupVariablesNoop->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
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
    $APP_NAME_TITLE        = "Vital Victoria ToDo ";
    $ProjectTableName      = 'vitalvic_project_tb';
    $SITE_DISPLAY_NAME       = $SetupVariablesVitalVic->{-SITE_DISPLAY_NAME};
}
elsif ($SiteName eq "Skye" or
       $SiteName eq "SkyeStore") {
use SkyeFarmSetup;
  my $SetupVariablesSkyeFarm   = new SkyeFarmSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesSkyeFarm->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesSkyeFarm->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesSkyeFarm->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesSkyeFarm->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesSkyeFarm->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesSkyeFarm->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesSkyeFarm->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesSkyeFarm->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesSkyeFarm->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablesSkyeFarm->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSkyeFarm->{-LAST_UPDATE}; 
 #Mail settings
     $site_update              = $SetupVariablesSkyeFarm->{-SITE_LAST_UPDATE};
    $mail_from             = $SetupVariablesSkyeFarm->{-MAIL_FROM};
    $mail_to               = $SetupVariablesSkyeFarm->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesSkyeFarm->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME     = $SetupVariablesSkyeFarm->{-SITE_DISPLAY_NAME};
   $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/SkyeFarm';
  }elsif ($SiteName eq "WiseWoman") {
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



my $apsubmenu = 'ApplicationSubMenuView';
if  ($CGI->param('view') eq 'ContactView'){
 $apsubmenu ='' ;
}
my $modify = '1';
my $delete = '1';
my $add ='1';
my $group_search = '1';

 if ($username eq "Shanta"  ) {
    $modify = '1';
    $delete = '1';
    $group_search = '0';
    $add ='1';
  }
if ($CGI->param('embed')){
   $page_top_view = "EmbedPageTopView";
   $records = 1;
   }
if ($CGI->param('frame')){
     $frame        = "1";
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
 	  -FAVICON                 => $FAVICON || '/images/apis/favicon.ico',
	  -ANI_FAVICON             => $ANI_FAVICON,
	  -FAVICON_TYPE            => $FAVICON_TYPE,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -LINK_TARGET             => $LINK_TARGET,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
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
       sitename            => 'sitename',
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       subject          => 'Subject',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       project_code	      	=> 'Project Code',
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
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       subject          => 'Subject',
       description      => 'Description',
       project_code	      	=> 'Project Code',
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
       start_date
       due_date
       subject
       description
       estimated_man_hours
       accumulative_time
       project_code
       status
       priority
       share
       last_mod_by
       last_mod_date
       group_of_poster
      );

# prepare the data then used in the form input definition
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (2011..2020);
my %days  = ();
$days{$_} = $_ for (1..31);

my %priority =
    (
                 
      1 => 'LOW',
      2 => 'MODERATE',
      3 => 'CONSIDERABLE',
      4 => 'HIGH',
      5 => 'EXTREME',
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

  share => [
        -DISPLAY_NAME => 'What level of sharing do you want? ',
        -TYPE         => 'popup_menu',
        -NAME         => 'share',
        -LABELS  => { 
               '' 	=> "I'm not sure",
               'pub'		=> 'Every Body',
               'priv'		=> 'This is personal.',
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
#   sitename => [
 #       -DISPLAY_NAME => 'Site',
#        -TYPE         => 'popup_menu',
#        -NAME         => 'sitename',
#        -VALUES       => [qw(All AltPower Apis BCHPA BeeMaster CSC CS ECF ENCY
 #                         Extropia Forager Fly Marts News Organic RV Shanta 
 #                         Skye TelMark USBM VitalVic 
#                          )]
#    ],


     accumulative_time => [
        -DISPLAY_NAME => 'Accumulated Please Add time to entry',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    estimated_man_hours => [
        -DISPLAY_NAME => 'Est. Man Hours',
        -TYPE         => 'textfield',
        -NAME         => 'estimated_man_hours',
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
   );


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (
       qw(project_code),
       qw(sitename),
       qw(subject ),
       [qw(start_day start_mon start_year)],
       [qw(due_day due_mon due_year)],
       qw(description),
       qw(priority),
       [qw(status)],
       qw(estimated_man_hours),
       qw(accumulative_time),
       qw(comments),
       qw(share),
    );


my %ACTION_HANDLER_PLUGINS =
    (

     'Default::DisplayAddFormAction' =>
     {       qw(estimated_man_hours),
       qw(accumulative_time),

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
        sitename
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

my @DROPLIST_DATASOURCE_FIELD_NAMES = qw(
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

my  @DROPLIST_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => $droplist_tb,
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

my @LOG_DATASOURCE_FIELD_NAMES = qw(
        record_id
        todo_record_id
        time
        username_of_poster
        group_of_poster
);

my  @LOG_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => $log_tb,
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@LOG_DATASOURCE_FIELD_NAMES,
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
	        -TABLE        => $client_tb,
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
    -CLIENT_DATASOURCE_CONFIG_PARAMS   => \@CLIENT_DATASOURCE_CONFIG_PARAMS,
    -DROPLIST_DATASOURCE_CONFIG_PARAMS  => \@DROPLIST_DATASOURCE_CONFIG_PARAMS,
    -LOG_DATASOURCE_CONFIG_PARAMS       => \@LOG_DATASOURCE_CONFIG_PARAMS,
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
       project_code
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
       ToDoHomeView
       MailView
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
    -DEFAULT_CHARSET                => $DEFAULT_CHARSET,
    -DISPLAY_FIELDS                 => [qw(
        project_code
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
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_HTML_TAG => [qw(
        description
	subject
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        description
 	subject
   )],
    -FIELD_NAME_MAPPINGS     => {
        'project_code'=> 'Project Code',
        'subject'     => 'Subject',
        'description' => 'Description',
        'start_date'  => 'Start Date',
        'due_date'    => 'Due Date',
        'status'      => 'Status',
        'priority'    => 'Priority',
        },
    -HOME_VIEW               => 'TodoHomeView',
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -HTTP_HEADER_KEYWORDS    => $HTTP_HEADER_KEYWORDS,
    -HTTP_HEADER_DESCRIPTION => $HTTP_HEADER_DESCRIPTION,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => $columnstoview,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SORT_FIELDS             => $SortFields,
);  

######################################################################
#                           DATE TIME SETUP                             #
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
#CSC::PopulateInputWidgetDefinitionListWithAccumlatedLogTimeWidgetAction

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST =
    qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction
       
              CSC::PopulateInputWidgetDefinitionListWithProjectCodeWidgetAction
       CSC::PopulateInputWidgetDefinitionListWithDropListSiteNameWidgetAction
       CSC::ProcessShowAllOpenToDosAction
       Apis::ProcessShowBillsRecordsAction
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
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => $apsubmenu,
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => 'ToDoHomeView',
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
	 -DEBUG                                  => $CGI->param('debug')||0,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $RecordsToDisplay || 210,
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
    -LOCAL_IP                               => $LocalIp,
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
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => $group_search,
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