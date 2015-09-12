# $Id: Default.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::DataSource::Locale::Default;

use strict;
use Extropia::Core::DataSource::Locale;
use Extropia::Core::DataSource::DataType;
use Extropia::Core::Base qw(_rearrange);

use vars qw(@ISA);
@ISA = ('Extropia::Core::DataSource::Locale');

sub getDataType {
    my $self = shift;
    my @args = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift @args;
    return Extropia::Core::DataSource::DataType->create(-TYPE => $type, @args);
}

1;
