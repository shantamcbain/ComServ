package AikikaiSetup;


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
            -SITE_LAST_UPDATE       => 'January 6, 2014',
            -SITE_DISPLAY_NAME          => 'Grand View Bench Aikikai',
            -HOME_VIEW_NAME    => 'PageView',
	    -HOME_VIEW         => 'PageView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/logo.gif',
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
	    -MAIL_FROM         => 'peter@grandviewbenchaikikai.com',
	    -MAIL_TO           => 'shanta@grandviewbenchaikikai.com',
	    -MAIL_REPLYTO      => 'peter@grandviewbenchaikikai.com',
	    -MAIL_TO_USER      => 'skye_user_list@grandviewbenchaikikai.com',
	    -MAIL_TO_DISCUSSION=> 'skye_discussion@grandviewbenchaikikai.com',
	    -MAIL_LIST_BCC     => 'shanta@grandviewbenchaikikai.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Grand View Bench Aikikai",
       -HTTP_HEADER_KEYWORDS    => "Marshal arts, aikikdo, dojo ",
	    -DATASOURCE_TYPE     => $datesourcetype,
       -DATA_TABLE          => 'ecf_order_table',
       -DATA_TABLE_BILL     => 'bill_order_table',
       -AUTH_TABLE          => 'aikikai_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Skye",
	    };


return bless $self, $package; 
}






1;
