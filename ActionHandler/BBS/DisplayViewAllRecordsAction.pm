package BBS::DisplayViewAllRecordsAction;

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
        -POSTED_DATE
            ],
            [
        -APPLICATION_OBJECT,
        -BASIC_DATA_VIEW_NAME,
        -CGI_OBJECT,
            ],
        @_
    );

    my $app = $params->{-APPLICATION_OBJECT};
    my $cgi = $params->{-CGI_OBJECT};
    my $posted_date = $params->{-POSTED_DATE} ||'date_time_posted';

    return 0 unless defined($cgi->param('view_all_records'));

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

    $app->setNextViewToDisplay(
        -VIEW_NAME => $cgi->param('view') || $params->{-BASIC_DATA_VIEW_NAME}
    );

    my @config_params = _rearrange([
        -BASIC_DATASOURCE_CONFIG_PARAMS
            ],
            [
            ],
        @{$params->{'-DATASOURCE_CONFIG_PARAMS'}}
    );

    my $datasource_config_params = shift (@config_params);

    # Get only data from certain forums
    my $forum = $cgi->param('forum') || '';
    unless ($forum) {
        #redirect to the forums page
        return 0;
    }   
    
    $cgi->param('forum', $forum);
    $cgi->param('raw_search',qq{forum == $forum});

    if ($datasource_config_params) {
         my ($ra_records,$total_records) = $app->loadData((
            -ENABLE_SORTING_FLAG         => $params->{-ENABLE_SORTING_FLAG},
            -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED => $params->{-ALLOW_USERNAME_FIELD_TO_BE_SEARCHED},
            -KEY_FIELD                   => $params->{-KEY_FIELD},
            -DATASOURCE_CONFIG_PARAMS    => $datasource_config_params,
            -SORT_DIRECTION              => $params->{-SORT_DIRECTION},
            -RECORD_ID                   => $cgi->param('record_id') || "",
            -SORT_FIELD1                 => 'thread_id',
#$params->{-SORT_FIELD1},
            -SORT_FIELD2                 => 'parent_id',
#$params->{-SORT_FIELD2},
            -MAX_RECORDS_PER_PAGE        => $params->{-MAX_RECORDS_PER_PAGE},
            -LAST_RECORD_ON_PAGE         => $params->{-LAST_RECORD_ON_PAGE},
            -SIMPLE_SEARCH_STRING        => $params->{-SIMPLE_SEARCH_STRING}, 
            -CGI_OBJECT                  => $params->{-CGI_OBJECT},
            -SESSION_OBJECT              => $params->{-SESSION_OBJECT},
            -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG},
            -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG => $params->{-REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG}
        ));

#        my $ra_display_fields = $params->{-FIELDS_NAMES} || [];
#        my @columns_to_view = $cgi->param('columns_to_view') 
#            ? $cgi->param('columns_to_view')
#            : @$ra_display_fields;
#        my @columns_to_view = qw(name subject  record_id parent_id thread_id );
        my @columns_to_view = ("name", "subject",$posted_date,  "record_id", "parent_id", "thread_id" );

#print STDERR "cols: @columns_to_view\n";
        # now convert the record set into a nested tree
        my $key_field               = $params->{-KEY_FIELD};
        my %threads = ();

        for my $rh_record (@$ra_records) {	

            my $record_id = $rh_record->{$key_field};
            my %row = ();
            foreach my $field (@columns_to_view) {
                $row{$field} =  $rh_record->{$field};
                
                $row{$field} = "&nbsp;" unless defined $row{$field};
            }

            # adjust/convert data
#            $row{$posted_date} = gmtime($row{$posted_date});

            push @{ $threads{ $row{thread_id} } }, \%row;
           
        }

#        use Data::Dumper;
#        print STDERR Data::Dumper::Dumper(\%threads);

        my %nest_threads;
        for my $thread_id (keys %threads) {
            $nest_threads{$thread_id}= build_sub_thread($threads{$thread_id});
        }

#        use Data::Dumper;
#        print STDERR Data::Dumper::Dumper(\%nest_threads);

        $app->setAdditionalViewDisplayParam(
            -PARAM_NAME  => "-NEST_THREADS",
            -PARAM_VALUE => \%nest_threads,
        );

        $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-RECORDS",
                 -PARAM_VALUE => $ra_records,
                );
        $app->setAdditionalViewDisplayParam
                (
                 -PARAM_NAME  => "-TOTAL_RECORDS",
                 -PARAM_VALUE => $total_records,
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


#####################
sub build_sub_thread{
    my $r_ary      = shift;

    # build the inheritance tree
    my %inh_tree = ();
    foreach my $r_row (@$r_ary) {
        my $id  = $r_row->{record_id};
        my $pid = $r_row->{parent_id};
        my $tid = $r_row->{thread_id};
        # store the data;
        $inh_tree{$id}->{data} = $r_row;

        # add children, orig stories don't have parents
        push @{ $inh_tree{$pid}->{kids} },$id 
            unless $id == $pid and $pid == $tid;
    }

    # dump the generated data structure to understand what it does
    #  use Data::Dumper;
    #  print STDERR Data::Dumper::Dumper(\%inh_tree));

    return \%inh_tree;

}

