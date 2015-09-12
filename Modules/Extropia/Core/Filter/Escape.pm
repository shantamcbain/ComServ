#$Id: Escape.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::Escape;

# By Lyndon Drake <lyndon@kcbbs.gen.nz>
#
# Use this filter to escape data.  For example, you may wish to
# automatically escape < and > characters appearing in HTML code.
# You need to provide a hash from the < to some other string
# (e.g. "lt").  The filter will convert any occurrences of "<" to
# "~qqltqq~".  The filter only operates between configurable
# start and end tags, and the escape prefix and suffix are
# configurable.  Note that both the keys and the values in
# -ESCAPE_MAP are strings, not just characters.
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
    my ($self) =
        _rearrangeAsHash (
            [
                -ESCAPE_MAP,
                -ESCAPE_PREFIX,
                -ESCAPE_SUFFIX,
                -ESCAPE_START_TAG,
                -ESCAPE_END_TAG,
            ],
            [
                -ESCAPE_MAP
            ],
            @_);
    
    $self = _assignDefaults ($self,
        {
            -ESCAPE_PREFIX    => '~qq',
            -ESCAPE_SUFFIX    => 'qq~',
            -ESCAPE_START_TAG => '<!--START_ESCAPE-->',
            -ESCAPE_END_TAG   => '<!--END_ESCAPE-->'
        });

    return bless $self, $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);
                    
    my $content = shift;
    
    my $escape_map       = $self->{-ESCAPE_MAP};
    my $escape_start_tag = $self->{-ESCAPE_START_TAG};
    my $escape_end_tag   = $self->{-ESCAPE_END_TAG};
    my $escape_prefix    = $self->{-ESCAPE_PREFIX};
    my $escape_suffix    = $self->{-ESCAPE_SUFFIX};
    
# note the .*? instead of .* so that the regex is nongreedy
    foreach my $block ($content =~ /$escape_start_tag(.*?)$escape_end_tag/gs) {
        my ($key, $value);
        
        while (($key, $value) = each (%{$escape_map})) {
            $block =~ s/$key/$escape_prefix$value$escape_suffix/gs;
        }
        
        $content =~ s/$escape_start_tag.*?$escape_end_tag/$block/s;
    }

    return $content;
} # end of filter

1;
