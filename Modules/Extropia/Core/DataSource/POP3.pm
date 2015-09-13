# $Id: POP3.pm,v 1.2 2001/03/28 03:30:05 stas Exp $
# Copyright (C) 2000  Jason Wilder
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

package Extropia::Core::DataSource::POP3;

use strict;
use vars qw($VERSION @ISA);

use Carp;
use Extropia::Core::Base qw(_rearrangeAsHash _rearrange);
use Extropia::Core::DataSource;
use Net::POP3;
use Mail::Internet;
use Date::Parse;
use Date::Format;


$VERSION = do { my @r = q$Revision: 1.2 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);


sub new {
    my $package = shift;
    my $self = 0;
    
    my ($parameters) = _rearrangeAsHash(
        [-SERVER,          
         -USERNAME, 
         -PASSWORD,       
         -SYNC_FILE_NAME,
         -POP3_FIELD_TO_DS_FIELD_MAPPINGS,
         -FIELD_NAMES],          
        [-SERVER, -USERNAME, -PASSWORD], @_);
    
    
    my @DEFAULT_FIELD_NAMES = ('ID','MSGNUM','TO', 'FROM', 'SUBJECT', 'CC', 
                               'BCC','DATE','HEADER','BODY', 'FULLTEXT');   

    my %DEFAULT_FIELD_MAPPINGS;
    foreach (@DEFAULT_FIELD_NAMES) {
        $DEFAULT_FIELD_MAPPINGS{$_} = $_;
    } 
    
    ## Use default field names?
    if (!defined($$parameters{'-FIELD_NAMES'})) {
    
        ## Use default field names      
       $self = $package->SUPER::new((@_, -FIELD_NAMES => \@DEFAULT_FIELD_NAMES)); 
       
    ## Make sure they specify all of the field names or specify a mapping to use instead
    } elsif (!defined($$parameters{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'})) {
                            
        my @USER_DEFINED_FIELD_NAMES = @{$$parameters{'-FIELD_NAMES'}};
        if ($#USER_DEFINED_FIELD_NAMES == $#DEFAULT_FIELD_NAMES) { 
            foreach (@USER_DEFINED_FIELD_NAMES) {
                if (!defined($DEFAULT_FIELD_MAPPINGS{$_})) {
                    die "Whoopsy! You have specified a non-default field named, $_, without a POP3 mapping.".
                         " Please specify which POP3 field this field maps to with the".
                         " -POP3_FIELD_TO_DS_FIELD_MAPPINGS parameter";                        
                }
            }
        } else {
            die "Whoopsy! You have specified an incorrect number of field names in the -FIELD_NAMES".
                " parameters.  Please use all of the following field names: ".
                join(", ",@DEFAULT_FIELD_NAMES)." or do not specify the -FIELD_NAMES parameter to use".
                " the defaults.";                        
        }
        
        $self = $package->SUPER::new(@_); 

    } else {

        $self = $package->SUPER::new(@_); 

    }
    
    
    $self->{-SERVER} = $$parameters{'-SERVER'}; 
    $self->{-USERNAME} = $$parameters{'-USERNAME'}; 
    $self->{-PASSWORD} = $$parameters{'-PASSWORD'}; 
    $self->{-SYNC_FILE_NAME} = $$parameters{'-SYNC_FILE_NAME'} || ""; 
            
    
    if (defined($$parameters{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'})) {
        foreach (@DEFAULT_FIELD_NAMES) {            
            if (defined(${$$parameters{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'}}{$_})) {
                ${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_} = 
                    ${$$parameters{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'}}{$_};
            } else {
                ${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_} = $DEFAULT_FIELD_MAPPINGS{$_};
            }                     
        }  
        
        ## Check that all mappings are valid mappings.  Don't allow mappings of fields that
        ## are not default fields (i.e.) MY_POP3_FIELD => my_field.  
        ## lhs must be a value from @DEFAULT_FIELD_NAMES
        foreach (keys %{$$parameters{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'}}) {  
        
            if (!defined(${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_})) {
                warn "WARNING: $_ is not a default field name and will not be mapped.  Are you ".
                     "sure the field name is spelled correctly?\n";
            } else {
                my $invalid_field = 1;
                foreach my $valid_field ($self->getFieldNames()) {
                    if ($valid_field eq ${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_}) {
                        $invalid_field = 0;
                    }
                }
                if ($invalid_field) {
                    warn "WARNING: ".${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_}." is not ".
                         "listed in -FIELD_NAMES and will not be mapped.  Are you ".
                         "sure the field name is spelled correctly?\n";
                }
            }
        }
        
        ## Check for DEFAULT_FIELD => invalid_field errors (i.e. TO => Tp)        
        foreach my $valid_field ($self->getFieldNames()) {               
            my $invalid_field = 1;
            foreach (values %{$self->{'-POP3_FIELD_TO_DS_FIELD_MAPPINGS'}}) {
                if ($valid_field eq $_) {
                    $invalid_field = 0;
                }
            }
            if ($invalid_field) {
                warn "WARNING: ".$valid_field." is not ".
                     "listed in -POP3_FIELD_TO_DS_FIELD_MAPPINGS and will not be mapped.  Are you ".
                     "sure the field name is spelled correctly?\n";
            }            
        }
        
        
    ## Use default mappings    
    } else {
        $self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS} = \%DEFAULT_FIELD_MAPPINGS;
    }
                              
    ## Create handle to pop server   
    my $pop3 = $self->__connect($self->{-SERVER}, $self->{-USERNAME}, $self->{-PASSWORD});
    
    $self->{'_pop3'} = $pop3;        
    
    return bless $self, $package;
}

sub _realSearch {
    my $self = shift;
    my $ra_search = shift;
    my $last_record_retrieved = shift;
    my $max_records_to_retrieve = shift;
    my $order = shift;
    my $rs_data = shift;
    
    my $pop3 = $self->{'_pop3'};
    my ($total_msgs, $total_size) = (($pop3->popstat())[0,1]) or (0, 0);

    $self->{'_messages_remaining'} = $self->{'_pop3'}->uidl();             
    $self->{'_total_messages'} = $total_msgs;
    
    ## if we're using a sync file (only retrieve new messages), then read in the 
    ## previously retrieved message ids
    if ($self->{-SYNC_FILE_NAME} ne "") {  
    
        if (-e $self->{-SYNC_FILE_NAME}) {
            
            $self->{'_stored_count'} = 0;
            open(IN, "<".$self->{-SYNC_FILE_NAME});
            while (<IN>) {            
                chomp;

                ## mark it as previously read
                $self->{'_stored_msgs'}{$_} = "stored"; 
                $self->{'_stored_count'}++;
            }
            close(IN);
        } 
    }
    
    
    my $record_set = Extropia::Core::DataSource::RecordSet->create(
        @$rs_data,
        -DATASOURCE => $self,
        -KEY_FIELDS => $self->_getKeyFields(),
        -UPDATE_STRATEGY => $self->getUpdateStrategy(),
        -REAL_SEARCH_QUERY => $ra_search,
        -LAST_RECORDS_RETRIEVED => $last_record_retrieved,
        -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve);
        
    return $record_set;
}

sub _searchForNextRecord {
    my $self = shift;
    my $ra_search = shift;
    
    my $record_found = 0;
    
    ## Test connection
    if (defined($self->{'_pop3'})) {
        $self->{'_pop3'}->popstat();               
    }
        
    if (!$self->{'_pop3'}->ok() || !$self->_matchesActiveQuery($ra_search)) {
        $self->addError(
            -CODE => 501,
            -MESSAGE => "Attempt to retrive data on an inactive connection",
            -SOURCE => 'DataSource::POP3',
            -CALLER => (caller)[0]);
        
        return undef;           
    }
    
    my %stored_msgs = ();
    my %stored_msgs_reverse = ();
    
    ## Only want to return all new messages    
    
    if ($self->{-SYNC_FILE_NAME}) {
                
        foreach (keys %{$self->{'_messages_remaining'}}) {  
    
            $stored_msgs_reverse{${$self->{'_messages_remaining'}}{$_}} = $_;
            
            my $msg_id = "";
            if ($self->{'_stored_count'}) {
                $msg_id = $self->{'_stored_msgs'}{${$self->{'_messages_remaining'}}{$_}} || "";                
            }
            
            if ($msg_id eq "") {         
                
                my %record = ();

                my $msg = $self->{'_pop3'}->get($_);
                my $id = $self->{'_pop3'}->uidl($_); chomp($id);                

                $msg = new Mail::Internet($msg);
                %record = $self->_msgToRecord($msg);

                $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'MSGNUM'}} = $_;
                $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'ID'}} = $id;

                ## mark it as a new message
                $self->{'_stored_msgs'}{${$self->{'_messages_remaining'}}{$_}} = "new";

                delete ${$self->{'_messages_remaining'}}{$_};

                return $self->_recordInternal2Display(\%record);
                            
            } else {
                
                ## change mark to message is old but still on server
                $self->{'_stored_msgs'}{${$self->{'_messages_remaining'}}{$_}} = "old";
            }

        }
    
        ## save messages retrieved
        open(OUT, ">".$self->{-SYNC_FILE_NAME}) or die $!;
        foreach (keys %{$self->{'_stored_msgs'}}) {
        
            ## remove ids that are no longer on the server
            if ($self->{'_stored_msgs'}{$_} ne "stored") {
                print OUT $_,"\n";        
            }
        }
        close(OUT);    
    
    
    } else {
    
        while ($self->{'_total_messages'} > 0) {
            my %record = ();
            my $msg = $self->{'_pop3'}->get($self->{'_total_messages'});
            my $id = $self->{'_pop3'}->uidl($self->{'_total_messages'}); chomp($id);                   
            
            
            $msg = new Mail::Internet($msg);
            
            my @record = ();
            %record = $self->_msgToRecord($msg);
            
            $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'MSGNUM'}} = $self->{'_total_messages'};
            $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'ID'}} = $id;

            $self->{'_total_messages'}--;        

            if (defined($ra_search)) {

                if (eval{ $self->_matches($ra_search, \%record) }) {                  
                    return $self->_recordInternal2Display(\%record);
                }                
           } else {
                return $self->_recordInternal2Display(\%record);
           } 
        } 
    }    
    return undef;
    
}


sub doUpdate {
    my $self = shift;
    @_ = _rearrange([-RETURN_ORIGINAL],[],@_);
    my $ret_orig = shift || 0;
    
    # Check that we can update (not READ_ONLY)
    return undef unless $self->_canUpdate("AddError");

    # If no work to do, can cut it short
    my $pending_updates = $self->_getPendingUpdates();
    return 0 if (!@$pending_updates && !$ret_orig);

    my @original = ();
    my $errors = 0;
    my $affected_rows = 0;
    
    my $pop3 = $self->{'_pop3'};
    my ($total_msgs, $total_size) = $pop3->popstat();
    
    $self->{'_total_messages'} = $total_msgs;
          
    my $uidl;
          
    if (@$pending_updates) {        

        my $update;

        foreach $update (@$pending_updates) {

            my $search  = ${$update->[1]}[0]; 
            my $optimized_ok = 1;
            foreach ('MSGNUM', 'TO', 'FROM', 'SUBJECT', 'CC', 'BCC', 'DATE', 'HEADER', 'BODY', 'FULLTEXT') {
                my $mapped = ${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{$_};
                if (($search =~ /$_/i) or ($search =~ /$mapped/i)) {
                    $optimized_ok = 0;
                }
            }             

            if ($optimized_ok) {

                if (ref($uidl) ne "HASH") {
                    $uidl = $self->{'_pop3'}->uidl();
                }


                foreach (keys %{$uidl}) {
                    my %record = ();
                    my $id = $$uidl{$_};
                    chomp($id);
                    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'ID'}} = $id;
                    if ( $self->_matches($update->[1], \%record) ) {
                        push @original, return $self->_recordInternal2Display(\%record) if $ret_orig;
                        ## POP3 only supports deleting of messages
                        if ($update->[0] eq "DELETE") {

                            $pop3->delete($self->{'_total_messages'});

                        }    

                        ++$affected_rows;
                    }                                                        
                }
                $self->{'_total_messages'} = 1;

            } else {
                while ($self->{'_total_messages'}) { 

                    my %record = ();
                    my $msg = $self->{'_pop3'}->get($self->{'_total_messages'});

                    my $id = $self->{'_pop3'}->uidl($self->{'_total_messages'});
                    chomp($id);                   
                    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'ID'}} = $id;


                    $msg = new Mail::Internet($msg);
                    my @record = ();

                    %record = $self->_msgToRecord($msg);

                    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'MSGNUM'}} = $self->{'_total_messages'};




                    if ( $self->_matches($update->[1], \%record) ) {

                        push @original, return $self->_recordInternal2Display(\%record) if $ret_orig;

                        ## POP3 only supports deleting of messages
                        if ($update->[0] eq "DELETE") {

                            $pop3->delete($self->{'_total_messages'});
                        }    

                        ++$affected_rows;

                    }
                    $self->{'_total_messages'}--;
                }
            }    
        
        }             
        
    } 

    if ($errors) {
        return undef;
    }
    return $self->_successfulUpdate($ret_orig, \@original, $affected_rows);
}




