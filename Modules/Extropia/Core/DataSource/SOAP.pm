# $Id: SOAP.pm,v 1.2 2001/03/28 03:30:05 stas Exp $
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

#
# This is datasource to a SOAP Server that interprets DataSource
# Requests...
#

package Extropia::Core::DataSource::SOAP;

use strict;
use vars qw($VERSION @ISA);

use Carp;
use Extropia::Core::Base qw(_rearrangeAsHash _assignDefaults _rearrange);
use Extropia::Core::DataSource;
use Extropia::Core::SOAPClient;

$VERSION = do { my @r = q$Revision: 1.2 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);

# Based on code from XML::Dumper

sub EscapeXMLChars {
    $_[0] =~ s/&/&amp;/g;
    $_[0] =~ s/</&lt;/g;
    $_[0] =~ s/>/&gt;/g;
    $_[0] =~ s/'/&apos;/g;
    $_[0] =~ s/"/&quot;/g;
    $_[0] =~ s/([\x80-\xFF])/&XmlUtf8Encode(ord($1))/ge;
    return($_[0]);
}

sub XmlUtf8Encode {
# borrowed from XML::DOM
    my $n = shift;
    if ($n < 0x80) {
    return chr ($n);
    } elsif ($n < 0x800) {
        return pack ("CC", (($n >> 6) | 0xc0), (($n & 0x3f) | 0x80));
    } elsif ($n < 0x10000) {
        return pack ("CCC", (($n >> 12) | 0xe0), ((($n >> 6) & 0x3f) | 0x80),
                     (($n & 0x3f) | 0x80));
    } elsif ($n < 0x110000) {
        return pack ("CCCC", (($n >> 18) | 0xf0), ((($n >> 12) & 0x3f) | 0x80),
                     ((($n >> 6) & 0x3f) | 0x80), (($n & 0x3f) | 0x80));
    }
    return $n;
}

sub UnescapeXMLChars {
    $_[0] =~ s/&amp;/&/g;
    $_[0] =~ s/&lt;/</g;
    $_[0] =~ s/&gt;/>/g;
    $_[0] =~ s/&apos;/'/g;
    $_[0] =~ s/&quot;/"/g;
#    $_[0] =~ s/([\x80-\xFF])/&XmlUtf8Encode(ord($1))/ge;
    return($_[0]);
}

# End of code based on XML::Dumper

sub new {
    my $package = shift;
    my $self = $package->SUPER::new(@_);
    my $params;
    ($params, @_) = _rearrangeAsHash(
        [-SOAP_URI, 
         -SOAP_URN,
         -SOAP_HOST,
         -SOAP_PORT, 
         -SOAP_TIMEOUT,
         -SOAP_LOG_FILE,
         -FIELD_TO_SOAP_XSITYPE_MAPPINGS
         ], 
        [-SOAP_URI, -SOAP_URN, -SOAP_HOST, -SOAP_PORT], @_);

    $self = _assignDefaults($self, $params);
    $self = _assignDefaults($self, {
                                -SOAP_TIMEOUT => 1000
                                }
                                );

    return $self;
}

