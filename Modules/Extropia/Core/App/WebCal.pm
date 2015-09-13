package Extropia::Core::App::WebCal;

# Copyright (C) 1994 - 2001  eXtropia.com
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

use strict;
use Carp;

use base qw(Extropia::Core::App::DBApp);
use Extropia::Core::DateTime;

# any day in the event constructed of a few days can be: the only day
# in event (ONEDAY) the FIRST day, the MIDDLE day and finally the LAST
# day of the event
use enum qw(ONEDAY FIRSTDAY MIDDLEDAY LASTDAY);
use enum qw(LESS=-1 EQUAL=0 GREATER=1);
use enum qw(NONE DAY WEEK MONTH YEAR);

use Extropia::Core::Base qw(
    _rearrangeAsHash 
    _rearrange
    _assignDefaults
    _dieIfRemainingParamsExist
);


# $self->interset(\@dates,$start_obj,$end_obj);
# 
# input:
#
# - a ref to an array with @dates as strings (must be sorted from the
#   oldest date to the latest date),
# - start_obj (the interval starting datetime object)
# - end_obj   (the interval ending datetime object)
#
# the function modifies the @dates array and sets the elements that
# don't fit into the interval as undefs and turns the fitting one into
# datetime objects (since we will have these objects anyway).
#
# so by observing the resulting @dates you can tell the following:
#
#my $i = 0;
#for (@dates) {
#    if (defined $dates[$i]) {
#        if (@dates == 1) {
#            # starts and ends on this day
#        } elsif ($i == 0) {
#            # starts on this day
#        } elsif ($i == $#dates) {
#            # ends on this day
#        } else {
#            # in the middle of the multi-day event
#        }
#    } else {
#        # skip (not in the interval)
#    }
#    $i++;
#}
#
#############
sub interset{
    my $self = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash
        (
         [-DATETIME_CONFIG_PARAMS,-RA_DATES,-START_OBJ,-END_OBJ],
         [-DATETIME_CONFIG_PARAMS,-RA_DATES,-START_OBJ,-END_OBJ],
         @_);
    _dieIfRemainingParamsExist(@_);
    my $datetime_config  = $data->{-DATETIME_CONFIG_PARAMS};
    my $ra_dates  = $data->{-RA_DATES};
    my $start_obj = $data->{-START_OBJ};
    my $end_obj   = $data->{-END_OBJ};


    for my $date (@$ra_dates) {

        my $date_obj = Extropia::Core::DateTime::create
            ( @$datetime_config,-DATETIME => $date);

        if ($date_obj->compare_date(-WITH_OBJECT => $start_obj) == Extropia::Core::DateTime::LESS 
            ||
            $date_obj->compare_date(-WITH_OBJECT => $end_obj) == Extropia::Core::DateTime::GREATER ) {
            $date = undef;
        } else {
            $date = $date_obj;
        }
    }
}




# sets the key -SELECTED_DATE_DATA to a hash whose data is based on
# the selected date and used in various view widgets
######################
sub setSelectedDateData{
    my $self = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash([-DATE_OBJECT],[-DATE_OBJECT],@_);
    _dieIfRemainingParamsExist(@_);
    my $date_obj = $data->{-DATE_OBJECT};

    my %valid_date_by_mon = ();
    my $year = $date_obj->year;
    my $mday = $date_obj->mday;

    {
        # make sure that in the yearwidget calendar the dates will be
        # set correctly, e.g. if the current date is XXXX-XX-31, Feb
        # will point to XXXX-XX-28 and not 31.
        my $tmp = $date_obj->clone;
        $tmp->mday(-VALUE => 1); # make sure that we always get the month correctly

        for my $mon (1..12) {
            $tmp->month(-VALUE => $mon);
            my $days_in_month = $tmp->days_in_month;
            $valid_date_by_mon{$mon} = $days_in_month < $mday 
                ? $days_in_month
                : $mday;
        }
    }

    my $rh_selected_date_data =
        {
         mon      => $date_obj->month,
         mon_str  => $date_obj->month_string,
         wday_str => $date_obj->wday_string,
         year     => $year,
         mday     => $mday,
         date     => $date_obj->get(-FORMAT => "%Y-%m-%d"),
         date_str => $date_obj->date_string,
         month_begin_wday => $date_obj->month_begin_wday,
         days_in_month    => $date_obj->days_in_month,

         prev_day_date   => $date_obj->clone->add_delta_ymd(-DAYS=>-1)->get(-FORMAT => "%Y-%m-%d"),
         next_day_date   => $date_obj->clone->add_delta_ymd(-DAYS=>+1)->get(-FORMAT => "%Y-%m-%d"),
         prev_month_date => $date_obj->clone->add_delta_ymd(-MONTHS=>-1)->get(-FORMAT => "%Y-%m-%d"),
         next_month_date => $date_obj->clone->add_delta_ymd(-MONTHS=>+1)->get(-FORMAT => "%Y-%m-%d"),
         prev_year_date  => $date_obj->clone->add_delta_ymd(-YEARS=>-1)->get(-FORMAT => "%Y-%m-%d"),
         next_year_date  => $date_obj->clone->add_delta_ymd(-YEARS=>+1)->get(-FORMAT => "%Y-%m-%d"),
         valid_date_by_mon => \%valid_date_by_mon,
        };

        $self->setAdditionalViewDisplayParam
        (
         -PARAM_NAME  => "-SELECTED_DATE_DATA",
         -PARAM_VALUE => $rh_selected_date_data,
        );

}


