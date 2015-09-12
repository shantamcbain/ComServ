package WebCal::DisplayDayViewAction;

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
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::Action;
use Extropia::Core::DateTime;
use Extropia::Core::App::WebCal;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED,
        -APPLICATION_OBJECT,
        -AUTH_MANAGER_CONFIG_PARAMS,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -MAX_RECORDS_PER_PAGE,
        -REQUIRE_AUTH_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -SESSION_OBJECT,
        -LAST_RECORD_ON_PAGE,
        -SIMPLE_SEARCH_STRING,
        -SORT_DIRECTION,
        -SORT_FIELD1,
        -SORT_FIELD2,
        -DATETIME_CONFIG_PARAMS,
        -VALID_WORKING_HOURS,
        -DEFAULT_VIEW_MODE,
	-PRINT_MODE
           ],
            [
        -APPLICATION_OBJECT,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
        -DATETIME_CONFIG_PARAMS,
        -VALID_WORKING_HOURS,
        -DEFAULT_VIEW_MODE,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};
    my $default_view_mode = $params->{-DEFAULT_VIEW_MODE};

# the default action, so it's always executed if we get here

 if (!$cgi->param('DisplayMonthViewAction') && !$cgi->param('DisplayDayViewAction') && !$cgi->param('DisplayYearViewAction')){
    if($default_view_mode != Extropia::Core::App::WebCal::DAY) {
            return 0;
   }
 } elsif ( !$cgi->param('DisplayDayViewAction') ) {
            return 0;
 }
                                                       
    
    if ($params->{-REQUIRE_AUTH_FOR_SEARCHING_FLAG}) {
        if ($params->{-AUTH_MANAGER_CONFIG_PARAMS}) {
            my $auth_manager = Extropia::Core::AuthManager->create(@{$params->{-AUTH_MANAGER_CONFIG_PARAMS}})
                or die("Whoopsy!  I was unable to construct the " .
                       "Authentication object. " .
                       "Please contact the webmaster.");
            $auth_manager->authenticate();
        }
        else {
            die('You have set -REQUIRE_AUTH_FOR_SEARCHING_FLAG to 1 ' .
                ' in the application executable, but you have not ' .
                ' defined -AUTH_MANAGER_CONFIG_PARAMS in the ' .
                '@ACTION_HANDLER_ACTION_PARAMS array ' .
                'in the application executable. This action ' .
                ' cannot procede unless you do both.'
            );
        }
      }


    my $PrintMode = $cgi->param('mode');

    if ($cgi->param('mode')){
    $app->setNextViewToDisplay(
        -VIEW_NAME => 'PrintView',
    );  
  }else{
 $app->setNextViewToDisplay(
        -VIEW_NAME => 'DayView',
    );  
  }

    # today's data
    $app->setTodayData(-DATETIME_CONFIG_PARAMS => $params->{-DATETIME_CONFIG_PARAMS});

    my $datetime_config = $params->{-DATETIME_CONFIG_PARAMS};
    my $date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => $cgi->param('date') || 'now',
        );

    $app->setSelectedDateData(-DATE_OBJECT => $date_obj);

    # trying to get all the event possibly falling into the selected day
    # later check the search range

    # algorithm: 
    # (start_date <= 'selected_date 23:59' AND end_date >= 'selected_date 00:00')
    # or
    # (recur_interval > 0 AND start_date <= 'selected_date 23:59' AND recur_until_date >= selected_date)
    # 
    # this picks also recurrent events that might not happen today, we
    # need to delete those after the search is done

    my $selected_date = $date_obj->get(-FORMAT => "%Y-%m-%d");
    my @select = ();

    # normal selected day events
    push @select, 
        qq{start_date <= "$selected_date 23:59" AND end_date >= "$selected_date 00:00"};
    # recurring events
    push @select, 
        qq{recur_interval > 0 AND start_date <= "$selected_date 23:59" AND recur_until_date >= "$selected_date"};

    my $select = join ' OR ', map {"($_)"} @select;
