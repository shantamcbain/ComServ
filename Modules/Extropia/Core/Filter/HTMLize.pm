#$Id: HTMLize.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::HTMLize;

# By Lyndon Drake <lyndon@kcbbs.gen.nz>
#
# Use this filter to automagically convert carriage returns to
# <BR> and/or <P> tags, and HTTP and mailto URLs to <A HREF>
# tags.  The filter only operates on text between configurable
# start and end tags, and each of the operations is optional.
# 

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
                -HTMLIZE_START_TAG,
                -HTMLIZE_END_TAG,
                -CONVERT_DOUBLE_LINEBREAK_TO_P,
                -CONVERT_LINEBREAK_TO_BR,
                -CONVERT_HTTP_URL_TO_A,
                -CONVERT_MAILTO_URL_TO_A,
            ],
            [
            ],
            @_);
    
    $self = _assignDefaults ($self,
        {
            '-HTMLIZE_START_TAG' => '<!--__START_HTMLIZE__-->',
            '-HTMLIZE_END_TAG' => '<!--__END_HTMLIZE__-->'
        });

    return bless $self, $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);
                    
    my $content = shift;
    
    my $htmlize_start_tag = $self->{-HTMLIZE_START_TAG};
    my $htmlize_end_tag   = $self->{-HTMLIZE_END_TAG};
    my $convert_double_linebreak_to_p = $self->{-CONVERT_DOUBLE_LINEBREAK_TO_P};
    my $convert_linebreak_to_br       = $self->{-CONVERT_LINEBREAK_TO_BR};
    my $convert_http_url_to_a         = $self->{-CONVERT_HTTP_URL_TO_A};
    my $convert_mailto_url_to_a       = $self->{-CONVERT_MAILTO_URL_TO_A};
    
    foreach my $block ($content =~ /$htmlize_start_tag(.*?)$htmlize_end_tag/gs) {
        # convert double carriage returns to <P> tags
        if (defined ($convert_double_linebreak_to_p)) {
            $block =~ s/\r\n\r\n|\r\r|\n\n/<P>/g;
        }
        # convert carriage returns to <BR> tags
        if (defined ($convert_linebreak_to_br)) {
            $block =~ s/\r\n|\r|\n/<BR>/g;
        }
        # convert HTTP URLs to <A HREF=""> tags (i.e. links)
        if (defined ($convert_http_url_to_a)) {
            $block =~ s{(http:[;/?:@&#=+$,.!~*'()\w]*)} {<A HREF="$1">$1</A>}g;
        }
        # convert MAILTO URLs to <A HREF=""> tags
        if (defined ($convert_mailto_url_to_a)) {
            $block =~ s{(mailto:[;/?:@&#=+$,.!~*'()\w]*)} {<A HREF="$1">$1</A>}g;
        }

        $content =~ s/$htmlize_start_tag.*?$htmlize_end_tag/$block/s;
    }
    
    return $content;
} # end of filter

1;
