# $Id: Locale.pm,v 1.2 2001/03/28 03:30:05 stas Exp $
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

package Extropia::Core::DataSource::Locale;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver _notImplemented);
use Extropia::Core::DataSource::DataType;

sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift @_;
    my @fields = @_;

    my $rs_class = _getDriver("Extropia::Core::DataSource::Locale", $type)
        || croak("Locale type '$type' is not supported");
            
    # hand-off to specific implementation sub-class
    $rs_class->new(@fields);
}

sub new {
    my $package = shift;
    return bless {}, ref $package || $package;
}

sub getDefaultSort {
    return undef;
}

1;
__END__

=head1 NAME

Extropia::Core::DataSource::Locale - abstract factory for creating
locale-specific DataType and Sort objects

=head1 DESCRIPTION

Knows which DataType and Sort modules to use for a given field type and
locale.  The purpose of this class is to avoid having to create subclasses
for every data type for every locale; if two locales share the same
implementation, the locale objects can simply return the same DataType and
Sort classes.

While String, Date and Number are the primary data types used in
the Extropia::Core::DataSource module, other user-defined types may be added.

=head1 SYNOPSIS

You will generally use Locale objects along with the Extropia::Core::DataSource
object (see L<DataSource> for more detail).  A Locale sets the default data
type and sorting conventions for all of the fields in a DataSource,
according to their respective field types:

  my $ds = Extropia::Core::DataSource->create( 
      @OTHER_DS_PARAMS,
      -FIELD_TYPES => { 
          Name   => 'String', 
          DOB    => 'Date', 
          Visits => 'Number'
                      },
      -LOCALE => 'US' 
  );

This particular DataSource will employ String::US as the DataType for Name
(providing case-insensitive sorting), Date for DOB, and Number::US for
Visits (allowing thousands separators in input and output).

=head1 PUBLIC METHODS

=over 4

=item create()

The create() method loads the specified Locale module and returns it to the
caller.

This class method takes one argument, which should be specified using a
named parameter, for the sake of future expandability:

  my $sort = Extropia::Core::DataSource::Locale->create(-TYPE => $type);

The list of available SortFactories include:

    Default (perl defaults)
    US (case insensitive sorting, commas separate thousands in numbers)

This list should be growing soon!

=item getDataType($type, @args)

Returns a DataType object of the correct subclass, according to the locale
specified, and the optional arguments passed.  These arguments are passed
directly through to the DataType object constructor, and should be
specified using named parameters.  getDataType() will throw an exception
if the DataType specified cannot be found.

=item getDefaultSort($type, @args)

Returns a Sort object to sort the specified type, according to the locale
specified, and the optional arguments (format strings) passed.  These
arguments are passed directly through to the sort object constructor, and
should be specified using named parameters.

Usually, it will be most appropriate to use the compare() method that it
part of the DataType class as the default sorting method.  In these cases,
getDefaultSort() should return undef.

=back

=head1 WRITING DRIVER MODULES

To implement your own locale, you must create a Locale driver.  This
driver is simply a Perl object with the methods described above.  These
methods must have the same semantics (i.e. take the same arguments and work
the same way) as the methods described above.

The easiest way to create a working Locale driver is to begin by
naming it Extropia::Core::DataSource::Locale::YourLocale, by declaring this
as the package name, and placing it into the appropriate place in your Perl
library directory.  'YourLocale', of course, should be replaced with a name
you select.

Next, inherit the basic functionality from Extropia::Core::DataSource::Locale, by
including this package in your @ISA array.

Finally, write the getDataType() and getDefaultSort() methods, to create
and return the proper types of DataType and Sort objects to deal with each
of these field types in your locale.

=head1 SEE ALSO

=item L<Extropia::Core::DataSource>
=item L<Extropia::Core::Sort>

=head1 AUTHOR

B<Extropia::Core::DataSource::Locale> is a module written by Extropia
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
