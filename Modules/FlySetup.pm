package FlySetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $site = 'file';
my $site = 'MySQL';
my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME    => 'FlyHomeView',
	    -AFFILIATE           => '13',
	    -PID                 => '44',
	    -HOME_VIEW         => 'FlyHomeView',
	    -MySQLPW           => '!herbsRox!',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '../shanta/shantasmall.gif',
	    -APP_LOGO_ALT      => 'Shanta.org Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '100',
	    -CSS_VIEW_NAME     => '/styles/FlyCSSView.css',
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'shanta@shanta.org',
	    -MAIL_TO_ADMIN      => 'webmaster@computersystemconsulting.ca',
	    -MAIL_TO           => 'fly_list@shanta.org',
	    -MAIL_REPLYTO      => 'shanta@shanta.org',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
            -LINK_TARGET       => '_self',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Fly",
	    -DATASOURCE_TYPE   => $site,
            -AUTH_TABLE        => 'shanta_user_auth_tb',
            -DEFAULT_CHARSET   => 'ISO-8859-1',
            -HTTP_HEADER_DESCRIPTION => "Fly fishing and fly tying application",
            -HTTP_HEADER_KEYWORDS    => "Fly fishing, fly tying, application hosting, fishing, fly patterns",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
