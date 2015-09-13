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

package Extropia::Core::AuthManager::CGI::UserMailBodyView;


use strict;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::View;

use Extropia::Core::AuthManager::CGI::BaseView;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::View);

sub display {
    my $self = shift;
    @_ = _rearrange([-USERNAME,
                     -PASSWORD
                     ],[
                     -USERNAME,
                     -PASSWORD
                     ],@_);
 
    my $username = shift;
    my $password = shift;

    return qq[
Congratulations! You've been accepted into our
system.  You may now logon with your username of
$username and your password of $password.

Thanks!
];
       
}

1;