# sets the key -TODAY_DATA to ref to a hash with today's data
######################
sub setTodayData{
    my $self = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash([-DATETIME_CONFIG_PARAMS],[-DATETIME_CONFIG_PARAMS],@_);
    _dieIfRemainingParamsExist(@_);
    my $datetime_config = $data->{-DATETIME_CONFIG_PARAMS};

    my $date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => 'now',
        );

    my $rh_today_data =
        {
         mon      => $date_obj->month,
         mon_str  => $date_obj->month_string,
         wday_str => $date_obj->wday_string,
         year     => $date_obj->year,
         mday     => $date_obj->mday,
         date     => $date_obj->get(-FORMAT => "%Y-%m-%d"),
         date_str => $date_obj->date_string,
        };

        $self->setAdditionalViewDisplayParam
        (
         -PARAM_NAME  => "-TODAY_DATA",
         -PARAM_VALUE => $rh_today_data,
        );

}




# This functions expects these named arguments:
#
# -SELECTED_DATE - the selected date
#
# -DATETIME_CONFIG_PARAMS - the datetime config params (forwarded)
#
# -RA_DATA: an array of events for a given day. Where each event has to
# have at least the following fields: starting and the ending date and
# time (where we don't care about the day) and the subject of the
# event.
#
# -RA_HOURS: a ref to an array with a range of hours to construct the
# matrix with.
#
# This function returns two arguments:
#
# out-1. a ref to a 2D matrix where the rows are denominated by hours
# and columns by events. There are two and more columns if two or more
# events happen overlap within the same hour. Note that if there is an
# event 09:00-09:30 and 09:31-10:00, because of HTML limitations these
# two event are considered to be overlapping and will consume two
# columns.
#
#   each cell in this matrix, has either:
#
#  undef  -- an empty cell
#  {}     -- record continues from the previous row
#  {note=>...,rowspan=>...}
#         -- record is starting in this cell
#            o 'note' includes the content to be printed in the cell
#            o 'rowspan' specifies for how many rows the event spawns
#
# out-2. the last column number in the matrix (assuming that the first
# column is counted as zero)
#
#
# The algorithm for building the matrix
#
# 1. Go through all entries and stack all the entries into a hash,
#    where those starting at the same hour, will be placed into the
#    same entry of the hash (as a list). Handle the spanning
#    non-recurrent events and adjust the start and end hours according
#    to:
#    - use the start hour and the hour of the end of the day for the
#      first day in the span
#    - use the end hour and the hour of the beginning of the day for
#      the last day in the span
#    - use all working hours if it's none from the above
#
# 2. sort the entries within the same hour by the event start_min!
#
# 3. Go through the hours:
#
#   for 8..23 (use the passed 'hours' array)
#     * go through all entries for the given hour and insert them into
#       the matrix one by one:
#         o if the event starts at the hour of the cell -- assign a
#           ref to the hash into the current cell. (see above for the
#           content of the hash)
#         o if the event extends beyond this hour -- fill other cells
#           in the same column hours with {} (to indicate that the
#           cell is occupied)
#         o empty cells will be undefs.
#    * figure out the max overlap width on the way (at the end of
#      processing of all the events starting at the same hour)
#
##########################
sub GetDataForSelectedDay{
    my $self = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash
        (
         [-RA_DATA,-RA_HOURS],
         [-RA_DATA,-RA_HOURS],
         @_);
    _dieIfRemainingParamsExist(@_);

    my $ra_data         = $data->{-RA_DATA};
    my $ra_hours        = $data->{-RA_HOURS};

    # alg-1
    my %by_hour = ();
    for my $event (@$ra_data) {
        #print STDERR $event->{id},": $s_hour:$s_min $e_hour:$e_min\n";
        push @{ $by_hour{ $event->{s_hour} } }, $event;
    }

    # alg-2
    for (keys %by_hour){
        $by_hour{$_} = [sort {$a->{s_min} <=> $b->{s_min}} @{ $by_hour{$_} }];
    }

    # alg-3
    my %data = ();
    my $last_col = 0;
    for my $hour (@$ra_hours) {
        my $col = 0;
        next unless $by_hour{$hour};
        for my $event (@{ $by_hour{$hour} }){
            # find the next empty cell
            $col++ while $data{$hour}{$col};

            my $row_span = 1;
            my $next_hour = $hour;
            unless ($event->{e_hour} == $hour){
                $next_hour += 1;
                # mark the cells in the following column if the event
                # is extending into the next hour
                while ($next_hour < $event->{e_hour} or 
                       ($next_hour == $event->{e_hour} and $event->{e_min} > 0)
                      ){
                    $data{$next_hour++}{$col} = {}; # mark that the cell is taken
                    $row_span++;
                }
            }

            # construct the note:
            my $note = '';
            # if the event doesn't start and finish at the round hour,
            # we have to specify the exact beginning and ending time
            $note .= sprintf " %02d:%02d-%02d:%02d",
                $event->{s_hour},$event->{s_min},
                $event->{e_hour},$event->{e_min}
                    unless $event->{s_min} == 0 and $event->{e_min} == 0;

            $note .= " ".$event->{subject};
            $note .= " (".$event->{location}.")" if $event->{location};

            # fill the cell with start at this hour
            $data{$hour}{$col} = {
                                  note    => $note,
                                  rowspan => $row_span,
                                  record_id => $event->{record_id},
                                 };
        }

        # calculate the max cols width
        $last_col = $col if $col > $last_col;
    }

#    print STDERR "last_col $last_col\n";
#    # debug: prints the matrix
#    for my $hour (@$ra_hours) {
#        printf STDERR "%02d: ",$hour;
#        for my $col (0..$last_col){
#            local $_ = $data{$hour}{$col};
#            print (STDERR ". ") && next unless ref $_ and ref $_ eq 'HASH';
#            print (STDERR "O ") && next if %$_;
#            print (STDERR "# ") && next;
#        }
#        print STDERR "\n";
#    }

    return (\%data,$last_col);

}






