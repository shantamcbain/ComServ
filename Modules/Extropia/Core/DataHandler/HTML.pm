#$Id: HTML.pm,v 1.8 2002/06/21 02:54:01 jason Exp $
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

####################################################
#
# Extropia::Core::DataHandler::HTML
#
####################################################
package Extropia::Core::DataHandler::HTML;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.8 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

# get the encoding sub right
if ($ENV{MOD_PERL}) {
    require Apache::Util;
    *encode_html = \&Apache::Util::escape_html;
} else {
	require HTML::Entities;
	# fixed to resemble apache_1.3.26/src/main/util.c:ap_escape_html() exactly - HMS
	*encode_html = sub { HTML::Entities::encode($_[0], '<>&') };
}

sub getHandlerRules {
    my $self = shift;

    return {
        -ESCAPE_HTML_TAGS    => [$self,\&escapeHTMLTags],
        -REMOVE_HTML         => [$self,\&removeHTML],
        -REMOVE_IMAGES       => [$self,\&removeImages],
        -REMOVE_JAVA         => [$self,\&removeJava],
        -REMOVE_ACTIVEX      => [$self,\&removeActiveX],
        -REMOVE_SSI          => [$self,\&removeSSI],
        -REMOVE_SSI_EXEC     => [$self,\&removeSSIExec]
    };

} # getHandlerRules

#
# escapeHTMLTags merely escapes the HTML begin
# and end brackets so that the HTML shows up with the 
# regular text.
#
sub escapeHTMLTags {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        return encode_html($field);
    } else {
        # assume that it's always an ARRAY
        return map {encode_html($_)} @$field;
    }

} # end of escapeHTMLTags

#
# removeHTML removes all < > tags in a document
# without regard to newlines.
#
# Of course, this simple routine is easily broken by 
# HTML that has "" and uses brackets within its own HTML.
#
# However, that will result in merely making an ugly document
# if someone screws up... remember this is just a quickie
# form validator to make sure harmful HTML might be
# removed as needed. If you want to do full scale HTML parsing
# use LWP.
#
sub removeHTML {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<[^>]*>//gs;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<[^>]*>//gs;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeHTML

#
# removeImages removes IMG tags from
# a field. Note that this is just a quickie regex
# which may be subject to the same issues as the
# removeHTML method in this object.
#
# However, it should suit most purposes without
# resorting to LWP. Users are encouraged to subclass
# this and make a HTML::LWP DataHandler. :)
#
sub removeImages {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<\s*IMG\s+[^>]*>//gis;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<\s*IMG\s+[^>]*>//gis;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeImages

#
# removeJava removes APPLET tags from
# a field. Note that this is just a quickie regex
# which may be subject to the same issues as the
# removeHTML method in this object.
#
# However, it should suit most purposes without
# resorting to LWP. Users are encouraged to subclass
# this and make a HTML::LWP DataHandler. :)
#
sub removeJava {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<\s*APPLET\s+[^>]*>//gis;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<\s*APPLET\s+[^>]*>//gis;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeJava

#
# removeActiveX removes OBJECT tags from
# a field. Note that this is just a quickie regex
# which may be subject to the same issues as the
# removeHTML method in this object.
#
# However, it should suit most purposes without
# resorting to LWP. Users are encouraged to subclass
# this and make a HTML::LWP DataHandler. :)
#
sub removeActiveX {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<\s*OBJECT\s+[^>]*>//gis;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<\s*OBJECT\s+[^>]*>//gis;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeActiveX

#
# removeSSI removes SSI related tags from
# a field. Note that this is just a quickie regex
# which may be subject to the same issues as the
# removeHTML method in this object.
#
# Even if a problem is encountered in the parsing, the
# SSI will at least be disabled and it is the posters fault
# for being a $%(# and trying to post in SSI as a hack.
#
# However, it should suit most purposes without
# resorting to LWP. Users are encouraged to subclass
# this and make a HTML::LWP DataHandler. :)
#
sub removeSSI {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<!--#[^>]*>//gis;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<!--#[^>]*>//gis;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeSSI

#
# removeSSIExec removes SSI Exec tags from
# a field. Note that this is just a quickie regex
# which may be subject to the same issues as the
# removeHTML method in this object.
#
# Even if a problem is encountered in the parsing, the SSI
# Exec will at least be disabled and it is the posters fault
# for being a $%(# and trying to post in SSI as a hack.
#
# However, it should suit most purposes without
# resorting to LWP. Users are encouraged to subclass
# this and make a HTML::LWP DataHandler. :)
#
sub removeSSIExec {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE],[-FIELD_VALUE],@_);

    my $field = shift;
    return undef if (!defined($field));

    if (!ref($field)) {
        $field =~ s/<!--#\s*EXEC[^>]*>//gis;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/<!--#\s*EXEC[^>]*>//gis;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeSSIExec

1;
