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

package Extropia::Core::DateTime::DateManip;

use vars qw($VERSION @ISA);
$VERSION = "1.0";
@ISA = qw(Extropia::Core::DateTime);

use Date::Manip ();

use strict;
use Extropia::Core::Base qw(
    _rearrange
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

# untaint PATH
$ENV{'PATH'} = '/bin:/usr/bin';

use Carp;
#use Carp qw(verbose);

# constants used for dates comparison
use enum qw(LESS=-1 EQUAL=0 GREATER=1);

# indices into the object;
use enum qw(DATE TZ ERROR);

use vars qw(%date_attrs %time_attrs);
BEGIN{
    %date_attrs = (year  => 'Y', 
                   month => 'm', 
                   mday  => 'd',
                  );
    %time_attrs = (hour  => 'H',
                   min   => 'M',
                   sec   => 'S',
                  );
}
use subs keys %date_attrs, %time_attrs;



#
# new(%config_args,-DATETIME => $date)
#
# $date can be of the following formats:
#    "%Y-%m-%d %H:%M:%S"
#    "%Y-%m-%d %H:%M"
#    "%Y-%m-%d"
#    "YYYYMMDDhhmmss"  #  mysql-style timestamp at least 14 digits
#    "now"             # now!
#    "973897262"       # A valid 32-bit integer unix timestamp
#
# in addition a reference to an array can be used
# [$year,$month,$day,$hour,$min,$sec];
#
# in case of failure to parse/set the date $obj->error() will return
# the error string. If everything is fine, $obj->error() will return
# undef.
#
#
####################
sub new {
    my $package = shift;
    my $data;
    ($data, @_) = _rearrangeAsHash
        (
         [
          '-TZ',
          '-DATETIME',
         ],
         [],
         @_
        );

    _dieIfRemainingParamsExist(@_);

    my $self = bless [], $package || ref $package;
    # META: handle timezone!
    # $self->[TZ]= defined $data->{'-TZ'} ? $data->{'-TZ'} : 'some default';

    # META: under persistent engine, $^T has to be set to the time of
    # the request, make sure to adjust this to whatever timezone/gmt
    # handling we go for.
    $^T = time;

    $self->_set_datetime($data->{-DATETIME});

    return $self;
}

# returns an error if set or undef
##########
sub error{
    return shift->[ERROR];
}

# deep copy clone
##########
sub clone{
    my $self = shift;
    my $secs = Date::Manip::UnixDate($self->[DATE],"%s");
    Date::Manip::ParseDateString("epoch $secs");
    my $new_date_obj = Date::Manip::ParseDateString("epoch $secs");
    my $clone = bless [], ref $self;
    $clone->[DATE] = $new_date_obj;
    return $clone;
}

##################
sub _set_datetime{
    my $self = shift;
    my $date = shift || '';

    Carp::carp("no date specified") unless $date;

    my $error = undef;
    if ($date eq 'now') {
        $self->[DATE] = Date::Manip::ParseDateString("today");
    }
    elsif (my $ref = ref $date) {
        if ($ref eq 'ARRAY') {
            $self->[DATE] = Date::Manip::ParseDateString
                (sprintf "%04d%02d%02d%02d%02d%02d",@$date);
        }
    }
    elsif ($date =~ /^\d+$/ && length($date) != 14) {
        # A valid 32-bit integer unix timestamp
        $self->[DATE] = Date::Manip::ParseDateString("epoch $date");
    }
    else {
        # try to parse the date format
        # META: in case of failure shouldn't die, but return the error
        $self->[DATE] = Date::Manip::ParseDateString($date);
    }
 
   # make sure that the date is valid
    $self->[ERROR] = "invalid date" unless $self->[DATE];

    return $error;
}


# return the date formatted according to strftime(3) format
########
sub get{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -FORMAT, ], [ -FORMAT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    return Date::Manip::UnixDate($self->[DATE],$data->{-FORMAT});
}


# the following code creates accessor methods for get/set of: year,
# month and mday
## $obj->month() returns object's month: 1..12
## $obj->month(-VALUE => 11) sets object's month to 11
# the rest of the accessors use the same API
for my $attr (keys %date_attrs){
    no strict 'refs';
    *$attr = sub {
        my $self = shift;

        # get (remove 0 formatting if any)
        return 0 + Date::Manip::UnixDate
            ($self->[DATE],"%".$date_attrs{$attr})
                unless @_;

        # set
        my $data;
        ($data, @_) = _rearrangeAsHash([-VALUE],[],@_);
        _dieIfRemainingParamsExist(@_);
        $self->[DATE] = Date::Manip::Date_SetDateField
            ($self->[DATE],$date_attrs{$attr},$data->{-VALUE});
        return $self;
    }
}



# the following code creates accessor methods for get/set of:
# hour, min and sec
## $obj->hour() returns object's hour: 0..23
## $obj->hour(-VALUE => 11) sets object's hour to 11
# the rest of the accessors use the same API
for my $attr (keys %time_attrs){
    no strict 'refs';
    *$attr = sub {
        my $self = shift;

        # get (remove 0 formatting if any)
        return 0 + Date::Manip::UnixDate
            ($self->[DATE],"%".$time_attrs{$attr})
                unless @_;

        # set
        my $data;
        ($data, @_) = _rearrangeAsHash([-VALUE],[],@_);
        _dieIfRemainingParamsExist(@_);

        my %time = ($attr => $data->{-VALUE});
        for (keys %time_attrs) {
            next if $time{$_};
            $time{$_} = 0 + Date::Manip::UnixDate
                ($self->[DATE],"%".$time_attrs{$_});
        }

        $self->[DATE] = Date::Manip::Date_SetTime
            ($self->[DATE],@time{qw(hour min sec)});
        return $self;
    }
}


sub month_string { Date::Manip::UnixDate(shift->[DATE],"%B")}

# returns 3 char long month string
########################
sub month_string_short { 
    substr Date::Manip::UnixDate(shift->[DATE],"%B"),0,3;
}

#  1 = Sunday
sub wday         { Date::Manip::UnixDate(shift->[DATE],"%w")}
sub wday_string  { Date::Manip::UnixDate(shift->[DATE],"%A")}

# return the date as a string
# DD Month_string YYYY
################
sub date_string { 
    my $string = Date::Manip::UnixDate(shift->[DATE],"%e %B %Y");
    $string =~ s/^\s//; # strip the space if DD < 10
    return $string;
}

# equivalent to get(-FORMAT => "%Y-%m-%d %H:%M:%S");
#########
sub dump{
    shift->get(-FORMAT => "%Y-%m-%d %H:%M:%S");
}


# returns the wday (number) of the first day of the month (for the
# date object)
#
# assumes that Monday is the first day of the week: e.g. returns 1 if
# the months begins on Monday, 7 if Sunday.
######################
sub month_begin_wday {
    shift->clone->mday(-VALUE => 1)->wday;
}

# how many days in the month of the date object
###################
sub days_in_month {
    my $self = shift;
    return Date::Manip::Date_DaysInMonth($self->month,$self->year);
}

# returns the object of the previous month's first date
###########################
sub prev_month_first_date {
    my $self = shift;
    my $mon  = $self->month;
    my $year = $self->year;
    my $clone = $self->clone;
    my $p_mon = $mon == 1 ? 12 : $mon - 1;
    $clone->month(-VALUE => $p_mon);
    $clone->year(-VALUE => $year-1) if $mon == 1;
    $clone->mday(-VALUE => 1);
    return $clone;
}

# returns the object of the month's first date
###########################
sub month_first_date {
    return shift->clone->mday(-VALUE => 1);
}

# returns the object of the next month's first date
###########################
sub next_month_first_date {
    my $self = shift;
    my $mon  = $self->month;
    my $year = $self->year;
    my $clone = $self->clone;
    my $n_mon = $mon == 12 ? 1 : $mon + 1;
    $clone->month(-VALUE => $n_mon);
    $clone->year(-VALUE => $year+1) if $mon == 12;
    $clone->mday(-VALUE => 1);
    return $clone;
}


# returns the object of the prev month's last date
###########################
sub prev_month_last_date {
    my $self = shift;
    my $mon  = $self->month;
    my $year = $self->year;
    my $clone = $self->clone;
    my $p_mon = $mon == 1 ? 12 : $mon - 1;
    $clone->month(-VALUE => $p_mon);
    $clone->year(-VALUE => $year-1) if $mon == 1;
    my $days_in_month = 
        Date::Manip::Date_DaysInMonth($clone->month,$clone->year);
    $clone->mday(-VALUE => $days_in_month);
    return $clone;
}

# returns the object of the next month's last date
###########################
sub next_month_last_date {
    my $self = shift;
    my $mon  = $self->month;
    my $year = $self->year;
    my $clone = $self->clone;
    my $n_mon = $mon == 12 ? 1 : $mon + 1;
    $clone->month(-VALUE => $n_mon);
    $clone->year(-VALUE => $year+1) if $mon == 12;
    my $days_in_month = 
        Date::Manip::Date_DaysInMonth($clone->month,$clone->year);
    $clone->mday(-VALUE => $days_in_month);
    return $clone;
}


# add a delta of years, months, days (any is optional)
# $obj->add_delta_ymd(
#        -YEARS  => $add_years,
#        -MONTHS => $add_months,
#        -DAYS   => $add_days,
#                    );
# the object gets modified
#
# returns the modified $obj, which makes it suitable for piping
# a->b->c
#
##################
sub add_delta_ymd{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -YEARS, -MONTHS, -DAYS, ], [ ], @_ );
    _dieIfRemainingParamsExist(@_);

    my $delta_years  =  $data->{-YEARS}  || 0;
    my $delta_months =  $data->{-MONTHS} || 0;
    my $delta_days   =  $data->{-DAYS}   || 0;

    my $delta_string = sprintf "%dY %dM %dD",
        $delta_years,$delta_months,$delta_days;

    my $new_date_obj = Date::Manip::DateCalc($self->[DATE],$delta_string);
    $self->[DATE] = $new_date_obj;
    return $self;
}






