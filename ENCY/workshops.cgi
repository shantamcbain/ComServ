#!/usr/bin/perl -wT 
# 	$Id: workshops.cgi,v 0.1 2011/8/28 22:40:29 shanta Exp shanta $	
#CSC file location /cgi-bin/ENCY/
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

BEGIN{
    use vars qw(@dirs);
    @dirs = qw(../Modules/
               ../Modules/CPAN .);
}
use lib @dirs;
unshift @INC, @dirs unless $INC[0] eq $dirs[0];

my @VIEWS_SEARCH_PATH = 
    qw(../Modules/Extropia/View/ENCY
       ../Modules/Extropia/View/Todo
       ../Modules/Extropia/View/Default
      );

my @TEMPLATES_SEARCH_PATH = 
    qw(../HTMLTemplates/ENCY
       ../HTMLTemplates/CSC
       ../HTMLTemplates/CSPS
       ../HTMLTemplates/Shanta
       ../HTMLTemplates/Todo
       ../HTMLTemplates/HelpDesk
       ../HTMLTemplates/Default
      );

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
my $SiteName =  $CGI->param('site') || "ENCY";
    my $PrintMode =  $CGI->param('mode') || "month";
my $APP_NAME = "ency"; 
    my $SITE_DISPLAY_NAME = 'None Defined for this site.';
    my $last_update = 'Febuary 26, 2015';
    my $site_update = 'Feburary 26, 2015';

    my $APP_NAME_TITLE = "Work Shops";
    my $homeviewname         ;
    my $home_view            ;
    my $BASIC_DATA_VIEW      ;
    my $page_top_view        ;
    my $page_bottom_view     ;
    my $page_left_view;
    my $left_page_view       ;
    my $MySQLPW;
