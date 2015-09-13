package KamasketSetup;

use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'HomeView',
            -SITE_LAST_UPDATE       => 'September 15, 2010',
 	    -SHOP	            => "cs",
            -SITE_DISPLAY_NAME      => 'Kamakset Music Festival',
	    -HOME_VIEW              => 'HomeView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/apis/bee.gif',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
      -AUTH_TABLE             => 'komasket_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/Kamasket.css",
      -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'komasket@beemaste.ca',
	    -MAIL_TO                => 'komasket@beemaster.ca',
	    -MAIL_TO_ADMIN          => 'helpdesk@computersystemconsulting.ca',
      -MAIL_REPLYTO           => 'grindrod@grindrodbc.com',
	    -MAIL_TO_USER           => 'komasketvalunteers@beemaster.ca',
	    -MAIL_TO_DISCUSSION     => 'grindrodparkmarket@grindrodbc.com',
	    -MAIL_LIST_BCC          => '',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'images/extropia',
      -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
      -HTTP_HEADER_DESCRIPTION => "The Kamasket.  ",
      -HTTP_HEADER_KEYWORDS    => "Kamasket Music Festival",
#	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'komasket_news_tb',
            -PROJECT_TB              => 'komasket_project_tb',
            -CLIENT_TB               => 'komasket_client_tb',
            -LOG_TB                  => 'komasket_log_tb',
	    };



return bless $self, $package; 
}






1;