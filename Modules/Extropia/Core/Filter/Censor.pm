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

package Extropia::Core::Filter::Censor;

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
    my ($self) = _rearrangeAsHash([-WORDS_TO_FILTER,-REPLACEMENT_WORD,-CASE_SENSITIVE],
                                  [-WORDS_TO_FILTER],
                                  @_);

    if (!defined($self->{-CASE_SENSITIVE})) {
        $self->{-CASE_SENSITIVE} = 1;
    }
    if (!$self->{-REPLACEMENT_WORD}) {
        $self->{-REPLACEMENT_WORD} = "[CENSORED]";
    }
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

    my $ra_words_to_filter = $self->{-WORDS_TO_FILTER};
    my $replacement_word   = $self->{-REPLACEMENT_WORD};
    my $case_sensitive     = $self->{-CASE_SENSITIVE};

    my $word;
    foreach $word (@$ra_words_to_filter) {
        if ($case_sensitive) {
            $content =~ s/$word/$replacement_word/g;
        } else {
            $content =~ s/$word/$replacement_word/gi;
        }
    } 
    return $content;

} # end of filter

1;
