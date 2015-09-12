package TemplateSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {
            -SITE_LAST_UPDATE       => 'August 16, 2012', 
 	    -APP_NAME_TITLE         => 'Name of application',
            -SITE_DISPLAY_NAME      => 'Name of site',
	    -HOME_VIEW              => 'PageView',
	    -BASIC_DATA_VIEW        => 'BasicDataView',
	    -APP_LOGO               => '/images/apis/bee.gif',
	    -APP_LOGO_ALT           => 'apis Logo',
	    -APP_LOGO_WIDTH         => '60',
	    -APP_LOGO_HEIGHT        => '60',
            -AUTH_TABLE             => 'apis_user_auth_tb',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME          => "/styles/apis.css",
            -DEFAULT_CHARSET        => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW          => 'PageTopView',
	    -PAGE_BOTTOM_VIEW       => 'PageBottomView',
	    -PAGE_LEFT_VIEW         => 'LeftPageView',
	    -MAIL_FROM              => 'beemaster@beemaster.ca',
	    -MAIL_TO                => 'shanta@beemaster.ca',
	    -MAIL_TO_ADMIN          => 'support@beemaster.ca',
            -MAIL_REPLYTO           => 'beemasters@beemaster.ca',
	    -MAIL_TO_USER           => 'beemaster_user_list@list.beemaster.ca',
	    -MAIL_TO_DISCUSSION     => 'beemaster@list.beemaster.ca',
	    -MAIL_LIST_BCC          => '',
	    -DOCUMENT_ROOT_URL      => '/',
	    -IMAGE_ROOT_URL         => 'http://shanta.org/images/extropia',
            -HTTP_HEADER_PARAMS     => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "Replace with your header discripion ",
            -HTTP_HEADER_KEYWORDS    => "keyword for search engines",
	    -DATASOURCE_TYPE        => $datesourcetype,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
            -SITE_DISPLAY_NAME     => 'BeeMaster BeeKeeping application',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    -NEWS_TB                 => 'apis_news_tb',
	    };



return bless $self, $package; 
}






1;
