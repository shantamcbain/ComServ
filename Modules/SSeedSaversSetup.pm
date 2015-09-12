package SSeedSaversSetup;
# 	$Id: OKbeekeeperSetup.pm,v 1.1 2003/11/29 06:34:06 shanta Exp shanta $	


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;


my $self = {-HOME_VIEW               => 'PageView',
	    -AFFILIATE               => '01',
        -APP_NAME_TITLE          => 'Seed for the future.',
	    -LAST_UPDATE             => '2012/09/10',
        -SITE_DISPLAY_NAME       => 'Shuwswap Seed Savers',
	    -BASIC_DATA_VIEW         => 'BasicDataView',
	    -CSS_VIEW_NAME           => '/styles/SSSCSSView.css',
        -DEFAULT_CHARSET         => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW           => 'PageTopView',
	    -PAGE_BOTTOM_VIEW        => 'PageBottomView',
	    -PAGE_LEFT_VIEW          => 'LeftPageView',
	    -MAIL_FROM               => 'shuwswapseedsavers@grindrodbc.com',
	    -MAIL_TO                 => 'shuwswapseedsavers@grindrodbc.com',
	    -MAIL_REPLYTO            => 'shuwswapseedsavers@grindrodbc.com',
	    -MAIL_TO_USER            => 'shuwswapseedsavers@grindrodbc.com',
	    -MAIL_TO_Member          => 'shuwswapseedsavers@grindrodbc.com',
	    -MAIL_TO_DISCUSSION      => 'shuwswapseedsavers@grindrodbc.com',
        -MAIL_BCC                => 'shanta@beemaster.ca',
	    -DOCUMENT_ROOT_URL       => 'http://shuwswapseedsavers.grindrodbc.com/',
	    -IMAGE_ROOT_URL          => '/images',
        -HTTP_HEADER_PARAMS      => "[-EXPIRES => '-1d']",
        -HTTP_HEADER_DESCRIPTION => "Shuwswap Seed Savers.  ",
        -HTTP_HE
	    -MAIL_TO_AMIN                       => 'admin@shamanbotanicals.ca',
	    -MAIL_TO                            => 'admin@shamanbotanicals.ca',
	    -HTTP_HEADER_KEYWORDS    => "Seeds, pollen, pollination, pollinator, seed saving, agri-food ",
        -AUTH_TABLE          => 'SSeedSavers_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/",
	    };


return bless $self, $package; 
}






1;
