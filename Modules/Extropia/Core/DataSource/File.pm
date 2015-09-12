# $Id: File.pm,v 1.3 2001/08/10 07:28:51 stas Exp $
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


package Extropia::Core::DataSource::File;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::DataSource;
use Extropia::Core::Lock;
use Extropia::Core::KeyGenerator;
use vars qw($VERSION @ISA $MAX_FIELDS);

$VERSION = do { my @r = q$Revision: 1.3 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);
$MAX_FIELDS = 255;

sub new {
    my $package = shift;
    my $self = $package->SUPER::new(@_);
    my $params;
    ($params,@_) = _rearrangeAsHash(
        [ -FILE, 
          -FIELD_DELIMITER, 
          -RECORD_DELIMITER,
          -UPDATE_TEMP_FILE, 
          -KEYGENERATOR_PARAMS,
          -LOCK_PARAMS,
          -CREATE_FILE_IF_NONE_EXISTS,
          -COMMENT_PREFIX,
          -NULL_STRING,
          -TEST_FILE,
        ],
        [-FILE], @_);

    $self = _assignDefaults($self, $params);
    $self = _assignDefaults($self, 
        { -RECORD_DELIMITER    => "\n",
          -FIELD_DELIMITER     => '|',
          -UPDATE_TEMP_FILE    => $self->{-FILE} . ".new",
          -KEYGENERATOR_PARAMS => [ -TYPE => 'Counter',
                                    -COUNTER_FILE => $self->{-FILE} . ".count",
                                    -LOCK_PARAMS => [ -TYPE => 'None' ],
                                  ],
          -LOCK_PARAMS         => [ -TYPE => 'File',
                                    -FILE => $self->{-FILE} . ".lck",
                                  ],
          -CREATE_FILE_IF_NONE_EXISTS => 0,
          -COMMENT_PREFIX      => '',
          -NULL_STRING         => '',
          -TEST_FILE           => 1,
        });
    push @{$self->{-KEYGENERATOR_PARAMS}}, -INITIAL_KEY_SOURCE => $self;

    $self->_testFile();
    return $self;
}

##
## Data Manipulation
##

