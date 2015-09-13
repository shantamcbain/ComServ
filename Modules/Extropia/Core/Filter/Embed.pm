#$id$
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

package Extropia::Core::Filter::Embed;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash _rearrange);
use Extropia::Core::Filter;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Filter);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new Censor filter
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([-ENABLE],
                                  [],
                                  @_);

    return bless $self, $package;

} # end of new

#
# filter implements the interface to a filter...
#
sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],@_);
    
    my $content = shift;
    if (!$self->{'-ENABLE'}) {
        return $content;
    }
    my $modified_content;
#    $modified_content = "Content-type:text/html\n\n";

    my @lines = split("\n", $content);

    my $line;
    chomp($line);
    foreach $line (@lines) {
        $line =~ s/"/\\"/gs;
        $line =~ s/\cM/ /gs;
        if ($line =~ /^Content-/ ||
            $line =~ /^Expires/ ||
            $line =~ /^Date:/) {
           next;
        }
        $modified_content .= qq[document.write("$line");];
    }
    return $modified_content;

} # end of filter

1;
