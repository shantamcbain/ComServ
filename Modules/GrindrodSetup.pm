package GrindrodSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME             => 'GrindrodHome',
            -SITE_LAST_UPDATE           => 'August 30, 2015',
 	          -PAGE_DBI                   => 'mysql:database=shanta_forager',
 	          -PAGE_MySQLPW               => 'UA=nPF8*m+T#',
            -PAGE_MSQL_USER_NAME        => 'shanta_forager',
  	        -SHOP	                      => "cs",
            -SITE_DISPLAY_NAME          => 'grinrodbc.com',
	          -HOME_VIEW                  => 'PageView',
	          -BASIC_DATA_VIEW            => 'BasicDataView',
      	    -APP_LOGO                   => '/images/apis/bee.gif',
      	    -APP_LOGO_ALT               => 'apis Logo',
	          -APP_LOGO_WIDTH             => '60',
	          -APP_LOGO_HEIGHT            => '60',
            -AUTH_TABLE                 => 'grindrod_user_auth_tb',
	          -FAVICON                    => '/images/apis/favicon.ico',
	          -ANI_FAVICON                => '/images/apis/extra/animated_favicon.gif',
	          -FAVICON_TYPE               => '/image/x-icon',
	          -CSS_VIEW_NAME              => "/styles/apis.css",
            -DEFAULT_CHARSET            => 'ISO-8859-1', 
	          -PAGE_TOP_VIEW              => 'PageTopView',
	          -PAGE_BOTTOM_VIEW           => 'PageBottomView',
	          -PAGE_LEFT_VIEW             => 'LeftPageView',
	          -MAIL_FROM                  => 'grindrod@grindrodbc.com',
	          -MAIL_TO                    => 'grindrod@grindrodbc.com',
	          -MAIL_TO_ADMIN              => 'helpdesk@computersystemconsulting.ca',
             -MAIL_REPLYTO               => 'grindrod@grindrodbc.com',
	          -MAIL_TO_USER               => 'beemaster_user_list@list.beemaster.ca',
	          -MAIL_TO_DISCUSSION         => 'grindrodparkmarket@grindrodbc.com',
	          -MAIL_LIST_BCC              => '',
	          -DOCUMENT_ROOT_URL          => '/',
	          -IMAGE_ROOT_URL             => 'images/extropia',
            -HTTP_HEADER_PARAMS         => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION    => "The Grindrod BC.  ",
            -HTTP_HEADER_KEYWORDS       => "Grindrod BC",
#	           -DATASOURCE_TYPE        => $datesourcetype,
 	          -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
            -SITE_DISPLAY_NAME          => 'The Grindrod BC',
	          -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	          -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	          -APP_DATAFILES_DIRECTORY    => "../../Datafiles/Apis",
	          -NEWS_TB                    => 'grindrod_news_tb',
	    };



return bless $self, $package; 
}






1;
