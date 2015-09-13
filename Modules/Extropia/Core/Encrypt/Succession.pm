#$Id: Succession.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Encrypt::Succession;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Encrypt);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $encrypt = new Extropia::Core::Encrypt(-TYPE => "md5");
# $encrypted_text = $encrypt->encrypt($some_text);
# if ($encrypt->compare($some_text,$encrypted_text)) {
#   print "It matches\n";
# }
sub new {
    my $package = shift;

    my $self;
    ($self, @_) = _rearrangeAsHash([-CHAIN_OF_ENCRYPT_PARAMS],
                                   [-CHAIN_OF_ENCRYPT_PARAMS],@_);

    return bless $self, $package;
}

sub encrypt {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_ENCRYPT],[-CONTENT_TO_ENCRYPT],@_);

    my $content_to_encrypt = shift;

    if (!$self->{_encrypt_object_chain}) {
        my @encrypt_object_chain;
        my $param;
        foreach $param (@{$self->{-CHAIN_OF_ENCRYPT_PARAMS}}) {
            my $encrypt = Extropia::Core::Encrypt->create(@$param);
            push(@encrypt_object_chain,$encrypt);
        }
        $self->{_encrypt_object_chain} = \@encrypt_object_chain;
    }
    
    my $encrypt;
    my $encrypt_success = 0;
    my $encrypted_content;
    foreach $encrypt (@{$self->{_encrypt_object_chain}}) {
        eval { $encrypted_content =
                    $encrypt->encrypt(-CONTENT_TO_ENCRYPT =>
                                         $content_to_encrypt); 
        };
        if (!$@) {
            $encrypt_success = 1;    
            last;
        }
    }
    if (!$encrypt_success) {
        die("Encryption was not successful: $@.");
    }
    return $encrypted_content;
}

1;