#Mail settings
    my $mail_from            ;
    my $mail_to              ;
    my $mail_replyto         ;
    my $CSS_VIEW_NAME        ;
    my $app_logo             ;
    my $app_logo_height      ;
    my $app_logo_width       ;
    my $app_logo_alt             ;
    my $IMAGE_ROOT_URL       ;
    my $DOCUMENT_ROOT_URL    ;
    my $LINK_TARGET;
    my $HTTP_HEADER_PARAMS;
    my $GLOBAL_DATAFILES_DIRECTORY ;
    my $TEMPLATES_CACHE_DIRECTORY;
    my $APP_DATAFILES_DIRECTORY;
    my $site;
    my $DATAFILES_DIRECTORY;
    my $site_session;
    my $auth;
    my $datafile;
    my  $DBI_DSN;
    my $AUTH_TABLE;
    my  $AUTH_MSQL_USER_NAME;
    my $HasMembers = 0;

 
  use SiteSetup;
  my $UseModPerl = 0;
  my $SiteNameSetup = $SiteName."Setup";
  my $SetupVariables   = new  SiteSetup($UseModPerl);
  $APP_NAME_TITLE             = $SiteName.": ".$APP_NAME_TITLE;
  $DBI_DSN                    = $SetupVariables->{-DBI_DSN};
  $AUTH_TABLE                 = $SetupVariables->{-AUTH_TABLE};
  $AUTH_MSQL_USER_NAME        = $SetupVariables->{-AUTH_MSQL_USER_NAME};

  $home_view                  = $SetupVariables->{-BASIC_DATA_VIEW}; 
  $BASIC_DATA_VIEW            = $SetupVariables->{-BASIC_DATA_VIEW};
  $page_top_view              = $SetupVariables->{-PAGE_TOP_VIEW}||'PageTopView';
  $page_bottom_view           = $SetupVariables->{-PAGE_BOTTOM_VIEW};
  $left_page_view             = $SetupVariables->{-LEFT_PAGE_VIEW};
  $MySQLPW                    = $SetupVariables->{-MySQLPW};
  #Mail settings
  $mail_from                  = $SetupVariables->{-MAIL_FROM}; 
  $mail_to                    = $SetupVariables->{-MAIL_TO};
  $mail_replyto               = $SetupVariables->{-MAIL_REPLYTO};
  $app_logo                   = $SetupVariables->{-APP_LOGO};
  $app_logo_height            = $SetupVariables->{-APP_LOGO_HEIGHT};
  $app_logo_width             = $SetupVariables->{-APP_LOGO_WIDTH};
  $app_logo_alt               = $SetupVariables->{-APP_LOGO_ALT};
  $IMAGE_ROOT_URL             = $SetupVariables->{-IMAGE_ROOT_URL}; 
  $DOCUMENT_ROOT_URL          = $SetupVariables->{-DOCUMENT_ROOT_URL};
  $LINK_TARGET                = $SetupVariables->{-LINK_TARGET};
  $HTTP_HEADER_PARAMS         = $SetupVariables->{-HTTP_HEADER_PARAMS};
  $SITE_DISPLAY_NAME          = $SetupVariables->{-SITE_DISPLAY_NAME};

  $site                       = $SetupVariables->{-DATASOURCE_TYPE};
  $GLOBAL_DATAFILES_DIRECTORY = $SetupVariables->{-GLOBAL_DATAFILES_DIRECTORY}||'BLANK';
  $TEMPLATES_CACHE_DIRECTORY  = $GLOBAL_DATAFILES_DIRECTORY.$SetupVariables->{-TEMPLATES_CACHE_DIRECTORY,};
  $APP_DATAFILES_DIRECTORY    = $SetupVariables->{-APP_DATAFILES_DIRECTORY};
  my $HTTP_HEADER_DESCRIPTION = $SetupVariables->{-HTTP_HEADER_DESCRIPTION};
  my $HTTP_HEADER_KEYWORDS    = $SetupVariables->{-HTTP_HEADER_KEYWORDS};
  my $AUTH_TABLE              = $SetupVariables->{-AUTH_TABLE};
  $CSS_VIEW_NAME              = $SetupVariables->{-CSS_VIEW_NAME};
  my $CSS_VIEW_URL            = $SetupVariables->{-CSS_VIEW_NAME}||'none';
  my $FAVICON                 = $SetupVariables->{-FAVICON};
  my $ANI_FAVICON             = $SetupVariables->{-ANI_FAVICON};
  my $FAVICON_TYPE            = $SetupVariables->{-FAVICON_TYPE};
  my $Affiliate               = $SetupVariables->{-AFFILIATE};

#script override Varibles
  $mail_from        = "$CGI->param('email')||$mail_from"; 





my $VIEW_LOADER = new Extropia::Core::View
  (\@VIEWS_SEARCH_PATH,\@TEMPLATES_SEARCH_PATH) or
    die("Unable to construct the VIEW LOADER object in " . $CGI->script_name() .
        " Please contact the webmaster.");
use constant HAS_CLASS_DATE  => eval { require Class::Date; };

######################################################################
#                          SESSION SETUP                             #
######################################################################

my @SESSION_CONFIG_PARAMS = (
    -TYPE            => 'File',
    -MAX_MODIFY_TIME => 60 * 60,
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

if ($CGI->param('mode')){
    if  ($CGI->param('mode') ne $SESSION ->getAttribute(-KEY => 'PrintMode') ){
      $SESSION ->setAttribute(-KEY => 'PrintMode', -VALUE => $CGI->param('mode')) ;
       $PrintMode = $CGI->param('mode');
    }else {
	$SESSION ->setAttribute(-KEY => 'PrintMode', -VALUE => $PrintMode );
    }
	 
}else {
  if ( $SESSION ->getAttribute(-KEY => 'PrintMode')) {
    $PrintMode = $SESSION ->getAttribute(-KEY => 'PrintMode');
  }else {
	$SESSION ->setAttribute(-KEY => 'PrintMode', -VALUE => $PrintMode );
      }
}



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
        -TABLE        => $AUTH_TABLE,
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
    -SITE_NAME            => $SiteName,
    -CSS_VIEW_URL            => $CSS_VIEW_URL,
    -APPLICATION_LOGO        => $app_logo,
    -APPLICATION_LOGO_HEIGHT => $app_logo_height,
    -APPLICATION_LOGO_WIDTH  => $app_logo_width,
    -APPLICATION_LOGO_ALT    => $APP_NAME_TITLE,
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -HTTP_HEADER_PARAMS      => $HTTP_HEADER_PARAMS,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -PAGE_TOP_VIEW                          => $CGI->param('page_top_view')||$page_top_view,
    -PAGE_BOTTOM_VIEW                       => $CGI->param('page_bottom_view')||$page_bottom_view,
    -LEFT_PAGE_VIEW                         => $left_page_view,
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
    -TO      => '$mail_to',
    -SUBJECT => $APP_NAME_TITLE.' Password Generated'
);