sub doUpdate {
    my $self = shift;
    @_ = _rearrange([-RETURN_ORIGINAL],[],@_);
    my $return_orig = shift || 0;

    return undef unless $self->_canUpdate("AddError");

    my $pending_updates = $self->_getPendingUpdates();
    my $data_types = $self->_getAllDataTypes();
    my @fields     = $self->getFieldNames();

    my @original = ();
    my $errors = 0;
    my $completed = 0;
    my $affected = 0;

    my $soap = new Extropia::Core::SOAPClient(
            -SOAP_URI  => $self->{-SOAP_URI},
            -SOAP_URN  => $self->{-SOAP_URN},
            -SOAP_HOST => $self->{-SOAP_HOST},
            -SOAP_PORT => $self->{-SOAP_PORT}
            );

    # BEGIN LARGE EVAL BLOCK -----------------------------------------
eval {
    # According to the DBI standard, this line should not be necessary,
    # since transactions are automatically started when AutoCommit is not set.
    # However, this could be used to lock the table, in order to allow
    # manual rollback on databases that don't support this feature.
    # (note that begin_transaction is an experimental DBIx::SQL92 method)
    # $dbh->begin_transaction;

    my $xml = "";
    my $field;
    my $xsi_type;
    my $update;
    foreach $update (@$pending_updates) {
        my $type = $update->[0];
        if ($type eq "ADD") {

            $xml = "";
            foreach $field (keys %{$update->[1]}) {
                my $value = $update->[1]->{$field};
                $value = $data_types->{$field}->internal2storage($value);
                $xsi_type = $self->__getFieldToSOAPXSITypeMapping($field);
                if ($xsi_type =~ /xsd:string/i &&
                        defined($value)) {
                    $value = EscapeXMLChars($value);
                } 
                if (!defined($value) ||
                    ($xsi_type !~ /^xsd:string$/i && length($value) == 0)) {
                    $xml .= qq[<$field xsi:null="true"/>\n];
                } else {
                    $xml .= qq[<$field xsi:type="$xsi_type">$value</$field>\n];
                }
            }

            $xml = qq[<Values 
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xsi:type="SOAP-ENC:Struct">
$xml
</Values>
];
    
#print "XML: $xml\n";
    $self->_logSOAPRequest("Start Add:$xml");
            my $soap_results = $soap->sendSOAPRequest(
                                        -METHOD      => "add",
                                        -REQUEST_XML => $xml,
                                        -SEND_SOAP_FAULT => 0);
    $self->_logSOAPRequest("End Add:" . length($soap_results) . "\n");

            if (!defined($soap_results)) {
                $self->_setActiveQuery();
                die ("SOAP Add failed: " . 
                        $soap->getLastError()->getMessage());
#$self->addError(
#                   -CODE    => 300,
#                   -MESSAGE => "SOAP Add failed: " . 
#                       $soap->getLastError()->getMessage(),
#                   -SOURCE  => 'DataSource::SOAP',
#                   -CALLER  => (caller)[0]
#               );
            } else {
                $affected++;
            }

            my $add_result = $self->__decodeSOAPAddResult(
                        -SOAP_RESULT => $soap_results
                        );
            $self->_setLastAutoincrementID($add_result);
        }
        elsif ($type eq "UPDATE" || $type eq "DELETE") {
            my ($rh_col_names, $ra_records) = 
                $self->__performSOAPQuery($update->[1]);

            if (defined($ra_records)) {
                my ($rec, $disp);
                foreach $rec (@$ra_records) {
                    $disp = $self->_recordStorage2Display($rec)
                        || die "Could not read all values in original "
                            ."record.  See previous error message.\n";
                    push @original, $disp;
                }
            }

            my $rows = 0;
            if ($type eq "UPDATE") {
                $rows = $self->__performSOAPUpdate(
                        $update->[1],$update->[2]);
            } else {
                $rows = $self->__performSOAPDelete($update->[1]);
            }
            if (!defined($rows)) {
                die "Update/Delete Failed: " . 
                    $self->getLastError()->getMessage();
            }
            if ($rows >= 0 && $return_orig && $rows != @$ra_records) {
                die "Consistency error: SOAP database changed between "
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

};
    # END LARGE EVAL BLOCK ------------------------------------------
    if ($@) {
# Place marker if statement...
        if (1) {
            $self->addError(
                -CODE    => 251,
                -MESSAGE => "doUpdate failed: Changes CANNOT BE rolled back\n"
                    . "$completed completed actions removed from update queue\n"
                    . $@,
                -SOURCE  => 'DataSource::SOAP'
            );
            splice(@$pending_updates, 0, $completed);
        }
        return undef;
    }

    return $self->_successfulUpdate($return_orig, \@original, $affected);
}

# count is like search except that it returns the number of records...

sub count {
    my $self = shift;
    @_ = _rearrange([
            -SEARCH,
                    ],
                     [],@_);
    my $search = shift || "";

    $search =~ s/^\s+//g;
    $search =~ s/\s+$//g;

    my $expr_tree;
    $expr_tree = $self->_buildExprTree($search);
    $self->_setActiveQuery($expr_tree);
    if (defined $expr_tree) {
        return $self->__performSOAPCount($expr_tree);
    } else {
        return 0;
    }


} # end of count

sub _realSearch {
    my $self = shift;
    my $ra_search               = shift;
    my $last_record_retrieved   = shift;
    my $max_records_to_retrieve = shift;
    my $order                   = shift;
    my $rs_data                 = shift;

    my ($rh_col_names, $ra_records) = 
        $self->__performSOAPQuery($ra_search,
                $last_record_retrieved,
                $max_records_to_retrieve,
                $order);
   
    if (!defined($rh_col_names)) {
        return 0;
    }
    
    $self->{_current_results_ra_records}   = $ra_records;
    $self->{_current_results_rh_col_names} = $rh_col_names;
    $self->{_current_results_index}        = 0;
   
    $self->_setActiveQuery($ra_search);

    my $record_set = Extropia::Core::DataSource::RecordSet->create( 
          @$rs_data,
          -DATASOURCE => $self,
          -KEY_FIELDS => $self->_getKeyFields(),
          -UPDATE_STRATEGY => $self->getUpdateStrategy(),
          -REAL_SEARCH_QUERY => $ra_search,
          -LAST_RECORD_RETRIEVED => $last_record_retrieved,
          -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve
    );

    return $record_set;
}

sub __performSOAPQuery {
    my $self = shift;
    my $ra_search               = shift;
    my $last_record_retrieved   = shift;
    my $max_records_to_retrieve = shift;
    my $order                   = shift;

    my $xml;
    if ($ra_search) {
        $xml = $self->_tree2XML($ra_search);
    } else {
        $xml = "";
    }

#    if ($max_records_to_retrieve) {
#        $xml .= "  <Limit>$max_records_to_retrieve</Limit>\n";
#    }
    if ($last_record_retrieved) {
        my $offset = $last_record_retrieved;
#        $xml .= "  <Offset>$offset</Offset>\n";
    }
    if ($order) {
#$xml .= "  <Order>$order</Order>\n";
    # Create sort expression
        my ($field, $field_name, $descend, $type, $format);
        my $sort_expr = '';
        my @order_fields = split(/,/, $order);
        my $i; 
        for ($i = 0; $i < @order_fields; ++$i) {
            $descend = '';
            if ( $order_fields[$i] =~ m/^\s*(\w+)(?:\s+(ASC|DESC))?/i
                && defined($self->getFieldIndex($1)) ) {
                $field_name = $1;
                $descend    = '-' if defined $2 && uc($2) eq 'DESC';
                my $direction;
                if ($descend eq "-") {
                    $direction = "DESCEND";
                } else {
                    $direction = "ASCEND"; 
                }
                $sort_expr .= qq[  <SortBy>\n];
                $sort_expr .= qq[    <Field>$field_name</Field>\n];
                $sort_expr .= qq[    <Direction>$direction</Direction>\n];
                $sort_expr .= qq[  </SortBy>\n];
            } else {
                $self->addError("Invalid order clause: '$1' not recognized "
                        . "as a field name");
            }
        }
        $xml .= "  <Order>\n$sort_expr</Order>\n";

# END OF SORT>...
    }
    $xml = qq[<Query xsi:type="m:Query" >
$xml
</Query>
];
    
    my $soap = new Extropia::Core::SOAPClient(
            -SOAP_URI  => $self->{-SOAP_URI},
            -SOAP_URN  => $self->{-SOAP_URN},
            -SOAP_HOST => $self->{-SOAP_HOST},
            -SOAP_PORT => $self->{-SOAP_PORT}
            );

    
    $self->_logSOAPRequest("Start Search:$xml");
    my $soap_results = $soap->sendSOAPRequest(
                                        -METHOD      => "search",
                                        -REQUEST_XML => $xml);
    $self->_logSOAPRequest("End Search:" . length($soap_results) . "\n");

    if (!defined($soap_results)) {
        $self->_setActiveQuery();
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "SOAP Query failed: " . 
                $soap->getLastError()->getMessage(),
            -SOURCE  => 'DataSource::SOAP',
            -CALLER  => (caller)[0]
        );
        return undef;
    }
    return $self->__decodeSOAPSearchResult($soap_results);

} # end of __performSOAPQuery

sub _logSOAPRequest {
    my $self = shift;
    my $message = shift;

    my $log_file = $self->{-SOAP_LOG_FILE};
    if ($log_file) {
        open(LOGFILE, ">>$log_file") ||
           die("Could not open $log_file for writing: $!\n");
        print LOGFILE "================\n";
        print LOGFILE "$message\n";
        print LOGFILE "================\n";
        close (LOGFILE);
    }

} # end of _logSOAPRequest

sub __performSOAPCount {
    my $self = shift;

    my $ra_search = shift;

    my $xml;
    if ($ra_search) {
        $xml = $self->_tree2XML($ra_search);
    } else {
        $xml = "";
    }

    $xml =~ s/(Criterion)/$1 xsi:type="m:Criterion"/i;

#    $xml = qq[<Query xsi:type="m:Query" >
#$xml
#</Query>
#];
    
    my $soap = new Extropia::Core::SOAPClient(
            -SOAP_URI  => $self->{-SOAP_URI},
            -SOAP_URN  => $self->{-SOAP_URN},
            -SOAP_HOST => $self->{-SOAP_HOST},
            -SOAP_PORT => $self->{-SOAP_PORT}
            );

    $self->_logSOAPRequest("Start Count:$xml");
#die($xml);
    my $soap_results = $soap->sendSOAPRequest(
                                        -METHOD      => "count",
                                        -REQUEST_XML => $xml);
#die($soap_results);
    $self->_logSOAPRequest("End Count:" . length($soap_results) . "\n");

    if (!defined($soap_results)) {
        $self->_setActiveQuery();
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "SOAP Count failed: " . 
                $soap->getLastError()->getMessage(),
            -SOURCE  => 'DataSource::SOAP',
            -CALLER  => (caller)[0]
        );
        return undef;
    }
    return $self->__decodeSOAPDeleteResult($soap_results);

} # end of __performSOAPCount

sub __performSOAPDelete {
    my $self = shift;

    my $ra_search = shift;

    my $xml;
    if ($ra_search) {
        $xml = $self->_tree2XML($ra_search);
    } else {
        $xml = "";
    }

    $xml =~ s/(Criterion)/$1 xsi:type="m:Criterion"/i;

#    $xml = qq[<Query xsi:type="m:Query" >
#$xml
#</Query>
#];
    
    my $soap = new Extropia::Core::SOAPClient(
            -SOAP_URI  => $self->{-SOAP_URI},
            -SOAP_URN  => $self->{-SOAP_URN},
            -SOAP_HOST => $self->{-SOAP_HOST},
            -SOAP_PORT => $self->{-SOAP_PORT}
            );

    $self->_logSOAPRequest("Start Delete:$xml");
    my $soap_results = $soap->sendSOAPRequest(
                                        -METHOD      => "delete",
                                        -REQUEST_XML => $xml);
    $self->_logSOAPRequest("End Delete:" . length($soap_results) . "\n");

    if (!defined($soap_results)) {
        $self->_setActiveQuery();
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "SOAP Delete failed: " . 
                $soap->getLastError()->getMessage(),
            -SOURCE  => 'DataSource::SOAP',
            -CALLER  => (caller)[0]
        );
        return undef;
    }
    return $self->__decodeSOAPDeleteResult($soap_results);

} # end of __performSOAPDelete

