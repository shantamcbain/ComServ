package AltPowerSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#my $datesourcetype = 'MySQL';
my $datesourcetype = 'file';

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;
my %VALID_FORUMS = (
       altpowernews          =>  'Announcements',
       wind                  =>  'wind',
       batteries             =>  'Batteries',
       solar                 =>  'solar',
       general               =>  'General Topics',
       equipment             =>  'Equipment',
       hydro                 =>  'Water power',
       water                 =>  'Water pumping',
       rv                    =>  'Mobile and marine',
       winter                =>  'Wintering',
                                );

my $self = {-HOME_VIEW_NAME                 => 'OrganicHome',
	    -AFFILIATE           => '13',
	    -PID                 => '117',
       -SITE_DISPLAY_NAME => "Alternate and Sustainable Power",            

       -SITE_LAST_UPDATE  => 'Nov 22, 2018 ',
	    -HOME_VIEW                      => 'HomeView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
	    -APP_LOGO                       => '',
	    -APP_LOGO_ALT                   => 'AltPower Logo',
	    -APP_LOGO_WIDTH                 => '0',
	    -APP_LOGO_HEIGHT                => '0',
	    -CSS_VIEW_NAME                  => '/styles/AltPowerCSSView.css',
        -DEFAULT_CHARSET                => 'ISO-8859-1', 
	    -PAGE_TOP_VIEW                  => 'PageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -MAIL_FROM                      => 'altpower@usbm.ca',
	    -MAIL_TO                        => 'altpower@usbm.ca',
	    -MAIL_REPLYTO                   => 'altpower@forager.com',
	    -MAIL_TO_USER                   => 'altpower_user_list@usbm.ca',
	    -MAIL_TO_DISCUSSION             => 'altpower_discussion@usbm.ca',
	    -DOCUMENT_ROOT_URL              => '/',
	    -IMAGE_ROOT_URL                 => '/images/extropia',
       -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION        => "AltPower is an application to help you run your alternate power system ",
       -HTTP_HEADER_KEYWORDS           => "AltPower, Hydro power, wind power, solar power, Tesla, ",
	    -DATASOURCE_TYPE                => $datesourcetype,
       -AUTH_TABLE                     => 'altpower_user_auth_tb',
  	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY        => "../../Datafiles/AltPower",
	    -VALID_FORUMS                   => (
                                ) ,
       altpowernews          =>  'Announcements',
       wind                  =>  'wind',
       batteries             =>  'Batteries',
       solar                 =>  'solar',
       general               =>  'General Topics',
       equipment             =>  'Equipment',
       hydro                 =>  'Water power',
       water                 =>  'Water pumping',
       rv                    =>  'Mobile and marine',
       winter                =>  'Wintering',

	    };


return bless $self, $package; 
}






1;
