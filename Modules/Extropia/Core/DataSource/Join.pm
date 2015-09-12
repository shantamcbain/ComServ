# $Id: Join.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::DataSource::Join;
# Read only implemented at the moment

use Carp;
use strict;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataSource;
use vars qw(@ISA $VERSION);

$VERSION = do { my @r = q$Revision: 1.1.1.1 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);

sub new {
    my $package = shift;
    my $self = $package->SUPER::new( @_ );
    @_ = _rearrange([-DATASOURCE1, 
                     -DATASOURCE2, 
                     -FOREIGN_KEY 
                    ],
                    [-DATASOURCE1, 
                     -DATASOURCE2, 
                     -FOREIGN_KEY
                    ],
                    @_);

    #required parameters
    my $dsh1 = shift;
    my $dsh2 = shift;
    my $foreignKey = shift;

    #calculate field names for joined table
    #and store the numeric positions of the fields of ds2 to use
    my @fields= $dsh1->getFieldNames();
    my %fieldTypes= $dsh1->getFieldTypes();
    my @allDs2Fields= $dsh2->getFieldNames();
    my %allDs2FieldTypes= $dsh2->getFieldTypes();
    my @dsh2FieldsToUse;
    my $i;
    for ($i = 0; $i < @allDs2Fields; ++$i)
    { $_ = $allDs2Fields[$i];
      if ( !exists($foreignKey->{$_}) )
      { push(@fields, $_);
        $fieldTypes{$_}= $allDs2FieldTypes{$_};
        push @dsh2FieldsToUse, $i;
      }
    }
    # Important to use these methods, because they also generate indexes to
    # individual fields and require the appropriate modules to process
    # dates/times if needed
    $self->_setFieldNames(\@fields);
    $self->_setFieldTypes(\%fieldTypes);
    
    #optimisation - store foreign keys as field position numbers
    #-means that each _evaluateForeignKey won't have to do this
    my $foreignKeyNumeric= {};
    my ($dsh1KeyElement, 
        $dsh2KeyElement,
        $dsh1KeyElementNumeric,
        $dsh2KeyElementNumeric);
        
    foreach $dsh2KeyElement (keys %$foreignKey)
    { $dsh1KeyElement= $foreignKey->{$dsh2KeyElement};
      #find the numeric position of the fields
      $dsh1KeyElementNumeric = $dsh1->getFieldIndex($dsh1KeyElement);
      $dsh2KeyElementNumeric = $dsh2->getFieldIndex($dsh2KeyElement);
      #add the numeric version to the hash
      $foreignKeyNumeric->{$dsh2KeyElementNumeric}= $dsh1KeyElementNumeric;
    }

    # SETUP DATA STRUCTURE
    $self->{'dsh1'} = $dsh1;
    $self->{'dsh2'} = $dsh2;
    $self->{'foreignKey'} = $foreignKey;
    $self->{'foreignKeyNumeric'} = $foreignKeyNumeric;
    $self->{'dsh1RecordSet'} = '';
    $self->{'dsh2RecordSet'} = '';
    $self->{'dsh1RecordSetPointer'} = '';
    $self->{'dsh1RecordSetPointer'} = '';
    $self->{'join_complete'} = '0';
    $self->{'dsh2FieldsToUse'} = \@dsh2FieldsToUse;

    bless $self, $package;
    
    return $self;
}

##
## Methods
##

sub _evaluateForeignKey { 
  my $self= shift;
  my $comparisonOperator= shift;
  my $ds1Row= shift;
  my $ds2Row= shift;
  #only equality implemented
  Carp::croak "Can't Join with $comparisonOperator\n" if ($comparisonOperator ne "=");
  my $OK= 1;
  my ($ds1KeyElementNumeric,
      $ds2KeyElementNumeric);
  foreach $ds2KeyElementNumeric (keys %{$self->{'foreignKeyNumeric'}})
  { $ds1KeyElementNumeric= $self->{'foreignKeyNumeric'}->{$ds2KeyElementNumeric};
    if ($ds1Row->[$ds1KeyElementNumeric] ne $ds2Row->[$ds2KeyElementNumeric])
    { $OK= 0;
    }
  }
  return $OK;
}

sub _searchForNextRecord {
  my $self= shift;
  my $ra_search = shift;
  my (@newRecord,
      $ds1Row,
      $ds2Row);
  my %record;
  my $gotRecord= 0;
  #check if not already finished
  if ($self->{'join_complete'})
  { return undef;
  }

  #loop to find the next record. We are already pointing at the first
  #record that is as yet unchecked
  do
  { undef @newRecord;
    $ds1Row= $self->{'dsh1RecordSet'}->getRecord();
    $ds2Row= $self->{'dsh2RecordSet'}->getRecord();

    #check to see if the foreignKey matches from ds2 => ds1
    if ($self->_evaluateForeignKey("=", $ds1Row, $ds2Row))
    { #create the new record
      @newRecord= @$ds1Row;
      foreach (@{$self->{'dsh2FieldsToUse'}})
      { push (@newRecord, $ds2Row->[$_]);
      }
      
      #now we have created the new row, check against search parameter to see
      #if it fits the bill - put into a field=>value and pass to _matches
      my $i = 0;
      my @fields = $self->getFieldNames();
      for ($i = 0; $i < @newRecord; ++$i)
      { $record{$fields[$i]} = $newRecord[$i];
      }
      if (eval{ $self->_matches($ra_search, \%record) })
      { $gotRecord = 1;
      }
      elsif ($@)
      { $self->addError($@);
      }
    }

    #increment record pointers
    $self->{'dsh2RecordSet'}->moveNext();
    if ($self->{'dsh2RecordSet'}->endOfRecords()) { 
        $self->{'dsh1RecordSet'}->moveNext();
        $self->{'dsh2RecordSet'}->moveFirst();
    }
    if ($self->{'dsh1RecordSet'}->endOfRecords()) { 
        $self->{'join_complete'}= 1;
    }
  } while (!$gotRecord && !$self->{'join_complete'});

  if ($gotRecord)
  { return \@newRecord;
  }
  else
  { return undef;
  }
}


sub _realSearch {
    my $self = shift;
    my $ra_search = shift;
    my $last_record_retrieved = shift;
    my $max_records_to_retrieve = shift;
    my $order = shift;
    my $rs_data = shift;

    #now would be a good time to get the record sets of the
    #tables that we are joining
    $self->{'dsh1RecordSet'}= $self->{'dsh1'}->search("");
    $self->{'dsh2RecordSet'}= $self->{'dsh2'}->search("");

    #now buffer all results and point to the first one
    $self->{'dsh1RecordSet'}->getAllRecords();
    $self->{'dsh2RecordSet'}->getAllRecords();
    $self->{'dsh1RecordSet'}->moveFirst();
    $self->{'dsh2RecordSet'}->moveFirst();
    
    my $record_set = Extropia::Core::DataSource::RecordSet->create( @$rs_data,
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
