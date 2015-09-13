#$Id: SSIInclude.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::SSIInclude;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash _rearrange);
use Extropia::Core::Filter;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Filter);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new SSIInclude filter
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([-VIRTUAL_ROOT],
                                  [],
                                  @_);

    if (!defined($self->{-VIRTUAL_ROOT})) {
        $self->{-VIRTUAL_ROOT} = "";
    }
    
    my $self = {};

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
    while($content =~ /<!--#include\s+([^>]+)-->/i) {
        my $ssi_code    = $1;
        my $ssi_content = $self->_filterSSIInclude(-SSI_INCLUDE => $ssi_code);
        $content =~ s/<!--#include\s+$ssi_code-->/$ssi_content/;
    } # end of SSI Include

    return $content;

} # end of filter

#
# _filterSSIInclude
#
sub _filterSSIInclude {
    my $self = shift;
    @_ = _rearrange([-SSI_INCLUDE],[-SSI_INCLUDE],@_);

    my $ssi_include = shift;

    my $ssi_file;
    if ($ssi_include =~ /file\s*=\s*["'](.+)['"]/i) {
        $ssi_file = $1;
    } elsif ($ssi_include =~ /virtual\s*=\s*["'](.+)['"]/i) {
        my $virtual_file = $1;
        my $virtual_root = $self->{-VIRTUAL_ROOT};
        if (!defined($virtual_root)) {
            croak("You did not pass the virtual web server root " .
                    "to this object, yet you are attempting to " .
                    "use the virtual SSI include tag.");
        } else {
            $virtual_root .= "/" if ($virtual_root !~ /\/$/);
            $ssi_include = $virtual_root . $virtual_file;
        }
    } else {
        croak("Could not figure out how to parse " .
                "$ssi_include SSI include command");
    }
    $self->_filterFile(-FILE => $ssi_file);

} # end of _filterSSICode

#
# _filterFile 
#
sub _filterFile {
    my $self = shift;
    @_ = _rearrange([-FILE],[-FILE],@_);

    my $file = shift;

    local(*FILE);
    my $content;

    open(FILE, "<$file") ||
        die ("Could not open $file for reading!:$!\n");
    {
        local($/) = undef;
        $content = <FILE>;
    }
    close(FILE);
    return $self->filter(-CONTENT_TO_FILTER => $content);

} # end of _filterFile

1;
