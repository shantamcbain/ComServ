package BCHPASetup;
# 	$Id: BCHPASetup.pm,v 1.1 2003/11/29 06:34:06 shanta Exp shanta $	


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'BCHPAHome',
	    -HOME_VIEW         => 'BCHPAAdminHomeView',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -CSS_VIEW_NAME     => '/styles/bchpa.css',
            -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'apis@forager.com',
	    -MAIL_TO           => 'apis@forager.com',
	    -MAIL_REPLYTO      => 'apis@forager.com',
	    -MAIL_TO_USER      => 'apis_user_list@forager.com',
	    -MAIL_TO_DISCUSSION=> 'apis_discussion@forager.com',
            -MAIL_BCC          => 'bobnkaye@shaw.ca,wen_webdesign@yahoo.com',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://bcbeekeepers.com/images',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "BCHPA is a the BC Honey producers Assoiation site.  ",
            -HTTP_HEADER_KEYWORDS    => "bchpa, BCHPA, bee,keeping, membership, honeybees, bees, british columbia, bc, beescene, field day, pollen, pollination, pollinator, bee trust, agri-food futures fund, fund raising, meetings, agm, conference, fair, ipe, exhibition, library, photo gallery, news release,bee publication, nucs, varroa mites, tracheal mites, honey, apiculture, beekeeper, apitherapy, agriculture, honey producers, Canadian Bee Research Fund, CBRF, bee breeders, apitherapy, pesticide, article, propolis, commercial, industry, Bees, bees, beebreeding, bee keeping, honey, honey poroduction, queens, apis, apis therapies, ",
	    -DATASOURCE_TYPE     => $datesourcetype,
            -DBI_DSN             => 'mysql:host=localhost;database=forager',
	    -MySQLPW             => '!herbsRox!',
            -AUTH_TABLE          => 'bchpa_user_auth_tb',
            -AUTH_MSQL_USER_NAME => 'forager',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    };


return bless $self, $package; 
}






1;
