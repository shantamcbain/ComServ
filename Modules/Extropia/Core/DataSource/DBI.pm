# $Id: DBI.pm,v 1.5 2001/12/06 15:45:02 gunther Exp $
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

package Extropia::Core::DataSource::DBI;

use strict;
use vars qw($VERSION @ISA);

use Carp;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataSource;
use DBI;
use DBIx::SQL92;

$VERSION = do { my @r = q$Revision: 1.5 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);

sub new {
    my $package = shift;
    my $self = $package->SUPER::new(@_);
    @_ = _rearrange(
        [-DBI_DSN, 
         -TABLE,
         -USERNAME, 
         -PASSWORD,
          -DBIX_PARAMS], 
        [-DBI_DSN, -TABLE], @_);
    my $dbi_ds = shift;
    my $table = shift;

    # Optional Fields
    my $user = shift || "";
    my $pass = shift || "";
    my $dbix_params = shift;

    # This peculiar assignment allows PrintError to be overriden, but
    # ensures that RaiseError and AutoCommit cannot:
    my %attr = (PrintError => 0, @_, RaiseError => 0, AutoCommit => 1);

    # Create handle to database (attempt to load driver)
    $dbi_ds = 'dbi:'.$dbi_ds unless $dbi_ds =~ /^dbi:/;
    my $dbh = $self->__connect($dbi_ds, $user, $pass, \%attr);
    $self->{'dbh'} = $dbh;
    my $stdsql = new DBIx::SQL92($dbh);
    $self->{'__dbi_sql_standard'} = $stdsql;

    # Define additional DBIX Params to give hints
    # to the DBIX driver as to how the database is 
    # setup.
    #
    # eg if you use autoinc sequence in Oracle
    # you need to tell DataSource the sequence name.
    #
    if (defined($dbix_params)) {
        my %params = @{$dbix_params};
        foreach my $param (keys %params) {
            $stdsql->{$param} = $params{$param};
        }
    }


    # Turning off AutoCommit with a database that doesn't support
    # transactions is a fatal error.  So we don't.
    if ($stdsql->can_rollback) {
        $dbh->{'AutoCommit'} = 0;
    }

    $self->{'__dbi_datasource'} = $dbi_ds;
    $self->{'__dbi_username'} = $user;
    $self->{'__dbi_password'} = $pass;
    $self->{'__dbi_attributes'} = \%attr;
    $self->{'__dbi_table'} = $table;
    $self->{'__dbi_active_statement'} = 0;

    return $self;
}

