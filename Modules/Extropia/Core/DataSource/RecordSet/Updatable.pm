# $Id: Updatable.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::DataSource::RecordSet::Updatable;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataSource::RecordSet;
use vars qw(@ISA);

@ISA = qw( Extropia::Core::DataSource::RecordSet );

sub new {
    # Construct Base RecordSet
    my $class = shift;
    my $self = $class->SUPER::new(@_);

    $self->{'__updatable_updates'} = [];
    return $self;
}

sub add {
    my $self = shift;
    my ($add,$rs_only) = _rearrange([
            -ADD,
            -CHANGE_RECORDSET_ONLY,
                ],[
            -ADD,
                ],@_);
    # Test parameter to make sure it is valid
    if (ref $add ne 'HASH') {
        croak "Record to add must be a HASH reference";
    }
    my $success = 1;
    my $ds = $self->getDataSource();
    if (!$rs_only) {
        if ($self->{'update_strategy'} == $Extropia::Core::DataSource::READ_ONLY) {
            $self->addError(
                -MESSAGE => 'Cannot update a Read-only DataSource'
            );
            return 0;
        }
        # Schedule addition in DataSource queue
        $success = $ds->add(-ADD => $add, -DEFER => 1);
        if (!$success) {
            $self->_migrateErrors($ds, "Originated From DataSource");
        }
    }
    if ($success) {
        # Remember how to undo the change
        my $buffer = $self->{'databuffer'};
        my $log = $self->{'__updatable_updates'};
        push @$log, ['ADD', scalar(@$buffer)];

        # Make change to current RecordSet
        my @record = map { $add->{$_} } $ds->getFieldNames();
        push @$buffer, \@record;
    }
    return $success;
}

sub update {
    my $self = shift;
    my ($update,$rs_only) = _rearrange([
            -UPDATE,
            -CHANGE_RECORDSET_ONLY,
                ],[
            -UPDATE
                ],@_);
    # Test parameter to make sure it is valid
    if (ref $update ne 'HASH') {
        croak "Update parameter must be a HASH reference";
    }
    my $success = 1;
    my $ds = $self->getDataSource();
    if (!$rs_only) {
        if ($self->{'update_strategy'} == $Extropia::Core::DataSource::READ_ONLY) {
            $self->addError(
                -MESSAGE => 'Cannot update a Read-only DataSource'
            );
            return 0;
        }
        # Could check whether all fields are known fields?
        # Schedule update in DataSource queue
        $success = $ds->update(
            -QUERY => $self->getRecordIDQuery($update), 
            -UPDATE => $update,
            -DEFER => 1
        );
        if (!$success) {
            $self->_migrateErrors($ds, "Originated From DataSource");
        }
    }
    if ($success) {
        # Remember how to undo the change
        my %old_values = ();
        my $field;
        foreach $field (keys %$update) {
            $old_values{$field} = $self->getField($field);
        }
        my $log = $self->{'__updatable_updates'};
        push @$log, ['UPDATE', $self->getRecordNumber(), \%old_values];

        # Make change to current RecordSet
        my $record = $self->getRecord();
        foreach $field (keys %$update) {
            $record->[$ds->getFieldIndex($field)] = $update->{$field};
        }
    }
    return $success;
}

sub delete {
    my $self = shift;
    my ($rs_only) = _rearrange([-CHANGE_RECORDSET_ONLY],[],@_);
    my $success = 1;
    if (!$rs_only) {
        if ($self->{'update_strategy'} == $Extropia::Core::DataSource::READ_ONLY) {
            $self->addError(
                -MESSAGE => 'Cannot update a Read-only DataSource'
            );
            return 0;
        }
        # Schedule delete in DataSource queue
        my $ds = $self->getDataSource();
        $success = $ds->delete(
                -DELETE => $self->getRecordIDQuery(),
                -DEFER  => 1,
        );
        if (!$success) {
            $self->_migrateErrors($ds, "Originated From DataSource");
        }
    }
    if ($success) {
        # Make change to current RecordSet
        my $buffer = $self->{'databuffer'};
        my $recno = $self->getRecordNumber();
        my $deleted = splice(@$buffer, $recno, 1);
        # Remember how to undo the change
        my $log = $self->{'__updatable_updates'};
        push @$log, ['DELETE', $recno, $deleted];
    }
    return $success;
}

sub doUpdate {
    my $self = shift;
    my ($rs_only) = _rearrange([-CHANGE_RECORDSET_ONLY],[],@_);
    my $success = 1;
    if (!$rs_only) {
        $success = $self->getDataSource()->doUpdate();
    }
    if ($success) {
        $self->{'__updatable_updates'} = [];
    }
    return $success;
}

sub clearUpdate {
    my $self = shift;
    my ($rs_only) = _rearrange([-CHANGE_RECORDSET_ONLY],[],@_);
    # Undo each change
    my $change;
    foreach $change (reverse @{$self->{'__updatable_updates'}}) {
        my $type = $change->[0];
        my $recno = $change->[1];
        my $buffer = $self->{'databuffer'};
        if ($type eq 'ADD') {
            splice(@$buffer, $recno, 1);
        }
        elsif ($type eq 'UPDATE') {
            my $undo = $change->[2];
            my $record = $buffer->[$recno];
            my $ds = $self->getDataSource();
            my $field;
            foreach $field (keys %$undo) {
                $record->[$ds->getFieldIndex($field)] = $undo->{$field};
            }
        }
        elsif ($type eq 'DELETE') {
            splice(@$buffer, $recno, 0, $change->[2]);
        }
        else {
            die("Invalid update type $type");
        }
    }
    # Then clear both lists
    $self->{'__updatable_updates'} = [];
    if (!$rs_only) {
        $self->getDataSource()->clearUpdate();
    }
}

sub _bufferByDefault {
    return 1;
}

sub _migrateErrors {
    my ($self, $obj, $preface) = @_;
    if ($preface) {
        # Add a final colon and space, if there isn't one already
        $preface =~ s/:?\s*$/: /;
    } else {
        $preface = '';
    }
    my $errors = $obj->getErrors();
    my $error;
    foreach $error (@$errors) {
        my $msg = $preface . $error->getMessage();
        $error->setMessage($msg);
        $self->addError($error);
    }
}

1;
