#$Id: DataHandlerManager.pm,v 1.3 2001/11/07 04:06:49 cyph Exp $
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

package Extropia::Core::DataHandlerManager;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver _rearrangeAsHash);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION @EXPORT_OK);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.3 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@EXPORT_OK = qw(VALIDATE UNTAINT TRANSFORM);

sub VALIDATE()  { 1; }
sub UNTAINT()   { 2; }
sub TRANSFORM() { 3; }

sub create {
    my $package = shift;
    
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::DataHandlerManager", $type) or
        Carp::croak("DataHandlerManager type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);

} # end of create

sub init {
    my $self = shift;
    @_ = _rearrange([-RULES],[-RULES],@_);

    my $ra_rules = shift;
    $self->{-RULES} = $ra_rules;

    $self->{_datahandler_handlers} = {};
    
    my $datahandler;
    foreach $datahandler (@{$self->{-DATAHANDLERS}}) {
        my $dh_object;
        my $type = $datahandler;
        my $class = _getDriver("Extropia::Core::DataHandler", $type) or
            Carp::croak("DataHandler type '$type' is not supported");
        # hand-off to scheme specific implementation sub-class
        $dh_object = $class->new($self);
        $self->{_datahandler_objects}->{$datahandler} =
                                                   $dh_object;
        my $rh_handlers = $dh_object->getHandlerRules();
        my $handler;
        foreach $handler (keys %$rh_handlers) {
            $rh_handlers->{$datahandler . '::' . $handler} = 
                $rh_handlers->{$handler}; 
        }
        %{$self->{_datahandler_handlers}} = (
            %{$self->{_datahandler_handlers}},
            %{$rh_handlers}
        );

    }

# $self->_sortDataHandlerCategories(
#               -RULES => $ra_rules,
#               -VALIDATE_PREFIXES => ['-IS','-DOES'],
#               -UNTAINT_PREFIXES => ['-UNTAINT']
#               );

} # end of init

#
# _getFieldMapping helper routine to get the mapping
# of a field or return the field itself in case a
# nice clean description had not been given before.
#
sub _getFieldMapping {
    my $self = shift;
    @_ = _rearrange([-FIELD],[-FIELD],@_);

    my $field = shift;
  
    return $self->{-FIELD_MAPPINGS}->{$field} || $field;

} # end of _getFieldMapping

#
# validate is a public method which runs through all the 
# validation of a datahandler.
#
sub validate {
    my $self = shift;

    $self->_rulesEngine(VALIDATE,$self->{-RULES},0);

} # end of validate

#
# untaint is a public method that runs through all the
# untaint methods in a datahandler
#
sub untaint {
    my $self = shift;

    $self->_rulesEngine(UNTAINT,$self->{-RULES},0);

} # end of untaint

#
# transform is a public method that runs through all
# the transform methods in a datahandler
#
sub transform {
    my $self = shift;

    $self->_rulesEngine(TRANSFORM,$self->{-RULES},0);

} # end of transform

#
# return rule type
#
sub _getRuleType {
    my $self = shift;
    @_ = _rearrange([-RULE_NAME],
                    [-RULE_NAME],@_);

    my $rule = shift;

    my @validate_prefixes = qw(-IS -DOES -ARE);
    my @untaint_prefixes  = qw(-UNTAINT);

    my $validate_regex  = "(" . join('|',@validate_prefixes)  . ")";
    my $untaint_regex   = "(" . join('|',@untaint_prefixes)   . ")";

    # If a rule begins with ClassName::, we strip
    # it out for comparison so that just the hyphenated
    # handler name is left
    #
    my $rule_to_compare = $rule;
    if ($rule =~ /^.+::(-.+)/) {
        $rule_to_compare = $1;
    }

    if ($rule_to_compare =~ /^$validate_regex/) {
        return VALIDATE;
    } elsif ($rule_to_compare =~ /^$untaint_regex/) {
        return UNTAINT;
    } else {
        return TRANSFORM;
    }

} # end of _getRuleType

#
# _rulesEngine is the heart of the data validator
# it contains code to go through all the passed
# rules and automatically validate, untaint, or
# transform the rules.
#
sub _rulesEngine {
    my $self = shift;
    @_ = _rearrange([-RULE_TYPE,-RULES,-ORDERED_RULES],
                    [-RULE_TYPE,-RULES],@_);

    my $rule_type = shift;
    my $rule_list = shift;
    my $ordered_rules = shift || 0;

#    use Data::Dumper;
#    print Data::Dumper->Dump([$rule_list]) . "\n";
    my $rule;

    my $was_there_an_error = 0;

#    print "RULE LIST:$rule_list\n";
#    print "DEREF: " . join(",",@$rule_list) . "\n";
    my $i = 0;
RULELOOP: for ($i = 0; $i < @$rule_list; $i = $i + 2) {
        my $rule_map      = $rule_list->[$i];
        my $rule_params   = $rule_list->[$i + 1];

# Are we processing ordered or composite rules? then recurse...
        if ($rule_map eq "-ORDERED_RULES") {
            if (!$self->_rulesEngine($rule_type,$rule_params,1)) {
                $was_there_an_error++;
            } 
            next RULELOOP;
        }
        if ($rule_map eq "-COMPOSITE_RULES") {
            if (!$self->_rulesEngine($rule_type,$rule_params,0)) {
                $was_there_an_error = 1;
            } 
            next RULELOOP;
        }
# Are we processing the right rule type
        if ($self->_getRuleType(-RULE_NAME => $rule_map) != $rule_type) {
            next RULELOOP;
        }

        my $rule_info     = $self->{_datahandler_handlers}->{$rule_map};

        if (!$rule_info) {
            die("$rule_map rule was not imported into this datahandler's " .
                "namespace. Check your DataHandler creation variables.");  
        }

        my $rule_object   = $rule_info->[0];
        my $rule_function = $rule_info->[1];
        my @fields;
        my @params;
        if (!(ref($rule_params) eq "ARRAY")) {
            die("One of the rule parameters is a number. " .
                "This usually means a comma is missing between " .
                "some of the rules when the data handler was " .
                "created.");
        }
        if ($rule_params->[0] eq "-FIELDS") {
            @fields = @{$rule_params->[1]};
            if (@fields == 1 && $fields[0] eq "*") {
                @fields = $self->_getDataStoreFieldList();
            }
            if(defined $rule_params->[2] && $rule_params->[2] eq "-EXCEPT") {
                my %except = map {$_ => 1} @{$rule_params->[3]};
                @fields = map {$except{$_} ? () : $_ } @fields;
                @params = @{$rule_params}[4..$#$rule_params];
            } else {
                @params = @{$rule_params}[2..$#$rule_params];
            }
        } else {
            @fields = @$rule_params;
            if (@fields == 1 && $fields[0] eq "*") {
                @fields = $self->_getDataStoreFieldList();
            }
            @params = (); 
        }

        my @datastore_values;
        my $field;
        foreach $field (@fields) {
            my @ref_params = ();
            if (ref($field) eq "ARRAY") {
                my $field_marker;
                my $field_marker_name;
                foreach $field_marker (@$field) {
                    if (substr($field_marker,0,1) eq "-") {
                        $field_marker_name = $field_marker;
                        push(@ref_params,$field_marker);
                    } else {
                        @datastore_values = 
                            $self->_getDataStoreValueList($field_marker);
                        if (@datastore_values > 1) {
                            push(@ref_params,\@datastore_values);
                        } else {
                            push(@ref_params,$datastore_values[0]);
                        }
                        push(@ref_params,
                                $field_marker_name . "_NAME");
                        push(@ref_params,
                                $self->_getFieldMapping($field_marker));
                    }
                }
            } else { # end of field passed as an array
                @datastore_values = $self->_getDataStoreValueList($field);
            }


# Must make sure the rule is called at least once for every field...
# even if the field value is undefined. eg Check for Required Fields?
        @datastore_values = (undef) if (!@datastore_values);

            my @new_datastore_values = ();
            my $field_name = $self->_getFieldMapping($field);

            if ($rule_type == VALIDATE) {
                my $status;
                if (@ref_params) {
                    $status = 
                        &$rule_function(
                            $rule_object,
                            @ref_params,
                            @params
                            );
                } else {
                    if (@datastore_values > 1) {
                        $status = 
                            &$rule_function(
                                    $rule_object,
                                     -FIELD_VALUE => \@datastore_values,
                                     -FIELD_NAME => $field_name,
                                    @params);
                    } else {
                        my $ds_value = $datastore_values[0];
# if its a file handle don't touch it if the handler isn't upload or file aware...
                        if ($ds_value && ref($ds_value) && fileno($ds_value) && $rule_map !~ /(UPLOAD|FILE)/i) {
                            next;
                        }
                        $status = 
                            &$rule_function(
                                    $rule_object,
                                     -FIELD_VALUE => $datastore_values[0],
                                     -FIELD_NAME => $field_name,
                                    @params);
                    }
                }
                if (!defined($status)) {
                    $was_there_an_error++;
                }
            } else {
                if (@datastore_values > 1) {
                    @new_datastore_values = &$rule_function(
                                $rule_object,
                               -FIELD_VALUE => \@datastore_values,
                               -FIELD_NAME => $field_name,
                               @params);
                    if (ref($new_datastore_values[0])) {
                        confess("$rule_map is operating on a field " .
                                "that has multi values yet it does not " .
                                "know how to deal with them.");
                    }
                } else {
                    my $ds_value = $datastore_values[0];
# if its a file handle don't touch it if the handler isn't upload or file aware...
                    if ($ds_value && ref($ds_value) && fileno($ds_value) && $rule_map !~ /(UPLOAD|FILE)/i) {
                        next;
                    }
                    @new_datastore_values = &$rule_function(
                                $rule_object,
                               -FIELD_VALUE => $datastore_values[0],
                               -FIELD_NAME => $field_name,
                               @params);
                }
                if (!@new_datastore_values) {
                    $was_there_an_error++;
                }

                $self->_setDataStoreValueList($field, \@new_datastore_values) 
                    if (@new_datastore_values);
            }
        }
        if ($was_there_an_error && $ordered_rules) {
            last RULELOOP;
        }
    } # end of @rules

    if ($was_there_an_error) {
        return undef;
    } else {
        return 1;
    }
    
} # end of _rulesEngine

1;
