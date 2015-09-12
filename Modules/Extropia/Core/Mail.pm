package Extropia::Core::Mail;
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

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Base);

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::Mail", $type) or
        Carp::croak("Mail type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

sub send {
	_notImplemented((caller())[3]);
}

package Extropia::Core::Mail::Base;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Mail);

sub _format_send_param {
    my $self = shift;
    my $param = shift;
    my $ref_type = ref ($param);
    if ($ref_type eq "ARRAY") {
        return join (",", $param);
    }

    else {
        return $param;
    }
}

1;
