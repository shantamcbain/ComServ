package HESetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME         => 'PageView',
            -SITE_LAST_UPDATE       => 'Janualry 19, 2013',
	    -HOME_VIEW              => 'PageView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/apis/bee.gif',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
            -AUTH_TABLE             => 'he_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/he.css",
            -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'helpfulearth@helpfullearth.com',
	    -MAIL_TO                => 'helpfulearth@helpfullearth.com',
	    -MAIL_TO_ADMIN          => 'support@helpfullearth.com',
            -MAIL_REPLYTO           => 'helpfuleart@helpfullearth.com',
	    -MAIL_TO_USER           => 'helpfulearth_list@helpfullearth.com',
	    -MAIL_TO_DISCUSSION     => 'helpfulearth_discoussion@helpfullearth.com',
	    -MAIL_LIST_BCC          => '',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'http://forager.com/images/extropia',
            -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Helpfull Earth is dedicated to living in harmony with the planet.  ",
       -HTTP_HEADER_KEYWORDS    => "Organic farming, Sustainable agriculture, Natural land development,  Resuable Goods",
	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME     => 'Helpfull Earth On The Web',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'apis_news_tb',
	    };



return bless $self, $package; 
}






1;
;
