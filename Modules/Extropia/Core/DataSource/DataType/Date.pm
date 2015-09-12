# $Id: Date.pm,v 1.4 2002/02/04 09:25:36 gunther Exp $
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

#
# GB: added a new format type that is just like yyyy-mm-dd hh:mm:ss
# except that there is a T instead of a space. This accommodates 
# one of the SOAP spec data types.
#
package Extropia::Core::DataSource::DataType::Date;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataSource::DataType;
use Date::Language;
use vars qw(@ISA);

@ISA = ('Extropia::Core::DataSource::DataType');

sub new {
    my $package = shift;
    @_ = _rearrange([-DISPLAY,-STORAGE,-LANGUAGE,-STRICT],[],@_);
    my $display = shift || '';
    my $storage = shift || $display;
    my $lang    = shift || 'English';
    my $self = { 
        _sub_for_format  => {}
      , _strict_format   => shift || 0 
      , _date_object     => Date::Language->new($lang)
    };
    bless $self, ref $package || $package;
    $self->setDisplayFormat($display);
    $self->_setStorageFormat($storage);
    return $self;
}

sub setDisplayFormat {
    my ($self, $format) = @_;
    if (!$format) {
        $self->{'_strict_format'} = 0;
        $format = $self->_getDefaultDisplayFormat();
    }
    my $new_format = $self->_template2format($format);
    $self->{'_display_format'} = $new_format;
    if ($new_format !~ /%[Yy]/ &&
        $new_format !~ /%m/ &&
        $new_format !~ /%[Dd]/) {
# Can't really test format... because internal time will
# be different...
        return 1;
    }
    my $test_time = time;
    my $internal = $self->internal2display($test_time);
#print $internal . "\n";
#   print $self->display2internal($internal) . "\n";
    if (abs($self->display2internal($internal) 
            - $test_time) > 60 * 60 * 24) {
        die "Fatal error: date display format '" . $format
           ."' cannot be converted back to valid date\n";
    }
    return 1;
}

sub storage2internal {
    my ($self, $value) = @_;
    my $format = $self->{'_storage_format'};
    if ($format =~ /T/) {
        $format =~ s/T/ /;
        $value  =~ s/T/ / if ($value);
    }
    if ($format eq "mysqltimestamp") {
        $format = "%Y-%m-%d %H:%M:%S";
        if ($value =~ /(\d{4})(\d{2})(\d{2})(\d{2})?(\d{2})?(\d{2})?/) {
            $value = "$1-$2-$3 $4:$5:$6"; 
        } else {
            die("Error converting mysqltimestamp value: $value to internal format.");
        }
    }
    #print "STORAGE2INTERNAL: $value\n";
    return $self->_str2time($value, $format);
}

sub display2internal {
    my ($self, $value) = @_;

    #print "DISPLAY2INTERNAL: $value\n";
    #$value = undef if ($value eq "");
    my $new_value = $self->_str2time($value, $self->{'_display_format'});
    #return undef if ($new_value eq "");
    # 
    # Return a legitimate undef where the error is bypassed in the 
    # case where str2time failed to produce a value.
    #
    # This will force empty strings and undef's to insert a NULL
    # into the SQL database such as Oracle.
    #
    return (undef, 1) if (!defined($new_value));
    return $new_value;
}

sub internal2storage {
    my ($self, $value) = @_;
    my $format = $self->{'_storage_format'};
    if ($format =~ /T/) {
        $format =~ s/T/ /;
        $value  = $self->_time2str($value,$format); 
        $value  =~ s/ /T/;
        return $value;
    } else {
        if ($format eq "mysqltimestamp") {
            $format = "%Y-%m-%d %H:%M:%S";
            $value = $self->_time2str($value, $format);
            if (!$value) {
                return $value;
            }

            if ($value =~ /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/) {
                $value = "$1$2$3$4$5$6";
            } else {
                die("Error converting $value to mysqltimestamp format."); 
            }

        } else {
            $value = $self->_time2str($value, $format);
        }
    }
    #print "INTERNAL2STORAGE: $value\n";
    return $value;
}

sub internal2display {
    my ($self, $value) = @_;
    #print "INTERNAL2DISPLAY: $value\n";
    return $self->_time2str($value, $self->{'_display_format'});
}

sub compare {
    if (!defined $_[1]) {
        return -(defined $_[2]);
    } elsif (!defined $_[2]) {
        return 1;
    } else {
        return $_[1] <=> $_[2];
    }
}