# gets * the start and the end of the range to check
#      * the start and the end of the recurrent event
#      * recurrency interval
#
# returns: a ref to a list of dates ("%Y-%m-%d") following within the
#          requested range
#
#########################################
sub Events2DatesInRange{
    my $self = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash
        ([-DATETIME_CONFIG_PARAMS,
          -RANGE_START_DATE,
          -RANGE_END_DATE,
          -EVENT_START_DATE,
          -EVENT_END_DATE,
          -RECUR_END_DATE,
          -RECUR_INTERVAL,
         ],
         [-DATETIME_CONFIG_PARAMS,
          -RANGE_START_DATE,
          -RANGE_END_DATE,
          -EVENT_START_DATE,
          -EVENT_END_DATE,
          -RECUR_END_DATE,
          -RECUR_INTERVAL,
         ],
         @_
        );
    _dieIfRemainingParamsExist(@_);

    my $datetime_config  = $data->{-DATETIME_CONFIG_PARAMS};
    my $range_start_date = $data->{-RANGE_START_DATE};
    my $range_end_date   = $data->{-RANGE_END_DATE};
    my $event_start_date = $data->{-EVENT_START_DATE};
    my $event_end_date   = $data->{-EVENT_END_DATE};
    my $recur_end_date   = $data->{-RECUR_END_DATE};
    my $recur_interval   = $data->{-RECUR_INTERVAL};

    my $range_start = Extropia::Core::DateTime::create
        (@$datetime_config,-DATETIME   => $range_start_date);
    my $range_end   = Extropia::Core::DateTime::create
        (@$datetime_config,-DATETIME   => $range_end_date);
    my $event_start = Extropia::Core::DateTime::create
        (@$datetime_config,-DATETIME   => $event_start_date);
    my $event_end   = Extropia::Core::DateTime::create
        (@$datetime_config,-DATETIME   => $event_end_date);
    my $recur_end   = Extropia::Core::DateTime::create
        (@$datetime_config,-DATETIME   => $recur_end_date);

    # fix the recurrency end date for spanning+recurrent events. The
    # actual recurrency date should add the span.
    my $days_span = $event_end->days_span(-WITH_OBJECT => $event_start);
    my $exact_days_between = $event_end->exact_days_between(-WITH_OBJECT => $event_start);
    #if ($days_span > 1) {
        # the following is supposed the do the right thing when a user
        # choses to have a recurrent and spanning event at the same
        # time. So consider the case for an event starts on the first
        # day of the month (just to make the example simple) that
        # recurs weekly and its length is of 3 days, so we have:
        # 1-3, 7-10, 14-17, ... 
        # now if the recurrency end is marked as 22, should it be:
        # a) 1-3, 7-10, 14-17, 21-22
        # or
        # b) 1-3, 7-10, 14-17, 21-23
        #
        # the question is whether the last span should be completed or
        # stopped as specified by user.  Currently the implementation
        # is of the case a), where the last day is as specified by
        # user
        #
        # If a different design is desired this can be arranged by the
        # following code. It's possible to have a flag to choose which
        # behavior is to be used.
        # 
        # META: this is not clean! Should add the logic to do this
        # expanding based on the actual recurrency intervals, for
        # example if we take a weekly interval, we want to add only
        # the number of days till the end of the event and not the
        # whole week.
        # So I turn this off for now.
        # $recur_end->add_delta_ymd(-DAYS => ($days_span-1) );
    #}

    # in case where the recurrent event starts after the range's start,
    # shorten the range to start from this later date.
    $range_start = $event_start 
        if $range_start->compare_date(-WITH_OBJECT => $event_start) < GREATER;

    # in case where the recurrent event ends before the range's end,
    # shorten the range to end at this earlier date.
    $range_end = $recur_end 
        if $range_end->compare_date(-WITH_OBJECT => $recur_end) == GREATER;

#    print STDERR "Range: ",$range_start->get(-FORMAT => "%Y-%m-%d"),
#        " - ",$range_end->get(-FORMAT => "%Y-%m-%d"),"\n";
#    print STDERR "Reccu: ",$event_start->get(-FORMAT => "%Y-%m-%d"),
#        " - ",$recur_end->get(-FORMAT => "%Y-%m-%d"),"\n";
#    print STDERR "Reccurency: $recur_interval \n";

    my @dates = ();
    if ($recur_interval == NONE) {
        # non-recursive event
        my $days = $range_start->days_between(-WITH_OBJECT => $event_start);

        if ($days <= 0) {
            # if the event goes inside the range, adjust the range start
            $range_start = $event_start;
        }

        my $count = $days > 0 ? $days : 0;
        # go from range_start to range_end and return all the dates in between
        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
            $count++;

            my $day = $count;
            my @occur = ();
            if ($days_span == 1) {
                # all events here start and end on the same day: hence ONEDAY
                push @occur, ONEDAY;
            }
            else {
                # the same date might appear twice: as the end of the
                # event from the previous day and the beginning of the
                # event on this day
                if ($day == 1) {
                    push @occur, FIRSTDAY;
                } elsif ($day == $days_span) {
                    push @occur, LASTDAY;
                } else {
                    push @occur, MIDDLEDAY;
                }
            }
            # store it if overlaps (must clone the object so we can use it later)
            push @dates,[$range_start->clone,\@occur] if @occur;
            $range_start->add_delta_ymd(-DAYS => 1); # add one day
        } 

    } elsif ($recur_interval == DAY) {
        # we assume that the events don't overlap over themselves, but
        # an event which recurs daily but starts on the evening and
        # finishes on the next day's morning is a valid one (a night
        # shift?)

        my $already_started =
            $event_start->compare_date(-WITH_OBJECT => $range_start) == LESS ? 1 : 0;

        # go from range_start to range_end and return all the dates in between
        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
            my @occur = ();
            if ($days_span == 1) {
                # all events here start and end on the same day: hence ONEDAY
                push @occur, ONEDAY;
            }
            elsif ($days_span == 2) {
                # the same date might appear twice: as the end of the
                # event from the previous day and the beginning of the
                # event on this day

                push @occur, FIRSTDAY
                    unless $recur_end->compare_date
                        (-WITH_OBJECT => $range_start) < GREATER;

                push @occur, LASTDAY if $already_started;
                $already_started = 1; #  now started for sure
            } else {
                warn "daily recurrent event cannot overlap on itself: $days_span";
            }
            # store it if overlaps (must clone the object so we can use it later)
            push @dates,[$range_start->clone,\@occur] if @occur;
            $range_start->add_delta_ymd(-DAYS => 1); # add one day
        }

    } elsif ($recur_interval == WEEK) {

        my $days = $range_start->days_between(-WITH_OBJECT => $event_start);
        # propogate fast to the first occurence of the event within
        # the range (if at all, the week event might skip over the
        # range which itself is shorter than week)
        if ($days > 7) {
            my $weeks = int ($days / 7);
            $weeks += 1 if $days % 7; # unless there is exactly n*7 days
            $event_start->add_delta_ymd(-DAYS => $weeks*7); # add $week days
            $days -= $weeks*7;
        }

        if ($days <= 0) {
            # if the event goes inside the range, adjust the range start
            $range_start = $event_start;
        }

        # E::dumper("test: $days",$event_start->dump,$range_start->dump,$range_end->dump);

        my $count = $days > 0 ? $days : 0;
        # go from range_start to range_end and return all the dates in between
        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER) {
            $count++;

            # $day: 1..7 (inside the week span)
            my $day = $count % 7 ? $count % 7 : 7;
            if ($day <= $days_span) {
                my @occur = ();
                if ($days_span == 1) {
                    # all events here start and end on the same day: hence ONEDAY
                    push @occur, ONEDAY;
                } elsif ($days_span <= 7) {
                    # the same date might appear twice: as the end of the
                    # event from the previous day and the beginning of the
                    # event on this day

                    # META: test an event starting at the first day
                    # and ends at the last day and it's recurring
                    # weekly
                    if ($day == 1) {
                        push @occur, FIRSTDAY;
                    } elsif ($day == $days_span) {
                        push @occur, LASTDAY;
                    } else {
                        push @occur, MIDDLEDAY;
                    }

                } else {
                    warn "weekly recurrent event cannot overlap on itself: $days_span";
                }
                # store it if overlaps (must clone the object so we can use it later)
                push @dates,[$range_start->clone,\@occur] if @occur;
            }

            $range_start->add_delta_ymd(-DAYS => 1); # add one day
        }

    } elsif ($recur_interval == MONTH) {

        my $orig_mday = $event_start->mday;

        # skip months that are before the range (ideally should be as
        # WEEK case, but a month is not always of the same length, so
        # we have to iterate)
        while ($event_end->compare_date(-WITH_OBJECT => $range_start) < EQUAL){
            $event_start = add_one_month($event_start,$orig_mday);
            $event_end = $event_start->clone();
            $event_end->add_delta_ymd(-DAYS => $exact_days_between); # adjust the event_end
        }

        my $days = $range_start->days_between(-WITH_OBJECT => $event_start);

        if ($days <= 0) {
            # if the event goes inside the range, adjust the range start
            $range_start = $event_start;
        }

        # E::dumper("test: $days",$event_start->dump,$range_start->dump,$range_end->dump);

        my $count = $days > 0 ? $days : 0;
        # go from range_start to range_end and return all the dates in between
        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER) {
            $count++;

            # $day (inside the year span)
            my $day = $count;
            if ($day <= $days_span) {
                my @occur = ();
                if ($days_span == 1) {
                    # all events here start and end on the same day: hence ONEDAY
                    push @occur, ONEDAY;
                } elsif ($days_span <= 31) {
                    # the same date might appear twice: as the end of the
                    # event from the previous day and the beginning of the
                    # event on this day
                    if ($day == 1) {
                        push @occur, FIRSTDAY;
                    } elsif ($day == $days_span) {
                        push @occur, LASTDAY;
                    } else {
                        push @occur, MIDDLEDAY;
                    }

                } else {
                    warn "yearly recurrent event cannot overlap on itself: $days_span";
                }
                # store it if overlaps (must clone the object so we can use it later)
                push @dates,[$range_start->clone,\@occur] if @occur;
            } else {
                # out of the event, need to move to the next occurence
                # of the event within the given range. This of course
                # assumes, that days_span is less than 28 days (just
                # to be sure), need to validate this when accepting
                # the events settings

                # move the dates by $count days back, so we can jump one month
                my $trace_back = $days > 0 ? $days + $count : $count;
                $event_start->add_delta_ymd(-DAYS => -$trace_back);

                # move the range and event starts one month forward
                $range_start = add_one_month($range_start,$orig_mday);

                # adjust the range start
                $event_start = $range_start->clone();

                # reset the days counter
                $count = 0;

                # no need to increment one day, we have already jumped
                # to the beginning of the next event if any
                next;
            }

            $range_start->add_delta_ymd(-DAYS => 1); # add one day
        }

    } elsif ($recur_interval == YEAR) {

        # skip years that are before the range (ideally should be as
        # WEEK case, but year is not always 365, so we have to
        # iterate)
        while ($event_end->compare_date(-WITH_OBJECT => $range_start) < EQUAL){
            $event_start->add_delta_ymd(-YEARS => 1); # add one year
            $event_end->add_delta_ymd  (-YEARS => 1); # add one year
        }

        my $days = $range_start->days_between(-WITH_OBJECT => $event_start);

        if ($days <= 0) {
            # if the event goes inside the range, adjust the range start
            $range_start = $event_start;
        }
        # E::dumper("test: $days",$event_start->dump,$range_start->dump,$range_end->dump);

        my $count = $days > 0 ? $days : 0;
        # go from range_start to range_end and return all the dates in between
        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER) {
            $count++;

            # NOTE: the following assumes that the requested range
            # will be never longer than one year.

            # $day (inside the year span)
            my $day = $count;
            if ($day <= $days_span) {
                my @occur = ();
                if ($days_span == 1) {
                    # all events here start and end on the same day: hence ONEDAY
                    push @occur, ONEDAY;
                } elsif ($days_span <= 364 ) {
                    # META: the same date might appear twice: as the
                    # end of the event from the previous day and the
                    # beginning of the event on this day: this is
                    # currently not handled due to the high
                    # unlikelyhood of this when the recurrency is one
                    # year.
                    if ($day == 1) {
                        push @occur, FIRSTDAY;
                    } elsif ($day == $days_span) {
                        push @occur, LASTDAY;
                    } else {
                        push @occur, MIDDLEDAY;
                    }
                } else {
                    warn "yearly recurrent event cannot overlap on itself: $days_span";
                }
                # store it if overlaps (must clone the object so we can use it later)
                push @dates,[$range_start->clone,\@occur] if @occur;
            }

            $range_start->add_delta_ymd(-DAYS => 1); # add one day
        }

    } else {
        # do nothing
    }

    return \@dates;

}


