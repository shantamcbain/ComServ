#$Id: Temperature.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
# Extropia::Core::DataHandler::Temperature
#
####################################################
package Extropia::Core::DataHandler::Temperature;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -CONVERT_F_TO_C    => [$self,\&convertFToC],
        -CONVERT_C_TO_F    => [$self,\&convertCToF],
        -CONVERT_C_TO_K    => [$self,\&convertCToK],
        -CONVERT_K_TO_C    => [$self,\&convertKToC]
    };

} # getHandlerRules

#
# convertFToC converts from Fahrenheit to Celsius
#
sub convertFToC {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    $field = "" if (!defined($field));

    $field = ($field - 32) / 9 * 5;

    return $field;

} # end of convertFToC

#
# convertCToF converts from Celsius to Fahrenheit
#
sub convertCToF {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    $field = "" if (!defined($field));

    $field = $field * 9 / 5 + 32;

    return $field;

} # end of convertCToF

#
# convertCToK converts from Celsius to Kelvin
#
# Of course, our conversions could be more precise...
#
sub convertCToK {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    $field = "" if (!defined($field));

    $field = $field + 273;

    return $field;

} # end of convertCToK

#
# convertKToC converts from Celsius to Kelvin
#
# Of course, our conversions could be more precise...
#
sub convertKToC {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    $field = "" if (!defined($field));

    $field = $field - 273;

    return $field;

} # end of convertKToC

1;