my @ADMIN_MAIL_SEND_PARAMS = (
    -FROM    => "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO      => '$mail_to',
    -SUBJECT => $APP_NAME_TITLE.' Registration Notification'
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
    -EMAIL_REGISTRATION_TO_ADMIN => 1,
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
       WorkShop_Code	 => 'WorkShop Code',
       participants 	 => 'Participants',
       accumulative_time => 'Accumulated time',
       start_date        => 'Date',
       workshop_name     => 'WorkShop Name',
       description       => 'Description',
       status            => 'Status',
       priority          => 'Priority',
       last_mod_by       => 'Last Modified By',
       last_mod_date     => 'Last Modified Date',
       comments          => 'Comments',
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
                           sitename
                           start_day
                           workshop_name
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
       WorkShop_Code	 => 'WorkShop Code',
       participants  	 => 'Participants',
       accumulative_time => 'Accumulated time',
       start_date        => 'Date',
       workshop_name     => 'WorkShop Name',
       description       => 'Description',
       status            => 'Status',
       priority          => 'Priority',
       comments          => 'Comments',
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
                           
                           start_day
                           workshop_name
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
       start_date
       workshop_code
       participants 
       accumulative_time
       end_date
       workshop_name
       description
       registration
       status
       priority
       last_mod_by
       last_mod_date
       comments        
      );
my $define_am_pm =0;


# prepare the data then used in the form input definition
# this field denominates the valid range of hours for the calendar
my @VALID_WORKING_HOURS = (4..24);

# this variable array is for the pull down hour display.
my @DISPLAY_VALID_WORKING_HOURS = (4..21);

# Be careful about columns or the display will be distorted.
# It is defined below and will be used in the BASIC_INPUT_WIDGET_DEFINITIONS 
my $added_columns;

if($define_am_pm) {
	@DISPLAY_VALID_WORKING_HOURS = (1..12);
	$added_columns = 2;
} else {
	@DISPLAY_VALID_WORKING_HOURS = @VALID_WORKING_HOURS ;
	$added_columns = 0;
}
my @months = qw(January February March April May June July August
                September October November December);
my %months;
@months{1..@months} = @months;
my %years = ();
$years{$_} = $_ for (2019..2025);
my %days  = ();
$days{$_} = $_ for(1..31);

my %hours = ();
$hours{$_} = sprintf "%02d",$_  for @DISPLAY_VALID_WORKING_HOURS;

my %mins  = ();
$mins{+$_*5} = sprintf "%02d",$_*5 for (0..11);

my %priority =
    (
      1 => 'LOW',
      2 => 'MIDDLE',
      3 => 'HIGH',
    );

my %status =
    (
      'New' => 'NEW',
      'Active' => 'IN PROGRESS',
      'Done' => 'DONE',
      'Full' => 'Full',
    );



