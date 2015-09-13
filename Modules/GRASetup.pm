package GRASetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'GrindrodParkMarketHome',
            -SITE_LAST_UPDATE       => 'September 28, 2010',
 	    -SHOP	            => "cs",
            -SITE_DISPLAY_NAME      => 'gra.grinrodbc.com',
	    -HOME_VIEW              => 'HomeView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/apis/bee.gif',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
            -AUTH_TABLE             => 'gpm_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/apis.css",
            -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'gra@grindrodbc.com',
	    -MAIL_TO                => 'gra@grindrodbc.com',
	    -MAIL_TO_ADMIN          => 'helpdesk@computersystemconsulting.ca',
            -MAIL_REPLYTO           => 'gra@grindrodbc.com',
	    -MAIL_TO_USER           => 'GPM_user@grindrodbc.com',
	    -MAIL_TO_DISCUSSION     => 'GPM_Discoussion@grindrodbc.com',
	    -MAIL_LIST_BCC          => '',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'images/extropia',
            -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "The Grindrod Park Market.  ",
            -HTTP_HEADER_KEYWORDS    => "Sustainable Agriculture",
#	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
            -SITE_DISPLAY_NAME     => 'The Grindrod Recreation Association ',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'gpm_news_tb',
	    };



return bless $self, $package; 
}






1;