sub doUpdate {
    my $self = shift;
    @_ = _rearrange([-RETURN_ORIGINAL],[],@_);
    my $ret_orig = shift || 0;
    
    # Check that we can update (not READ_ONLY)
    return undef unless $self->_canUpdate("AddError");

    # If no work to do, can cut it short
    my $pending_updates = $self->_getPendingUpdates();
    return 0 if (!@$pending_updates && !$ret_orig);

    my $pending_adds = $self->_optimizeAdds() || return undef;
    # After successful optimize, only UPDATES and DELETES are left in 
    # $pending updates

    my $ds_file = $self->_getFileName();
    my $update_tempfile = $self->_getUpdateTempFile();
    my $field_delim = $self->_getFieldDelimiter();
    my $autoincrement_field = $self->getAutoincrementFieldName();
    my $lock_params = $self->_getLockParams();
    my $comment_prefix = $self->_getCommentPrefix();
    my $null_string = $self->_getNullString();
    my @original = ();

    # Obtain a single lock covering the data file, the temporary file, and
    # the counter file
    my $lock;
    if ($lock_params) {
        $lock = Extropia::Core::Lock->create( @$lock_params );
        $lock->obtainLock();
    }
    
    local *DATASOURCEFILE;
    local *NEWDATASOURCEFILE;

    $self->__openFile(*DATASOURCEFILE, $ds_file);
    open(NEWDATASOURCEFILE, ">$update_tempfile") ||
        die("Could not open $update_tempfile for writing: $!\n");

    # The eval block, and associated tests are to ensure that update is
    # atomic: either make all updates correctly or roll them all back.
    my $errors = 0;
    my $affected_rows = 0;

    eval { # BEGIN BIG EVAL BLOCK ------------------------

    local($/) = $self->_getRecordDelimiter();
    # Updates and Deletes
    if (@$pending_updates) {
        RECORD: while (<DATASOURCEFILE>) {
            chomp;
            # Eliminate blank lines
            next RECORD if /^\s*$/ && $_ !~ /\Q$field_delim/;
            # Keep comment lines
            if ($comment_prefix && /^$comment_prefix/) {
                print NEWDATASOURCEFILE $_, $self->_getRecordDelimiter();
                next RECORD;
            }
            my $rh_rec = $self->__line2record($_);

            my $update;
            foreach $update (@$pending_updates) {
                if ( $self->_matches($update->[1], $rh_rec) ) {
                    push @original, $self->_recordInternal2Display($rh_rec)
                        if $ret_orig;
                    next RECORD 
                        if ($update->[0] eq "DELETE");
                    confess "Unknown update type: '$update->[0]'\n"
                        if ($update->[0] ne "UPDATE");
                    # Update record:
                    my ($type, $value, $newval);
                    my $field;
                    foreach $field (keys %{$update->[2]}) {
                        $type = $self->getDataType($field);
                        if ($type) {
                            $value = $update->[2]->{$field};
                            $newval = $type->display2internal($value);
                            if (defined($value) && !defined($newval)) {
                                die "Invalid value '$value' for field "
                                    ."'$field', DataType " . ref $type . "\n";
                            }
                            $rh_rec->{$field} = $newval;
                        } else {
                            die "Unrecognized field '$field' in update\n";
                        }
                    }
                    ++$affected_rows;
                }
            }
            print NEWDATASOURCEFILE $self->__record2line($rh_rec),
                $self->_getRecordDelimiter();
        }

    } else { # no UPDATES or DELETES, so just copy file
        while (<DATASOURCEFILE>) {
            print NEWDATASOURCEFILE;
        }
    }

    # records are added last...
    if (@$pending_adds) {
        my $add;
        foreach $add (@$pending_adds) {
            confess "Unknown update type: '$add->[0]' (expected ADD)\n"
              if ($add->[0] ne "ADD");
            if ($autoincrement_field) {
                die("You must not supply a value for "
                    ."Autoincrement field '$autoincrement_field'; "
                    ."the value will be generated automatically.\n") 
                    if $add->[1]->{$autoincrement_field};
                $add->[1]->{$autoincrement_field} =
                    $self->_getNextAutoincrementValue();
            }
            print NEWDATASOURCEFILE $self->__record2line($add->[1]),
                $self->_getRecordDelimiter();
            ++$affected_rows;
        }
    }
    
    }; # END BIG EVAL BLOCK -----------------------

    close(DATASOURCEFILE);
    close(NEWDATASOURCEFILE);

    # Ideally, we would die with an error object, and just pass that error
    # object along here.  In the interest of being compatible with older
    # versions of Perl (5.003_07), we have to test strings to determine
    # which error codes to assign.
    if ($@) {
        my $code = 200;
        if ($@ =~ /^Could not open/) {
            $code = 103;
        }
        elsif ($@ =~ /^Unknown update type/) {
            die "$@\n";
        }
        elsif ($@ =~ /^Unrecognized field/) {
            $code = 204;
        }
        elsif ($@ =~ /^Invalid value/) {
            $code = 202;
        }
        # PSC: Add more error codes here...
        $self->addError(
            -CODE    => $code,
            -MESSAGE => $@, 
            -SOURCE  => 'DataSource::File::doUpdate()'
        );
        $errors = 1;
        push( @$pending_updates, @$pending_adds );
        unlink($update_tempfile);
    } else {
        unlink($ds_file);
        rename($update_tempfile, $ds_file);
    }

    if ($lock) {
        $lock->releaseLock();
    }

    if ($errors) {
        return undef;
    }
    return $self->_successfulUpdate($ret_orig, \@original, $affected_rows);
}

