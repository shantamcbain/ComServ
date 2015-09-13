# $Id: FileCache.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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


package Extropia::Core::DataSource::RecordSet::FileCache;

use strict;
use Extropia::Core::Lock;
use vars qw($VERSION @ISA);

$VERSION = do { my @r = q$Revision: 1.1.1.1 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw( Extropia::Core::DataSource::RecordSet );

sub new {
    # Construct Base RecordSet
    my $class = shift;
    my $self = $class->SUPER::new(@_);

    @_ = Extropia::Core::Base::_rearrange([-CACHE_FILE],[-CACHE_FILE],@_);
    $self->{'cache_file'} = shift;

    my $ds = $self->{'datasource'};
    my $cache = $self->_getCacheFile();
    my @fieldnames = $ds->getFieldNames();
    my %fieldtypes = $ds->getFieldTypes();
    $self->{'cache_datasource'} = Extropia::Core::DataSource->create(
                -TYPE => 'File',
                -FILE => $cache,
                -FIELD_DELIMITER => '|',
                -FIELD_NAMES => \@fieldnames,
                -FIELD_TYPES => \%fieldtypes,
                -CREATE_FILE_IF_NONE_EXISTS => 1
    );
    my $cachelock = Extropia::Core::Lock->create(
                -TYPE => 'File', 
                -FILE => $self->_getLockFile()
    );
    if (!$self->_doesCacheMatch()) {
        # Consider fork-ing to do this?
        $cachelock->obtainLock();
        $self->_createNewCache();
        $cachelock->releaseLock();
    }
    return $self;
}

sub _getCacheFile {
    my $self = shift;
    return $self->{'cache_file'};
}

sub _getLockFile {
    my $self = shift;
    return $self->_getCacheFile() . ".lck";
}

sub _getExprFile {
    my $self = shift;
    return $self->_getCacheFile() . ".exp";
}

sub _doesCacheMatch {
    my $self = shift;
    my $exprfile = $self->_getExprFile();
    return 0 unless -f $exprfile;
    my $search = $self->_search2string($self->{'search_expression'});
    my $expr;
    {
        local *EXPRFILE;
        local($/) = undef;
        open(EXPRFILE, $exprfile) or die "Can't read $exprfile, $!\n";
        $expr = <EXPRFILE>;
        close EXPRFILE;
    }
    return $search eq $expr;
}

sub _search2string {
    my ($self, $expr) = @_;
    if (ref $expr eq "ARRAY") {
        my $string = '';
        my $part;
        foreach $part (@$expr) {
            $string .= $self->_search2string($part);
        }
        return $string;
    } elsif (!ref $expr) {
        return $expr;
    } else {
        die "Internal error: search expression is not array ref or string\n";
    }
}

sub _createNewCache {
    my $self = shift;

    my $file = $self->_getCacheFile();
    local(*CACHE, *EXPRFILE);
    open(CACHE, ">$file") || return 0;
    close(CACHE);

    # Cache has already been locked, so turn off locking to avoid collision
    # with self:
    my $cache = $self->{'cache_datasource'};
    $cache->_setLockParams();

    # Retrieve all records from DataSource and insert into Cache
    my $rs = $self->{'datasource'}->search(
        -SEARCH => $self->{'search_expression'},
        -RECORDSET_PARAMS => [-TYPE => 'ForwardOnly']
    );
    $rs->moveFirst();
    while (!$rs->endOfRecords()) {
        $cache->add(-ADD => $rs->getRecordAsHash(), -DEFER => 1);
        $rs->moveNext();
    }
    return $cache->doUpdate();
}

sub _retrieveNextRecord {
    my $self = shift;
    my $buffer = shift || 0;

    return 0 if ( $self->isRetrievalFinished ); 
    
    my $ds = $self->{"cache_datasource"};
    my $search = $self->{'search_expression'};
    # Skip over records retrieved previously
    my $ra_fields = 1;
    while ( $self->{"last_record_retrieved"} > 
            $self->{"total_matching_records"} ) {
        $ra_fields = $ds->_searchForNextRecord($search);
        last unless $ra_fields;
        ++$self->{"total_matching_records"};
    }

    # Retrieve next record, if available
    if ($ra_fields) {
        $ra_fields = $ds->_searchForNextRecord($search);
    }
    
    if ($ra_fields) {
        ++$self->{"total_matching_records"};

        if ($buffer) {
            push @{$self->{"databuffer"}}, $ra_fields;
        } else {
            $self->{"databuffer_start_offset"} += @{$self->{"databuffer"}};
            $self->{"databuffer"} = [ $ra_fields ];
        }

        if ($self->{"max_records_to_retrieve"} &&
                $self->{"total_matching_records"} ==
                $self->{"max_records_to_retrieve"} 
                + $self->{"last_record_retrieved"}) {
            $self->{"retrieval_finished"} = 1;
        }
    } else {
        $self->{"retrieval_finished"} = 1;
        $self->{"total_retrieval_finished"} = 1;
        return 0;
    }

    return $ra_fields;
}

1;