sub doUpdate {
    my $self = shift;
    @_ = _rearrange([-RETURN_ORIGINAL],[],@_);
    my $return_orig = shift || 0;

    return undef unless $self->_canUpdate("AddError");

    my $pending_updates = $self->_getPendingUpdates();
    my $table = $self->_getTable();
    my $data_types = $self->_getAllDataTypes();
    my @fields = $self->getFieldNames();
    my $dbh = $self->_getStandardSql();

    # Close any active cursor before performing update
    $self->__closeCursor();

    my $sql = "";
    my @original = ();
    my $errors = 0;
    my $completed = 0;
    my $affected = 0;

    # BEGIN LARGE EVAL BLOCK -----------------------------------------
eval {
    # According to the DBI standard, this line should not be necessary,
    # since transactions are automatically started when AutoCommit is not set.
    # However, this could be used to lock the table, in order to allow
    # manual rollback on databases that don't support this feature.
    # (note that begin_transaction is an experimental DBIx::SQL92 method)
    # $dbh->begin_transaction;

    my $update;
    foreach $update (@$pending_updates) {
        my $type = $update->[0];
        if ($type eq "ADD") {
            my $autoincfield = $self->getAutoincrementFieldName();
            if (defined($autoincfield)) {
                delete $update->[1]->{$autoincfield};
            }
            $sql = "insert into $table ("
                . join(",", keys %{$update->[1]})
                . ") values ("
                . join(",", 
                  map { $dbh->quote(
                        $data_types->{$_}->internal2storage(
                            $update->[1]->{$_} ),
                        $data_types->{$_}->getOdbcType()
                        ) } 
                  keys %{$update->[1]})
                . ")";
            $affected += $dbh->do($sql) 
                || die "Could not add record; DBI error: " . $dbh->errstr;
            $self->_setLastAutoincrementID($dbh->get_last_auto_id());
        }
        elsif ($type eq "UPDATE" || $type eq "DELETE") {
            my $where = $self->_tree2sql($update->[1]);
            my $data;
            if ($return_orig) {
                $sql = "select " . join(",", @fields)
                    . " from $table where $where";
                #print "DEBUG: $sql\n";
                $data = $dbh->selectall_arrayref($sql);
                if ($data) {
                    my ($rec, $disp);
                    foreach $rec (@$data) {
                        $disp = $self->_recordStorage2Display($rec)
                            || die "Could not read all values in original "
                                ."record.  See previous error message.\n";
                        push @original, $disp;
                    }
                } else {
                    die "Could not select original records for " 
                        . lc($type) . "; DBI error: " .  $dbh->errstr;
                }
            }
            if ($type eq "UPDATE") {
                $sql = "update $table set "
                    . join(",", 
                      map { "$_ = " . $dbh->quote(
                          $data_types->{$_}->display2storage(
                              $update->[2]->{$_} ),
                          $data_types->{$_}->getOdbcType()
                          ) }
                      keys %{$update->[2]}) 
                    . " where $where\n";
            } else {
                # mysql requires the 'from'
                $sql = "delete from $table where $where";
            }
            my $rows = $dbh->do($sql) 
                || die "Could not ".lc($type)." records, with SQL:\n$sql\n" 
                    ."Error reported from DBI: " . $dbh->errstr;
                    # Note that mySQL cannot handle the consistency check because
                    # the update method works weirdly...
            if ($self->{__dbi_datasource} !~ /dbi:mysql/i && $rows >= 0 && $return_orig && $rows != @$data) {
                die "Consistency error: DBI database changed between "
                    ."selection of old values and " . lc($type) . ".";
            }
            $affected += $rows;
        }
        else {
            confess("Update type '$type' is unknown");
        }
    } continue {
        ++$completed;
    }

    $dbh->commit || die "Error committing changes: " . $dbh->errstr;
};
    # END LARGE EVAL BLOCK ------------------------------------------
    if ($@) {
        if ($dbh->can_rollback) {
            $self->addError(
                -CODE    => 203,
                -MESSAGE => "doUpdate failed: Changes rolled back\n" . $@,
                -SOURCE  => 'DataSource::DBI'
            );
            $dbh->rollback;
        }
        else {
            $self->addError(
                -CODE    => 251,
                -MESSAGE => "doUpdate failed: Changes CANNOT BE rolled back\n"
                    . "$completed completed actions removed from update queue\n"
                    . $@,
                -SOURCE  => 'DataSource::DBI'
            );
            splice(@$pending_updates, 0, $completed);
        }
        return undef;
    }

    return $self->_successfulUpdate($return_orig, \@original, $affected);
}

sub _realSearch {
    my $self = shift;
    my $ra_search = shift;
    my $last_record_retrieved = shift;
    my $max_records_to_retrieve = shift;
    my $order = shift;
    my $rs_data = shift;

    my $dbh = $self->_getRawDBIHandle();
    my $table = $self->_getTable();
    my @fields = $self->getFieldNames();
    
    $self->__closeCursor();
    my $sql = "select " . join(",", @fields);
    $sql .= " from $table "; 
    eval { $sql .= "where " . $self->_tree2sql($ra_search) if $ra_search };
    if ($@) {
        $self->addError(
            -CODE    => 300,
            -MESSAGE => $@,
            -SOURCE  => 'DataSource::DBI',
            -CALLER  => (caller)[0]
        );
        return 0;
    }
    $sql .= " order by " . $order if $order;

    #use Data::Dumper;
    #print "DEBUG:", Dumper($ra_search);
    #print "DEBUG SQL:\n$sql\n";

    my $success = 0;
    my $sth = $dbh->prepare($sql);
    $success = $sth->execute() if $sth;

    my $record_set = 0;
    if ($success) {
        $self->_setActiveQuery($ra_search, $sth);

        $record_set = Extropia::Core::DataSource::RecordSet->create( 
          @$rs_data,
          -DATASOURCE => $self,
          -KEY_FIELDS => $self->_getKeyFields(),
          -UPDATE_STRATEGY => $self->getUpdateStrategy(),
          -REAL_SEARCH_QUERY => $ra_search,
          -LAST_RECORD_RETRIEVED => $last_record_retrieved,
          -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve
        );
    } else {
        $self->_setActiveQuery();
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "Query failed: " . $dbh->errstr,
            -SOURCE  => 'DataSource::DBI',
            -CALLER  => (caller)[0]
        );
    }

    return $record_set;
}

sub _searchForNextRecord {
    my $self = shift;
    my $ra_row = $self->_skipToNextRecord(@_);
    if ($ra_row) {
        $ra_row = $self->_recordStorage2Display($ra_row);
    }
    return $ra_row;
}

