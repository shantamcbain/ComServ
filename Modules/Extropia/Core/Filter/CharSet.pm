#$Id: CharSet.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Filter::CharSet;

# By Gunther Birznieks
#
# Use this filter to add on a charset to the Content-type: text/html 
# string in case the view author forgot to do so. This is important
# to resolve one of the causes of the Cross Site Scripting problem 
# highlighted in the following document:
#
# http://www.cert.org/advisories/CA-2000-02.html
# http://www.cert.org/tech_tips/malicious_code_mitigation.html 
# 
# Default charset is given as ISO-8859-1

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
                -CHARSET,
                -CHECK_FOR_CONTENT_TYPE
            ],
            [
            ],
            @_);
    
    $self = _assignDefaults ($self,
        {
            '-CHARSET'                => 'ISO-8859-1',
            '-CHECK_FOR_CONTENT_TYPE' => 1
        });

    return bless $self, $package;
} # end of new

sub filter {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_FILTER],
                    [-CONTENT_TO_FILTER],
                    @_);

    my $content = shift;

    my $charset = $self->{-CHARSET} || '';

    return $content
        if $content =~ s!^(Content-type: text/html)$!$1; charset=$charset!im;

# breaks under mod_perl
#    if ($self->{-CHECK_FOR_CONTENT_TYPE} && $content !~ /^Content-type/im) {
#        warn ("CharSet Filter detected that you forgot to specify a " .
#              "Content-Type header string in your view contents.");
#    }

    return $content;

} # end of filter

1;