# $end_date_obj->days_span(-WITH_OBJECT => $start_date_obj);
# compares the dates of two objects, returns:
#
# a days span between two dates, based on the date and not time.  so if
# one date is today (at 23:59) and the other is tomorrow at (0:01) the
# span is 2 days.  if the two objects reside in the same date, the
# span is 1 day.
#################
sub days_span{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    # reset the time to 00:00:00
    my $date1 = Date::Manip::Date_SetTime($self->[DATE],                0,0,0);
    my $date2 = Date::Manip::Date_SetTime($data->{-WITH_OBJECT}->[DATE],0,0,0);
    my $delta = Date::Manip::DateCalc($date2,$date1);
    return Date::Manip::Delta_Format($delta,0,"%dd") + 1;
}

# $end_date_obj->days_between(-WITH_OBJECT => $start_date_obj);
# compares the dates of two objects, returns:
# a diff in days between $obj1 and $obj2 in full days
# the diff is rounded up to the ceiling (so 1.2 and 1.9 both rounded
# to 2 days)
#################
sub days_between{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    # reset the time to 00:00:00
    my $delta = Date::Manip::DateCalc($data->{-WITH_OBJECT}->[DATE],$self->[DATE]);
    my $diff  = Date::Manip::Delta_Format($delta,1,"%dt");
    my $sign = $diff > 0 ? 1 : -1;
    $diff = abs $diff;
    my $add_day = $diff - int($diff) ? 1 : 0;
    return $sign * int($diff + $add_day);
}


