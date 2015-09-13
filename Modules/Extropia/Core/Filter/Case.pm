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

package Extropia::Core::Filter::Case;

     # NOTE THAT THIS FILTER WAS KINDLY DONATED TO THE OPEN SOURCE COMMUNITY BY
     # Henryk Bochmann (bochmann-usenet0499@gmx.net)


use strict;
use Carp;
use Extropia::Core::Base qw(_rearrangeAsHash _rearrange _assignDefaults);
use Extropia::Core::Filter;
use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Filter);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf "%d."."%02d" x $#r, @r};

sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash(
            [
        -TO_UPPER,
        -TO_LOWER,
        -CASE_FILTER_START_TAG,
        -CASE_FILTER_END_TAG,
            ],
            [
            ],
        @_
    );

    $self = _assignDefaults ($self,
        {
            -CASE_FILTER_START_TAG => '<!--__START_CASE_FILTER__-->',
            -CASE_FILTER_END_TAG   => '<!--__END_CASE_FILTER__-->',
            -TO_UPPER              => 0,
            -TO_LOWER              => 0
        });

    return bless $self, $package;
}

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER], [-CONTENT_TO_FILTER],@_);

    my $start_tag = $self->{-CASE_FILTER_START_TAG};
    my $end_tag   = $self->{-CASE_FILTER_END_TAG};

    my $content = shift;

    my $to_upper = $self->{-TO_UPPER};
    my $to_lower = $self->{-TO_LOWER};
    my $case_filter_error = 'Setup error - Choose either upper case or lower case filter.';

    my $block;
    foreach $block ($content =~ /$start_tag(.*?)$end_tag/gs) {
        if ($to_upper) {
            $block =~ tr/[a-z]/[A-Z]/;
        }

        elsif ($to_lower) {
           $block =~ tr/[A-Z]/[a-z]/;
        }
                          
        else {
            $block =~ s/$block/$case_filter_error/g;
        }

        $content =~ s/$start_tag.*?$end_tag/$block/s;
    }
                         
    return $content;
}
1;
