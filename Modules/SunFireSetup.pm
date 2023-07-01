package SunFireSetup;

use strict;
use CGI::Carp qw(fatalsToBrowser);

#Create local Variable for use here only
# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';

#my $datesourcetype = 'file';

sub new
{
 my $package = shift;
 my $UseModPerl = shift || 1;

 # This is where you define your variable mapping.
 my $self = {
  -HOME_VIEW_NAME                 => 'HomeView',
	    -AFFILIATE           => '6',
	    -PID                 => '134',
  -SITE_LAST_UPDATE               => 'July 1, 2023',
  -HOME_VIEW                      => 'HomeView',
  -BASIC_DATA_VIEW                => 'BasicDataView',
  -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
  -APP_LOGO                       => '/images/csc/cscbig.gif',
  -APP_LOGO_ALT                   => "CSC Logo",
  -APP_LOGO_WIDTH                 => '150',
  -APP_LOGO_HEIGHT                => '60',
  -APP_NAME_TITLE                 => 'Sunfire Support Page',
  -FAVICON                        => '/images/apis/favicon.ico',
  -ANI_FAVICON                    => '/images/apis/extra/animated_favicon.gif',
  -FAVICON_TYPE                   => '/image/x-icon',
  -CSS_VIEW_NAME                  => '/styles/usbmstyle.css',
  -DEFAULT_CHARSET                => 'ISO-8859-1',
  -DOCUMENT_ROOT_URL              => '/',
  -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
  -APP_DATAFILES_DIRECTORY        => "../../Datafiles/CSC",
  -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
  -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
  -IMAGE_ROOT_URL                 => '/images/extropia',
  -LINK_TARGET                    => '_self',
  -MAIL_FROM                      => 'support@computersystemconsulting.ca',
  -MAIL_TO                        => 'csc@computersystemconsulting.ca, gillian@sunfiresystems.ca',
  -MAIL_TO_ADMIN                  => 'support@computersystemconsulting.ca',
  -MAIL_TO_USER                   => 'csc_user_list@computersystemconsulting.ca',
  -MAIL_TO_CLIENT                 => 'csc_client@computersystemconsulting.ca',
  -MAIL_REPLYTO                   => 'csc@computersystemconsulting.ca',
  -PAGE_TOP_VIEW                  => 'PageTopView',
  -PAGE_BOTTOM_VIEW               => 'PageBottomView',
  -PAGE_LEFT_VIEW                 => 'LeftPageView',
  -LEFT_PAGE_VIEW                 => 'LeftPageView',
  -SESSION_TIME_OUT               => 60 * 60 * 2,
  -SHOP                           => "csc",
  -SITE_DISPLAY_NAME              => 'SunFire Support',
  -AUTH_TABLE                     => 'csc_user_auth_tb',
  -ADMIN_AUTH_TABLE               => 'csc_admin_auth_tb',
  -HAS_MEMBERS                    => 1,
  -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
  -HTTP_HEADER_DESCRIPTION        =>
"sunfiresystems.ca Sunfire Systems • Woodstoves, gas stoves, chimney sweep, off-grid appliances, solar panels,
inverters, charge controllers, led lighting, accessories, mounts and everything else you might need to achieve energy independence. Serving Lumby, Vernon &amp; North America since 1992!",
  -HTTP_HEADER_KEYWORDS           =>
"Woodstoves, gas stoves, chimney sweep, off-grid appliances, solar panels, inverters, charge controllers, led lighting, accessories, mounts",
 };

 #return your variables to the application file.
 return bless $self, $package;
}

1;
