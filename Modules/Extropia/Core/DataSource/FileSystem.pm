# $Id: FileSystem.pm,v 1.2 2001/03/28 03:30:04 stas Exp $
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

package Extropia::Core::DataSource::FileSystem;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _cloneRef);
use Extropia::Core::DataSource;
use File::Spec;
use vars qw(@ISA $VERSION);

$VERSION = do { my @r = q$Revision: 1.2 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);

sub new {
    my $package = shift;
    my $self = $package->SUPER::new(@_);
    @_ = _rearrange([-ROOTS, 
                     -INCLUDE,
                     -EXCLUDE,
                     -INFO,
                     -FIELD_DELIMITER, 
                     -LOCK_PARAMS],
                    [-ROOTS], @_);
    $self->{'roots'} = shift;

    # OPTIONAL FIELDS
    my $include = shift || [ q/[.]html?$/, q/[.]txt$/ ];
    my $exclude = shift || [];
    $self->{'info'}        = shift || {};
    $self->{'field_delim'} = shift;
    $self->{'lock_data'}   = shift;

    $include = [ $include ] unless ref $include;
    $exclude = [ $exclude ] unless ref $exclude;
    $self->{'include'} = $include;
    $self->{'exclude'} = $exclude;

    $self->{'dir_stack'} = [];
    $self->{'files'} = [];
    my $info = $self->{'info'};
    $info->{'title'} ||= q/<TITLE>(.+)<\/TITLE>/;
    unless ($self->getFieldNames()) {
#        print "DEBUG: ", join('|', keys %$info), "\n";
        $self->_setFieldNames( [ 'url', 'title', 
                grep {!/^(url|title)$/} keys %$info ] );
        $self->_setFieldTypes( {} );
    }
    
    # PSC: read only for now
    $self->setUpdateStrategy(Extropia::Core::DataSource::READ_ONLY);

    return $self;
}

##
## Data Manipulation
##

# PSC: read only for now
#sub doUpdate {
#}

sub disconnect {
    my $self = shift;

    my $dir_stack = $self->{'dir_stack'};
    my $dir;
    foreach $dir (@$dir_stack) {
        closedir($dir);
    }
    $self->{'current_search'} = undef;
}

##
## Querying Methods
##

sub _realSearch {
    my $self = shift;
    my $ra_search = shift;
    my $last_record_retrieved = shift;
    my $max_records_to_retrieve = shift;
    my $order = shift;
    my $rs_data = shift;

    # Prepare object for repeated callbacks to _searchForNextRecord

    my $dir_stack = $self->{'dir_stack'};
    push @$dir_stack, keys %{$self->{'roots'}};
    $self->{'current_search'} = $ra_search;

    my $record_set = Extropia::Core::DataSource::RecordSet->create( 
      @$rs_data,
      -DATASOURCE => $self,
      -KEY_FIELDS => $self->_getKeyFields(),
      -UPDATE_STRATEGY => $self->getUpdateStrategy(),
      -REAL_SEARCH_QUERY => $ra_search,
      -LAST_RECORD_RETRIEVED => $last_record_retrieved,
      -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve,
      -ORDER => $order
    );

    return $record_set;
}

sub _searchForNextRecord {
    my $self = shift;
    my $ra_search = shift;

    my $roots       = $self->{'roots'};
    my $files       = $self->{'files'};
    my $dir_stack   = $self->{'dir_stack'};
    my $current_dir = $self->{'current_dir'};
    my $info        = $self->{'info'};

    my $record_found = 0;
    my %record = ();

    FILE: while (1) {
        # Get next file
        unless (@$files) {
            $current_dir = shift @$dir_stack;
            $self->{'current_dir'} = $current_dir;
            last FILE unless $current_dir;
            local *DIR;
            my $rc = opendir(DIR, $current_dir);
            unless ($rc) {
                $self->addError("Can't open directory $current_dir: $!");
                next FILE;
            }
            @$files = grep { !/^[.]{1,2}$/ } readdir DIR;
            closedir DIR;
            next FILE;
        }
        my $basename = shift @$files;
        my $file = File::Spec->catfile($current_dir, $basename);
#        print "DEBUG: testing $file\n";
        
        # Test whether included and not excluded
        my $included = -d $file;
        my $inc;
        foreach $inc (@{$self->{'include'}}) {
            if ($file =~ /$inc/) {
                $included = 1;
                last;
            }
        }
        next FILE unless $included;
        my $exc;
        foreach $exc (@{$self->{'exclude'}}) {
            next FILE if $file =~ /$exc/;
        }

        # If directory, deal with contents later
        if (-d $file) {
            push @$dir_stack, $file;
            next FILE;
        }

#        print "DEBUG: READing $file\n";
        my $temp;
        my $root;
        foreach $root (sort { length($b)-length($a) } keys %$roots) {
            if ( ($temp = $file) =~ s/^$root// ) {
                $record{'url'} = $roots->{$root} . $temp;
            }
        }

        local *RECORD;
        my $rc = open(RECORD, $file);
        unless ($rc) {
            $self->addError("Can't open file $file: $!\n");
            next FILE;
        }
        my $fulltext = join('', <RECORD>);
        close(RECORD);
        
        $record{'title'} = $basename;
        my $field;
        foreach $field (keys %$info) {
            if ($field eq 'fulltext') {
                $record{$field} = $fulltext;
            }
            elsif ($fulltext =~ /$info->{$field}/) {
                $record{$field} = $1;
            }
        }

        if ($self->_matches($ra_search, \%record, $fulltext)) {
            $record_found = 1;
            last FILE;
        }
    }

    if ($record_found) {
#        print "DEBUG: Found Matching $record{'url'}\n";
        return $self->_recordInternal2Display(\%record);
    } else {
        return undef;
    }
}

