package SiteSetup;


use strict;
use CGI::Carp qw(fatalsToBrowser);
# $site = 'file';
#Create local Variable for use here only

# $datasourcetype = 'file';
my $datesourcetype = 'MySQL';
#my $datesourcetype = 'file';


sub new {
my $package    = shift;
my $UseModPerl = shift || 1;

# This is where you define your variable mapping.
my $self = {-SITE_NAME         => 'CSCDev',
            -AFFILIATE         => '001',
            -HOME_VIEW_NAME    => 'HomeView',
	    -HOME_VIEW         => 'BasicDataView',
	    -LAST_UPDATE       => 'Febuary, 2012',
       -LOCAL_IP          => '174.120.175.42',
	    -BASIC_DATA_VIEW   => 'BasicDataView',
	    -APP_LOGO          => '../csc/cscsmall.gif',
	    -APP_LOGO_ALT      => 'CSC Logo',
	    -APP_LOGO_WIDTH    => '108',
	    -APP_LOGO_HEIGHT   => '40',
	    -FAVICON           => '/favicon.ico',
	    -ANI_FAVICON       => '/animated_favicon.gif',
	    -FAVICON_TYPE      => '/image/x-icon',
	    -CSS_VIEW_NAME     => '/styles/CSSView.css',
	    -PAGE_TOP_VIEW     => 'PageTopView',
	    -PAGE_BOTTOM_VIEW  => 'PageBottomView',
	    -PAGE_LEFT_VIEW    => 'LeftPageView',
	    -MAIL_TO_ADMIN     => 'webmaster@computersystemconsulting.ca',
	    -MAIL_FROM         => 'webmaster@computersystemconsulting.ca',
	    -MAIL_TO_AUTH      => 'csc@computersystemconsuting.ca',
	    -MAIL_TO           => 'webmaster@computersystemconsulting.ca',
		 -MAIL_FROM_HELPDESK => 'helpdesk@computersystemconsulting.ca',
       -MAIL_REPLYTO      => 'webmaster@computersystemconsulting.ca',
	    -DOCUMENT_ROOT_URL => '/',
	    -IMAGE_ROOT_URL    => '/images/extropia',
	    -GLOBAL_DATAFILES_DIRECTORY => "/home/shanta/Datafiles/",
	    -APP_DATAFILES_DIRECTORY    => "/home/shanta/Datafiles/",
	    -TEMPLATES_CACHE_DIRECTORY  => '/TemplatesCache',
       -LINK_TARGET       => '_self',
       -HTTP_HEADER_PARAMS => "[-EXPIRES => '-1d']",
	    -DATASOURCE_TYPE   => $datesourcetype,      
       -DBI_DSN           => 'mysql:database=shanta_forager',
       -DBI_DSN_STORES    => 'mysql:database=forager',
       -MySQLPW           => 'UA=nPF8*m+T#',
       -AUTH_TABLE        => 'csc_user_auth_tb',
       -AUTH_MSQL_USER_NAME => 'shanta_forager',
       -DEFAULT_CHARSET   => 'ISO-8859-1', 
       -CAL_TABLE         => 'cal_event',
       -HTTP_HEADER_DESCRIPTION => "forager.com, computersystemconsulting.ca, webcthelpdesk.com, organicfarming.ca, shanta.org",
       -HTTP_HEADER_KEYWORDS    => "eXtropia HelpDesk,eXtropia, HelpDesk,Web applications, Application hosting, hosting, support,shanta mcbain, shanta, McBain, csps, organic farming, bee keeping, beekeeping ",
       -VALID_VIEWS             =>  "
          ApisCSSView
          BCHPACSSView
          ECFCSSView
          OrganicCSSView

          DetailsRecordView
       BasicDataView
       InventoryBasicDataView

       AddRecordView
       AddRecordConfirmationView
       AddAcknowledgementView

       DeleteRecordConfirmationView
       DeleteAcknowledgementView
       LinkListView

       ModifyRecordView
       ModifyRecordConfirmationView
       ModifyAcknowledgementView

       PowerSearchFormView
       OptionsView
       LogoffView

       TelMarkHomeView
       ApisProductView
       ApisPolinatorsView
       MiteGoneDocsView
       ApisHoneyView
       CertifiedOrganicView
       AssociateView
       MGWaverView 
       ForumsView

       BCHPAHomeView
       BCHPAAdminHomeView
       BeeTrustView
       BCHPAByLawsView
       BCHPAContactView
       BCHPABoardView
       BCHPAMemberView
       BCHPAPolinatorsView

       ECFHomeView
       ECFSideBarHomeView
       PrintView
       AppToolsView
       ContactView
       ForageIndicatorView
       PollinatorSQLView
       InventoryHomeView
       ItemView
       InventoryProjectionView
       InventoryView
       InventorySQLView
       SQLView
        OrganicProductView
       ContactView
       InventoryProjectionView
       WeatherView
       PrivacyView
       AdventureDiaryView
       ",
    
	    };
#'pwxx88',

#return your variables to the aplication file.
return bless $self, $package; 
}

1;