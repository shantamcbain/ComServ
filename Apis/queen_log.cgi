#!/usr/bin/perl -wT
# 	$Id: queen_log.cgi,v 1.91 2020/03/10 21:26:43 shanta Exp shanta $	
# 	$Id: queen_log.cgi,v 1.9 2020/03/10 21:26:43 shanta Exp shanta $	
# 	$Id: queen_log.cgi,v 1.8 2002/11/03 21:26:43 shanta Exp shanta $	
#CSC file location /cgi-bin/CSC
# Copyright (C) 1994 - 2001  eXtropia.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, 
# Boston, MA  02111-1307, USA.

use strict;
my $AppVer = "ver 0.02, April 4, 2022";
BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules/
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];


my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default);

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/Apis
        ../HTMLTemplates/CSC
       ../HTMLTemplates/ECF
       ../HTMLTemplates/ENCY
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Todo
       ../HTMLTemplates/Default);

use CGI qw(-debug);

#Carp commented out due to Perl 5.60 bug. Uncomment when using Perl 5.61.
#use CGI::Carp qw(fatalsToBrowser);

use Extropia::Core::App::DBApp;
use Extropia::Core::View;
use Extropia::Core::Action;
use Extropia::Core::SessionManager;

my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");

foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x$/);
}
######################################################################
#                          SITE SETUP                             #
######################################################################
my $additonalautusernamecomments;
my $Affiliate = 001;
my $APP_NAME = "queen_log";     
    my $APP_NAME_TITLE =  "Queen log";
my $CustCode = $CGI->param('custcode') || "BMaster";
    my $DEFAULT_CHARSET;
    my $HasMembers = 0;
my $HostName   = $ENV{'SERVER_NAME'};
my $OffLine    = 'yes';
my $Page           = $CGI->param('page');
my $procedure      = $CGI->param('procedure');
my $project        = $CGI->param('project');
    my $QueenCode      = $CGI->param('queen_code');
    my $QueenRecordID      = $CGI->param('record_id');
my $style = $CGI->param('pagestyle');
my $title          = $CGI->param('title');
my $View           = $CGI->param('view') ;

use SiteSetup;
#my $S   = &CSCSetup::SiteVariables;
my $UseModPerl = 1;
my $SetupVariables  = new SiteSetup($UseModPerl);
my $app_logo              = $SetupVariables->{-APP_LOGO};
my $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
my  $APP_NAME_TITLE          = $SetupVariables->{-APP_NAME_TITLE};
my $app_logo_height       = $SetupVariables->{-APP_LOGO_HEIGHT};
my $app_logo_width        = $SetupVariables->{-APP_LOGO_WIDTH};
my $app_logo_alt          = $SetupVariables->{-APP_LOGO_ALT};
my  $AUTH_TABLE            = $SetupVariables->{-AUTH_TABLE};
my $AUTH_MSQL_USER_NAME   = $SetupVariables->{-AUTH_MSQL_USER_NAME};
my $BASIC_DATA_VIEW       = $SetupVariables->{-BASIC_DATA_VIEW};
my $CSS_VIEW_NAME         = $SetupVariables->{-CSS_VIEW_NAME};
my $CSS_VIEW_URL  = $SetupVariables->{-CSS_VIEW_NAME};
my $DBI_DSN               = $SetupVariables->{-DBI_DSN};
my $DEFAULT_CHARSET       = $SetupVariables->{-DEFAULT_CHARSET};
my $DOCUMENT_ROOT_URL     = $SetupVariables->{-DOCUMENT_ROOT_URL};
my $FAVICON                 = $SetupVariables->{-FAVICON};
my $ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
my $FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
my $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
my $HeaderImage             = $SetupVariables->{-HEADER_IMAGE};
my $Header_height           = $SetupVariables->{-HEADER_HEIGHT};
my $Header_width            = $SetupVariables->{-HEADER_WIDTH};
my $Header_alt              = $SetupVariables->{-HEADER_ALT};
my $HasMembers              = $SetupVariables->{-HAS_MEMBERS};
my $home_view             = 'ApisQueenLogView'||$SetupVariables->{-HOME_VIEW}; 
my $homeviewname            = 'ApisQueenLogView'||$SetupVariables->{-HOME_VIEW_NAME};
my $HTTP_HEADER_PARAMS       = $SetupVariables->{-HTTP_HEADER_PARAMS};
my $HTTP_HEADER_KEYWORDS     = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
my $HTTP_HEADER_DESCRIPTION  = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
#Mail settings
my $IMAGE_ROOT_URL          = $SetupVariables->{-IMAGE_ROOT_URL};
my $last_update             = $SetupVariables->{-LAST_UPDATE};
my $LineStatus              = $SetupVariables->{-Line_Status};
my $LINK_TARGET             = $SetupVariables->{-LINK_TARGET};
my $LocalIp              = $SetupVariables->{-LOCAL_IP};
my $last_update             = $SetupVariables->{-LAST_UPDATE};
my $LINK_TARGET             = $SetupVariables->{-LINK_TARGET};
my $LocalIp              = $SetupVariables->{-LOCAL_IP};
my $mail_from             = $SetupVariables->{-MAIL_FROM}; 
my $mail_to               = $SetupVariables->{-MAIL_TO};
my $mail_replyto          = $SetupVariables->{-MAIL_REPLYTO};
my $mail_to_user         = $SetupVariables->{-MAIL_USER};
my $mail_to_member       = $SetupVariables->{-MAIL_MEMBER};
my $mail_to_discussion   = $SetupVariables->{-MAIL_DISCUSSION};
my $MySQLPW               = $SetupVariables->{-MySQLPW};
my $NEWS_TB               = $SetupVariables->{-NewsTable};
my $page_top_view         = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
my $page_bottom_view      = $SetupVariables->{-PAGE_BOTTOM_VIEW};
my $left_page_view        = $SetupVariables->{-LEFT_PAGE_VIEW};
my $Page_tb                 = $SetupVariables->{-PAGE_TB} || 'page_tb';
my $pid                     = $SetupVariables->{-PID};
my $site                    = $SetupVariables->{-DATASOURCE_TYPE};
my $SITE_DISPLAY_NAME          = $SetupVariables->{-SITE_DISPLAY_NAME};
my $SiteName =  $CGI->param('site') || "CSC";
my $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
my $site = $SetupVariables->{-DATASOURCE_TYPE};
my $site_session = $GLOBAL_DATAFILES_DIRECTORY.'/Sessions';
my $site_update             = $SetupVariables->{-SITE_LAST_UPDATE};
my $shop                    = $SetupVariables->{-SHOP};
my $StoreUrl                = $SetupVariables->{-STORE_URL};
my $TEMPLATES_CACHE_DIRECTORY = $GLOBAL_DATAFILES_DIRECTORY . $SetupVariables->{ -TEMPLATES_CACHE_DIRECTORY, };

