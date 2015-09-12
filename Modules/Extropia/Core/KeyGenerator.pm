#$Id: KeyGenerator.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::KeyGenerator;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::KeyGenerator", $type) or
        Carp::croak("KeyGenerator type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

#
# METHODS to implement in subclass
#
# createKey
#

####################################################
#
# METHODS FOR USE IN SUBCLASSED DRIVERS 
#
####################################################

sub _hash {
    my $self   = shift;
    @_ = _rearrange([-VALUE, -LENGTH], [-VALUE], @_);

    my $value  = shift;
    my $length = shift;

    if (!$self->{-ENCRYPT_PARAMS}) {
        $self->{-ENCRYPT_PARAMS} = 
            [
                -TYPE => 'Succession',
                -CHAIN_OF_ENCRYPT_PARAMS =>
                [
                    [-TYPE => 'SHA'],
                    [-TYPE => 'MD5'],
                    [-TYPE => 'ASCIIHash']
                ]
            ];
    }

    require Extropia::Core::Encrypt;
    my $encrypt = Extropia::Core::Encrypt->create(@{$self->{-ENCRYPT_PARAMS}});
    
    my $hashed_key = $encrypt->encrypt(-CONTENT_TO_ENCRYPT => $value);

    if ($length) {
        $hashed_key = substr($hashed_key,0,$length);
    }
    return $hashed_key;

} # end of _hash

1;
