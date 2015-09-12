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

package Extropia::Core::DateTime::ClassDate;

use vars qw($VERSION @ISA);
$VERSION = "1.0";
@ISA = qw(Extropia::Core::DateTime);

require Class::Date;
my $require = "1.0.5";
die "You need to install the $require version of Class::Date"
    if compare_version($Class::Date::VERSION, $require) < 0 ;

sub compare_version{
    my ($l, $r) = @_;
    $l =~ s/_/\./g;
    $r =~ s/_/\./g;
 
    my @l = split /\./, $l;
    my @r = split /\./, $r;
 
    my $mitems = @l > @r ? $#l : $#r;
    for (my $i = 0; $i <= $mitems; $i++) {
        my $result = ($l[$i] <=> $r[$i]) || ($l[$i] cmp $r[$i]);
        return $result unless $result == 0;
    }
    return 0;
}



$Class::Date::MONTH_BORDER_ADJUST = 1;
# print date("2001-01-31")+'1M'; # will print 2001-02-28
$Class::Date::RANGE_CHECK = 1;
# make sure that dates are valid like Feb, 31 is invalid

use strict;
use Extropia::Core::Base qw(
    _rearrange
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

use Carp;
#use Carp qw(verbose);

# constants used for dates comparison
use enum qw(LESS=-1 EQUAL=0 GREATER=1);

# indices into the object;
use enum qw(DATE TZ ERROR);

use vars qw(@attrs);
BEGIN{
    @attrs = qw(year month mday hour min sec);
}
use subs @attrs;

# my $obj = new(%config_args,-DATETIME => $date)
#
# $date can be of the following formats:
#    "%Y-%m-%d %H:%M:%S"
#    "%Y-%m-%d %H:%M"
#    "%Y-%m-%d"
#    "YYYYMMDDhhmmss"  #  mysql-style timestamp at least 14 digits
#    "973897262"       # A valid 32-bit integer unix timestamp
#    "now"             # now!
# in addition a reference to an array can be used
# [$year,$month,$day,$hour,$min,$sec];
#
# in case of failure to parse/set the date $obj->error() will return
# the error string. If everything is fine, $obj->error() will return
# undef.
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

    # initialize the object and set the error if it fails
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
    my $clone = bless [], ref $self;
    $clone->[DATE] = $self->[DATE]->clone;
    return $clone;
}


##################
sub _set_datetime{
    my $self = shift;
    my $date = shift || '';

    Carp::carp("no date specified") unless $date;

    my $error = undef;
    if ($date eq 'now') {
        $self->[DATE] = Class::Date::now();
    } else {
        $self->[DATE] = Class::Date->new($date);
    }

    # validate the date obj construction
    unless ($self->[DATE]) {
        $self->[ERROR] = $self->[DATE]->errstr;
    }
}


# return the date formatted according to strftime(3) format
########
sub get{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -FORMAT, ], [ -FORMAT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    return $self->[DATE]->strftime($data->{-FORMAT});
}


# the following code creates accessor methods for get/set of: 
# year, month, mday, hour, min and sec
## $obj->month() returns object's month: 1..12
## $obj->month(-VALUE => 11) sets object's month to 11
# the rest of the accessors use the same API
for my $attr (@attrs){
    no strict 'refs';
    *$attr = sub {
        my $self = shift;

        # get
        return $self->[DATE]->$attr() unless @_;

        #set
        my $data;
        ($data, @_) = _rearrangeAsHash([-VALUE],[],@_);
        _dieIfRemainingParamsExist(@_);
        $self->[DATE] = $self->[DATE]->set( $attr => $data->{-VALUE});
        return $self;
    }
}

sub month_string { shift->[DATE]->monthname();}

# returns 3-char-long month string
sub month_string_short { substr (shift->[DATE]->monthname(),0,3);}

# Monday = 1, Sunday = 7
sub wday {
    my $wday = shift->[DATE]->_wday(); 
    return $wday ? $wday : 7;
}
sub wday_string  { shift->[DATE]->wdayname();}

# return the date as a string
# DD Month YYYY
################
sub date_string { 
    my $date = shift->[DATE]; 
    return join " ", $date->mday,$date->monthname,$date->year;
}

# returns the wday (number) of the first day of the month (for the
# date object)
#
# assumes that Monday is the first day of the week: e.g. returns 1 if
# the months begins on Monday, 7 if Sunday.
######################
sub month_begin_wday {
    my $self = shift;
    my $wday = Class::Date->new([$self->year,$self->month, 1])->_wday;
    return $wday ? $wday : 7;
}

# how many days in the month of the date object
###################
sub days_in_month {
    my $self = shift;
    my $mon  = $self->month;
    my $year = $self->year;
    my $n_mon  = $mon == 12 ? 1 : $mon + 1;
    my $n_year = $mon == 12 ? $year + 1 : $year;

#    print STDERR "$n_year $n_mon ",(Class::Date->new( [$n_year,$n_mon,1] ) - '1D' )->mday,"\n";

    # go to the first day of the following month, subtract one day
    # (back to the current month), and get this day ==> gives the
    # number of days in the month.
    return (Class::Date->new( [$n_year,$n_mon,1] ) - '1D' )->mday;

}

