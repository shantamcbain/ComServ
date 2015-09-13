package HoneyDoSetup;
# 	$Id: RVSetup.pm,v 1.2 2004/02/02 21:21:00 shanta Exp $	


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
my $datesourcetype = 'File';

sub new {
my $package    = shift;
my $UseModPerl = shift || 1;


my $self = {-HOME_VIEW_NAME => 'HomeView',
	    -HOME_VIEW           => 'HomeView',
	    -BASIC_DATA_VIEW     => 'BasicDataView',
	    -APP_LOGO            => '',
	    -APP_LOGO_ALT        => 'Honey Do Logo',
	    -APP_LOGO_WIDTH      => '20',
	    -APP_LOGO_HEIGHT     => '20',
	    -CSS_VIEW_NAME       => '/styles/honeydoCSSView.css',
       -DEFAULT_CHARSET     => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW       => 'PageTopView',
	    -PAGE_BOTTOM_VIEW    => 'PageBottomView',
	    -LEFT_PAGE_VIEW      => 'LeftPageView',
	    -MAIL_FROM           => 'honeydo@honeydosmallengine.com',
	    -MAIL_TO             => 'honeydo@honeydosmallengine.com',
	    -MAIL_REPLYTO        => 'honeydo_admin@forager.com',
	    -MAIL_TO_USER        => 'honeydo_user_list@honeydosmallengine.com',
	    -MAIL_TO_DISCUSSION  => 'honey_discussion@honeydosmallengine.com',
	    -DOCUMENT_ROOT_URL   => '/',
	    -IMAGE_ROOT_URL      => 'http://shanta.org/images/extropia',
       -HTTP_HEADER_PARAMS  => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION => "Honey Do Small Engine Repair and Sales",
       -HTTP_HEADER_KEYWORDS => "Small Engine.",
	    -DATASOURCE_TYPE     => $datesourcetype,
       -AUTH_TABLE          => 'honeydo_user_auth_tb',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/HoneyDo",
       -SESSION_DIR         => "../store/shops/honeydo/Sessions",
	    };


return bless $self, $package;
}






1;
