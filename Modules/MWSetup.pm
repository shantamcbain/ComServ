package MWSetup;


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
my $self = {-HOME_VIEW_NAME    => 'PageView',
	    -HOME_VIEW         => 'PageView',
	 #   -MySQLPW           => '!herbsRox!',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'MacDonald Water Systems Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '100',
	    -CSS_VIEW_NAME     => '/styles/MWCSSView.css',
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'sales@macdonaldwatersystem.com',
	    -MAIL_TO_AMIN      => 'helpdesk@computersystemconsulting.ca',
	    -MAIL_TO           => 'sales@macdonaldwatersystem.com',
	    -MAIL_REPLYTO      => 'sales@macdonaldwatersystem.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '../images/extropia',
            -LINK_TARGET       => '_self',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
            -SITE_LAST_UPDATE           => 'Oct 8, 2013',
	    -APP_DATAFILES_DIRECTORY => "Datafiles/MW",
	    -DATASOURCE_TYPE   => $site,
            -AUTH_TABLE        => 'mw_user_auth_tb',
            -CLIENT_TB         => 'mw_client_tb',
            -DEFAULT_CHARSET   => 'ISO-8859-1',
            -SITE_DISPLAY_NAME => 'Water Application',
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