sub __performSOAPUpdate {
    my $self = shift;

    my $ra_search = shift;
    my $rh_update = shift;

    my $data_types = $self->_getAllDataTypes();
    
    my $xml = "";
    my $field;
    my $xsi_type;
    foreach $field (keys %$rh_update) {
        my $value = $rh_update->{$field};
# Handle null updates
        $xsi_type = $self->__getFieldToSOAPXSITypeMapping($field);
        if (!defined($value) ||
            ($xsi_type !~ /^xsd:string$/i && length($value) == 0)) {
            $xml .= qq[<$field xsi:null="true"/>\n];
        } else {
            confess("Field Not Defined.") if (!$field);
            $value = $data_types->{$field}->display2storage($value);
            if ($xsi_type =~ /xsd:string/i) {
                $value = EscapeXMLChars($value);
            } 
            $xml .= qq[<$field xsi:type="$xsi_type">$value</$field>\n];
        }
    }

    $xml = qq[<Values 
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xsi:type="SOAP-ENC:Struct">
$xml
</Values>
];

    if ($ra_search) {
        $xml .= $self->_tree2XML($ra_search);
    } else {
        $xml .= "";
    }

    $xml =~ s/(Criterion)/$1 xsi:type="m:Criterion"/i;
#    $xml = qq[<Query xsi:type="m:Query" >
#$xml
#</Query>
#];
    
    my $soap = new Extropia::Core::SOAPClient(
            -SOAP_URI  => $self->{-SOAP_URI},
            -SOAP_URN  => $self->{-SOAP_URN},
            -SOAP_HOST => $self->{-SOAP_HOST},
            -SOAP_PORT => $self->{-SOAP_PORT}
            );

    $self->_logSOAPRequest("Start Update:$xml");
    my $soap_results = $soap->sendSOAPRequest(
                                        -METHOD      => "update",
                                        -REQUEST_XML => $xml);
    $self->_logSOAPRequest("End Update:" . length($soap_results) . "\n");

    if (!defined($soap_results)) {
        $self->_setActiveQuery();
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "SOAP Update failed: " . 
                $soap->getLastError()->getMessage() || "No Message Defined",
            -SOURCE  => 'DataSource::SOAP',
            -CALLER  => (caller)[0]
        );
        return undef;
    }
    return $self->__decodeSOAPUpdateResult($soap_results);

} # end of __performSOAPUpdate

