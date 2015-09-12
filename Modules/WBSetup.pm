package WBSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'Pageiew',
	    -HOME_VIEW         => 'PageView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'apis Logo',
	    -APP_LOGO_WIDTH    => '80',
	    -APP_LOGO_HEIGHT   => '80',
	    -SITE_DISPLAY_NAME => 'Weaver Beck Family',
	    -CSS_VIEW_NAME     => '/styles/WBCSSView.css',
       -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'shanta@weaverbeck.com',
	    -MAIL_TO           => 'shanta@weaverbeck.com',
	    -MAIL_REPLYTO      => 'shanta@weaverbeck.com',
	    -MAIL_TO_USER      => 'wb_user_list@weaverbeck.com',
	    -MAIL_TO_DISCUSSION=> 'weaverbeck_discussion@weaverbeckbeemaster.ca',
	    -MAIL_LIST_BCC     => '',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Weaver Beck is the geneology home of the weaver beck family.  ",
       -HTTP_HEADER_KEYWORDS    => "Weaver, Beck, McBain, Shanta, Lew, Jens, Bea",
	    -DATASOURCE_TYPE     => $datesourcetype,
       -DATA_TABLE          => 'ecf_order_table',
       -DATA_TABLE_BILL     => 'bill_order_table',
       -AUTH_TABLE          => 'wb_user_auth_tb',
       -AUTH_MSQL_USER_NAME => 'forager',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    };


return bless $self, $package; 
}






1;
