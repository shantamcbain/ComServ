package eXtropiaSetup;


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
my $self = {-HOME_VIEW_NAME    => 'ExtropiaHomeView',
       -SITE_LAST_UPDATE  => 'March, 8 2006',
       -AUTH_TABLE        => 'csc_user_auth_tb',
       -SITE_DISPLAY_NAME => "eXtropia HelpDesk",
	    -HOME_VIEW         => 'ExtropiaHomeView',
	    -BASIC_DATA_VIEW   => 'ExtropiaHomeView',
	    -APP_LOGO          => '/images/csc/cscsmall.gif',
	    -APP_LOGO_ALT      => 'CSC Logo',
	    -APP_LOGO_WIDTH    => '108',
	    -APP_LOGO_HEIGHT   => '40',
	    -CSS_VIEW_NAME     => '/styles/eXtropiaCSSView.css',
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_TO_ADMIN     => 'webmaster@computersystemconsulting.ca',
	    -MAIL_FROM         => 'csc@computersystemconsulting.ca',
	    -MAIL_TO           => 'extropiauser@forager.com',
	    -MAIL_REPLYTO      => 'csc@computersystemconsulting.ca',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/CSC",
            -LINK_TARGET => '_self',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "eXtropia HelpDesk",
            -HTTP_HEADER_KEYWORDS    => "eXtropia HelpDesk,eXtropia, HelpDesk,Web applications, Application hosting, hosting, support, ",
	    -DATASOURCE_TYPE   => $site,
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;