sub disconnect {
    my $self = shift;

    if ($self->{'filehandle'}) {
        close($self->{'filehandle'});
        $self->{"filehandle"} = undef;
    }
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

    my $filename = $self->_getFileName();

    $self->disconnect();
    local *FH;
    $self->__openFile(*FH, $filename);
    $self->{"filehandle"} = *FH;
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

    my $record_found = 0;
    my $field_delim = $self->_getFieldDelimiter();
    my $comment_prefix = $self->_getCommentPrefix();
    my $fh = $self->{"filehandle"};

    if (!$fh || !$self->_matchesActiveQuery($ra_search)) {
        $self->addError(
            -CODE    => 401,
            -MESSAGE => "Attempt to retrieve data from an inactive result set",
            -SOURCE  => 'DataSource::File',
            -CALLER  => (caller)[0]
        );
        return 0;
    }

    local($/) = $self->_getRecordDelimiter();
    my $rh_rec;
    my $line;
    while (defined($line = <$fh>)) {
        chomp($line);
        # Skip blank lines and comments
        next if $line =~ /^\s*$/ && $line !~ /\Q$field_delim/;
        next if $comment_prefix && $line =~ /^$comment_prefix/;

        $rh_rec = $self->__line2record($line);
        if (eval{ $self->_matches($ra_search, $rh_rec) }) {
            $record_found = 1;
            last;
        } elsif ($@) {
            $self->addError(
                -CODE => 300,
                -MESSAGE => $@, 
                -SOURCE => 'DataSource::File',
                -CALLER => (caller)[0]
            );
        }
    } 

    if ($record_found) {
        return $self->_recordInternal2Display($rh_rec);
    } else {
        $self->disconnect();
        $self->_setActiveQuery();
        return undef;
    }
}

##
## Protected Methods (use at your own risk; API subject to change)
##

sub _getRawFileHandle {
    my $self = shift;
    local *FH;
    open (FH, "+<" . $self->_getFileName);
    return *FH;
}

sub _getFileName {
    return $_[0]->{'-FILE'};
}

sub _getFieldDelimiter {
    return $_[0]->{'-FIELD_DELIMITER'};
}

sub _getRecordDelimiter {
    return $_[0]->{'-RECORD_DELIMITER'};
}

sub _getUpdateTempFile {
    return $_[0]->{'-UPDATE_TEMP_FILE'};
}

sub _getLockParams {
    return $_[0]->{'-LOCK_PARAMS'};
}

sub _setLockParams {
    my ($self, @lock_params) = @_;
    if (@lock_params) {
        $self->{'-LOCK_PARAMS'} = \@lock_params;
    }
    else {
        $self->{'-LOCK_PARAMS'} = 0;
    }
}

sub _canCreateFile {
    return $_[0]->{'-CREATE_FILE_IF_NONE_EXISTS'};
}

sub _getCommentPrefix {
    return $_[0]->{'-COMMENT_PREFIX'};
}

sub _getNullString {
    return $_[0]->{'-NULL_STRING'};
}

# These next two routines, and the -KEYGENERATOR_PARAMS parameter are all
# candidates for inclusion in the base DataSource, but can remain here if
# it is anticipated that most file-oriented DataSources inherit from
# DataSource::File.

sub _getNextAutoincrementValue {
    my $self = shift;

    if (!$self->{_key_generator}) {
        $self->{_key_generator} = Extropia::Core::KeyGenerator->create(
                @{$self->{-KEYGENERATOR_PARAMS}}
                );
    }

    my $kg = $self->{_key_generator};
    my $value = $kg->createKey();
    $self->_setLastAutoincrementID($value);
    return $value;
}

# This method is called by KeyGenerator::Counter through a callback
# mechanism when the counter file is lost.  We read the datafile to obtain
# the maximum existing value + 1

sub getInitialKey {
    my $self = shift;

    my $filename = $self->_getFileName();
    my $autofield = $self->getAutoincrementFieldName();
    my $fs = $self->_getFieldDelimiter();
    my $comment_prefix = $self->_getCommentPrefix();

    my $auto = $self->getFieldIndex($autofield);
    croak("Autoincrement field $autofield is not found in DataSource ")
      if !defined($auto);

    local($/) = $self->_getRecordDelimiter();
    local *DSFILE;
    open(DSFILE, $filename) ||
      die("Could not open $filename for reading max value: $! ");
    my $max = 0;
    while (<DSFILE>) {
        next if /^\s*$/ && $_ !~ /\Q$fs\E/;
        next if $comment_prefix && /^\Q$comment_prefix\E/;
        chomp;
        my $next = (split($fs, $_, $auto+1))[$auto];
        $max = $next if $next > $max;
    }
    close DSFILE;

    return ++$max;
}