# $end_date_obj->exact_days_between(-WITH_OBJECT => $start_date_obj);
# compares the dates of two objects, returns:
# a diff in days between $obj1 and $obj2 in days without rounding
#
# currently it uses a precision of 10**-4
#################
sub exact_days_between{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    # reset the time to 00:00:00
    my $delta = Date::Manip::DateCalc($data->{-WITH_OBJECT}->[DATE],$self->[DATE]);
    return Date::Manip::Delta_Format($delta,4,"%dt");
}

# $obj1->compare_date(-WITH_OBJECT => $obj2);
# compares the dates (not the time!) of two objects, returns:
# -1 if $obj1 < $obj2
#  0 if $obj1 == $obj2
#  1 if $obj1 > $obj2
#################
sub compare_date{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    # clone
    my $date1 = $self->clone->[DATE];
    my $date2 = $data->{-WITH_OBJECT}->clone->[DATE];

    # reset time
    $date1 = Date::Manip::Date_SetTime($date1,0,0,0);
    $date2 = Date::Manip::Date_SetTime($date2,0,0,0);

    # compare
    return Date::Manip::Date_Cmp($date1,$date2);


}

# $obj1->compare_datetime(-WITH_OBJECT => $obj2);
# compares the datetime of two objects, returns:
# -1 if $obj1 < $obj2
#  0 if $obj1 == $obj2
#  1 if $obj1 > $obj2
#################
sub compare_datetime{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    # clone
    my $date1 = $self->clone->[DATE];
    my $date2 = $data->{-WITH_OBJECT}->clone->[DATE];

    # compare
    return Date::Manip::Date_Cmp($date1,$date2);
}


1;

__END__


