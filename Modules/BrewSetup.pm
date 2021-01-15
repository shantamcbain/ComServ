package BrewSetup;


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
my $self = {-HOME_VIEW_NAME    => 'HomrView',
	    -HOME_VIEW         => 'HomeView',
	    -MySQLPW           => '!herbsRox!',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'Brew Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '100',
	    -CSS_VIEW_NAME     => '/styles/BrewCSSView.css',
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'shanta@grindrodbc.com',
	    -MAIL_TO_AMIN      => 'shanta@computersystemconsulting.ca',
	    -MAIL_TO           => 'shanta@usbm.com',
	    -MAIL_REPLYTO      => 'shanta@grindrodbc.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
        -LINK_TARGET       => '_self',
        -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
        -SITE_LAST_UPDATE           => 'Noveber16, 2016',
	    -APP_DATAFILES_DIRECTORY => "Datafiles/Brew",
	    -DATASOURCE_TYPE   => $site,
       -AUTH_TABLE        => 'brew_user_auth_tb',
       -DEFAULT_CHARSET   => 'ISO-8859-1',
       -SITE_DISPLAY_NAME => 'Brew Application',
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
