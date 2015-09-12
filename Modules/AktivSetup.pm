package AktivSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Varible for use here only
# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME    => 'TelMarkHomeView',
       -SITE_LAST_UPDATE  => 'Febuary, 25 2006',
       -SITE_DISPLAY_NAME => 'Aktiv trak ',
	    -HOME_VIEW         => 'HomeView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -APP_LOGO          => '',
	    -APP_LOGO_ALT      => 'TelMark Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '106',
	    -CSS_VIEW_NAME     => '/styles/TelMarkCSSView.css',
       -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL => '/',
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Active",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
       -LINK_TARGET       => '_self',
	    -MAIL_FROM         => 'csc@computersystemconsulting.ca',
	    -MAIL_TO           => 'csc@computersystemconsulting.ca',
	    -MAIL_TO_AMIN      => 'admin@shanta.org',
	    -MAIL_TO_DISCUSSION=> 'telmark_discussion@shanta.org',
	    -MAIL_TO_USER      => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT    => 'telmark_client@shanta.org',
	    -MAIL_REPLYTO      => 'telmark@shanta.org',
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -SESSION_TIME_OUT  => 60 * 60 * 2,
	    -DATASOURCE_TYPE   => $datesourcetype,
            -DBI_DSN           => 'mysql:host=localhost;database=forager',
	    -MySQLPW           => '!herbsRox!',
            -AUTH_TABLE           => 'telmark_user_auth_tb',
            -AUTH_MSQL_USER_NAME => 'forager',
	    };

#return your variables to the aplication file.
return bless $self, $package; 
}

1;
