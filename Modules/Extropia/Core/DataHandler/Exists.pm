#$Id: Exists.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
# Extropia::Core::DataHandler::Exists does the required
# fields checking
#
####################################################
package Extropia::Core::DataHandler::Exists;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
       -IS_FILLED_IN                   => [$self,\&isFilledIn]
    };
} # getHandlerRules

#
# isFilledIn returns true if the field was filled
# in. Used to check for requried fields.
#
sub isFilledIn {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -ERROR_MESSAGE, 
        -STRINGS_CONSIDERED_BLANK,
            ],
            [
            ],
        @_
    );

    my $field      = shift;
    $field = "" if (!defined($field));

    if (!defined ($field)) {
        $field = "";
    }

# If the field is just filled with whitespace its not
# really filled in...
    $field =~ s/^\s+$//;

    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not filled in.";
    my $ra_strings_considered_blank = shift;

    if (length($field) > 0) {
        if ($ra_strings_considered_blank) {
            my $string;
            foreach $string (@$ra_strings_considered_blank) {
                if ($string eq $field) {
                    $self->addError(new Extropia::Core::Error(
                        -MESSAGE => $self->_getMessage($field_name, $field, $error_msg))
                    );
                    return undef;
                }
            }
        }
        return 1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
        return undef;
    }

} # end of isFilledIn

1;