sub _skipToNextRecord {
    my $self = shift;
    my $ra_search = shift;

    if (!$self->_matchesActiveQuery($ra_search)) {
        $self->addError(
            -CODE    => 401,
            -MESSAGE => "Attempt to retrieve data from an inactive result set",
            -SOURCE  => 'DataSource::DBI',
            -CALLER  => (caller)[0]
        );
        return 0;
    }

    my $ra_row = undef;
    my $sth = $self->_getActiveStatement();
    if ($sth) {
        my @row = $sth->fetchrow_array();
        $ra_row = \@row if @row;
    } else {
        $self->addError(
            -CODE    => 401,
            -MESSAGE => "No DBI statement handle is active",
            -SOURCE  => 'DataSource::DBI',
            -CALLER  => (caller)[0]
        );
    }
    if (!$ra_row) {
        $self->_setActiveQuery();
    }
    return $ra_row;
}

sub disconnect {
    my $self = shift;

    $self->__closeCursor();
    my $dbh = $self->{'dbh'};
    $dbh->disconnect() if $dbh;
}

##
## Protected Methods
##

# Overrides and extends method in DataSource.pm
sub _setActiveQuery {
    my ($self, $active_query, $active_statement) = @_;
    $self->SUPER::_setActiveQuery($active_query);
    $self->{'__dbi_active_statement'} = $active_statement;
}

sub _getActiveStatement {
    my $self = shift;
    return $self->{'__dbi_active_statement'};
}

#### Protected method: _tree2sql
# Converts an Extropia::Core::DataSource expression tree into SQL expression,
#   flattening trees by inserting parentheses where required.
# Returns SQL (perhaps empty); DIEs in case of errors.
####
sub _tree2sql {
    my $self = shift;
    my $ra_search = shift;

    my $sql = '';
    if (!ref $ra_search) {
        eval { $sql .= $self->__wholeExpression($ra_search) };
        if ($@) {
            # catch and re-throw exception (with offending search string)
            chomp $@;
            die($@ . ": '" . $ra_search . "'\n");
        }
    }
    elsif (ref $ra_search eq "ARRAY") {
        $sql .= "( " ;
        my $expr;
        foreach $expr (@$ra_search) {
            $sql .= $self->_tree2sql($expr);
        }
        $sql .= ") " ;
    } 
    else {
        confess("Search is not array ref or string");
    }
    return $sql;
}

sub _getRawDBIHandle {
    my $self = shift;
    my $duplicate = shift || 0;

    my $dbh = $self->{'dbh'};
    croak("Invalid DBI Handle.  Connection to DataSource did not succeed.\n"
        . "Please test for errors immediately after DataSource is created,\n"
        . "using \$ds->getErrorCount().") unless $dbh;
    if ($duplicate) {
        $dbh = $self->__connect($self->_getDBIDatasource(), 
                $self->_getDBIUsername(),
                $self->_getDBIPassword(), 
                $self->_getDBIAttributes());
    }
    return $dbh;
}

sub _getTable {
    return $_[0]->{'__dbi_table'};
}

sub _getDBIDatasource {
    return $_[0]->{'__dbi_datasource'};
}

sub _getDBIUsername {
    return $_[0]->{'__dbi_username'};
}

sub _getDBIPassword {
    return $_[0]->{'__dbi_password'};
}

sub _getDBIAttributes {
    return $_[0]->{'__dbi_attributes'};
}

sub _getDefaultDateStorageFormat {
    return '%Y-%m-%d %H:%M:%S';
}

sub _getStandardSql {
    my $self = shift;
    if ($self->_getRawDBIHandle) {
        return $self->{'__dbi_sql_standard'};
    }
    return 0;
}

##
## Private Methods
##

sub __connect {
    my $self = shift;
    my @ds_param = @_;

    my $dbh;
    eval { $dbh = DBI->connect(@ds_param) };
    if ($@ || !$dbh) {
        undef $dbh;
        $self->addError(
           -CODE    => 112,
           -MESSAGE => "Could not connect to DBI datasource '$ds_param[0]': $DBI::errstr",
           -SOURCE  => 'DataSource::DBI',
           -CALLER  => (caller)[0]
        );
    }
    return $dbh;
}

#### Private method: __closeCursor
# Finishes active statement, if any.  Used before beginning next query
# or update, because most DBD implementations support only one active
# handle at a time.
####
sub __closeCursor {
    my $self = shift;

    my $sth = $self->_getActiveStatement();
    if ($sth) {
        $sth->finish();
        $self->_setActiveQuery();
    }
}

