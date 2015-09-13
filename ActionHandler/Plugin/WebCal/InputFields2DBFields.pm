package Plugin::WebCal::InputFields2DBFields;

use strict;
use Extropia::Core::Base qw(_rearrangeAsHash);
use base qw(Extropia::Core::Action);

use Extropia::Core::App::WebCal;

#
# This plugin is mainly used for translation between user input
# definitions and the database fields. For example you can add to cgi
# object database fields, which weren't filled by user. (i.e. think of
# last_modified_by, etc.)
#
# Notice that all fields are forwarded from the action hanler, so you
# can basically access any field.
#
# Basically this plugin mungles the CGI_OBJECT. But you can think
# about other possible uses as well.
#
#############
sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash
        ([
          -CGI_OBJECT,
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
          -VALID_WORKING_HOURS,
          -DATETIME_CONFIG_PARAMS,
         ],
         [
          -CGI_OBJECT,
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
          -VALID_WORKING_HOURS,
          -DATETIME_CONFIG_PARAMS,
         ],
         @_
        );

    my $cgi     = $params->{-CGI_OBJECT};
    my $app     = $params->{-APPLICATION_OBJECT};
    my $session = $params->{-SESSION_OBJECT};
    my $datetime_config = $params->{-DATETIME_CONFIG_PARAMS};

    if ($cgi->param('is_all_day')) {
        # artificially set the start and end times to the edges of
        # the working day. Ignore the values set by user.
        my $ra_valid_working_hours = $params->{-VALID_WORKING_HOURS};
        $cgi->param('start_hour',$ra_valid_working_hours->[0]);
        $cgi->param('start_min', 0);
        $cgi->param('end_hour',  $ra_valid_working_hours->[-1]);
        $cgi->param('end_min',   0);
    }

    # set start_date and end_date db fields (and also original_ values
    # if available)
    for my $prefix ( qw(start end original_start original_end) ) {
        # set the date only if all values were set. Note that we use
        # defined only for value which can be zero.
        if ($cgi->param("${prefix}_year") and
            $cgi->param("${prefix}_mon")  and
            $cgi->param("${prefix}_day")  and
            $cgi->param("${prefix}_hour") and
            defined $cgi->param("${prefix}_min")
           ) {

            $cgi->param("${prefix}_date",
                        sprintf "%04d-%02d-%02d %02d:%02d",
                            $cgi->param("${prefix}_year"),
                            $cgi->param("${prefix}_mon"),
                            $cgi->param("${prefix}_day"),
                            $cgi->param("${prefix}_hour"),
                            $cgi->param("${prefix}_min"),
                       );
        }
    }

    # set recur_date db field (and also original_ value if available)
    for my $prefix ( qw(recur original_recur) ) {

        if ($cgi->param("${prefix}_interval")) {
            # set the date only if all values were set. Note that since
            # none of this can be 0, we don't need to use defined().
            if ($cgi->param("${prefix}_until_year")     and
                $cgi->param("${prefix}_until_mon")      and
                $cgi->param("${prefix}_until_day")
               ) {
                # recurring mode is on
                $cgi->param("${prefix}_until_date",
                            sprintf "%04d-%02d-%02d",
                            $cgi->param("${prefix}_until_year"),
                            $cgi->param("${prefix}_until_mon"),
                            $cgi->param("${prefix}_until_day"),
                           );
            }

        } else {
            # unset the interval date bits if interval is not set
            $cgi->delete("${prefix}_until_year");
            $cgi->delete("${prefix}_until_mon");
            $cgi->delete("${prefix}_until_day");

        }

    }

    # need the 'date' cgi field to be the same as 'start_date', so the
    # user will be shown the calendar page for this date, when she
    # proceeds (note that this is not a db field)

    $cgi->param('date',$cgi->param('start_date'));

    # META: is owner is not the same who modifies?

    my $username = $session->getAttribute(-KEY => 'auth_username');
    $cgi->param('owner',$username);
    $cgi->param('last_mod_by',$username);

    my $date_obj = Extropia::Core::DateTime::create (
         @$datetime_config,
         -DATETIME   => 'now',
    );

    
    $cgi->param('last_mod_date',
                $date_obj->get(-FORMAT => "%Y-%m-%d %H:%M:%S")
               );

    # the following fields are reserved for the future feature
    # extensions; they aren't used now.

    $cgi->param('type',    255);
    $cgi->param('status',  255);
    $cgi->param('priority',255);

    #############################
    # User Input Error checking
    #############################

    my $errors = 0;
    my $fatal_errors = 0;

    # I wish I had easier access to fields names definitions, this is
    # a hack (duplicate the info from .cgi)
    my %labels =
        (
         end_date         => 'End Date',
         start_date       => 'Start Date',
         recur_until_date => 'The Last Date of Recurrency',
        );

    # initialize date objects if we have the data.
    ### check: compare that the dates are valid
    my %date_objs = ();
    for my $prefix ( qw(start end recur_until ) ) {
        my $key = "${prefix}_date";
        next unless $cgi->param($key);

        $date_objs{$key} = Extropia::Core::DateTime::create
            (
             @$datetime_config,
             -DATETIME   => $cgi->param($key),
            );
        #E::dumper($date_objs{$key});
        #E::dumper($date_objs{$key}->get(-FORMAT => "%Y-%m-%d %H:%M:%S"));
        if (my $error = $date_objs{$key}->error) {
            $fatal_errors = 1;
            $app->addError("$labels{$key} is $error");
        }
    }

    # check whether we can proceed
    return 2 if $fatal_errors;

    ### check: compare the dates against the start_date
    if ($date_objs{start_date}) {

        for my $prefix (qw(end recur_until)) {
            my $key = "${prefix}_date";
            next unless $date_objs{$key};
            # start_date should always be smaller than the other dates
            E::dumper($key,$date_objs{$key}->dump,$date_objs{start_date}->compare_datetime(-WITH_OBJECT=>$date_objs{$key}));
            if ($date_objs{start_date}->compare_datetime(-WITH_OBJECT=>$date_objs{$key}) >= 0 ) {
                $errors++;
                $app->addError("$labels{$key} must be later than $labels{start_date}");
            }

        }
    }
    ### check: silently unset the recur_interval if recur date is not
    ### set (but only if there were no errors so far). we check the
    ### opposite possibility beforehand.
    if (!$errors) {
        $cgi->delete('recur_interval')
            unless $cgi->param('recur_until_date');
    }

    return 2 if $errors;

    ### check: make sure that spanning events which are also
    ### recurrent, don't overlap!

    # META: need to correct this to check for actual overlapping
    if (my $recur_interval = $cgi->param('recur_interval') ) {
        my $days_span = abs
            $date_objs{end_date}->exact_days_between(-WITH_OBJECT => $date_objs{start_date});
        my $error = "The spanning event you have specified overlaps with ".
                     "itself using the ";
        if ($recur_interval == Extropia::Core::App::WebCal::DAY and $days_span >= 1) {
            $errors++;
            $app->addError($error."daily recurrency interval");
        }
        elsif ($recur_interval == Extropia::Core::App::WebCal::WEEK and $days_span >= 7) {
            $errors++;
            $app->addError($error."weekly recurrency interval");
        }
        elsif ($recur_interval == Extropia::Core::App::WebCal::MONTH and $days_span >= 28) {
            # 28 should be fine, since nobody will have this kind of
            # event, other than having a typo
            $errors++;
            $app->addError($error."monthly recurrency interval");
        }
        elsif ($recur_interval == Extropia::Core::App::WebCal::YEAR and $days_span >= 364) {
            # 364 should be fine, since nobody will have this kind of
            # event, other than having a typo
            $errors++;
            $app->addError($error."yearly recurrency interval");
        } 
        else {
            # nothing
        }
    }

    return 2;
}


1;
__END__
