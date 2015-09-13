# $Id: FileSystemIndex.pm,v 1.3 2001/08/10 07:28:51 stas Exp $
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


package Extropia::Core::DataSource::FileSystemIndex;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::DataSource;
use Extropia::Core::Lock;
use Extropia::Core::KeyGenerator;
use vars qw($VERSION @ISA $MAX_FIELDS $DS);

$VERSION = do { my @r = q$Revision: 1.3 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);
$MAX_FIELDS = 255;

sub new {
    my $package = shift;
    my $self = $package->SUPER::new(@_);
    my $params;
    ($params,@_) = _rearrangeAsHash(
        [ -ROOT_DIRECTORY, 
          -FIELD_TO_DIRECTORY_MAPPINGS,
          -FIELD_TO_FILENAME_MAPPINGS,
          -FILENAME_EXTENSION,
          -FILENAME_DELIMITER,
          -FIELD_DELIMITER, 
          -RECORD_DELIMITER,
          -UPDATE_TEMP_FILE, 
          -KEYGENERATOR_PARAMS,
          -LOCK_PARAMS,
          -COMMENT_PREFIX,
          -NULL_STRING,
          -FILENAME_FILTER
        ],
        [], @_);

    $self = _assignDefaults($self, $params);

    if ($self->{-ROOT_DIRECTORY} &&
        ($self->{-ROOT_DIRECTORY} !~ /\/$/)) {
        $self->{-ROOT_DIRECTORY} .= "/";
    }

    $self = _assignDefaults($self, 
        { -RECORD_DELIMITER    => "\n",
          -FILENAME_EXTENSION  => ".db",
          -FIELD_TO_DIRECTORY_MAPPINGS => [],
          -FILENAME_DELIMITER  => "-",
          -FIELD_DELIMITER     => '|',
          -UPDATE_TEMP_FILE    => $self->{-ROOT_DIRECTORY} . "temp.new",
          -KEYGENERATOR_PARAMS => [ -TYPE => 'Counter',
                                    -COUNTER_FILE => 
                                        $self->{-ROOT_DIRECTORY}
                                        . "keygenerator.count",
                                    -LOCK_PARAMS => [ -TYPE => 'None' ],
                                  ],
          -LOCK_PARAMS         => [ -TYPE => 'File',
                                    -FILE => $self->{-ROOT_DIRECTORY} . ".dir",
                                  ],
          -COMMENT_PREFIX      => '',
          -NULL_STRING         => '',
        });
    push @{$self->{-KEYGENERATOR_PARAMS}}, -INITIAL_KEY_SOURCE => $self;

    if (!-e $self->{-ROOT_DIRECTORY}) {
        mkdir($self->{-ROOT_DIRECTORY}, 0755) ||
            die("Could not create " . 
                    $self->{-ROOT_DIRECTORY} . ": $!");
    }
    if (!$self->{-FIELD_TO_FILENAME_MAPPINGS}) {
        die("This driver must have at least one field to filename mapping!");
    }
    return $self;
}

#
# __createDirectoriesForFile
#

