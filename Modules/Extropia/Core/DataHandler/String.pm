#$Id: String.pm,v 1.4 2001/06/21 07:00:41 stas Exp $
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
# Extropia::Core::DataHandler::String checks for valid 
# values of strings
#
####################################################
package Extropia::Core::DataHandler::String;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.4 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -DOES_NOT_CONTAIN                  => [$self,\&doesNotContain],
        -IS_LENGTH_EQUAL_TO                => [$self,\&isLengthEqualTo],
        -IS_LONGER_THAN                    => [$self,\&isLongerThan],
        -IS_SHORTER_THAN                   => [$self,\&isShorterThan],
        -SUBSTITUTE_ONE_STRING_FOR_ANOTHER => [$self,\&substituteOneStringForAnother],
        -REMOVE_DOS_CHARACTERS             => [$self,\&removeDOSCharacters],
        -MAKE_EMPTY_STRING_UNDEF           => [$self,\&makeEmptyStringUndef]
    };
} # getHandlerRules

sub doesNotContain {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -CONTENT_TO_DISALLOW,
        -ERROR_MESSAGE,
        -ADD_ERROR,
            ],
            [
        -CONTENT_TO_DISALLOW
            ],
        @_
    );

    my $field                  = shift;
    $field = "" if (!defined($field));
    my $field_name             = shift || "unknown";
    my $content_to_disallow    = shift;
    my $error_msg              = shift || "%FIELD_NAME% may not contain '$content_to_disallow'.";
    my $add_error              = shift;

    $add_error = 1 if (!defined($add_error));

    if (ref($field)) {
        return 1;
    }

    # note that we consider nothing to be
    # a valid word since it hasn't actually
    # failed a test.

    if ($field =~ /\Q$content_to_disallow\E/) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    }

    return 1;

} # end of isWordVoidOfSpaces

sub isLengthEqualTo {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -LENGTH,
        -ERROR_MESSAGE,
        -ADD_ERROR,
            ],
            [
        -LENGTH
            ],
        @_
    );

    my $field                  = shift;
    $field = "" if (!defined($field));
    my $field_name             = shift || "unknown";
    my $length             = shift;
    my $error_msg              = shift || "%FIELD_NAME% must be equal to $length characters.";
    my $add_error              = shift;

    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid word since it hasn't actually
    # failed a test.

    if ($field && length($field) != $length) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return 0;
    }

    return $field;

} # end of isLengthEqualTo

sub isLongerThan {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -MIN_LENGTH,
        -ERROR_MESSAGE,
        -ADD_ERROR,
            ],
            [
        -FIELD_VALUE,
        -MIN_LENGTH
            ],
        @_
    );

    my $field                  = shift;
    $field = "" if (!defined($field));
    my $field_name             = shift || "unknown";
    my $min_length             = shift;
    my $error_msg              = shift || "%FIELD_NAME% must be longer than $min_length characters.";
    my $add_error              = shift;

    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid word since it hasn't actually
    # failed a test.

    if ($field && length($field) < $min_length) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return 0;
    }

    return $field;

} # end of isLongerThan

sub isShorterThan {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -MAX_LENGTH,
        -ERROR_MESSAGE,
        -ADD_ERROR,
            ],
            [
        -MAX_LENGTH
            ],
        @_
    );

    my $field                  = shift;
    $field = "" if (!defined($field));
    my $field_name             = shift || "unknown";
    my $max_length             = shift;
    my $error_msg              = shift || "%FIELD_NAME% must be shorter than $max_length characters.";
    my $add_error              = shift;

    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid word since it hasn't actually
    # failed a test.

    if ($field && length($field) > $max_length) {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return 0;
    }

    return $field;

} # end of isWordVoidOfSpaces

sub substituteOneStringForAnother {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -ORIGINAL_STRING,
        -NEW_STRING,
        -ERROR_MESSAGE,
        -ADD_ERROR,
            ],
            [
        -ORIGINAL_STRING,
        -NEW_STRING,
            ],
        @_
    );

    my $field                  = shift;
    return undef if (!defined($field));
    my $field_name             = shift || "unknown";
    my $old_string             = shift;
    my $new_string             = shift;
    my $error_msg              = shift || "%FIELD_NAME% is invalid.";
    my $add_error              = shift;

    my $ref = ref $field;
    if (!$ref) {
        $field =~ s/$old_string/$new_string/g;
    } elsif ($ref eq 'ARRAY') {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/$old_string/$new_string/g;
            push(@new_fields,$f);
        }
        return @new_fields;
    } else {
        warn "\$field is a $ref ref, dunno what to do";
    }

    return $field;

}

sub removeDOSCharacters {
    my $self = shift;
    @_ = _rearrange([
            -FIELD_VALUE,
            -FIELD_NAME,
            -ERROR_MESSAGE
            ],[
            -FIELD_VALUE
            ],
            @_);

    my $field      = shift;
    return undef if (!defined($field));
    my $field_name = shift;
    my $error_msg  = shift;

    if (!ref($field)) {
        $field =~ s/\r//g;
    } else {
        my @new_fields = ();
        my $f;
        foreach $f (@$field) {
            $f =~ s/\r//g;
            push(@new_fields,$f);
        }
        return @new_fields;
    }

    return $field;

} # end of removeDOSCharacters

#
# Designed to make empty strings undefined so that
# they will get entered into the database as nulls...
#
sub makeEmptyStringUndef {
  my $self = shift;
  @_ = _rearrange([
  		-FIELD_VALUE,
  		-FIELD_NAME
  	], [
  		-FIELD_NAME
  	],
  		@_);

  my $field      = shift;
  my $field_name = shift;

  if (ref($field)) {
    if (@$field) {
        return @$field;
    } else {
        return undef;
    }
  }
  if (defined($field) && $field =~ /^\s*$/) {
  	#die "is nothing: $fieldName";
  	return undef;
  } else {
  	return $field;
  }

} # end of makeEmptyStringUndef

1;
