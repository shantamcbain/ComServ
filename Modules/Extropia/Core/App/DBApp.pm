package Extropia::Core::App::DBApp;

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

use Extropia::Config;
use vars qw(@ISA);

use Extropia::Core::App;
@ISA = qw(Extropia::Core::App);

use Extropia::Core::Base qw(
    _rearrangeAsHash 
    _rearrange
    _assignDefaults
    _dieIfRemainingParamsExist
);

use Extropia::Core::Log;
use Extropia::Core::AuthManager;
use Extropia::Core::Mail;
use Extropia::Core::DataSource;

use HTML::Entities;

sub loadData {
    my $self = shift;
    @_ = _rearrange([
        -DATASOURCE_CONFIG_PARAMS,  
        -ALLOW_USERNAME_FIELD_TO_BE_SEARCHED,
        -SORT_FIELD1,  
        -SORT_FIELD2,  
        -MAX_RECORDS_PER_PAGE,
        -LAST_RECORD_ON_PAGE,
        -SIMPLE_SEARCH_STRING,
        -CGI_OBJECT,
        -SESSION_OBJECT,
        -RECORD_ID,
        -REQUIRE_MATCHING_USERNAME_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_SEARCHING_FLAG,
        -REQUIRE_MATCHING_SITE_FOR_SEARCHING_FLAG,
        -ENABLE_SORTING_FLAG,
        -KEY_FIELD,
        -SORT_DIRECTION,
        -TEST_COMMAND,
        -ACTION_HANDLER_PLUGINS,
        -RETURN_RECORD_SET,
            ],
            [
        -DATASOURCE_CONFIG_PARAMS,  
        -CGI_OBJECT
            ],
        @_);

    my $datasource_config_params_ref = shift;
    my $allow_username_to_be_searched = shift;
    my $sort_field1                  = shift;
    my $sort_field2                  = shift;
    my $max_records_to_retrieve      = shift;
    my $last_record_retrieved        = shift;
    my $simple_search_string         = shift;
    my $cgi                          = shift;
    my $session                      = shift;
    my $record_id                    = shift;
    my $require_matching_username_for_searching_flag = shift;
    my $require_matching_group_for_searching_flag    = shift;
    my $require_matching_site_for_searching_flag    = shift;
    my $enable_sorting_flag          = shift;
    my $key_field                    = shift;
    my $sort_direction               = shift;
    my $test_command                 = shift;
    my $action_handler_plugins       = shift;
    my $return_record_set            = shift;

    my $search_ds = Extropia::Core::DataSource->create(
        @$datasource_config_params_ref
    );

    if ($search_ds->getErrorCount()) {
        die("Whoopsy!  I was unable to construct the " .
            "DataSource object in the _loadData() mathod of " .
            "WebDB.pm. Please contact the webmaster. " . 
            $search_ds->getLastError()->getMessage()
        );
    } 

    my $search_string = "";

    if ($record_id) {
        $search_string = "$key_field == '$record_id'";
    }

    elsif($cgi->param('raw_search')) {
        $search_string = $cgi->param('raw_search');
    }

    elsif ($simple_search_string) {
        my $field;
        my @search_params;
        foreach $field ($search_ds->getFieldNames()) {
            if (($allow_username_to_be_searched || $field ne 'username_of_poster') &&
                $field ne 'group_of_poster' && $field ne $key_field) {
                push (@search_params, qq[$field =i "*$simple_search_string*"]);
            }
        }
        $search_string = "(" . join(" OR ", @search_params) . ")";
    }

    elsif ($cgi->param('submit_power_search')) {
        my $field;
        my @search_params;
        foreach $field ($search_ds->getFieldNames()) {
            my $admin_field = "search_$field";
            my $value = "*";
            if ($cgi->param($admin_field)) {
                $value = $cgi->param($admin_field);
                push (@search_params, qq[$field =i "*$value*"]);
            }
        }
        $search_string .= join (" AND ", @search_params);
    }
    else {
        $search_string = qq[* =i "*"];
    }
    
   if ($require_matching_site_for_searching_flag) {
        my $site = $session->getAttribute(
            -KEY => 'SiteName'
        )||'';
       $search_string .= " AND sitename == '*$site*'";
        }
    
   
    if ($require_matching_username_for_searching_flag) {
        my $username = $session->getAttribute(
            -KEY => 'auth_username'
        );
        $search_string .= " AND username_of_poster == '*$username*'";
    }

 
    if ($require_matching_group_for_searching_flag) {
        my $groups = $session->getAttribute(
            -KEY => 'auth_groups'
        )||'normal';

        my $group;
        $search_string .= " AND ";
        my @search_elements;
        foreach $group (split(",",$groups)) {
            push (@search_elements, "group_of_poster == '*$group*'");
        }
        
       $search_string .= "(" .
                          join (" OR ", @search_elements) .
                          ")";
    }
    my $record_set;
    if ($record_id) {
        $record_set = $search_ds->search(
            -SEARCH => $search_string
        );
    }

    else {
        if ($enable_sorting_flag) {
            $record_set = $search_ds->search(
                -ORDER                   => "$sort_field1 $sort_direction",
                -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve,
                -LAST_RECORD_RETRIEVED   => $last_record_retrieved,
                -SEARCH                  => $search_string
            );
        }

        else {
            $record_set = $search_ds->search(
                -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve,
                -LAST_RECORD_RETRIEVED   => $last_record_retrieved,
                -SEARCH                  => $search_string
            );
        }
    }

    if ($record_set) {
        if ($test_command) {
            die($record_set->getTotalCount() . $search_string);
        }

        if ($return_record_set) {
            # don't do a thing, return the record_set
            $record_set->moveFirst();
            return $record_set;

        } else {

            # convert record_set into data_set (an array of hashes).
            # note that to conform we always need to pass a list, even
            # when we have only one record
            my @records = ();
            $record_set->moveFirst();
            while (!$record_set->endOfRecords()) {
                push @records, $record_set->getRecordAsHash;
                $record_set->moveNext();
            }

            # Run plugins if any registered in the caller package. We
            # use caller() to get the package name of the caller and
            # then look it up in the
            # $param_hash->{-ACTION_HANDLER_PLUGINS} hash, if the
            # entry exists, we check wether there are plugins that
            # should be executed for -loadData_END
            #
            # note that this _END plugin, so we run it as late as
            # possible in this function
            my @conversion_plugins = 
                @{ $action_handler_plugins->{caller()}{-loadData_END} || [] };
            for my $plugin (@conversion_plugins) {
                $self->executePlugin($plugin,
                                      -RECORDS => \@records,
                                     );
            }

            # return either a ref to a list of records or if called in
            # list context return a ref to a list of records and the
            # total number of records (the total count can be bigger
            # than the returned slice)
            return wantarray
                ? (\@records,$record_set->getTotalCount()) 
                : \@records;
        }

    } else {
        die($search_ds->getLastError()->getMessage());
    }
}