#print STDERR "select $select\n";

    # set the search args
    $cgi->param('raw_search', $select);

    my @config_params = _rearrange([
        -BASIC_DATASOURCE_CONFIG_PARAMS
            ],
            [
            ],
        @{$params->{'-DATASOURCE_CONFIG_PARAMS'}}
    );

    my $datasource_config_params = shift (@config_params);

    if ($datasource_config_params) {
        my $record_set = $app->loadData((
            -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
            -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
            -KEY_FIELD                   => $params->{-KEY_FIELD},
            -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
            -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
            -RECORD_ID                   => $cgi->param('record_id') || "",
            -SORT_FIELD1                 => 'start_date',
#$params->{-SORT_FIELD1},
            -SORT_FIELD2                 => 'start_date',
#$params->{-SORT_FIELD2},
            -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
            -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
            -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING}, 
            -CGI_OBJECT                  => $params->{-CGI_OBJECT},
            -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
            -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
            -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG},
            -RETURN_RECORD_SET           => 1,
        ));

        my @columns_to_view = qw(record_id start_date end_date subject description
                                 location description recur_interval
                                 recur_until_date);
        # META: more fields to extract later on

        # META: next stage, need to remove any recurrent events
        # falling into this range, but not happening on the selected
        # day in the future, may be need to modify the query so it
        # won't fetch those in first place

        my $key_field = $params->{-KEY_FIELD};
        $record_set->moveFirst();

        my @days_data = ();
        my $ra_valid_working_hours = $params->{-VALID_WORKING_HOURS};
        
        while (!$record_set->endOfRecords()) {
            my $id = $record_set->getField($key_field);

#print STDERR "*** ID: $id\n";
            my %row = ();
            foreach my $field (@columns_to_view) {
                $row{$field} =  $record_set->getField($field);
                $row{$field} = '' unless defined $row{$field};
#print  STDERR "$field $row{$field}\n";
            }

            my $start = Extropia::Core::DateTime::create
                ( @$datetime_config,-DATETIME => $row{start_date});

            my $end = Extropia::Core::DateTime::create
                ( @$datetime_config,-DATETIME => $row{end_date});

            my $ra_overlap_dates = [];
            # get the dates when the event overlaps with the given month
            if ($row{recur_interval} and $row{recur_until_date}) {
                $ra_overlap_dates = $app->Events2DatesInRange
                    (
                     -DATETIME_CONFIG_PARAMS => $params->{-DATETIME_CONFIG_PARAMS},
                     -RANGE_START_DATE       => $selected_date,
                     -RANGE_END_DATE         => $selected_date,
                     -EVENT_START_DATE       => $row{start_date},
                     -EVENT_END_DATE         => $row{end_date},
                     -RECUR_END_DATE         => $row{recur_until_date},
                     -RECUR_INTERVAL         => $row{recur_interval},
                    );
            } else {
                # spanning or single day non-recurrent event
                $ra_overlap_dates = $app->Events2DatesInRange
                    (
                     -DATETIME_CONFIG_PARAMS => $params->{-DATETIME_CONFIG_PARAMS},
                     -RANGE_START_DATE       => $selected_date,
                     -RANGE_END_DATE         => $selected_date,
                     -EVENT_START_DATE       => $row{start_date},
                     -EVENT_END_DATE         => $row{end_date},
                     -RECUR_END_DATE         => $row{end_date},
                     -RECUR_INTERVAL         => Extropia::Core::App::WebCal::NONE,
                    );
            }

            my ($start_hour,$start_min) = ($start->hour,$start->min);
            my ($end_hour,$end_min)     = ($end->hour,  $end->min);

            for my $ref (@$ra_overlap_dates) {
                my ($date_obj,$ra_occur) = @$ref;
                #E::dumper($date_obj);

                for (@$ra_occur) {
                    my ($s_hour,$s_min,$e_hour,$e_min);
                    if ($_ == Extropia::Core::App::WebCal::ONEDAY) {
                        # starts and ends on this day
                        $s_hour = $start_hour;
                        $s_min  = $start_min;
                        $e_hour = $end_hour;
                        $e_min  = $end_min;
                    } elsif ($_ == Extropia::Core::App::WebCal::FIRSTDAY) {
                        # starts on this day
                        $s_hour = $start_hour;
                        $s_min  = $start_min;
                        $e_hour = $ra_valid_working_hours->[-1] + 1;
                        $e_min  = 0;
                    } elsif ($_ == Extropia::Core::App::WebCal::LASTDAY) {
                        # ends on this day
                        $s_hour = $ra_valid_working_hours->[0];
                        $s_min  = 0;
                        $e_hour = $end_hour;
                        $e_min  = $end_min;
                    } elsif ($_ == Extropia::Core::App::WebCal::MIDDLEDAY) {
                        # in the middle of the multi-day event
                        $s_hour = $ra_valid_working_hours->[0];
                        $s_min  = 0;
                        $e_hour = $ra_valid_working_hours->[-1] + 1;
                        $e_min  = 0;
                    } else {
                        # nothing
                    }

                    my %rec = %row;
                    @rec{qw(s_hour s_min e_hour e_min)} = ($s_hour,$s_min,$e_hour,$e_min);
                    $rec{date_obj} = $date_obj;
                    push @days_data, \%rec;
                }

            }

            $record_set->moveNext();
        }

      #  E::dumper(\@days_data);

        my ($rh_sel_day_data,$last_col) = $app->GetDataForSelectedDay
            (-RA_DATA  => \@days_data,
             -RA_HOURS => $ra_valid_working_hours
            );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-SEL_DAY_DATA",
            -PARAM_VALUE => $rh_sel_day_data,
        );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-VIEW_MODE",
            -PARAM_VALUE => 'DisplayDayViewAction',
        );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-LAST_COL",
            -PARAM_VALUE => $last_col,
        );
        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-DISPLAY_HOURS",
            -PARAM_VALUE => $ra_valid_working_hours,
        );
    }

    else {
        die('You must specify a configuration for ' .
            '-BASIC_DATASOURCE_CONFIG_PARAMS in order to ' .
            'use loadData(). You may do so in the ' .
            '@ACTION_HANDLER_ACTION_PARAMS array ' .
            'in the application executable');
    }
    return 1;
}

1;
__END__


