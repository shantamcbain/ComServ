#$Id: Crypt.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Encrypt::Crypt;

use strict;
use Carp;
use Extropia::Core::Base qw(
    _rearrange 
    _rearrangeAsHash 
    _assignDefaults
);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Encrypt);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# $encrypt = new Extropia::Core::Encrypt(-TYPE => "crypt", -SALT => "42");
# $encrypted_text = $encrypt->encrypt($some_text);
# if ($encrypt->compare($some_text,$encrypted_text)) {
#   print "It matches\n";
# }
sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([-SALT],[],@_);

    $self = _assignDefaults($self, {-SALT => '42'});

    return bless $self, $package;
}

sub encrypt {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_ENCRYPT],[-CONTENT_TO_ENCRYPT],@_);

    my $content_to_encrypt = shift;
    my $encrypted_content  = ''; 

    eval { $encrypted_content =  crypt($content_to_encrypt,$self->{-SALT}); };
    if ($@) {
        die ("crypt() function call not supported on this version of " .
             "Perl or Operating System: $@");
    }
    return $encrypted_content;

}

sub compare {
    my $self = shift;
    @_ = _rearrange([-ENCRYPTED_CONTENT,-CONTENT_TO_COMPARE],
                    [-ENCRYPTED_CONTENT,-CONTENT_TO_COMPARE],@_);

    my $encrypted_content  = shift || "";
    my $content_to_compare = shift || "";

    my $encrypted_processing = $encrypted_content;
            
    # the following code is added for FreeBSD MD5 crypt
    if ($encrypted_content =~ /^\$1\$(..)\$(.*)/) {   
        $encrypted_processing = $1 . $2;
    } 

    # for crypt we add some code to use the salt
    # of the encrypted password if it used a different
    # salt...
                    
    my $old_salt = $self->{-SALT};
    $self->{-SALT} = substr($encrypted_processing,0,2);
    my $new_encrypted_content =
        $self->encrypt(-CONTENT_TO_ENCRYPT => $content_to_compare);
    $self->{-SALT} = $old_salt;

    return ($encrypted_content eq $new_encrypted_content);

} # end of compare

1;

