package OrganicSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;
my %VALID_FORUMS = (
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
                                );

my $self = {-HOME_VIEW_NAME                 => 'OrganicHome',
	    -AFFILIATE           => '13',
	    -PID                 => '126',
	    -HOME_VIEW                      => 'OrganicHomeView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
       -SITE_LAST_UPDATE           => 'December 16, 2006',
	    -APP_LOGO                       => '/images/apis/bee.gif',
	    -APP_LOGO_ALT                   => 'apis Logo',
	    -APP_LOGO_WIDTH                 => '60',
	    -APP_LOGO_HEIGHT                => '60',
	    -CSS_VIEW_NAME                  => '/styles/OrganicCSSView.css',
       -DEFAULT_CHARSET                => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW                  => 'PageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -MAIL_FROM                      => 'apis@shanta.org',
	    -MAIL_TO                        => 'organic@shanta.org',
	    -MAIL_REPLYTO                   => 'organic@forager.com',
	    -MAIL_TO_USER                   => 'orgnic_user_list@forager.com',
	    -MAIL_TO_DISCUSSION             => 'organic_discussion@forager.com',
	    -MAIL_LIST_BCC                  => 'homestead_small_farming_exchange@yahoogroups.com',
	    -DOCUMENT_ROOT_URL              => '/',
	    -IMAGE_ROOT_URL                 => 'http://shanta.org/images/extropia',
            -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION        => "Organic Farming is an application to help you run your organic farm ",
            -HTTP_HEADER_KEYWORDS           => "Organic, Organic Farming, organic honey, Herbs, Organic Beekeeping, organic beebreeding, Small Cell Beekeeping.",
	    -DATASOURCE_TYPE                => $datesourcetype,
       -SITE_DISPLAY_NAME              => 'Organic Farming.ca',
       -AUTH_TABLE                     => 'organic_user_auth_tb',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY        => "../../Datafiles/Organic",
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
       HelpDesk           =>  'System HelpDesk',
                               ) ,

	    };


return bless $self, $package; 
}






1;
