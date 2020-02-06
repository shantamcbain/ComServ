#!/usr/bin/perl -wT
#version .05
# 	$Id: bbs.cgi,v 1.2 2004/01/05 19:51:15 shanta Exp shanta $
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
    qw(../Modules/Extropia/View/BBS
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/BBS
       ../HTMLTemplates/AltPower
       ../HTMLTemplates/Apis
       ../HTMLTemplates/Brew
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/HelpDesk		
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/Extropia
       ../HTMLTemplates/Fly
       ../HTMLTemplates/HE
       ../HTMLTemplates/IM
       ../HTMLTemplates/Organic
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/TelMark
       ../HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out for Perl 5.60 bugs. Uncomment in 5.61
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");
$CGI->autoEscape(undef);

######################################################################
#                          SITE SETUP                             #
######################################################################

my $APP_NAME         = "bbs";
my $APP_NAME_TITLE   = "Forums";
my $SiteName =  $CGI->param('site') || "CSC";

#Mail settings
    my $homeviewname ;
    my $home_view; 
    my $BASIC_DATA_VIEW; 
    my $page_top_view;
    my $page_bottom_view;
    my $page_left_view;
#Mail settings
    my $mail_from; 
    my $mail_to;
    my $mail_to_admin;
    my $mail_replyto;
    my $subscrib;
    my $unsubscrib;
    my $listinfo;
    my $listfaq;
    my $CSS_VIEW_NAME;
    my $app_logo;
    my $app_logo_height;
    my $app_logo_width;
    my $app_logo_alt;
    my $FAVICON;
    my $ANI_FAVICON;
    my $FAVICON_TYPE;
    my $IMAGE_ROOT_URL; 
    my $DOCUMENT_ROOT_URL;
    my $DEFAULT_CHARSET;
    my $site;
    my $GLOBAL_DATAFILES_DIRECTORY;
    my $TEMPLATES_CACHE_DIRECTORY;
    my $APP_DATAFILES_DIRECTORY;
    my $DATAFILES_DIRECTORY;
    my $site_session;
    my $auth;
    my $MySQLPW;
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my  $additonalautusernamecomments;
    my  $AccountURL;
    my $listname;
    my $salutaion;
     my $PAGE_LIST_VIEW;
     my $SitedisplyName;
     my %VALID_FORUMS;
    my $ListTable = 'bbs_tb';
    my $HTTP_HEADER_KEYWORDS;
    my $HTTP_HEADER_DESCRIPTION;
    my $listfaq;
    my $mail_cc;
    
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $last_update;
    my $HasMembers = 0;

use SiteSetup;
  my $UseModPerl = 0;
  my $SetupVariables  = new SiteSetup($UseModPerl);
    $home_view             = $SetupVariables->{-HOME_VIEW}; 
    $homeviewname          = $SetupVariables->{-HOME_VIEW_NAME};
    $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
    $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
    $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariables->{-page_left_view};
    $MySQLPW               = $SetupVariables->{-MySQLPW};
    $DBI_DSN               = $SetupVariables->{-DBI_DSN};
    $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
    $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
#Mail settings
#    $mail_from             = $SetupVariables->{-MAIL_FROM}; 
#    $mail_to               = $SetupVariables->{-MAIL_TO};
#    $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
    $SiteName               =  $CGI->param('site')|| $SetupVariables->{-FAVICON_TYPE};
    $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
    $app_logo              = $SetupVariables->{-APP_LOGO};
    $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
    $IMAGE_ROOT_URL        = $SetupVariables->{-IMAGE_ROOT_URL}; 
    $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
    $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
    $LINK_TARGET           = $SetupVariables->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariables->{-HTTP_HEADER_PARAMS};
    $GLOBAL_DATAFILES_DIRECTORY = '/home/shanta/Datafiles/'||$SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
    $additonalautusernamecomments  = $SetupVariables->{-ADDITIONALAUTHUSERNAMECOMMENTS};
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
my $username =  $SESSION ->getAttribute(-KEY => 'auth_username');
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_groups');

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
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariablesApis->{-TEMPLATES_CACHE_DIRECTORY,};
$CSS_VIEW_URL            = $SetupVariablesApis->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/Apis";
#Mail settings
    $mail_from        = 'apis_bbs@forager.com';
    $mail_to          = 'apis_discussion@beemaster.ca';
    $subscrib         = '<apis_discussion-subscribo@forager.com>';
    $unsubscrib       = '<apis_discussion-unsubscribe@forager.com>';
    $listinfo         = '<apis_discussion-info@@forager.com>';
    $listfaq          = '<apis_discussion-faq@@forager.com>';
    $mail_replyto     = 'apis_discussion@forager.com';
    $PAGE_LIST_VIEW   = 'ApisSubscribeListView';
    $SITE_DISPLAY_NAME       = $SetupVariablesApis->{-SITE_DISPLAY_NAME};
    $salutaion        = "Apis at beemaster.ca ";
    %VALID_FORUMS     = (
       announcements         =>  'Announcements',
       breeding              =>  'Breeding',
       diseases              =>  'Diseases and pests',
       pollination           =>  'Pollination',
       general               =>  'General Bee keeping',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       therapies             =>  'Therapies',
       winter                =>  'Wintering',
       csc_helpdesk          =>  'HelpDesk',
                                );
    $AccountURL              = "http://beemaster.ca/cgi-bin/Apis/apis.cgi" ;
    $ListTable               = 'apis_bbs_tb';
   $mail_cc          = 'Norlandbeekeepers@yahoogroups.com';
}


