package IMSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'CSCHome',
       -SHOP              => 'IM',
       -SITE_LAST_UPDATE       => 'March 31, 2012',
	    -HOME_VIEW              => 'PageView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/IM/nut1.JPG',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
       -AUTH_TABLE             => 'he_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/IM.css",
       -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'paul@iamnutsaboutcrystals.com',
	    -MAIL_TO                => 'nuts@iamnutsaboutcrystals.com',
		 -MAIL_TO_ADMIN          => 'support@iamnutsaboutcrystals.com',
       -MAIL_REPLYTO           => 'nuts@iamnutsaboutcrystals.com',
	    -MAIL_TO_USER           => 'nuts@iamnutsaboutcrystals.com',
	    -MAIL_TO_DISCUSSION     => 'ia_discoussion@iamnutsaboutcrystals.com',
	    -MAIL_LIST_BCC          => '',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'http://forager.com/images/extropia',
       -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "I am nuts about crystals is dedicated to crystal harmony with the planet.  ",
       -HTTP_HEADER_KEYWORDS    => "crystals, healing",
	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
       -SITE_DISPLAY_NAME     => 'I am nuts about crystals!',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'apis_news_tb',
	    };



return bless $self, $package; 
}






1;
;