sub getOdbcType {
    if ($DBI::VERSION) { 
        return DBI::SQL_DATE();
    }
    return 9;
}

#
# Protected methods
#

sub _setStorageFormat {
    my $self = shift;
    my $format = shift || 'y-m-d H:M:S';
    $self->{'_storage_format'} = $self->_template2format($format);
    my $test_time = time;
    if (abs($self->storage2internal($self->internal2storage($test_time)) 
            - $test_time) > 60 * 60 * 24) {
        die "Fatal error: "
           ."date storage format cannot be converted back to valid date\n";
    }
}

sub _getDateObject {
    my $self = shift;
    return $self->{'_date_object'} ||= Date::Language->new('English');
}

sub _getDefaultDisplayFormat {
    return 'm/d/y';
}

sub _time2str {
    my ($self, $time, $format) = @_;
    return undef unless defined($time);
    my $formatter = $self->_getDateObject();
    return $formatter->time2str($format, $time);
}

sub _str2time {
    my ($self, $datestr, $format) = @_;
#    print "Entering _str2time with format: $format\n";
    if ($format !~ /%[Yy]/ &&
        $format !~ /%[m]/ &&
        $format !~ /%[dD]/) {
        $format = "%Y-%m-%d $format";
# Note that 1970-01-01 subtracts an hour!!! 
        $datestr = "1970-01-03 $datestr";
#    print "Format: $format\n";
#print "DateString: $datestr\n";
    }
    my $date;
    ($datestr, $format) = $self->_fixDMYFormat($datestr, $format);
    my $parser = $self->_getDateObject();
    if ($self->{'_strict_format'}) {
        eval { $date = $parser->formatted_str2time($datestr, $format) };
    } else {
        return $date unless $datestr;
        eval { $date = $parser->str2time($datestr, $format) };
    }
    if ($@ || !defined($date) || $date == -1) {
        if ($datestr =~ /^\d+$/) {
            # Assume all digits is a time value
            $date = $datestr;
        } else {
            # Can't parse: report an error?
            undef $date;
        }
    }
    return $date;
}

# Fixes DMY Format by changing the value temporarily
# to a MDY format...
#
sub _fixDMYFormat {
    my $self = shift;

    my $datestr = shift;
    my $format  = shift;

    if (defined($format) &&
        $format =~ /^(%[dD])(.?)(%m)(.*)/) {
        my $new_format .= "$3$2$1$4";
        if ($datestr =~ /^(\d+)([^\d]?)(\d+)(.*)/) {
            my $new_datestr = "$3$2$1$4";
            return ($new_datestr, $new_format);
        } else {
            return ($datestr, $format);
        }
    } else {
        return ($datestr, $format);
    }

} # end of __fixDMYFormat

#### Protected method: _template2format
# Build a date format string for time2str() out of template
####
sub _template2format {
    my $self = shift;
    my $template = shift;
    return $template if ($template eq "mysqltimestamp");

    my $format = $template;
    # If user specified template using native %-style codes, leave as is
    return $format if $format =~ /%[^%]/;  

    my ($hourfmt);
    if ($format =~ s/AM|PM|AM\/PM/%p/i) {
        $hourfmt = '%I';
    } else {
        $hourfmt = '%H';
    }
    $format =~ s/H+/$hourfmt/;
    $format =~ s/M+/%M/;
    $format =~ s/S+/%S/;

    $format =~ s/mmmm+/%B/;
    $format =~ s/mmm/%b/;
    $format =~ s/mm?/%m/;
    $format =~ s/dddd+/%A/;
    $format =~ s/ddd/%a/;
    $format =~ s/dd?/%d/;
    $format =~ s/y+/%Y/;
    # yy -> 2-digit year, else 4-digit
    $format =~ s/Y/y/ if $template =~ m/(?:^yy(?!y)|[^y]yy(?!y))/;

    return $format;
}

1;
__END__

##########################
# To be incorporated into Date::Language

sub _isMonthFirst {
    my $self = shift;
    return $self->{'_is_month_first'};
}