sub deleteRecord() {
    my $self = shift;
    @_ = _rearrange([
        -CGI_OBJECT,
        -SESSION_OBJECT,
        -LOG_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG,
        -UPLOAD_MANAGER_CONFIG_PARAMS,
        -DELETE_FILE_FIELD_LIST,
        -KEY_FIELD
            ],
            [
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -REQUIRE_MATCHING_USERNAME_FOR_DELETIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_DELETIONS_FLAG
            ],
        @_);

    my $cgi                          = shift;
    my $session                      = shift;
    my $log                          = shift;
    my $datasource_config_params_ref = shift;
    my $require_matching_username_for_deletions_flag = shift;   
    my $require_matching_group_for_deletions_flag    = shift;
    my $upload_manager_config_params = shift;
    my $delete_file_field_list       = shift;
    my $key_field                    = shift;
    my $record_id                    = $cgi->param($key_field);

    my $delete_ds = Extropia::Core::DataSource->create(
         @$datasource_config_params_ref
    );

    if ($delete_ds->getErrorCount()) {
        die("Whoopsy!  I was unable to construct the " .
            "DataSource object in the _deleteRecord() " .
            "method of WebDB.pm. Please contact the webmaster." .
            $delete_ds->getLastError()->getMessage()
        );
    }
	
    my $delete_string = "$key_field = " . $record_id;

    if ($require_matching_username_for_deletions_flag) {
        my $username = $session->getAttribute(
            -KEY => 'auth_username'
        );

        $delete_string .= " AND username_of_poster = $username";
    }

    if ($require_matching_group_for_deletions_flag) {
        my $groups = $session->getAttribute(
           -KEY => 'auth_groups'
        );

        my $group;
        $delete_string .= " AND "; 
        my @modify_elements;
        foreach $group (split(",",$groups)) {
            push (@modify_elements, "group_of_poster == '*$group*'");
        }
        $delete_string .= "(" . 
                          join (" OR ", @modify_elements) .
                          ")";
    }

    my $original_rows_rs = $delete_ds->delete(
        -DELETE          => $delete_string,
        -RETURN_ORIGINAL => 1
    ); 

    if ($delete_ds->getErrorCount()) {
        if ($log) {
            $log->log(  
                 -SEVERITY => Extropia::Core::Log::WARN,
                 -EVENT    => "FAILED_DELETE|" . 
                              $delete_ds->getLastError(-KEEP_ERRORS => 1)->getMessage()
            );   
        }
        $self->addError($delete_ds->getLastError());
        return undef;
    }
             
    elsif ($original_rows_rs->isEmpty()) {   
        my $security_addendum = "";
        if ($require_matching_username_for_deletions_flag) {
            $security_addendum = "(that you are allowed to delete)";
        }

        $self->addError(
             "Whoopsy, I could not find a row $security_addendum " .
             "matching your modify criteria"
        );

        return undef;
    }

    else {   
        if ($log || $delete_file_field_list) {
            my @records;
            my @orig_records = $original_rows_rs->getAllRecordsAsHash();
            my $record;
            my $records;
            foreach $records (@orig_records) {
                foreach $record (@$records) {


                    if ($delete_file_field_list) {
                        require Extropia::Core::UploadManager;
                        my $upload_manager = 
                            Extropia::Core::UploadManager->create
                                  (@$upload_manager_config_params);
                        my $field;
                        foreach $field (@$delete_file_field_list) {
                            $upload_manager->deleteUploadedFile(-URL =>
                                    $record->{$field});
                        }
                    }

                if ($log) {
                        my $key;
                        foreach $key (keys %$record) {
                            push (@records, "$key=" . $record->{$key});
                        }
                    }
                }
            }

            if ($log) {
                $log->log(
                 -SEVERITY => Extropia::Core::Log::INFO,
                 -EVENT    => "DELETE PERFORMED\|" .
                              "DELETE_DEFINITION: $delete_string\|" .
                              "ORIGNAL_ROWS: " . join (" AND ", @records)
                );
            }
        }   
    }
    return 1;
}



