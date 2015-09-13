package Plugin::WebCal::DisplayAddFormAction;

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use base qw(Extropia::Core::Action);

#
# This plugin is used for presetting data in add form
#

sub execute {
    my $self = shift;
   my ($params) = _rearrangeAsHash
        ([
          -CGI_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         [
          -CGI_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         @_
        );

    my $cgi     = $params->{-CGI_OBJECT};


    # we arrive to this form by two pathes:
    # 1. when the add form is rendered for the first time
    # 2. when user clicks 'back' image instead of 'submit' because he
    #    wants to fix something, in the later case we don't have to
    #    set anything

    # I think that just checking for one bit is enough
    return 2 if $cgi->param('start_year');


    # the date may come as two pieces ('date'+'time') or 3 pieces
    # ('year','mon','mday' and no 'time') or none at all
    my $selected_datetime = '';
    if (my $selected_date = $cgi->param('date')) {
        my $selected_hour = $cgi->param('time') || '00:00';
        # META: temp Class::Date bug workaround, :00 should be gone
        # when it's fixed
        $selected_datetime = "$selected_date $selected_hour:00"
    } elsif (my $mday = $cgi->param('mday')) { # mday > 0
        my $year =  $cgi->param('year');
        my $mon =  $cgi->param('mon');
        $selected_datetime = sprintf "%04d-%02d-%02d 00:00:00", 
            $year, $mon, $mday;
    } else {
        $selected_datetime = 'now'; # default
    }

#print STDERR "datetime: $selected_datetime\n";
    my $datetime_config = $params->{-DATETIME_CONFIG_PARAMS};
    my $date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => $selected_datetime,
        );
#print STDERR "hour: ",$date_obj->hour,"\n";
    $cgi->param('start_year',$date_obj->year);
    $cgi->param('start_mon', $date_obj->month);
    $cgi->param('start_day', $date_obj->mday);
    $cgi->param('start_hour',$date_obj->hour);
    $cgi->param('end_year',  $date_obj->year);
    $cgi->param('end_mon',   $date_obj->month);
    $cgi->param('end_day',   $date_obj->mday);
    $cgi->param('end_hour',  $date_obj->hour+1); # suggest next hour

    return 2;
}


1;
__END__ 
