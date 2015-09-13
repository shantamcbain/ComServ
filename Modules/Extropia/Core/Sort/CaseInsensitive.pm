# $Id: CaseInsensitive.pm,v 1.1.1.1 2001/03/12 05:38:32 stas Exp $
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

package Extropia::Core::Sort::CaseInsensitive;
use strict;

sub new {
    my $package = shift;
    return bless [], ref $package || $package;
}

sub compare {
    if (!defined $_[1]) {
        return -(defined $_[2]);
    } elsif (!defined $_[2]) {
        return 1;
    } else {
        return (uc($_[1]) cmp uc($_[2]));
    }
}

1;