sub addRecord {
    my $self = shift;
    @_ = _rearrange([
        -CGI_OBJECT,
        -LOG_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -SESSION_OBJECT,
        -ALLOW_DUPLICATE_ENTRIES,
        -POSTED_DATE
            ],
            [
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
            ],
        @_);

    my $cgi                          = shift;
    my $log                          = shift;
    my $datasource_config_params_ref = shift;
    my $session                      = shift;
    my $allow_duplicate_entries      = shift || 1;
    my $posted_date                  = shift || "date_time_posted";

    my @params = $cgi->param();

    my (%add_hash, $param);

    my @datasource_config_fields = _rearrange([
        -FIELD_NAMES
            ],
            [
        -FIELD_NAMES
            ],
        @$datasource_config_params_ref
    );
    my $datasource_fields = shift(@datasource_config_fields);

    my $field;
    foreach $field (@$datasource_fields) {
       
        if(defined($cgi->param($field))) {
        	# The next line will break if there are commas in the data - PSC
			
			# decode_entities is able to correctly decode more type of HTML entities (ie &auml;)
			# then CGI.pm's unescapeHTML. Previously certain entities were not being properly decoded before
			# being stored - HMS
        	$add_hash{$field} = decode_entities(join (",", $cgi->param($field)));
	    } else {
            # Field with empty data will be set to undef as in sybase, 
            # the field with undef value will not be in the insert statement.
		    $add_hash{$field}=undef;
	    }

        if ($field eq "username_of_poster" && defined ($session)) {
            $add_hash{'username_of_poster'} = $session->getAttribute(
                -KEY => 'auth_username'
            ) || "";
        }

        elsif ($field eq "group_of_poster" && defined $session) {
            $add_hash{'group_of_poster'} = $session->getAttribute(
                -KEY => 'auth_groups'
            ) || "";
        }

        elsif ($field eq $posted_date) {
            $add_hash{$posted_date} = $self->getCurrentTime();
        }
    }


    my $add_ds = Extropia::Core::DataSource->create(
        @$datasource_config_params_ref
    );

    if ($add_ds->getErrorCount()) {
        die("Whoopsy!  I was unable to construct the " .
            "DataSource object in the _addRecord() method " .
            "of WebDB.pm. Please contact the webmaster." .
            $add_ds->getLastError()->getMessage()
        );
    }

    if (!$allow_duplicate_entries) {
        my $field;
        my @search_params;
        foreach $field ($add_ds->getFieldNames()) {
            if ($field ne $posted_date &&
                $field ne 'record_id' &&
                $add_hash{$field} ne "") {
                push (@search_params, "$field == $add_hash{$field}");
            }
        }

        my $search_string = join (" AND ", @search_params);

        my $record_set = $add_ds->search($search_string);

        if ($record_set && $record_set->getTotalCount()) {
            $self->addError("Whoopsy!  I am sorry but it appears that " .
                "the record you are attemptiong to add is a duplicate " .
                "of a record already in the database.");
            return undef;
        }

        else {
            $add_ds->getLastError();
        }
    }

    my $rows_added = $add_ds->add(-ADD => \%add_hash);
    my $last_id = $add_ds->getLastAutoincrementID();

    if ($add_ds->getErrorCount()) {
        if ($log) {
            $log->log(   
                 -SEVERITY =>  Extropia::Core::Log::WARN,
                 -EVENT    => "FAILED_ADDITION|" . 
                              $add_ds->getLastError(-KEEP_ERRORS => 1)->getMessage()
            );
        }

        $self->addError($add_ds->getLastError());
        return undef;
    }
             
    else {
        if ($log) {
            my $key;
            my @add_array;
            foreach $key (keys %add_hash) {
            # The condition to check if the value is defined is added
            # so to allow the uninitialised value warning which may cause 
            # Internal server error in some of the system environment.
    		if(defined($add_hash{$key})) {
               push (@add_array, "$key=" . $add_hash{$key});
               }
            } 
            my $add_string = join("\|", @add_array);
            $log->log(
                 -SEVERITY =>  Extropia::Core::Log::INFO,
                 -EVENT    => "ADDITION PERFORMED\|" . 
                              "ADD_DEFINITION: $add_string"
            );
        }       
    }
    return wantarray ? (1,$last_id) : 1;
}



