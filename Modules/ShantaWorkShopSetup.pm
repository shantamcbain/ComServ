package ShantaWorkShopSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $site = 'file';
my $site = 'MySQL';
my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {
       -Site_Last_Update  => 'February, 2022',
  	    -AFFILIATE           => '2',
	    -PID                 => '122',
       -HOME_VIEW_NAME    => 'HomeView',
	    -HOME_VIEW         => 'HomeView',
 	    -ADDITIONALAUTHUSERNAMECOMMENTS => 'Please do not use spaces.',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '/images/shanta/shantasmall.gif',
	    -APP_LOGO_ALT      => 'Shantasworkshop Logo',
	    -APP_LOGO_WIDTH    => '100',
	    -APP_LOGO_HEIGHT   => '100',
	    -CSS_VIEW_NAME     => '/styles/ShantaCSSView.css',
       -DEFAULT_CHARSET   => 'ISO-8859-1',
	    -DOCUMENT_ROOT_URL => '/',
	    -GLOBAL_DATAFILES_DIRECTORY => "/home/shanta/Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "/home/shanta/Datafiles",
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -MAIL_FROM         => 'shanta@shanasworkshop.grindrodbc.com',
	    -MAIL_TO           => 'shanta@shantasworkshop.grindrodbc.com',
	    -MAIL_TO_ADMIN      => 'sysadmin@computersystemconsulting.ca',
	    -MAIL_TO_USER      => 'csc_user_list@computersystemconsulting.ca',
	    -MAIL_TO_CLIENT    => 'csc_client@computersystemconsulting.ca',
	    -MAIL_REPLYTO      => 'shanta@shantasworkshop.grindrodbc.com',
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => '',
	    -LEFT_PAGE_VIEW    => '',
       -LINK_TARGET       => '_self',
	    -DATASOURCE_TYPE   => $site,
       -AUTH_TABLE        => 'shanta_user_auth_tb',
       -AUTH_MSQL_USER_NAME => 'forager',
       -HTTP_HEADER_DESCRIPTION => "Shanta Workshop. Fine woodworking",
       -HTTP_HEADER_KEYWORDS    => "Woodworking, woodworking workshops. wooden toys.    ",
	    -VALID_FORUMS                   => (
            HelpDesk           =>  'System HelpDesk',
 	         ) ,

 };

#return your variables to the application file.
return bless $self, $package; 
}

1;
