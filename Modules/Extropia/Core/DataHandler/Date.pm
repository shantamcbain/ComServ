#$Id: Date.pm,v 1.3 2001/08/31 10:12:21 gozer Exp $
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

####################################################
#
# Extropia::Core::DataHandler::Date
#
####################################################
package Extropia::Core::DataHandler::Date;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.3 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;
            
    return {
        -IS_DATE       => [$self,\&isDate],
        -IS_VALID_DATE => [$self,\&isValidDate],
        -IS_VALID_TIME => [$self,\&isValidTime],
        -FORMAT_DATE   => [$self,\&formatDate],
        -UNTAINT_DATE  => [$self,\&untaintDate]
    };

} # getHandlerRules

#
# isDate checks if the field is a date. 
# If it doesn't use Date::Manip or Date::Calc
# Then it checks for an MM/DD/YYYY format where
# the separatos can be -,/,., and spaces
#
# If -NON_US_FORMAT is specified, the date comparison
# is done using DD/MM order instead.
#
# -USE_DATE_MANIP optionally loads and uses Date manip' date
# parser.
#
# -USE_DATE_CALC optionally loads and uses Date calc's date
# parse.
#
sub isDate {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-NON_US_FORMAT,
                     -USE_DATE_MANIP,-USE_DATE_CALC,-FIELD_NAME,
                     -ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field          = shift;
    $field = "" if (!defined($field));
    my $non_us_format  = shift || 0;
    my $use_date_manip = shift || 0;
    my $use_date_calc  = shift || 0;
    my $field_name     = shift || "unknown";
    my $error_msg      = shift || "%FIELD_NAME% field is not a valid date.";
    my $add_error      = shift;
    $add_error = 1 if (!defined($add_error));

    # Note that a null field is also considered a valid
    # date since it has not explicitly failed. 

    if ($field =~ /^\s*$/) {
        return 1;
    } 
    
    my ($day, $month, $year) = _parseDate(
            -FIELD_VALUE   => $field,
            -NON_US_FORMAT => $non_us_format,
            -USE_DATE_MANIP => $use_date_manip,
            -USE_DATE_CALC => $use_date_calc,
            );


    if ($year && $month && $day) {
        my $status = $self->isValidDate(
            -DAY   => $day,
            -MONTH => $month,
            -YEAR  => $year,
            -ADD_ERROR => 0
        );
        if ($status) {
            return 1;
        }
    }

    if ($add_error) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
    }
    return undef;

} # end of isDate

#
# isValidDate checks to see if the passed data contains a valid
# date.
# 
sub isValidDate {
    my $self = shift;
    @_ = _rearrange([-DAY, -MONTH, -YEAR, -DAY_NAME, -MONTH_NAME, 
            -YEAR_NAME, -YEAR_ERROR_MESSAGE,
            -MONTH_ERROR_MESSAGE, -DAY_ERROR_MESSAGE, -ADD_ERROR],
           [],@_);

    my $day   = shift;
    my $month = shift;
    my $year  = shift;
    my $day_name        = shift;
    my $month_name      = shift;
    my $year_name       = shift;
    my $year_error_msg  = shift || 
        "The date you passed does not have a %YEAR_NAME%.";
    my $month_error_msg = shift || 
        "The date you passed does not have a valid %MONTH_NAME%.";
    my $day_error_msg   = shift || 
        "The date you passed does not have a valid %DAY_NAME% for the %MONTH_NAME% and %YEAR_NAME%.";
    my $add_error       = shift;

    $add_error = 1 if (!defined($add_error));

# no date entered... use -IS_FILLED_IN to detect required fields.
    if (!$day && !$month && !$year) {
        return 1;
    }

    if (!$year) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage(
                    [-YEAR_NAME => $year_name],
                    [-YEAR      => $year],
                    $year_error_msg
                    )
                )
            );
        }
        return undef;
    }

    if (!$month || $month < 1 || $month > 12) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage(
                    [-MONTH_NAME => $month_name],
                    [-MONTH      => $month],
                    $month_error_msg
                    )
                )
            );
        }
        return undef;
    }
    

    my %month_day_map = (
            1  => 31, 2  => 28, 3  => 31, 4  => 30,
            5  => 31, 6  => 30, 7  => 31, 8  => 31,
            9  => 30, 10 => 31, 11 => 30, 12 => 31
            );

    $month =~ s/0//g;
    if (defined($day) && $day <= $month_day_map{$month} && $day >= 1) {
        return 1;
    }