sub __openFile {
    my ($self, $r_glob, $file) = @_;
    my $can_read = open(*$r_glob, "<$file");
    if (!$can_read && $self->_canCreateFile()) {
        if ($file =~ m'(.*)[/\\]') {
            my $dir = $1;
            if (!-d $dir) {
                die "Directory $dir does not exist\n";
            }
            elsif (!-w $dir) {
                die "Directory $dir is not writeable\n";
            }
        }
        unless (-e $file) {
            open(*$r_glob, ">$file") ||
                die("Could not create $file: $!\n");
            close(*$r_glob);
            $can_read = open(*$r_glob, "<$file");
        }
    }
    die("Could not open $file for reading: $!\n") unless $can_read;
    return 1;
}

sub _testFile {
    my $self = shift;
    my $force = shift || $self->{'-TEST_FILE'};
    my $error = 0;
    if ($force) {
        my $file = $self->_getFileName();
        if ($self->_canCreateFile()) {
            if (!-f $file) {
                # test whether directory is writable
                my $dir;
                if ($file =~ m'(.*)[\/\\]') {
                    $dir = $1;
                }
                if ($dir && !-w $dir) {
                    $self->addError(
                        -CODE => 102,
                        -MESSAGE => "Data file directory not writable."
                    );
                    $error = 1;
                }
            }
        }
        else {
            if (!-f $file) {
                $self->addError(
                    -CODE => 101,
                    -MESSAGE => "Data file '$file' not found."
                );
                $error = 1;
            }
            elsif (!-r $file) {
                $self->addError(
                    -CODE => 103,
                    -MESSAGE => "Data file '$file' not readable."
                );
                $error = 1;
            }
        }
    }
    if ($error) {
        return 0;
    }
    return 1;
}

#
# Private method: __line2record
#   Takes line of datafile and converts it to a hash-ref in Internal form
#
sub __line2record {
    my ($self, $line) = @_;
    my $field_delim = $self->_getFieldDelimiter;
    my $record_delim = $self->_getRecordDelimiter;
    my $null = $self->_getNullString;

    # Note: third argument to split() is essential, since otherwise empty
    # arguments at end are simply ignored, and number of elements in
    # @fields array is not accurate
    my @fields = split(/\Q$field_delim/, $line, $MAX_FIELDS);
    my @expected = $self->getFieldNames();
    if (@fields != @expected) {
        die "Incorrect number of fields in data line:\n$line\n"
            . "Expected " . scalar(@expected) . "; saw " . scalar(@fields)
            . ".  Possible data corruption, or perhaps you added a field "
            . "to the DataSource definition but forgot to add the field "
            . "to the data file itself.\n";
    }
    my $i;
    for ($i = 0; $i < @expected; ++$i) {
        if ($fields[$i]) {
            $fields[$i] =~ s/\\(.)/
                ($1 eq 'n') && $record_delim or
                ($1 eq 't') && $field_delim or
                ($1 eq '\\') && '\\' or
                "\\$1"/eg;
            # test for leftover escapes (shouldn't be any)
            die "Found unexpected escape code in field: $fields[$i].\n"
                ."This indicates the data has been corrupted, either "
                ."by manual editing or some unexpected failure\n"
                if $fields[$i] =~ /\\/;
            undef $fields[$i] if $null && $fields[$i] eq $null;
        }
        else {
            $fields[$i] = '' if $null;
        }
    }
    my $rec = $self->_recordStorage2Internal(\@fields);
    if (!$rec) {
        die "Invalid value in data file; possible file corruption or\n"
            . "improperly specified field type.\n"
            . $self->getLastError()->getMessage() . "\n";
    }
    return $rec;
}