elsif ($SiteName eq "OKB") {
use OKbeekeeperSetup;
  my $UseModPerl = 0;
  my $SetupVariablesOKB   = new OKbeekeeperSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesOKB->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesOKB->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesOKB->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesOKB->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesOKB->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesOKB->{-APP_LOGO_ALT};
    $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariablesOKB->{-TEMPLATES_CACHE_DIRECTORY,};
    $CSS_VIEW_URL          = $SetupVariablesOKB->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/Apis";
#Mail settings
    $listname              = $SetupVariablesOKB->{-MAIL_TO_DISCUSSION};
    $mail_from        = 'okbeekepers_bbs@shanta.org';
    $mail_to          = $SetupVariablesOKB->{-MAIL_TO_USER};
    $subscrib         = '<apis_discussion-subscribo@forager.com>';
    $unsubscrib       = '<apis_discussion-unsubscribe@forager.com>';
    $listinfo         = '<apis_discussion-info@@forager.com>';
    $listfaq          = '<apis_discussion-faq@@forager.com>';
    $mail_replyto     = 'apis_discussion@forager.com';
    $PAGE_LIST_VIEW   = 'SubscribeListView';
    $SITE_DISPLAY_NAME       = $SetupVariablesOKB->{-SITE_DISPLAY_NAME};
    $salutaion        = "North Okanagan Beekeepers. ";
    %VALID_FORUMS     = (
       announcements         =>  'Announcements',
       breeding              =>  'Breeding',
       diseases              =>  'Diseases and pests',
       pollination           =>  'Pollination',
       general               =>  'General Bee keeping',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       therapies             =>  'Therapies',
       winter                =>  'Wintering',
        csc_helpdesk          =>  'HelpDesk',
                               );
    $AccountURL              = 'http://beemaster.ca/cgi-bin/Apis/apis.cgi' ;
    $ListTable               = 'apis_bbs_tb';
    $mail_cc                 = 'Norlandbeekeepers@yahoogroups.com';
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
     $listname                  = $SetupVariablesAktiv->{-MAIL_TO_DISCUSSION};
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
     $last_update               = $SetupVariablesAktiv->{-SITE_LAST_UPDATE}; 
     $APP_NAME_TITLE            ='Adventures';
     $PAGE_LIST_VIEW            = 'ActivSubscribeListView';
     %VALID_FORUMS              = (
       equipment            =>  'Equipment',
       snowtrac_maint       =>  'Maintenance',
       snowtrac             =>  'Snow-trac/Snow-Master',
       winter_camping       => 'Winter camping and survival',
       avalanche            =>  'Avalanche safety',
       other                =>  'Other',
       csc_helpdesk          =>  'HelpDesk',
                                );
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
    $mail_from                = $SetupVariablesBMaster->{-MAIL_FROM};
#    $mail_to                  = $SetupVariablesBMaster->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_REPLYTO};
    $listname                 = $SetupVariablesBMaster->{-MAIL_TO_DISCUSSION};
    $subscrib                 = '<apis_discussion-subscribo@beemaster.ca>';
    $unsubscrib               = '<apis_discussion-unsubscribe@forager.com>';
    $listinfo                 = '<apis_discussion-info@beemaster.ca>';
    $listfaq                  = '<apis_discussion-faq@beemaster.ca>';
    $mail_replyto             = $SetupVariablesBMaster->{-MAIL_TO_DISCUSSION};
    $PAGE_LIST_VIEW           = 'SubscribeListView';
    $SITE_DISPLAY_NAME        = $SetupVariablesBMaster->{-SITE_DISPLAY_NAME};
    $salutaion                = "BeeMaster.ca ";
    %VALID_FORUMS             = (
        announcements         =>  'Announcements',
        breeding              =>  'Breeding',
        diseases              =>  'Diseases and pests',
        pollination           =>  'Pollination',
        general               =>  'General Bee keeping',
        honey                 =>  'Honey',
        organic               =>  'Organic',
        therapies             =>  'Therapies',
        winter                =>  'Wintering',
       csc_helpdesk          =>  'HelpDesk',
                                 );
    $AccountURL               = 'http://beemaster/cgi-bin/Apis/apis.cgi' ;
    $ListTable                = 'apis_bbs_tb';
   $mail_cc                   = 'Norlandbeekeepers@yahoogroups.com';
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
     $home_view             = $SetupVariablesHE->{-HOME_VIEW_NAME};
     $home_view                = $SetupVariablesHE->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesHE->{-LAST_UPDATE}; 
#Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesHE->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
if ($group eq "HE_admin"){
%VALID_FORUMS                  = (
       sustainable               =>  'Sustainable',
       HEMember=>                =>  'HE private member group',
       workshops                 =>  'Workshops',
       general                   =>  'General Topics',
       HEAdmin                   =>  'HE Admin group',
       csc_helpdesk              =>  'HelpDesk',
                                );    
}

elsif ($group eq "HEMember") {
%VALID_FORUMS                  = (
       sustainable               =>  'Sustainable Group',
       HEMember=>                =>  'HE private member group',
       workshops                 =>  'Workshops',
       general                   =>  'General Topics',
       csc_helpdesk              =>  'HelpDesk',
                                );    
}
else{
%VALID_FORUMS                  = (
       sustainable               =>  'Sustainable',
       workshops                 =>  'Workshops',
       general                   =>  'General Topics',
       csc_helpdesk              =>  'HelpDesk',
                                );    
}
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."HE";   
       

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
%VALID_FORUMS                  = (
       iamnuts                   =>  'Nuts',
       gems                      =>  'Gems',
       general                   =>  'General Topics',
       csc_helpdesk              =>  'HelpDesk',
                                );    
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."Nuts";     }



