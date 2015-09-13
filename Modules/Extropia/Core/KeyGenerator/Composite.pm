#$Id: Composite.pm,v 1.2 2002/09/16 10:37:13 gozer Exp $
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

package Extropia::Core::KeyGenerator::Composite;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::KeyGenerator;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::KeyGenerator);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new KeyGenerator Object 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([-COMPOSITE_KEY_GENERATOR_PARAMS,
                                   -LENGTH,
                                   -ENCRYPT_PARAMS
                                  ],
                                  [-COMPOSITE_KEY_GENERATOR_PARAMS],
                                  @_);

# 0 length leaves hash length up to the hash algorithm itself
    $self = _assignDefaults($self,
                            {-SECRET_KEY => '42' x 8,
                             -LENGTH     => 0});
    
    return bless $self, $package;

} # end of new

sub createKey {
    my $self = shift;
    @_ = _rearrange([-EXTRA_ELEMENT],[],@_);

    my $extra_element = shift || "";

    my $secret = $self->{-SECRET_KEY} || "";
    my $length = $self->{-LENGTH};

    my $key_string = '';
    my $params;
    foreach $params (@{$self->{-KEY_GENERATOR_PARAMS}}) {
        my $kg = Extropia::Core::KeyGenerator->create(@$params);
        $key_string .= $kg->createKey(-EXTRA_ELEMENT => $extra_element);
    }

    return $self->_hash(-VALUE => $key_string, -LENGTH => $length);
}
1;
