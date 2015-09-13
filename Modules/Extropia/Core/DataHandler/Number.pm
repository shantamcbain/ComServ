#$Id: Number.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
# Extropia::Core::DataHandler::Number
#
####################################################
package Extropia::Core::DataHandler::Number;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -IS_NUMBER          => [$self,\&isNumber],
        -FORMAT_NUMBER      => [$self,\&formatNumber],
        -UNTAINT_NUMBER     => [$self,\&untaintNumber],
        -IS_BETWEEN_NUMBERS => [$self,\&isBetweenNumbers]
    };

} # getHandlerRules

#
# isNumber checks whether the field provided is a number
# Of course, we could do more than just use a regex, but 
# for now this is powerful enough for a basic class.
#
sub isNumber {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid number.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid number since it hasn't actually
    # failed a test.
    if ($field =~ /^\s*$/ ||
        $field =~ /^\s*-?[\d.,]*\s*$/) {
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

} # end of isNumber

#
# formatNumber takes a -FORMAT and transforms it into that
# format...
#
# Format's are used in an Excel way.
#
sub formatNumber {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE, -FORMAT,-FIELD_NAME,-ERROR_MESSAGE],
                    [-FORMAT],@_);

    my $field      = shift;
    my $format     = shift || "###.00";
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid number.";

    # stub in no change for now.
    if (defined($field)) {
         return $field;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of formatNumber

#
# sprintfNumber takes a -FORMAT in sprintf style
# and transforms it into that into the sprintf format.
#
sub sprintfNumber {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FORMAT,-FIELD_NAME,-ERROR_MESSAGE],
                    [-FORMAT],@_);

    my $field      = shift;
    my $format     = shift || "%.2f";
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid number.";

    if (!$self->isNumber(-FIELD_VALUE => $field,-ADD_ERROR => 0)) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
        return undef;
    }

    if ($field) {
         return sprintf($format,$field);
    } else {
        return '';
    }

} # end of sprintfNumber

#
# untaintNumber basically untaints a number
# based on the regex from isNumber
#
sub untaintNumber {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE],[],@_);

    my $field      = shift;
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid number.";

    return undef if (!defined($field));

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # if the isXXXX method has a more stringent way of
    # untainting then we check this as well as a double
    # check.

    if ($self->isNumber(-FIELD_VALUE => $field,-ADD_ERROR => 0) &&
        $field =~ /^\s*(-?[\d.,]*)\s*$/) {
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintNumber

#
# isBetweenNumbers checks whether the field provided is
# between two numbers (inclusive)
#
sub isBetweenNumbers {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,
                     -LOW_RANGE,-HIGH_RANGE,
                     -ERROR_MESSAGE],
                    [],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $low_range  = shift || 0;
    my $high_range = shift || 0;
    my $error_msg  = shift || 
         "%FIELD_NAME% field is not between $low_range and $high_range.";

    # note that we consider nothing to be
    # a valid number since it hasn't actually
    # failed a test.

    if (!$field) {
        return 1;
    }

    elsif ($field >= $low_range &&
        $field <= $high_range) {
        return 1;

    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
        return undef;
    }

} # end of isBetweenNumbers

1;