sub disconnect {
    my $self = shift;

    
    my $pop3 = $self->{'_pop3'};
    $pop3->quit() if $pop3;
}


##
## Private Methods
##


sub _msgToRecord {
    
    my $self = shift;
    my $msg = shift;    
    
    my %record = ();
    my $to = $msg->head()->get("To") || ""; chomp($to) if $to;           
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'TO'}} = $to;

    my $from = $msg->head()->get("From") || ""; chomp($from) if $from;
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'FROM'}} = $from;

    my $subj = $msg->head()->get("Subject") || ""; chomp($subj) if $subj;
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'SUBJECT'}} = $subj;

    my $cc = $msg->head()->get("Cc") || ""; chomp($cc) if $cc;
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'CC'}} = $cc;

    my $bcc = $msg->head()->get("Bcc") || ""; chomp($bcc) if $bcc;
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'BCC'}} = $bcc;

    my $date = $msg->head()->get("Date") || ""; chomp($date) if $date;    
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'DATE'}} = str2time($date);

    my $header = $msg->head()->as_string() || ""; chomp($header) if $header;    
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'HEADER'}} = $header;

    my $body = join("", @{$msg->body()}) || ""; chomp($body) if $body;    
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'BODY'}} = $body;

    my $fulltext = $msg->as_string() || ""; chomp($fulltext) if $fulltext;
    $record{${$self->{-POP3_FIELD_TO_DS_FIELD_MAPPINGS}}{'FULLTEXT'}} = $fulltext;    
    
    return %record;

}


