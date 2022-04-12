package MonasheeSupportSetup;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;



my $self = {-HOME_VIEW_NAME    => 'HomeView',
	    -HOME_VIEW         => 'HomeView',
 	    -AFFILIATE           => '1',
	    -PID                 => '137',
           -SITE_LAST_UPDATE  => 'April, 12 2022',
            -AUTH_TABLE        => 'monasheesupport_user_auth_tb',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => 'https://www.monasheecommunitycoop.ca/wp-content/uploads/2020/04/Smaller-Co-op-Logo.jpg',
	    -APP_LOGO_ALT      => 'Monashee coop Logo',
	    -APP_LOGO_WIDTH    => '60',
	    -APP_LOGO_HEIGHT   => '60',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME     => "/styles/monasheesupport.css",
       -DEFAULT_CHARSET    => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'support@computersystemconsulting.ca',
	    -MAIL_TO           => 'support@computersystemconsulting.ca',
	    -MAIL_REPLYTO      => 'support@computersystemconsulting.ca',
	    -MAIL_TO_USER      => 'support@computersystemconsulting.ca',
	    -MAIL_TO_DISCUSSION=> 'support@computersystemconsulting.ca',
	    -MAIL_LIST_BCC     => '',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Monashee coop support site.  ",
       -HTTP_HEADER_KEYWORDS    => "Food, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME => 'Monashee support application',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Monasseesupport",
	    };
#	    -MySQLPW             => '!herbsRox!',


return bless $self, $package; 
}






1;
