# $Id: WMLUtils.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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
# Defines routines to help Extropia objects send SOAP Requests
# and get data back.
# 
package Extropia::Core::WMLUtils;

use Carp;
use strict;
#
# we will use _rearrangeAsHash and _assignDefaults from Base,
# but we cannot import them because Base relies on Error. Therefore
# we cannot import statements from Base until Error has been
# fully compiled. But Error will not fully compile until the
# statements have been imported.
#
# Thererfore, the routines in Base will be prefixed with 
# Extropia::Core::Base:: to reference them in that package directly from
# this module.
#
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults); 

use vars qw($VERSION @ISA @EXPORT_OK);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::Base);
@EXPORT_OK = qw(
            hasSelectBug
            isMotorolaAccompli
            escapeWMLChars
            );

sub new {
    my $package = shift;
    my ($self) = Extropia::Core::Base::_rearrangeAsHash(
                    [],
                    [],
                    @_);

    return bless $self, $package;

}

sub hasSelectBug {
    my $cgi = shift;

    return isMotorolaAccompli($cgi);
}

sub isMotorolaAccompli {
    my $cgi = shift;

    my $user_agent = $cgi->user_agent() || "";
    if ($user_agent =~ /^MOT-CF/i) {
        return 1;
    }
    return 0;

} # end of isMotorolaAccompli

sub escapeWMLChars {
    my $value = shift;
    if (!defined($value)) {
        return undef;
    }
    $value =~ s/\$/\$\$/g;
# The following 2 lines clean out bad WML chars that don't display
# well on all phones...
    $value =~ s/([\x80-\xFF])//ge;
    $value =~ s/([^ \w\d+=\-_!@#\$\%^&*()~`\/.,?><';:"\[\]{}\\\|])//ge;
    $value = escapeXMLChars($value);
    return($value);
}
# The following routines were paraphrased from another XML Library

sub escapeXMLChars {
    $_[0] =~ s/&/&amp;/g;
    $_[0] =~ s/</&lt;/g;
    $_[0] =~ s/>/&gt;/g;
    $_[0] =~ s/'/&apos;/g;
    $_[0] =~ s/"/&quot;/g;
    $_[0] =~ s/([\x80-\xFF])/&xmlUtf8Encode(ord($1))/ge;
    return($_[0]);
}

sub xmlUtf8Encode {
# borrowed from XML::DOM
    my $n = shift;
    if ($n < 0x80) {
    return chr ($n);
    } elsif ($n < 0x800) {
        return pack ("CC", (($n >> 6) | 0xc0), (($n & 0x3f) | 0x80));
    } elsif ($n < 0x10000) {
        return pack ("CCC", (($n >> 12) | 0xe0), ((($n >> 6) & 0x3f) | 0x80),
                     (($n & 0x3f) | 0x80));
    } elsif ($n < 0x110000) {
        return pack ("CCCC", (($n >> 18) | 0xf0), ((($n >> 12) & 0x3f) | 0x80),
                     ((($n >> 6) & 0x3f) | 0x80), (($n & 0x3f) | 0x80));
    }
    return $n;
}

1;

__END__

