package Default::CheckForLogicalConfigurationErrorsAction;

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
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::Action;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([
        -ACTION_HANDLER_LIST,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -HIDDEN_ADMIN_FIELDS_VIEW_NAME,
        -URL_ENCODED_ADMIN_FIELDS_VIEW_NAME,
        -DEFAULT_MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -REQUIRE_AUTH_FOR_ADDING_FLAG,
        -REQUIRE_AUTH_FOR_MODIFYING_FLAG,
        -REQUIRE_AUTH_FOR_DELETING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -VIEW_LOADER,
        -VALID_VIEWS,
        -MAIL_CONFIG_PARAMS,
        -SEND_EMAIL_ON_DELETE_FLAG,
        -SEND_EMAIL_ON_MODIFY_FLAG,
        -SEND_EMAIL_ON_ADD_FLAG,
        -MAIL_SEND_PARAMS,
        -DELETE_EMAIL_BODY_VIEW,
        -ADD_EMAIL_BODY_VIEW,
        -MODIFY_EMAIL_BODY_VIEW,
            ],
            [
        -ACTION_HANDLER_LIST,
        -DATASOURCE_CONFIG_PARAMS,
        -VALID_VIEWS,
        -VIEW_LOADER
            ],
        @_);

    my $cgi = $params->{'-CGI_OBJECT'};

    if ($params->{'-SEND_EMAIL_ON_MODIFY_FLAG'}) {
        if (!$params->{'-MAIL_CONFIG_PARAMS'} ||
            !$params->{'-MODIFY_EMAIL_BODY_VIEW'} ||
            !$params->{'-MAIL_SEND_PARAMS'}) {
            die("Whoopsy! In order to send mail, you must specify " .
                "-MAIL_CONFIG_PARAMS and -MODIFY_EVENT_MAIL_SEND_PARAMS");
        }
    }

    if ($params->{'-SEND_EMAIL_ON_ADD_FLAG'}) {
        if (!$params->{'-MAIL_CONFIG_PARAMS'} ||
            !$params->{'-ADD_EMAIL_BODY_VIEW'} ||
            !$params->{'-MAIL_SEND_PARAMS'}) {
            die("Whoopsy! In order to send mail, you must specify " .
                "-MAIL_CONFIG_PARAMS and -ADD_EVENT_MAIL_SEND_PARAMS");
        }
    }

    if ($params->{'-SEND_EMAIL_ON_DELETE_FLAG'}) {
        if (!$params->{'-MAIL_CONFIG_PARAMS'} ||
            !$params->{'-DELETE_EMAIL_BODY_VIEW'} ||
            !$params->{'-MAIL_SEND_PARAMS'}) {
            die("Whoopsy! In order to send mail, you must specify " .
                "-MAIL_CONFIG_PARAMS and -DELETE_EVENT_MAIL_SEND_PARAMS");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_SEARCHING_FLAG'}) {
            die("Whoopsy! In order to require matching username " .
                " for searching, you must set -REQUIRE_AUTH_FOR_SEARCHING_FLAG " .
                " equal to 1");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_SEARCHING_FLAG'}) {
            die("Whoopsy! In order to require matching group " .
                " for searching, you must set -REQUIRE_AUTH_FOR_SEARCHING_FLAG " .
                " equal to 1");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_MODIFYING_FLAG'}) {
            die("Whoopsy! In order to require matching username " .
                " for modifying, you must set -REQUIRE_AUTH_FOR_MODIFYING_FLAG " .
                " equal to 1");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_MODIFYING_FLAG'}) {
            die("Whoopsy! In order to require matching group " .
                " for modifying, you must set -REQUIRE_AUTH_FOR_MODIFYING_FLAG " .
                " equal to 1");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_DELETING_FLAG'}) {
            die("Whoopsy! In order to require matching username " .
                " for deleting, you must set -REQUIRE_AUTH_FOR_DELETING_FLAG " .
                " equal to 1");
        }
    }

    if ($params->{'-REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG'}) {
        if (!$params->{'-REQUIRE_AUTH_FOR_DELETING_FLAG'}) {
            die("Whoopsy! In order to require matching group " .
                " for deleting, you must set -REQUIRE_AUTH_FOR_DELETING_FLAG " .
                " equal to 1");
        }
    }

    my @config_params = _rearrange([
        -BASIC_DATASOURCE_CONFIG_PARAMS
            ],
            [
        -BASIC_DATASOURCE_CONFIG_PARAMS
            ],
        @{$params->{'-DATASOURCE_CONFIG_PARAMS'}}
    );

    my $datasource_config_params = shift (@config_params);

    my @datasource_config_fields = _rearrange([
        -FIELD_NAMES
            ],
            [
        -FIELD_NAMES
            ],
        @$datasource_config_params
    );

    my $datasource_fields = shift(@datasource_config_fields);

    if ($params->{'-REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG'} ||
        $params->{'-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG'} ||
        $params->{'-REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG'}) {

       my $field;
       my $found = 0;

       foreach $field (@$datasource_fields) {
           if ($field eq "username_of_poster") {
               $found = 1;
           }
       }

       if (!$found) {
           die("Whoopsy! In order to use authentication, you must specify " .
               "the username_of_poster field in the datasource configuration. " .
               "In particular, add the field to the \@DATASOURCE_FIELD_NAMES  " .
               "array in the application executable (eg address_book.cgi).  " .
               "We recommend adding it to the end of the list, but it does " .
               "really matter all that much.");
       }

    }

    if ($params->{'-REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG'} ||
        $params->{'-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG'} ||
        $params->{'-REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG'}) {

       my $field;
       my $found = 0;

       foreach $field (@$datasource_fields) {
           if ($field eq "group_of_poster") {
               $found = 1;
           }
       }

       if (!$found) {
           die("Whoopsy! In order to use authentication, you must specify " .
               "the group_of_poster field in the datasource configuration. " .
               "In particular, add the field to the \@DATASOURCE_FIELD_NAMES  " .
               "array in the application executable (eg address_book.cgi).  " .
               "We recommend adding it to the end of the list, but it does " .
               "really matter all that much.");
       }
    }

    return 2;
}