#
# __decodeSOAPAddResult decodes the add result...
#

sub __decodeSOAPAddResult {
    my $self = shift;

    @_ = _rearrange([-SOAP_RESULT],[-SOAP_RESULT],@_);

    my $result = shift;

    my $column_names;
    if ($result =~ /\<\s*return[^>]*\>(.*)\<\s*\/return\s*\>/is) {
        return $1;
    }
    die("Return value could not be parsed out of $result");

} # end of __decodeSOAPAddResult

#
# __decodeSOAPUpdateResult decodes the update result...
#

sub __decodeSOAPUpdateResult {
    my $self = shift;

    @_ = _rearrange([-SOAP_RESULT],[-SOAP_RESULT],@_);

    my $result = shift;

    my $column_names;
    if ($result =~ /\<\s*return[^>]*\>(.*)\<\s*\/return\s*\>/is) {
        return $1;
    }
    die("Return value could not be parsed out of $result");

} # end of __decodeSOAPUpdateResult

#
# __decodeSOAPDeleteResult decodes the delete result...
#

sub __decodeSOAPDeleteResult {
    my $self = shift;
    @_ = _rearrange([-SOAP_RESULT],[-SOAP_RESULT],@_);

    my $result = shift;

#print "$result\n";
    my $column_names;
    if ($result =~ /\<\s*return[^>]*\>(.*)\<\s*\/return\s*\>/is) {
        return $1;
    }
    die("Return value could not be parsed out of $result");

} # end of __decodeSOAPDeleteResult

