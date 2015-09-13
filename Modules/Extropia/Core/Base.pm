# $Id: Base.pm,v 1.2 2001/07/19 10:00:47 stas Exp $
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

package Extropia::Core::Base;

use Carp;
use strict;

use Extropia::Core::Error;

use Exporter;
use vars qw(@EXPORT @EXPORT_OK @ISA $VERSION);


# NOTE: These methods are class level methods.
#
# The object level methods implemented at the bottom of
# Extropia::Core::Base are not exported because they will be
# found using the inheritence path when Extropia::Core::Base
# is inherited by the objects using it.
#
@EXPORT_OK = qw(_rearrange
                _rearrangeAsHash
                _assignDefault
                _assignDefaults
                _dieIfRemainingParamsExist
                _getDriver 
                _notImplemented
                _cloneRef
                _equalsRef
                _dieIfError);

@ISA = qw(Exporter);

$VERSION = do { my @r = (q$Revision: 1.10 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

####################################################
#
# Extropia::Core::Base package level methods... 
# 
# These need to be exported to be seen.
#
####################################################

#
# _rearrange takes a set of parameters whether they
# are named parameters or unnamed and returns an
# array of unnamed parameters. It also does checking
# for required parameters.
#
# $ra_order         ref to an array of the parameter order
# $ra_required      ref to an array of required parameters
# @param            paramaters passed to _rearrange
#
sub _rearrange {
    my ($ra_order,$ra_required,@param) = @_;

    # If we've got parameters, we need to check to see whether
    # they are named or simply listed.

    # if they are listed, we check for required fields
    # and whether any of the defaults need to be applied.
    my(%order_hash);
    my $count = 0;
    my $key;
    foreach $key (@{$ra_order}) {
        $order_hash{$key} = $count++;
        if ($key eq "0") {
            confess("One of the keys in the order list was a zero value. " .
                    "This usually means you forgot a comma in the " .
                    "parameter list. Here it is for your perusal: " . 
                    join(",", @$ra_order));

        }
    }

    my(@return_array,@leftover);
    if (defined($param[0]) && $param[0] =~ /^-/) {

# If the array is not an evan number of parameters then a
# comma may be missing.
        if (@param % 2) {
            confess("An even number of named parameters were not " .
                    "passed. Perhaps you forgot a comma between " .
                    "one of them. Here is the list: " . 
                    join("," , @param));
        }
        my %dup_test = @param;
        if (((keys %dup_test) * 2) != @param) {
            confess("You passed in duplicate parameters:" . 
                    join(",\n" ,@{__returnDuplicateParams(\@param)}));
        }
        # Ensure return array is proper length
        $return_array[$count-1] = undef;
        my $i;
        for ($i=0;$i<@param;$i+=2) {
            my $key = $param[$i];
            my $value = $param[$i+1];
            if (defined($order_hash{$key})) {
                $return_array[$order_hash{$key}] = $value;
            } else {
                push(@leftover,$key);
                push(@leftover,$value);
            }
        }

    } else {
        @return_array = @param;
    }

    my @did_not_pass_required = ();
    my $required_field;
    if (ref($ra_required) ne "ARRAY") {
        confess("Required fields array not a reference!");
    }
    foreach $required_field (@$ra_required) {
        if ($required_field eq "0") {
            croak("One of your required params was a 0. This usually means " .
                  "that you forgot a comma between two parameters so " .
                  "that one of the -PARAM values looks like the string " .
                  "PARAM is being subtracted from the prior value in the " .
                  "list of parameters. Go back and check that you properly " .
                  "delimited all your paramter -PARAM => VALUE pairs with " .
                  "commas");
        } else {
            croak("Required parameter $required_field is not listed among "
           ."the possible parameters for this module type.\n"
           ."This error is in the module itself, not in user-level code.\n")
                  unless defined($order_hash{$required_field});
        }
        if (!defined($return_array[$order_hash{$required_field}])) {
            push(@did_not_pass_required, $required_field);
        }
    }
    __required(\@did_not_pass_required, $ra_order) 
        if (@did_not_pass_required);

    return (@return_array,@leftover);

} # end of _rearrange

sub __returnDuplicateParams {
    my $params = shift;

    my @dups = ();

    my $param;
    my %used;
    foreach $param (@$params) {
        if (defined($used{$param})) {
            push(@dups,$param);
        } else {
            $used{$param} = 1;
        }
    }
    return \@dups;

} # end of __returnDuplicateParams

#
# _rearrangeAsHash is the same as _rearrange except
# that it returns a reference to a hash of named parameters
#
# $ra_order         ref to an array of the parameter order
# $ra_required      ref to an array of required parameters
# @param            paramaters passed to _rearrange
#
sub _rearrangeAsHash {
    my ($ra_order, $ra_required, @param) = @_;
    my %return_hash;
    my @leftover;
    if (@param && $param[0] =~ /^-/) {
        if (@param % 2) {
            confess("An even number of named parameters were not " .
                    "passed. Perhaps you forgot a comma between " .
                    "one of them. Here is the list: " . 
                    join(",\n" , @param));
        }
        my %dup_test = @param;
        if (((keys %dup_test) * 2) != @param) {
            confess("You passed in duplicate parameters:" . 
                    join(",\n" ,@{__returnDuplicateParams(\@param)}));
        }
        foreach (@$ra_order) {
            if ($_ eq "0") {
                confess("One of the keys in the order list was a zero value. " .
                    "This usually means you forgot a comma in the " .
                    "parameter list. Here it is for your perusal: " . 
                    join(",", @$ra_order));
            }
        }
        my %known;
        @known{@$ra_order} = ();
        my %param_hash = @param;
        @return_hash{@$ra_order} = @param_hash{@$ra_order};
        my $key;
        foreach $key (grep { !exists($known{$_}) } keys %param_hash) {
            push @leftover, $key, $param_hash{$key};
        }
    } else {
        @return_hash{@$ra_order} = splice(@param, 0, @$ra_order);
        @leftover = @param;
    }
    my @missing = grep { !defined($return_hash{$_}) } @$ra_required;
    __required(\@missing, $ra_order) if @missing;

    return (\%return_hash, @leftover);
} # end of _rearrangeAsHash

#
# __required complains about required parameters not
# being passed properly to _rearrange methods.
#
sub __required {
    my $ra_required_params = shift;
    my $ra_order           = shift;

    my $error = "";

    my $required;
    foreach $required (@$ra_required_params) {
        if ($required eq "0") {
            croak("One of your required params was a 0. This usually means " .
                  "that you forgot a comma between two parameters so " .
                  "that one of the -PARAM values looks like the string " .
                  "PARAM is being subtracted from the prior value in the " .
                  "list of parameters. Go back and check that you properly " .
                  "delimited all your paramter -PARAM => VALUE pairs with " .
                  "commas");
        }
        $error .= 
           "Required Parameter: $required was missing from a method call!\n";
    }
    $error .= "Possible Parameters Are: " . join(",\n\t", @$ra_order) . ".\n";

    confess($error);

} # end of __required

#
# _assignDefault takes a value and a default
# And if the value is not defined, the default
# is returned in its place.
#
sub _assignDefault {
    my $value   = shift;
    my $default = shift;

    if (!defined($value)) {
        return $default;
    }
    $value;

} # end of _assignDefault

#
# _assignDefaults is like _assignDefault
# except that it operates on entire hash
# of parameters.
#
# It takes a reference to a hash of
# paramaters and a reference to a hash
# of default values.
#
# Then, any default fields that do not have
# corresponding values in the original
# field/parameters hash are assigned.
#
# The resulting reference to a hash
# is returned.
#
sub _assignDefaults {
  my $rh_fields   = shift;
  my $rh_defaults = shift;

  my $key;
  foreach $key (keys %$rh_defaults) {
        if (!defined($rh_fields->{$key})) {
            $rh_fields->{$key} = $rh_defaults->{$key}; 
        }
  }

  return $rh_fields;

} # end of _assignDefaults

#
# _dieIfRemainingParamsExist will die with an error
# message to the programmer of app if bad params were
# passed. This utility method should be used after
# _rearrangeAsHash or _rearrange because any parameters
# that are left over are likely typos that should be
# corrected anyway.
#
sub _dieIfRemainingParamsExist {

    if (@_) {
        confess("You passed parameters that were not " .
                "included in the required or optional " .
                "parameter list. It's likely that you " .
                "typed a parameter name in incorrectly. " .
                "Here are the leftover parameters: " . 
                join (", ", @_) . "!\n");
    }

} # end of _dieIfRemainingParamsExist

#
# _getDriver obtains a package and driver for 
# a particular object. Used in factory object 
# create methods in the Extropia object hierarchy
#
sub _getDriver {
    my $driver_type   = shift;
    my $driver_source = shift;

    # --- load the code
    eval "use ${driver_type}::$driver_source;";
    if ($@) {
        my $advice = "";
        if ($@ =~ /Can't find loadable object/) {
           $advice = "Perhaps ${driver_type}::$driver_source was statically "
                 . "linked into a new perl binary."
                 . "\nIn which case you need to use that new perl binary."
                 . "\nOr perhaps only the .pm file was installed but not "
                 . "the shared object file."
        }
        elsif ($@ =~ /Can't locate.*?$driver_type\/$driver_source\.pm/) {
          $advice = "Perhaps the ${driver_type}::$driver_source perl module "
                     . "hasn't been installed,\n"
                     . "or perhaps the capitalization of '$driver_source' "
                     . "isn't right.\n";
        }
        Carp::croak("_getDriver() failed: $@: $advice\n");
    }

    "${driver_type}::$driver_source";

} # end of _getDriver

#
# _cloneRef makes a private copy of the supplied hash ref or
# list ref so that parameters passed by value such as update
# or delete specifications cannot be inadvertently changed.
#
# Note: objects are cloned by calling the object's clone method
#
# You will see that any object that inherits from Extropia::Core::Base
# also inherit a clone method that is not implemented and dies
# ...Thus warning the user of _cloneRef that they need to use it
# on an object that actually implements clone properly.
#
sub _cloneRef {
    my $ref = shift;

    my $clone;

    if (ref $ref eq "ARRAY") {
        $clone = [];
        push(@$clone, map { _cloneRef($_) } @$ref );
    }
    elsif (ref $ref eq "HASH") {
        $clone = {};
        my $key;
        foreach $key (keys %$ref) {
            $clone->{$key} = _cloneRef($ref->{$key});
        }
    }
    elsif (ref $ref eq "CODE") {
        $clone = $ref;
    }
    elsif (ref $ref) {
        $clone = $ref->clone();
    }
    else {
        $clone = $ref;
    }

    return $clone;

} # end of _cloneRef

#
# _equalsRef takes a ref to a hash or
# a ref to an array and checks that all
# the elements are equal as well as their
# elements if this is a more complicated
# and deep data structure.
#
# Note: If an object is reached, there is an
# attempt to call the equals method to determine
# equality.
#
# All objects obtain an equals method from
# Extropia::Core::Base that will die if invoked. This
# forces anyone using _equalsRef to know that they
# must make sure the objects they are using
# implements the equals method.
#
sub _equalsRef {
    my $first  = shift;
    my $second = shift;

    if (!defined($first)) {
        return 0 if defined($second);
    } elsif (!defined($second)) {
        return 0;
    } elsif (!ref $first) {
        return ($first eq $second);
    } elsif (ref $first ne ref $second) {
        return 0;
    } elsif (ref $first eq 'ARRAY') {
        return 0 unless @$first == @$second;
        my $i;
        for ($i = 0; $i < @$first; ++$i) {
            return 0 unless _equalsRef($first->[$i],$second->[$i]);
        }
    } elsif (ref $first eq 'HASH') {
        return 0 unless (keys %$first) == (keys %$second);
        my $key;
        foreach $key (keys %$first) {
            return 0 unless _equalsRef($first->{$key},$second->{$key});
        }
    } else {
        return $first->equals($second);
    }
    return 1;
    
} # end of _equalsRef

#
# _dieIfError dies with an error message if
# an error exists in the datasource object...
#

sub _dieIfError {
    my $object = shift;

    my $all_errors  = shift || 0;
    my $stack_trace = shift || 0;

    if ($object->getErrorCount()) {
        my $message;
        if ($all_errors) {
            my $error;
            my $count = 1;
            foreach $error ($object->getErrors()) {
                $message .= "Error $count: " .
                    $error->getMessage() . "\n";
                $count++;
            }
        } else {
            $message = 
                $object->getLastError()->getMessage();
        }
        if ($stack_trace) {
            confess($message);
        } else {
            confess($message);
        }
    }

}

####################################################
#
# Extropia::Core::Base object level methods... 
# 
# These are seen by an object that inherits from
# Extropia::Core::Base and are NEVER exported.
#
####################################################

sub clone  { _notImplemented("From Extropia::Core::Base"); }
sub equals { _notImplemented("From Extropia::Core::Base"); }

####################################################
#
# Extropia::Core::Base Error object related methods
# 
# The routines below have to do with manipulating
# a reference to an array of Extropia::Core::Error objects
# contained in $self->{__errors}. __errors is,
# by convention, a private variable common to all
# Extropia objects
#
####################################################

#
# getErrors gets a list of error objects and then
# clears the current list out. if -KEEP_ERRORS
# is set to true, then the list does not get cleared
# out.
#
sub getErrors {
    my $self = shift;
    @_ = _rearrange([-KEEP_ERRORS],[],@_);

    my $keep_errors = shift;

    # Note: have to create new array here so that user manipulation of this
    # array does not affect the object.  If error objects were mutable, we
    # would probably want to clone instead of just a shallow copy

    $self->{__errors} ||= [];

    my @errors = @{ $self->{__errors} };
    $self->{__errors} = [] unless $keep_errors;
    return \@errors;

} # end of getErrors

#
# getErrorCount returns the number of errors 
# on the error list of this current object
#
sub getErrorCount {
    my $self = shift;

    $self->{__errors} = [] unless $self->{__errors};
    return scalar(@{$self->{__errors}});

} # end of getErrorCount

#
# getLastError is like getErrors but returns
# the last error in the list rather than
# the whole list itself.
#
sub getLastError {
    my $self = shift;
    @_ = _rearrange([-KEEP_ERRORS],[],@_);

    my $keep_errors = shift;

    my $error_list = $self->getErrors(-KEEP_ERRORS => $keep_errors);
    my $last_error = @$error_list - 1;   
    if ($last_error < 0) {
        return undef;
    } else {
        return $error_list->[$last_error];
    }

} # end of getLastError

#
# addError adds an error to the error
# list for the current object.
# 
# The error can be one of three things:
#
# 1. An error object or subclass
# 2. A string to be used as a message to create
#    an error
# 3. A definition hash just like other constructors
#
sub addError {
    my $self = shift;
    @_ = _rearrange([-ERROR],[],@_);

    my $error_message = shift;

    my $error;
    if (defined($error_message) || @_) {
        #
        # If it is a definition hash
        #
        if (@_) {
            # Create error object from hash
            $error = new Extropia::Core::Error(@_);
        } else {
            #
            # If it is a preconstructed Extropia::Core::Error
            # Object.
            #
            if (ref $error_message) {
                croak "The object passed to addError was not an "
                    . "Extropia::Core::Error object" 
                    unless $error_message->isa("Extropia::Core::Error");
                $error = $error_message;
            # 
            # If it is just an error message string
            # 
            } else {
                # Create error object from string
                $error = new Extropia::Core::Error(-MESSAGE => $error_message);
            }
        }
        push(@{$self->{__errors}}, $error);
    } else {
        confess ("No error message was sent to the addError() method.");
    }

} # end of addError

1;

__END__