# accepts a date object and adds one month to it performing a correct
# month incrementing.  making sure to preserve the original start day
# across all months, and lower it only when some month is shorter than
# this day.  It uses the correct day for the next month (note: mon 1
# == January) (leap years are taken into account by the used datetime
# class).
#
# returns the updated object
##################
sub add_one_month{
    my ($event_start,$orig_mday) = @_;
    #E::dumper($event_start->dump);
    # add month
    my $next_month_last_date_obj = $event_start->next_month_last_date;
    my $days_in_next_month = $next_month_last_date_obj->days_in_month;
    my $delta_days = $days_in_next_month - $orig_mday;
    # is original mday is possible in the next month (e.g. 30
    # is not possible in February)
    if ($delta_days >= 0) {
        # local $Class::Date::RANGE_CHECK = 0;
        $event_start->add_delta_ymd(-MONTHS => 1);
        # force the original mday, (where prev month shrinked
        # it), but instead of checking we just force it, since
        # we know that orig_mday is possible
        $event_start->mday(-VALUE=> $orig_mday);
    } else {
        $event_start = $next_month_last_date_obj;

    }

    #E::dumper($event_start->dump);

    return $event_start;
}








1;
__END__






## This functions expects these named arguments:
##
## -SELECTED_DATE - the selected date
##
## -DATETIME_CONFIG_PARAMS - the datetime config params (forwarded)
##
## -RA_DATA: an array of events for a given day. Where each event has to
## have at least the following fields: starting and the ending date and
## time (where we don't care about the day) and the subject of the
## event.
##
## -RA_HOURS: a ref to an array with a range of hours to construct the
## matrix with.
##
## This function returns two arguments:
##
## out-1. a ref to a 2D matrix where the rows are denominated by hours
## and columns by events. There are two and more columns if two or more
## events happen overlap within the same hour. Note that if there is an
## event 09:00-09:30 and 09:31-10:00, because of HTML limitations these
## two event are considered to be overlapping and will consume two
## columns.
##
##   each cell in this matrix, has either:
##
##  undef  -- an empty cell
##  {}     -- record continues from the previous row
##  {note=>...,rowspan=>...}
##         -- record is starting in this cell
##            o 'note' includes the content to be printed in the cell
##            o 'rowspan' specifies for how many rows the event spawns
##
## out-2. the last column number in the matrix (assuming that the first
## column is counted as zero)
##
##
## The algorithm for building the matrix
##
## 1. Go through all entries and stack all the entries into a hash,
##    where those starting at the same hour, will be placed into the
##    same entry of the hash (as a list). Handle the spanning
##    non-recurrent events and adjust the start and end hours according
##    to:
##    - use the start hour and the hour of the end of the day for the
##      first day in the span
##    - use the end hour and the hour of the beginning of the day for
##      the last day in the span
##    - use all working hours if it's none from the above
##
## 2. sort the entries within the same hour by the event start_min!
##
## 3. Go through the hours:
##
##   for 8..23 (use the passed 'hours' array)
##     * go through all entries for the given hour and insert them into
##       the matrix one by one:
##         o if the event starts at the hour of the cell -- assign a
##           ref to the hash into the current cell. (see above for the
##           content of the hash)
##         o if the event extends beyond this hour -- fill other cells
##           in the same column hours with {} (to indicate that the
##           cell is occupied)
##         o empty cells will be undefs.
##    * figure out the max overlap width on the way (at the end of
##      processing of all the events starting at the same hour)
##
###########################
#sub GetDataForSelectedDay{
#    my $self = shift;
#    my $data;
#    ($data, @_) = _rearrangeAsHash([-SELECTED_DATE,-DATETIME_CONFIG_PARAMS,-RA_DATA,-RA_HOURS],
#                                   [-SELECTED_DATE,-DATETIME_CONFIG_PARAMS,-RA_DATA,-RA_HOURS],@_);
#    _dieIfRemainingParamsExist(@_);

