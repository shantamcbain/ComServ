package CityShopSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Varible for use here only
# $site = 'file';
my $site = 'MySQL';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME    => 'CSHomeView',
	    -HOME_VIEW         => 'CSHomeView',
	    -MySQLPW           => '!herbsRox!',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '../cs/csbig.gif',
	    -APP_LOGO_ALT      => 'City Shop Logo',
	    -APP_LOGO_WIDTH    => '158',
	    -APP_LOGO_HEIGHT   => '70',
	    -CSS_VIEW_NAME     => 'CSCSSView',
	    -PAGE_TOP_VIEW     => 'SubTopFrameView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'cityshopadmin@forager.com',
	    -MAIL_TO           => 'cityshopadmin@forager.com',
	    -MAIL_REPLYTO      => 'cityshopadmin@forager.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
            -LINK_TARGET => '_mainCon',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/CS",
	    -DATASOURCE_TYPE   => $site,
            -DBI_DSN           => 'mysql:host=localhost;database=forager',
	    -MySQLPW           => '!herbsRox!',
            -AUTH_TABLE           => 'csc_user_auth_tb',
            -AUTH_MSQL_USER_NAME => 'forager',
            -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    };

#return your variables to the aplication file.
return bless $self, $package; 
}

1;
