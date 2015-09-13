package SocialExpSetup;

# 	$Id: SocialExpSetup.pm,v 1.1 2012/9/1 06:35:52 shanta Exp shanta $	

use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Varible for use here only
my $GLOBAL_DATAFILES_DIRECTORY;
my $TEMPLATES_CACHE_DIRECTORY;
my $APP_DATAFILES_DIRECTORY;
my $datesourcetype;
my $AUTH_TABLE= 'socialexp_user_auth_tb';
my @PRODUCT_DATASOURCE_CONFIG_PARAMS;
my @URL_DATASOURCE_CONFIG_PARAMS;
my @AUTH_USER_DATASOURCE_PARAMS;

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME                => 'HomeView',
            -AFFILIATE                     => '012',
            -SITE_LAST_UPDATE              => 'Sept 1,  2012',
	    -HOME_VIEW                     => 'PageView',
            -SITE_DISPLAY_NAME             => 'A Social Experiment',
	    -BASIC_DATA_VIEW               => 'BasicDataView',
	    -APP_NAME_TITLE                => 'Man experiencing Man',
	    -APP_LOGO                      => '/images/forager/foragericon.gif',
	    -APP_LOGO_ALT                  => 'Social Experiment Logo',
	    -APP_LOGO_WIDTH                => '108',
	    -APP_LOGO_HEIGHT                    => '108',
	    -CSS_VIEW_NAME                      => '/styles/SocialExpCSSView.css',
       -DEFAULT_CHARSET                    => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL                  => '/',
       -HTTP_HEADER_PARAMS                 => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION            => "Mans have been leaning to discover how to get along with each other for as long as there have been man
                                   ",
       -HTTP_HEADER_KEYWORDS               => "social, Man
            ",
	    -IMAGE_ROOT_URL                     => 'http://forager.com/images/extropia',
	    -LEFT_PAGE_VIEW                     => 'LeftPageView',
       -LINK_TARGET                        => '_self',
	    -MAIL_FROM                          => 'socialexp@forager.com',
	    -MAIL_TO_AMIN                       => 'admin@computersystemconsulting.ca',
	    -MAIL_TO                            => 'socialexp@forager.com',
	    -MAIL_TO_USER                       => 'user_list@forager.com',
	    -MAIL_TO_DISCUSSION                 => 'forager_discoussion@forager.com',
	    -MAIL_LIST_BCC                      => 'beekeeping_exchange@yahoogroups.com',
	    -MAIL_TO_CLIENT                     => 'client@forger.com',
	    -MAIL_REPLYTO                       => 'forger@forager.com',
	    -PAGE_TOP_VIEW                      => 'PageTopView',
	    -PAGE_BOTTOM_VIEW                   => 'PageBottomView',
	    -PAGE_LEFT_VIEW                     => 'LeftPageView',
	    -SESSION_TIME_OUT                   => '7200',
	    -GLOBAL_DATAFILES_DIRECTORY         => $GLOBAL_DATAFILES_DIRECTORY,
	    -TEMPLATES_CACHE_DIRECTORY          => $TEMPLATES_CACHE_DIRECTORY,
	    -APP_DATAFILES_DIRECTORY            => $APP_DATAFILES_DIRECTORY,
	    -DATASOURCE_TYPE                    => $datesourcetype,
       -AUTH_TABLE                         => $AUTH_TABLE,
 	    -PRODUCT_DATASOURCE_CONFIG_PARAMS   => \@PRODUCT_DATASOURCE_CONFIG_PARAMS,
       -URL_DATASOURCE_CONFIG_PARAMS       => \@URL_DATASOURCE_CONFIG_PARAMS,
       -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS,
 	    -ADDITIONALAUTHUSERNAMECOMMENTS     => 'Please do not use spaces.',
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