#    my $selected_date   = $data->{-SELECTED_DATE};
#    my $datetime_config = $data->{-DATETIME_CONFIG_PARAMS};
#    my $ra_data         = $data->{-RA_DATA};
#    my $ra_hours        = $data->{-RA_HOURS};

#    # For the reference to the comment see the algorithm above!

#    my $selected = Extropia::Core::DateTime::create
#            (
#             @$datetime_config,
#             -DATETIME   => $selected_date,
#            );

#    # alg-1
#    my %by_hour = ();
#    for my $event (@$ra_data) {
#        my $start = Extropia::Core::DateTime::create
#            (
#             @$datetime_config,
#             -DATETIME   => $event->{start_date},
#            );
#        my $end = Extropia::Core::DateTime::create
#            (
#             @$datetime_config,
#             -DATETIME   => $event->{end_date},
#            );
#        my ($s_date) = $start->get(-FORMAT=>"%Y%m%d");
#        my ($e_date) =   $end->get(-FORMAT=>"%Y%m%d");
#        my ($s_hour,$s_min) = ($start->hour,$start->min);
#        my ($e_hour,$e_min) = ($end->hour,  $end->min);

#        my $res = $start->compare_date(-WITH_OBJECT => $end);
#        if ($res == EQUAL) {
#            # an event starting and ending at the same day (non
#            # spanning event)
#            $event->{s_hour} = $s_hour;
#            $event->{s_min}  = $s_min;
#            $event->{e_hour} = $e_hour;
#            $event->{e_min}  = $e_min;
#        } else {
#            # a spanning event, need to adjust hours
#            my $s_res = $selected->compare_date(-WITH_OBJECT => $start);
#            my $e_res = $selected->compare_date(-WITH_OBJECT => $end);
#            if ($s_res == EQUAL) {
#                # the first day of the spanning event
#                $event->{s_hour} = $s_hour;
#                $event->{s_min}  = $s_min;
#                $event->{e_hour} = $ra_hours->[-1] + 1;
#                $event->{e_min}  = 0;
#            } elsif ($e_res == EQUAL) {
#                # the last day of the spanning event
#                $event->{s_hour} = $ra_hours->[0];
#                $event->{s_min}  = 0;
#                $event->{e_hour} = $e_hour;
#                $event->{e_min}  = $e_min;
#            } else {
#                # non-first and non-last day of the spanning event
#                $event->{s_hour} = $ra_hours->[0];
#                $event->{s_min}  = 0;
#                $event->{e_hour} = $ra_hours->[-1] + 1;
#                $event->{e_min}  = 0;
#            }
#        }