my $auth = $GLOBAL_DATAFILES_DIRECTORY.'/csc.admin.users.dat';

#use CSCSetup;

my $VIEW_LOADER = new Extropia::Core::View
    (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60 * 2,
    -SESSION_DIR     => "$GLOBAL_DATAFILES_DIRECTORY/Sessions",
    -FATAL_TIMEOUT   => 0,
    -FATAL_SESSION_NOT_FOUND => 1
);

######################################################################
#                     SESSION MANAGER SETUP                          #
######################################################################

my @SESSION_MANAGER_CONFIG_PARAMS = (
    -TYPE           => 'FormVar',
    -CGI_OBJECT     => $CGI,
    -SESSION_PARAMS => \@SESSION_CONFIG_PARAMS
);

my $SESSION_MGR = Extropia::Core::SessionManager->create(
    @SESSION_MANAGER_CONFIG_PARAMS
);

my $SESSION    = $SESSION_MGR->createSession();
my $SESSION_ID = $SESSION->getId();

if ($CGI->param('site')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'SiteName') ){
      $SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $CGI->param('site')) ;
       $SiteName = $CGI->param('site');
    }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'SiteName')) {
    $SiteName = $SESSION ->getAttribute(-KEY => 'SiteName');
  }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
      }
}
if ($CGI->param('site')){
    if  ($CGI->param('site') ne $SESSION ->getAttribute(-KEY => 'SiteName') ){
      $SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $CGI->param('site')) ;
       $SiteName = $CGI->param('site');
    }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'SiteName')) {
    $SiteName = $SESSION ->getAttribute(-KEY => 'SiteName');
  }else {
	$SESSION ->setAttribute(-KEY => 'SiteName', -VALUE => $SiteName );
      }
}
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_groups');
my $group    =  $SESSION ->getAttribute(-KEY => 'auth_group');

######################################################################
#                       AUTHENTICATION SETUP                         #
######################################################################

my @AUTH_USER_DATASOURCE_FIELD_NAMES = qw(
    username
    password
    groups
    firstname
    lastname
    email
);
my @AUTH_USER_DATASOURCE_PARAMS;
if ($site eq "file") {

	@AUTH_USER_DATASOURCE_PARAMS = (
	    -TYPE                       => 'File',
	    -FIELD_DELIMITER            => '|',
	    -CREATE_FILE_IF_NONE_EXISTS => 1,
	    -FIELD_NAMES                => \@AUTH_USER_DATASOURCE_FIELD_NAMES,
	    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.users.dat"
	);
}
else {

   @AUTH_USER_DATASOURCE_PARAMS = (
        -TYPE         => 'DBI',
        -DBI_DSN      => $DBI_DSN,
        -TABLE        => 'csc_user_auth_tb',
        -USERNAME     => $AUTH_MSQL_USER_NAME,
        -PASSWORD     => $MySQLPW,
        -FIELD_NAMES  => \@AUTH_USER_DATASOURCE_FIELD_NAMES
    );
}


my @AUTH_ENCRYPT_PARAMS = (
    -TYPE => 'Crypt'
);

my %USER_FIELDS_TO_DATASOURCE_MAPPING = (
    'auth_username'  => 'username',
    'auth_password'  => 'password',
    'auth_firstname' => 'firstname',
    'auth_lastname'  => 'lastname',
    'auth_groups'    => 'groups',
    'auth_email'     => 'email'
);

my @AUTH_CACHE_PARAMS = (
    -TYPE           => 'Session',
    -SESSION_OBJECT => $SESSION
);

my @AUTH_CONFIG_PARAMS = (
    -TYPE                                => 'DataSource',
    -USER_DATASOURCE_PARAMS              => \@AUTH_USER_DATASOURCE_PARAMS,
    -ENCRYPT_PARAMS                      => \@AUTH_ENCRYPT_PARAMS,
    -ADD_REGISTRATION_TO_USER_DATASOURCE => 1,
    -USER_FIELDS_TO_DATASOURCE_MAPPING   => \%USER_FIELDS_TO_DATASOURCE_MAPPING,
    -AUTH_CACHE_PARAMS                   => \@AUTH_CACHE_PARAMS
);

######################################################################
#                 AUTHENTICATION MANAGER SETUP                       #
######################################################################