my %BASIC_INPUT_WIDGET_DEFINITIONS = 
    (
     workshop_name => [
                 -DISPLAY_NAME => 'WorkShop Name',
                 -TYPE         => 'textfield',
                 -NAME         => 'workshop_name',
                 -SIZE         => 44,
                 -MAXLENGTH    => 200,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    accumulative_time => [
        -DISPLAY_NAME => 'Length',
        -TYPE         => 'textfield',
        -NAME         => 'accumulative_time',
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

     registration => [        
        -DISPLAY_NAME => 'To register',        
        -TYPE         => 'textfield',        
        -NAME         => 'registration',        
        -SIZE         => 30,        
        -MAXLENGTH    => 200    
        ],

   comments => [
        -DISPLAY_NAME => 'Comments',
        -TYPE         => 'textarea',
        -NAME         => 'comments',
        -ROWS         => 10,
        -COLS         => 30,
        -WRAP         => 'VIRTUAL'
    ],

     description  => [
                 -DISPLAY_NAME => 'Description',
                 -TYPE         => 'textarea',
                 -NAME         => 'description',
                 -ROWS         => 8,
                 -COLS         => 42,
                 -WRAP         => 'VIRTUAL',
                 -INPUT_CELL_COLSPAN => 3,
               ],

    participants => [
        -DISPLAY_NAME => 'Number of partisipants',
        -TYPE         => 'popup_menu',
        -NAME         => 'participants',
        -VALUES       => [1..31],
    ],

     start_day => [
	                 -DISPLAY_NAME => 'Start Date',
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
     start_hour => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_hour',
                 -VALUES       => [sort {$a <=> $b} keys %hours],
                 -LABELS       => \%hours,
                ],

     start_min => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'start_min',
                 -VALUES       => [sort {$a <=> $b} keys %mins],
                 -LABELS       => \%mins,
                 
                ],
                
     start_am_pm  => [
                -DISPLAY_NAME => '',
                -TYPE         => 'popup_menu',
                -NAME         => 'start_am_pm',
                -VALUES       =>  ["AM", "PM" ],  
                -LABELS       =>  "",
               

                ],

     is_all_day => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'checkbox',
                 -NAME         => 'is_all_day',
                 -VALUE        => 1,
                 -LABEL        => 'All Day Event'
                ],


     end_day => [
                 -DISPLAY_NAME => 'End Date',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'end_day',
                 -VALUES       => [1..31],
                ],

     end_mon => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'end_mon',
                 -VALUES       => [1..12],
                 -LABELS       => \%months,
                ],

     end_year => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'end_year',
                 -VALUES       => [sort {$a <=> $b} keys %years],
                ],

     end_hour => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'end_hour',
                 -VALUES       => [sort {$a <=> $b} keys %hours],
                 -LABELS       => \%hours,
                ],

     end_min => [
                 -DISPLAY_NAME => '',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'end_min',
                 -VALUES       => [sort {$a <=> $b} keys %mins],
                 -LABELS       => \%mins,
                 -INPUT_CELL_COLSPAN => 2 - $added_columns,
                ],

     end_am_pm  => [
                -DISPLAY_NAME => '',
                -TYPE         => 'popup_menu',
                -NAME         => 'end_am_pm',
                -VALUES       =>  ["AM", "PM" ],  
                -LABELS       =>  "",
                -INPUT_CELL_COLSPAN => $added_columns,

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
                 -DISPLAY_NAME => 'Priority',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'priority',
                 -VALUES       => [sort {$a <=> $b} keys %priority],
                 -LABELS       => \%priority,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    WorkShop_Code => [
        -DISPLAY_NAME => 'WorkShop Code',
        -TYPE         => 'textfield',
        -NAME         => 'workshop_code',

    ],

      sitename => [
        -DISPLAY_NAME => 'Site',
        -TYPE         => 'textfield',
        -NAME         => 'sitename',
        -VALUE        => $SiteName,
        -SIZE         => 30,
        -MAXLENGTH    => 80
    ],

    status => [
                 -DISPLAY_NAME => 'Status',
                 -TYPE         => 'popup_menu',
                 -NAME         => 'status',
                 -VALUES       => [sort {$a <=> $b} keys %status],
		 -LABELS       => \%status,
                 -INPUT_CELL_COLSPAN => 3,
                ],

    );


