# $Id: Number.pm,v 1.3 2001/05/15 08:37:35 stas Exp $
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


package Extropia::Core::DataSource::DataType::Number;

use strict;
use Extropia::Core::DataSource::DataType;
use vars qw(@ISA);

@ISA = ('Extropia::Core::DataSource::DataType');

sub compare {
    if (!defined $_[1]) {
        return -(defined $_[2]);
    } elsif (!defined $_[2]) {
        return 1;
    } else {
        return ($_[1] <=> $_[2]);
    }
}

sub getOdbcType {
    if ($DBI::VERSION) {
        return DBI::SQL_NUMERIC();
    }
    return 2;
}

sub storage2internal { return $_[1]; }
sub internal2storage { return $_[1]; }
sub display2internal { return $_[1]; }
sub internal2display { return $_[1]; }

sub isValid {
    my ($self, $value) = @_;
    if (defined $value) {
        if ($value =~ /\d/ && 
            $value =~ /^[+-]?\d*\.?\d*(?:\d[eE][+-]?\d+)?$/) {
            return 1;
        }
        return 0;
    }
    else {
        return 1;
    }
}

1;