my @AUTH_VIEW_DISPLAY_PARAMS = (
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $app_logo_alt,
    -HTTP_HEADER_PARAMS      => [-EXPIRES => '-1d'],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SITE_NAME               => $SiteName,
    -PAGE_TOP_VIEW           => $page_top_view,
    -PAGE_BOTTOM_VIEW        => $page_bottom_view,
    -LINK_TARGET             => '_self'
);

my @AUTH_REGISTRATION_DH_MANAGER_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,
    -DATAHANDLERS => [qw(
        Email
        Exists
    )],
    
    -FIELD_MAPPINGS => {
                'auth_username'     => 'Username',
                'auth_password'     => 'Password',
                'auth_password2'    => 'Confirm Password',
                'auth_firstname'    => 'First Name',
                'auth_lastname'     => 'Last Name',
                'auth_email'        => 'E-Mail Address'
        },
  
        -IS_FILLED_IN => [qw(
                auth_username
                auth_firstname
                auth_lastname
                auth_email
        )],
    
        -IS_EMAIL => [qw(
                auth_email
        )]
);
    
my @USER_FIELDS = (qw(
    auth_username
    auth_password
    auth_groups
    auth_firstname
    auth_lastname
    auth_email
));

my %USER_FIELD_NAME_MAPPINGS = (
    'auth_username'  => 'Username',
    'auth_password'  => 'Password',
    'auth_groups'    => 'Groups',
    'auth_firstname' => 'First Name',
    'auth_lastname'  => 'Last Name',
    'auth_email'     => 'E-Mail'
);

my %USER_FIELD_TYPES = (
    -USERNAME_FIELD => 'auth_username',
    -PASSWORD_FIELD => 'auth_password',
    -GROUP_FIELD    => 'auth_groups',
    -EMAIL_FIELD    => 'auth_email'
);

my @MAIL_PARAMS = (
    -TYPE         => 'Sendmail',
);

my @USER_MAIL_SEND_PARAMS = (
    -FROM    => '$mail_from',
    -TO      => '$mail_to',
    -SUBJECT => '$APP_NAME_TITLE Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => '$mail_from',
    -TO      => '$mail_to',
    -SUBJECT => '$APP_NAME_TITLE Registration Notification'
);

                
my @AUTH_MANAGER_CONFIG_PARAMS = (
    -TYPE                        => 'CGI',
    -ADMIN_MAIL_SEND_PARAMS      => \@ADMIN_MAIL_SEND_PARAMS,
    -AUTH_VIEW_PARAMS            => \@AUTH_VIEW_DISPLAY_PARAMS,
    -MAIL_PARAMS                 => \@MAIL_PARAMS,
    -USER_MAIL_SEND_PARAMS       => \@USER_MAIL_SEND_PARAMS,
    -SESSION_OBJECT              => $SESSION,
    -LOGON_VIEW                  => 'AuthManager/CGI/LogonScreen',
    -REGISTRATION_VIEW           => 'AuthManager/CGI/RegistrationScreen',
    -REGISTRATION_SUCCESS_VIEW   => 'AuthManager/CGI/RegistrationSuccessScreen',
    -SEARCH_VIEW                 => 'AuthManager/CGI/SearchScreen',
    -SEARCH_RESULTS_VIEW         => 'AuthManager/CGI/SearchResultsScreen',
    -VIEW_LOADER                 => $VIEW_LOADER,
    -AUTH_PARAMS                 => \@AUTH_CONFIG_PARAMS,
    -CGI_OBJECT                  => $CGI,
    -ALLOW_REGISTRATION          => 1,   
    -ALLOW_USER_SEARCH           => 0,
    -USER_SEARCH_FIELD           => 'auth_email',
    -GENERATE_PASSWORD           => 0,
    -DEFAULT_GROUPS              => 'normal',
    -EMAIL_REGISTRATION_TO_ADMIN => 0,
    -USER_FIELDS                 => \@USER_FIELDS,
    -USER_FIELD_TYPES            => \%USER_FIELD_TYPES,
    -USER_FIELD_NAME_MAPPINGS    => \%USER_FIELD_NAME_MAPPINGS,
    -DISPLAY_REGISTRATION_AGAIN_AFTER_FAILURE => 1,
    -AUTH_REGISTRATION_DH_MANAGER_PARAMS => \@AUTH_REGISTRATION_DH_MANAGER_PARAMS
);

######################################################################
#                      DATA HANDLER SETUP                            #
######################################################################