#
# __decodeSOAPSearchResult decodes the search result...
#

sub __decodeSOAPSearchResult {
    my $self = shift;
    @_ = _rearrange([-SOAP_RESULT],[-SOAP_RESULT],@_);

    my $result = shift;

#print "$result\n";
    my $column_names;
    if ($result =~ /\<\s*columnnames\s*\>(.*)\<\s*\/columnnames\s*\>/is) {
        $column_names = $1; 
    } else {
        die("Column names could not be parsed out of $result");
    }

    my $index = 0;
    my %col_names = map { $_ => $index++ }
        @{$self->__decodeArrayOfTags($column_names, "name")};
# use Data::Dumper;
#   print Data::Dumper->Dump([\%col_names]);
    
    my $ra_rows = $self->__decodeArrayOfTags($result, "row");

    my @records = ();
    my $row;
    foreach $row (@$ra_rows) {
        my $ra_col_values = $self->__decodeArrayOfTags($row, "colvalue");
        my @real_row = ();
        my $field;
        foreach $field ($self->getFieldNames()) {
            my $field_value = 
                $ra_col_values->[$col_names{$field}];
            push(@real_row,$field_value);
        }
        push(@records, \@real_row);
    }

    return (\%col_names, \@records);

} # end of __decodeSOAPSearchResult

