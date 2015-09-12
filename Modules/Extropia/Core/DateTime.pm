package Extropia::Core::DateTime;
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

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver);

use base qw(Extropia::Core::Base);

# constants used for dates comparison
use enum qw(LESS=-1 EQUAL=0 GREATER=1);

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::DateTime", $type) or
        Carp::croak("DateTime type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

package Extropia::Core::DateTime::Base;

# META: Fill in the functions
# These functions must be implemented in the child classes
my @not_implemented_subs = qw(
                             );

eval q{sub $_{_notImplemented((caller())[3]);} } for @not_implemented_subs;

use base qw(Extropia::Core::DateTime);

# here we put the methods which don't rely on the drivers

1;


__END__

