package ULCSetup;




use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Varible for use here only
# $site = 'file';

my $site = 'MySQL';
my $datesourcetype = 'file';



sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME => 'HomeView',
 	    -AFFILIATE           => '13',
	    -PID                 => '120',
       -AUTH_TABLE          => 'ulc_user_auth_tb',
       -LAST_UPDATE         => 'October 02, 2021',
       -SITE_LAST_UPDATE    => 'October 02, 202',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -HOME_VIEW           => 'HomeView',
	    -BASIC_DATA_VIEW     => 'HomeView',
	    -APP_LOGO            => '/images/ency/encyicon.gif',
	    -APP_LOGO_ALT        => 'ULC Logo',
	    -APP_LOGO_WIDTH      => '130',
	    -APP_LOGO_HEIGHT     => '120',
	    -CSS_VIEW_NAME       => '/styles/ulcstyle.css',
	    -PAGE_TOP_VIEW       => 'PageTopView',
	    -PAGE_BOTTOM_VIEW    => 'PageBottomView',
	    -PAGE_LEFT_VIEW      => 'LeftPageView',
	    -LEFT_PAGE_VIEW      => 'LeftPageView',
	    -MAIL_FROM           => 'admin@usbm.ca',
	    -MAIL_TO             => 'admin@usbm.ca',
	    -MAIL_TO_DISCUSSION  => 'ency@usbm.ca',
	    -MAIL_TO_ADMIN       => 'webmaster@usbm.ca',
	    -MAIL_TO_USER        => 'usbm_user_list@usbm.ca',
	    -MAIL_TO_CLIENT      => 'usbm_client@usbm.ca',
	    -MAIL_REPLYTO        => 'admin@usbm.ca',
	    -SITE_DISPLAY_NAME   => 'Universal Life Church.',
	    -DOCUMENT_ROOT_URL   => '/',
       -LINK_TARGET         => '_self',
       -HTTP_HEADER_PARAMS  => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL      => '/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "/home/usbm/Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "/home/usbm/Datafiles/Todo",
	    -DATASOURCE_TYPE     => $site,
       -CAL_TABLE           => 'cal_event',
       -HTTP_HEADER_DESCRIPTION => "Universal Life Church",
       -HTTP_HEADER_KEYWORDS    => "spirtuality",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;

