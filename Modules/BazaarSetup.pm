package BazaarSetup;


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
my $self = {-HOME_VIEW_NAME => 'PageView',
            -AUTH_TABLE          => 'bazaar_user_auth_tb',
            -LAST_UPDATE         => 'March 20, 2014',
            -SITE_LAST_UPDATE    => 'March 20, 2014',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -HOME_VIEW           => 'PageView',
	    -BASIC_DATA_VIEW     => 'BasicDataView',
	    -APP_LOGO            => '/images/apis/bee.gif',
	    -APP_LOGO_ALT        => 'Gypsy Bazaar Logo',
	    -APP_LOGO_WIDTH      => '130',
	    -APP_LOGO_HEIGHT     => '120',
	    -CSS_VIEW_NAME       => '/styles/WiseWomanCSSView.css',
	    -PAGE_TOP_VIEW       => 'PageTopView',
	    -PAGE_BOTTOM_VIEW    => 'PageBottomView',
	    -PAGE_LEFT_VIEW      => 'LeftPageView',
	    -LEFT_PAGE_VIEW      => 'LeftPageView',
	    -MAIL_FROM           => 'bazaar@countrystores.ca',
	    -MAIL_TO             => 'bazaar@countrystores.ca',
	    -MAIL_TO_DISCUSSION  => 'bazaar@countrystores.ca',
	    -MAIL_TO_ADMIN       => 'webmaster@computersystemconsulting.ca',
	    -MAIL_TO_USER        => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT      => 'csc_client@computersystemconsulting.ca',
	    -MAIL_REPLYTO        => 'bazaar@countrystores.ca',
	    -SITE_DISPLAY_NAME   => 'Gypsy Bazaar.',
	    -DOCUMENT_ROOT_URL   => '/',
            -LINK_TARGET         => '_self',
            -HTTP_HEADER_PARAMS  => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL      => 'http://forager.com/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Todo",
	    -DATASOURCE_TYPE     => $site,
            -CAL_TABLE           => 'cal_event',
            -HTTP_HEADER_DESCRIPTION => "Gypsy Bazaar.",
            -HTTP_HEADER_KEYWORDS    => "health, herbs, herbology, ENCY, apis theropys, homiopothy, alternate healing, integrated health management, nutrition, clothing, food, soap, seeds ",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