my @BASIC_INPUT_WIDGET_DISPLAY_ORDER = 
    (
     qw(sitename),
     qw(WorkShop_Code),
     qw(workshop_name ),
     [qw(start_day start_mon start_year start_hour start_min start_am_pm is_all_day)],
     [qw(end_day end_mon end_year end_hour end_min end_am_pm)],
     qw(description),
     [qw(status)],
     qw(participants),
     qw(registration),
     qw(accumulative_time),
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
      -loadData_END             => [qw(Plugin::WebCal::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::WebCal::InputFields2DBFields)],
     },
     'Default::ProcessAddRequestAction' => 
     {
      -loadData_END             => [qw(Plugin::WebCal::DBRecords2InputFields)],
      -handleIncomingData_BEGIN => [qw(Plugin::WebCal::InputFields2DBFields)],
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
        -TABLE        => 'workshop_tb',
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


my @DATASOURCE_CONFIG_PARAMS = (
    -BASIC_DATASOURCE_CONFIG_PARAMS     => \@BASIC_DATASOURCE_CONFIG_PARAMS,
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
       workshop_name
       location
       start_date
       end_date
       recur_interval
       recur_until_date
       description
       participants
       accumulative_time
       comments        
      );

my @DELETE_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => $APP_NAME_TITLE." Delete"
);

my @ADD_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => $APP_NAME_TITLE." Addition"
);

my @MODIFY_EVENT_MAIL_SEND_PARAMS = (
    -FROM     =>  "$SESSION->getAttribute(-KEY =>
'auth_email')"||'$mail_from',
    -TO       => '$mail_to',
    -REPLY_TO => '$mail_replyto',
    -SUBJECT  => $APP_NAME_TITLE." Modification"
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
    -LOG_ENTRY_PREFIX => 'Todo|'
);

sub _generateEnvVarsString {
    my @env_values;
    
    my $key;
    foreach $key (keys %ENV) {
        push (@env_values, "$key=" . $ENV{$key});
    }   
    return join ("\|", @env_values);
}   
   
######################################################################
#                          VIEW SETUP                                #
######################################################################

my @VALID_VIEWS = 
    qw(
       ENCYCSSView
       VitalVicCSSView

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
       ENCYHomeView
       ENCYSideBarHomeView
       MembersView
       HostingView
       MentorView
      );

my @ROW_COLOR_RULES = (
);

