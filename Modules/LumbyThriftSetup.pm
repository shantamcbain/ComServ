package LumbyThriftSetup;


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

my $self = {-HOME_VIEW_NAME            => 'PageView',
	    -HOME_VIEW                      => 'PageView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
	    -APP_LOGO                       => '/images/apis/bee.gif',
	    -APP_LOGO_ALT                   => 'Lumby Thrift Store Logo',
	    -APP_LOGO_WIDTH                 => '60',
	    -APP_LOGO_HEIGHT                => '60',
	    -CSS_VIEW_NAME                  => '/styles/LumbyThrift.css',
       -DEFAULT_CHARSET                => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW                  => 'PageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -MAIL_FROM                      => 'lumbythrift@countrystores.ca',
	    -MAIL_TO                        => 'lumbythrift@countrystores.ca',
	    -MAIL_REPLYTO                   => 'lumbythrift@countrystores.ca',
	    -MAIL_TO_USER                   => 'lumbythrift@countrystores.ca',
	    -MAIL_TO_DISCUSSION             => 'organic_discussion@forager.com',
	    -MAIL_LIST_BCC                  => '',
	    -DOCUMENT_ROOT_URL              => '/',
	    -IMAGE_ROOT_URL                 => '/images/extropia',
       -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION        => "Lumby Thrift Store.",
       -HTTP_HEADER_KEYWORDS           => "Lumby, Thrift store",
	    -DATASOURCE_TYPE                => $datesourcetype,
       -SITE_DISPLAY_NAME              => 'Lumby Thrift Store',
       -AUTH_TABLE                     => 'lumbythrift_user_auth_tb',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY        => "../../Datafiles/LumbyThrift",
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