#        #print STDERR $event->{id},": $s_hour:$s_min $e_hour:$e_min\n";

#        push @{ $by_hour{ $event->{s_hour} } }, $event;
#    }

#    # alg-2
#    $by_hour{$_} = [sort {$a->{s_min} <=> $b->{s_min}} @{ $by_hour{$_} }]
#        for keys %by_hour;

#    # alg-3
#    my %data = ();
#    my $last_col = 0;
#    for my $hour (@$ra_hours) {
#        my $col = 0;
#        next unless $by_hour{$hour};
#        for my $event (@{ $by_hour{$hour} }){
#            # find the next empty cell
#            $col++ while $data{$hour}{$col};

#            my $row_span = 1;
#            my $next_hour = $hour;
#            unless ($event->{e_hour} == $hour){
#                $next_hour += 1;
#                # mark the cells in the following column if the event
#                # is extending into the next hour
#                while ($next_hour < $event->{e_hour} or 
#                       ($next_hour == $event->{e_hour} and $event->{e_min} > 0)
#                      ){
#                    $data{$next_hour++}{$col} = {}; # mark that the cell is taken
#                    $row_span++;
#                }
#            }

#            # construct the note:
#            my $note = '';
#            # if the event doesn't start and finish at the round hour,
#            # we have to specify the exact beginning and ending time
#            $note .= sprintf " %02d:%02d-%02d:%02d",
#                $event->{s_hour},$event->{s_min},
#                $event->{e_hour},$event->{e_min}
#                    unless $event->{s_min} == 0 and $event->{e_min} == 0;

#            $note .= " ".$event->{subject};
#            $note .= " (".$event->{location}.")" if $event->{location};

#            # fill the cell with start at this hour
#            $data{$hour}{$col} = {
#                                  note    => $note,
#                                  rowspan => $row_span,
#                                  record_id => $event->{record_id},
#                                 };
#        }

#        # calculate the max cols width
#        $last_col = $col if $col > $last_col;
#    }

##    print STDERR "last_col $last_col\n";
##    # debug: prints the matrix
##    for my $hour (@$ra_hours) {
##        printf STDERR "%02d: ",$hour;
##        for my $col (0..$last_col){
##            local $_ = $data{$hour}{$col};
##            print (STDERR ". ") && next unless ref $_ and ref $_ eq 'HASH';
##            print (STDERR "O ") && next if %$_;
##            print (STDERR "# ") && next;
##        }
##        print STDERR "\n";
##    }

#    return (\%data,$last_col);

#}




## gets * the start and the end of the range to check
##      * the start and the end of the recurrent event
##      * recurrency interval
##
## returns: a ref to a list of dates ("%Y-%m-%d") following within the
##          requested range
##
##########################################
#sub GetOverlappingDatesForRecurrentEvents{
#    my $self = shift;
#    my $data;
#    ($data, @_) = _rearrangeAsHash
#        ([-DATETIME_CONFIG_PARAMS,
#          -RANGE_START_DATE,
#          -RANGE_END_DATE,
#          -RECUR_START_DATE,
#          -RECUR_END_DATE,
#          -RECUR_INTERVAL,
#         ],
#         [-DATETIME_CONFIG_PARAMS,
#          -RANGE_START_DATE,
#          -RANGE_END_DATE,
#          -RECUR_START_DATE,
#          -RECUR_END_DATE,
#          -RECUR_INTERVAL,
#         ],
#         @_
#        );
#    _dieIfRemainingParamsExist(@_);

