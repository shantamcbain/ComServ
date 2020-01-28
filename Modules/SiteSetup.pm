package SiteSetup;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
#This is the only main difference between domain configuration.All this should move to mysql
my $HostName ;
# $datasourcetype = 'file';
#my $datesourcetype = 'file';
my $CGI = new CGI()
  or die(
     "Unable to construct the CGI object" . ". Please contact the webmaster." );

foreach ( $CGI->param() )
{
 $CGI->param( $1, $CGI->param($_), $HostName ) if (/(.*)\.x$/);
}

if ($HostName eq "computersystemconsulting.ca") {
my $GLOBAL_DATAFILES_DIRECTORY="/home/shanta/Datafiles";
};
#my $GLOBAL_DATAFILES_DIRECTORY="/home/usbmca/Datafiles";
#my $GLOBAL_DATAFILES_DIRECTORY="/home/weaver/Datafiles";
#my $GLOBAL_DATAFILES_DIRECTORY="/home/wisewoma/Datafiles";
# $site = 'file';
#Create local Variable for use here only

my $datesourcetype = 'MySQL';
my $Affiliate;
my $home_view;
my $MySQLPW;
my $AUTH_MSQL_USER_NAME;
my $AUTH_TABLE; 
my $SITE_DISPLAY_NAME;
my $AUTH_TABLE;
my $APP_NAME_TITLE;
my $BASIC_DATA_VIEW;
my $site_update;
my $last_update;
my $SiteLastUpdate;
my $HasMembers;
my $HTTP_HEADER_KEYWORDS;
my $HTTP_HEADER_PARAMS;
my $HTTP_HEADER_DESCRIPTION;
my $page_top_view;
my $page_bottom_view;
my $page_left_view;
my $app_logo;
my $app_logo_height;
my $app_logo_width;
my $app_logo_alt;
my $FAVICON;
my $ANI_FAVICON;
my $FAVICON_TYPE;
my $mail_from;
my $mail_to;
my $mail_replyto;
my $mail_to_auth;
my $mail_to_user;
my $mail_to_member;
my $mail_to_discussion;
my $APP_DATAFILES_DIRECTORY;

my $CSS_VIEW_NAME;
my $CSS_VIEW_URL;
my $StoreUrl;
my $shop;
my $UseModPerl;
my $NEWS_TB;
my $IMAGE_ROOT_URL;
my $DOCUMENT_ROOT_URL;
my @SESSION_CONFIG_PARAMS = (
                         -TYPE            => 'File',
                         -MAX_MODIFY_TIME => 60 * 60 * 60,
                         -SESSION_DIR => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
                         -FATAL_TIMEOUT           => 0,
                         -FATAL_SESSION_NOT_FOUND => 1
);
my @SESSION_MANAGER_CONFIG_PARAMS = (
                                      -TYPE           => 'FormVar',
                                      -CGI_OBJECT     => $CGI,
                                      -SESSION_PARAMS => \@SESSION_CONFIG_PARAMS
);my $SESSION_MGR =
  Extropia::Core::SessionManager->create( @SESSION_MANAGER_CONFIG_PARAMS );
my $SESSION    = $SESSION_MGR->createSession();

my $group    = $SESSION->getAttribute( -KEY => 'auth_group' );


my $SiteName =  $CGI->param('site')||'CSC';

 if ($SiteName eq "AltPower") {
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
     $APP_NAME_TITLE          = $SetupVariablesAltPower->{-APP_NAME_TITLE};
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
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY."/AltPower";
 
}

