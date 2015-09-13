package ApisSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'ShantaLaptopHome',
	    -HOME_VIEW         => 'ShantaLaptopHomeView',
            -SITE_LAST_UPDATE  => 'June, 28 2006',
            -AUTH_TABLE        => 'apis_user_auth_tb',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => 'http://shanta.org/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'apis Logo',
	    -APP_LOGO_WIDTH    => '60',
	    -APP_LOGO_HEIGHT   => '60',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME     => "/styles/apis.css",
            -DEFAULT_CHARSET    => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'SLTPageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'apis@beemaster.ca',
	    -MAIL_TO           => 'apis@beemaster.ca',
	    -MAIL_REPLYTO      => 'apis@beemaster.ca',
	    -MAIL_TO_USER      => 'apis_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION=> 'apis_discoussion@beemaster.ca',
	    -MAIL_LIST_BCC     => 'beekeeping_exchange@yahoogroups.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://shanta.org/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Apis\@shanta.org is a Bee Keepers application created 
                                         by a bee keeper for Bee Keepers.  ",
       -HTTP_HEADER_KEYWORDS    => "Bees, bees, beebreeding,  bee breeding, bee keeping, beekeeping, honey, honey production, queens, apis, apis therapies, pollen, pollination, pollinators, propolus, bee pollen, pollination services, Bee mentor, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME => 'Apis BeeKeeping appliation',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    };
#	    -MySQLPW             => '!herbsRox!',


return bless $self, $package; 
}






1;