#    my $datetime_config  = $data->{-DATETIME_CONFIG_PARAMS};
#    my $range_start_date = $data->{-RANGE_START_DATE};
#    my $range_end_date   = $data->{-RANGE_END_DATE};
#    my $recur_start_date = $data->{-RECUR_START_DATE};
#    my $recur_end_date   = $data->{-RECUR_END_DATE};
#    my $recur_interval   = $data->{-RECUR_INTERVAL};

#    # check that the event is indeed recurrent
#    return [] unless $recur_interval && $recur_interval != NONE;

#    my $range_start = Extropia::Core::DateTime::create
#        (@$datetime_config,-DATETIME   => $range_start_date);
#    my $range_end = Extropia::Core::DateTime::create
#        (@$datetime_config,-DATETIME   => $range_end_date);
#    my $recur_start = Extropia::Core::DateTime::create
#        (@$datetime_config,-DATETIME   => $recur_start_date);
#    my $recur_end = Extropia::Core::DateTime::create
#        (@$datetime_config,-DATETIME   => $recur_end_date);

#    # in case where the recurrent event starts after the range's start,
#    # shorten the range to start from this later date.
#    $range_start = $recur_start 
#        if $range_start->compare_date(-WITH_OBJECT => $recur_start) == LESS;

#    # in case where the recurrent event ends before the range's end,
#    # shorten the range to end at this earlier date.
#    $range_end = $recur_end 
#        if $range_end->compare_date(-WITH_OBJECT => $recur_end) == GREATER;

##    print STDERR "Range: ",$range_start->get(-FORMAT => "%Y-%m-%d"),
##        " - ",$range_end->get(-FORMAT => "%Y-%m-%d"),"\n";
##    print STDERR "Reccu: ",$recur_start->get(-FORMAT => "%Y-%m-%d"),
##        " - ",$recur_end->get(-FORMAT => "%Y-%m-%d"),"\n";
##    print STDERR "Reccurency: $recur_interval \n";

#    my @dates = ();

#    if ($recur_interval == DAY) {

#        # go from range_start to range_end and return all the dates in between
#        while ($range_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
#            push @dates, $range_start->get(-FORMAT => "%Y-%m-%d");
#            $range_start->add_delta_ymd(-DAYS => 1); # add one day
#        }

#    } elsif ($recur_interval == WEEK) {

#        my $days = $range_start->days_between(-WITH_OBJECT => $recur_start);
#        # propogate fast to the first occurence of the event within
#        # the range (if at all, the week event might skip over the
#        # range of one day)
#        if ($days > 0) {
#            my $weeks = int ($days / 7);
#            $weeks += 1 if $days % 7; # unless there is exactly n*7 days
#            $recur_start->add_delta_ymd(-DAYS => $weeks*7); # add $week days
#        }
#        # go from recur_start to range_end and return all the dates in
#        # between (where the weekly event happens)
#        while ($recur_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
#            push @dates, $recur_start->get(-FORMAT => "%Y-%m-%d");
#            $recur_start->add_delta_ymd(-DAYS => 7); # add one week
#        }

#    } elsif ($recur_interval == MONTH) {

#        # Algorithm:
#        # ---------
#        # Performing a correct month incrementing.  making sure to
#        # preserve the original start day across all months, and lower
#        # it only when some month is shorter than this day.  It uses
#        # the correct day for the next month (note: mon 1 == January)
#        # (leap years are taken into account by the used datetime
#        # class)
#        #
#        my $orig_mday = $recur_start->mday;
#        {
#            # out of the range: $recur_start > $range_end
#            last if $recur_start->compare_date(-WITH_OBJECT => $range_end) == GREATER;

#            # in range: $recur_start > $range_start (and !prev cond)
#            push @dates, $recur_start->get(-FORMAT => "%Y-%m-%d")
#                if $recur_start->compare_date(-WITH_OBJECT => $range_start) > LESS;

#            # add month
#            my $next_month_last_date_obj = $recur_start->next_month_last_date;
#            my $days_in_next_month = $next_month_last_date_obj->days_in_month;
#            my $delta_days = $days_in_next_month - $orig_mday;
#            # is original mday is possible in the next month (e.g. 30
#            # is not possible in February)
#            if ($delta_days >= 0) {
#                $recur_start->add_delta_ymd(-MONTHS => 1);
#                # force the original mday, (where prev month shrinked
#                # it), but instead of checking we just force it, since
#                # we know that orig_mday is possible
#                $recur_start->mday(-VALUE=> $orig_mday);
#            } else {
#                $recur_start = $next_month_last_date_obj;
#            }

#            redo; # try again with a new date
#        }


##        # skip months that are before the range (ideally should be as
##        # WEEK case, but a months is not always 30 days, so we have to
##        # iterate)
##        while ($recur_start->compare_date(-WITH_OBJECT => $range_start) < EQUAL){
##            $recur_start->add_delta_ymd(-MONTHS => 1); # add one year
##        }

##        # go from recur_start to range_end and return all the dates in
##        # between (where the monthly event happens)
##        while ($recur_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
##            push @dates, $recur_start->get(-FORMAT => "%Y-%m-%d");
##            $recur_start->add_delta_ymd(-MONTHS => 1); # add one year
##        }

#    } elsif ($recur_interval == YEAR) {

#        # skip years that are before the range (ideally should be as
#        # WEEK case, but year is not always 365, so we have to
#        # iterate)
#        while ($recur_start->compare_date(-WITH_OBJECT => $range_start) < EQUAL){
#            $recur_start->add_delta_ymd(-YEARS => 1); # add one year
#        }

#        # go from recur_start to range_end and return all the dates in
#        # between (where the yearly event happens)
#        while ($recur_start->compare_date(-WITH_OBJECT => $range_end) < GREATER){
#            push @dates, $recur_start->get(-FORMAT => "%Y-%m-%d");
#            $recur_start->add_delta_ymd(-YEARS => 1); # add one year
#        }