sub _getServer {
    return $_[0]->{-SERVER};
}

sub _getUsername {
    return $_[0]->{-USERNAME};
}

sub _getPassword {
    return $_[0]->{-PASSWORD};
}


sub __connect {
    my $self = shift;
    my ($server, $user, $pass) = @_;

    my $pop3;
    $pop3 = new Net::POP3($server);
    if ($pop3) {
    
        ## login closes the connection if there are no messages        
        my $msg_count = $pop3->login($user, $pass);        
        if (defined($msg_count)) {            
 
            return $pop3;
            
        } else {
            $self->addError(
                -CODE    => $pop3->code(),
                -MESSAGE => "Login failed: " . $pop3->message(),
                -SOURCE  => 'DataSource::POP3',
                -CALLER  => (caller)[0]);
        }                    
    
    } else {
        $self->addError(
            -CODE    => 300,
            -MESSAGE => "Connect failed with ".$server,
            -SOURCE  => 'DataSource::POP3',
            -CALLER  => (caller)[0]);    
    }    
    
    return $pop3;
}

1;
__END__


=head1 NAME

Extropia::Core::DataSource::POP3 - A Perl5 object for manipulating mail messages on 
a POP3 mail server.

=head1 SYNOPSIS

  use Extropia::Core::DataSource;
         
  my $ds = Extropia::Core::DataSource->create(
             -TYPE        => 'POP3',
             -SERVER      => 'server',
             -USERNAME    => 'username',
             -PASSWORD    => 'password',
             -SYNC_FILE_NAME => 'filename.syn',    
             -FIELD_NAMES => 
                ['TO', 'FROM', 'SUBJECT', 'CC', 'BCC', 'DATE',
                 'HEAD','BODY','FULLTEXT','ID','MSGNUM'],    
             -FIELD_TYPES => 
                { DATE => 'Date', MSGNUM => 'Number'}
           );           
                    

