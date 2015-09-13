#$Id: EscapeHTML.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::EscapeHTML;

#
# Use this filter to explicitly escape HTML within visible form
# fields using the same basic algorithm as CGI.pm's escapeHTML()
# method
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
                -ESCAPE_START_TAG,
                -ESCAPE_END_TAG,
            ],
            [
            ],
            @_);
    
    $self = _assignDefaults ($self,
        {
            -ESCAPE_START_TAG => '<!--START_HTML_ESCAPE-->',
            -ESCAPE_END_TAG   => '<!--END_HTML_ESCAPE-->'
        });

    return bless $self, ref($package) | $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);
                    
    my $content = shift;
    
    return undef unless defined($content);
                       
# note the .*? so that the regex is non-greedy.
    foreach my $block ($content =~ /\"$escape_start_tag(.*?)$escape_end_tag\"/gs) {
        
        $block =~ s/&/&amp;/g;
        $block =~ s/\"/&quot;/g;
        $block =~ s/>/&gt;/g;
        $block =~ s/</&lt;/g;
        
        $content =~ s/(\")$escape_start_tag.*?$escape_end_tag(\")/\1$block\2/s;
    }

    return $content;
} # end of filter

1;
