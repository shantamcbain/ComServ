#$Id: URLEncode.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::URLEncode;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Filter;

use vars qw($VERSION @ISA);

$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::Filter);

sub new {
    my $package = shift;
    my ($self) =
        _rearrangeAsHash (
            [
                -ENCODE_START_TAG,
                -ENCODE_END_TAG,
            ],
            [
            ],
            @_);
    
    $self = _assignDefaults ($self,
        {
            -ENCODE_START_TAG => '<!--START_URL_ENCODE-->',
            -ENCODE_END_TAG   => '<!--END_URL_ENCODE-->'
        });

    return bless $self, $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);

    my $start_tag = $self->{-ENCODE_START_TAG};
    my $end_tag   = $self->{-ENCODE_END_TAG};

    my $content = shift;
    
    return undef unless defined($content);

    my $block;
    foreach $block ($content =~ /$start_tag(.*?)$end_tag/gs) {
        $block =~ s/ /%20/g;
        $block =~ s/!/%21/g;
        $block =~ s/"/%22/g;
        $block =~ s/#/%23/g;
        $block =~ s/%/%25/g;
        $block =~ s/&/%26/g;
        $block =~ s/'/%27/g;
        $block =~ s/\+/%2B/g;
        $block =~ s/=/%3D/g;
        $block =~ s/\?/%3F/g;
        $content =~ s/$start_tag.*?$end_tag/$block/s;
    }


    return $content;
} # end of filter

1;
