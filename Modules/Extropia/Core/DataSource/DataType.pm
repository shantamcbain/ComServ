# $Id: DataType.pm,v 1.2 2001/03/28 03:30:04 stas Exp $
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


package Extropia::Core::DataSource::DataType;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver);
use vars qw($VERSION);

$VERSION = do { my @r = q$Revision: 1.2 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift @_;
    my @fields = @_;

    if ($type eq 'Auto' || $type eq 'Autoincrement') {
        $type = 'Number';
    }
    my $rs_class = _getDriver("Extropia::Core::DataSource::DataType", $type)
        || croak("DataType type '$type' is not supported");
            
    # hand-off to specific implementation sub-class
    $rs_class->new(@fields);
}

# Often overridden
sub new {
    my $package = shift;
    return bless {}, ref $package || $package;
}

sub display2storage {
    my $self = shift;
    my $value = shift;
    return $self->internal2storage($self->display2internal($value));
}

sub storage2display {
    my $self = shift;
    my $value = shift;
    return $self->internal2display($self->storage2internal($value));
}

# The following base implementations of these methods assume that no
# conversion is necessary; this is often not the case

sub storage2internal { return $_[1]; }
sub internal2storage { return $_[1]; }
sub display2internal { return $_[1]; }
sub internal2display { return $_[1]; }

sub setDisplayFormat { return 0; }
sub getOdbcType      { return 0; }

sub isValid {
    my ($self, $value) = @_;
    return 1 unless defined $value;
    return defined($self->display2internal($value));
}


1;
__END__

=head1 NAME

Extropia::Core::DataSource::DataType - abstract data type class

=head1 DESCRIPTION

=head1 SYNOPSIS

=head1 PUBLIC METHODS

=over 4

=item create()

The create() factory method loads the right module and returns a DataType
object of the -TYPE specifed.

This class method takes one argument, which should be specified using a
named parameter.  Any additional arguments are passed on to the constructor
(new) method of the specified DataType:

  my $type = Extropia::Core::DataSource::DataType->create(-TYPE => $type);

Create will throw an exception if the named DataType module cannot be found
or loaded.  

Built-in DataTypes include:
  Autoincrement
  Date
  Number
  String

=item new

Creates a new DataType object.  Should usually not be called directly.

=item compare($first, $second);

Returns -1 if the first argument is less than the second, +1 if it is
greater, and 0 if they are the same.

=item getOdbcType

Returns an integer code representing the ODBC type of this Datatype.  These
values are used by the DBI module to determine whether and how the field
should be quoted.

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

=head1 WRITING DRIVER MODULES

To implement your own data type, you must create a DataType driver.  This
driver is simply a Perl object with the methods described above.  These
methods must have the same semantics (i.e. take the same arguments and work
the same way) as the methods described above.

The easiest way to create a working DataType driver is to begin by
naming it Extropia::Core::DataSource::DataType::YourType, by declaring this
as the package name, and placing it into the appropriate place in your Perl
library directory.  'YourType', of course, should be replaced with a name
you select.

Next, inherit the basic functionality from Extropia::Core::DataSource::DataType,
by including this package in your @ISA array.

Write the display2internal() and internal2display() methods, to convert the
expected display and data-entry value to and from an internal
representation of the data type.

Finally, if the storage format is different than the internal
representation, override the storage2internal() and internal2storage()
methods to do these conversions.

=head1 SEE ALSO

L<Extropia::Core::DataSource>

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