#
# Private method: __record2line
#   Takes hash-ref in Internal form and converts to line suitable for
#   printing to file
#
sub __record2line {
    my ($self, $rec) = @_;
    my $field_delim = $self->_getFieldDelimiter;
    my $record_delim = $self->_getRecordDelimiter;
    my $null = $self->_getNullString;
    my $fields = $self->_recordInternal2Storage($rec);
    my $field;
    foreach $field (@$fields) {
        if (!defined($field)) {
            $field = $null || '';
        }
        $field =~ s/\\/\\\\/g;
        $field =~ s/\Q$field_delim\E/\\t/g;
    }
    my $line = join($field_delim, @$fields);
    $line =~ s/\Q$record_delim\E/\\n/g;
    return $line;
}

1;
__END__


=head1 NAME

Extropia::Core::DataSource::File - A Perl5 object for manipulating flat file databases

=head1 SYNOPSIS

  use Extropia::Core::DataSource;

  my $ds = Extropia::Core::DataSource->create(
             -TYPE => "File",
             -FILE => "Path/datafile.dat",
             -FIELD_DELIMITER => '|',
             -FIELD_NAMES =>
                 ["ID", "Name", "Description", "Price"]
             -FIELD_TYPES =>
                 { ID => 'Autoincrement', Price => 'Number' }
           );

=head1 DESCRIPTION

This module is a driver that implements the Extropia::Core::DataSource interface.
Thus, apart from the single line of code that creates this particular type
of driver, you use it in exactly the same way as you would any other 
Extropia::Core::DataSource.

See S<USAGE> for a description of driver-specific creation parameters.  
See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 USAGE

=head2 Object Creation

In general, you will not create an Extropia::Core::DataSource::File object
directly.  Instead, call the Extropia::Core::DataSource->create() method with the
following parameters.  A DataSource object of the appropriate type will be
returned.

These parameters are required, for all File DataSources:

=over 4

=item -TYPE

Specifies the type of DataSource to create.  Set to "File" for a File
DataSource.

=item -FILE

The path to the file where the data is stored.  This value must be
supplied; there is no default.

=item -FIELD_DELIMITER

The character or characters used to separate one field from another.
Obviously, the delimiter must not appear in the actual data.  This
value must be supplied; there is no default.

=item -FIELD_NAMES

A reference to an array of field names, in the order in which they appear
in the DataSource file.

=back

The remaining parameters are optional.  This next set is common to all
types of DataSource:

=over 4

=item -FIELD_TYPES

A reference to a hash, in which field names are the keys and the
corresponding field types are the values.  Accepted values for field types
include:

    String          for character data
    Date            for dates
    Number          for numeric data
    Auto            for autoincrementing numeric data, often used for
                    implementing a unique key field; only one such field
                    allowed per DataSource.

Additional user-defined datatypes may be created.  See
L<Extropia::Core::DataSource::DataType>.

Any field not assigned a field type defaults to String.

Date and datetime field types may be optionally followed by a format
string, showing how this data should be stored in the database and
presented to the user, e.g. date(<storage format>, <presentation format>).
If only a storage format is provided, this format will also be used for
presentation.  Date and time formats may be specified using any of the 
following symbols:

    m, mm       month number
    mmm         month abbreviation
    mmmm        month name
    d, dd       day number
    ddd         day abbreviation
    dddd        day name
    y, yyyy     four-digit year
    yy          two-digit year (strongly discouraged for storage values)

    H           hour
    M           minute
    S           second
    AM, PM      use 12-hour clock, with AM/PM

    e           seconds since the epoch (1/1/1970 on most systems), in 
                Universal Coordinated Time (UCT); this is the form returned
                from the time() function in Perl and C.

NOTE: while it is our intention to eventually allow any display format to
be used, currently only "standard" formats are accepted.  Any format that
cannot be recognized will result in an immediate error.

=item -KEY_FIELDS

A reference to an array of field names that together form a unique key for
a given record.  No two records should have the same values in all of their
key fields.

=item -UPDATE_STRATEGY

The update strategy tells the DataSource which fields should be used to
identify the records to be updated.  You must set this parameter to one of
the following constant values:

    $Extropia::Core::DataSource::KEY_FIELDS
    $Extropia::Core::DataSource::KEY_AND_MODIFIED_FIELDS
    $Extropia::Core::DataSource::ALL_FIELDS
    $Extropia::Core::DataSource::READ_ONLY