=head1 DESCRIPTION

This module is a driver that implements the Extropia::Core::DataSource interface.
Thus, apart from the single line of code that creates this particular type
of driver, you use it in exactly the same way as you would any other 
Extropia::Core::DataSource.

Only searching and deleting of messages are supported since POP3 does not 
allow inserts or updates to messages.

This module requires Mail::Internet and Net::POP3.

See S<USAGE> for a description of driver-specific creation parameters.  
See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 USAGE

=head2 Object Creation

In general, you will not create an Extropia::Core::DataSource::POP3 object
directly.  Instead, call the Extropia::Core::DataSource->create() method with the
following parameters.  A DataSource object of the appropriate type will be
returned.

These parameters are required, for all POP3 DataSources:

=over 4

=item -SERVER

Specifies the POP3 server to use for retrieving messages.  Set to "POP3"
for POP3 DataSource.  This value must be supplied; there is no default.

=item -USERNAME

The username for login.  This value must be supplied; there is no default.

=item -PASSWORD

The password associated with the username. This value must be supplied; 
there is no default.

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



=back

The following optional parameters are specific to the DataSource::File
driver:

=over 4

=item -SYNC_FILE_NAME

An optional filename for storing the state of the login/password on the POP3
server.  If -SYNC_FILE_NAME is specified, DataSource::POP3 will only retrieve
messages that have not previously been retrieved.  Specifying this parameter
will ignore any query that is specified when searching.  This is useful for 
retrieving only new messages since that last time messages were retrieved.

The only valid search when this parameter is specfied is:
  
  $rs = $ds->search();

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

This module also uses Graham Barr's Mail::Internet and Net::POP3 modules
from the libnet bundle.

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

Extropia::Core::DataSource::File $Revision: 1.2 $

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

=head1 SEE ALSO

See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 COPYRIGHT

(c) 2000, Jason Wilder (http://www.jasonwilder.com)

This module is open source software, and may generally be used according to
the spirit of the Perl "Artistic License".  If you are interested, however,
the actual license for this module may be found at http://www.extropia.com
(or more directly, at http://www.extropia.com/download.html).

=head1 AUTHOR

Extropia::Core::DataSource::POP3 is a Perl module written by Jason Wilder
(http://www.extropia.com). Special thanks to Gunther Birznieks,
Peter Chines and Selena Sol.

=head1 SUPPORT

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

Questions, comments and bug reports should be sent to support@extropia.com.

=cut