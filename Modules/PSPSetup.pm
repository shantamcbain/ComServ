package PSPSetup;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'HomeView',
	    -HOME_VIEW         => 'HomeView',
        -SITE_LAST_UPDATE  => 'May, 23 2019',
        -AUTH_TABLE        => 'apis_user_auth_tb',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => 'https://static.wixstatic.com/media/4c22e4_1bc14a11a92b4d1e8e1e002389840924~mv2.png/v1/fill/w_96,h_96,al_c,q_80,usm_0.66_1.00_0.01/Anu-Collective-Logo-Final_2x.webp',
	    -APP_LOGO_ALT      => 'Anu Logo',
	    -APP_LOGO_WIDTH    => '60',
	    -APP_LOGO_HEIGHT   => '60',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME     => "/styles/apis.css",
            -DEFAULT_CHARSET    => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'anu@anucollective.beemaster.ca',
	    -MAIL_TO           => 'anu@anucollective.beemaster.ca',
	    -MAIL_REPLYTO      => 'anu@anucollective.beemaster.ca',
	    -MAIL_TO_USER      => 'apis_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION=> 'anubeekeeping@anucollective.beemaster.ca',
	    -MAIL_LIST_BCC     => '',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Anu Collective Beekeeping course.  ",
       -HTTP_HEADER_KEYWORDS    => "Bees, bees, beebreeding,  bee breeding, bee keeping, beekeeping, honey, honey production, queens, apis, apis therapies, pollen, pollination, pollinators, propolus, bee pollen, pollination services, Bee mentor, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME => 'Anu BeeKeeping application',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Anu",
	    };
#	    -MySQLPW             => '!herbsRox!',


return bless $self, $package; 
}






1;
