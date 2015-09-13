package ForagerSetup;

# 	$Id: ForagerSetup.pm,v 1.1 2003/11/29 06:35:52 shanta Exp shanta $	

use strict;
use CGI::Carp qw(fatalsToBrowser);
#Create local Varible for use here only
# $datasourcetype = 'file';
my $datesourcetype               = 'MySQL';
my $DBI_DSN                      = 'mysql:host=localhost;database=forager';
my $MySQLPW                      = '!herbsRox!';
my $AUTH_TABLE                   = 'forager_user_auth_tb';
my $AUTH_MSQL_USER_NAME          = 'forager';
my $site                         = 'MySQL';
my $GLOBAL_DATAFILES_DIRECTORY   = "/home/forager/Datafiles"||'BLANK';
my $TEMPLATES_CACHE_DIRECTORY    = $GLOBAL_DATAFILES_DIRECTORY.'/TemplatesCache';
my $APP_DATAFILES_DIRECTORY      = "/home/forager/Datafiles/CSC";
my $DATAFILES_DIRECTORY          = $APP_DATAFILES_DIRECTORY;
my $site_session                 = $DATAFILES_DIRECTORY.'/Sessions';
my $auth                         = $DATAFILES_DIRECTORY.'/csc.admin.users.dat';

my @AUTH_USER_DATASOURCE_FIELD_NAMES = qw(
    username
    password
    groups
    firstname
    lastname
    email
    developer_status
);

my @AUTH_USER_DATASOURCE_PARAMS;
if ($site eq "file") {

	@AUTH_USER_DATASOURCE_PARAMS = (
	    -TYPE                       => 'File',
	    -FIELD_DELIMITER            => '|',
	    -CREATE_FILE_IF_NONE_EXISTS => 1,
	    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
	    -FILE                       => $auth
	);
}
else {

   @AUTH_USER_DATASOURCE_PARAMS = (
        -TYPE         => 'DBI',
        -DBI_DSN      => $DBI_DSN,
        -TABLE        => $AUTH_TABLE,
        -USERNAME     => $AUTH_MSQL_USER_NAME,
        -PASSWORD     => $MySQLPW,
        -FIELD_NAMES  => \@AUTH_USER_DATASOURCE_FIELD_NAMES
    );
}
my @PRODUCT_DATASOURCE_FIELD_NAMES = 
    qw(
 ProductID CategoryID DiscountID ProductPrice ProductTaxable 
 ManufacturerID AuthorID ManufacturerPID
 ProductShortDescriptionENG ProductShortDescriptionGER 
 ProductLongDescriptionENG ProductLongDescriptionGER
 ProductImageURL ProductImageThmbURL ProductAssociateLink 
 ProductOptions ProductDeliveryMethod ProductDownloadData
 ProductShipsIndividually ProductPackingFactor 
 ProductMinimumOrder ProductMaximumOrder ProductExpires 
 ProductDisabled ProductWeight ReleaseDate
);
my	@PRODUCT_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'File',
                -FILE         => '/cgi-bin/store/shops/csc/Data_files/',
                -FIELD_DELIMITER => '|',
                -COMMENT_PREFIX  => '#',
                -CREATE_FILE_IF_NONE_EXISTS => 1,
	        -FIELD_NAMES     => \@PRODUCT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
                                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
	        },
	);

my @URL_DATASOURCE_FIELD_NAMES = 
    qw(
       record_id
       owner
       category
       subject
       share
       name 
       description
       url
       last_mod_by
       last_mod_date
       comments        
      );

my @URL_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'url_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@URL_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
	        },
	);

sub new {
my $package    = shift;
my $UseModPerl = shift || 0;

# This is where you define your variable mapping.
my $self = {-HOME_VIEW_NAME                => 'HomeView',
       -SITE_LAST_UPDATE                   => 'January 19,  2012',
	    -HOME_VIEW                     => 'PageView',
       -SITE_DISPLAY_NAME                  => 'Forager',
	    -BASIC_DATA_VIEW               => 'BasicDataView',
	    -APP_NAME_TITLE                => 'around the world',
	    -APP_LOGO                           => '/images/forager/foragericon.gif',
	    -APP_LOGO_ALT                       => 'Forager Logo',
	    -APP_LOGO_WIDTH                     => '108',
	    -APP_LOGO_HEIGHT                    => '108',
	    -CSS_VIEW_NAME                      => '/styles/ForagerCSSView.css',
       -DEFAULT_CHARSET                    => 'ISO-8859-1', 
	    -DOCUMENT_ROOT_URL                  => '/',
       -HTTP_HEADER_PARAMS                 => "[-EXPIRES => '-1d']",
       -HTTP_HEADER_DESCRIPTION            => "Foragers have been scouring the world for the entire history of man. Join us in the adventure. 
                                   ",
       -HTTP_HEADER_KEYWORDS               => "foraging, forager, herbs, metal, wood, Firewood, food, building materials.
            ",
	    -IMAGE_ROOT_URL                     => 'http://forager.com/images/extropia',
	    -LEFT_PAGE_VIEW                     => 'LeftPageView',
       -LINK_TARGET                        => '_self',
	    -MAIL_FROM                          => 'forager@forager.com',
	    -MAIL_TO_AMIN                       => 'admin@computersystemconsulting.ca',
	    -MAIL_TO                            => 'forager.com@forager.com',
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