# leap year is only in effect if
# year is divisible by 4. If this is the case then leap year occurs
# if year is also not divisible by 100 or is divisible by 100 and by 400.
    if (defined($day) && $month == 2 && $day == 29 && !($year % 4)) {
        if ($year % 100) { # not divisible by 100
            return 1;
        } elsif (!($year % 400)) { # is divisible by 400
            return 1;
        }
    }

    if ($add_error) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage(
                [-DAY_NAME => $day_name, -MONTH_NAME => $month_name,
                 -YEAR_NAME => $year_name],
                [-DAY => $day, -MONTH => $month, -YEAR => $year],
                $day_error_msg
                )
            )
        );
    }
    return undef;

} # end of isValidDate

# isValidTime checks to see if hte passed data contains a valid 
# time.
#
sub isValidTime {
    my $self = shift;
    @_ = _rearrange([-HOUR, -MINUTE, -AMPM, -HOUR_NAME, -MINUTE_NAME,
                     -AMPM_NAME,
                     -HOUR_ERROR_MESSAGE, -MINUTE_ERROR_MESSAGE,
                     -ADD_ERROR],
                     [],@_);

    my $hour             = shift;
    my $minute           = shift;
    my $ampm             = shift;
    my $hour_name        = shift;
    my $minute_name      = shift;
    my $ampm_name        = shift;
    my $hour_error_msg   = shift;
    if (!$hour_error_msg) {
        if ($ampm) {
            $hour_error_msg = 
                "The time you passed does not have an hour between 1 and 12.";
        } else { 
            $hour_error_msg = 
                "The time you passed does not have an hour between 0 and 23.";
        }
    }

    my $minute_error_msg = shift || "The time you passed does not have a minute between 0 and 59.";
    my $add_error        = shift;

    $add_error = 1 if (!defined($add_error));

# no time entered... use -IS_FILLED_IN to detect required fields.
    if (!$hour && !$minute) {
        return 1;
    }

    if ($ampm && ($hour < 1 || $hour > 12)) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage(
                    [-HOUR_NAME => $hour_name],
                    [-HOUR      => $hour],
                    $hour_error_msg
                    )
                )
            );
        }
        return undef;
    }

    if (!$ampm && ($hour < 0 || $hour > 23)) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage(
                    [-HOUR_NAME => $hour_name],
                    [-HOUR      => $hour],
                    $hour_error_msg
                    )
                )
            );
        }
        return undef;
    }


    if ($minute < 0 || $minute > 59) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage(
                    [-MINUTE_NAME => $minute_name],
                    [-MINUTE      => $minute],
                    $minute_error_msg
                    )
                )
            );
        }
        return undef;
    }

    return 1;

} # end of isValidTime

sub _parseDate {
    my $self = shift;
    @_ = _rearrange([
            -FIELD_VALUE,
            -NON_US_FORMAT,
            -USE_DATE_MANIP,
            -USE_DATE_CALC
            ],[],@_);

    my $field          = shift;
    $field = "" if (!defined($field));
    my $non_us_format  = shift || 0;
    my $use_date_manip = shift || 0;
    my $use_date_calc  = shift || 0;

    if ($use_date_manip) {
        require Date::Manip;
        if ($non_us_format) {
            Date::Manip::Date_Init("DateFormat=nonUS");
        }
        my $date = Date::Manip::ParseDate($field);
        if ($date) {
            ($day, $month, $year) =
                Date::Manip::UnixDate($date,"%y","%m","%d");
        }
    } 
    
    if ($use_date_calc) {
        require Date::Calc;
        if ($non_us_format) {
            ($year, $month, $day) = Date::Calc::Decode_Date_EU2($field);
        } else {
            ($year, $month, $day) = Date::Calc::Decode_Date_US($field);
        }
    }
    
    if (!$use_date_calc && !$use_date_manip) {
        if ($field =~ /(\d{1,2})[\/.\-\s]*(\d{1,2})[\/.\-\s]*(\d+)/) {
            if ($non_us_format) {
                $day   = $1;
                $month = $2;
                $year  = $3;
            } else {
                $month = $1;
                $day   = $2;
                $year  = $3;
            }
        } 
    } # End of my own date routine

    return ($day, $month, $year);

} # end of _parseDate