my @ADD_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,
    -DATAHANDLERS => [qw(
        Email
        Exists
        HTML
        String
        )],

    -FIELD_MAPPINGS =>
      {
       queen_code	      	=> 'Queen Code',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       owner            => 'Owner',
       queen_record_id  	=> 'queen id',
       start_date       => 'Start Date',
       due_date         => 'Due Date',
       abstract         => 'Subject',
       details          => 'Description',
       status           => 'Status',
       priority         => 'Priority',
       last_mod_by      => 'Last Modified By',
       last_mod_date    => 'Last Modified Date',
       comments         => 'Comments',
      },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                *
            )]
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\\',
            -ERROR_MESSAGE => "You may not have a '\\' character in the " .
                              "%FIELD_NAME% field."
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                *
            )],

            -CONTENT_TO_DISALLOW => '\"',
            -ERROR_MESSAGE => "You may not have a '\"' character in the " .
                              "%FIELD_NAME% field."
        ],


        -IS_EMAIL => [
            -FIELDS => [qw(
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
        ],

        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
            -FIELDS => [qw(
                *
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [
                        qw(
                           owner
                           abstract
                           status
                           last_mod_by
                           last_mod_date
                          )
                       ]
        ]
    ]
);

my @MODIFY_FORM_DHM_CONFIG_PARAMS = (
    -TYPE         => 'CGI',
    -CGI_OBJECT   => $CGI,  
    -DATAHANDLERS => [qw(
        Email 
        Exists
        HTML
        String
        )],

    -FIELD_MAPPINGS => {
       queen_code	      	=> 'Queen Code',
       queen_record_id	      	=> 'queen id',
       estimated_man_hours 	=> 'Estimated Man Hours',
       accumulative_time 	=> 'Accumulated time',
       start_date               => 'Start Date',
       due_date                 => 'Due Date',
       abstract                 => 'Subject',
       details                  => 'Description',
       status                   => 'Status',
       priority                 => 'Priority',
       comments                 => 'Comments',
    },

    -RULES => [
        -ESCAPE_HTML_TAGS => [
            -FIELDS => [qw(
                
            )]
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                
            )],

            -CONTENT_TO_DISALLOW => '\\',
            -ERROR_MESSAGE => "You may not have a '\\' character in the " .
                              "%FIELD_NAME% field."
        ],

        -DOES_NOT_CONTAIN => [
            -FIELDS => [qw(
                
            )],

            -CONTENT_TO_DISALLOW => '\"',
            -ERROR_MESSAGE => "You may not have a '\"' character in the " .
                              "%FIELD_NAME% field."
        ],

        -IS_EMAIL => [
            -FIELDS => [qw(
                email
            )],

            -ERROR_MESSAGE => '%FIELD_VALUE% is not a valid value ' .
                              'for %FIELD_NAME%.'
        ],

        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [
            -FIELDS => [qw(
                *
            )],
            -ORIGINAL_STRING => '"',
            -NEW_STRING => "''"
        ],

        -IS_FILLED_IN => [
            -FIELDS => [qw(
                           owner
                           abstract
                           status
                           last_mod_by
                           last_mod_date
                          )
                       ]
        ]
    ]
);

my @DATA_HANDLER_MANAGER_CONFIG_PARAMS = (
    -ADD_FORM_DHM_CONFIG_PARAMS    => \@ADD_FORM_DHM_CONFIG_PARAMS,
    -MODIFY_FORM_DHM_CONFIG_PARAMS => \@MODIFY_FORM_DHM_CONFIG_PARAMS,
);

######################################################################
#                      DATASOURCE SETUP                              #
######################################################################

my @DATASOURCE_FIELD_NAMES = 
    qw(
       record_id
       sitename
       queen_record_id
       pallet_code
       owner
       start_date
       queen_code
       abstract
       box_1_bees
       box_1_brood
       box_1_broodadded
       box_1_foundation
       box_1_comb
       box_1_empty
       box_1_honey
       box_2_bees
       box_2_brood
       box_2_brood_x
       box_2_broodadded
       box_2_foundation
       box_2_comb
       box_2_empty
       box_2_honey
       box_x_bees
       box_x_brood
       box_x_broodadded
       box_x_foundation
       box_x_comb
       box_x_empty
       box_x_honey
       brood_given_x
       honey_box
       honey_box_foundation
       honey_removed
       honey_added
       details
       start_time
       group_of_poster
       status
       last_mod_by
       last_mod_date
       comments        
      );

# prepare the data then used in the form input definition
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (2020..2025);
my %days  = ();
$days{$_} = $_ for (1..31);

my %priority =
    (
      1 => 'LOW',
      2 => 'MIDDLE',
      3 => 'HIGH',
    );
    

my %queencode = $_ for (0..100);
my %status =
    (
      1 => 'New',
      2 => 'Laying',
      3 => 'Breeder',
      4 => 'Over Wintred',
   );

my %frames =
    (
      0  => 'None',
      1  => '1',
      2  => '2',
      3  => '3',
      4  => '4',
      5  => '5',
      6  => '6',
      7  => '7',
      8  => '8',
      9  => '9',
      10 => '10',
    );

 my %xframes =
    (
      0  => 'None',
      1  => '1',
      2  => '2',
      3  => '3',
      4  => '4',
      5  => '5',
      6  => '6',
      7  => '7',
      8  => '8',
      9  => '9',
      10 => '10',
      11  => '11',
      12  => '12',
      13  => '13',
      14  => '14',
      15  => '15',
      16  => '16',
      17  => '17',
   );
my %site_code;
if ( $group eq "CSC_admin" ||
         $SiteName eq "CSC" 
       ){
      %site_code = (
       $SiteName  => $SiteName,
        Altpower  => 'Alternat Power',
        Apis      => 'Apis beekeepig',
        Brew      => 'Brewing',
        CSC       => 'Computer System Consultin.ca',
        CS        => 'Country Stores',
        Demo      => "Computer System Consultin.ca Demo",
        Forager   => 'Forager.com',
        OKB       => 'Okanagan Beekeepers',
        Organic   => 'Organic Farming',
        Stawns    => "Stawn's Honey",
        VitalVic  => 'Vital Victoria',
        );
        
}else{
    %site_code = (
       $SiteName => $SiteName,
       );
}


