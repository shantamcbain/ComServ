package SMOSetup;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {
       -HOME_VIEW_NAME     => 'HomeView',
	    -AFFILIATE          => '1',
	    -PID                => '121',
	    -HOME_VIEW          => 'HomeView',
       -SITE_LAST_UPDATE   => ' 02, 18 2022',
       -AUTH_TABLE         => 'smo_user_auth_tb',
	    -BASIC_DATA_VIEW    => 'BasicDataView',
	    -APP_LOGO           => '',
	    -APP_LOGO_ALT       => 'Anu Logo',
	    -APP_LOGO_WIDTH     => '60',
	    -APP_LOGO_HEIGHT    => '60',
	    -FAVICON            => '/images/apis/favicon.ico',
	    -ANI_FAVICON        => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE       => '/image/x-icon',
	    -CSS_VIEW_NAME      => '/styles/apis.css',
       -DEFAULT_CHARSET    => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW      => 'PageTopView',
	    -PAGE_BOTTOM_VIEW   => 'PageBottomView',
	    -PAGE_LEFT_VIEW     => ,
	    -MAIL_FROM          => 'info@saddlemountainornanics.beemaster.ca',
	    -MAIL_TO            => 'shanta@beemaster.ca, mnickers@beemaster.ca',
	    -MAIL_REPLYTO       => 'info@saddlemountainornanics.beemaster.ca',
	    -MAIL_TO_USER       => 'smo_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION => 'beekeeping@saddlemountainorganics.beemaster.ca',
	    -MAIL_LIST_BCC      => '',
	    -DOCUMENT_ROOT_URL  => '/',
	    -IMAGE_ROOT_URL     => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Saddle Mountain Beekeeping.  ",
       -HTTP_HEADER_KEYWORDS    => "Bees, bees, beebreeding,  bee breeding, bee keeping, beekeeping, honey, honey production, queens, apis, apis therapies, pollen, pollination, pollinators, propolus, bee pollen, pollination services, Bee mentor, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME => 'Saddle Mountain Organics BeeKeeping',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/SMO",
	    };
#	    -MySQLPW             => '!herbsRox!',


return bless $self, $package; 
}






1;
