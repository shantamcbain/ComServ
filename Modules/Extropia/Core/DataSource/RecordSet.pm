# $Id: RecordSet.pm,v 1.2 2002/06/28 11:23:22 cyph Exp $
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


package Extropia::Core::DataSource::RecordSet;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver _notImplemented);
use vars qw($VERSION @ISA);

$VERSION = do { my @r = q$Revision: 1.2 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw( Extropia::Core::Base );

sub NO_RECORD () { -1 }
sub BEFORE_FIRST_RETRIEVE () { -2 }

sub create {
    my $package = shift;
    @_ = _rearrange([-TYPE],[-TYPE],@_);
    my $type = shift @_;
    my @fields = @_;

    my $rs_class = _getDriver("Extropia::Core::DataSource::RecordSet", $type)
        || croak("RecordSet type '$type' is not supported");
            
    # hand-off to specific implementation sub-class
    $rs_class->new(@fields);
}

sub new {
    my $package = shift;
    @_ = _rearrange(
        [-DATASOURCE,
         -REAL_SEARCH_QUERY, 
         -KEY_FIELDS, 
         -UPDATE_STRATEGY,
         -LAST_RECORD_RETRIEVED, 
         -MAX_RECORDS_TO_RETRIEVE,
         -ORDER],
        [-DATASOURCE,
         -REAL_SEARCH_QUERY,
         -KEY_FIELDS,
         -UPDATE_STRATEGY],@_);
          
    my $self = {};
    $self->{'datasource'} = shift;
    $self->{'search_expression'} = shift;
    $self->{'key_fields'} = shift;
    $self->{'update_strategy'} = shift;
    $self->{'last_record_retrieved'} = shift || 0;
    $self->{'max_records_to_retrieve'} = shift || 0;
    $self->{'order'} = shift || 0;

    $self->{'databuffer'} = [];
    $self->{'databuffer_start_offset'} = 0;
    $self->{'retrieval_finished'} = 0;
    $self->{'total_retrieval_finished'} = 0;
    $self->{'total_matching_records'} = 0;

    bless $self, ref $package || $package;
    $self->{'index_to_databuffer'} = BEFORE_FIRST_RETRIEVE;

    $self->_performInitialOrdering();
    return $self;
}

#
# Methods to Retrieve data
#

sub getRecord {
    my $self = shift;

    $self->moveNext 
        if $self->{"index_to_databuffer"} == BEFORE_FIRST_RETRIEVE;
    return undef if $self->{"index_to_databuffer"} == NO_RECORD;
    return $self->{"databuffer"}->[$self->{"index_to_databuffer"}];
}

sub getAllRecords {
    my $self = shift;

    # If user had been grabbing records one at a time before,
    # then buffer will include previous record, but that's his lookout
    $self->finishRetrieval();
    return $self->{"databuffer"};
}

sub getRecordAsHash {
    my $self = shift;

    my $ra_fields = $self->getRecord();
    return undef unless $ra_fields;

    my %rh_fields = ();
    my @field_names = $self->{"datasource"}->getFieldNames();
    @rh_fields{@field_names} = @$ra_fields;
    return \%rh_fields;
}

sub getAllRecordsAsHash {
    my $self = shift;

    my $old_index = $self->getRecordNumber();
    my $ra_records = [];

    $self->moveFirst();
    my $rh_record;
    while (($rh_record = $self->getRecordAsHash()) &&
           !$self->endOfRecords()) {
        push(@$ra_records, $rh_record);
        $self->moveNext();
    }
    $self->setRecordNumber($old_index);
    return $ra_records;
}

sub getField {
    my $self = shift;
    my $fieldname = shift;

    my $ra_fields = $self->getRecord();
    return undef unless defined $ra_fields;

    if ($fieldname =~ /^\d+$/) {
        return $ra_fields->[$fieldname];
    } else {
        my $index = $self->{"datasource"}->getFieldIndex($fieldname);
        if (defined $index) {
            return $ra_fields->[$index];
        } else {
            croak("Field '$fieldname' not in ResultSet.");
        }
    }
} 

sub getFieldNames {
    my $self = shift;
    return $self->getDataSource()->getFieldNames();
}

#
# Methods to Move around within RecordSet
#

sub moveFirst {
    my $self = shift;

    if (!$self->isRetrievalFinished() &&
        @{$self->{"databuffer"}} < 1) {
        $self->_retrieveNextRecord();
    }
    if (@{$self->{"databuffer"}} > 0) {
        $self->{"index_to_databuffer"} = 0;
    }
    return $self->getRecordNumber();
}

sub moveLast {
    my $self = shift;

    $self->finishRetrieval();

    if (@{$self->{"databuffer"}} > 0) {
        $self->{"index_to_databuffer"} = @{$self->{"databuffer"}} - 1;
    }
    return $self->getRecordNumber();
}

sub moveNext {
    my $self = shift;

    return -1 if $self->{"index_to_databuffer"} == NO_RECORD;

#print "DEBUG in moveNext: start at ", $self->{"index_to_databuffer"}, " and ", scalar @{$self->{"databuffer"}}, " rows in buffer\n";

    my $gotNeededRec = 1;
    if ($self->{"index_to_databuffer"} == BEFORE_FIRST_RETRIEVE) {
        $gotNeededRec = $self->_retrieveNextRecord();
        $self->{"index_to_databuffer"} = 0;
    } 
    elsif ($self->{"index_to_databuffer"} >= @{$self->{"databuffer"}} - 1) {
        if ($self->isRetrievalFinished) {
#use Data::Dumper;
#           print Data::Dumper->Dump([@{$self->{"databuffer"}},
#                    $self->{"index_to_databuffer"}]);
            $gotNeededRec = 0;
        } else {
            $gotNeededRec = $self->_retrieveNextRecord();
        }
    }

    if ($self->{"index_to_databuffer"} < @{$self->{"databuffer"}} - 1) {
        ++$self->{"index_to_databuffer"};
    } 
    elsif (!$gotNeededRec) {
        $self->{"index_to_databuffer"} = NO_RECORD;
    }

#print "DEBUG in moveNext: end   at ", $self->{"index_to_databuffer"}, " and ", scalar @{$self->{"databuffer"}}, " rows in buffer\n";

    return $self->getRecordNumber();
}

sub movePrevious {
    my $self = shift;

    if ($self->{"index_to_databuffer"} > 0) {
        $self->{"index_to_databuffer"}--;
    }
    return $self->getRecordNumber();
}

sub setRecordNumber {
    my $self = shift;
    my $record_number = shift;

    $self->moveFirst() if $record_number < $self->getRecordNumber();

    # If still before beginning, desired record has been removed from buffer
    if ($record_number < $self->getRecordNumber()) {
        $self->{"index_to_databuffer"} = NO_RECORD;
    } else {
        while (!$self->isRetrievalFinished() &&
            $self->getRecordNumber() <= $record_number) {
            $self->moveNext(); 
        }
    }
    return $self->getRecordNumber();
}

#
# Methods to get information about RecordSet
#

sub getRecordNumber {
    my $self = shift;

    return -1 if $self->{"index_to_databuffer"} < 0;
    return $self->{"index_to_databuffer"} + $self->{"databuffer_start_offset"};
}

sub endOfRecords {
    my $self = shift;

    if ($self->{"index_to_databuffer"} == BEFORE_FIRST_RETRIEVE) {
        $self->moveNext();
    }
#$self->{"databuffer"}]);
    return ($self->{"index_to_databuffer"} == NO_RECORD);
}

sub isEmpty {
    my $self = shift;
    if ($self->{'index_to_databuffer'} == BEFORE_FIRST_RETRIEVE) {
        $self->moveNext();
    }
    return ($self->isRetrievalFinished() && @{$self->{'databuffer'}} == 0);
}

sub getTotalCount {
    my $self = shift;

    $self->finishRetrieval();
    if ( !$self->{'total_retrieval_finished'} ) {
        while ( $self->{'datasource'}->
               _searchForNextRecord($self->{'search_expression'}) ) {
            ++$self->{'total_matching_records'};
        }
        $self->{'total_retrieval_finished'} = 1;
    }
    return $self->{'total_matching_records'};
}

sub getCount {
    my $self = shift;
    $self->finishRetrieval();
    return $self->{'databuffer_start_offset'} + @{$self->{'databuffer'}};
}

sub isRetrievalFinished {
    my $self = shift;
    return $self->{"retrieval_finished"};
}

#
# Other Public Methods
#

sub finishRetrieval {
    my $self = shift;

    # This method makes no sense without buffering
    # so buffering is forced
    while ($self->_retrieveNextRecord(1)) { }
}

sub getRecordIDQuery {
    my $self = shift;
    my $update_record = shift;
    my $strategy = shift || $self->{'update_strategy'};

    my $rh_record = $self->getRecordAsHash();

    my @keys;
    if ($strategy == Extropia::Core::DataSource::KEY_FIELDS() ||
        $strategy == Extropia::Core::DataSource::READ_ONLY()) {
        @keys = @{$self->{'key_fields'}};
        if (!@keys) {
            @keys = $self->getDataSource()->getFieldNames();
        }
    }
    elsif ($strategy == Extropia::Core::DataSource::ALL_FIELDS() ||
          ($strategy == Extropia::Core::DataSource::KEY_AND_MODIFIED_FIELDS()
           && !defined $update_record )) {
        @keys = $self->getDataSource()->getFieldNames();
    }
    elsif ($strategy == Extropia::Core::DataSource::KEY_AND_MODIFIED_FIELDS()) {
        my %used = ();
        @used{@{$self->{'key_fields'}}} = ();
        @used{keys %$update_record} = ();
        @keys = keys %used;
    }
    else {
        die("Unknown UPDATE_STRATEGY specified; "
           ."use a constant from Extropia::Core::DataSource\n");
    }
    my $query = "";
    my $key;
    foreach $key (@keys) {
        $query .= " AND $key = '$rh_record->{$key}'";
    }
    return substr($query, 5);
}

sub sort {
    my $self = shift;
    my $order = shift;

    return 1 unless $order;

    my $ds = $self->getDataSource();

    # Create sort expression
    my (@field, $field_name, @invert, $type, $format);
    my $error = 0;
    my @sorter = ();
    my @dt = ();
    my @order_fields = split(/,/, $order);
    my $i;
    for ($i = 0; $i < @order_fields; ++$i) {
        if ( $order_fields[$i] =~ m/^\s*(\w+)(?:\s+(ASC|DESC))?/i 
          && defined($ds->getFieldIndex($1)) ) {
            $field_name = $1;
            $invert[$i] = defined $2 && uc($2) eq 'DESC';
            $field[$i]  = $ds->getFieldIndex($1);
            $sorter[$i] = $ds->getSort($field_name);
            $dt[$i]     = $ds->getDataType($field_name);
            if ($sorter[$i] && $dt[$i]) {
            } else {
                $self->addError(
                    -MESSAGE => "Cannot determine datatype or sort strategy"
                        . " for field '$field_name'"
                );
                $error = 1;
            }
        } else {
            $self->addError("Invalid order clause: '$1' not recognized "
                    . "as a field name");
            $error = 1;
        }
    }
	my $sort_sub = sub {
		foreach my $j (0 .. $i-1) {
			my $result;
			my $r = $sorter[$j]->compare(
				$dt[$j]->display2internal($a->[$field[$j]]),
				$dt[$j]->display2internal($b->[$field[$j]]),
			);
			$result = $invert[$j] ? -$r : $r;
			$result and return $result;
		}
		return 0;
	};
    return 0 if $error;

    # Retrieve all records and sort them
    $self->finishRetrieval();
    my @sorted = sort { &$sort_sub($a,$b) } @{$self->{'databuffer'}};
    $self->{'databuffer'} = \@sorted;
    $self->moveFirst();

    return 1;
}

sub getDataSource {
    my $self = shift;
    return $self->{'datasource'};
}

# DEPRECATED Method:
sub getTotalMatchingRecords {
    my $self = shift;
    carp "RecordSet::getTotalMatchingRecords() is deprecated;\n"
        ."use getTotalCount() instead";
    return $self->getTotalCount();
}

#
# Protected Methods
#

sub _retrieveNextRecord {
    my $self = shift;
    my $buffer = shift || $self->_bufferByDefault();

    return 0 if ( $self->isRetrievalFinished ); 
    
    my $ds = $self->{'datasource'};
    my $search = $self->{'search_expression'};
    # Skip over records retrieved previously
    my $ra_fields = 1;
    while ( $self->{'last_record_retrieved'} > 
            $self->{'total_matching_records'} ) {
        $ra_fields = $ds->_skipToNextRecord($search);
        last unless $ra_fields;
        ++$self->{'total_matching_records'};
    }

    # Retrieve next record, if available
    if ($ra_fields) {
        $ra_fields = $ds->_searchForNextRecord($search);
    }
    
    if ($ra_fields) {
        ++$self->{'total_matching_records'};

        if ($buffer) {
            push @{$self->{'databuffer'}}, $ra_fields;
        } else {
            $self->{'databuffer_start_offset'} += @{$self->{'databuffer'}};
            $self->{'databuffer'} = [ $ra_fields ];
        }

        if ($self->{'max_records_to_retrieve'} &&
                $self->{'total_matching_records'} ==
                $self->{'max_records_to_retrieve'} 
                + $self->{'last_record_retrieved'}) {
            $self->{'retrieval_finished'} = 1;
        }
    } else {
        $self->{'retrieval_finished'} = 1;
        return 0;
    }

    return $ra_fields;
}

sub _performInitialOrdering {
    my $self = shift;
    if ($self->{'order'}) {
        my $hold_last = $self->{'last_record_retrieved'};
        my $hold_max  = $self->{'max_records_to_retrieve'};
        $self->{'last_record_retrieved'} = 0;
        $self->{'max_records_to_retrieve'} = 0;
        $self->sort($self->{'order'});
        if ($hold_last) {
            splice(@{$self->{'databuffer'}}, 0, $hold_last);
            $self->{'last_record_retrieved'} = $hold_last;
            $self->{'databuffer_start_offset'} = $hold_last;
        }
        if ($hold_max) {
            splice(@{$self->{'databuffer'}}, $hold_max, 
                $self->getTotalCount());
            $self->{'max_records_to_retrieve'} = $hold_max;
        }
    }
}

1;
__END__

