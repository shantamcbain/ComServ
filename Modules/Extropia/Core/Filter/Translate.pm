#$Id: Translate.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::Translate;

# By Lyndon Drake <lyndon@kcbbs.gen.nz>
#
# This filter simply replaces each key in the supplied hash
# with the corresponding value.  It is useful for globally
# replacing strings.
#

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Filter;

use vars qw($VERSION @ISA);

$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::Filter::Base);

sub new {
    my $package = shift;
    my ($self) =_rearrangeAsHash ([
        -TRANSLATE_MAP,
        -TRANSLATE_START_TAG,
        -TRANSLATE_END_TAG,
            ],
            [
        -TRANSLATE_MAP
            ],
        @_
       );

   $self = _assignDefaults ($self,
        {
            '-TRANSLATE_START_TAG' => '<!--__START_TRANSLATE__-->',
            '-TRANSLATE_END_TAG'   => '<!--__END_TRANSLATE__-->'
        });
    

    return bless $self, $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);
                    
    my $content = shift;

    my $translate_start_tag = $self->{-TRANSLATE_START_TAG};
    my $translate_end_tag   = $self->{-TRANSLATE_END_TAG};
    my $translate_map       = $self->{-TRANSLATE_MAP};

    my ($key, $value);
    my $block;
    foreach $block ($content =~ /$translate_start_tag(.*?)$translate_end_tag/gs) {
        while (($key, $value) = each (%{$translate_map})) {
            $block =~ s/$key/$value/gs;
        }
    $content =~ s/$translate_start_tag.*?$translate_end_tag/$block/s;
    }


    return $content;
} # end of filter

1;
