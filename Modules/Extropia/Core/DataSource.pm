# $Id: DataSource.pm,v 1.10 2001/08/31 10:44:51 gozer Exp $
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

package Extropia::Core::DataSource;

use strict;

use vars qw($VERSION @ISA @EXPORT_OK @EXPORT);
use Carp;
use Exporter;
use Extropia::Core::Base qw(_rearrange _getDriver _cloneRef _equalsRef);
use Extropia::Core::DataSource::RecordSet;
use Extropia::Core::DataSource::Locale;

$VERSION = do { my @r = q$Revision: 1.10 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::Base Exporter);
@EXPORT_OK = qw(READ_ONLY KEY_FIELDS KEY_AND_MODIFIED_FIELDS ALL_FIELDS
                update);

# UpdateStrategy Options (constants)
sub READ_ONLY () { -1 };
sub KEY_FIELDS () { 1 };
sub KEY_AND_MODIFIED_FIELDS () { 2 };
sub ALL_FIELDS () { 3 };

%Extropia::Core::DataSource::op2condition = (
    '='  => '== 0',
    '==' => '== 0',
    '<'  => '== -1',
    '>'  => '== 1',
    '<=' => '!= 1',
    '>=' => '!= -1',
    '!=' => '!= 0',
    '<>' => '!= 0'
);

#
# create
#   Factory method
#
sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $source_type = shift @_;
    my @fields = @_;

    my $ds_class = _getDriver("Extropia::Core::DataSource", $source_type) or
        Carp::croak("DataSource type '$source_type' is not supported");
            
    # hand-off to specific implementation sub-class
    $ds_class->new(@fields);
}

# 
# new
#   Base constructor, handles all creation parameters that are common
#   to all DataSources.  Called from driver-specific new(), using the
#   following syntax:
#       my $self = $package->SUPER::new(@_);
#
sub new {
    my $package = shift;
    @_ = _rearrange(
        [-KEYWORD_SEARCH_OR_FLAG,
         -RECORDSET_PARAMS,
         -FIELD_NAMES,
         -FIELD_TYPES,
         '-KEY_FIELDS', # because of the KEY_FIELDS constant
         -UPDATE_STRATEGY,
         -LOCALE,
         -FIELD_SORTS],
        [], @_);
    # All of these fields are optional
    my $keyword_search_or_flag = shift || 0;
    my $recordset_data = shift || [-TYPE => 'ForwardOnly'];
    my $field_names = shift || [];
    my $field_types = shift || {};
    my $key_fields = shift || $field_names;
    my $update_strategy = shift || ALL_FIELDS;
    my $locale = shift || 'Default';
    my $field_sorts = shift || {};
    # note: remaining parameters are still in @_, awaiting processing

    my $self = {'_base_field_names'     => [],
                '_base_field_types'     => {},
                '_base_field_index'     => {},
                '_base_locale'          =>
                    Extropia::Core::DataSource::Locale->create(-TYPE => $locale),
                '_base_datatypes'       => {},
                '_base_field_sorts'     => $field_sorts,
                '_base_keyword_search_or_flag' => $keyword_search_or_flag,
                '_base_recordset_data'  => $recordset_data,
                '_base_key_fields'      => $key_fields,
                '_base_pending_updates' => []
               };
    # Does not need to be re-blessed into final package, if this
    # constructor is called using the following syntax:
    #    $self = $pkg->SUPER::new( @args );
    bless $self, ref $package || $package;

    # Unless above syntax is used, these calls will not be appropriately
    # polymorphic:
    $self->setUpdateStrategy($update_strategy);
    $self->_setFieldNames($field_names);
    $self->_setFieldTypes($field_types);

    return $self;
}

sub DESTROY {
    my $self = shift;
    if (my $disconnect = $self->can('disconnect'))
        {
        $self->$disconnect();
        }
} 

##
## Public Interface: Data Manipulation
##

#
# Method: add()
#   Adds record to DataSource, or to list of pending updates, if called
#   with -DEFER flag true.
# Parameters:
#   -ADD    Record to be added, specified as either a hash reference or an
#           array reference.
#   -DEFER  True if this add should be deferred to be performed in a batch
#           when doUpdate() is called.  Defaults to false.
# Returns:
#   True (1) if added successfully, undef if failed.  When -DEFER is true,
#   returns true now, will return real success value from doUpdate().
#   If undef returned, DS object will hold errors.
# Exceptions:
#   Croaks if invalid -ADD record provided.
#
sub add {
    my $self = shift;
    @_ = _rearrange([-ADD,-DEFER],[-ADD],@_);
    my $add_record = shift;
    my $defer = shift || 0;

    if (ref $add_record ne 'ARRAY' && ref $add_record ne 'HASH') {
        croak("DataSource->add() must be called with a reference to "
            . "a record to add,\nspecified as either a Hash ref or an "
            . "Array ref.\nThis routine was called incorrectly");
    }
    return undef unless $self->_canUpdate("AddError");

    my $real_add = $self->_recordDisplay2Internal($add_record) 
        || return undef;
    $self->__addPendingUpdate('ADD', $real_add);
    return $defer || $self->doUpdate(@_);
}

