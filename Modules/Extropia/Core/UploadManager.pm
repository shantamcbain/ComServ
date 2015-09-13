#$Id: UploadManager.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::UploadManager;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrange _getDriver _rearrangeAsHash);
use Extropia::Core::Session;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $upload_manager_class = 
        Extropia::Core::Base::_getDriver("Extropia::Core::UploadManager", $type) or
        Carp::croak("Extropia::Core::UploadManager type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $upload_manager_class->new(@fields);
}

#
# Drivers must implement the following methods
#
# downloadFile()
#