my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     sitename => [
        -DISPLAY_NAME => 'Site Name *',
        -TYPE         => 'popup_menu',
        -NAME         => 'sitename',
        -VALUES       => [sort {$a <=> $b} keys %site_code],
        -LABELS       => \%site_code,
        -INPUT_CELL_COLSPAN => 3, 
    ],
     abstract => [
                 -DISPLAY_NAME => 'What was done.',
                 -TYPE         => 'textfield',
                 -NAME         => 'abstract',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    accumulative_time => [
        -DISPLAY_NAME => 'Accumulated Please Add time to entry',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
 #    queen_code => [
#     -DISPLAY_NAME => 'Queen code',
#       -TYPE         => 'checkbox_group',
#        -NAME         => 'queen_code',
#        -VALUES       => [sort {$a <=> $b} keys %queencode],
#        -LABELS       => \%queencode
#     
#    ],
 #    pallet_code => [
 #       -DISPLAY_NAME => 'Pallet Code',
 #       -TYPE         => 'textfield',
 #       -NAME         => 'pallet_code',
 #       -SIZE         => 30,
 #       -MAXLENGTH    => 80
#    ],
   queen_record_id => [
        -DISPLAY_NAME => 'Queen Record Id',
        -TYPE         => 'textfield',
        -NAME         => 'queen_record_id',
        -value        =>  $QueenRecordID,
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 6,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

     details  => [
                 -DISPLAY_NAME => 'Description',
                 -TYPE         => 'textarea',
                 -NAME         => 'details',
                 -ROWS         => 8,
                 -COLS         => 42,
                 -WRAP         => 'VIRTUAL',
                 -INPUT_CELL_COLSPAN => 3,
               ],

    box_1_bees => [
        -DISPLAY_NAME => 'Frames of Bees in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_bees',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
    box_1_brood => [
        -DISPLAY_NAME => 'Frames of Brood in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_brood',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
      box_1_broodadded => [
        -DISPLAY_NAME => 'Frames of Brood added',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_broodadded',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
  box_1_foundation => [
        -DISPLAY_NAME => 'Frames of Foundation in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_foundation',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 box_1_comb => [
        -DISPLAY_NAME => 'Frames of Comb in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_comb',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
        
     
    ],
  box_1_honey => [
        -DISPLAY_NAME => 'Frames of Honey in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_honey',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
box_1_empty => [
        -DISPLAY_NAME => 'Frames of Empty in Box 1',
        -TYPE         => 'textfield',
        -NAME         => 'box_1_empty',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
   
box_2_bees => [
        -DISPLAY_NAME => 'Frames of Bees in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_bees',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 box_2_brood => [
        -DISPLAY_NAME => 'Frames of Brood in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_brood',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 box_2_comb => [
        -DISPLAY_NAME => 'Frames of Comb in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_comb',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 box_2_empty => [
        -DISPLAY_NAME => 'Frames of Empty in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_empty',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 box_2_honey => [
        -DISPLAY_NAME => 'Frames of honey in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_honey',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
box_x_bees => [
        -DISPLAY_NAME => 'Frames of Bees in x',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_bees',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],
 box_x_brood => [
        -DISPLAY_NAME => 'Frames of Brood in  xBox ',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_brood',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],
 box_x_comb => [
        -DISPLAY_NAME => 'Frames of Comb in x Box ',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_comb',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],
 box_x_empty => [
        -DISPLAY_NAME => 'Frames of Empty in x Box ',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_empty',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ], 
 box_x_honey => [
        -DISPLAY_NAME => 'Frames of honey in x Box ',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_honey',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],
box_x_foundation => [
        -DISPLAY_NAME => 'Frames of Foundation in  xBox ',
        -TYPE         => 'textfield',
        -NAME         => 'box_x_foundation',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],

brood_given_x => [
        -DISPLAY_NAME => 'Frames of X Brood Given',
        -TYPE         => 'textfield',
        -NAME         => 'brood_given_x',
        -VALUES       =>  => [0..17],
        -LABELS       => \%xframes
     
    ],

  brood_given => [
        -DISPLAY_NAME => 'Frames of Brood Given',
        -TYPE         => 'textfield',
        -NAME         => 'brood_given',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
   
 
   box_2_foundation => [
        -DISPLAY_NAME => 'Frames of Foundation in Box 2',
        -TYPE         => 'textfield',
        -NAME         => 'box_2_foundation',
        -VALUES       =>  => [1..10],
        -LABELS       => \%frames
     
    ],

  brood_added => [
        -DISPLAY_NAME => 'Frames of Brood added',
        -TYPE         => 'textfield',
        -NAME         => 'brood_added',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
 honey_box => [
        -DISPLAY_NAME => 'Frames of honey',
        -TYPE         => 'textfield',
        -NAME         => 'honey_box',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],

    honey_box_foundation => [
        -DISPLAY_NAME => 'Frames of Foundation in honey box',
        -TYPE         => 'textfield',
        -NAME         => 'honey_box_foundation',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
     honey_added => [
        -DISPLAY_NAME => 'Frames of honey box added',
        -TYPE         => 'textfield',
        -NAME         => 'honey_added',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],
     honey_removed => [
        -DISPLAY_NAME => 'Frames of honey box Removed',
        -TYPE         => 'textfield',
        -NAME         => 'honey_removed',
        -VALUES       =>  => [0..10],
        -LABELS       => \%frames
     
    ],  estimated_man_hours => [
        -DISPLAY_NAME => 'Est. Man Hours',
        -TYPE         => 'textfield',
        -NAME         => 'estimated_man_hours',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     start_time => [
        -DISPLAY_NAME => 'Start Time',
        -TYPE         => 'textfield',
        -NAME         => 'start_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     end_time => [
        -DISPLAY_NAME => 'End Time',
        -TYPE         => 'textfield',
        -NAME         => 'end_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     time => [
        -DISPLAY_NAME => 'Time',
        -TYPE         => 'textfield',
        -NAME         => 'time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],
    start_day => [
                 -DISPLAY_NAME => 'Date of check',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_day',
                 -VALUES       => [1..31],
                ],

     start_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     start_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],

     due_day => [
                 -DISPLAY_NAME => 'Due Date',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_day',
                 -VALUES       => [1..31],
                ],

     due_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     due_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'due_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],

     priority => [
                 -DISPLAY_NAME => 'Priorit',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'priority',
                 -VALUES       => [sort {$a <=> $b} keys %priority],
                 -LABELS       => \%priority,
                 -INPUT_CELL_COLSPAN => 3,
                ],

 
     status => [
                 -DISPLAY_NAME => 'Status',
                 -TYPE         => 'checkbox_group',
                 -NAME         => 'status',
                 -VALUES       => [sort {$a <=> $b} keys %status],
		         -LABELS       => \%status,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    );

 #    [qw(due_day due_mon due_year)],

my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (      
     qw(sitename),
     qw(queen_code),
     qw(queen_record_id),
     qw(pallet_code),
     qw(abstract ),
     [qw(start_day start_mon start_year)],
     qw(details),
     qw(box_1_bees),
     qw(box_1_brood),
     qw(box_1_foundation),
     qw(box_1_comb),
     qw(box_1_empty),
     qw(box_1_honey),
     qw(box_1_broodadded),
     qw(box_2_bees),
     qw(box_2_brood),
     qw(box_2_foundation),
     qw(box_2_comb),
     qw(box_2_empty),
     qw(box_2_honey),
     qw(box_x_bees),
     qw(box_x_brood),
     qw(box_x_foundation),
     qw(box_x_comb),
     qw(box_x_empty),
     qw(box_x_honey),
     qw(honey_box),
     qw(honey_box_foundation),
     qw(honey_added),
     qw(honey_removed),
     [qw(status)],
     qw(brood_given),
     qw(brood_given_x),
     qw(comments),
    );


my %ACTION_HANDLER_PLUGINS =
    (

     'Default::DisplayAddFormAction' =>
     {
      -DisplayAddFormAction     => [qw(Plugin::Todo::DisplayAddFormAction)],
     },

     'Default::DisplayDetailsRecordViewAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayDeleteRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayModifyFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayModifyRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::ProcessModifyRequestAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayAddRecordConfirmationAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::ProcessAddRequestAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DefaultAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayViewAllRecordsAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplaySimpleSearchResultsAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayOptionsFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::DisplayPowerSearchFormAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },

     'Default::PerformPowerSearchAction' => 
     {
      -loadData_END             => [qw(Plugin::Todo::Records2Display)],
      -handleIncomingData_BEGIN => [qw(Plugin::Todo::InputFields2DBFields)],
     },



    );


my @INPUT_WIDGET_DEFINITIONS = (
    -BASIC_INPUT_WIDGET_DEFINITIONS => \%BASIC_INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_ORDER => \@BASIC_INPUT_WIDGET_DISPLAY_ORDER
);
my @BASIC_DATASOURCE_CONFIG_PARAMS;
if ($site eq "file"){
 @BASIC_DATASOURCE_CONFIG_PARAMS = (    -TYPE                       => 'File', 
    -FILE                       => "$APP_DATAFILES_DIRECTORY/$APP_NAME.dat",
    -FIELD_DELIMITER            => '|',
    -COMMENT_PREFIX             => '#',
    -CREATE_FILE_IF_NONE_EXISTS => 1,
    -FIELD_NAMES                => \@DATASOURCE_FIELD_NAMES,
    -KEY_FIELDS                 => ['record_id'],
    -FIELD_TYPES                => {
                                    record_id        => 'Autoincrement',
                                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
                                   },
);
}
else{
	@BASIC_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_queen_log_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
	        },
	);

    }

my @QUEENS_DATASOURCE_FIELD_NAMES = 
    qw(
        status
        sitename
        queen_code
        queen_name
        pallet_code
        box_number
        parent
        queen_colour
        date
        client_name
        comments
        username_of_poster
        group_of_poster
      );

my	@QUEENS_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_queens_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@QUEENS_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
);
my @PROJECT_DATASOURCE_FIELD_NAMES = qw(
        record_id
        sitename
        status
        queen_code
        queen_name
        queen_colour
        date
        location
        client_name
        comments        
        username_of_poster
        group_of_poster
        date_time_posted
);

my	@PROJECT_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_queens_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@PROJECT_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
);
my @PALLET_DATASOURCE_FIELD_NAMES = qw(
       sitename
       pallet_code
       status
       username_of_poster
       group_of_poster
 );

my	@PALLET_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_pallet_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@PALLET_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['username'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement'
	        },
	);
my @DROPLIST_DATASOURCE_FIELD_NAMES = qw(
        record_id
        status
        category
        sitename
        app_name
        list_name
        display_value
        client_name
        comments        
        username_of_poster
        group_of_poster
        date_time_posted
);

my  @DROPLIST_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'csc_droplist_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@DROPLIST_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['project_code'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
	        },
	);
my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
    -PALLET_DATASOURCE_CONFIG_PARAMS    => \@PALLET_DATASOURCE_CONFIG_PARAMS,
    -DROPLIST_DATASOURCE_CONFIG_PARAMS  => \@DROPLIST_DATASOURCE_CONFIG_PARAMS,
    -PROJECT_DATASOURCE_CONFIG_PARAMS     => \@PROJECT_DATASOURCE_CONFIG_PARAMS,
    -QUEENS_DATASOURCE_CONFIG_PARAMS     => \@QUEENS_DATASOURCE_CONFIG_PARAMS,
    -AUTH_USER_DATASOURCE_CONFIG_PARAMS => \@AUTH_USER_DATASOURCE_PARAMS
);

######################################################################
#                          MAILER SETUP                              #
######################################################################
my @MAIL_CONFIG_PARAMS = 
    (
     -TYPE         => 'Sendmail'
    );

my @EMAIL_DISPLAY_FIELDS = 
    qw(
       queen_code
       abstract
       start_date
       details
       comments        
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => "$APP_NAME_TITLE Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => "$APP_NAME_TITLE Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     => "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => "$APP_NAME_TITLE Modification"
);


my @MAIL_SEND_PARAMS = (
    -DELETE_EVENT_MAIL_SEND_PARAMS => \@DELETE_EVENT_MAIL_SEND_PARAMS,
    -ADD_EVENT_MAIL_SEND_PARAMS    => \@ADD_EVENT_MAIL_SEND_PARAMS,
    -MODIFY_EVENT_MAIL_SEND_PARAMS => \@MODIFY_EVENT_MAIL_SEND_PARAMS
);

##################################################################
#                         LOGGING SETUP                          #
##################################################################

my @LOG_CONFIG_PARAMS = (
    -TYPE             => 'File',
    -LOG_FILE         => "$APP_DATAFILES_DIRECTORY/$APP_NAME.log",
    -LOG_ENTRY_SUFFIX => '|' . _generateEnvVarsString() . '|',
    -LOG_ENTRY_PREFIX => 'log|'
);

sub _generateEnvVarsString {
    my @env_values;
    
    my $key;
    foreach $key (keys %ENV) {
        push (@env_values, "$key=" . $ENV{$key});
    }   my @QUEENS_DATASOURCE_FIELD_NAMES = qw(
        status
        record_id
        queen_code
        queen_name
        pallet_code
        box_number
        parent
        queen_colour
        date
        client_name
        comments
        username_of_poster
        group_of_poster
);
my @QUEENS_DATASOURCE_CONFIG_PARAMS = (
	        -TYPE         => 'DBI',
	        -DBI_DSN      => $DBI_DSN,
	        -TABLE        => 'apis_queens_tb',
	        -USERNAME     => $AUTH_MSQL_USER_NAME,
	        -PASSWORD     => $MySQLPW,
	        -FIELD_NAMES  => \@QUEENS_DATASOURCE_FIELD_NAMES,
	        -KEY_FIELDS   => ['queen_code'],
	        -FIELD_TYPES  => {
	            record_id        => 'Autoincrement',
                    datetime         => 
                                    [
                                     -TYPE  => "Date",
                                     -STORAGE => 'y-m-d H:M:S',
                                     -DISPLAY => 'y-m-d H:M:S',
                                    ],
	        },
	);


    return join ("\|", @env_values);
}   
   
######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = 
    qw(
       CSPSCSSView
       CSCCSSView
       CAPCSSVie
       VitalVicCSSView
       CSCTotalView
       ApisCSSView
       ENCYCSSView
       BCAFCSSView
       ApisQueenLogView
       DetailsRecordView
       BasicDataView

       AddRecordView 
       AddRecordConfirmationView
       AddAcknowledgementView

       DeleteRecordConfirmationView
       DeleteAcknowledgementView

       ModifyRecordView
       ModifyRecordConfirmationView
       ModifyAcknowledgementView

       PowerSearchFormView
       OptionsView
       LogoffView
       BeeDiseaseView
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
     -DISPLAY_FIELDS                 => [qw(
        start_date
        queen_code
        pallet_code
        queen_code
        box_1_bees
        box_1_brood
        box_1_foundation
        box_2_bees
        box_2_brood
        box_2_foundation
        honey_box
        honey_box_foundation
        honey_removed
        abstract
        details
        start_date
        status
        )],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        url
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        body
    )],
    -FIELD_NAME_MAPPINGS     => {
        'queen_code' => 'Queen Code',
        'abstract'     => 'Subject',
        'details'      => 'Description',
        'pallet_code'      => 'pallet_code',
        'queen_code'      => 'queen_code',
        'box_1_bees'      => 'box_1_bees',
        'box_1_brood'      => 'box_1_brood',
        'box_1_foundation'      => 'box_1_foundation',
        'box_2_bees'      => 'box_2_bees',
        'box_2_brood'      => 'box_2_brood',
        'box_2_foundation'      => 'box_2_foundation',
        'honey_box'      => 'honey_box',
        'honey_box_foundation'      => 'oney_box_foundation',
        'honey_removed'      => 'honey_removed',
        'start_date'   => 'Date ',
        'due_date'     => 'Due Date',
        'end_time'     => 'Due Time',
        'time'     => 'Time',
        'status'       => 'Status',
        'priority'     => 'Priority',
        },
    -HOME_VIEW               => $homeviewname,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => '_self',
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
        start_date
        queen_code
        abstract
        pallet_code
        box_1_bees
        box_1_brood
        box_1_foundation
        box_2_bees
        box_2_brood
        box_2_foundation
        honey_box
        honey_box_foundation
        honey_removed
       )],
    -SORT_FIELDS             => [qw(
        abstract
        pallet_code
       queen_code
       box_1_bees
       box_1_brood
       box_1_foundation
       box_2_bees
       box_2_brood
       box_2_foundation
       honey_box
       honey_box_foundation
       honey_removed

        )],
        -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,

);  

######################################################################
#                           DATE TIME SETUP                             #
######################################################################

my @DATETIME_CONFIG_PARAMS = 
    (
     -TYPE => 'ClassDate',
    );

######################################################################
#                           FILTER SETUP                             #
######################################################################

my @HTMLIZE_FILTER_CONFIG_PARAMS = (
    -TYPE                          => 'HTMLize',
    -CONVERT_DOUBLE_LINEBREAK_TO_P => 1,
    -CONVERT_LINEBREAK_TO_BR       => 1,
);

my @CHARSET_FILTER_CONFIG_PARAMS = (
    -TYPE            => 'CharSet'
);


my @EMBED_FILTER_CONFIG_PARAMS = (
    -TYPE            => 'Embed',
    -ENABLE          => $CGI->param('embed') || 0
);

my @VIEW_FILTERS_CONFIG_PARAMS = (
     \@HTMLIZE_FILTER_CONFIG_PARAMS,
     \@CHARSET_FILTER_CONFIG_PARAMS,
     \@EMBED_FILTER_CONFIG_PARAMS
); 

######################################################################
#                      ACTION/WORKFLOW SETUP                         #
######################################################################
 #     Default::PopulateInputWidgetDefinitionListWithSiteWidgetAction
#      Apis::PopulateInputWidgetDefinitionListWithQueenCodeWidgetAction
  #     Apis::PopulateInputWidgetDefinitionListWithPalletCodeWidgetAction

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST = 
    qw(
       Apis::PopulateInputWidgetDefinitionListWithQueenCodeWidgetAction
       Apis::PopulateInputWidgetDefinitionListWithPalletCodeWidgetAction
       Default::SetSessionData
       Default::DisplayCSSViewAction

        CSC::BillingStatsAction

       Default::DisplayDetailsRecordViewAction

       Default::DisplayDeleteFormAction
       Default::ProcessDeleteRequestAction
       Default::DisplayDeleteRecordConfirmationAction

       Default::DisplayModifyFormAction
       Default::ProcessModifyRequestAction
       Default::DisplayModifyRecordConfirmationAction

       Default::DisplayAddFormAction
       Default::ProcessAddRequestAction
       Default::DisplayAddRecordConfirmationAction

       Default::DisplaySimpleSearchResultsAction
       Default::DisplayOptionsFormAction
       Default::DisplayPowerSearchFormAction
       Default::PerformPowerSearchAction

       Default::PerformLogonAction
       Default::PerformLogoffAction

       Default::DisplayViewAllRecordsAction
       Default::DefaultAction

      );


my @ACTION_HANDLER_ACTION_PARAMS = (
    -ACTION_HANDLER_LIST                    => \@ACTION_HANDLER_LIST,
    -APP_NAME                               => $APP_NAME,
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -AFFILIATE_NUMBER                       => $Affiliate,
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
 -APP_VER                                => $AppVer,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => $homeviewname||'BasicDataView',
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
 -Debug                                  => $CGI->param('debug') || 0,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 0,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 0,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 0,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 0,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 0,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 0,
 -DOMAIN_NAME                            => $HostName,
    -ENABLE_SORTING_FLAG                    => 1,
    -FIRST_RECORD_ON_PAGE => $CGI->param('first_record_to_display') || 0,
 -GLOBAL_DATAFILES_DIRECTORY             => $GLOBAL_DATAFILES_DIRECTORY,
 -GROUP                                  => $group,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -KEY_FIELD                              => 'record_id',
    -LAST_RECORD_ON_PAGE  => $CGI->param('first_record_to_display') || "0",
 -LAST_UPDATE                            => $last_update,
  -LineStatus                             => $LineStatus,
  -LOCAL_IP                               => $LocalIp,
  -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
  -MAIL_USER                              => $mail_to_user,
 -MAIL_MEMBER                            => $mail_to_member,
 -MAIL_DISCUSSION                        => $mail_to_discussion ,
  -MOBILE                                 => $CGI->param('m') || 0,  
  -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 100,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
     -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
-NEWS_TB                                => $NEWS_TB,
 -OFF_LINE                               => $OffLine,
   -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -PAGE_TOP_VIEW           =>  $CGI->param('page_top_view') ||  $page_top_view ,
   -PID                                  => $pid,
   -LEFT_PAGE_VIEW          =>  $CGI->param('left_page_view') || $left_page_view,
    -PAGE_BOTTOM_VIEW        =>  $CGI->param('page_bottom_view') || $page_bottom_view,
  -PAGE_NAME                              => $Page,
   -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
 -PROCEDURE                              => $procedure,
 -PROJECT                                => $project,
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 1,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 1,
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
-SHOP                                   => $shop,
     -SIMPLE_SEARCH_STRING => $CGI->param('simple_search_string') || "",
    -SITE_NAME            => $SiteName,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'queen_code',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'start_date',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'DESC',
    -STAT_VIEW_NAME                         => 'CSCTotalView',
  -STORE_URL                              => $StoreUrl,
 -STYLE                                  => $style,
   -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
  -TITLE                                  => $title,
   -VALID_VIEWS                            => \@VALID_VIEWS,
  -VIEW                                   => $View,
   -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -DATETIME_CONFIG_PARAMS                 => \@DATETIME_CONFIG_PARAMS,
    -ACTION_HANDLER_PLUGINS                 => \%ACTION_HANDLER_PLUGINS,
);

######################################################################
#                      LOAD APPLICATION                              #
######################################################################

my $APP = Extropia::Core::App::DBApp->new(
    -ROOT_ACTION_HANDLER_DIRECTORY => "../ActionHandler",
    -ACTION_HANDLER_ACTION_PARAMS => \@ACTION_HANDLER_ACTION_PARAMS,
    -ACTION_HANDLER_LIST          => \@ACTION_HANDLER_LIST,
    -VIEW_DISPLAY_PARAMS          => \@VIEW_DISPLAY_PARAMS
    ) or die("Unable to construct the application object in " . 
             $CGI->script_name() .  ". Please contact the webmaster.");

#print "Content-type: text/html\n\n";
print $APP->execute();