sub __decodeArrayOfTags {
    my $self = shift;
    my $data = shift;
    my $tag  = shift;

    my @fields = ();

# Normalize single ended tags...
    $data =~ s/<\s*($tag)([^>]*)\/>/<$1$2><\/$1>/gis;

# Now process...
    while ($data =~ /<\s*$tag([^>]*)>(.*?)<\s*\/$tag\s*>/gis) {
        my $attributes = $1;
        my $value      = $2;
        if ($attributes =~ /xsi:null\s*=\s*"true"/i) {
            push(@fields,undef);
        } else {
            if ($attributes =~ /xsi:type\s*=\s*"xsd:string"/i) {
                $value = UnescapeXMLChars($value);
            }
            push(@fields, $value);
        }
    }

    return \@fields;

} # end of __decodeArrayOfTags

sub _searchForNextRecord {
    my $self = shift;

#$self->{_current_results_ra_records}   = $ra_records;
#   $self->{_current_results_ra_col_names} = $ra_col_names;
#   $self->{_current_results_index}        = 0;

    my $index      = $self->{_current_results_index};
    my $rh_cols    = $self->{_current_results_rh_col_names};
    my $ra_records = $self->{_current_results_ra_records};

    my $record = $ra_records->[$index];
    my $ra_row = [];
    if (!defined($record)) {
        return undef;
    }

    $self->{_current_results_index}++;
    if ($record) {
        $record = $self->_recordStorage2Display($record);
    }
    return $record;
}

sub disconnect {
    my $self = shift;

}

##
## Protected Methods
##

#### Protected method: _tree2XML
# Converts an Extropia::Core::DataSource expression tree into a SOAP XML expression,
#   flattening trees by inserting parentheses where required.
# Returns XML (perhaps empty); DIEs in case of errors.
####

sub _tree2XML {
    my $self = shift;

    my $ra_search = shift;
    my $level = shift || 0;
                
#    use Data::Dumper;
#    print "===================================\n";
#    print Data::Dumper->Dump([$level,$ra_search]);
#    print "===================================\n";
    my $XML = ""; 
    if (!ref $ra_search) { 
        eval { $XML .= $self->__wholeExpression($ra_search) };
        if ($@) {
            # catch and re-throw exception (with offending search string)
            chomp $@;
            die($@ . ": '" . $ra_search . "'\n");
        }
    }    
    elsif (ref $ra_search eq "ARRAY") {
        $XML .= "<Criterion>\n" ; # In DBI used to be open paren
        my $expr;
        foreach $expr (@$ra_search) {
            $level++;
            $XML .= $self->_tree2XML($expr,$level);
        }
        $XML .= "</Criterion>\n" ; # in DBI used to be close paren
    }  
    else {
        confess("Search is not array ref or string");
    }   
    return $XML;

} # end of __treeToXML


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


##
## Private Methods
##