sub breakDateIntoDayMonthYear {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,
                     -DAY_FIELD,
                     -MONTH_FIELD,
                     -YEAR_FIELD,
                     -CGI_OBJECT,
                     -NON_US_FORMAT,
                     -USE_DATE_MANIP,-USE_DATE_CALC,-FIELD_NAME,
                     -ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field          = shift;
    $field = "" if (!defined($field));
    my $day_field      = shift || "";
    my $month_field    = shift || "";
    my $year_field     = shift || "";
    my $cgi            = shift || "";
    my $non_us_format  = shift || 0;
    my $use_date_manip = shift || 0;
    my $use_date_calc  = shift || 0;
    my $field_name     = shift || "unknown";
    my $error_msg      = shift || "%FIELD_NAME% field is not a valid date.";
    my $add_error      = shift;
    $add_error = 1 if (!defined($add_error));

    my ($day, $month, $year) = _parseDate(
            -FIELD_VALUE   => $field,
            -NON_US_FORMAT => $non_us_format,
            -USE_DATE_MANIP => $use_date_manip,
            -USE_DATE_CALC => $use_date_calc,
            );

    if ($day && $month && $year) {
        $cgi->param($day_field,$day);
        $cgi->param($month_field,$month);
        $cgi->param($year_field,$year);
    } else {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    } 

    return $field;

} # end of break date into day, month, year

sub combineDayMonthYearIntoDate {
    my $self = shift;


} # end of 

#
# formatDate takes a field, input format and output
# format and converts the field to the output date.
# 
# If the field is not in the right format, an error will
# be raised.
#
# Note: This method is dependent on Date::Manip
#
sub formatDate {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-OUTPUT_FORMAT,-INPUT_FORMAT_LIST,
                     -FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE,-OUTPUT_FORMAT],@_);

    my $field              = shift;
    $field = "" if (!defined($field));
    my $output_format      = shift || "";
    my $input_format_list  = shift || "";
    my $field_name = shift || "unknown";
    my $alt_msg    = shift || "%FIELD_NAME% field is not a valid date.";

    # stub in no change for now...
    if ($field) {
         return $field;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $alt_msg)  
           )
        );
        return undef;
    }

} # end of formatDate

#
# untaintDate basically untaints a dates
# based on the data from isDate and then
# makes sure only date characters are 
# in the date and therefore no shell 
# meta characters
#
# This method is a little bit different
# in that you are expected to pass a FORMAT
# that the date is expected to be in by default
# so that the routine does not have to guess.
#
sub untaintDate {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,
            -NON_US_FORMAT,-USE_DATE_MANIP,-USE_DATE_CALC,
            -FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE,-FORMAT],@_);

    my $field          = shift;
    $field = "" if (!defined($field));
    my $non_us_format  = shift || 0;
    my $use_date_manip = shift || 0;
    my $use_date_calc  = shift || 0;
    my $field_name     = shift || "unknown";
    my $error_msg      = shift || "%FIELD_NAME% field is not a valid date.";

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # if the isXXXX method has a more stringent way of
    # untainting then we check this as well as a double
    # check.
    #
    # regex: only whitespace, word, -, /, : and , allowed
    #
    if ($self->isDate(-FIELD_VALUE    => $field,
                      -NON_US_FORMAT  => $non_us_format,
                      -USE_DATE_MANIP => $use_date_manip,
                      -USE_DATE_CALC  => $use_date_calc,
                      -ADD_ERROR => 0) &&
        $field =~ /^\s*([\s\w\-\/:.,]*)\s*$/) {
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintDate

1;