=item -RECORDSET_PARAMS

A definition hash, specified as a list reference, that provides the
parameters needed to create the default type of RecordSet to be used with
this DataSource.  By default, the DataSource will use a ForwardOnly
(unbuffered) RecordSet.

You may specify a different RecordSet type to use with a particular search
by specifying the -RECORDSET_PARAMS parameter as part of the keywordSearch()
or search() method call.  See the L<DataSource> for more information.

=item -KEYWORD_SEARCH_OR_FLAG

This flag, if set to any true value, allows the keywordSearch() method to
return a record if any one of the keywords matches.  By default, this flag
is false, and all of the words specified in a keywordSearch() must match.
This flag can also be manipulated after the DataSource has been created
using the getKeywordSearchOrFlag() and setKeywordSearchOrFlag() methods.

=back

The following optional parameters are specific to the DataSource::File
driver:

=over 4

=item -RECORD_DELIMITER

A string that separates one record from another in the data file.  If this
value appears in the data, it will be transparently translated to '\n' and
back as needed.

=item -CREATE_FILE_IF_NONE_EXISTS

If this option is true, the data file will be created if it is missing.
This option should only be set if your scripts will be running in an
unknown, and potentially uninitialized environment.  If this option is not
set, a missing data file will raise an error.

=item -COUNTER_FILE

The path to the file where the next autoincrement value is stored.  This
value is used only when one of the fields has been defined as an
autoincrementing field.  The default value is the name of the DataSource
file with '.counter' appended to it.

=item -UPDATE_TEMP_FILE

The path to the file used as a temporary location to store the contents of
the DataSource while it is being updated.  This file should not exist, and
will be overwritten without warning if it does.  For greatest efficiency,
the update temp file should be on the same file system as the main
DataSource file.  The default value is the name of the DataSource file
with '.new' appended to it.

=item -LOCK_PARAMS

A reference to an array of parameters to be used to construct the lock on
the DataSource file.  See L<Extropia::Core::Lock> for details.  

Default is to use Flock locking, on a file named the same as the
DataSource file with a '.lock' extension appended, using a timeout of 
120 seconds, with 20 attempts during this period.

=back

=head1 DEPENDENCIES

This module is the driver that implements the Extropia::Core::DataSource
interface.  Thus, all of the modules that the Extropia::Core::DataSource depends
on must be in the library path, including:
    Extropia::Core::Base
    Extropia::Core::Error
    Extropia::Core::DataSource
    Extropia::Core::DataSource::Locale
    Extropia::Core::DataSource::DataType
    Extropia::Core::DataSource::RecordSet
Along with any particular Locales, DataTypes, and RecordSets that your
applications use.

In addition, this module depends on file-locking facilities provided by the
Extropia::Core::Lock module, and the particular locking strategy used, e.g.
Extropia::Core::Lock::Flock.

If date or datetime fields are used, Gordon Barr's TimeDate bundle is also
required.  Installing this bundle installs the following modules:

  Date::Parse
  Date::Format
  Date::Language
  Time::Zone

Furthermore, the Date::Parse module depends on Time::Local, which is part
of the standard Perl distribution.  Unfortunately, as of Perl 5.005_03, 
Time::Local had a serious bug that prevents it from handling dates between
1939 and 1969.  A patched version of Time::Local is available from Extropia,
and is being merged into the standard Perl distribution, beginning with 
Perl 5.6.

=head1 VERSION

Extropia::Core::DataSource::File $Revision: 1.3 $

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

=head1 SEE ALSO

See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 COPYRIGHT

(c)1999, Extropia.com

This module is open source software, and may generally be used according to
the spirit of the Perl "Artistic License".  If you are interested, however,
the actual license for this module may be found at http://www.extropia.com
(or more directly, at http://www.extropia.com/download.html).

=head1 AUTHOR

Extropia::Core::DataSource::File is a Perl module written by Extropia
(http://www.extropia.com). Special technical and design acknowledgements
are given to Gunther Birznieks, Peter Chines and Selena Sol.

=head1 SUPPORT

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

Questions, comments and bug reports should be sent to support@extropia.com.

=cut
