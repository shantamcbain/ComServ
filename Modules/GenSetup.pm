package GenSetup;


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
my $self = {-HOME_VIEW_NAME    => 'GenHomeView',
	    -AFFILIATE           => '13',
	    -PID                 => '44',
	    -HOME_VIEW         => 'GenHomeView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '../shanta/shantasmall.gif',
	    -APP_LOGO_ALT      => 'Shanta.org Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '100',
	    -CSS_VIEW_NAME     => '/styles/GenCSSView.css',
            -DEFAULT_CHARSET   => 'ISO-8859-1',
	    -DOCUMENT_ROOT_URL => '/',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles",
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -MAIL_FROM         => 'shanta@shanta.org',
	    -MAIL_TO           => 'shanta@shanta.org',
	    -MAIL_TO_ADMIN      => 'sysadmin@computersystemconsulting.ca',
	    -MAIL_TO_USER      => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT    => 'csc_client@computersystemconsulting.ca',
	    -MAIL_REPLYTO      => 'shanta@shanta.org',
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
            -LINK_TARGET       => '_self',
	    -DATASOURCE_TYPE   => $site,
            -AUTH_TABLE        => 'shanta_user_auth_tb',
            -AUTH_MSQL_USER_NAME => 'forager',
            -HTTP_HEADER_DESCRIPTION => "Shanta McBain's geneiology site. Gateway to many applications",
            -HTTP_HEADER_KEYWORDS    => "health, herbs, herbalogy, ENCY, apis theropys, homiopothy, alternate healing, integrated health management, nutrition, CSPS, Brewing, Beer , wine, mead, organic farming, ham radio, Shanta McBain, shanta, McBain, geniology    ",

 };

#return your variables to the application file.
return bless $self, $package; 
}

1;