# Converts expression to XML Criterion object...
sub __wholeExpression {
    my $self = shift;
    my $whole_expr = shift;
            
    #print "Entering __wholeExpression with :$whole_expr:\n";
        
    my $xml_expr = ""; #"<Criterion>\n";
    my @pieces = $self->_splitOnQuotes($whole_expr);
    my $j;
    for ($j = 0; $j < @pieces; $j += 2) {
        my @expressions = split(/\b(AND|OR)\b/, $pieces[$j]);
        $expressions[-1] .= $pieces[$j+1] if $pieces[$j+1];
        my $i;
        for ($i = 0; $i < @expressions; ++$i) {
            next if !$expressions[$i] || $expressions[$i] =~ m/^\s+$/;
            my $expr = uc($expressions[$i]);
            if ($expr eq "OR" || $expr eq "AND") {
                $xml_expr .= "\n  <Type>$expr</Type> \n\n";
            } else {
# This was surrounding in parens but now it's expected to be
# a returned <Condition> XML object.
                $xml_expr .=
                    $self->__atomicExpression($expressions[$i]);
            }
        }
    }
    
#$xml_expr .= "</Criterion>\n";

    #print " --> $xml_expr\n";
    
    return $xml_expr;
} # end of __wholeExpression       

sub __atomicExpression {
    my $self = shift;
    my $expression = shift;

    my $atom_expr = "  <Condition>\n";
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

#    if ($lhs eq "*") {
#        my $field;
#        $atom_expr .= "    <Type>OR</Type>\n";
#        foreach $field ($self->getFieldNames) {
#            my $next = $self->__compareOneField($field, $op, $rhs);
#            $atom_expr .= $next if $next;
#        }
#    } else {
        $atom_expr .= $self->__compareOneField($lhs, $op, $rhs);
#    }

    $atom_expr .= "  </Condition>\n";

    return $atom_expr;
} # end of __atomicExpression

sub __compareOneField {
    my $self = shift;

    my $lhs = shift;
    my $op  = shift;
    my $rhs = shift;
    my $case_insensitive = shift || ($op =~ s/i$//i);

    #print "DEBUG: Called compareOneField with $lhs $op".($case_insensitive?"i"

    my $type = $self->getDataType($lhs);
    if (!defined($type) && $lhs ne "*") {
        die("Unknown Field: $lhs!");
    }

    my $expr;
    $op = "=" if $op eq "==";
    $op = "<>" if $op eq "!=";

    my $op_convert_hash = {
        '='  => 'EQUAL',
        '<>' => 'NOT_EQUAL',
        '>=' => 'GREATER_OR_EQUAL',
        '>'  => 'GREATER_THAN',
        '<=' => 'LESS_OR_EQUAL',
        '<'  => 'LESS_THAN'
    };

    $op = $op_convert_hash->{$op};
    my $rhs_value = $type->display2storage($rhs);

    my $xsi_type = $self->__getFieldToSOAPXSITypeMapping($lhs);
    $expr  = qq{    <Field>$lhs</Field>\n};
    $expr .= qq{    <Operand>$op</Operand>\n};
    if ($rhs eq "NULL") {
#$expr .= qq{    <Value xsi:type="$xsi_type" xsi:null="true"/>\n};
        $expr .= qq{    <Value xsi:null="true"/>\n};
    } else {
        if ($xsi_type =~ /xsd:string/i) {
           $rhs_value = EscapeXMLChars($rhs_value); 
        }
        $expr .= qq{    <Value xsi:type="$xsi_type">$rhs_value</Value>\n};
    }

    return $expr;

} # end of __compareOneField

sub __getFieldToSOAPXSITypeMapping {
    my $self = shift;
    my $field = shift;

    my $xsi_type = $self->{-FIELD_TO_SOAP_XSITYPE_MAPPINGS}->{$field};
    if (!defined($xsi_type)) {
        $xsi_type = "xsd:string";
    }
    
    return $xsi_type;

} # end of __getFieldToSOAPXSITyoeMappping

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

Extropia::Core::DataSource::DBI $Revision: 1.2 $

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