sub __createDirectoriesForFile {
    my $self = shift;
    my $file = shift;
    my $root = shift || "";

    return if (-e $file && -w $file);
    if (-e $file) {
        confess("The file: $file exists but is not writable.");
    }
# strip file off of $file and leave directories...
    $file =~ /$root(.*)\/.*/;

    my $dir = $1;
    if (!defined($dir)) {
        $dir = "";
    }
# If all the dirs exist then exit sooner...
    if (-e "$root$dir") {
        if (!(-d "$root$dir")) {
            confess("$root$dir exists but is not a directory.");
        } else {
            return;
        }
    }
    my @dir_list = split(/\//,$dir);
    $dir = $root;

    while (@dir_list > 0) {
        if (!(-e $dir)) {
            confess("The dir: $dir does not exist!");
        }
        if (!(-w $dir)) {
            confess("The dir: $dir is not writable!");
        }
        my $subdir = shift @dir_list;
        $dir .= $subdir . "/";
# Create the dir if it does not exist....
        if (!(-e $dir)) {
            mkdir($dir, 0777) || 
                confess("Could not create dir $dir: $!");
        }
    }

} # end of __createDirectoriesForFile

#
# __deleteEmptyDirectoriesForFile
#

sub __deleteEmptyDirectoriesForFile {
    my $self = shift;
    my $file = shift;
    my $root = shift || "";

# strip file off of $file and leave directories...
    $file =~ /$root(.*)\//;

    my $dir = $1;
    if (!defined($dir)) {
        $dir = "";
    }
    while (1) {
        if (!$self->__areAnyFilesInDirectory("$root$dir")) {
            rmdir("$root$dir") ||
                die("Could not remove dir: $root$dir: $!");
        } else {
# if there are files in the dir then we don't delete anymore...
            last;
        }
        if ($dir =~ /(.*)\//) {
            $dir = $1;
        } else {
# there are no more dirs to delete...
            last;
        }
    }

} # end of __deleteEmptyDirectoriesForFile

#
# __areAnyFilesInDirectory
# 

sub __areAnyFilesInDirectory {
    my $self = shift;
    my $dir  = shift;

    local(*DIR);
    opendir(DIR, $dir) ||
        die("Could not open: $dir for reading: $!");
    while(1) {
        my $line = readdir(DIR);
# We got through without finding files...
        return 0 if (!defined($line));
# We found a real file...
        return 1 if ($line !~ /^\./);
    }
    closedir(DIR);

} # end of __areAnyFilesInDirectory

sub __doDelete {
    my $self            = shift; 
    my $delete_criteria = shift;
    my $ret_orig        = shift || 0;

    my $field_delim         = $self->_getFieldDelimiter();
    my $comment_prefix      = $self->_getCommentPrefix();

# init return vars
    my $affected_rows = 0;
    my @original      = ();

    my $update_temp_file = $self->_getUpdateTempFile();

    $self->__clearFileIndex();
    $self->{_current_search_criteria} = $delete_criteria;
    while (1) {
        my $file = $self->__getNextFile();
        if (!defined($file)) {
            last;
        }
        local(*DATASOURCEFILE);
        local(*NEWDATASOURCEFILE);

        open (DATASOURCEFILE, "<$file");
        open (NEWDATASOURCEFILE, ">$update_temp_file");

# DELETION ALGORITHM:
#
# Read file...
#
# If no records deleted... just close and go away .. unlink
# NEWDATASOURCEFILE.
#
# If records deleted, then see if all records deleted. If so
# Remove file and recursively see if files need removing.
#
# If not all records deleted, then unlink old datasource file
# and move new one over to it...
#
        my $total_records   = 0;
        my $deleted_records = 0;
        while (<DATASOURCEFILE>) {
            my $original_line = $_;
            chomp;
            # Eliminate blank lines
            next if (/^\s*$/ && $_ !~ /\Q$field_delim/);
            # Keep comment lines
            if ($comment_prefix && /^$comment_prefix/) {
                print NEWDATASOURCEFILE $original_line;
                next;
            }
            $total_records++;
            my $index_field_hash = $self->{_field_hash};
            my $rh_rec = $self->__line2record($_,$index_field_hash);
            if ($self->_matches($delete_criteria, $rh_rec)) {
                push @original, $self->_recordInternal2Display($rh_rec)
                    if $ret_orig;
                ++$affected_rows;
                ++$deleted_records;
                next;
            }
            print NEWDATASOURCEFILE $original_line;
        }
        close (DATASOURCEFILE);
        close (NEWDATASOURCEFILE);

# handle the case if it was all deleted...

        unlink($file);
        if ($deleted_records == $total_records) {
            unlink($update_temp_file);
# delete directories recursively if empty...
            $self->__deleteEmptyDirectoriesForFile(
                    $file,$self->{-ROOT_DIRECTORY});
        } else {
            rename($update_temp_file, $file);
        }
    } # end of while true for files...
    return($affected_rows, \@original);
       
} # end of __doDelete

##
## __doUpdate actually performs the update...
##

sub __doUpdate {
    my $self            = shift;
    my $update_criteria = shift;
    my $update_fields   = shift;
    my $ret_orig        = shift || 0;

    my $field_delim         = $self->_getFieldDelimiter();
    my $comment_prefix      = $self->_getCommentPrefix();

# init return vars
    my $affected_rows = 0;
    my @original      = ();

    my $total_records   = 0;
    my $updated_records = 0;

    my @add_records = ();

#print "Starting update\n" . Dumper([$update_criteria, $update_fields]) . "\n";
    my $update_temp_file = $self->_getUpdateTempFile();

    local(*DATASOURCEFILE);
    local(*NEWDATASOURCEFILE);

#
# If the fields are outside the file then we must 
# delete the records in the files and then add the
# changed fields to the add queue...
#
    if ($self->__isAnyFieldOutsideFile(keys %{$update_fields})) {

        $self->__clearFileIndex();
        $self->{_current_search_criteria} = $update_criteria;
        while (1) {
            my $file = $self->__getNextFile();
            if (!defined($file)) {
                last;
            }
            local(*DATASOURCEFILE);
            local(*NEWDATASOURCEFILE);

            open (DATASOURCEFILE, "<$file");
            open (NEWDATASOURCEFILE, ">$update_temp_file");

            my $total_records   = 0;
            my $deleted_records = 0;
            while (<DATASOURCEFILE>) {
                my $original_line = $_;
                chomp;
                # Eliminate blank lines
                next if /^\s*$/ && $_ !~ /\Q$field_delim/;
                # Keep comment lines
                if ($comment_prefix && /^$comment_prefix/) {
                    print NEWDATASOURCEFILE $original_line;
                    next;
                }
                $total_records++;
                my $index_field_hash = $self->{_field_hash};
                my $rh_rec = $self->__line2record($_,$index_field_hash);
                if ($self->_matches($update_criteria, $rh_rec)) {
                    push @original, $self->_recordInternal2Display($rh_rec)
                        if $ret_orig;
# UPDATE PERFORMED HERE... 
                    my ($type, $value, $newval);
                    my $field;
                    foreach $field (keys %$update_fields) {
                        $type = $self->getDataType($field);
                        if ($type) {
                            $value = $update_fields->{$field};
                            $newval = $type->display2internal($value);
                            if (defined($value) && !defined($newval)) {
                                die "Invalid value '$value' for field "
                                    ."'$field', DataType " . ref $type . "\n";
                            }
                            $rh_rec->{$field} = $newval;
                        } else {
                            die("Unrecognized field '$field' in update\n");
                        }
                    } # endo f going through and updating the fields
                    push (@add_records, ["ADD", $rh_rec]);
                    ++$affected_rows;
                    ++$updated_records;
                    next;
                }
                print NEWDATASOURCEFILE $original_line;
        }
        close (DATASOURCEFILE);
        close (NEWDATASOURCEFILE);

# handle the case if it was all deleted...
        unlink($file);
        if ($updated_records == $total_records) {
            unlink($update_temp_file);
# delete directories recursively if empty...
            $self->__deleteEmptyDirectoriesForFile(
                    $file,$self->{-ROOT_DIRECTORY});
        } else {
            rename($update_temp_file, $file);
        }
    } # end of while true for files...
        $self->__clearFileIndex();
        while (1) {
            my $file = $self->__getNextFile();
            if (!defined($file)) {
                last;
            }

        } # While going through all files...
#
# Otherwise we simply update in place...
#
    } else {

        $self->__clearFileIndex();
        $self->{_current_search_criteria} = $update_criteria;
        while (1) {
            my $file = $self->__getNextFile();
            if (!defined($file)) {
                last;
            }

            open (DATASOURCEFILE, "<$file");
            open (NEWDATASOURCEFILE, ">$update_temp_file");

            while (<DATASOURCEFILE>) {
                my $original_line = $_;
                chomp;
                # Eliminate blank lines
                next if /^\s*$/ && $_ !~ /\Q$field_delim/;
                # Keep comment lines
                if ($comment_prefix && /^$comment_prefix/) {
                    print NEWDATASOURCEFILE $_, $self->_getRecordDelimiter();
                    next;
                }
                $total_records++;
                my $was_record_updated = 0;
                my $index_field_hash = $self->{_field_hash};
                my $rh_rec = $self->__line2record($_,$index_field_hash);
                if ($self->_matches($update_criteria, $rh_rec)) {
                    push @original, $self->_recordInternal2Display($rh_rec)
                        if $ret_orig;
                    my ($type, $value, $newval);
                    my $field;
                    foreach $field (keys %$update_fields) {
                        $type = $self->getDataType($field);
                        if ($type) {
                            $value = $update_fields->{$field};
                            $newval = $type->display2internal($value);
                            if (defined($value) && !defined($newval)) {
                                die "Invalid value '$value' for field "
                                    ."'$field', DataType " . ref $type . "\n";
                            }
                            $rh_rec->{$field} = $newval;
                        } else {
                            die("Unrecognized field '$field' in update\n");
                        }
                        ++$affected_rows;
                        ++$updated_records;
                        $was_record_updated = 1;
                    } # end of foreach
                } # end of if update done...
                if ($was_record_updated) {
                    my $line;
                    my $file;
                    ($line, $file) = $self->__record2line($rh_rec);
                    print NEWDATASOURCEFILE $line, $self->_getRecordDelimiter();
                } else {
                    print NEWDATASOURCEFILE $original_line;
                }
            }
            close (DATASOURCEFILE);
            close (NEWDATASOURCEFILE);

            unlink($file);
            rename($update_temp_file, $file);
        } # end of while true for files...
    } # end of if fields are outside the file...

    return($affected_rows, \@original, \@add_records);

} # end of __doUpdate

##
## Data Manipulation
##

#
# GB: doUpdate in DataSource::FileSystemIndex is particularly 
# difficult... here are the scenarios that are supported..
#
# 1) Add -- Just simply constructs the filename and line from
#           the record, and adds the sucker. If any subdirectory
#           does not exist then create it.
#
#    Algorithm: Pass __record2line() to get directory and 
#               line that exists in file. Then append line to file.
#
#               Generic routine needed that takes a directory and
#               if it does not exist, create the subdirectories
#               until root is reached. __createDirectoriesForFile();
#
# 2) Delete -- Open the file. Delete the record.
#              If the file is empty, delete the file.
#              If the directories are empty, delete the 
#              directories.
#
#    Algorithm: relies on __deleteEmptyDirectoriesForFile()
#               to delete empty directories. Same basic algorithm
#               as __createDIrectoriesForFile
#
# 3) Update -- If a field changed is inside the file, then just
#              update as normal.
#              If a field that is changed is a directory or
#              filename, then we must delete the record from
#              the original filename and construct a new record
#              and add it to another filename.
#
#     Algorithm: relies on __isAnyFieldOutsideFile routine to check if
#                a set of changes occurs outside the file
#

sub doUpdate {
    my $self = shift;
    @_ = _rearrange([-RETURN_ORIGINAL],[],@_);
    my $ret_orig = shift || 0;
    
    # Check that we can update (not READ_ONLY)
    return undef unless $self->_canUpdate("AddError");

    # If no work to do, can cut it short
    my $pending_updates = $self->_getPendingUpdates();
    return 0 if (!@$pending_updates && !$ret_orig);

    my $pending_adds = $self->_optimizeAdds() || return undef;
    # After successful optimize, only UPDATES and DELETES are left in 
    # $pending updates

    my $ds_file             = $self->_getFileName();
    my $update_tempfile     = $self->_getUpdateTempFile();
    my $field_delim         = $self->_getFieldDelimiter();
    my $autoincrement_field = $self->getAutoincrementFieldName();
    my $lock_params         = $self->_getLockParams();
    my $comment_prefix      = $self->_getCommentPrefix();
    my $null_string         = $self->_getNullString();
    my @original            = ();

    # Obtain a single lock covering the data file, the temporary file, and
    # the counter file
    my $lock;
    if ($lock_params) {
        $lock = Extropia::Core::Lock->create( @$lock_params );
        $lock->obtainLock();
    }
    
    # The eval block, and associated tests are to ensure that update is
    # atomic: either make all updates correctly or roll them all back.
    my $errors = 0;
    my $affected_rows = 0;

    eval { # BEGIN BIG EVAL BLOCK ------------------------

    local($/) = $self->_getRecordDelimiter();
    # Updates and Deletes
    my $update;
    foreach $update (@$pending_updates) {
        my $ret_original_rows;
        my $ret_affected_rows;
        my $ret_add_records;
        if ($update->[0] eq "UPDATE") {
            ($ret_affected_rows, $ret_original_rows, $ret_add_records) =
                $self->__doUpdate($update->[1],$update->[2],$ret_orig);
            push(@original,@$ret_original_rows);
            $affected_rows += $ret_affected_rows;
            push(@$pending_adds, @$ret_add_records);
        } elsif ($update->[0] eq "DELETE") {
            ($ret_affected_rows, $ret_original_rows) =
                $self->__doDelete($update->[1],$ret_orig);
            push(@original,@$ret_original_rows);
            $affected_rows += $ret_affected_rows;
        } else {
            confess "Unknown update type: '$update->[0]'\n"
        }
    } # end of foreach...

    # records are added last...
##
## This has been modified to work with FileSystemIndex
##
    if (@$pending_adds) {
        my $add;
        foreach $add (@$pending_adds) {
            confess "Unknown update type: '$add->[0]' (expected ADD)\n"
              if ($add->[0] ne "ADD");
            if ($autoincrement_field) {
                die("You must not supply a value for "
                    ."Autoincrement field '$autoincrement_field'; "
                    ."the value will be generated automatically.\n") 
                    if $add->[1]->{$autoincrement_field};
                $add->[1]->{$autoincrement_field} =
                    $self->_getNextAutoincrementValue();
            }
            my $line;
            my $file;
            ($line, $file) = $self->__record2line($add->[1]);
            $self->__createDirectoriesForFile(
                    $file,
                    $self->{-ROOT_DIRECTORY}
                    );
            open(NEWDATASOURCEFILE, ">>$file") ||
                die("Could not open $file for writing: $!\n");
            print NEWDATASOURCEFILE $line . 
                $self->_getRecordDelimiter();
            close(NEWDATASOURCEFILE);
            ++$affected_rows;
        }
    }
    
    }; # END BIG EVAL BLOCK -----------------------

# Release the lock earlier than in DataSource::File because each 
# update is considered atomic rather than going through one file...
#
    if ($lock) {
        $lock->releaseLock();
    }

    # Ideally, we would die with an error object, and just pass that error
    # object along here.  In the interest of being compatible with older
    # versions of Perl (5.003_07), we have to test strings to determine
    # which error codes to assign.
    if ($@) {
        my $code = 200;
        if ($@ =~ /^Could not open/) {
            $code = 103;
        }
        elsif ($@ =~ /^Unknown update type/) {
            die "$@\n";
        }
        elsif ($@ =~ /^Unrecognized field/) {
            $code = 204;
        }
        elsif ($@ =~ /^Invalid value/) {
            $code = 202;
        }
        # PSC: Add more error codes here...
        $self->addError(
            -CODE    => $code,
            -MESSAGE => $@, 
            -SOURCE  => 'DataSource::FileSystemIndex::doUpdate()'
        );
        $errors = 1;
# GB: I didn't know what this did so I commented it out...
# push( @$pending_updates, @$pending_adds );
    }

    if ($errors) {
        return undef;
    }
    return $self->_successfulUpdate($ret_orig, \@original, $affected_rows);
}

#
# __generateDataFileName
#

sub __generateDataFileName {
    my $self      = shift;
    my $rh_fields = shift;
    
    my $field_to_directory_mappings =
        $self->{-FIELD_TO_DIRECTORY_MAPPINGS};
    my $field_to_filename_mappings =
        $self->{-FIELD_TO_FILENAME_MAPPINGS};

    my $file_ext   = $self->{-FILENAME_EXTENSION};
    my $file_delim = $self->{-FILENAME_DELIMITER};
    my $root_dir   = $self->{-ROOT_DIRECTORY};

    my $dir = $root_dir;

    my $field_value;
    my $field;
    foreach $field (@$field_to_directory_mappings) {
        $field_value = $rh_fields->{$field};
        if (!defined($field_value)) {
            die("Field: $field did not a value!");
        }
        $dir .= $field_value . "/";
    }

    my @filename_field_values = ();
    foreach $field (@$field_to_filename_mappings) {
        $field_value = $rh_fields->{$field};
        if (!defined($field_value)) {
            die("Field: $field did not a value!");
        }
        push(@filename_field_values, $field_value);
    }
    $dir .= join($file_delim, @filename_field_values);
    $dir .= $file_ext;

    return $dir;

} # end of __generateDataFileName

sub disconnect {
    my $self = shift;

    if ($self->{'filehandle'}) {
        close($self->{'filehandle'});
        $self->{"filehandle"} = undef;
    }
}

##
## Querying Methods
##

sub __clearFileIndex {
    my $self = shift;

    $self->{_file_list_index} = undef;
} # end of __clearFileIndex

sub __getNextFile {
    my $self    = shift;

    my $index = $self->{_file_list_index};
    if (!defined($index)) {
       require File::Find;
       $DS = $self;
       $self->{_find_file_list}       = [];
       $self->{_find_field_hash_list} = [];
       File::Find::find(\&__fileFindCriteria, $self->{-ROOT_DIRECTORY});
       $index = 0;
    }
    my $file_list = $self->{_find_file_list};
#print Dumper([$file_list]) . "\n";

    my $file       = $file_list->[$index];
    my $field_hash = $self->{_find_field_hash_list}->[$index];
# Increment index...
    $index++;
# out of files!
    if (!$file) {
        $index = undef;
    }
    $self->{_file_list_index} = $index;
    $self->{_filename}        = $file;
    $self->{_field_hash}      = $field_hash;
    return $file;
    
} # end of __getNextFile

sub __fileFindCriteria {
    if (/^\./) {
        return;
    }
    my $self = $DS;
    my $ext  = $self->{-FILENAME_EXTENSION};
    if ($self->{-FILENAME_FILTER}) {
        my $filename_filter = $self->{-FILENAME_FILTER};
        if (/$filename_filter/) {
            return;
        }
    }

    my $orig_name = $File::Find::name;
    my $is_file   = -f $_;
    if ($is_file && $orig_name !~ /$ext$/) {
        return;
    }
    
# Trim the name down...
    my $root = $self->{-ROOT_DIRECTORY};
    $orig_name =~ /$root(.*)/;
    my $name = $1;

    my $field_to_directory_mappings =
        $self->{-FIELD_TO_DIRECTORY_MAPPINGS};
    my $field_to_filename_mappings =
        $self->{-FIELD_TO_FILENAME_MAPPINGS};

#
# Search criteria...
# 
    my $search_criteria = $self->{_current_search_criteria};

# We need to parse out the field names...
# 
# First, we need to grab all the directories..
# Then, we need to parse out the filename...
    my $dir_field;
    my %field_hash = ();
    foreach $dir_field (@$field_to_directory_mappings) {
        my $index = index($name,"/");
        my $field_value = "";
        if ($index >= 0) {
            $field_value = substr($name,0,$index);
            $name        = substr($name,$index + 1);
        } else {
            $field_value = $name;
            $name        = "";
        }
        $field_hash{$dir_field} = $field_value;
        last if (length($name) < 1);
    }
#
# check query criteria
#
# This is tricky because we can only realisticly
# check criteria on a partial basis...
#
    if ((scalar(keys %field_hash) > 0) &&
         !$self->_matches($search_criteria,
                        \%field_hash,
# The 1 at the end tells matches to check a match based on
# partial record info...
                        1)) {
#        print "Got pruned!\n";
        $File::Find::prune = 1;
        return;
    }
    my $delim = $self->{-FILENAME_DELIMITER};

    if ($name =~ /(.*)$ext$/) {
        $name = $1;
        my @fields = split(/$delim/,$name);
        my $file_field;
        foreach $file_field (@$field_to_filename_mappings) {
            my $field_value = shift(@fields);
#
# Criteria check
#
            $field_hash{$file_field} = $field_value;
            if (!$self->_matches($search_criteria,
                                \%field_hash,
# The 1 at the end tells matches to check a match based on
# partial record info...
                                1)) {
                return;
            }
        }
    }
#
# If successful match then we've reached here..
#
# But first we check if it is a directory or a file...
# if it's a directory we can't push it on the file stack...
#
    if ($is_file) {
        push(@{$self->{_find_file_list}}, $orig_name);
        push(@{$self->{_find_field_hash_list}}, \%field_hash);
    }

} # end of __fileFindCriteria

sub __openFile {
    my $self = shift;
    
# Close the file before opening another one...
    $self->disconnect();

    my $filename = $self->__getNextFile();
    if (!$filename) {
        return undef;
    }

    local *FH;
    if (open (FH, "<$filename")) {
        $self->{"filehandle"} = *FH;
    } elsif (!$self->_canCreateFile()) {
        die("Could not open $filename for reading: $!\n");
    }

    return $self->{"filehandle"};

} # end of __openFile

sub _realSearch {
    my $self = shift;

    my $ra_search               = shift;
    my $last_record_retrieved   = shift;
    my $max_records_to_retrieve = shift;
    my $order                   = shift;
    my $rs_data                 = shift;

    $self->{_current_search_criteria} = $ra_search;
    $self->__openFile();

    my $record_set = Extropia::Core::DataSource::RecordSet->create( 
                                  @$rs_data,
      -DATASOURCE              => $self,
      -KEY_FIELDS              => $self->_getKeyFields(),
      -UPDATE_STRATEGY         => $self->getUpdateStrategy(),
      -REAL_SEARCH_QUERY       => $ra_search,
      -LAST_RECORD_RETRIEVED   => $last_record_retrieved,
      -MAX_RECORDS_TO_RETRIEVE => $max_records_to_retrieve,
      -ORDER                   => $order
    );

    return $record_set;
}

sub _searchForNextRecord {
    my $self      = shift;
    my $ra_search = shift;

    my $record_found   = 0;
    my $field_delim    = $self->_getFieldDelimiter();
    my $comment_prefix = $self->_getCommentPrefix();
    my $fh             = $self->{"filehandle"};

    if (!$fh || !$self->_matchesActiveQuery($ra_search)) {
        $self->addError(
            -CODE    => 401,
            -MESSAGE => "Attempt to retrieve data from an inactive result set",
            -SOURCE  => 'DataSource::FileSystemIndex',
            -CALLER  => (caller)[0]
        );
        return 0;
    }

    local($/) = $self->_getRecordDelimiter();
    my $rh_rec;
    my $line;
    while (1) {
# Allow multiple files to be opened
# for searching...
        if (!(defined($line = <$fh>))) {
           $fh = $self->__openFile(); 
           if (!defined($fh) ||
               !(defined($line = <$fh>))) {
                last;
           }
        }
        chomp($line);
        # Skip blank lines and comments
        next if $line =~ /^\s*$/ && $line !~ /\Q$field_delim/;
        next if $comment_prefix && $line =~ /^$comment_prefix/;

        my $index_field_hash = $self->{_field_hash};
        $rh_rec = $self->__line2record($line,$index_field_hash);
        if (eval{ $self->_matches($ra_search, $rh_rec) }) {
            $record_found = 1;
            last;
        } elsif ($@) {
            $self->addError(
                -CODE => 300,
                -MESSAGE => $@, 
                -SOURCE => 'DataSource::FileSystemIndex',
                -CALLER => (caller)[0]
            );
        }
    } 

    if ($record_found) {
        return $self->_recordInternal2Display($rh_rec);
    } else {
        $self->disconnect();
        $self->_setActiveQuery();
        return undef;
    }
}

##
## Protected Methods (use at your own risk; API subject to change)
##

sub _getFileName {
    return $_[0]->{'_filename'};
}

sub _getFieldDelimiter {
    return $_[0]->{'-FIELD_DELIMITER'};
}

sub _getRecordDelimiter {
    return $_[0]->{'-RECORD_DELIMITER'};
}

sub _getUpdateTempFile {
    return $_[0]->{'-UPDATE_TEMP_FILE'};
}

sub _getLockParams {
    return $_[0]->{'-LOCK_PARAMS'};
}

sub _setLockParams {
    my ($self, @lock_params) = @_;
    if (@lock_params) {
        $self->{'-LOCK_PARAMS'} = \@lock_params;
    }
    else {
        $self->{'-LOCK_PARAMS'} = 0;
    }
}

sub _canCreateFile {
    return 1; # $_[0]->{'-CREATE_FILE_IF_NONE_EXISTS'};
}

sub _getCommentPrefix {
    return $_[0]->{'-COMMENT_PREFIX'};
}

sub _getNullString {
    return $_[0]->{'-NULL_STRING'};
}

# These next two routines, and the -KEYGENERATOR_PARAMS parameter are all
# candidates for inclusion in the base DataSource, but can remain here if
# it is anticipated that most file-oriented DataSources inherit from
# DataSource::FileSystemIndex.

sub _getNextAutoincrementValue {
    my $self = shift;

    if (!$self->{_key_generator}) {
        $self->{_key_generator} = Extropia::Core::KeyGenerator->create(
                @{$self->{-KEYGENERATOR_PARAMS}}
                );
    }

    my $kg = $self->{_key_generator};
    my $value = $kg->createKey();
    $self->_setLastAutoincrementID($value);
    return $value;
}

# This method is called by KeyGenerator::Counter through a callback
# mechanism when the counter file is lost.  We read the datafile to obtain
# the maximum existing value + 1

sub getInitialKey {
    my $self = shift;

# This is too complicated to code in DataSource::FileSystemIndexSystemIndex

    return 1;
    
}

sub __getFieldsOutsideFile {
    my $self = shift;

    my $dir_fields = $self->{-FIELD_TO_DIRECTORY_MAPPINGS};
    my $file_fields = $self->{-FIELD_TO_FILENAME_MAPPINGS};

    my @fields = (@$dir_fields, @$file_fields);

    return \@fields;

} # end of __getFieldsOutsideFile

sub __isAnyFieldOutsideFile {
    my $self      = shift;
    my @fields    = @_;

    my %outside_file_field_names = 
        map { $_ => 1 } @{$self->__getFieldsOutsideFile()};

    my $field;
    foreach $field (@fields) {
        if ($outside_file_field_names{$field}) {
            return 1;
        }
    }
    return 0;

} # end of __isAnyFieldOutsideFile

#
# __getFileFieldNames returns a list of field names
# that are contained inside the file...
#

sub __getFileFieldNames {
    my $self = shift;

    if ($self->{_file_field_names}) {
        return @{$self->{_file_field_names}};
    }

    my %outside_file_field_names = 
        map { $_ => 1 } @{$self->__getFieldsOutsideFile()};

    my @new_field_list = ();
    my $field;
    foreach $field ($self->getFieldNames()) {
        if (!$outside_file_field_names{$field}) {
            push(@new_field_list,$field);
        }
    }
    $self->{_file_field_names} = \@new_field_list;

    return @new_field_list;

} # end of __getFileFieldNames 

#
# Private method: __indexFields2line
#
sub __indexFields2Line {
    my $self = shift;
    my $index_field_hash = shift;
    my $orig_line        = shift;

    my $delim = $self->_getFieldDelimiter();

    my $line;
    my @index_fields = @{$self->__getFieldsOutsideFile()};
    my $field;
    my @field_values = ();
    foreach $field (@index_fields) {
        push(@field_values, $index_field_hash->{$field});
    }
    $line = join($delim, @field_values);
    if ($orig_line) {
        $line = $line . $delim . $orig_line;
    }

    return $line;
} # end of __indexFields2Line

#
# Private method: __line2record
#   Takes line of datafile and converts it to a hash-ref in Internal form
#
sub __line2record {
    my ($self, $line, $index_field_hash) = @_;

    $line = $self->__indexFields2Line($index_field_hash,$line);

    my $field_delim  = $self->_getFieldDelimiter;
    my $record_delim = $self->_getRecordDelimiter;
    my $null         = $self->_getNullString;

    # Note: third argument to split() is essential, since otherwise empty
    # arguments at end are simply ignored, and number of elements in
    # @fields array is not accurate
    my @fields   = split(/\Q$field_delim/, $line, $MAX_FIELDS);
    my @expected = $self->getFieldNames();

    if (@fields != @expected) {
        die "Incorrect number of fields in data line:\n$line\n"
            . "Expected " . scalar(@expected) . "; saw " . scalar(@fields)
            . ".  Possible data corruption, or perhaps you added a field "
            . "to the DataSource definition but forgot to add the field "
            . "to the data file itself.\n";
    }
    my $i;
    for ($i = 0; $i < @expected; ++$i) {
        if ($fields[$i]) {
            $fields[$i] =~ s/\\(.)/
                ($1 eq 'n') && $record_delim or
                ($1 eq 't') && $field_delim or
                ($1 eq '\\') && '\\' or
                "\\$1"/eg;
            # test for leftover escapes (shouldn't be any)
            die "Found unexpected escape code in field: $fields[$i].\n"
                ."This indicates the data has been corrupted, either "
                ."by manual editing or some unexpected failure\n"
                if $fields[$i] =~ /\\/;
            undef $fields[$i] if $null && $fields[$i] eq $null;
        }
        else {
            $fields[$i] = '' if $null;
        }
    }
    my $rec = $self->_recordStorage2Internal(\@fields);
    if (!$rec) {
        die "Invalid value in data file; possible file corruption or\n"
            . "improperly specified field type.\n"
            . $self->getLastError()->getMessage() . "\n";
    }
    return $rec;
}

#
# Private method: __record2line
#   Takes hash-ref in Internal form and converts to line suitable for
#   printing to file
#
# In the FileSystemIndex DataSource, this also returns a path
# to the file that will be written to with this line...
#
sub __record2line {
    my ($self, $rec) = @_;

    my $field_delim  = $self->_getFieldDelimiter;
    my $record_delim = $self->_getRecordDelimiter;
    my $null         = $self->_getNullString;
    my $fields       = $self->_recordInternal2Storage($rec);

    my $field;
    foreach $field (@$fields) {
        if (!defined($field)) {
            $field = $null || '';
        }
        $field =~ s/\\/\\\\/g;
        $field =~ s/\Q$field_delim\E/\\t/g;
    }

    my @path_fields = ();

    my @path_field_names = @{$self->__getFieldsOutsideFile()};
    foreach $field (@path_field_names) {
        push(@path_fields,shift @$fields);
    }
    my @file_fields = @$fields;
   
    my $line = join($field_delim, @file_fields);
    $line =~ s/\Q$record_delim\E/\\n/g;

    my $path = $self->{-ROOT_DIRECTORY};
    
    my $dir_fields  = $self->{-FIELD_TO_DIRECTORY_MAPPINGS};
    my $file_fields = $self->{-FIELD_TO_FILENAME_MAPPINGS};
    my $file_delim  = $self->{-FILENAME_DELIMITER};        
    
    foreach $field (@$dir_fields) {
        $path .= (shift @path_fields) . "/";
    }
    my @file_field_values = ();
    foreach $field (@$file_fields) {
        push(@file_field_values, (shift @path_fields));
    }
    $path .= join($file_delim, @file_field_values);
    $path .= $self->{-FILENAME_EXTENSION};

    return ($line, $path);
}

1;
__END__


=head1 NAME

Extropia::Core::DataSource::FileSystemIndex - A Perl5 object for manipulating flat file databases

=head1 SYNOPSIS

  use Extropia::Core::DataSource;

  my $ds = Extropia::Core::DataSource->create(
             -TYPE => "File",
             -FILE => "Path/datafile.dat",
             -FIELD_DELIMITER => '|',
             -FIELD_NAMES =>
                 ["ID", "Name", "Description", "Price"]
             -FIELD_TYPES =>
                 { ID => 'Autoincrement', Price => 'Number' }
           );

=head1 DESCRIPTION

This module is a driver that implements the Extropia::Core::DataSource interface.
Thus, apart from the single line of code that creates this particular type
of driver, you use it in exactly the same way as you would any other 
Extropia::Core::DataSource.

See S<USAGE> for a description of driver-specific creation parameters.  
See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 USAGE

=head2 Object Creation

In general, you will not create an Extropia::Core::DataSource::FileSystemIndex object
directly.  Instead, call the Extropia::Core::DataSource->create() method with the
following parameters.  A DataSource object of the appropriate type will be
returned.

These parameters are required, for all File DataSources:

=over 4

=item -TYPE

Specifies the type of DataSource to create.  Set to "File" for a File
DataSource.

=item -FILE

The path to the file where the data is stored.  This value must be
supplied; there is no default.

=item -FIELD_DELIMITER

The character or characters used to separate one field from another.
Obviously, the delimiter must not appear in the actual data.  This
value must be supplied; there is no default.

=item -FIELD_NAMES

A reference to an array of field names, in the order in which they appear
in the DataSource file.

=back

The remaining parameters are optional.  This next set is common to all
types of DataSource:

=over 4

=item -FIELD_TYPES

A reference to a hash, in which field names are the keys and the
corresponding field types are the values.  Accepted values for field types
include:

    String          for character data
    Date            for dates
    Number          for numeric data
    Auto            for autoincrementing numeric data, often used for
                    implementing a unique key field; only one such field
                    allowed per DataSource.

Additional user-defined datatypes may be created.  See
L<Extropia::Core::DataSource::DataType>.

Any field not assigned a field type defaults to String.

Date and datetime field types may be optionally followed by a format
string, showing how this data should be stored in the database and
presented to the user, e.g. date(<storage format>, <presentation format>).
If only a storage format is provided, this format will also be used for
presentation.  Date and time formats may be specified using any of the 
following symbols:

    m, mm       month number
    mmm         month abbreviation
    mmmm        month name
    d, dd       day number
    ddd         day abbreviation
    dddd        day name
    y, yyyy     four-digit year
    yy          two-digit year (strongly discouraged for storage values)

    H           hour
    M           minute
    S           second
    AM, PM      use 12-hour clock, with AM/PM

    e           seconds since the epoch (1/1/1970 on most systems), in 
                Universal Coordinated Time (UCT); this is the form returned
                from the time() function in Perl and C.

NOTE: while it is our intention to eventually allow any display format to
be used, currently only "standard" formats are accepted.  Any format that
cannot be recognized will result in an immediate error.

=item -KEY_FIELDS

A reference to an array of field names that together form a unique key for
a given record.  No two records should have the same values in all of their
key fields.

=item -UPDATE_STRATEGY

The update strategy tells the DataSource which fields should be used to
identify the records to be updated.  You must set this parameter to one of
the following constant values:

    $Extropia::Core::DataSource::KEY_FIELDS
    $Extropia::Core::DataSource::KEY_AND_MODIFIED_FIELDS
    $Extropia::Core::DataSource::ALL_FIELDS
    $Extropia::Core::DataSource::READ_ONLY

=item -RECORDSET_PARAMS

A definition hash, specified as a list reference, that provides the
parameters needed to create the default type of RecordSet to be used with
this DataSource.  By default, the DataSource will use a ForwardOnly
(unbuffered) RecordSet.

You may specify a different RecordSet type to use with a particular search
by specifying the -RECORDSET_PARAMS parameter as part of the keywordSearch()
or search() method call.  See the L<DataSource> for more information.

=item -KEYWORD_SEARCH_OR_FLAG

This flag, if set to any true value, allows the keywordSearch() method to
return a record if any one of the keywords matches.  By default, this flag
is false, and all of the words specified in a keywordSearch() must match.
This flag can also be manipulated after the DataSource has been created
using the getKeywordSearchOrFlag() and setKeywordSearchOrFlag() methods.

=back

The following optional parameters are specific to the DataSource::FileSystemIndex
driver:

=over 4

=item -RECORD_DELIMITER

A string that separates one record from another in the data file.  If this
value appears in the data, it will be transparently translated to '\n' and
back as needed.

=item -CREATE_FILE_IF_NONE_EXISTS

If this option is true, the data file will be created if it is missing.
This option should only be set if your scripts will be running in an
unknown, and potentially uninitialized environment.  If this option is not
set, a missing data file will raise an error.

=item -COUNTER_FILE

The path to the file where the next autoincrement value is stored.  This
value is used only when one of the fields has been defined as an
autoincrementing field.  The default value is the name of the DataSource
file with '.counter' appended to it.

=item -UPDATE_TEMP_FILE

The path to the file used as a temporary location to store the contents of
the DataSource while it is being updated.  This file should not exist, and
will be overwritten without warning if it does.  For greatest efficiency,
the update temp file should be on the same file system as the main
DataSource file.  The default value is the name of the DataSource file
with '.new' appended to it.

=item -LOCK_PARAMS

A reference to an array of parameters to be used to construct the lock on
the DataSource file.  See L<Extropia::Core::Lock> for details.  

Default is to use Flock locking, on a file named the same as the
DataSource file with a '.lock' extension appended, using a timeout of 
120 seconds, with 20 attempts during this period.

=back

=head1 DEPENDENCIES

This module is the driver that implements the Extropia::Core::DataSource
interface.  Thus, all of the modules that the Extropia::Core::DataSource depends
on must be in the library path, including:
    Extropia::Core::Base
    Extropia::Core::Error
    Extropia::Core::DataSource
    Extropia::Core::DataSource::Locale
    Extropia::Core::DataSource::DataType
    Extropia::Core::DataSource::RecordSet
Along with any particular Locales, DataTypes, and RecordSets that your
applications use.

In addition, this module depends on file-locking facilities provided by the
Extropia::Core::Lock module, and the particular locking strategy used, e.g.
Extropia::Core::Lock::Flock.

If date or datetime fields are used, Gordon Barr's TimeDate bundle is also
required.  Installing this bundle installs the following modules:

  Date::Parse
  Date::Format
  Date::Language
  Time::Zone

Furthermore, the Date::Parse module depends on Time::Local, which is part
of the standard Perl distribution.  Unfortunately, as of Perl 5.005_03, 
Time::Local had a serious bug that prevents it from handling dates between
1939 and 1969.  A patched version of Time::Local is available from Extropia,
and is being merged into the standard Perl distribution, beginning with 
Perl 5.6.

=head1 VERSION

Extropia::Core::DataSource::FileSystemIndex $Revision: 1.3 $

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

=head1 SEE ALSO

See L<Extropia::Core::DataSource> for information on how to use this object.

=head1 COPYRIGHT

(c)1999, Extropia.com

This module is open source software, and may generally be used according to
the spirit of the Perl "Artistic License".  If you are interested, however,
the actual license for this module may be found at http://www.extropia.com
(or more directly, at http://www.extropia.com/download.html).

=head1 AUTHOR

Extropia::Core::DataSource::FileSystemIndex is a Perl module written by Extropia
(http://www.extropia.com). Special technical and design acknowledgements
are given to Gunther Birznieks, Peter Chines and Selena Sol.

=head1 SUPPORT

B<Warning:> This is alpha-level software.  The interface specified here,
as well as the implementation details are subject to change.

Questions, comments and bug reports should be sent to support@extropia.com.

=cut