# Converts expression to SQL
sub __wholeExpression {
    my $self = shift;
    my $whole_expr = shift;

    #print "Entering __wholeExpression with :$whole_expr:\n";

    my $eval_expr = "";
    my @pieces = $self->_splitOnQuotes($whole_expr);
    my $j;
    for ($j = 0; $j < @pieces; $j += 2) {
        my @expressions = split(/\b(AND|OR|LIKE)\b/, $pieces[$j]);
        $expressions[-1] .= $pieces[$j+1] if $pieces[$j+1];
        my $i;
        for ($i = 0; $i < @expressions; ++$i) {
            next if !$expressions[$i] || $expressions[$i] =~ m/^\s+$/;
            my $expr = uc($expressions[$i]);
            if ($expr eq "OR" || $expr eq "AND") {
                $eval_expr .= "\n $expr ";
            } else {
                $eval_expr .= 
                    '(' . $self->__atomicExpression($expressions[$i]) . ')';
            }
        }
    }

    #print " --> $eval_expr\n";

    return $eval_expr;
}

sub __atomicExpression {
    my $self = shift;
    my $expression = shift;

    my $atom_expr = "";
    my ($lhs, $op, $rhs) = split(/([=><!][=>]?[iI]?)/, $expression, 2);
    die("Parse error: unidentified operator in expression:\n'$expression'\n")
        unless ($lhs && $op && $rhs);
    $lhs =~ s/^\s+//;
    $lhs =~ s/\s+$//;
    $rhs =~ s/^\s+//;
    $rhs =~ s/\s+$//;

    my $quoteflag = ($rhs =~ s/^(\"|\')//);
    my $quote = $1;
    die("Parse error: unbalanced quotes in expression\n")
      if ( $quoteflag && !($rhs =~ s/$quote$//) )
      || ( $quoteflag && $rhs =~ m/[^\\]$quote/ );

    if ($lhs eq "*") {
        my $field;
        foreach $field ($self->getFieldNames) {
            my $next = $self->__compareOneField($field, $op, $rhs);
            $atom_expr .= " OR " . $next if $next;
        }
        $atom_expr = substr($atom_expr, 4);
    } else {
        $atom_expr = $self->__compareOneField($lhs, $op, $rhs);
    }
    return $atom_expr;
}

sub __compareOneField {
    my $self = shift;
    my $lhs = shift;
    my $op = shift;
    my $rhs = shift;
    my $case_insensitive = shift || ($op =~ s/i$//i);

    #print "DEBUG: Called compareOneField with $lhs $op".($case_insensitive?"i":"")." $rhs\n";

    my $stdsql = $self->_getStandardSql();
    my $lower = $stdsql->function('lower');
    my $type = $self->getDataType($lhs) || die "Unknown field '$lhs'\n";

    my $expr;
    $op = "=" if $op eq "==";
    $op = "<>" if $op eq "!=";

    #print "DEBUG: dbi: " . $stdsql->allows_like_for_all_fields . "; type: " . $type->getOdbcType() . "\n";
    if ($stdsql->allows_like_for_all_fields() || $type->getOdbcType() == 1) {
        if ($rhs =~ m/[\*\?]/) {
            die("Can't combine relational operator with wildcard\n")
              if ($op =~ /^[><]=?$/ );

            $rhs =~ s/\*/%/g;
            $rhs =~ s/\?/_/g;
            if ($op eq "!=" || $op eq "<>") {
                $op = "NOT LIKE";
            } else {
                $op = "LIKE";
            }
        }
    } 
    else {
        # case sensitivity and wildcards do not apply
        $case_insensitive = 0;
        $rhs =~ s/^\*//;
        $rhs =~ s/\*$//;
    }

    my $rhs_value = $type->display2storage($rhs);
    my $dbh = $self->_getRawDBIHandle();
    if ($case_insensitive) {
        if ($op =~ /LIKE$/) {
            $rhs =~ s/([A-Za-z])/\[\u$1\l$1\]/g;
            $expr = "$lhs $op ".$dbh->quote($rhs_value, $type->getOdbcType());
        } else {
            $expr = "$lower($lhs) $op " 
                . $dbh->quote(lc($rhs_value), $type->getOdbcType()) ;
        }
    } 
    else {
        if ($type->isValid($rhs_value)) { 
            $expr = "$lhs $op ".$dbh->quote($rhs_value, $type->getOdbcType());
        }
        else {
            $expr = "1 = 0";
        }
    }
    return $expr;
}


1;

__END__

=head1 NAME

Extropia::Core::DataSource::DBI - A Perl5 object for manipulating DBI databases

=head1 SYNOPSIS

  use Extropia::Core::DataSource;

  my $ds = Extropia::Core::DataSource->create(
      -TYPE => "DBI",
      -DBI_DATASOURCE => "Sybase:server=SYBASE;database=pubs2",
      -USERNAME => "username",
      -PASSWORD => "password" );

=head1 DESCRIPTION

This module is a driver that implements the Extropia::Core::DataSource interface.
Thus, apart from the single line of code that creates this particular type
of driver, you use it in exactly the same way as you would any other 
Extropia::Core::DataSource.

See B<USAGE> for a description of driver-specific creation parameters.  
See L<Extropia::Core::DataSource> for a description of generic creation parameters 
and information on how to use this object.

=head1 USAGE

=head2 Object Creation

Do not create an Extropia::Core::DataSource::DBI object directly.  Instead,
call the Extropia::Core::DataSource->create() method with the following
parameters.  A DataSource object of the appropriate type will be returned.

These parameters are required, for all DBI DataSources:

=over 4

=item -TYPE

Specifies the type of DataSource to create.  Set to "DBI" for a DBI
DataSource.

=item -DBI_DATASOURCE

Specifies the type of DBD database and any necessary connection parameters.
See the specific DBD database documentation for details.  For example, to
connect to a Sybase database, you might use the following string:

  "Sybase:server=SERVER_NAME;database=pubs2"

=back

The remaining parameters are optional.  The following parameters are
specific to the DataSource::DBI driver:

=over 4

=item -USERNAME

Many database systems require you to provide a valid username and password
in order to access the data.  If not specified, the module will attempt to
connect to the database using an empty string as the username.

=item -PASSWORD

And this is where you specify the password.  If not specified, the module
will attempt to connect to the database using an empty string as the
password.

=back

This next set of optional parameters is common to all types of DataSource:

=over 4

=item -FIELD_NAMES

A reference to an array of field names, in the order in which they appear
in the DataSource file.

=item -FIELD_TYPES

A reference to a hash, in which field names are the keys and the
corresponding field types are the values.  Accepted values for field types
include:

    string/char/varchar/text        for character data
    date                            for dates
    datetime                        for combined date and time
    int/real/float/numeric/decimal  for numeric data; precision and scale 
                                    are not (currently) enforced
    auto                            for autoincrementing numeric data,
                                    often used for implementing a unique
                                    key field.
    ctime/mtime/time                RESERVED FOR FUTURE USE

Any field not assigned a field type defaults to string.  Any unrecognized
fieldtype results in the field being treated as a form of numeric data.

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

=item -KEY_FIELDS

A reference to an array of field names that together form a unique key for
a given record.  No two records should have the same values in all of their
key fields.

=item -UPDATE_STRATEGY

The update strategy tells the DataSource which fields should be used to
identify the records to be updated.  You must set this parameter to one of
the following constant values:

    Extropia::Core::DataSource::KEY_FIELDS
    Extropia::Core::DataSource::KEY_AND_MODIFIED_FIELDS
    Extropia::Core::DataSource::ALL_FIELDS
    Extropia::Core::DataSource::READ_ONLY

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

=head1 DEPENDENCIES

This module is the driver that marries the Extropia::Core::DataSource interface 
to the DBI (database independent) module interface.  Thus, both of these
interface modules are required.

In addition to the interface modules, a database-specific DBD module is
required.  At present, there are DBD modules for a wide variety of
databases, including DBD::Sybase, DBD::Oracle, DBD::MySQL, etc.

If date or time fields are used, Gordon Barr's TimeDate bundle is also
required.  Installing this bundle installs the following modules:

  Date::Parse
  Date::Format
  Date::Language
  Time::Zone

Furthermore, the Date::Parse module depends on Time::Local, which is part
of the standard Perl distribution.  Unfortunately, as of Perl 5.005_03, 
Time::Local had a serious bug that prevents it from handling dates between
1939 and 1969.  A patched version of Time::Local is available from Extropia,
and will be merged into the standard Perl distribution beginning with Perl
5.6.

=head1 VERSION

Extropia::Core::DataSource::DBI $Revision: 1.5 $

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

=head1 SEE ALSO

See Extropia::Core::DataSource for information on how to use this object.

=head1 COPYRIGHT

(c)1999, Extropia.com

This module is open source software, and may generally be used according to
the spirit of the "Perl Artistic License".  If you are interested, however,
the actual license for this module may be found at http://www.extropia.com
(or more directly, at http://www.extropia.com/download.html).

=head1 AUTHOR

Extropia::Core::DataSource::DBI is a Perl module written by Extropia
(http://www.extropia.com). Special technical and design acknowledgements
are given to Peter Chines, Gunther Birznieks and Selena Sol.

=head1 SUPPORT

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

Questions, comments and bug reports should be sent to support@extropia.com.

=cut

