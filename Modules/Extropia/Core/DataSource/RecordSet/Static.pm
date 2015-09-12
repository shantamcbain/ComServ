# $Id: Static.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::DataSource::RecordSet::Static;

use strict;
use Extropia::Core::DataSource::RecordSet;
use Extropia::Core::Base qw(_rearrange);
use vars qw($VERSION @ISA);

$VERSION = do { my @r = q$Revision: 1.1.1.1 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw( Extropia::Core::DataSource::RecordSet );

# Note the update_strategy is set to -1, corresponding to the named
# constant Extropia::Core::DataSource::READ_ONLY.  Generally, it is best to use
# the named constant, but here we are trying to avoid any reliance on
# Extropia::Core::DataSource.  This was achieved through creating a "Static"
# DataSource, which implements minimal stubs for the required methods,
# below.

sub new {
    my $class = shift;
    my $self = bless {
        'databuffer_start_offset' => 0
      , 'retrieval_finished' => 1
      , 'total_retrieval_finished' => 1
      , 'index_to_databuffer' => 0
      , 'update_strategy' => -1
    }, ref $class || $class;
    @_ = _rearrange(
        [-DATA_BUFFER,-FIELD_NAMES,-DATA_TYPES,-FIELD_SORTS,-ORDER],
        [-DATA_BUFFER,-FIELD_NAMES],@_);
    $self->{'databuffer'} = shift;
    $self->{'index_to_databuffer'} = @{$self->{'databuffer'}} ||
        Extropia::Core::DataSource::RecordSet::NO_RECORD;
    my $fields = shift;
    my $types  = shift || {};
    my $sorts  = shift || {};
    my $order  = shift || '';
    $self->{'datasource'} = Extropia::Core::DataSource::Driver::Static->new(
        -FIELD_NAMES => $fields
      , -DATA_TYPES  => $types
      , -FIELD_SORTS => $sorts
    );

    $self->_performInitialOrdering();
    return $self;
}

sub _retrieveNextRecord {
    return 0;
}


package Extropia::Core::DataSource::Driver::Static;

sub new {
    my $package = shift;
    my $self = bless {}, ref $package || $package;
    @_ = Extropia::Core::Base::_rearrange(
        [-FIELD_NAMES,-DATA_TYPES,-FIELD_SORTS],[-FIELD_NAMES],@_);
    $self->{'_field_names'} = shift;
    $self->{'_data_types'}  = shift || {};
    $self->{'_field_sorts'} = shift || {};
    return $self;
}

sub _searchForNextRecord {
    return 0;
}

sub getDataType {
    my ($self, $field) = @_;
    return $self->{'_data_types'}->{$field};
}

sub getSort {
    my ($self, $field) = @_;
    return $self->{'_field_sort'}->{$field};
}

sub getFieldNames {
    my $self = shift;
    return @{$self->{'_field_names'}};
}

sub getFieldIndex {
    my ($self, $field) = @_;
    if (!exists $self->{'_field_index'}) {
        my %index;
        my @fields = $self->getFieldNames();
        @index{@fields} = (0..$#fields);
        $self->{'_field_index'} = \%index;
    }
    return $self->{'_field_index'}->{$field};
}

1;
