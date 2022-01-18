package ENCYSetup;


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
	    -PID                 => '132',
       -AUTH_TABLE          => 'ency_user_auth_tb',
       -LAST_UPDATE         => 'March 25, 2006',
       -SITE_LAST_UPDATE    => 'March 25, 2006',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -HOME_VIEW           => 'HomeView',
	    -BASIC_DATA_VIEW     => 'BasicDataView',
	    -APP_LOGO            => '/images/ency/encyicon.gif',
	    -APP_LOGO_ALT        => 'ENCY Logo',
	    -APP_LOGO_WIDTH      => '130',
	    -APP_LOGO_HEIGHT     => '120',
	    -CSS_VIEW_NAME       => '/styles/encystyle.css',
	    -PAGE_TOP_VIEW       => 'PageTopView',
	    -PAGE_BOTTOM_VIEW    => 'PageBottomView',
	    -PAGE_LEFT_VIEW      => 'LeftPageView',
	    -LEFT_PAGE_VIEW      => 'LeftPageView',
	    -MAIL_FROM           => 'encyadmin@forager.com',
	    -MAIL_TO             => 'encyadmin@forager.com',
	    -MAIL_TO_DISCUSSION  => 'ency@forager.com',
	    -MAIL_TO_ADMIN       => 'webmaster@computersystemconsulting.ca',
	    -MAIL_TO_USER        => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT      => 'csc_client@computersystemconsulting.ca',
	    -MAIL_REPLYTO        => 'encyadmin@forager.com',
	    -SITE_DISPLAY_NAME   => 'Encyclopedia of Biological Life.',
	    -DOCUMENT_ROOT_URL   => '/',
       -LINK_TARGET         => '_self',
       -HTTP_HEADER_PARAMS  => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL      => 'http://forager.com/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Todo",
	    -DATASOURCE_TYPE     => $site,
       -CAL_TABLE           => 'cal_event',
       -HTTP_HEADER_DESCRIPTION => "Encyclopedia of Biological Life",
       -HTTP_HEADER_KEYWORDS    => "health, herbs, herbology, ENCY, apis theropys, homiopothy, alternate healing, integrated health management, nutrition,  ",
	    };

#return your variables to the aplication file.
return bless $self, $package; 
}

1;
