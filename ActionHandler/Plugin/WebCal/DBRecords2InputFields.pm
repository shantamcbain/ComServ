package Plugin::WebCal::DBRecords2InputFields;

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
    my ($params) = _rearrangeAsHash([
        -CGI_OBJECT,
        -RECORDS,
            ],
            [
        -CGI_OBJECT,
        -RECORDS,
            ],
        @_
    );

    my $cgi        = $params->{-CGI_OBJECT};
    my $ra_records = $params->{-RECORDS};


 my @months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");   



    for my $rh_record (@$ra_records) {

        # META: need to use the DateTime
        if ($rh_record->{start_date} =~ /^(\d{4})-(\d\d)-(\d\d)\s(\d\d):(\d\d)/) {
            $rh_record->{start_day}  = $3 + 0;
            $rh_record->{start_mon}  = $2 + 0;
            $rh_record->{start_year} = $1 + 0;
            $rh_record->{start_hour} = $4 + 0;
            $rh_record->{start_min}  = $5 + 0;
            my $mon = $rh_record->{start_mon} -1;
            $rh_record->{start_mon_short_string} = $months[$mon];
        } 
        if ($rh_record->{end_date} =~ /^(\d{4})-(\d\d)-(\d\d)\s(\d\d):(\d\d)/) {
            $rh_record->{end_day}  = $3 + 0;
            $rh_record->{end_mon}  = $2 + 0;
            $rh_record->{end_year} = $1 + 0;
            $rh_record->{end_hour} = $4 + 0;
            $rh_record->{end_min}  = $5 + 0;
             my $mon = $rh_record->{end_mon} -1;
            $rh_record->{end_mon_short_string} = $months[$mon];
        } 
        if ($rh_record->{recur_until_date} =~ /^(\d{4})-(\d\d)-(\d\d)/) {
            $rh_record->{recur_until_day}  = $3 + 0;
            $rh_record->{recur_until_mon}  = $2 + 0;
            $rh_record->{recur_until_year} = $1 + 0;
        }

        #E::dumper($rh_record);
    }

    return 2;
}


1;
__END__
