#$Id: Log.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Log;

# changed some stuff here
#

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver _assignDefaults);

use vars qw(@ISA $VERSION %SEVERITY @EXPORT_OK);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@EXPORT_OK = qw(EMERG ALERT CRIT ERR WARN INFO DEBUG);

#
# Log Severity Levels
#
sub EMERG () { 80; };
sub ALERT () { 70; };
sub CRIT  () { 60; };
sub ERR   () { 50; };
sub WARN  () { 40; };
sub NOTICE() { 30; };
sub INFO  () { 20; };
sub DEBUG () { 10; };

#
# Log Severity Descriptions 
#
%SEVERITY = (   
                EMERG()   =>  'EMERG',
                ALERT()   =>  'ALERT',
                CRIT()    =>  'CRIT', 
                ERR()     =>  'ERR',
                WARN()    =>  'WARN',
                NOTICE()  =>  'NOTICE',
                INFO()    =>  'INFO',
                DEBUG()   =>  'DEBUG' 
            );

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::Log", $type) or
        Carp::croak("Log type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

####################################################
#
# EXTERNAL LOG DRIVER METHODS
#
####################################################

# _baseInit does basic initialization for all log drivers...
sub _baseInit {
    my $self = shift;

    $self = _assignDefaults($self,
                            {-DEFAULT_SEVERITY => Extropia::Core::Log::INFO,
                             -LOG_FILTER_CHARS => 
                                ['\n','|','"',
                                ['/'=>'/']  #'%2F']
                                ]});

}

# _filterLogChars filters the stuff that should not go into a native
# log file format...
#
sub _filterLogChars {
    my $self = shift;

    my $string = shift;

    my $filter;
    foreach $filter (@{$self->{-LOG_FILTER_CHARS}}) {
        if (ref($filter) eq "ARRAY") {
            my $char    = $filter->[0];
            my $replace = $filter->[1];
            $string =~ s/\Q$char\E/$replace/g;
        } else {
            $string =~ s/\Q$filter\E/ /g;
        }
    }

    return $string;
}

#
# logError decodes an error object and then passes
# it to the standard log method for true logging.
#
sub logError {
    my $self = shift;
    @_ = _rearrange([-ERROR_OBJECT,
                     -MAP_CODE_TO_EVENT_ID,
                     -SEVERITY],
                     [-ERROR_OBJECT],@_);

    my $error_object         = shift;
    my $map_code_to_event_id = shift;
    my $severity             = shift;

    my @EVENT_PARAM    = (-EVENT => $error_object->getMessage());
    my @EVENT_ID_PARAM = ();
    my @SEVERITY_PARAM = ();

    if ($severity) {
        @SEVERITY_PARAM = (-SEVERITY => $severity);
    }

    if ($map_code_to_event_id && $error_object->getCode()) {
        @EVENT_ID_PARAM = (-EVENT_ID => $error_object->getCode());
    }

    $self->log(@SEVERITY_PARAM, @EVENT_PARAM, @EVENT_ID_PARAM);

} # end of logError

#
# _createLogEntry creates a log message behind the scenes for logging...
#
sub _createLogEntry {
    my $self = shift;

    @_ = _rearrange([-EVENT,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $event_id = shift || $self->{_default_event_id};

    my $log_format = $self->{-LOG_FORMAT};

    my $date_time            = localtime(time);
    my $event_log = "";

    my %month_to_value = (
            'Jan' => 1,
            'Feb' => 2,
            'Mar' => 3,
            'Apr' => 4,
            'May' => 5,
            'Jun' => 6,
            'Jul' => 7,
            'Aug' => 8,
            'Sep' => 9,
            'Oct' => 10,
            'Nov' => 11,
            'Dec' => 12
            );
            
    if (!defined($log_format)) {
        $event_log = $date_time . "|";
        if ($event_id) {
            $event_log .= $event_id . "|";
        }   
        if (ref($event) eq "ARRAY") {
            $event_log .= join("|", @$event);
        } else {
            $event_log .= $event;
        }
    } else {
        my $log_date_time = $date_time;
        my $number_log_date_time = $date_time;
        if ($date_time =~ /\w+\s+(\w+)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)/) {
            my $month = $1;
            my $day   = $2;
            my $year  = $6;
            my $hour  = $3;
            my $min   = $4;
            my $sec   = $5;
            my $numbermonth = $month_to_value{$month};
            $day = "0$day" if (length($day) < 2);
            $log_date_time = "$day/$month/$year:$hour:$min:$sec";
            $number_log_date_time = "$day/$numbermonth/$year:$hour:$min:$sec";
        }
        $log_format =~ s/\{DATE\}/$date_time/;
        $log_format =~ s/\{LOGDATE\}/$log_date_time/;
        $log_format =~ s/\{NUMBERLOGDATE\}/$number_log_date_time/;
        my %events;
        my $rh_defaults   = $self->{-LOG_FORMAT_DEFAULTS};
        my $default_field = $self->{-LOG_FORMAT_DEFAULT_FIELD};
        if (ref($event)) {
            %events = @$event;
        } else {
            $events{$default_field} = $event;
        }
        my $rh_events = \%events;
        if (defined($rh_defaults)) {
           $rh_events = _assignDefaults($rh_events,$rh_defaults); 
        }
        my $param;
        foreach $param (keys %$rh_events) {
            my $value = $rh_events->{$param};
            $log_format =~ s/\{$param\}/$value/;
        }
        $event_log .= $log_format;
    }

    return $event_log . "\n";

} # end of _createLogEntry

sub _getSeverityDescription {
    my $self = shift;
    @_ = _rearrange([-SEVERITY],[-SEVERITY],@_);

    my $severity = shift || Extropia::Core::Log::INFO;

    return $Extropia::Core::Log::SEVERITY{$severity};

} # end of _getSeverityDescription

sub log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift || $self->{-DEFAULT_SEVERITY};
    my $event_id = shift || $self->{-DEFAULT_EVENT_ID};

    if ($self->_checkSeverity(-SEVERITY => $severity)) {
        $self->_log(-EVENT    => $event,
                    -SEVERITY => $severity,
                    -EVENT_ID => $event_id);
    }

} # end of log

sub _checkSeverity {
    my $self = shift;
    @_ = _rearrange([-SEVERITY],[-SEVERITY],@_);

    my $severity = shift;
    my $disable_severity_list = $self->{-DISABLE_SEVERITY_LIST};
    my $enable_severity_list  = $self->{-ENABLE_SEVERITY_LIST};

    $self->_checkItem(-ITEM         => $severity,
                    -DISABLE_LIST => $disable_severity_list,
                    -ENABLE_LIST  => $enable_severity_list);

} # end of _checkSeverity

sub _checkItem {
    my $self = shift;
    @_ = _rearrange([-ITEM,-DISABLE_LIST,-ENABLE_LIST],
                    [-ITEM],@_);
    
    my $item         = shift;
    my $disable_list = shift;
    my $enable_list  = shift;

    my $log_this = 1;
    if ($disable_list &&
        $self->_doesListMatch(-ITEM => $item,
                              -LIST_TO_MATCH => $disable_list)) {
        $log_this = 0;
    } elsif ($enable_list &&
             !$self->_doesListMatch(-ITEM => $item,
                              -LIST_TO_MATCH => $enable_list)) {
        $log_this = 0;
    }
    return $log_this;

} # end of _checkItem

sub _doesListMatch {
    my $self = shift;
    @_ = _rearrange([-ITEM,-LIST_TO_MATCH],[-ITEM,-LIST_TO_MATCH],@_);

    my $item = shift;
    my $list = shift;

    my $matched = 0;
    my $list_item;
    foreach $list_item (@$list) {
        if ($list_item eq $item) {
            $matched = 1;
            last;
        }
    }
    return $matched; 

} # end of _doesListMatch

1;