elsif ($SiteName eq "Noop") {
use NoopSetup;
  my $SetupVariablesNoop  = new  NoopSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesNoop->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesNoop->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesNoop->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesNoop->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesNoop->{-PAGE_LEFT_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesNoop->{-MAIL_FROM};
    $mail_to               = $SetupVariablesNoop->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesNoop->{-MAIL_REPLYTO};
    $home_view             = $SetupVariablesNoop->{-HOME_VIEW};
    $homeviewname          = $SetupVariablesNoop->{-HOME_VIEW_NAME};
    $CSS_VIEW_URL          = $SetupVariablesNoop->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $SetupVariablesNoop->{-GLOBAL_DATAFILES_DIRECTORY}."/Organic";
    $SITE_DISPLAY_NAME       = $SetupVariablesNoop->{-SITE_DISPLAY_NAME};
    $AccountURL              = 'http://beemaster.ca/cgi-bin/Apis/apis.cgi' ;
    
%VALID_FORUMS              = (
       organicnews           =>  'Announcements',
       pandanimalbreeding    =>  'Breeding and genetics',
       diseases              =>  'Diseases and pests',
       farmtech              =>  'Farming Technique',
       general               =>  'General Topics',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       pollination           =>  'Pollination',
       seed                  =>  'Seed and seed saving',
       winter                =>  'Wintering',
       coopmembers          =>  'Co-op development',
        csc_helpdesk          =>  'HelpDesk',
                               );    

#%VALID_FORUMS          = $SetupVariablesOrganic->{-VALID_FORUMS};
 #Mail settings
    $mail_from        = 'co-op_bbs@forager.com';
    $mail_to          = 'grower_co-op_discussion@forager.com';
    $subscrib         = '<grower_co-op_discussion-subscribo@forager.com>';
    $unsubscrib       = '<grower_co-op_discussion-unsubscribe@forager.com>';
    $listinfo         = '<grower_co-op_discussion-info@@forager.com>';
    $listfaq          = '<grower_co-op_discussion-faq@@forager.com>';
    $mail_replyto     = 'grower_co-op_discussion@forager.com';
    $PAGE_LIST_VIEW   = 'OrganicSubscribeListView';
    $salutaion        = "Organic Co-Op Member";
    $AccountURL              = 'http://organicfarming.ca/cgi-bin/Organic/organic.cgi?site=noop' ;

}
elsif ($SiteName eq "Organic") {
use OrganicSetup;
  my $SetupVariablesOrganic  = new  OrganicSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesOrganic->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesOrganic->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesOrganic->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesOrganic->{-PAGE_LEFT_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesOrganic->{-MAIL_FROM};
    $mail_to               = $SetupVariablesOrganic->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesOrganic->{-MAIL_REPLYTO};
    $home_view             = $SetupVariablesOrganic->{-HOME_VIEW};
    $homeviewname          = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/Organic";
    $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
%VALID_FORUMS              = (
       organicnews           =>  'Announcements',
       pandanimalbreeding    =>  'Breeding and genetics',
       diseases              =>  'Diseases and pests',
       farmtech              =>  'Farming Technique',
       general               =>  'General Topics',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       pollination           =>  'Pollination',
       seed                  =>  'Seed and seed saving',
       winter                =>  'Wintering',
       csc_helpdesk          =>  'HelpDesk',
                                );    

#%VALID_FORUMS          = $SetupVariablesOrganic->{-VALID_FORUMS};
 #Mail settings
    $mail_from        = 'organic_bbs@organicfarming.ca';
    $mail_to          = 'organic_discussion@organicfarming.ca';
    $subscrib         = '<organic_discussion@organicfarming.ca>';
    $unsubscrib       = '<organic_discussion-unsubscribe@organicfarming.ca>';
    $listinfo         = '<organic_discussion-info@@organicfarming.ca>';
    $listfaq          = '<organic_discussion-faq@@organicfarming.ca>';
    $mail_replyto     = 'organic_discussion@organicfarming.ca';
    $PAGE_LIST_VIEW   = 'OrganicSubscribeListView';
    $salutaion        = "Organic  ";
    $AccountURL       = 'http://organicfarming.ca/cgi-bin/Organic/organic.cgi?site=Organic' ;


 if ($group eq "Organic_admin") {
    $home_view             = 'OrganicAdminHomeView';
    $homeviewname          = 'OrganicAdminHomeView';
 };
    $ListTable               = 'apis_bbs_tb';
}
elsif ($SiteName eq "BCHPA") {
use BCHPASetup;
  my $SetupVariablesBCHPA  = new  BCHPASetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesBCHPA->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesBCHPA->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesBCHPA->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBCHPA->{-PAGE_LEFT_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesBCHPA->{-MAIL_FROM};
    $mail_to               = $SetupVariablesBCHPA->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBCHPA->{-MAIL_REPLYTO};
    $home_view             = $SetupVariablesBCHPA->{-HOME_VIEW};
    $homeviewname          = $SetupVariablesBCHPA->{-HOME_VIEW_NAME};
     $CSS_VIEW_URL            = $SetupVariablesBCHPA->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/BCHPA";
    $SITE_DISPLAY_NAME       = $SetupVariablesBCHPA->{-SITE_DISPLAY_NAME};
 #Mail settings
    $mail_from        = 'apis_bbs@forager.com';
    $mail_to          = 'apis_discussion@forager.com';
    $subscrib         = '<apis_discussion-subscribo@forager.com>';
    $unsubscrib       = '<apis_discussion-unsubscribe@forager.com>';
    $listinfo         = '<apis_discussion-info@@forager.com>';
    $listfaq          = '<apis_discussion-faq@@forager.com>';
    $mail_replyto     = 'apis_discussion@forager.com';
    $PAGE_LIST_VIEW   = 'ApisSubscribeListView';
    $salutaion        = "BCHPA  ";
    $mail_cc          = 'Norlandbeekeepers@yahoogroups.com';
%VALID_FORUMS = (
       announcements         =>  'Announcements',
       breeding              =>  'Breeding',
       diseases              =>  'Diseases and pests',
       general               =>  'General Bee keeping',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       therapies             =>  'Therapies',
       winter                =>  'Wintering',
       csc_helpdesk          =>  'HelpDesk',
                                );
    $AccountURL              = 'http://shanta.org/cgi-bin/Apis/apis.cgi?site=BCHPA' ;

 if ($group eq "BCHPA_admin") {
    $home_view             = 'BCHPAAdminHomeView';
    $homeviewname          = 'BCHPAAdminHomeView';
 };
    $ListTable               = 'apis_bbs_tb';
}
elsif ($SiteName eq "CSC") {
use CSCSetup;
  my $UseModPerl = 0;
  my $SetupVariablesCSC   = new CSCSetup($UseModPerl);
     $HasMembers               = $SetupVariablesCSC->{-HAS_MEMBERS};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
     $page_top_view           = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesCSC->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesCSC->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesCSC->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesCSC->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesCSC->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesCSC->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesCSC->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/CSC";
          $mail_from        = 'csc@computersystemconsulting.ca'; 
     $mail_to          = 'csc_user_list@computersystemconsulting.ca';
     $subscrib         = '<csc_user_list-subscribe@computersystemconsulting.ca>';  
     $unsubscrib      = '<csc_user_list-unsubscribe@computersystemconsulting.ca>';
     $listinfo        = '<csc_user_list-info@computersystemconsulting.ca>';
     $listfaq          = '<csc_user_list-faq@computersystemconsulting.ca>';
     $mail_replyto     = 'csc@computersystemconsulting.ca';
     $SITE_DISPLAY_NAME       = $SetupVariablesCSC->{-SITE_DISPLAY_NAME};
%VALID_FORUMS = (
       support_installation  =>  'Installation support',
       support_extropia     =>  'Extropia support',
       support_linux_       => 'Linux support',
       support_webdb        =>  'WebDB support',
       support_perl         =>  'Perl support',
       csc_helpdesk          =>  'HelpDesk',
                                );

    $PAGE_LIST_VIEW   = 'eXtropiaSubscribeListView';
    $AccountURL              = 'http://computersystemconsulting.ca/cgi-bin/Extropia/extropia.cgi?site=eXtropia' ;
    $ListTable               = 'csc_bbs_tb';
}

elsif ($SiteName eq "ECF") {
use ECFSetup;
  my $SetupVariablesECF = new  ECFSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesECF->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesECF->{-AUTH_TABLE};
    $page_top_view         = $SetupVariablesECF->{-PAGE_TOP_VIEW};
    $page_bottom_view      = $SetupVariablesECF->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesECF->{-PAGE_LEFT_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesECF->{-MAIL_FROM};
    $mail_to               = $SetupVariablesECF->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesECF->{-MAIL_REPLYTO};
    $home_view             = $SetupVariablesECF->{-HOME_VIEW};
    $homeviewname          = $SetupVariablesECF->{-HOME_VIEW_NAME};
     $CSS_VIEW_URL         = $SetupVariablesECF->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/ECF";
 #Mail settings
    $mail_from        = 'apis_bbs@forager.com';
    $mail_to          = 'apis_discussion@forager.com';
    $mail_cc          = 'Norlandbeekeepers@yahoogroups.com';
    $subscrib         = '<apis_discussion-subscribo@forager.com>';
    $unsubscrib       = '<apis_discussion-unsubscribe@forager.com>';
    $listname         = $SetupVariablesECF->{-MAIL_TO_DISCUSSION};
    $listinfo         = '<apis_discussion-info@@forager.com>';
    $listfaq          = '<apis_discussion-faq@@forager.com>';
    $mail_replyto     = 'apis_discussion@forager.com';
    $PAGE_LIST_VIEW   = 'ApisSubscribeListView';
    $salutaion        = "Eagle Creek Farms: Apis  ";
    $SITE_DISPLAY_NAME       = $SetupVariablesECF->{-SITE_DISPLAY_NAME};

%VALID_FORUMS = (
       announcements         =>  'Announcements',
       breeding              =>  'Breeding',
       diseases              =>  'Diseases and pests',
       general               =>  'General Bee keeping',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       therapies             =>  'Therapies',
       winter                =>  'Wintering',
       csc_helpdesk          =>  'HelpDesk',
                                );
    $AccountURL              = 'http://beemaster.ca/cgi-bin/Apis/apis.cgi?site=ECF' ;

    $ListTable               = 'apis_bbs_tb';
}
elsif ($SiteName eq "Brew") {

use  BrewSetup;

 my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
    $homeviewname          = 'BrewHomeView';
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
    $LINK_TARGET           = $SetupVariablesBrew->{-LINK_TARGET};
    $HTTP_HEADER_PARAMS    = $SetupVariablesBrew->{-HTTP_HEADER_PARAMS};
    $DEFAULT_CHARSET       = $SetupVariablesBrew->{-DEFAULT_CHARSET};
    $AUTH_TABLE            = $SetupVariablesBrew->{-AUTH_TABLE};
    $DEFAULT_CHARSET       = $SetupVariablesBrew->{-DEFAULT_CHARSET};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/BREW";
    $mail_from             = 'brew_bbs@shanta.org'; 
    $mail_to               = 'brew@shanta.org';
    $subscrib              = '<brew-subscribo@shanta.org>';
    $unsubscrib            = '<brew-unsubscribe@shanta.org>';
    $listinfo              = '<brew-info@@shanta.org>';
    $listfaq               = '<brew-faq@@shanta.org>';
    $mail_replyto          = 'brew@shanta.org';

%VALID_FORUMS = (
       announcements         =>  'Announcements',
       beer                  =>  'Beer',
       wine                  =>  'Wine',
       mead                  =>  'Mead  (Honey)',
       organic               =>  'Organic',
       equipment             =>  'Equipment',
       supplies              =>  'Supplies',
        csc_helpdesk          =>  'HelpDesk',
                               );

    $PAGE_LIST_VIEW   = 'ApisSubscribeListView';
    $SITE_DISPLAY_NAME       = $SetupVariablesBrew->{-SITE_DISPLAY_NAME};
    $salutaion        = "Brew Manager  ";
    $AccountURL              = 'http://shanta.org/cgi-bin/Brew/brew.cgi?site=Brew' ;
    $ListTable               = 'apis_bbs_tb';
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
 %VALID_FORUMS = (
       announcements         =>  'Announcements',
       solar                 =>  'Solar',
       hydro                 =>  'Hydro',
       wind                  =>  'Wind',
       heating               =>  'Heating',
       equipment             =>  'Equipment',
       supplies              =>  'Supplies',
        csc_helpdesk          =>  'HelpDesk',
                               );

    $PAGE_LIST_VIEW   = 'ApisSubscribeListView';
    $SITE_DISPLAY_NAME       = $SetupVariablesAltPower->{-SITE_DISPLAY_NAME};
    $salutaion        = "AltPower  ";
    $AccountURL              = 'http://shanta.org/cgi-bin/Brew/brew.cgi?site=Brew' ;
    $ListTable               = 'apis_bbs_tb';

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
    $homeviewname          = $SetupVariablesFly->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesFly->{-HOME_VIEW};
#Mail settings
    $mail_from             = $SetupVariablesFly->{-MAIL_FROM};
    $mail_to               = $SetupVariablesFly->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesFly->{-MAIL_REPLYTO};
    $HTTP_HEADER_PARAMS    = $SetupVariablesFly->{-HTTP_HEADER_PARAMS};
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/Fly";
    $HTTP_HEADER_KEYWORDS  = $SetupVariablesFly->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesFly->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_URL            = $SetupVariablesFly->{-CSS_VIEW_NAME};
    $mail_from             = 'fly_bbs@shanta.org'; 
    $mail_to               = 'fly_fishing@shanta.org';
    $subscrib              = '<fly_fishing-subscribo@shanta.org>';
    $unsubscrib            = '<fly_fishing-unsubscribe@shanta.org>';
    $listinfo              = '<fly_fishing-info@@shanta.org>';
    $listfaq               = '<fly_fishing-faq@@shanta.org>';
    $mail_replyto          = 'fly_fishing@shanta.org';
    $SITE_DISPLAY_NAME       = $SetupVariablesFly->{-SITE_DISPLAY_NAME};
%VALID_FORUMS = (
       announcements         =>  'Announcements',
       beer                  =>  'Streams',
       wine                  =>  'Lakes',
       mead                  =>  'Casting',
       organic               =>  'Tying',
       equipment             =>  'Equipment',
       supplies              =>  'Supplies',
        csc_helpdesk          =>  'HelpDesk',
                               );

    $PAGE_LIST_VIEW   = 'FlySubscribeListView';
    $AccountURL              = 'http://shanta.org/cgi-bin/Fly/fly.cgi?site=Fly' ;
    $ListTable               = 'apis_bbs_tb';
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
     $APP_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}."/CSC";
          $mail_from        = 'csc@computersystemconsulting.ca'; 
     $mail_to          = 'csc_user_list@computersystemconsulting.ca';
     $subscrib         = '<csc_user_list-subscribe@computersystemconsulting.ca>';  
     $unsubscrib      = '<csc_user_list-unsubscribe@computersystemconsulting.ca>';
     $listinfo        = '<csc_user_list-info@computersystemconsulting.ca>';
     $listfaq          = '<csc_user_list-faq@computersystemconsulting.ca>';
     $mail_replyto     = 'csc@computersystemconsulting.ca';
     $SITE_DISPLAY_NAME       = $SetupVariableseXtropia->{-SITE_DISPLAY_NAME};
%VALID_FORUMS = (
       support_installation  =>  'Installation support',
       support_extropia     =>  'Extropia support',
       support_linux_       => 'Linux support',
       support_webdb        =>  'WebDB support',
       support_perl         =>  'Perl support',
       csc_helpdesk          =>  'HelpDesk',
                                );

    $PAGE_LIST_VIEW   = 'eXtropiaSubscribeListView';
    $AccountURL              = 'http://computersystemconsulting.ca/cgi-bin/Extropia/extropia.cgi?site=eXtropia' ;
    $ListTable               = 'csc_bbs_tb';
}
elsif ($SiteName eq "Genealogy") {
use GenSetup;
  my $UseModPerl = 0;
  my $SetupVariablesGen   = new GenMarkSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGen->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGen->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGen->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGen->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGen->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGen->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGen->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGen->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGen->{-APP_LOGO_ALT};
     $homeviewname            = $SetupVariablesGen->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesGen->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesGen->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY    = $SetupVariablesGen->{-APP_DATAFILES_DIRECTORY};
     $mail_from        = 'genealogy@shanta.org'; 
     $mail_to          = 'genealogy_user_list@shanta.org';
     $subscrib         = '<gemealogy_list-subscribe@shanta.org>';  
     $unsubscrib      = '<genealogy_user_list-unsubscribe@shanta.org>';
     $listinfo        = '<genealogy_user_list-info@shanta.org>';
     $listfaq          = '<genealogy_user_list-faq@shanta.org>';
     $mail_replyto     = 'genealogy@shanta.org';
     $SITE_DISPLAY_NAME       = $SetupVariablesGen->{-SITE_DISPLAY_NAME};
%VALID_FORUMS = (
       general          => 'General',
       beck             => 'Beck Family',
       weaver           => ' Weaver family',
       fish             => 'Fish Family',
       other            =>  'Other',
       site             =>  'Application improvements and problems.',
       csc_helpdesk          =>  'HelpDesk',
                                );
    $PAGE_LIST_VIEW   = 'TelMarkSubscribeListView';
    $AccountURL              = '/cgi-bin/TelMark/telmark.cgi?site=TelMark' ;
    $ListTable               = 'csc_bbs_tb';
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
 #     $site_update            = $SetupVariablesKamasket->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesKamasket->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesKamasket->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesKamasket->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesKamasket->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesKamasket->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesKamasket->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesKamasket->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesKamasket->{-FAVICON_TYPE};
%VALID_FORUMS = (
       general          => 'General',
       beck             => 'Beck Family',
       weaver           => ' Weaver family',
       fish             => 'Fish Family',
       other            =>  'Other',
       site             =>  'Application improvements and problems.',
       csc_helpdesk          =>  'HelpDesk',
                                );
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
#      $site_update            = $SetupVariablesGrindrod->{-SITE_LAST_UPDATE};
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
 #     $site_update            = $SetupVariablesGRMarket->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablesGRMarket->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesGRMarket->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesGRMarket->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesGRMarket->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesGRMarket->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesGRMarket->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesGRMarket->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesGRMarket->{-FAVICON_TYPE};
    if ($group eq "GPMarket_admin" or
        $username eq "Shanta") {
      %VALID_FORUMS = (
        gpm_discousion  =>  'General market discusion.',
        gpm_Committe    =>  'Market committee',
        gpm_customer    =>  'Cutomer forum',
        gpm_vendor      =>  'Vender forum',
        site            =>  'Application improvements and problems.',
        csc_helpdesk    =>  'HelpDesk',
         );
      $listname      = $SetupVariablesGRMarket->{-MAIL_TO_COMMITTEE};              } else {

       %VALID_FORUMS = (
       gpm_discousion  =>  'General market discusion.',
       gpm_customer    =>  'Cutomer forum',
       gpm_vendor      =>  'Vender forum',
       site            =>  'Application improvements and problems.',
       csc_helpdesk    =>  'HelpDesk',
                                );
      $listname = $SetupVariablesGRMarket->{-MAIL_TO_COMMITTEE}; 

    }
     $APP_DATAFILES_DIRECTORY =   $GLOBAL_DATAFILES_DIRECTORY.$SetupVariablesGRMarket->{-APP_DATAFILES_DIRECTORY}; 
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
     $home_view               = $SetupVariablesSkyeFarm->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesSkyeFarm->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSkyeFarm->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSkyeFarm->{-LAST_UPDATE}; 
 #Mail settings
    $mail_from             = $SetupVariablesSkyeFarm->{-MAIL_FROM};
    $mail_to               = $SetupVariablesSkyeFarm->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesSkyeFarm->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME     = $SetupVariablesSkyeFarm->{-SITE_DISPLAY_NAME};
   $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/SkyeFarm';
        %VALID_FORUMS = (
       Skye_discousion  =>  'General Garlic and farm discusion.',
       Skye_customer    =>  'Cutomer forum',
       Skye_vendor      =>  'Vender forum',
       Skye_farmer      =>  'Farmer forum',
       site             =>  'Application improvements and problems.',
       csc_helpdesk     =>  'HelpDesk',
                                );
 }

elsif ($SiteName eq "WB" or
       $SiteName eq "WBDev" ) {
use WBSetup;
  my $UseModPerl = 0;
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
 #Mail settings
    $mail_from                = $SetupVariablesWB->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesWB->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesWB->{-MAIL_REPLYTO};
    $SITE_DISPLAY_NAME        = $SetupVariablesWB->{-SITE_DISPLAY_NAME};
    $FAVICON                  = $SetupVariablesWB->{-FAVICON}||'/images/apis/favicon.ico';
    $ANI_FAVICON              = $SetupVariablesWB->{-ANI_FAVICON};
    $page_top_view            = $SetupVariablesWB->{-PAGE_TOP_VIEW};
  %VALID_FORUMS           = 
                               (
       announcements         =>  'Public Announcements',
       wbanouncements        =>  'WeaverBeck Announcements',
       becks                 =>  'The Becks',
       geneology             =>  'Geneology',
       weavers               =>  'The Weavers',
       csc_helpdesk          =>  'HelpDesk',
                                ); 
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
     $APP_DATAFILES_DIRECTORY    = $SetupVariablesTelMark->{-APP_DATAFILES_DIRECTORY};
     $mail_from        = 'telmark@shanta.org'; 
     $mail_to          = '<telmark_discussion@shanta.org>';  
     $unsubscrib      = '<telmarkcsc_discussion-unsubscribe@shanta.org>';
     $listinfo        = '<telmark_discussion-info@shanta.org>';
     $listfaq          = '<telmark_discussion-faq@shanta.org>';
     $mail_replyto     = '<telmark_discussion@shanta.org>';
     $SITE_DISPLAY_NAME       = $SetupVariablesTelMark->{-SITE_DISPLAY_NAME};
%VALID_FORUMS = (
       equipment            =>  'Equipment',
       Technique              =>  'How to ski',
       snowtrac             =>  'Snow-trac/Snow-Master',
      winter_camping       => 'Winter camping and survival',
       avalanche             =>  'Avalanche safety',
       other                =>  'Other',
       csc_helpdesk          =>  'HelpDesk',
                                );
    $PAGE_LIST_VIEW   = 'TelMarkSubscribeListView';
    $AccountURL              = '/cgi-bin/TelMark/telmark.cgi?site=TelMark' ;
    $ListTable               = 'csc_bbs_tb';
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

".$SITE_DISPLAY_NAME ." respects your privacy. We do not sell our mailing list information nor do we release your information to anyone, except as required by law.

Thanks,"
.$salutaion;
    $auth = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';

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
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||'$mail_from',
    -TO      =>  '$mail_to',
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => $SESSION ->getAttribute(-KEY => 'auth_email')||'$mail_from',
    -TO      =>  $SetupVariables->{-MAIL_TO_ADMIN}||'$mail_to',
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
        'forum'     => 'Forum',
        'email'     => 'Email',
        'name'      => 'Full Name',
        'subject'   => 'Subject',
        'body'      => 'Message',
        'thread_id' => 'Thread ID',
        'parent_id' => 'Parent ID',
        'date_time_posted'  => 'Date',
    },

    -RULES => [
    #    -ESCAPE_HTML_TAGS => [
    #        -FIELDS => [qw(
    #            *
    #        )]
    #    ],

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
                name
                subject
                body
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
        'name'     => 'Full Name',
        'subject'  => 'Subject',
        'body'     => 'Message',

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
                name
                subject
                body
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

my @DATASOURCE_FIELD_NAMES = 
    qw(
       record_id
       forum
       parent_id
       thread_id
       magic

       email
       name
       subject
       body

       username_of_poster
       group_of_poster
       date_time_posted
);

my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     name    => [
                 -DISPLAY_NAME => 'Full Name',
                 -TYPE         => 'textfield',
                 -NAME         => 'name',
                 -SIZE         => 30,
                 -MAXLENGTH    => 80,
                ],

     email    => [
                 -DISPLAY_NAME => 'Email',
                 -TYPE         => 'textfield',
                 -NAME         => 'email',
                 -SIZE         => 30,
                 -MAXLENGTH    => 80,
                ],

     subject => [
                 -DISPLAY_NAME => 'Subject',
                 -TYPE         => 'textfield',
                 -NAME         => 'subject',
                 -SIZE         => 74,
                 -MAXLENGTH    => 200,
                ],

     body    => [
                 -DISPLAY_NAME => 'Message',
                 -TYPE         => 'textarea',
                 -NAME         => 'body',
                 -ROWS         => 8,
                 -COLS         => 72,
                 -WRAP         => 'VIRTUAL'
                ],

);

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = (
       qw(name email),
       qw(subject body),
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
	        -TABLE        => $ListTable,
	        -USERNAME     =>  $AUTH_MSQL_USER_NAME,
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
        forum
        subject
        body
);
my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $mail_to,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);
    

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION->getAttribute(-KEY => 'auth_email')||$mail_from,
    -TO       => $listname || $mail_to,
    -CC       => $mail_cc,
    -REPLY_TO => $mail_replyto,
    -SUBJECT  => $APP_NAME_TITLE."  Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => $SESSION->getAttribute(-KEY => 'auth_email')||$mail_from,
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
    ApisCSSView
    BCHPACSSView
    ENCYCSSView
    CSPSCSSView
    CSCCSSView
    VitalVicCSSView
    ENCYCSSView
    OrganicCSSView
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
    SelectForumView
    PrivacyView
    GrowersView
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
        forum
        name
        email
        subject
        body
        date_time_posted
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
        'name'     => 'Full Name',
        'email'  => 'Email',
        'subject'  => 'Subject',
        'body'     => 'Message',
        'date_time_posted' => 'Date',
        },
    -VALID_FORUMS            => \%VALID_FORUMS,
    -HOME_VIEW               => 'BasicDataView',
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SITE_NAME               => $SiteName,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
        name
        email
        subject
        date_time_posted
        )],
    -SORT_FIELDS             => [qw(
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

my @ACTION_HANDLER_LIST = qw(
    Default::SetSessionData
    Default::DisplayCSSViewAction
    Default::ProcessConfigurationAction
    Default::CheckForLogicalConfigurationErrorsAction
    BBS::DisplayViewAllRecordsAction
    BBS::DisplayDetailsRecordViewAction
    Default::DisplaySessionTimeoutErrorAction
    Default::PerformLogonAction
    Default::PerformLogoffAction
    Default::DisplayOptionsFormAction
    Default::DownloadFileAction
    BBS::DisplayAddFormAction
    Default::DisplayAddRecordConfirmationAction
    BBS::ProcessAddRequestAction
    Default::DisplayDeleteFormAction
    Default::DisplayDeleteRecordConfirmationAction
    Default::ProcessDeleteRequestAction
    Default::DisplayModifyFormAction
    Default::DisplayModifyRecordConfirmationAction
    Default::ProcessModifyRequestAction
    Default::DisplayPowerSearchFormAction
    Default::DisplaySimpleSearchResultsAction
    Default::PerformPowerSearchAction
    Default::HandleSearchByUserAction
    BBS::DisplaySelectForumAction
);
#    Default::DisplayBasicDataViewAction

my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'BBCAddEventEmailView',
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
    -SCRIPT_NAME2                           => $CGI->script_name(),
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -Debug                                  => $CGI->param('debug')||0,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -DOCUMENT_ROOT_URL2       => 'shanta.org',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 100,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || '',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || '',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'DESC',
    -SORT_DIRECTION                         => 'ASC',
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
    -KEY_FIELD                              => 'record_id',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MESSAGE_FOOTER                         => $footer,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -LAST_UPDATE                            => $last_update,
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
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 0,
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
    -PAGE_TOP_VIEW                          => $page_top_view ,
    -PAGE_LEFT_VIEW                         => $page_left_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -SELECT_FORUM_VIEW	                    => 'SelectForumView',
    -LIST_NAME                              => $listname,
    -PAGE_LIST_VIEW	                       => $PAGE_LIST_VIEW
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