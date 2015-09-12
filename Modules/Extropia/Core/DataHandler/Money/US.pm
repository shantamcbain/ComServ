#$Id: US.pm,v 1.2 2001/05/19 12:18:34 gunther Exp $
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
# Extropia::Core::DataHandler::Money::US
#
####################################################
package Extropia::Core::DataHandler::Money::US;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;
            
    return {
        -IS_MONEY      => [$self,\&isMoney],
        -FORMAT_MONEY  => [$self,\&formatMoney],
        -UNTAINT_MONEY => [$self,\&untaintMoney]
    };

} # getHandlerRules

#
# isMoney checks whether a field looks roughly like a money
# value. Specifically becauase this is a US money class, we
# check for things like starting with a $ symbol (optional).
# and having two decimal places.
#
# We use a fairly complex regex to do the checking. Additional
# non-regex logic could conceivably parse the number better.
#
# The following regex is used
#
# Optional - symbol: -
# Optional ( symbol: \(?
# Optional $ symbol: \$?
# Followed by optional whitespace: \s*
# Followed by optional hyphen: -?
# Followed by optional (: \(?
# Followed by optional digit or commas
# Followed by mandatory .
# Followed by mandatory two digits
# Followed by optional ): \)?
# 
# Thus, at minimum, it must match .00 
# But could also match
# $0.00, $(0.00), -$0.00, ($0.00). etc...
#
# Note that we manually allow nothing to pass through because
# no value is also considered valid currency
#
sub isMoney {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid currency.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid currency since it hasn't actually
    # failed a test.
    #    

    if ($field =~ /^\s*$/ ||
        $field =~ /^
                   \s*    # optional whitespace
                   -?     # Optional - symbol
                   \(?    # Optional ( symbol
                   \$?    # Optional $ symbol
                   \s*    # Followed by optional whitespace
                   -?     # Followed by optional hyphen
                   \(?    # Followed by optional (
                   [\d,]* # Followed by optional digit or commas
                   \.     # Followed by mandatory .
                   \d\d   # Followed by mandatory two digits
                   \)?    # Followed by optional )
                   \s*    # optional whitespace
                  $/x) {   
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

} # end of isMoney

#
# formatMoney
#
# Takes an optional -INPUT_FORMAT (to decode)
# and outputs an output format specified by -OUTPUT_FORMAT
#
# Add an error if the transform did not work...
#
sub formatMoney {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-OUTPUT_FORMAT,-INPUT_FORMAT,
                     -FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE,-OUTPUT_FORMAT],@_);

    my $field         = shift;
    $field = "" if (!defined($field));
    my $input_format  = shift || "";
    my $output_format = shift || "";
    my $field_name    = shift || "";
    my $error_msg     = shift || "%FIELD_NAME% field is not a valid currency.";

    if ($field eq "MONEY") {
        
        # stub in no change for now...

        return $field;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of formatMoney

#
# untaintMoney uses the same basic regex in isMoney to
# determine whether to untaint it.
#
sub untaintMoney {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE],@_);

    my $field         = shift;
    $field = "" if (!defined($field));
    my $field_name    = shift || "";
    my $error_msg     = shift || "%FIELD_NAME% field is not a valid currency.";

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # if the isXXXX method has a more stringent way of
    # untainting then we check this as well as a double
    # check.

    if ($self->isMoney(-FIELD_VALUE => $field, -ADD_ERROR => 0) &&
        $field =~ /^
                   \s*    # optional whitespace
                   (-?    # Optional - symbol
                   \(?    # Optional ( symbol
                   \$?    # Optional $ symbol
                   \s*    # Followed by optional whitespace
                   -?     # Followed by optional hyphen
                   \(?    # Followed by optional (
                   [\d,]* # Followed by optional digit or commas
                   \.     # Followed by mandatory .
                   \d\d   # Followed by mandatory two digits
                   \)?)   # Followed by optional )
                   \s*    # optional whitespace
                  $/x) {   
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintMoney

1;
