package CertBeeSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'CSCHome',
            -SITE_LAST_UPDATE       => 'September, 10 2006',
	    -HOME_VIEW              => 'HomeView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/apis/bee.gif',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
       -AUTH_TABLE             => 'certbee_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/apis.css",
       -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'apis@certifiedorganicbeekeeping.com',
	    -MAIL_TO                => 'apis@certifiedorganicbeekeeping.com',
		 -MAIL_TO_ADMIN          => 'support@certifiedorganicbeekeeping.com',
       -MAIL_REPLYTO           => 'apis@certifiedorganicbeekeeping.com',
	    -MAIL_TO_USER           => 'apis_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION     => 'apis_discoussion@beemaster.ca',
	    -MAIL_LIST_BCC          => 'beekeeping_exchange@yahoogroups.com',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'http://shanta.org/images/extropia',
       -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Certifiedorganicbeekeeping.com is a Bee Keepers application created 
                                         by a bee keeper for Bee Keepers intrested in organic Certification.  ",
       -HTTP_HEADER_KEYWORDS    => "Bees, bees, bee breeding,  bee breeding, bee keeping, beekeeping, honey, honey production, queens, apis, apis therapies, pollen, pollination, pollinators, propolus, bee pollen, pollination services, Bee mentor, certified organic beekeeping, organic queens, organic bees ",
	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -APP_NAME_TITLE          => 'application',
       -SITE_DISPLAY_NAME     => 'Certified Organic BeeKeeping',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'apis_news_tb',
	    };



return bless $self, $package; 
}






1;