# overrides and extends base method
sub _matches {
    my ($self, $search, $record, $fulltext) = @_;
#    use Data::Dumper;
#    print Dumper($search);
    $search = _cloneRef($search);
    if (ref $search eq 'ARRAY') {
        my $subsearch;
        foreach $subsearch (@$search) {
            next if ref $subsearch;
            my @condition = split(/\b(?:AND|OR)\b/i, $subsearch);
            my $i;
            for ($i = 0; $i < @condition; ++$i) {
#                print "DEBUG: condition $i: $condition[$i] ";
                if ($condition[$i] =~ /\*\s*==?(i)?\s*([\'\"])\*([^\*]+)\*\2/) {
                    my $caseins = $1 || '';
                    my $keyword = $3;
                    if (eval "\$fulltext =~ m/$keyword/s$caseins") {
                        $condition[$i] = ' 1 ';
#                        print ' 1 ';
                    } else {
                        $condition[$i] = ' 0 ';
#                        print ' 0 ';
                    }
                }
#                print "\n";
            }
            $subsearch = join('', @condition);
        }
    }
    return $self->SUPER::_matches($search, $record);
}

__END__

=head1 NAME

Extropia::Core::DataSource::FileSystem - A Perl5 object for searching a
file system dynamically

=head1 SYNOPSIS

  use Extropia::Core::DataSource;

  my $ds = Extropia::Core::DataSource->create(
             -TYPE => "FileSystem",
             -ROOTS => { 'Modules' => 'http://localhost' },
             -INCLUDE => '[.]pm$',
             -EXCLUDE => "^Modules/Time"
           );

=head1 DESCRIPTION

Search a file system, treating each file as a record.

This module is a driver that implements the Extropia::Core::DataSource
interface.  Thus, apart from the single line of code that creates this
particular type of driver, you use it in exactly the same way as you
would any other Extropia::Core::DataSource.

See S<USAGE> for a description of driver-specific creation parameters.  
See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 USAGE

=head2 Object Creation

Do not create an Extropia::Core::DataSource::FileSystem object directly.
Instead, call the Extropia::Core::DataSource->create() method with the
following parameters.  A DataSource object of the appropriate type will
be returned.

These parameters are required, for all FileSystem DataSources:

=over 4

=item -TYPE

Specifies the type of DataSource to create.  Set to "FileSystem" for a
FileSystem DataSource.

=item -ROOTS

The path to the file where the data is stored.  This value must be
supplied; there is no default.

=back

The remaining parameters are optional.  This next set is common to all
types of DataSource:

=over 4

=item -FIELD_NAMES

A reference to an array of field names, in the order in which they
appear in the DataSource file.

=item -FIELD_TYPES

A reference to a hash, in which field names are the keys and the
corresponding field types are the values.  Accepted values for field
types include:

    string/char/varchar/text        for character data
    date                            for dates
    datetime                        for combined date and time
    int/real/float/numeric/decimal  for numeric data; specific type
                                    not (currently) enforced
    auto                            for autoincrementing numeric data,
                                    often used to implement a unique
                                    key field.
    ctime/mtime/time                RESERVED FOR FUTURE USE

Any field not assigned a field type defaults to string.  Any unrecognized
fieldtype results in the field being treated as a form of numeric data.

Date and datetime field types may be optionally followed by a format
string, showing how this data should be stored in the database and
presented to the user, e.g. date(<storage format>, <presentation
format>).  If only a storage format is provided, this format will also
be used for presentation.  Date and time formats may be specified using
any of the following symbols:

    m, mm       month number
    mmm         month abbreviation
    mmmm        month name
    d, dd       day number
    ddd         day abbreviation
    dddd        day name
    y, yyyy     four-digit year
    yy          two-digit year (OK for display, but strongly 
                discouraged for storage values)

    H           hour
    M           minute
    S           second
    AM, PM      use 12-hour clock, with AM/PM

    e           seconds since the epoch (1/1/1970 on most systems), in 
                Universal Coordinated Time (UCT); this is the form 
                returned from the time() function in Perl and C.

=item -KEY_FIELDS

A reference to an array of field names that together form a unique key
for a given record.  No two records should have the same values in all
of their key fields.

=item -UPDATE_STRATEGY

For the time being, this is a read-only type of DataSource.

=item -RECORDSET_PARAMS

A definition hash, specified as a list reference, that provides the
parameters needed to create the default type of RecordSet to be used
with this DataSource.  By default, the DataSource will use a ForwardOnly
(unbuffered) RecordSet.

You may specify a different RecordSet type to use with a particular
search by specifying the -RECORDSET_PARAMS parameter as part of the
keywordSearch() or search() method call.  See the L<DataSource> for more
information.

=item -KEYWORD_SEARCH_OR_FLAG

This flag, if set to any true value, allows the keywordSearch() method
to return a record if any one of the keywords matches.  By default, this
flag is false, and all of the words specified in a keywordSearch() must
match.  This flag can also be manipulated after the DataSource has been
created using the getKeywordSearchOrFlag() and setKeywordSearchOrFlag()
methods.

=back

The following optional parameters are specific to the
DataSource::FileSystem driver:

=over 4

=item -INCLUDE

A reference to a list of regular expressions identifying filenames to
include in the search.  The default value is ['[.]html?$', '[.]txt$']
which searches all files with extension .html, .htm, or .txt.

=item -EXCLUDE

A reference to a list of regular expressions identifying path or
filenames to exclude from the search.  Default is none.  This option is
often used to protect whole subtrees of your site, for example a data
directory, upload directory, or private section of your website that you
don't want casual searchers to happen across.

=item -ADDITIONAL_INFO

A reference to a list of hashes.  Each hash maps a field name to a
regular expressions that serves to extract additional data from each
file that is parsed.  For example, if many of your web pages have a
<META> tag to identify keywords, you might want to extract this
information into a Keywords field:

    -ADDITIONAL_INFO => [ 
        'Keywords' => qr/<META NAME="Keywords" CONTENT="([^"]+)"/
                        ]

