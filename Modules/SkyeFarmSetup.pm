package SkyeFarmSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {            
       -SHOP              => 'Skye',
       -SITE_LAST_UPDATE       => 'January 6, 2012',
       -SITE_DISPLAY_NAME          => 'Skye  Farm Gourmet Garlic',
       -HOME_VIEW_NAME    => 'HomeView',
	    -HOME_VIEW         => 'HomeView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => 'http://skyefarm.com/images/logo.gif',
	    -APP_LOGO_ALT      => 'skye Logo',
	    -APP_LOGO_WIDTH    => '238',
	    -APP_LOGO_HEIGHT   => '50',
	    -FAVICON                => '/images/apis/favicon.ico',
	    -ANI_FAVICON            => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE           => '/image/x-icon',
	    -CSS_VIEW_NAME     => '/styles/SkyeFarmCSSView.css',
            -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'peter@skyefarm.com',
	    -MAIL_TO           => 'shanta@skyefarm.com',
	    -MAIL_REPLYTO      => 'peter@skyefarm.com',
	    -MAIL_TO_USER      => 'skye_user_list@skyefarm.c',
	    -MAIL_TO_DISCUSSION=> 'skye_discussion@skyefarm.ca',
	    -MAIL_LIST_BCC     => 'shanta@skyefarm.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Bee, Queens, Honey",
       -HTTP_HEADER_KEYWORDS    => "Organic beekeeping, Bees, bees, beebreeding, bee keeping, honey, honey poroduction, queens, bee queens,  apis, apis therapies, pollination, pollination services, packages, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
       -DATA_TABLE          => 'ecf_order_table',
       -DATA_TABLE_BILL     => 'bill_order_table',
       -AUTH_TABLE          => 'skye_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Skye",
	    };


return bless $self, $package; 
}






1;