if ($SiteName eq "BMaster") {
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
     $APP_NAME_TITLE          = $SetupVariablesBMaster->{-APP_NAME_TITLE};
     $CSS_VIEW_URL            = $SetupVariablesBMaster->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesBMaster->{-LAST_UPDATE}; 
#      $site_update              = $SetupVariablesBMaster->{-SITE_LAST_UPDATE};
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
if ($SiteName eq "BMastBreeder") {
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
     $APP_NAME_TITLE          = $SetupVariablesBMaster->{-APP_NAME_TITLE};
 #    $home_view            = 'HomeView'||$SetupVariablesBMaster->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesBMaster->{-HOME_VIEW};
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
if ($SiteName eq "Brew") {

use  BrewSetup;
  my $SetupVariablesBrew  = new BrewSetup($UseModPerl);
#    $home_view          = $SetupVariablesBrew->{-HOME_VIEW_NAME};
    $home_view             = $SetupVariablesBrew->{-HOME_VIEW}; 
    $BASIC_DATA_VIEW       = $SetupVariablesBrew->{-BASIC_DATA_VIEW};
    $page_bottom_view      = $SetupVariablesBrew->{-PAGE_BOTTOM_VIEW};
    $page_left_view        = $SetupVariablesBrew->{-LEFT_PAGE_VIEW};
#Mail settings
    $CSS_VIEW_NAME         = $SetupVariablesBrew->{-CSS_VIEW_NAME};
    $mail_from             = $SetupVariablesBrew->{-MAIL_FROM}; 
    $mail_to               = $SetupVariablesBrew->{-MAIL_TO};
    $mail_replyto          = $SetupVariablesBrew->{-MAIL_REPLYTO};
    $CSS_VIEW_URL          = $SetupVariablesBrew->{-CSS_VIEW_NAME}||'blank';
    $app_logo              = $SetupVariablesBrew->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesBrew->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesBrew->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesBrew->{-APP_LOGO_ALT};
    $APP_NAME_TITLE         = $SetupVariablesBrew->{-APP_NAME_TITLE};
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
if($SiteName eq "CS" or
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
  $mail_from               = $SetupVariablesCS->{-MAIL_FROM};
  $mail_to                 = $SetupVariablesCS->{-MAIL_TO};
  $mail_replyto            = $SetupVariablesCS->{-MAIL_REPLYTO};
  $SITE_DISPLAY_NAME        = $SetupVariablesCS->{-SITE_DISPLAY_NAME};
  $site_update              = $SetupVariablesCS->{-SITE_LAST_UPDATE};
  $last_update              = $SetupVariablesCS->{-LAST_UPDATE}; 
  $app_logo                 = $SetupVariablesCS->{-APP_LOGO};
  $shop                     = $SetupVariablesCS->{-SHOP};
  $app_logo_height          = $SetupVariablesCS->{-APP_LOGO_HEIGHT};
  $app_logo_width           = $SetupVariablesCS->{-APP_LOGO_WIDTH};
  $app_logo_alt             = $SetupVariablesCS->{-APP_LOGO_ALT};
    $APP_NAME_TITLE         = $SetupVariablesCS->{-APP_NAME_TITLE};
  $FAVICON                  = $SetupVariablesCS>{-FAVICON};
  $ANI_FAVICON              = $SetupVariablesCS->{-ANI_FAVICON};
  $FAVICON_TYPE             = $SetupVariablesCS->{-FAVICON_TYPE};
  $CSS_VIEW_URL             = $SetupVariablesCS->{-CSS_VIEW_NAME};
#    $left_page_view = 'CSCLeftPageView';
}
if ( $SiteName eq "CSCDev" )
 {
  -SITE_NAME => $SiteName;
 }
if ($SiteName eq "CSC" or
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
    $mail_from               = $SetupVariablesCSC->{-MAIL_FROM};
    $mail_to                 = $SetupVariablesCSC->{-MAIL_TO};
    $mail_replyto            = $SetupVariablesCSC->{-MAIL_REPLYTO};
    $StoreUrl                = $SetupVariablesCSC->{-STORE_URL};
    $site_update             = $SetupVariablesCSC->{-SITE_LAST_UPDATE};
    $last_update             = $SetupVariablesCSC->{-LAST_UPDATE}; 
    $HasMembers              = $SetupVariablesCSC->{-HAS_MEMBERS};
    my $HTTP_HEADER_KEYWORDS = $SetupVariablesCSC->{-HTTP_HEADER_KEYWORDS};
    $HTTP_HEADER_PARAMS      = $SetupVariablesCSC->{-HTTP_HEADER_PARAMS};
    $HTTP_HEADER_DESCRIPTION = $SetupVariablesCSC->{-HTTP_HEADER_DESCRIPTION};
    $CSS_VIEW_NAME           = $SetupVariablesCSC->{-CSS_VIEW_NAME};
#    $home_view               = $SetupVariablesCSC->{-HOME_VIEW};
    $page_top_view           = $SetupVariablesCSC->{-PAGE_TOP_VIEW};
    $page_bottom_view        = $SetupVariablesCSC->{-PAGE_BOTTOM_VIEW};
    $page_left_view          = $SetupVariablesCSC->{-LEFT_PAGE_VIEW};
    $CSS_VIEW_URL            = $SetupVariablesCSC->{-CSS_VIEW_NAME};
    $APP_NAME_TITLE          = $SetupVariablesCSC->{-APP_NAME_TITLE};
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
    $mail_from                = $SetupVariablesDemo->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesDemo->{-MAIL_TO};
    $mail_replyto             = $SetupVariablesDemo->{-MAIL_REPLYTO};
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
    $APP_NAME_TITLE           = $SetupVariablesDemo->{-APP_NAME_TITLE};
    $CSS_VIEW_URL             = $SetupVariablesDemo->{-CSS_VIEW_NAME};
    $SITE_DISPLAY_NAME        = $SetupVariablesDemo->{-SITE_DISPLAY_NAME};
#    $home_view             = $SetupVariablesDemo->{-HOME_VIEW_NAME};
    $last_update              = $SetupVariablesDemo->{-SITE_LAST_UPDATE};
    $FAVICON                  = $SetupVariablesDemo->{-FAVICON};
    $ANI_FAVICON              = $SetupVariablesDemo->{-ANI_FAVICON};
    $FAVICON_TYPE             = $SetupVariablesDemo->{-FAVICON_TYPE};

}
if ($SiteName eq "ECF" ||
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
    $APP_NAME_TITLE          = $SetupVariablesECF->{-APP_NAME_TITLE};
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
if ($SiteName eq "ENCY") {
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
    $APP_NAME_TITLE          = $SetupVariablesENCY->{-APP_NAME_TITLE};
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
if ($SiteName eq "FeedBees") {
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
    $APP_NAME_TITLE          = $SetupVariablesFeedBees->{-APP_NAME_TITLE};
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
    $APP_NAME_TITLE          = $SetupVariablesForager->{-APP_NAME_TITLE};
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

if ($SiteName eq "GrindrodBC") {
use GrindrodSetup;
  my $SetupVariablesGrindrod   = new GrindrodSetup($UseModPerl);
     $home_view               = $SetupVariablesGrindrod->{-HOME_VIEW};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesGrindrod->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesGrindrod->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesGrindrod->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesGrindrod->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablesGrindrod->{-AUTH_TABLE};
     $app_logo                = $SetupVariablesGrindrod->{-APP_LOGO};
     $app_logo_height         = $SetupVariablesGrindrod->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablesGrindrod->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablesGrindrod->{-APP_LOGO_ALT};
     $APP_NAME_TITLE          = $SetupVariablesGrindrod->{-APP_NAME_TITLE};
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
    $APP_NAME_TITLE           = $SetupVariablesGRProject->{-APP_NAME_TITLE};
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
if ($SiteName eq "HE" or
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
     $APP_NAME_TITLE          = $SetupVariablesHE->{-APP_NAME_TITLE};
#    $home_view             = $SetupVariablesHE->{-HOME_VIEW_NAME};
 #    $home_view                = $SetupVariablesHE->{-HOME_VIEW};
     $CSS_VIEW_URL             = $SetupVariablesHE->{-CSS_VIEW_NAME};
     $last_update              = $SetupVariablesHE->{-LAST_UPDATE}; 
     $site_update              = $SetupVariablesHE->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from                = $SetupVariablesHE->{-MAIL_FROM};
     $mail_to                  = $SetupVariablesHE->{-MAIL_TO};
     $mail_replyto             =home_view $SetupVariablesHE->{-MAIL_REPLYTO};
     $shop                     = $SetupVariablesHE->{-SHOP};
     $SITE_DISPLAY_NAME        = $SetupVariablesHE->{-SITE_DISPLAY_NAME};
}

if ($SiteName eq "HoneyDo" or
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
     $APP_NAME_TITLE          = $SetupVariablesHoneyDo->{-APP_NAME_TITLE};
#    $home_view            = $SetupVariablesHoneyDo->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesHoneyDo->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesHoneyDo->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesHoneyDo->{-LAST_UPDATE}; 
     $site_update             = home_view$SetupVariablesHoneyDo->{-SITE_LAST_UPDATE};
 #Mail settings
     $mail_from               = $SetupVariablesHoneyDo->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesHoneyDo->{-MAIL_TO};
     $SITE_DISPLAY_NAME       = $SetupVariablesHoneyDo->{-SITE_DISPLAY_NAME};
     $mail_replyto            = $SetupVariablesHoneyDo->{-MAIL_REPLYTO};
 }

if (
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
    $APP_NAME_TITLE          = $SetupVariablesJennaBee->{-APP_NAME_TITLE};
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
 }if ($SiteName eq "LandTrust"){
use LTrustSetup;
  my $UseModPerl = 1;
  my $SetupVariablesLandTrust   = new LTrustSetup($UseModPerl);
    $CSS_VIEW_NAME           = $SetupVariablesLandTrust->{-CSS_VIEW_NAME};
    $AUTH_TABLE              = $SetupVariablesLandTrust->{-AUTH_TABLE};
    $app_logo                = $SetupVariablesLandTrust->{-APP_LOGO};
    $app_logo_height         = $SetupVariablesLandTrust->{-APP_LOGO_HEIGHT};
    $app_logo_width          = $SetupVariablesLandTrust->{-APP_LOGO_WIDTH};
    $app_logo_alt            = $SetupVariablesLandTrust->{-APP_LOGO_ALT};
    $APP_NAME_TITLE          = $SetupVariablesLandTrust->{-APP_NAME_TITLE};
#    $home_view          = $SetupVariablesLandTrust->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesLandTrust->{-HOME_VIEW}; 
    $CSS_VIEW_URL            = $SetupVariablesLandTrust->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/LandTrust';
    $SiteLastUpdate          = $SetupVariablesLandTrust->{-Site_Last_Update}; 
    $SITE_DISPLAY_NAME       = $SetupVariablesLandTrust->{-SITE_DISPLAY_NAME};
    $NEWS_TB                 = $SetupVariablesLandTrust->{-NEWS_TB};
  }
if ($SiteName eq "LumbyThrift") {
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
    $APP_NAME_TITLE          = $SetupVariablesLumbyThrift->{-APP_NAME_TITLE};
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
if ($SiteName eq "MW" or
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
    $APP_NAME_TITLE          = $SetupVariablesMW->{-APP_NAME_TITLE};
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
if ($SiteName eq "Organic") {
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
    $APP_NAME_TITLE          = $SetupVariablesOrganic->{-APP_NAME_TITLE};
 #    $home_view            = $SetupVariablesOrganic->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesOrganic->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesOrganic->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesOrganic->{-SITE_DISPLAY_NAME};
     $site_update             = $SetupVariablesOrganic-> {-SITE_LAST_UPDATE};
 }
 if ($SiteName eq "pihive") {
use pihiveSetup;
 my $SetupVariablespihive  = new pihiveSetup($UseModPerl);
     $HasMembers               = $SetupVariablespihive->{-HAS_MEMBERS};
     $HTTP_HEADER_KEYWORDS    = $SetupVariablespihive->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablespihive->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablespihive->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablespihive->{-CSS_VIEW_NAME};
     $AUTH_TABLE              = $SetupVariablespihive->{-AUTH_TABLE};
     $app_logo                = $SetupVariablespihive->{-APP_LOGO};
     $app_logo_height         = $SetupVariablespihive->{-APP_LOGO_HEIGHT};
     $app_logo_width          = $SetupVariablespihive->{-APP_LOGO_WIDTH};
     $app_logo_alt            = $SetupVariablespihive->{-APP_LOGO_ALT};
     $CSS_VIEW_URL            = $SetupVariablespihive->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablespihive->{-LAST_UPDATE}; 
#      $site_update              = $SetupVariablespihive->{-SITE_LAST_UPDATE};
#Mail settings
     $mail_from               = $SetupVariablespihive->{-MAIL_FROM};
     $mail_to                 = $SetupVariablespihive->{-MAIL_TO};
     $mail_replyto            = $SetupVariablespihive->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablespihive->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablespihive->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablespihive->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablespihive->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablespihive->{-FAVICON_TYPE};
}
 
 
if ($SiteName eq "SSeedSavers" or
       $SiteName eq "SSeedSaversDev" 
       ) {use SSeedSaversSetup;
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
     $APP_NAME_TITLE          = $SetupVariablesSSeedSavers->{-APP_NAME_TITLE};
     $home_view               = $SetupVariablesSSeedSavers->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSSeedSavers->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesSSeedSavers->{-LAST_UPDATE};   
     $site_update             = $SetupVariablesSSeedSavers->{-SITE_LAST_UPDATE};
#Mail settings
    $mail_from                = $SetupVariablesSSeedSavers->{-MAIL_FROM};
    $mail_to                  = $SetupVariablesSSeedSavers->{-MAIL_TO};
     $mail_replyto             = $SetupVariablesSSeedSavers->{-MAIL_REPLYTO};
	  $mail_to_user             = $SetupVariablesSSeedSavers->{-MAIL_TO_USER};
	  $mail_to_member           = $SetupVariablesSSeedSavers->{-MAIL_TO_Member};
	  $mail_to_discussion       = $SetupVariablesSSeedSavers->{-MAIL_TO_DISCUSSION};
 }
if ($SiteName eq "Sky") {
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
     $APP_NAME_TITLE          = $SetupVariablesSky->{-APP_NAME_TITLE};
#    $home_view            = $SetupVariablesSky->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesSky->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesSky->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesSky->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesSky->{-LAST_UPDATE};
     $site_update             = $SetupVariablesSky->{-SITE_LAST_UPDATE};
 }if ($SiteName eq "Shanta"){
use ShantaSetup;
  my $UseModPerl = 1;
  my $SetupVariablesShanta   = new ShantaSetup($UseModPerl);
    $CSS_VIEW_NAME         = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $AUTH_TABLE            = $SetupVariablesShanta->{-AUTH_TABLE};
    $app_logo              = $SetupVariablesShanta->{-APP_LOGO};
    $app_logo_height       = $SetupVariablesShanta->{-APP_LOGO_HEIGHT};
    $app_logo_width        = $SetupVariablesShanta->{-APP_LOGO_WIDTH};
    $app_logo_alt          = $SetupVariablesShanta->{-APP_LOGO_ALT};
    $APP_NAME_TITLE          = $SetupVariablesShanta->{-APP_NAME_TITLE};
#    $home_view          = $SetupVariablesShanta->{-HOME_VIEW_NAME};
#    $home_view             = $SetupVariablesShanta->{-HOME_VIEW}; 
    $CSS_VIEW_URL          = $SetupVariablesShanta->{-CSS_VIEW_NAME};
    $APP_DATAFILES_DIRECTORY= $GLOBAL_DATAFILES_DIRECTORY.'/Shanta';
    $SiteLastUpdate        = $SetupVariablesShanta->{-Site_Last_Update}; 
    $SITE_DISPLAY_NAME     = $SetupVariablesShanta->{-SITE_DISPLAY_NAME};
  }
  
if ($SiteName eq "ShantaWorkShop"){
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
     $APP_NAME_TITLE          = $SetupVariablesShantaWorkShop->{-APP_NAME_TITLE};
    $CSS_VIEW_URL            = $SetupVariablesShantaWorkShop->{-CSS_VIEW_NAME};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY.'/ShantasWorkShop';
     $site_update             = $SetupVariablesShantaWorkShop>{-Site_Last_Update};
     $SiteLastUpdate          = $SetupVariablesShantaWorkShop->{-Site_Last_Update}; 
     $SITE_DISPLAY_NAME       = $SetupVariablesShantaWorkShop->{-SITE_DISPLAY_NAME};
  }
  if ($SiteName eq "Sustainable" or
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
    $APP_NAME_TITLE          = $SetupVariablesSustainable->{-APP_NAME_TITLE};
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
 if ($SiteName eq "USBM") {
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
     $APP_NAME_TITLE          = $SetupVariablesUSBM->{-APP_NAME_TITLE};
#    $home_view            = $SetupVariablesUSBM->{-HOME_VIEW_NAME};
 #    $home_view               = $SetupVariablesUSBM->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesUSBM->{-CSS_VIEW_NAME};
     $SITE_DISPLAY_NAME       = $SetupVariablesUSBM->{-SITE_DISPLAY_NAME};
     $last_update             = $SetupVariablesUSBM->{-LAST_UPDATE};
     $site_update             = $SetupVariablesUSBM->{-SITE_LAST_UPDATE};
     $APP_DATAFILES_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY."/usbmca";
 }
if ($SiteName eq "WB" or
       $SiteName eq "WBDev" ) {
use WBSetup;
  my $SetupVariablesWB   = new WBSetup($UseModPerl);
     $HTTP_HEADER_KEYWORDS    = $SetupVariablesWB->{-HTTP_HEADER_KEYWORDS};
     $HTTP_HEADER_PARAMS      = $SetupVariablesWB->{-HTTP_HEADER_PARAMS};
     $HTTP_HEADER_DESCRIPTION = $SetupVariablesWB->{-HTTP_HEADER_DESCRIPTION};
     $CSS_VIEW_NAME           = $SetupVariablesWB->{-CSS_VIEW_NAME};
     $APP_NAME_TITLE          = $SetupVariablesWB->{-APP_NAME_TITLE};
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
if ($SiteName eq "WiseWoman") {
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
    $APP_NAME_TITLE          = $SetupVariablesWiseWoman->{-APP_NAME_TITLE};
    $home_view               = $SetupVariablesWiseWoman->{-HOME_VIEW_NAME};
     $home_view               = $SetupVariablesWiseWoman->{-HOME_VIEW};
     $CSS_VIEW_URL            = $SetupVariablesWiseWoman->{-CSS_VIEW_NAME};
     $last_update             = $SetupVariablesWiseWoman->{-LAST_UPDATE}; 
      $site_update            = $SetupVariablesWiseWoman->{-SITE_LAST_UPDATE};
#Mail settings= $ENV{'SERVER_NAME'}
     $mail_from               = $SetupVariablesWiseWoman->{-MAIL_FROM};
     $mail_to                 = $SetupVariablesWiseWoman->{-MAIL_TO};
     $mail_replyto            = $SetupVariablesWiseWoman->{-MAIL_REPLYTO};
     $SITE_DISPLAY_NAME       = $SetupVariablesWiseWoman->{-SITE_DISPLAY_NAME};
     $FAVICON                 = $SetupVariablesWiseWoman->{-FAVICON};
     $ANI_FAVICON             = $SetupVariablesWiseWoman->{-ANI_FAVICON};
     $page_top_view           = $SetupVariablesWiseWoman->{-PAGE_TOP_VIEW};
     $FAVICON_TYPE            = $SetupVariablesWiseWoman->{-FAVICON_TYPE};
     $GLOBAL_DATAFILES_DIRECTORY  = $SetupVariablesWiseWoman->{-GLOBAL_DATAFILES_DIRECTORY};
} 

sub new
{
 my $package    = shift;
 my $UseModPerl = shift || 1;
 my $SiteName   = shift;
  # This is where you define your variable mapping.
 my $self = {
  -SITE_NAME => $SiteName || 'CSCDev',
  -AFFILIATE => $Affiliate||'006',
  -HOME_VIEW_NAME     => $home_view||'PageView',
  -HOME_VIEW          => $home_view||'PageView',
  -SITE_DISPLAY_NAME  => $SITE_DISPLAY_NAME,
  -LAST_UPDATE        => $last_update,
  -Site_Last_Update   => $SiteLastUpdate,
  -LOCAL_IP           => '50.116.78.32',
  -BASIC_DATA_VIEW    => $BASIC_DATA_VIEW||'BasicDataView',
  -APP_LOGO           => $app_logo||'../csc/cscsmall.gif',
  -APP_LOGO_ALT       => $app_logo_alt||'CSC Logo',
  -APP_LOGO_WIDTH     => $app_logo_width||'108',
  -APP_LOGO_HEIGHT    => $app_logo_height||'40',
  -APP_NAME_TITLE     => $APP_NAME_TITLE || 'ComServ',
  -FAVICON            => $FAVICON||'/favicon.ico',
  -ANI_FAVICON        => $ANI_FAVICON||'/animated_favicon.gif',
  -FAVICON_TYPE       => $FAVICON_TYPE||'/image/x-icon',
  -CSS_VIEW_NAME      => $CSS_VIEW_NAME||'/styles/CSSView.css',
  -CSS_VIEW_URL       => $CSS_VIEW_URL,
  -HAS_MEMBERS        => $HasMembers,
  -PAGE_TOP_VIEW      => $page_top_view||'PageTopView',
  -PAGE_BOTTOM_VIEW   => $page_bottom_view||'PageBottomView',
  -PAGE_LEFT_VIEW     => $page_left_view||'LeftPageView',
  -MAIL_TO_ADMIN      => 'webmaster@computersystemconsulting.ca',
  -MAIL_FROM          => $mail_from||'webmaster@computersystemconsulting.ca',
  -MAIL_TO_AUTH       => $mail_to_auth||'csc@computersystemconsuting.ca',
  -MAIL_TO            => $mail_to||'webmaster@computersystemconsulting.ca',
  -MAIL_FROM_HELPDESK => 'helpdesk@computersystemconsulting.ca',
  -MAIL_REPLYTO       => $mail_replyto||'webmaster@computersystemconsulting.ca',
  -MAIL_TO_USER	      => $mail_to_user,
  -MAIL_TO_Member     => $mail_to_member,
  -MAIL_TO_DISCUSSION => $mail_to_discussion,
  -DOCUMENT_ROOT_URL  => $IMAGE_ROOT_URL||'/',
  -IMAGE_ROOT_URL     => $DOCUMENT_ROOT_URL||'/images/extropia',
  -GLOBAL_DATAFILES_DIRECTORY => $GLOBAL_DATAFILES_DIRECTORY,
  -APP_DATAFILES_DIRECTORY    => $GLOBAL_DATAFILES_DIRECTORY,
  -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
  -LINK_TARGET                => '_self',
  -HTTP_HEADER_PARAMS         => $HTTP_HEADER_PARAMS||"[-EXPIRES => '-1d']",
  -HTTP_HEADER_KEYWORDS       => $HTTP_HEADER_KEYWORDS||"eXtropia HelpDesk,eXtropia, HelpDesk,Web applications, Application hosting, hosting, support,shanta mcbain, shanta, McBain, csps, organic farming, bee keeping, beekeeping ",
  -HTTP_HEADER_DESCRIPTION    => $HTTP_HEADER_DESCRIPTION||"forager.com, computersystemconsulting.ca, webcthelpdesk.com, organicfarming.ca, shanta.org",
  -DATASOURCE_TYPE            => $datesourcetype,
  -DBI_DSN                    => 'mysql:database=shanta_forager',
  -DBI_DSN_STORES             => 'mysql:database=forager',
  -MySQLPW                    => 'UA=nPF8*m+T#',
  #-DBI_DSN                    => 'mysql:database=shanta',
  #-MySQLPW                    => 'herbsrox2,
  -PAGE_DBI                   => 'mysql:database=shanta_forager',
  -PAGE_MSQL_USER_NAME        => $AUTH_MSQL_USER_NAME||'shanta_forager',
  -PAGE_MySQLPW               => $MySQLPW||'UA=nPF8*m+T#',
  -AUTH_TABLE                 => $AUTH_TABLE||'csc_user_auth_tb',
  -AUTH_MSQL_USER_NAME        => 'shanta_forager',
  #-AUTH_MSQL_USER_NAME        => 'shanta',
  -DEFAULT_CHARSET            => 'ISO-8859-1',
  -CAL_TABLE                  => 'cal_event',
  -STORE_URL                  => $StoreUrl,
  -SHOP                       => $shop,
  -NEWS_TB                    => $NEWS_TB,
  -VALID_VIEWS => "
              ApisCSSView
              BCHPACSSView
              ECFCSSView
             OrganicCSSView
             DetailsRecordView
             BasicDataView
             InventoryBasicDataView
            AddRecordView
            AddRecordConfirmationView
            AddAcknowledgementView
            DeleteRecordConfirmationView
       DeleteAcknowledgementView
       LinkListView

       ModifyRecordView
       ModifyRecordConfirmationView
       ModifyAcknowledgementView

       PowerSearchFormView
       OptionsView
       LogoffView

       TelMarkHomeView
       ApisProductView
       ApisPolinatorsView
       MiteGoneDocsView
       ApisHoneyView
       CertifiedOrganicView
       AssociateView
       MGWaverView 
       ForumsView

       BCHPAHomeView
       BCHPAAdminHomeView
       BeeTrustView
       BCHPAByLawsView
       BCHPAContactView
       BCHPABoardView
       BCHPAMemberView
       BCHPAPolinatorsView

       ECFHomeView
       ECFSideBarHomeView
       PrintView
       AppToolsView
       ContactView
       ForageIndicatorView
       PollinatorSQLView
       InventoryHomeView
       ItemView
       InventoryProjectionView
       InventoryView
       InventorySQLView
       SQLView
        OrganicProductView
       ContactView
       InventoryProjectionView
       WeatherView
       PrivacyView
       AdventureDiaryView
       ",
 };

 #'pwxx88',

 #return your variables to the aplication file.
 return bless $self, $package;
}

1;
