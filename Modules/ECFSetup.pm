package ECFSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {            
       -SHOP              => 'apis',
       -APP_NAME_TITLE    => "Sustainable Farming Application",
       -SITE_LAST_UPDATE  => 'March 2, 2012',
       -SITE_DISPLAY_NAME => 'Eagle Creek Farms',
       -HOME_VIEW_NAME    => 'ECFHomeView',
	    -HOME_VIEW         => 'PageView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'apis Logo',
	    -APP_LOGO_WIDTH    => '80',
	    -APP_LOGO_HEIGHT   => '80',
	    -FAVICON           => '/images/apis/favicon.ico',
	    -ANI_FAVICON       => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE      => '/image/x-icon',
	    -CSS_VIEW_NAME     => '/styles/ECFCSSView.css',
       -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'shanta@beemaster.ca',
	    -MAIL_TO           => 'shanta@beemaster.ca',
	    -MAIL_REPLYTO      => 'shanta@beemaster.ca',
	    -MAIL_TO_USER      => 'apis_user_list@beemaster.ca',
	    -MAIL_TO_DISCUSSION=> 'apis_discussion@beemaster.ca',
	    -MAIL_LIST_BCC     => 'beekeeping_exchange@yahoogroups.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Bee, Queens, Honey",
       -HTTP_HEADER_KEYWORDS    => "Organic beekeeping, Bees, bees, bee breeding, bee keeping, honey, honey production, queens, bee queens,  apis, apis therapies, pollination, pollination services, packages, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
       -DATA_TABLE          => 'ecf_order_table',
       -DATA_TABLE_BILL     => 'bill_order_table',
       -AUTH_TABLE          => 'ecf_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    };


return bless $self, $package; 
}






1;