=item -FIELD_DELIMITER (future)

The character or characters used to separate one field from another.  
Use of this parameter has not yet been implemented.

=item -LOCK_PARAMS

A reference to an array of parameters to be used to construct the lock on
the DataSource file.  See L<Extropia::Core::Lock> for details.  

Default is to use File-based locking, on a file named the same as the
DataSource file with a '.lock' extension appended, using the default
Extropia::Core::Lock timeouts and number of attempts.

=back

=head1 DEPENDENCIES

This module is a driver that implements the Extropia::Core::DataSource
interface.  Thus, the Extropia::Core::DataSource module, and the
Extropia::Core::Base and Extropia::Core::Error modules upon which it in turn
depends, must be in the library path.

If date or time fields are used, Gordon Barr's TimeDate bundle is also
required.  Installing this bundle installs the following modules:

  Date::Parse
  Date::Format
  Date::Language
  Time::Zone
        
Furthermore, the Date::Parse module depends on Time::Local, which is
part of the standard Perl distribution.  Unfortunately, as of Perl
5.005_03, Time::Local had a serious bug that prevents it from handling
dates between 1939 and 1969.  A patched version of Time::Local is
available from Extropia, and is being merged into the Perl distribution,
beginning with Perl 5.6.  

=head1 VERSION

Extropia::Core::DataSource::FileSystem 0.01

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.  Only
limited testing has been done on this module so far.

=head1 BUGS

This DataSource proveds read-only access only.

There is a limit to the number of levels of directories that can be
searched.  This limit is system-dependent, since a file descriptor is
used for each open directory.

=head1 SEE ALSO

See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 COPYRIGHT

(c)1999, Extropia.com

This module is open source software, and may generally be used according
to the spirit of the Perl "Artistic License".  If you are interested,
however, the actual license for this module may be found at
http://www.extropia.com (or more directly, at
        http://www.extropia.com/download.html).

=head1 AUTHOR

Extropia::Core::DataSource::FileSystem is a Perl module written by Extropia
(http://www.extropia.com). Special technical and design acknowledgements
are given to Peter Chines, Gunther Birznieks and Selena Sol.

=head1 SUPPORT

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

Questions, comments and bug reports should be sent to
support@extropia.com.

=cut
