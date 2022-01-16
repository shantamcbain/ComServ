package LTrustSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 1;


my $self = {-HOME_VIEW_NAME          => 'PageView',
	    -AFFILIATE           => '13',
	    -PID                 => '129',
            -SITE_LAST_UPDATE        => 'Feb 22, 2010',
 	    -SHOP	             => "LTrust",
            -SITE_DISPLAY_NAME       => 'Sustainable Earth Conservatory',
	    -HOME_VIEW               => 'HomeView',
	    -BASIC_DATA_VIEW         => 'BasicDataView',
	    -APP_LOGO                => '/images/apis/bee.gif',
	    -APP_LOGO_ALT            => 'apis Logo',
	    -APP_LOGO_WIDTH          => '60',
	    -APP_LOGO_HEIGHT         => '60',
            -AUTH_TABLE              => 'ltrust_user_auth_tb',
	    -FAVICON                 => '/images/apis/favicon.ico',
	    -ANI_FAVICON             => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE            => '/image/x-icon',
	    -CSS_VIEW_NAME           => "/styles/apis.css",
            -DEFAULT_CHARSET         => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW           => 'PageTopView',
	    -PAGE_BOTTOM_VIEW        => 'PageBottomView',
	    -PAGE_LEFT_VIEW          => 'LeftPageView',
	    -MAIL_FROM               => 'ltrustlandtrust@beemaster.ca',
	    -MAIL_TO                 => 'ltrustlandtrust@beemaster.ca',
  	    -MAIL_TO_ADMIN           => 'support@beemaster.ca',
            -MAIL_REPLYTO            => 'ltrust@beemaster.ca',
  	    -MAIL_TO_USER            => 'landtrust_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION      => 'landtrust@beemaster.ca',
	    -MAIL_LIST_BCC           => '',
	    -DOCUMENT_ROOT_URL       => '/',
	    -IMAGE_ROOT_URL          => 'http://shanta.org/images/extropia',
            -HTTP_HEADER_PARAMS      => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "Land trust.  ",
            -HTTP_HEADER_KEYWORDS    => "Land trust ",
	    -DATASOURCE_TYPE         => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'landtrust_news_tb',
	    };



return bless $self, $package; 
}






1;
