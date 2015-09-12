package OKbeekeeperSetup;
# 	$Id: OKbeekeeperSetup.pm,v 1.1 2003/11/29 06:34:06 shanta Exp shanta $	


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW_NAME    => 'OkBeekepersHome',
	    -HOME_VIEW         => 'HomeView',
	    -LAST_UPDATE       => '2005/10/22',
       -SITE_DISPLAY_NAME => 'Okanagan BeeKeepers',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -CSS_VIEW_NAME     => '/styles/bchpaok.css',
            -DEFAULT_CHARSET   => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'okbeekepers_bbs@shanta.org',
	    -MAIL_TO           => 'okbeekepers_bbs@shanta.org',
	    -MAIL_REPLYTO      => 'okbeekepers_bbs@shanta.org',
	    -MAIL_TO_USER      => 'okbeekeeper_discussion@shanta.org',
	    -MAIL_TO_Member      => 'Nokbeekeeper_member@shanta.org',
	    -MAIL_TO_DISCUSSION=> 'apis_user_list@forager.comN',
        -MAIL_BCC          => 'chaser@cablelan.net',
	     -DOCUMENT_ROOT_URL => 'http://beemaster.ca/',
	     -IMAGE_ROOT_URL    => '/images',
            -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION => "North Okanagan Beekeepers is a the Okanagan Beekeepers site.  ",
            -HTTP_HEADER_KEYWORDS    => "Beekeepers, Okanagan, bee,keeping, membership, honeybees, bees, british columbia, bc, beescene, field day, pollen, pollination, pollinator, bee trust, agri-food futures fund, fund raising, meetings, agm, conference, fair, ipe, exhibition, library, photo gallery, news release,bee publication, nucs, varroa mites, tracheal mites, honey, apiculture, beekeeper, apitherapy, agriculture, honey producers, Canadian Bee Research Fund, CBRF, bee breeders, apitherapy, pesticide, article, propolis, commercial, industry, Bees, bees, beebreeding, bee keeping, honey, honey poroduction, queens, apis, apis therapies, ",
           -AUTH_TABLE          => 'okbeekeeper_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Apis",
	    };


return bless $self, $package; 
}






1;