sub update {
    my $self = shift;
    @_ = _rearrange([-QUERY,-UPDATE,-DEFER],
                    [-QUERY,-UPDATE],@_);
    my $update_query = shift;
    my $update_record = shift;
    my $defer = shift || 0;
    
    if (!ref $update_query) {
        $update_query = $self->_buildExprTree($update_query);
        return undef if !defined($update_query);
    }
    elsif (ref $update_query ne "ARRAY") {
        croak("-QUERY for DataSource->update() should be either a "
            . "reference to an expression tree or a string");
    }
    croak("-UPDATE for DataSource->update() must be a Hash ref")
        if (ref $update_record ne 'HASH');

    return undef unless $self->_canUpdate("AddError");
    $self->__addPendingUpdate('UPDATE', $update_query, $update_record);
    return $defer || $self->doUpdate(@_);
}

sub delete {
    my $self = shift;
    @_ = _rearrange([-DELETE,-DEFER],[-DELETE],@_);
    my $delete_query = shift;
    my $defer = shift || 0;

    if (!ref $delete_query) {
        $delete_query = $self->_buildExprTree($delete_query);
        return undef if !defined($delete_query);
    }
    elsif (ref $delete_query ne "ARRAY") {
        croak("-QUERY for DataSource->delete() should be either a "
            . "reference to an expression tree or a string");
    }
      
    return undef unless $self->_canUpdate("AddError");
    $self->__addPendingUpdate('DELETE', $delete_query);
    return $defer || $self->doUpdate(@_);
}

sub clearUpdate {
    my $self = shift;

    $self->{'_base_pending_updates'} = [];
}

##
## Public Interface: Querying
##