# equivalent to get(-FORMAT => "%Y-%m-%d %H:%M:%S");
#########
sub dump{
    shift->get(-FORMAT => "%Y-%m-%d %H:%M:%S");
}

# returns the object of the previous month's first date
###########################
sub prev_month_first_date {
    my $self = shift;
    my $new_date = Class::Date->new([$self->year,$self->month, 1]) - '1M';
    my $obj = bless [], ref $self;
    $obj->[DATE] = $new_date;
    return $obj;
}

# returns the object of the month's first date
###########################
sub month_first_date {
    my $self = shift;
    my $new_date = Class::Date->new([$self->year,$self->month, 1]);
    my $obj = bless [], ref $self;
    $obj->[DATE] = $new_date;
    return $obj;
}

# returns the object of the next month's first date
###########################
sub next_month_first_date {
    my $self = shift;
    my $new_date = Class::Date->new([$self->year,$self->month, 1]) + '1M';
    my $obj = bless [], ref $self;
    $obj->[DATE] = $new_date;
    return $obj;
}

# returns the object of the prev month's last date
###########################
sub prev_month_last_date {
    my $self = shift;

    my $prev_month_first_date_obj = $self->prev_month_first_date();
    my $new_date = Class::Date->new([$prev_month_first_date_obj->year,
                                     $prev_month_first_date_obj->month,
                                     $prev_month_first_date_obj->days_in_month
                                    ]);
    my $obj = bless [], ref $self;
    $obj->[DATE] = $new_date;
    return $obj;
}

# returns the object of the next month's last date
###########################
sub next_month_last_date {
    my $self = shift;

    # next month's first date
    my $next_month_first_date_obj = $self->next_month_first_date();
    my $new_date = Class::Date->new([$next_month_first_date_obj->year,
                                     $next_month_first_date_obj->month,
                                     $next_month_first_date_obj->days_in_month
                                    ]);
    my $obj = bless [], ref $self;
    $obj->[DATE] = $new_date;
    return $obj;
}


# add a delta of years, months, days (any is optional)
# $obj->add_delta_ymd(
#        -YEARS  => $add_years,
#        -MONTHS => $add_months,
#        -DAYS   => $add_days,
#                    );
#
# the original object gets modified
#
# note that date("2001-01-31")+'1M' => 2001-02-28
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

    # add whatever we were asked to add
    $self->[DATE] = $self->[DATE] + [$delta_years,$delta_months,$delta_days];
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

    my %obj1 = $self->[DATE]->hash;
    my %obj2 = $data->{-WITH_OBJECT}->[DATE]->hash;
    # reset the time to 00:00:00
    @obj1{qw(hour min sec)} = (0,0,0);
    @obj2{qw(hour min sec)} = (0,0,0);

    my $obj1 = Class::Date->new(\%obj1);
    my $obj2 = Class::Date->new(\%obj2);
    my $diff = ($obj1 - $obj2)->day;
    return int($diff) + 1;
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

    my $obj1 = $self->[DATE];
    my $obj2 = $data->{-WITH_OBJECT}->[DATE];

    my $diff = ($obj1 - $obj2)->day;
    my $sign = $diff > 0 ? 1 : -1;
    $diff = abs $diff;
    my $add_day = $diff - int($diff) ? 1 : 0;
    return $sign * int($diff + $add_day);
}

# $end_date_obj->exact_days_between(-WITH_OBJECT => $start_date_obj);
# compares the dates of two objects, returns:
# a diff in days between $obj1 and $obj2 in days without rounding
#################
sub exact_days_between{
    my $self = shift;
    my $data;

    ($data, @_) = _rearrangeAsHash
        ( [ -WITH_OBJECT, ], [ -WITH_OBJECT, ], @_ );
    _dieIfRemainingParamsExist(@_);

    my $obj1 = $self->[DATE];
    my $obj2 = $data->{-WITH_OBJECT}->[DATE];

    return ($obj1 - $obj2)->day;
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

    my $date1 = $self->[DATE];
    my $date2 = $data->{-WITH_OBJECT}->[DATE];

    my $obj1 = Class::Date->new([$date1->year,$date1->mon,$date1->day]);
    my $obj2 = Class::Date->new([$date2->year,$date2->mon,$date2->day]);

#print STDERR "obj1 ",ref($obj1)," obj2 ",ref($obj2),"\n";

    return -1 if $obj1 < $obj2;
    return  0 if $obj1 == $obj2;
    return  1 if $obj1 > $obj2;
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

    my $datetime1 = $self->[DATE];
    my $datetime2 = $data->{-WITH_OBJECT}->[DATE];

    return -1 if $datetime1 < $datetime2;
    return  0 if $datetime1 == $datetime2;
    return  1 if $datetime1 > $datetime2;
}

#######################
### NON PUBLIC SUBS ###
#######################

# return all the datetime segments as an array
# ($year,$month,$day,$hour,$min,$sec) = $obj->_array;
##########
sub _array{
    return shift->[DATE]->array();
}


1;

__END__
