package VitalVicSetup;
# 	$Id: organic.cgi,v 1.1 2003/11/29 06:30:04 shanta Exp shanta $


use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Variable for use here only
# $site = 'file';
my $site = 'MySQL';


sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME    => 'VitalVicHomeView',
	    -HOME_VIEW         => 'VitalVicHomeView',
	    -MySQLPW           => '!herbsRox!',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => 'http://shanta.org/images/apis/bee.gif',
	    -APP_LOGO_ALT      => 'Vital Victoria Logo',
	    -APP_LOGO_WIDTH    => '80',
	    -APP_LOGO_HEIGHT   => '80',
            -AUTH_TABLE        => 'vitalvic_user_auth_tb',
	    -CSS_VIEW_NAME     => '/styles/VitalVicCSSView.css',
	    -PAGE_TOP_VIEW     => 'templatePageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -LEFT_PAGE_VIEW    => 'LeftPageView',
	    -MAIL_FROM         => 'VitalVicOffice@computersystemconsulting.ca',
	    -MAIL_TO           => 'vitalvicadmin@computersystemconsulting.ca',
	    -MAIL_REPLYTO      => 'VitalVicOffice@computersystemconsulting.ca',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => 'http://forager.com/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "../../Datafiles",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
	    -APP_DATAFILES_DIRECTORY => "../../Datafiles/Todo",
	    -DATASOURCE_TYPE   => $site,
            -HTTP_HEADER_DESCRIPTION => "Vital Victoria, Dr Neil McKinney",
            -HTTP_HEADER_KEYWORDS    => "health, herbs, herbalogy, ENCY, apis theropys, homiopothy, alternate healing, integrated health management, nutrition, VitaVic, Vital Victoria, Dr Neil McKinney, accupunture, Chinese medicine, oncology, cancer,  ",
	    };

#return your variables to the application file.
return bless $self, $package; 
}

1;