my @VIEW_DISPLAY_PARAMS = (
    -APPLICATION_LOGO               => $app_logo,
    -APPLICATION_LOGO_HEIGHT        => $app_logo_height,
    -APPLICATION_LOGO_WIDTH         => $app_logo_width,
    -APPLICATION_LOGO_ALT           => $app_logo_alt,
    -DISPLAY_FIELDS                 => [qw(
        workshop_name
        description
        start_date
        due_date
        status
        priority
        )],
    -DOCUMENT_ROOT_URL       => $DOCUMENT_ROOT_URL,
    -EMAIL_DISPLAY_FIELDS    => \@EMAIL_DISPLAY_FIELDS,
    -FIELDS_TO_BE_DISPLAYED_AS_EMAIL_LINKS => [qw(
        email
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_LINKS => [qw(
        registration
    )],
    -FIELDS_TO_BE_DISPLAYED_AS_MULTI_LINE_TEXT => [qw(
        body
    )],
    -FIELD_NAME_MAPPINGS     => {
        'WorkShop_Code' => 'WorkShop Code',
        'workshop_name'     => 'WorkShop Name',
        'description'      => 'Description',
        'registration' => 'Registration',
        'start_date'   => 'Date',
        'participants'     => 'Participants',
        'status'       => 'Status',
        'priority'     => 'Priority',
        },
    -HOME_VIEW               => $homeviewname,
    -IMAGE_ROOT_URL          => $IMAGE_ROOT_URL,
    -LINK_TARGET             => $LINK_TARGET,
    -ROW_COLOR_RULES         => \@ROW_COLOR_RULES,
    -SITE_DISPLAY_NAME       => $SITE_DISPLAY_NAME,
    -SCRIPT_DISPLAY_NAME     => $APP_NAME_TITLE,
    -SCRIPT_NAME             => $CGI->script_name(),
    -SELECTED_DISPLAY_FIELDS => [qw(
        workshop_name
        start_date
        participants
        status
        registration
        )],
    -SORT_FIELDS             => [qw(
        start_date
        workshop_name
        )],
);  


######################################################################
#                           DATE TIME SETUP                             #
######################################################################

my @DATETIME_CONFIG_PARAMS = 
    (
     -TYPE => (HAS_CLASS_DATE ? 'ClassDate' : 'DateManip'),
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
    -ENABLE          => 0
);

my @VIEW_FILTERS_CONFIG_PARAMS = (
     \@HTMLIZE_FILTER_CONFIG_PARAMS,
     \@CHARSET_FILTER_CONFIG_PARAMS,
     \@EMBED_FILTER_CONFIG_PARAMS
); 

######################################################################
#                      ACTION/WORKFLOW SETUP                         #
######################################################################

# note: Default::DefaultAction must! be the last one
my @ACTION_HANDLER_LIST = 
    qw(
       Default::SetSessionData
       Default::DisplayCSSViewAction

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
    -ADD_ACKNOWLEDGEMENT_VIEW_NAME          => 'AddAcknowledgementView',
    -ADD_EMAIL_BODY_VIEW                    => 'AddEventEmailView',
    -ADD_FORM_VIEW_NAME                     => 'AddRecordView',
    -ALLOW_ADDITIONS_FLAG                   => 1,
    -ALLOW_MODIFICATIONS_FLAG               => 1,
    -ALLOW_DELETIONS_FLAG                   => 1,
    -ALLOW_DUPLICATE_ENTRIES                => 0,
    -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED    => 1,
    -APPLICATION_SUB_MENU_VIEW_NAME         => 'ApplicationSubMenuView',
    -OPTIONS_FORM_VIEW_NAME                 => 'OptionsView',
    -AUTH_MANAGER_CONFIG_PARAMS             => \@AUTH_MANAGER_CONFIG_PARAMS,
    -ADD_RECORD_CONFIRMATION_VIEW_NAME      => 'AddRecordConfirmationView',
    -BASIC_DATA_VIEW_NAME                   => $BASIC_DATA_VIEW,
    -DEFAULT_ACTION_NAME                    => 'DisplayDayViewAction',
    -CGI_OBJECT                             => $CGI,
    -CSS_VIEW_URL                           => $CSS_VIEW_URL,
    -CSS_VIEW_NAME                          => $CSS_VIEW_NAME,
    -DATASOURCE_CONFIG_PARAMS               => \@DATASOURCE_CONFIG_PARAMS,
    -DELETE_ACKNOWLEDGEMENT_VIEW_NAME       => 'DeleteAcknowledgementView',
    -DELETE_RECORD_CONFIRMATION_VIEW_NAME   => 'DeleteRecordConfirmationView',
    -RECORDS_PER_PAGE_OPTS                  => [5, 10, 25, 50, 100],
    -MAX_RECORDS_PER_PAGE                   => $CGI->param('records_per_page') || 50,
    -SORT_FIELD1                            => $CGI->param('sort_field1') || 'start_date',
    -SORT_FIELD2                            => $CGI->param('sort_field2') || 'priority',
#    -SORT_DIRECTION                         => $CGI->param('sort_direction') || 'ASEN',
    -SORT_DIRECTION                         => 'DESC',
    -DELETE_FORM_VIEW_NAME                  => 'DetailsRecordView',
    -DELETE_EMAIL_BODY_VIEW                 => 'DeleteEventEmailView',
    -DETAILS_VIEW_NAME                      => 'DetailsRecordView',
    -DATA_HANDLER_MANAGER_CONFIG_PARAMS     => \@DATA_HANDLER_MANAGER_CONFIG_PARAMS,
    -DISPLAY_ACKNOWLEDGEMENT_ON_ADD_FLAG    => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_DELETE_FLAG => 1,
    -DISPLAY_ACKNOWLEDGEMENT_ON_MODIFY_FLAG => 1,
    -DISPLAY_CONFIRMATION_ON_ADD_FLAG       => 1,
    -DISPLAY_CONFIRMATION_ON_DELETE_FLAG    => 1,
    -DISPLAY_CONFIRMATION_ON_MODIFY_FLAG    => 1,
    -ENABLE_SORTING_FLAG                    => 1,
    -HAS_MEMBERS                            => $HasMembers,
    -HIDDEN_ADMIN_FIELDS_VIEW_NAME          => 'HiddenAdminFieldsView',
    -INPUT_WIDGET_DEFINITIONS               => \@INPUT_WIDGET_DEFINITIONS,
    -BASIC_INPUT_WIDGET_DISPLAY_COLSPAN     => 4,
    -KEY_FIELD                              => 'record_id',
    -LOGOFF_VIEW_NAME                       => 'LogoffView',
    -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME     => 'URLEncodedAdminFieldsView',
    -LOG_CONFIG_PARAMS                      => \@LOG_CONFIG_PARAMS,
    -MODIFY_ACKNOWLEDGEMENT_VIEW_NAME       => 'ModifyAcknowledgementView',
    -MODIFY_RECORD_CONFIRMATION_VIEW_NAME   => 'ModifyRecordConfirmationView',
    -MAIL_CONFIG_PARAMS                     => \@MAIL_CONFIG_PARAMS,
    -MAIL_SEND_PARAMS                       => \@MAIL_SEND_PARAMS,
    -MODIFY_FORM_VIEW_NAME                  => 'ModifyRecordView',
    -MODIFY_EMAIL_BODY_VIEW                 => 'ModifyEventEmailView',
    -POWER_SEARCH_VIEW_NAME                 => 'PowerSearchFormView',
    -REQUIRE_AUTH_FOR_SEARCHING_FLAG        => 0,
    -REQUIRE_AUTH_FOR_ADDING_FLAG           => 1,
    -REQUIRE_AUTH_FOR_MODIFYING_FLAG        => 1,
    -REQUIRE_AUTH_FOR_DELETING_FLAG         => 1,
    -REQUIRE_AUTH_FOR_VIEWING_DETAILS_FLAG  => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG => 0,
    -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG    => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG        => 0,
    -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG     => 0,
    -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG        => 0,
    -SEND_EMAIL_ON_DELETE_FLAG              => 0,
    -SEND_EMAIL_ON_MODIFY_FLAG              => 1,
    -SEND_EMAIL_ON_ADD_FLAG                 => 1,
    -SESSION_OBJECT                         => $SESSION,
    -SESSION_TIMEOUT_VIEW_NAME              => 'SessionTimeoutErrorView',
    -TEMPLATES_CACHE_DIRECTORY              => $TEMPLATES_CACHE_DIRECTORY,
    -VALID_VIEWS                            => \@VALID_VIEWS,
    -VIEW_DISPLAY_PARAMS                    => \@VIEW_DISPLAY_PARAMS,
    -VIEW_FILTERS_CONFIG_PARAMS             => \@VIEW_FILTERS_CONFIG_PARAMS,
    -VIEW_LOADER                            => $VIEW_LOADER,
    -SIMPLE_SEARCH_STRING                   => $CGI->param('simple_search_string') || "",
    -FIRST_RECORD_ON_PAGE                   => $CGI->param('first_record_to_display') || 0,
    -LAST_RECORD_ON_PAGE                    => $CGI->param('first_record_to_display') || "0",
    -SITE_NAME                              => $SiteName,
    -LAST_UPDATE                            => $last_update,
    -SITE_LAST_UPDATE                       => $site_update||2,
    -PAGE_TOP_VIEW                          => $page_top_view ,
    -LEFT_PAGE_VIEW                         => $left_page_view,
    -page_left_view                         => $page_left_view,
    -PAGE_BOTTOM_VIEW                       => $page_bottom_view,
    -AMPM_HOUR_DISPLAY 			            => $define_am_pm,
    -VALID_WORKING_HOURS                    => \@VALID_WORKING_HOURS,
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