sub __createParser {
    my $self = shift;
    my $format = shift;
    my $sub = $self->{'_sub_for_format'}->{$format};
    unless ($sub) {
        my ($exp, $assign) = $self->__getExprAssign();
        my $regex = '';
        my $assignments = '';
        while ($format =~ m/\G(%[a-zA-Z]|[^%]+)/g) {
            if ($exp->{$1}) {
                $regex .= '('.$exp->{$1}.')';
                $assignments .= $assign->{$1} . ";\n";
            } else {
                $regex .= $1;
            }
        }
        $sub = eval qq! sub {
            my \$datestr = shift;
            my \$time;
            my \$sec = 0;
            my \$min = 0;
            my \$hr  = 0;
            my \$day   = 1;
            my \$month = 0;
            my \$year  = 0;
            my \$found_match = 0;
            if (\$datestr =~ /$regex/) {
                $assignments
                \$time =
                    Time::Local::gmtime(\$sec,\$min,\$hr,\$day,\$month,\$year);
            }
            return \$time;
        }!;
        $self->{'_sub_for_format'}->{$format} = $sub;
    }
    return $sub;
}

sub __getExprAssign {
    my $self = shift;
    my $expr   = $self->{'_pattern_expr'} || 0;
    my $assign = $self->{'_pattern_assign'} || 0;
    unless ($expr) {
        $expr = {
            '%%' => '%'
          , '%a' => join('|', @DoW)
          , '%A' => join('|', @DoW)
          , '%b' => join('|', @Month)
          , '%B' => join('|', @Month)
          , '%c' => join('|', @Month) . ') (\d+) (\d\d):(\d\d):(\d\d) (\d{4}'
          , '%d' => '\d\d?'
          , '%D' => '\d\d?)[/.-](\d\d?)[/.-](\d\d+'
          , '%H' => '\d\d?'
          , '%I' => '\d\d?'
          , '%j' => '\d{1,3}'
          , '%k' => '\d\d?'
          , '%l' => '\d\d?'
          , '%m' => '\d\d?'
          , '%M' => '\d\d?'
          , '%o' => '\d\d?)(?:'.join('|', @Suffixes)
          , '%p' => join('|', @AmPm)
          , '%r' => '\d\d):(\d\d):(\d\d) ('.join('|', @AmPm)
          , '%R' => '\d\d):(\d\d'
          , '%s' => '-?\d+'
          . '%S' => '\d\d?'
          , '%T' => '\d\d):(\d\d):(\d\d'
          , '%U' => '\d\d?'
          , '%w' => '\d'
          , '%W' => '\d\d?'
          , '%x' => '\d\d?)[/.-](\d\d?)[/.-](\d\d+'
          , '%y' => '\d\d'
          , '%Y' => '\d{4}'
          , '%z' => '[+-]\d{4}'
          , '%Z' => ''
        }
        $self->{'_pattern_expr'} = $expr;
        $self->{'_pattern_assign'} = $assign;
    }
    return ($expr, $assign);
}


=head1 NAME

Extropia::Core::DataSource::DataType:Date - Date handling for DataSource

=head1 DESCRIPTION

This module implements the DataType interface for Extropia DataSources, to
provide a means of converting among various representations of dates.  The
"internal" representation is epoch seconds, like Perl's built-in time()
function, while the "display" and "storage" formats are user-specified.

=head1 SYNOPSIS

This module is intended to be used as part of the Extropia::Core::DataSource
module.  It is automatically loaded and used when fields of type 'date' are
specified.

=head1 PUBLIC METHODS

=over 4

=item new

Constructor; takes the following optional parameters:

  -DISPLAY   Format for display and query (all interaction with user)
  -STORAGE   Format for storage in data source (defaults to same as
             display format)
  -LANGUAGE  Language to use in interpreting and formatting
             date values

=item setDisplayFormat

Changes display format

=item display2storage

Converts a display-formatted value to a storage-formatted value.

=item storage2display

Converts a storage-formatted value to a display-formatted value.

=item display2internal

Converts a display-formatted value to an internal representation.

=item internal2display

Converts an internal representation to a display-formatted value.

=item storage2internal

Converts a storage-formatted value to an internal representation.

=item internal2storage

Converts an internal representation to a storage-formatted value.

=back

=head1 SEE ALSO

=item L<Extropia::Core::DataSource>

=item L<Extropia::Core::DataSource::DataType>

=head1 AUTHOR

B<Extropia::Core::DataSource::DataType> is a module written by Extropia
(http://www.extropia.com).  Special technical and design acknowledgements
are given to Peter Chines, Gunther Birznieks and Selena Sol.

=head1 COPYRIGHT

(c)1999, Extropia.com.  

This module is open source and may generally be used according to the
spirit of the "Artistic Open Source License".  However, the actual license
for this module may be found at http://www.extropia.com (or more directly,
at http://www.extropia.com/download.html)

=head1 SUPPORT

Questions, comments and bug reports should be sent to support@extropia.com

=cut
