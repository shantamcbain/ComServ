#$Id: Email.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
# Copyright (C) 1996  eXtropia.com
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

####################################################
#
# Extropia::Core::DataHandler::Email
#
####################################################
package Extropia::Core::DataHandler::Email;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -IS_EMAIL          => [$self,\&isEmail],
        -IS_NOT_EMAIL      => [$self,\&isNotEmail],
        -UNTAINT_EMAIL     => [$self,\&untaintEmail]
    };

} # getHandlerRules

#
# isEmail does a rough check for email validity. Could be 
# made stronger eg by doing MX record DNS lookups to test
# host validity etc.
#
sub isEmail {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [],@_);

    my $field      = shift;
    $field = "" if (!defined($field));

    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid email.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # Note that if a field is blank we consider it
    # to be valid...

    if ($field =~ /^\s*$/ ||
        $field =~ /
                   ^                  # Start from the beginning
                   \s*                # Any amount of whitespace
                   \w{1}              # One word character
                   [\w\-.=+~!#$%^&\/]* # Any email characters
                   \@                 # One @ symbol
                   [\w\-_.]+           # Any word chars, hypehns, _ or .
                   \.\w{2,3}          # End with a period and 2-3 word chars
                   \s*$               # Any amount of whitespace to the end
                  /x) {
        return 1;
    } else {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    }

} # end of isEmail

sub isNotEmail{
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field may not be an email address.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # Note that if a field is blank we consider it
    # to be valid...

    if ($field =~ /^\s*$/ ||
        $field =~ /
                   ^                  # Start from the beginning
                   \s*                # Any amount of whitespace
                   \w{1}              # One word character
                   [\w\-.=+~!#$%^&\/]* # Any email characters
                   \@                 # One @ symbol
                   [\w\-_.]+           # Any word chars, hypehns, _ or .
                   \.\w{2,3}          # End with a period and 2-3 word chars
                   \s*$               # Any amount of whitespace to the end
                  /x) {

        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    }
    return 1;
}

#
# untaintEmail basically untaints an intended email
# variable by specifying the valid characters for an email
# which typically will not include shell escape characters
#
# See isEmail for information on further untaint checks that
# could theoretically be done.
#
sub untaintEmail {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE],
                    [],@_);

    my $field      = shift;
    my $field_name = shift || "unknown";
    my $error_msg  = shift || 
            "%FIELD_NAME% field: %FIELD_VALUE% could not be untainted.";

    return undef if (!defined($field));

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # if the isXXXX method has a more stringent way of
    # untainting then we check this as well as a double
    # check.

    if (($self->isEmail(-FIELD_VALUE => $field,-ADD_ERROR => 0)) &&
        $field =~ /
                   ^                  # Start from the beginning
                   \s*                # Any amount of whitespace
                   (\w{1}             # One word character
                   [\w\-.+]*           # Any untaintable email characters
                                      # not including many shell
                                      # metacharacters
                   \@                 # One @ symbol
                   [\w\-_.]+           # Any word chars, hypehns, _ or .
                   \.\w{2,3})         # End with a period and 2-3 word chars
                   \s*$               # Any amount of whitespace to the end
                  /x) {
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintEmail

1;
