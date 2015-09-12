package SkySetup;
#ver 1.01
# 	$Id: SkySetup.pm,v 1.1 2003/11/29 06:43:31 shanta Exp shanta $	

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

my $self = {
       -HOME_VIEW_NAME                 => 'SkyHome',
	    -HOME_VIEW                      => 'HomeView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
	    -APP_LOGO                       => 'http://organicfarming.ca/images/sky/skylogo.gif',
	    -APP_LOGO_ALT                   => 'Skye Logo',
	    -APP_LOGO_WIDTH                 => '300',
	    -APP_LOGO_HEIGHT                => '125',
	    -CSS_VIEW_NAME                  => '/styles/SkyCSSView.css',
       -DEFAULT_CHARSET                => 'ISO-8859-1',
	    -PAGE_TOP_VIEW                  => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -MAIL_FROM                      => 'skyfarm@organicfarming.ca',
	    -MAIL_TO                        => 'skyefarm@organicfarming.ca',
	    -MAIL_REPLYTO                   => 'sky@forager.com',
	    -MAIL_TO_USER                   => 'orgnic_user_list@organicfarming.ca',
	    -MAIL_TO_DISCUSSION             => 'organic_discussion@organicframing.ca',
	    -SITE_DISPLAY_NAME              => 'Skye Farm: Organics at is best.',
	    -DOCUMENT_ROOT_URL              => '/',
	    -IMAGE_ROOT_URL                 => 'http://shanta.org/images/extropia',
       -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION        => "Organic Farming is an application to help you run your organic farm ",
       -HTTP_HEADER_KEYWORDS           => "Organic, Organic Farming, organic honey, Herbs¸ Butternut Squash, Onions, garlic, corn, Potatos, leeks, pumkin, squash, spelt, red clover, white clover, chamomile, carrots, ",
	    -DATASOURCE_TYPE                => $datesourcetype,
       -AUTH_TABLE                     => 'organic_user_auth_tb',
       -AUTH_MSQL_USER_NAME            => 'forager',
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
                                ) 

	    };


return bless $self, $package; 
}






1;