sub keywordSearch {
    my $self = shift;
    @_ = _rearrange([-SEARCH,
                     -CASE_SENSITIVE,
                     -EXACT_FIELD_MATCH],
                     [],@_);
    my $search = shift || "";
    my $case_sensitive = shift || 0;
    my $exact_field_match = shift || 0;
    my @extra_args = @_;

    $search =~ s/^\s+|\s+//g;
    my $iop = ($case_sensitive ? "" : "i");
    my $wildcard = ($exact_field_match ? "" : "*");
    my $conjunction = ($self->getKeywordSearchOrFlag() ? " OR " : " AND ");

    # Build regular search expression to perform keyword searching
    my $power_search = "";
    if ($search) {
        my @phrases = $self->_splitOnQuotes($search, 1);
        my @terms = ();
        local $_;
        foreach (@phrases) {
            if (m/^(['"])(.+?)\1$/) {
                push @terms, $2;
            } else {
                s/^\s+|\s+$//g;
                push @terms, split(/\s+/);
            }
        }
        $power_search = join ($conjunction, 
          map {"* =$iop '$wildcard$_$wildcard'" } @terms);
    }
    #print "DEBUG keyword search $search => $power_search\n";

    return $self->search(-SEARCH => $power_search, @extra_args);
}

sub search {
    my $self = shift;
    @_ = _rearrange([-SEARCH,
                     -LAST_RECORD_RETRIEVED,
                     -MAX_RECORDS_TO_RETRIEVE,
                     -ORDER,
                     -RECORDSET_PARAMS],
                     [],@_);
    my $search = shift || "";
    my $last_record_retrieved   = shift;
    my $max_records_to_retrieve = shift;
    my $order = shift;
    my $recordset = shift || $self->_getRecordSetData();

    $search =~ s/^\s+|\s+$//g;

    my $expr_tree;
    $expr_tree = $self->_buildExprTree($search);
    $self->_setActiveQuery($expr_tree);
    if (defined $expr_tree) {
        return $self->_realSearch( 
            $expr_tree,
            $last_record_retrieved,
            $max_records_to_retrieve,
            $order, 
            $recordset 
        );
    } else {
        return 0;
    }
}

##
## Public Interface: Accessor and other methods
##

sub getFieldNames {
    my $self = shift;
    return @{$self->{'_base_field_names'}};
}

sub getFieldIndex {
    my $self = shift;
    my $field = shift;
    return $self->{'_base_field_index'}->{$field};
}

sub getFieldTypes {
    my $self = shift;
    return %{$self->{'_base_field_types'}};
}

sub getAutoincrementFieldName {
    my $self = shift;
    return $self->{'_base_autoincrement_field'};
}

sub getLastAutoincrementID {
    my $self = shift;
    return $self->{'_base_last_autoincrement_id'} || 0;
}

sub getDataType {
    my $self = shift;
    my $field = shift;
    return $self->{'_base_datatypes'}->{$field};
}

sub setDisplayFormat {
    my $self = shift;
    my $field = shift;
    my $format = shift;
    my $datatype = $self->getDataType($field);
    if (!$datatype) {
        $self->addError(
            -CODE    => 204,
            -MESSAGE => "Unknown field '$field'"
        );
    }
    elsif ($datatype->setDisplayFormat($format)) {
        return 1;
    } 
    else {
        $self->addError(
            -CODE    => 901,
            -MESSAGE => "Cannot set display format for $field"
        );
    }
    return 0;
}

sub getSort {
    my $self = shift;
    my $field = shift;
    return $self->{'_base_field_sorts'}->{$field} ||
        $self->getDataType($field);
}

sub setSort {
    my $self = shift;
    my $field = shift;
    my $sort = shift;
    if ( !defined($self->getFieldIndex($field)) ) {
        $self->addError(
            -CODE => 204,
            -MESSAGE => "Unknown field '$field'"
        );
        return 0;
    } elsif ( !$sort->can('compare') ) {
        $self->addError(
            -CODE => 902,
            -MESSAGE => "Sort object provided does not have a compare method"
        );
        return 0;
    } else {
        $self->{'_base_field_sorts'}->{$field} = $sort;
    }
}

sub getKeywordSearchOrFlag {
    return $_[0]->{'_base_keyword_search_or_flag'} || 0;
}

sub setKeywordSearchOrFlag {
    my $self = shift;
    my $flag = shift;
    return $self->{'_base_keyword_search_or_flag'} = $flag;
}

sub getUpdateStrategy {
    return $_[0]->{'_base_update_strategy'};
}

sub setUpdateStrategy {
    my ($self, $strat) = @_;
    if (   $strat == KEY_FIELDS 
        || $strat == READ_ONLY 
        || $strat == KEY_AND_MODIFIED_FIELDS
        || $strat == ALL_FIELDS) {
        $self->{'_base_update_strategy'} = $strat;
    } else {
        croak("Fatal Error: Invalid update strategy specified.\n"
            . "Use one of the constants from Extropia::Core::DataSource:\n"
            . join(", ", map {"Extropia::Core::DataSource::$_"} 
                qw(KEY_FIELDS READ_ONLY KEY_AND_MODIFIED_FIELDS ALL_FIELDS)));
    }
}

# PSC: Experimental; returns type of given field name or number
# These are safe versions; subclasses may choose to override these
# with DataSource-specific fast versions
sub getFieldType {
    my $self = shift;
    my $field = shift;
    croak "Method getFieldType must always be called with a parameter"
        unless defined($field);
    $field = $self->getFieldName($field) if $field =~ /^(\d+)$/;
    my %type = $self->getFieldTypes();
    return $type{$field};
}

# PSC: Experimental; returns name of given field number
sub getFieldName {
    my $self = shift;
    my $index = shift;
    my @fields = $self->getFieldNames();
    carp "Index $index is out of range" 
        if $index < 0 || $index > #@fields;
    return $fields[$index];
}


##
## Protected Interface: Called by DataSource and related objects only
##

#
# Method: _realSearch
#   Must be implemented in driver classes.
#   Prepares DataSource for query and constructs a RecordSet to deliver the
#   results.  Called by search() method above.
# Parameters (positional, only):
#   
# Returns:
#   RecordSet, if successful.  Undef if search failed.  Error will be added
#   to DS object on failure.
# Exceptions:
#

#
# Method: _searchForNextRecord
#   Returns next record that matches query criteria, if one exists, else
#   returns undef.
#

#
# Method: _skipToNextRecord
#   Returns raw form of next record that matches query criteria, if one
#   exists, else returns undef.  Supposed to provide an optimized means of
#   skipping records, in DataSources that allow this.  Should be overridden
#   in subclasses only where it can be optimized.  (See DataSource::DBI)
#
sub _skipToNextRecord {
    my $self = shift;
    return $self->_searchForNextRecord(@_);
}

##
## Protected Accessor Methods:
##

sub _getDefaultFieldType {
    return 'string';
}

sub _getDefaultDataTypeParams {
    return ();
}

sub _getRecordSetData {
    return $_[0]->{'_base_recordset_data'};
}

sub _getKeyFields {
    return $_[0]->{'_base_key_fields'};
}

sub _getPendingUpdates {
    return $_[0]->{'_base_pending_updates'};
}

sub _setFieldNames {
    my $self = shift;
    my $fields =  shift;
    
    my @field_list = ();
    $self->{'_base_field_index'} = {};
    if (ref($fields) eq "ARRAY") {
        my $i = 0;
        my $field;
        foreach $field (@$fields) {
            if ($field =~ /^\w+$/) {
                push @field_list, $field;
                $self->{'_base_field_index'}->{$field} = $i++;
            } else {
                die "Illegal field name '$field'\n";
            }
        }
    } else {
        croak ("_setFieldNames must be called with a reference to an array");
    }
    $self->{'_base_field_names'} = \@field_list;
}

sub _setFieldTypes {
    my $self = shift;
    my $types = shift || {};

    $self->{'_base_autoincrement_field'} = '';
    if (ref($types) eq "HASH") {
        my $field;
        foreach $field ($self->getFieldNames()) {
            my $type = $types->{$field} || $self->_getDefaultFieldType();
            $self->{'_base_field_types'}->{$field} = $type;
            if (ref $type eq 'ARRAY') {
                my @args = _rearrange([-TYPE],[-TYPE],@$type);
                $self->__setOneFieldType($field, @args);
            }
            elsif ($type =~ m'^(\w+)\s*\(([^\)]+)\)') {
                warn "WARNING: This style of specifying DataTypes ($type) "
                    ."is deprecated.\n"
                    ."Please start using the new named parameter form, "
                    ."e.g. [-TYPE => 'Date', -DISPLAY => 'm/d/yy']\n";
                my @args = split('\|', $2 || '');
                $self->__setOneFieldType($field, $1, @args);
            }
            elsif ($type =~ m/^\w+$/) {
                $self->__setOneFieldType($field, $type);
            }
            else {
                die "Unrecognized format in field type specification for "
                    ."$field: '$type'\n";
            }
        }
    } else {
        confess("_setFieldTypes must be called with a reference to a hash");
    }
}

sub __setOneFieldType {
    my ($self, $field, @type) = @_;
    my $class = shift @type;
    if ($class eq lc($class)) {
        $class = ucfirst($class);
    }
    if ($class =~ /^Auto/i) {
        if ($self->{'_base_autoincrement_field'}) {
            $self->addError(
                -CODE => 193,
                -MESSAGE => "There can be only one autoincrement field per table.",
                -SOURCE => 'DataSource::Base',
                -CALLER => (caller(2))[0]
            );
        } else {
            $self->{'_base_autoincrement_field'} = $field;
        }
    }
    if (!@type) {
        @type = $self->_getDefaultDataTypeParams($class);
    }
    $self->{'_base_datatypes'}->{$field} =
        $self->{'_base_locale'}->getDataType($class, @type)
        || die "Unable to set FieldType to [$class @type]\n";
}


sub _getAllDataTypes {
    return $_[0]->{'_base_datatypes'};
}

sub _getAllSorts {
    return $_[0]->{'_base_field_sorts'};
}

sub _setLastAutoincrementID {
    my ($self, $id) = @_;
    $self->{'_base_last_autoincrement_id'} = $id;
}

sub _setActiveQuery {
    my $self = shift;
    $self->{'_base_active_query'} = shift;
}

sub _matchesActiveQuery {
    my $self = shift;
    my $current = shift;
    my $active = $self->{'_base_active_query'};
    return _equalsRef($current, $active);
}

sub _canUpdate {
    my ($self, $add_error) = @_;
    my $can_update = ($self->getUpdateStrategy() != READ_ONLY);
    if (!$can_update && $add_error) {
        $self->addError(
            -CODE => 203,
            -MESSAGE => 'Cannot update a Read Only DataSource'
        );
    }
    return $can_update;
}

##
## Protected "Helper" Methods:
##

#
# Protected method: _successfulUpdate
#   Returns the appropriate success value from doUpdate() method.
# Arguments (positional only):
#   $return_original  Value of -RETURN_ORIGINAL flag passed to
#                       update(), delete() or doUpdate()
#   $ra_original      Original records, in display format
#   $affected_rows    Number of rows affected by all updates in batch
# Returns
#   RecordSet, if $return_original, otherwise $affected_rows
#
sub _successfulUpdate {
    my ($self, $return_original, $ra_original, $affected_rows) = @_;
    $self->clearUpdate();
    if ($return_original) {
        return Extropia::Core::DataSource::RecordSet->create(
            -TYPE => 'Static'
          , -DATA_BUFFER => $ra_original
          , -FIELD_NAMES => [$self->getFieldNames()]
          , -DATA_TYPES  => {%{$self->_getAllDataTypes()}}
          , -FIELD_SORTS => {%{$self->_getAllSorts()}}
        );
    } else {
        return $affected_rows;
    }
}
    
#
# Protected method: _buildExprTree
# Convert a query string, perhaps containing embedded quotes, into the
# standard DataSource expression tree
#
# This routine catches exceptions that may be thrown by __buildSubExprTree
# or lower-level routines and returns undef to signal parsing failure.
#
sub _buildExprTree {
    my $self = shift;
    my $search = shift || '';

    if (ref $search eq 'ARRAY') {
        return $search;
    } elsif (ref $search) {
        confess("Search is not an array ref or a string.");
    }
    #print "DEBUG: $search\n";
    my (@pieces, @result);
    eval {
        @pieces = $self->_splitOnQuotes($search);
        # insert placeholders for quoted pieces
        my $new_expr = $self->__stripQuotes(@pieces);
        $new_expr =~ s/\band\b/AND/gi;
        $new_expr =~ s/\bor\b/OR/gi;
        if ($new_expr) {
            push @result, $self->__buildSubExprTree($new_expr); 
        }
    };
    if ($@) {
        $self->addError(
            -CODE => 300,
            -MESSAGE => "Parse error: $@ in expression:\n$search\n",
            -SOURCE => 'DataSource::Base'
        );
        return undef;
    }
    #use Data::Dumper;
    #print "DEBUG before fillQuotes: ", Dumper(\@result);
    if (@result) {
        # re-insert quoted pieces at placeholders
        $self->__fillQuotes(\@result, \@pieces);
        return \@result;
    }
    return '';
}

#
# Protected method: _matches
# Returns true if record (passed as reference to a hash) satisfies the
# search criteria, else false.
# Dies if error is encountered; should be called from within an eval block
# to catch these exceptions.
#
# $allow_incomplete_record is an optional parameter that allows
# us to see if a record with incomplete information matches the
# query string so far...
#
sub _matches {
    my $self      = shift;
    my $ra_search               = shift || "1"; # Default returns true
    my $record                  = shift;
    my $allow_incomplete_record = shift || 0;

#use Data::Dumper;
#
#print Data::Dumper->Dump([$ra_search]); 
#if ((keys %$record) == 0) {
#       print("$record was bad..." . join(",",caller(1)) . "\n");
#   }
    if (!ref($ra_search)) {
        $self->__wholeExprEvaluator($ra_search, $record,
                $allow_incomplete_record);
    } 
    elsif (ref $ra_search eq "ARRAY") {
        my $string_to_evaluate = "";
        my $element;
        foreach $element (@$ra_search) {
            my $value = 0;
            if (!ref($element)) {
                $value = $element || '';
            } else {
                $value = $self->_matches($element, $record, $allow_incomplete_record);
            }
            $string_to_evaluate .= " $value "; 
        }
        $self->__wholeExprEvaluator($string_to_evaluate, $record,
                $allow_incomplete_record);
    } 
    else {
        confess("Search is not array reference or string. ");
    }
}

#
# Protected method: _optimizeAdds
# To optimize a set of updates for use on a file-based datasource,
# the updates should be arranged so that only one pass over the
# file is needed.  To do this, interactions between the updates 
# must be detected and resolved, in order to generate correct results.  
#
# This first version of this routine is intended
# to resolve the following types of interactions:
#   ADDs modified by a later UPDATE
#   ADDs removed by a later DELETE
#
# The following interactions are not addressed:
#   UPDATEs modified by a later UPDATE is best resolved by applying
#     all of the UPDATEs (in sequence) to each row.
#   UPDATEs removed by a later DELETE is a minor performance issue
#     and does not affect the accuracy of the results.
#   DELETEs occasioned/averted by an earlier UPDATE
# These latter interactions are easily addressed by applying all of
# the UPDATEs and DELETEs in sequence to each row.  The minor gain
# in efficiency to be gained by combining them may or may not be 
# outweighed by the compute time to resolve them (not to mention the
# programming time).
#
# On entrance: "pending_updates" => ordered updates (ADDs, UPDATEs, DELETEs)
#
# On exit    : "pending_updates" => ordered UPDATEs/DELETEs
#            :                      (unchanged, except for removals of ADDs)
#            : returns           => ADDs modified as necessary to be 
#            :                      performed *after* the UPDATEs/DELETEs. 
#
# On error   : returns 0, adds an error to object error stack
#            : tries to return pending updates to a stable state
#
sub _optimizeAdds {
    my $self = shift;

    my $pending_updates = $self->_getPendingUpdates();
    my @pending_adds = ();

    my $i;
    for ($i = 0; $i < @$pending_updates; ++$i) {
        next unless $pending_updates->[$i]->[0] eq "ADD";
        
        # Current update is an add; remove from update list
        my $add = splice(@$pending_updates, $i, 1);
        --$i;

        # What interacts with it?

        my $j;
        for ($j = $i+1; $j < @$pending_updates; ++$j) {
            my $follower = $pending_updates->[$j];

            if ($follower->[0] eq "UPDATE" || $follower->[0] eq "DELETE") {
                if (eval{ $self->_matches($follower->[1], $add->[1]) }) {
                    if ($follower->[0] eq "UPDATE") {
                        my $field;
                        foreach $field (keys %{$follower->[2]}) {
                            $add->[1]->{$field} = $follower->[2]->{$field};
                        }
                    } else { # DELETE
                        $add = 0;
                        last;
                    }
                } elsif ($@) {
                    $self->addError(
                        -CODE    => 300,
                        -MESSAGE => $@, 
                        -SOURCE  => 'DataSource::Base',
                        -CALLER  => (caller)[0] 
                    );
                    splice(@$pending_updates, $j, 0, $add);
                    push @$pending_updates, @pending_adds;
                    return 0;
                }
            }
        }

        # If not deleted, move add to pending_adds list
        push(@pending_adds, $add) if $add;
    }
    return \@pending_adds;
}

#
# Protected method: _recordStorage2Internal
# Returns hash-ref based record in internal format, built from list-ref in
# storage format
#
sub _recordStorage2Internal {
    my $self = shift;
    my $ra_row = shift;

    confess "Record is not list-ref in _recordStorage2Internal\n"
        unless ref $ra_row eq 'ARRAY';
    my $datatype = $self->_getAllDataTypes();
    my %record = ();
    my ($data, $conv);
    my $field;
    foreach $field ($self->getFieldNames()) {
        $data = $ra_row->[$self->getFieldIndex($field)];
        $conv = $datatype->{$field}->storage2internal($data);
        if (defined($data) && !defined($conv)) {
            $self->addError(
                    -CODE => 202,
                    -MESSAGE => "_recordStorage2Internal: Illegal value '$data' for field '$field': "
                        . ref($datatype->{$field})
            );
            return undef;
        }
        $record{$field} = $conv;
    }
    return \%record;
}

#
# Protected method: _recordInternal2Display
# Returns list-ref based record in display format, built from hash-ref in
# internal format
#
sub _recordInternal2Display {
    my $self = shift;
    my $rh_row = shift;

    confess "Record is not hash-ref in _recordInternal2Display\n"
        unless ref $rh_row eq 'HASH';
    my $datatype = $self->_getAllDataTypes();
    my @record = ();
    my ($data, $conv);
    my $field;
    foreach $field ($self->getFieldNames()) {
        $data = $rh_row->{$field};
        $conv = $datatype->{$field}->internal2display($data);
        if (defined($data) && !defined($conv)) {
            $self->addError(
                    -CODE => 202,
                    -MESSAGE => "_recordInternal2Display: Illegal value '$data' for field '$field': "
                        . ref($datatype->{$field})
            );
            return undef;
        }
        push @record, $conv;
    }
    return \@record;
}

#
# Protected method: _recordDisplay2Internal
# Returns hash-ref based record in storage format, built from either a
# hash-ref or list-ref in display format
#
sub _recordDisplay2Internal {
    my $self = shift;
    my $r_row = shift;

    my $datatype = $self->_getAllDataTypes();
    my @fields = $self->getFieldNames();
    if (ref $r_row eq 'ARRAY') {
        my %in = ();
        @in{@fields} = @$r_row;
        $r_row = \%in;
    } 
    if (ref $r_row ne 'HASH') {
        confess "Record should be list-ref or hash-ref "
            . "in _recordDisplay2Internal\n";
    }
    my %record = ();
    my ($data, $conv);
    my $field;
    foreach $field ($self->getFieldNames()) {
        $data = $r_row->{$field};
        if (defined $data) {
            $conv = $datatype->{$field}->display2internal($data);
            if (!defined($conv)) {
                $self->addError(
                        -CODE => 202,
                        -MESSAGE => "_recordDisplay2Internal: Illegal value '$data' for field '$field': "
                            . ref($datatype->{$field})
                );
                return undef;
            }
            $record{$field} = $conv;
        }
    }
    return \%record;
}

#
# Protected method: _recordInternal2Storage
# Returns list-ref based record in storage format, built from a
# hash-ref in internal format
#
sub _recordInternal2Storage {
    my $self = shift;
    my $rh_row = shift;

    if (ref $rh_row ne 'HASH') {
        confess "Record is not hash-ref in _recordInternal2Storage\n";
    }
    my $datatype = $self->_getAllDataTypes();
    my @record = ();
    my ($data, $conv);
    my $field;
    foreach $field ($self->getFieldNames()) {
        $data = $rh_row->{$field};
        $conv = $datatype->{$field}->internal2storage($data);
        if (defined($data) && !defined($conv)) {
            $self->addError(
                    -CODE => 202,
                    -MESSAGE => "_recordInternal2Storage: Illegal value '$data' for field '$field': "
                        . ref($datatype->{$field})
            );
            return undef;
        }
        push @record, $conv;
    }
    return \@record;
}

#
# Protected method: _recordStorage2Display
# Returns array-ref based record in display format, built from array-ref 
# in storage format.  Takes advantage of storage2display() optimizations in
# DataType, if any.
#
sub _recordStorage2Display {
    my $self = shift;
    my $ra_row = shift;

    confess "Record is not array-ref in _recordStorage2Display\n"
        unless ref $ra_row eq 'ARRAY';
    my $datatype = $self->_getAllDataTypes();
    my @record = ();
    my ($data, $conv);
    my $field;
    foreach $field ($self->getFieldNames()) {
        $data = $ra_row->[$self->getFieldIndex($field)];
        $conv = $datatype->{$field}->storage2display($data);
        if (defined($data) && !defined($conv)) {
            $self->addError(
                    -CODE => 202,
                    -MESSAGE => "_recordStorage2Display: Illegal value '$data' for field '$field': "
                        . ref($datatype->{$field})
            );
#print ":::$data," . $datatype->{$field} . "\n";

            return undef;
        }
        push @record, $conv;
    }
    return \@record;
}


##
## Private Methods: do not call these from any code outside this file
##

sub __addPendingUpdate {
    my ($self, @update) = @_;
    @update = map { _cloneRef($_) } @update;
    push @{$self->{'_base_pending_updates'}}, \@update;
}

sub __operator2condition {
    my $operator = shift;
    return $Extropia::Core::DataSource::op2condition{$operator};
}

sub __buildSubExprTree {
    my $self = shift;
    my $search = shift;

    #print "DEBUG sub-expr: $search\n";

    my $open_paren = index($search,"(");
    my $first_open_paren = $open_paren;
    my $close_paren = index($search,")");
    my $paren_count = 0;
    return $search if ($open_paren == -1 && $close_paren == -1);

    # Find close paren matching first open paren
    while ($open_paren < $close_paren && $open_paren > -1) {
        while ($open_paren < $close_paren && $open_paren > -1) {
            ++$paren_count;
            $open_paren = index($search,"(",$open_paren + 1);
        }
        while ($paren_count > 1 && $close_paren > -1) {
            --$paren_count;
            $close_paren = index($search, ")", $close_paren + 1);
        }
    }

    if ($paren_count == 1) {
        my $first_part = "";
        $first_part = substr($search, 0, $first_open_paren)
            if ($first_open_paren > 0);
        my $in_paren = substr($search,
                              $first_open_paren + 1,
                              $close_paren - 1 - $first_open_paren);
        my $last_part = "";
        $last_part = substr($search, $close_paren + 1)
            if ($close_paren < length($search) - 1);

        #print "DEBUG Division: '$first_part [ $in_paren ] $last_part'\n";

        return (
                $first_part, 
                [ $self->__buildSubExprTree( $in_paren ) ],
                $self->__buildSubExprTree( $last_part )
               );
    }
    die "Unbalanced parentheses in query string\n";
}

sub _splitOnQuotes {
    my $self = shift;
    my $string = shift;
    my $skip_tests = shift;

    # Break search into quoted and not-quoted pieces
    my @pieces = ($string =~ /\G("[^"]*"|'[^']*'|[^'"]*)/g);
    pop @pieces;    # eliminate empty piece at end
    unless ($skip_tests) {
        die "Search expression can't start with a string literal\n"
            if $string =~ /^['"]/;
        my $i;
        for ($i = 0; $i < @pieces; ++$i) {
            if ($i & 1) {
                die "Unbalanced quotes: $string\n" 
                    unless $pieces[$i] =~ /^(?:'[^']*'|"[^"]*")$/;
            } else {
                die "Unbalanced quotes: $string\n" if $pieces[$i] =~ /['"]/;
            }
        }
    }
    return @pieces;
}

sub __stripQuotes {
    my $self = shift;
    my @pieces = @_;

    my $new_string = '';
    my $i;
    for ($i = 0; $i < @pieces; ++$i) {
        if ($pieces[$i] =~ /^['"]/) {
            $new_string .= '~' . $i . '~';
        } else {
            $new_string .= $pieces[$i];
        }
    }
    return $new_string;
}

sub __fillQuotes {
    my $self = shift;
    my $expr_tree = shift;
    my $replacements = shift;

    if (ref $expr_tree eq "ARRAY") {
        for (my $i = 0; $i < @$expr_tree; ++$i) {
            $expr_tree->[$i] = 
                $self->__fillQuotes($expr_tree->[$i], $replacements);
        }
        return $expr_tree;
    } 
    elsif (ref $expr_tree) {
        croak "Expression not array reference or string";
    }
    else {
        my @pieces = split(/~(\d+)~/, $expr_tree);
        for (my $i = 1; $i < @pieces; $i += 2) {
            $pieces[$i] = $replacements->[$pieces[$i]];
        }
        return join('', @pieces);
    }
}

# Evaluates entire expression regardless of number of fields
#
# GB: $allow_incomplete_record is used when we are delibrately
# evaluating a record that has not had all fields filled in
# 
# See __atomicExprEvaluator for reason...
#
sub __wholeExprEvaluator {
    my $self = shift;
    my $whole_expr              = shift;
    my $record                  = shift;
    my $allow_incomplete_record = shift;

    my $eval_expr = "";
    my @pieces = $self->_splitOnQuotes($whole_expr);
    for (my $j = 0; $j < @pieces; $j += 2) {
        my @expressions = split(/\b(AND|OR)\b/, $pieces[$j]);
        $expressions[-1] .= $pieces[$j+1] if $pieces[$j+1];
        for (my $i = 0; $i < @expressions; $i++) {
            my $expr = $expressions[$i];
            if ($expr eq "OR") {
                $eval_expr .= "\n || ";
            } elsif ($expr eq "AND") {
                $eval_expr .= "\n && ";
            } elsif ($expr =~ /^\s*$/) {
                next;
            } else {
                $eval_expr .= 
                    "\$self->__atomicExprEvaluator(q~$expr~,\$record,\$allow_incomplete_record) "; 
            }
        } # next $i
    } # next $j
    my $result = eval $eval_expr || "0";
    die $@ if $@;   # pass error up the chain
    return $result;
}

# Evaluates simple operand + operator + operand expressions
#
# The third param, $allow_incomplete_record, allows us to
# pass an incomplete record hash. Fields that do not exist
# yet will have their expressions evaluate to true.
#
sub __atomicExprEvaluator {
    my $self = shift;
    my $expression              = shift;
    my $record                  = shift;
    my $allow_incomplete_record = shift;

    #print ":$expression:\n";
    $expression =~ s/^\s+|\s+$//g;
    if ($expression eq "1" || $expression eq "0") {
        return $expression;
    }

    my ($lhs, $op, $rhs) = split(/([=><!][=>]?[iI]?)/, $expression, 2);
    die("Parse error: unidentified operator in expression:\n'$expression'\n")
        unless ($lhs && $op && $rhs);
    $lhs =~ s/^\s+|\s+$//g;
    $rhs =~ s/^\s+|\s+$//g;
    if ($rhs =~ s/^(\"|\')//) {
        my $quote = $1;
        die("Parse error: unbalanced quotes in expression:\n'$expression'\n")
            if ($rhs !~ s/$quote$// || $rhs =~ m/[^\\]$quote/);
    }
    
#print "Dumper1: " . Dumper([$lhs,$self->getFieldIndex($lhs),
#                     $record->{$lhs},$allow_incomplete_record,$record]) if ($allow_incomplete_record == 0);
    if ($lhs eq "*") {
        my $boolean = 0;
        my $field;
# 
# if $lhs is a * then there is no way we can compare
# all the fields if we don't have them and we allow incomplete
# records...
#
        if ($allow_incomplete_record) {
            return 1;
        }
        foreach $field (keys %$record) {
            if ($self->__compareOneField($field,$record->{$field},$op,$rhs)) {
                $boolean = 1;
                last;
            }
        }
        return $boolean;
    } elsif (!defined($self->getFieldIndex($lhs))) {
        die("Parse error: unknown fieldname \'$lhs\'\n");
    } elsif (!defined($record->{$lhs})) {
        return $allow_incomplete_record;
    }
    return $self->__compareOneField($lhs, $record->{$lhs}, $op, $rhs);
#    } elsif (defined($self->getFieldIndex($lhs)) &&
#             (defined($record->{$lhs}) || !$allow_incomplete_record)) {
#        $self->__compareOneField($lhs, $record->{$lhs}, $op, $rhs);
# If incomplete field 
#    } elsif ($allow_incomplete_record) {
#        return 1;
#    } else {
#        $| = 1;
# use Data::Dumper;
#      print "Dumper2: " . Dumper([$self->getFieldIndex($lhs),
#                     $record->{$lhs},$allow_incomplete_record,
#                     $self->{_base_field_index},$record]);
#       if (!defined($record->{$lhs})) {
#           confess("Stack trace...");
#       }
#        die("Parse error: unknown fieldname '$lhs'\n");
#    }
} 

sub __compareOneField {
    my $self = shift;
    my $lhs = shift;
    my $lhs_value = shift;
    my $op = shift;
    my $rhs = shift;
    my $case_insensitive = shift || ($op =~ s/i$//i);

#print "Called compareOneField with $lhs ($lhs_value) $op".($case_insensitive?"i":"")." $rhs\n";

    my $boolean_value;
    my $type = $self->getDataType($lhs) || die "Unknown field '$lhs'\n";
    if ($rhs =~ m/[\*\?]/) {
        return $self->__compareWildcard($lhs, $lhs_value, $op, $rhs, 
            $case_insensitive);
    }

    my $rhs_value = $type->display2internal($rhs);
    # Invalid data for this DataType
    if (defined($rhs) && !defined($rhs_value)) {
        return "0";
    }
    my $condition = __operator2condition($op);
    if ($case_insensitive) {
         $lhs_value = lc($lhs_value);
         $rhs_value = lc($rhs_value);
    }
    $boolean_value = 
        eval "\$type->compare(\$lhs_value, \$rhs_value) $condition" || "0";
#print "BOOL IN ONE FIELD: $lhs_value $op $rhs => $boolean_value\n";
    return $boolean_value;
}

sub __compareWildcard {
    my $self = shift;
    my $lhs = shift;
    my $lhs_value = shift;
    my $op = shift;
    my $rhs = shift;
    my $case_insensitive = shift || ($op =~ s/i$//i);

    # if operator is relational, wildcard must be only at end,
    # and then can be ignored
    if ($op =~ /^[><]=?$/ ) {
        return $self->__compareOneField($lhs, $lhs_value, $op, 
                        substr($rhs,0,-1), $case_insensitive)
            if substr($rhs,0,-1) !~ m/[\*\?]/;
        die("Can't combine relational operator with wildcard\n");
    }

    $rhs =~ s/\*/\.\*/g;
    $rhs =~ s/\?/\./g;
#    $rhs = quotemeta $rhs;
#    $rhs =~ s/\*/.*/g;
#    $rhs =~ s/\?/./g;
    # temp correction, before quotemeta will be used: escape unsafe chars
    $rhs =~ s/([\$\@\%])/\\$1/g;
    my $newop = "=~";
    $newop = "!~" if ($op eq "!=" || $op eq "<>");
    my $opt = "s";
    $opt .= "i" if $case_insensitive;

    my $string = "\$lhs_value $newop m/^$rhs\$/$opt";
    #print "DEBUG-- $lhs $newop m/^$rhs\$/$opt => $boolean_value\n$@\n";
    #print "DEBUG-- $lhs $newop m/^$rhs\$/$opt => $boolean_value\n";
    #print "DEBUG-- $string
#   E::dumper($string);
    my $boolean_value = eval $string;
#    my $boolean_value = eval "\$lhs_value $newop m/^\\\Q$rhs\\\E\$/$opt";
    #print "DEBUG-- $lhs $newop m/^$rhs\$/$opt => $boolean_value\n$@\n";
    return $boolean_value || "0";
}

1;
__END__

