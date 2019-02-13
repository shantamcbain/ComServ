package universalSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME                 => 'PageView',
	    -HOME_VIEW                      => 'PageView',
	    -BASIC_DATA_VIEW                => 'BasicDataView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -APP_LOGO                       => 'http://d2earth.com/images/d2b2.gif',
	    -APP_LOGO_ALT                   => 'd2earth Logo',
	    -APP_LOGO_WIDTH                 => '150',
	    -APP_LOGO_HEIGHT                => '80',
	    -CSS_VIEW_NAME                  => '/styles/universalCSSView.css',
            -DEFAULT_CHARSET                => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL              => '/',
	    -TEMPLATES_CACHE_DIRECTORY      => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY        => "../../Datafiles/CSC",
	    -GLOBAL_DATAFILES_DIRECTORY     => "../../Datafiles",
            -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL                 => 'http://forager.com/images/extropia',
	    -LEFT_PAGE_VIEW                 => 'LeftPageView',
            -LINK_TARGET                    => '_self',
	    -MAIL_FROM                      => 'universal@forager.com',
	    -MAIL_TO                        => 'universal@forager.com',
	    -MAIL_TO_ADMIN                  => 'sysadmin@computersystemconsulting.ca',
	    -MAIL_TO_USER                   => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT                 => 'csc_client@computersystemconsulting.ca',

	    -MAIL_REPLYTO                   => 'csc@computersystemconsulting.ca',
	    -PAGE_TOP_VIEW                  => 'PageTopView',
	    -PAGE_BOTTOM_VIEW               => 'PageBottomView',
	    -PAGE_LEFT_VIEW                 => 'LeftPageView',
	    -SESSION_TIME_OUT               => 60 * 60 * 2,
	    -DATASOURCE_TYPE                => $datesourcetype,
            -AUTH_TABLE                     => 'universal_user_auth_tb',
            -HTTP_HEADER_PARAMS             => "[-EXPIRES => '-1d']",
            -HTTP_HEADER_DESCRIPTION        => " Universal forager",
            -HTTP_HEADER_KEYWORDS           => "Foraging, scrap removeal, we will find it for you",
	    
	   
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
