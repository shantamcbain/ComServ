package EVSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;
my %VALID_FORUMS = (
       herbs                 =>  'Herbs in general',
       pandanimalbreeding    =>  'Breeding and genetics',
       diseases              =>  'Diseases and pests',
       farmtech              =>  'Farming Technics',
       general               =>  'General Topics',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       pollination           =>  'Pollination',
       seed                  =>  'Seed and seed saving',
       winter                =>  'Wintering',
                                );

my $self = {-HOME_VIEW_NAME                 => 'EVHome',
	    -HOME_VIEW                      => 'EVHomeView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
	    -APP_LOGO                       => 'http://shanta.org/images/apis/bee.gif',
	    -APP_LOGO_ALT                   => 'apis Logo',
	    -APP_LOGO_WIDTH                 => '60',
	    -APP_LOGO_HEIGHT                => '60',
	    -CSS_VIEW_NAME                  => '/styles/EVCSSView.css',
            -DEFAULT_CHARSET                => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW                  => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -MAIL_FROM                      => 'apis@shanta.org',
	    -MAIL_TO                        => 'ev@shanta.org',
	    -MAIL_REPLYTO                   => 'ev@forager.com',
	    -MAIL_TO_USER                   => 'ev_user_list@forager.com',
	    -MAIL_TO_DISCUSSION             => 'forager_discussion@forager.com',
	    -DOCUMENT_ROOT_URL              => '/',
	    -IMAGE_ROOT_URL                 => 'http://shanta.org/images/extropia',
            -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION        => "Organic Farming is an application to help you run your organic farm ",
            -HTTP_HEADER_KEYWORDS           => "Organic, Organic Farming, organic honey, Herbs ",
	    -DATASOURCE_TYPE                => $datesourcetype,
            -DBI_DSN                        => 'mysql:host=localhost;database=forager',
	    -MySQLPW                        => '!herbsRox!',
            -AUTH_TABLE                     => 'ev_user_auth_tb',
            -AUTH_MSQL_USER_NAME            => 'forager',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY        => "../../Datafiles/EV",
	    -VALID_FORUMS                   => (
       organicnews           =>  'Announcements',
       pandanimalbreeding    =>  'Breeding and genetics',
       diseases              =>  'Diseases and pests',
       farmtech              =>  'Farming Technics',
       general               =>  'General Topics',
       honey                 =>  'Honey',
       organic               =>  'Organic',
       pollination           =>  'Pollination',
       seed                  =>  'Seed and seed saving',
       winter                =>  'Wintering',
                                ) ,

	    };


return bless $self, $package; 
}






1;
