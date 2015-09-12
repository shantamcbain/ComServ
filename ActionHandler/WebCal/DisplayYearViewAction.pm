package WebCal::DisplayYearViewAction;

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

    if (!$cgi->param('DisplayMonthViewAction') && !$cgi->param('DisplayDayViewAction') && !$cgi->param('DisplayYearViewAction')){
            if($default_view_mode != Extropia::Core::App::WebCal::YEAR) {
                  return 0;
             }
     } elsif ( !$cgi->param('DisplayYearViewAction') ) {
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

    if ($cgi->param('mode')){
    $app->setNextViewToDisplay(
        -VIEW_NAME => 'PrintView',
    );  
  }else{
    $app->setNextViewToDisplay(
        -VIEW_NAME => 'YearView',
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

    my $year  = $date_obj->year;
    my $month = $date_obj->month;
    my $days_in_month = $date_obj->days_in_month;
    my $sel_year_first_date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => [$year,1,1,0,0,0]
        );
    my $date_iterator_obj = $sel_year_first_date_obj->clone;
    # luckily Dec, 31 is always Dec, 31
    my $sel_year_last_date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => [$year,12,31,0,0,0]
        );

    my $sel_year_first_date = $sel_year_first_date_obj->get(-FORMAT => "%Y-%m-%d");
    my $sel_year_last_date  = $sel_year_last_date_obj->get(-FORMAT => "%Y-%m-%d");

    # trying to get all the event possibly falling into the selected day
    # later check the search range
    #
    # algorithm: 
    # (start_date <= 'sel_year_last_date 23:59' AND end_date >= 'sel_year_first_date 00:00')
    # or
    # (recur_interval > 0 AND start_date <= 'sel_year_last_date 23:59' AND recur_until_date >= sel_year_first_date)
    # 
    # this picks also recurrent events that might not happen today, we
    # need to delete those after the search is done

    my @select = ();

    # normal selected day events
    push @select, 
        qq{start_date <= "$sel_year_last_date 23:59" AND end_date >= "$sel_year_first_date 00:00"};
    # recurring events
    push @select, 
        qq{recur_interval > 0 AND start_date <= "$sel_year_last_date 23:59" AND recur_until_date >= "$sel_year_first_date"};

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

        my @columns_to_view = qw(record_id start_date end_date subject location
                                 description recur_interval
                                 recur_until_date);
        # META: more fields to extract later on

        # META: next stage, need to remove any recurrent events
        # falling into this range, but not happening on the selected
        # day in the future, may be need to modify the query so it
        # won't fetch those in first place

        my $selected_date = $date_obj->get(-FORMAT => "%Y-%m-%d");

        my $key_field = $params->{-KEY_FIELD};
        $record_set->moveFirst();

        my %days_data = ();

        # the cache that maps 'date's to a more informative datastructure
        my %dates = ();

        while (!$record_set->endOfRecords()) {
            my $id = $record_set->getField($key_field);

#print STDERR "*** ID: $id\n";
            my %row = ();
            foreach my $field (@columns_to_view) {
                $row{$field} =  $record_set->getField($field);
                $row{$field} = '' unless defined $row{$field};
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
                     -RANGE_START_DATE       => $sel_year_first_date,
                     -RANGE_END_DATE         => $sel_year_last_date,
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
                     -RANGE_START_DATE       => $sel_year_first_date,
                     -RANGE_END_DATE         => $sel_year_last_date,
                     -EVENT_START_DATE       => $row{start_date},
                     -EVENT_END_DATE         => $row{end_date},
                     -RECUR_END_DATE         => $row{end_date},
                     -RECUR_INTERVAL         => Extropia::Core::App::WebCal::NONE,
                    );
            }

            # render the content of the note
            my $note = $row{subject};
            $note .= " (".$row{location}.")" if $row{location};

            for my $ref (@$ra_overlap_dates) {
                my ($date_obj,$ra_occur) = @$ref;
                #E::dumper($date_obj);

                # for (@$ra_occur) {
                # not relevant since we aren't requested to specify hours here
                # }
                my $date = $date_obj->get(-FORMAT => "%Y-%m-%d");
                unless ($dates{$date}) {
                    $dates{$date} = {sort_num => $date_obj->get(-FORMAT => "%Y%m%d"),
                                     string   => join (" ",
                                                       $date_obj->mday,
                                                       $date_obj->month_string_short)
                                    };
                }
                push @{ $days_data{$date} },
                    {
                     note      => $note,
                     record_id => $id,
                    };
            }

            $record_set->moveNext();
        }

#            my @overlap_dates = ();

##            do {

#                # get the dates when the event overlaps with the requested range
#                if ($row{recur_interval} and $row{recur_until_date}) {
#                    my $ra_overlap_dates = $app->GetOverlappingDatesForRecurrentEvents
#                        (
#                         -DATETIME_CONFIG_PARAMS => $params->{-DATETIME_CONFIG_PARAMS},
#                         -RANGE_START_DATE       => $sel_year_first_date,
#                         -RANGE_END_DATE         => $sel_year_last_date,
#                         -RECUR_START_DATE       => $row{start_date},
#                         -RECUR_END_DATE         => $row{recur_until_date},
#                         -RECUR_INTERVAL         => $row{recur_interval},
#                        );
#                    @overlap_dates = @$ra_overlap_dates;
#                } else {
#                    # strip the time part of the date
#                    @overlap_dates = $start->get(-FORMAT => "%Y-%m-%d");
#                }
#                # try to check whether the following day is still in
#                # the span of the event
##                $start = $start->add_delta_ymd(-DAYS=>1);
##            } until ($start->compare_date(-WITH_OBJECT => $end) == Extropia::Core::DateTime::GREATER);

#            # the spanning events
#            my @tmp;
#            if (my $days_span = $end->days_span(-WITH_OBJECT => $start)) {
#                for my $date (@overlap_dates) {
#                    push @tmp, Extropia::Core::DateTime::create
#                        ( @$datetime_config,-DATETIME => $date)
#                            ->add_delta_ymd(-DAYS => $_)
#                            ->get(-FORMAT => "%Y-%m-%d")
#                                for 0..($days_span-1);
#                }
#                # put back
#                @overlap_dates = @tmp;
#            }

#            # render the content of the note
#            my $note = $row{subject};
#            $note .= " (".$row{location}.")" if $row{location};

#            for my $date (@overlap_dates) {
#                unless ($dates{$date}) {
#                    my $date_obj = Extropia::Core::DateTime::create
#                        ( @$datetime_config,-DATETIME => $date);
#                    $dates{$date} = {sort_num => $date_obj->get(-FORMAT => "%Y%m%d"),
#                                     string   => join (" ",
#                                                       $date_obj->mday,
#                                                       $date_obj->month_string_short)
#                                    };
#                }
#                push @{ $days_data{$date} },
#                    {
#                     note      => $note,
#                     record_id => $id,
#                    };
#            }

#            $record_set->moveNext();
#        }

        my @sel_year_data = ();
        # sort the dates
        for my $date (sort {$dates{$a}->{sort_num} <=> $dates{$b}->{sort_num}} keys %days_data) {
            my @day_events = @{ $days_data{$date} };
            # META: might need to sort these later on
             push @sel_year_data , 
                 {
                  date_str => $dates{$date}{string},
                  date     => $date,
                  events   => $days_data{$date},
                 };
        }

#        Extropia::Debug::dumper(\@sel_year_data);

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-SEL_YEAR_DATA",
            -PARAM_VALUE => \@sel_year_data,
        );

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-VIEW_MODE",
            -PARAM_VALUE => 'DisplayYearViewAction',
        );

    } else {
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


