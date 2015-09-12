#$Id: DependentFields.pm,v 1.3 2001/06/18 09:41:29 stas Exp $
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
# Extropia::Core::DataHandler::DependentFields does a lot of required
# fields checking
#
####################################################
package Extropia::Core::DataHandler::DependentFields;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.3 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
       -ARE_DEPENDANT_FIELDS_FILLED_IN => [$self,\&areDependentFieldsFilledIn],
       -ARE_DEPENDENT_FIELDS_FILLED_IN => [$self,\&areDependentFieldsFilledIn],
       -ARE_MINIMUM_DEPENDENT_FIELDS_FILLED_IN => 
           [$self,\&areMinimumDependentFieldsFilledIn],
       -ARE_MINIMUM_DEPENDANT_FIELDS_FILLED_IN => 
           [$self,\&areMinimumDependentFieldsFilledIn],
       -ARE_NO_MORE_THAN_MAX_FIELDS_FILLED_IN =>
           [$self,\&areNoMoreThanMaxFieldsFilledIn]
    };
} # getHandlerRules

sub areDependentFieldsFilledIn {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -DEPENDANT_FIELD_NAMES,
        -ERROR_MESSAGE, 
        -CGI_OBJECT
            ],
            [
            ],
        @_
    );

    my $field      = shift;
    $field = "" if (!defined($field));

    my $field_name = shift || "unknown";
    my $ra_dependant_field_names    = shift;
    my $error_msg  = shift || "%FIELD_NAME% field is dependant on " . join (", ", @$ra_dependant_field_names) ;
    my $cgi                         = shift;


    if (length($field) > 0) {
        my $dependant_field;
        foreach $dependant_field (@$ra_dependant_field_names) {
            if (!(length($cgi->param($dependant_field)) > 0)) {
                $self->addError(new Extropia::Core::Error(
                    -MESSAGE => $self->_getMessage($field_name, $field, $error_msg))
                );
                return undef;
            }
        }
    }
    return $field;
}

sub areMinimumDependentFieldsFilledIn {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -CGI_OBJECT,
        -MIN_NUMBER,
        -FIELD_NAMES,
        -DEPENDENT_FIELD_NAMES,
        -ERROR_MESSAGE, 
        -STRINGS_CONSIDERED_BLANK
            ],
            [
            -CGI_OBJECT,
            -FIELD_NAMES,
            -DEPENDENT_FIELD_NAMES
            ],
        @_
    );

    my $field      = shift;
    $field = "" if (!defined($field));

    my $field_name  = shift || "unknown";
    my $cgi         = shift;
    my $min_fields  = shift || 1;
    my $field_names = shift;
    my $dependent_field_names = shift;
    my $error_msg   = shift || "At least $min_fields fields should be filled in.";
    my $ra_strings_considered_blank = shift;

    my $number_of_dependent_fields_filled_in = 0;
    my $number_of_fields_filled_in = 0;

    foreach $field (@$dependent_field_names) {
        my $field_value = $cgi->param($field);
        if (length($field_value) > 0) {
            if ($ra_strings_considered_blank) {
                my $string;
                my $was_blank = 0;
                foreach $string (@$ra_strings_considered_blank) {
                    if ($string eq $field_value) {
                        $was_blank = 1;
                        last;
                    }
                }
                if (!$was_blank) {
                    $number_of_dependent_fields_filled_in++;
                }
            }
        } 
    }

    foreach $field (@$field_names) {
        my $field_value = $cgi->param($field);
        if (length($field_value) > 0) {
            if ($ra_strings_considered_blank) {
                my $string;
                my $was_blank = 0;
                foreach $string (@$ra_strings_considered_blank) {
                    if ($string eq $field_value) {
                        $was_blank = 1;
                        last;
                    }
                }
                if (!$was_blank) {
                    $number_of_fields_filled_in++;
                }
            }
        } 
    }

    if ($number_of_dependent_fields_filled_in < $min_fields &&
        $number_of_fields_filled_in > 0) {
        $self->addError(
            new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage('', '', $error_msg)  
            )
        );
        return undef;
    }
    return 1;

} # end of areMinimumDependentFieldsFilledIn

sub areNoMoreThanMaxFieldsFilledIn {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -CGI_OBJECT,
        -MAX_NUMBER,
        -FIELD_NAMES,
        -ERROR_MESSAGE, 
        -STRINGS_CONSIDERED_BLANK
            ],
            [
            -CGI_OBJECT,
            -FIELD_NAMES
            ],
        @_
    );

    my $field      = shift;
    $field = "" if (!defined($field));

    my $field_name  = shift || "unknown";
    my $cgi         = shift;
    my $max_fields  = shift || 1;
    my $field_names = shift;
    my $error_msg   = shift || "More than $max_fields fields were filled in.";
    my $ra_strings_considered_blank = shift;

    my $number_of_fields_filled_in = 0;

    foreach $field (@$field_names) {
        my $field_value = $cgi->param($field);
        if (length($field_value) > 0) {
            if ($ra_strings_considered_blank) {
                my $string;
                my $was_blank = 0;
                foreach $string (@$ra_strings_considered_blank) {
                    if ($string eq $field_value) {
                        $was_blank = 1;
                        last;
                    }
                }
                if (!$was_blank) {
                    $number_of_fields_filled_in++;
                }
            }
        } 
    }

    if ($number_of_fields_filled_in > $max_fields) {
        $self->addError(
            new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage('', '', $error_msg)  
            )
        );
        return undef;
    }
    return 1;

} # end of areNoMoreThanMaxFieldsFilledIn

1;