sub modifyRecord {
    my $self = shift;
    @_ = _rearrange([
        -CGI_OBJECT,     
        -SESSION_OBJECT,     
        -LOG_OBJECT,
        -DATASOURCE_CONFIG_PARAMS,
        -REQUIRE_MATCHING_USERNAME_FOR_MODIFICATIONS_FLAG,
        -REQUIRE_MATCHING_GROUP_FOR_MODIFICATIONS_FLAG,
        -UPLOAD_MANAGER_CONFIG_PARAMS,
        -MODIFY_FILE_FIELD_LIST,
        -MODIFY_STRING,
        -KEY_FIELD
            ],
            [
        -CGI_OBJECT,
        -DATASOURCE_CONFIG_PARAMS
            ],
        @_);

    my $cgi                          = shift;
    my $session                      = shift;
    my $log                          = shift;
    my $datasource_config_params_ref = shift;
    my $require_matching_username_for_modifications_flag = shift || 0;
    my $require_matching_group_for_modifications_flag = shift || 0;
    my $upload_manager_config_params = shift;
    my $modify_file_field_list       = shift;
    my $overriding_modify_string     = shift;
    my $key_field                    = shift;
    my $modify_ds = Extropia::Core::DataSource->create(
        @$datasource_config_params_ref
    );

    if ($modify_ds->getErrorCount()) {
        die("Whoopsy!  I was unable to construct the " .
            "DataSource object in the _modifyRecord() of " .
            "WebDB.pm. Please contact the webmaster." .
            $modify_ds->getLastError()->getMessage()
        );
    }

    my $modify_string = $overriding_modify_string || 
                        "$key_field ==  '" . 
                        $cgi->param($key_field) . 
                        "'";

    if ($require_matching_username_for_modifications_flag) {
        my $username = $session->getAttribute(
           -KEY => 'auth_username'
        );

        $modify_string .= " AND username_of_poster = $username";
    } 

    if ($require_matching_group_for_modifications_flag) {
        my $groups = $session->getAttribute(
            -KEY => 'auth_groups'
        );

        my $group;
        $modify_string .= " AND "; 
        my @modify_elements;

        foreach $group (split(",", $groups)) {
            push (@modify_elements, "group_of_poster == '*$group*'");
        }

        $modify_string .= "(" . 
                          join (" OR ", @modify_elements) .
                          ")";
    }

    my @params = $cgi->param();

    # the modified data is defined as follows:
    # 1. original_value is undef (didn't exist before) and value is defined
    # 2. it existed before and now was modified
    my %modifyHash = ();
    my $modify_item = 0;
    foreach my $param ($modify_ds->getFieldNames()) {
       # This condition (not allowing key field to be updateable) is added because
       # problem will be encountered in sybase if you tried to update the AUTOINCREMENTAL 
       # key field(primary field) of the table. But note that not all key fields are autoincremental.
       
       if ($param ne $key_field) {
       	
        if (
            (!defined $cgi->param("original_$param") 
             and defined $cgi->param($param))
            or
            (defined $cgi->param($param) and
             defined $cgi->param("original_$param") and
             $cgi->param($param) ne $cgi->param("original_$param")
            )
            
           ) {

            $modify_item ++;	
       		my $a = $cgi->param($param);
       		if(defined($a)) {
			 # decode_entities is able to correctly decode more type of HTML entities (ie &auml;)
			 # then CGI.pm's unescapeHTML. Previously certain entities were not being properly decoded before
			 # being stored - HMS
       		 $modifyHash{$param} = decode_entities(join ",", $cgi->param($param));
       		} else {
             # Again empty field will be set to undef and it will not be added into the sql insert statement.
       		 $modifyHash{$param} = undef;
       		}
        }
      }
    }

    if (Extropia::Config::DATASOURCE_DEBUG) {
        print STDERR "Doing modify\n";
        print STDERR "modify string: $modify_string\n";
        require Data::Dumper;
        print STDERR Data::Dumper::Dumper \%modifyHash;
    }

my $original_rows_rs;
if ($modify_item > 0) {
    $original_rows_rs = $modify_ds->update(
        -QUERY            => $modify_string,
        -UPDATE           => \%modifyHash,  # Ensure \%modifyHash is a hash reference
        -RETURN_ORIGINAL  => 1
    );
} else {
    return 1;  # No modifications to be made
}

    if ($modify_ds->getErrorCount()) {
        if ($log) {
             $log->log(  
                 -SEVERITY => Extropia::Core::Log::WARN,
                 -EVENT    => "FAILED_DELETE|" . 
                              $modify_ds->getLastError(-KEEP_ERRORS => 1)->getMessage()
            );        
        }
        $self->addError($modify_ds->getLastError());
        return undef;
    }

    elsif ($original_rows_rs->isEmpty()) {   
        my $security_addendum = "";
        if ($require_matching_username_for_modifications_flag ||
            $require_matching_group_for_modifications_flag) {
            $security_addendum = "(that you are allowed to modify)";
        }
        $self->addError(
             "Whoopsy, I could not find a row $security_addendum " . 
             "matching your modify criteria"
        );   
        return undef;
    }
#
# This handles the case of what if the records need logging or 
# if we need to delete a file that was contained in the original
# record... 
# 
# NOTE that this code is almost identical to the code in 
# _deleteRecord except that it checks to see if a new file has
# been uploaded. If it has, then we know that the old one must be
# deleted.
    
    else {
        if ($log || $modify_file_field_list) {
            my @records;
            my @orig_records = $original_rows_rs->getAllRecordsAsHash();
            my $record;
            my $records;
            foreach $records (@orig_records) {
                foreach $record (@$records) {

                    if ($modify_file_field_list) {
                        require Extropia::Core::UploadManager;
                        my $upload_manager = 
                            Extropia::Core::UploadManager->create(
                                    @$upload_manager_config_params);
                        my $field;
                        foreach $field (@$modify_file_field_list) {
                            if (defined($modifyHash{$field}) &&
                                 $modifyHash{$field} ne $record->{$field}) {
                                 $upload_manager->deleteUploadedFile(-URL =>
                                    $record->{$field});
                            }
                        }
                    }

                    if ($log) {
                        my $key;
                        foreach $key (keys %$record) {
                            # This additional conditional check for defined value is added to avoid uninitialized value warning.
if (defined($record->{$key})) {
    push(@records, "$key=" . $record->{$key});
}
                        }
                    }
                }
            }
#
# WRITE OUT THE LOG ENTRY
#
            if ($log) {
                $log->log(
                 -SEVERITY => Extropia::Core::Log::INFO,
                 -EVENT    => "MODIFY PERFORMED\|" .
                              "MODIFY_DEFINITION: $modify_string\|" .
                              "ORIGNAL_ROWS: " . join (" AND ", @records)
                );
            }
        }
    }
    return 1;
}

1;
__END__
