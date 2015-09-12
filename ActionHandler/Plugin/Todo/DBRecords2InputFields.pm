package Plugin::Todo::DBRecords2InputFields;

use strict;
use Extropia::Core::Base qw(_rearrangeAsHash);
use base qw(Extropia::Core::Action);

#
# This plugin is mainly used for translation between the database
# fields and user input definitions.
#
# This plugin accepts -RECORDS which always points to a reference to a
# list of references to hashes, where each hash is a record with
# key/values as they are coming out of the database.
#
# This plugin adjusts the data -RECORDS points to if needed.  If you
# modify this plugin make sure that you don't break $ra_records.
# 
#

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([-RECORDS,],[-RECORDS,],@_);
    my $ra_records = $params->{-RECORDS};

    for my $rh_record (@$ra_records) {

        # META: need to use the DateTime
        if ($rh_record->{start_date} =~ /^(\d{4})-(\d\d)-(\d\d)/) {
            $rh_record->{start_day}  = $3 + 0;
            $rh_record->{start_mon}  = $2 + 0;
            $rh_record->{start_year} = $1 + 0;
        } 
        if ($rh_record->{due_date} =~ /^(\d{4})-(\d\d)-(\d\d)/) {
            $rh_record->{due_day}  = $3 + 0;
            $rh_record->{due_mon}  = $2 + 0;
            $rh_record->{due_year} = $1 + 0;
        } 
        if ($rh_record->{birth_date} =~ /^(\d{4})-(\d\d)-(\d\d)/) {
            $rh_record->{birth_day}  = $3 + 0;
            $rh_record->{birth_mon}  = $2 + 0;
            $rh_record->{birth_year} = $1 + 0;
        } 

        #E::dumper($rh_record);
    }

    return 2;
}


1;
__END__