#    } else {
#        # do nothing
#    }

#    return \@dates;

#}







## This function accepts the datetime_config, the currently
## selected_date, the recurring event record's start_date and
## recur_interval as arguments and returns 0 if selected_date doesn't
## overlap with the recurring event, or 1 if it does
##
## see the comments in the code for particular to each interval
## decision making
##
## note this function *assumes* that:
## $start_date <= $selected_date <= $recur_until_date
## if $selected_date is not in this range, undefined behavior may occur
##
#############################################
#sub RecurrentEventOverlapsWithSelectedDate{
#    my $self = shift;
#    my $data;
#    ($data, @_) = _rearrangeAsHash
#        ([-DATETIME_CONFIG_PARAMS,
#          -SELECTED_DATE,
#          -START_DATE,
#          -RECUR_INTERVAL,
#         ],
#         [-DATETIME_CONFIG_PARAMS,
#          -SELECTED_DATE,
#          -START_DATE,
#          -RECUR_INTERVAL,
#         ],
#         @_
#        );
#    _dieIfRemainingParamsExist(@_);

#    my $datetime_config = $data->{-DATETIME_CONFIG_PARAMS};
#    my $selected_date   = $data->{-SELECTED_DATE};
#    my $start_date      = $data->{-START_DATE};
#    my $recur_interval  = $data->{-RECUR_INTERVAL};

#    # check that the event is indeed recurrent
#    return unless $recur_interval && $recur_interval != NONE;

#    my $selected_date_obj = Extropia::Core::DateTime::create
#        (
#         @$datetime_config,
#         -DATETIME   => $selected_date,
#        );

#    my $start_date_obj = Extropia::Core::DateTime::create
#        (
#         @$datetime_config,
#         -DATETIME   => $start_date,
#        );

#    if ($recur_interval == DAY) {
#        # Algorithm:
#        # ---------
#        # increment start_date by one day while start_date <= selected_date
#        # return 1 if start_date == selected_date
#        # return 0 otherwise
#        {
            
#            my $res = $selected_date_obj->compare_date(-WITH_OBJECT => $start_date_obj);
##print STDERR 
##    "selected_date: ", 
##    $selected_date_obj->get(-FORMAT => "%Y-%m-%d"),
##    ", start_date: ", 
##    $start_date_obj->get(-FORMAT => "%Y-%m-%d"),
##    " => $res\n";
#            return 1 if $res == 0;  # the same as selected date
#            return 0 if $res == -1; # we passed over the selected date
#            $start_date_obj->add_delta_ymd(-DAYS => 1); # add one day
#            redo; # try again with a new date
#        }

#    } elsif ($recur_interval == WEEK) {

#        # Algorithm:
#        # ---------
#        # increment start_date by one week while start_date <= selected_date
#        # return 1 if start_date == selected_date
#        # return 0 otherwise
#        {
#            my $res = $selected_date_obj->compare_date(-WITH_OBJECT => $start_date_obj);
#            return 1 if $res == 0;  # the same as selected date
#            return 0 if $res == -1; # we passed over the selected date
#            $start_date_obj->add_delta_ymd(-DAYS => 7); # add one week
#            redo; # try again with a new date
#        }
#    } elsif ($recur_interval == MONTH) {

#        # Algorithm:
#        # ---------
#        # increment start_date by one month while start_date <= selected_date
#        # return 1 if start_date == selected_date
#        # return 0 otherwise

#        # Performing a correct month incrementing.  making sure to
#        # preserve the original start day across all months, and lower
#        # it only when some month is shorter than this day.  It uses
#        # the correct day for the next month (note: mon 1 == January)
#        # (leap years are taken into account by the used datetime
#        # class)
#        #
#        my $orig_mday = $start_date_obj->mday;
#        {
#            my $res = $selected_date_obj->compare_date(-WITH_OBJECT => $start_date_obj);
##print STDERR 
##    "selected_date: ", 
##    $selected_date_obj->get(-FORMAT => "%Y-%m-%d"),
##    ", start_date: ", 
##    $start_date_obj->get(-FORMAT => "%Y-%m-%d"),
##    " => $res\n";
#            return 1 if $res == 0;  # the same as selected date
#            return 0 if $res == -1; # we passed over the selected date

#            my $next_month_last_date_obj = $start_date_obj->next_month_last_date;
#            my $days_in_next_month = $next_month_last_date_obj->days_in_month;
#            my $delta_days = $days_in_next_month - $orig_mday;
#            # is original mday is possible in the next month (e.g. 30
#            # is not possible in February)
#            if ($delta_days >= 0) {
#                $start_date_obj->add_delta_ymd(-MONTHS => 1);
#                # force the original mday, (where prev month shrinked
#                # it), but instead of checking we just force it, since
#                # we know that orig_mday is possible
#                $start_date_obj->mday(-VALUE=> $orig_mday);
#            } else {
#                $start_date_obj = $next_month_last_date_obj;
#            }

#            redo; # try again with a new date
#        }

#    } elsif ($recur_interval == YEAR) {

#        # Algorithm:
#        # ---------
#        # increment start_date by one year while start_date <= selected_date
#        # return 1 if start_date == selected_date
#        # return 0 otherwise
#        {
#            my $res = $selected_date_obj->compare_date(-WITH_OBJECT => $start_date_obj);
#            return 1 if $res == 0;  # the same as selected date
#            return 0 if $res == -1; # we passed over the selected date
#            $start_date_obj->add_delta_ymd(-YEARS => 1); # add one year
#            redo; # try again with a new date
#        }

#    } else {
#        # do nothing
#    }

#    return 0;
#}
