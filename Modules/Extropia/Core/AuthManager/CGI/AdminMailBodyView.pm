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

package Extropia::Core::AuthManager::CGI::AdminMailBodyView;


use strict;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::View;

use Extropia::Core::AuthManager::CGI::BaseView;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::View);

sub display {
    my $self = shift;
    @_ = _rearrange([-USER_FIELD_NAME_TO_VALUE_MAPPING,
                     -USER_FIELD_TYPES
                     ],[
                     -USER_FIELD_NAME_TO_VALUE_MAPPING,
                     -USER_FIELD_TYPES
                     ],@_);
 
    my $user_field_name_to_value_mapping = shift;
    my $user_field_types                 = shift;

    my $username_field = $user_field_types->{-USERNAME_FIELD};
    my $username = $user_field_name_to_value_mapping->{$username_field};

    return qq[
A user by the username of $username has applied to the system.
];
       
}

1;
