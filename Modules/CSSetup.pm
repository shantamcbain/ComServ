package CSSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';


sub new {
my $package   = shift;
my $UseModPerl = shift || 1;

# This is where you define your variable mapping.
my $self =  {-HOME_VIEW_NAME       => 'HomeView',
       -SITE_LAST_UPDATE           => 'April, 2, 2012',
	    -HOME_VIEW                  => 'PageView',
	    -BASIC_DATA_VIEW            => 'BasicDataView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -APP_LOGO                   => '',
	    -APP_LOGO_ALT               => "Country Stores"||"CS Logo, Web hosting, CSC Memberships, Honey, bees wax candles, organic food",
	    -APP_LOGO_WIDTH             => '150',
	    -APP_LOGO_HEIGHT            => '60',
	    -FAVICON                    => '/images/apis/favicon.ico',
	    -ANI_FAVICON                => '/images/apis/extra/animated_favicon.gif',
	    -FAVICON_TYPE               => '/image/x-icon',
	    -CSS_VIEW_NAME              => '/styles/CSSView.css',
       -DEFAULT_CHARSET            => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL          => '/',
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY    => "Datafiles/CSC",
	    -GLOBAL_DATAFILES_DIRECTORY => "Datafiles",
       -HTTP_HEADER_PARAMS         => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL             => '/images/extropia',
       -LINK_TARGET                => '_self',
	    -MAIL_FROM                  => 'support@countrystores.ca',
	    -MAIL_TO                    => 'support@countrystores.ca',
	    -MAIL_TO_ADMIN              => 'support@countrystores.ca',
	    -MAIL_TO_USER               => 'cs_user_list@countrystores.ca',
	    -MAIL_TO_CLIENT             => 'cs_client@countrystores.c',
	    -MAIL_REPLYTO               => 'cs@countrystores.ca',
	    -PAGE_TOP_VIEW              => 'PageTopView'  || 'CSFrameView',
	    -PAGE_BOTTOM_VIEW           => 'PageBottomView',
	    -PAGE_LEFT_VIEW             => 'LeftPageView' || 'CSLeftLinksView',
	    -LEFT_PAGE_VIEW             => 'LeftPageView',
 	    -SESSION_TIME_OUT           => 60 * 60 * 2,
       -SITE_DISPLAY_NAME          => 'Country Stores',
       -AUTH_TABLE                 => 'cs_user_auth_tb',
       -ADMIN_AUTH_TABLE           => 'cs_admin_auth_tb',
       -HTTP_HEADER_PARAMS         => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION    => "Country Stores Selling members goods online and at markets. ",
       -HTTP_HEADER_KEYWORDS       => "Honey, Bees wax, Candles, Bee Queens, Site Memberships, Organic food, Herbs, spices, browing hops,computers,  B.C., British, Columbia,
                                      Canada, Canadian, BC",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
