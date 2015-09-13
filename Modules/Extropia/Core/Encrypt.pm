#$Id: Encrypt.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Encrypt;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $encrypt = Extropia::Core::Encrypt->create(-TYPE => "pgp",
#                   -FILE => "filename",
#                   -TIMEOUT => 10,
#                   -TRIES   => 5);
# $encrypted_text = $encrypt->encrypt($some_text);
# if ($encrypt->compare($some_text,$encrypted_text)) {
#   print "It matches\n";
# }
sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::Encrypt", $type) or
        Carp::croak("Extropia::Core::Encrypt type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);

} # end of create

#
# methods that should be implemented in drivers:
# encrypt
# compare
# 
# A sample compare is already implemented below
#

sub compare {
    my $self = shift;
    @_ = _rearrange([-ENCRYPTED_CONTENT,-CONTENT_TO_COMPARE],
                    [-ENCRYPTED_CONTENT,-CONTENT_TO_COMPARE],@_);
    
    my $encrypted_content  = shift || "";
    my $content_to_compare = shift || "";

    my $new_encrypted_content = $self->encrypt($content_to_compare);

    return ($encrypted_content eq $new_encrypted_content);

} # end of compare

1;

