package SQLSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME    => 'SQL_Ledger_Support_View',
	    -HOME_VIEW         => 'BasicDataView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -APP_LOGO          => '../csc/cscsmall.gif',
	    -APP_LOGO_ALT      => 'CSC Logo',
	    -APP_LOGO_WIDTH    => '108',
	    -APP_LOGO_HEIGHT   => '40',
	    -CSS_VIEW_NAME     => '/styles/SQLView.css',
            -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL => '/',
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/CSC",
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
            -LINK_TARGET       => '_self',
	    -MAIL_FROM         => 'csc@computersystemconsulting.ca',
	    -MAIL_TO           => 'csc@computersystemconsulting.ca',
	    -MAIL_TO_ADMIN      => 'sysadmin@computersystemconsulting.ca',
	    -MAIL_TO_USER      => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT    => 'csc_client@computersystemconsulting.ca',
	    -MAIL_REPLYTO      => 'csc@computersystemconsulting.ca',
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -SESSION_TIME_OUT  => 60 * 60 * 2,
	    -DATASOURCE_TYPE   => $datesourcetype,
            -DBI_DSN           => 'mysql:host=localhost;database=forager',
	    -MySQLPW           => '!herbsRox!',
            -AUTH_TABLE           => 'csc_user_auth_tb',
            -AUTH_MSQL_USER_NAME => 'forager',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "Computer System Consulting.ca is dedicated to online applications using secure Linux/Unix systems. ",
            -HTTP_HEADER_KEYWORDS    => "web development, CGI, Perl, scripting, interactive, e-commerce, SSL,
                               cybercash, ibill, authorizenet, third party card processing, integration,
                               Selena Sol, WebWare, Webstore, Extropia, Devlopers, Network,
                               Unix, Linux, Apache, Modules, Sendmail, Majordomo, Monarch, SSH, BSD,
                               security, programming, webmaster, HTML, B.C., British, Columbia,
                               Canada, Canadian, Virtual, Server, Host, Development, Custom,
                               Scripting, Secure, Domain, Name, Registration, ",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
