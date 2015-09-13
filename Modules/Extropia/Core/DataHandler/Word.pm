#$Id: Word.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
# Extropia::Core::DataHandler::Word checks that there is 
# a word and only a word in this field.
#
####################################################
package Extropia::Core::DataHandler::Word;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -IS_WORD         => [$self,\&isWord],
        -IS_WORD_IN_LIST => [$self,\&isWordInList],
        -IS_WORD_NOT_IN_LIST => [$self,\&isWordNotInList],
        -IS_BETWEEN_NUMBER_OF_WORDS => [$self,\&isBetweenNumberOfWords],
        -UNTAINT_WORD    => [$self,\&untaintWord]
    };
} # getHandlerRules


#
# isWord checks whether the field provided is a word
# Of course, we could do more than just use a regex, but 
# for now this is powerful enough for a basic class.
#
sub isWord {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid word.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid word since it hasn't actually
    # failed a test.

    if ($field =~ /^\s*$/ ||
        $field =~ /^\s*[\w\-]+\s*$/) {
        return 1;
    } else {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return 0;
    }

} # end of isWord

#
# isWordInList checks whether the fireld provided is
# in a list of words. 
#
sub isWordInList {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-WORD_LIST,
                     -FIELD_NAME,-ERROR_MESSAGE,
                     -CASE_INSENSITIVE],
                    [-FIELD_VALUE,-WORD_LIST],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $word_list  = shift || [];
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not in " . 
                              "the list of words.";
    my $case_insensitive = shift || 0;

    my $word;
    my $word_in_list = 0;
    foreach $word (@$word_list) {
        if ($word eq $field ||
            ($case_insensitive &&
             $field =~ /^$word$/i)) {
            $word_in_list = 1;
            last;
        }
    }

    if (!$word_in_list) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
    }
    return $word_in_list;

} # end of isWordInList

sub isBetweenNumberOfWords {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,
                     -MIN_NUM_WORDS,-MAX_NUM_WORDS,
                     -ERROR_MESSAGE],
                    [-FIELD_VALUE],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $min  = shift || 0;
    my $max = shift || 0;
    my $error_msg  = shift ||
         "%FIELD_NAME% field is not between $low_range and $high_range.";

    my @words = split (" ", $field);
    if (length(@words) > $min &&
        length(@words) < $max) {
        return 1;
    }

    $self->addError(
        new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)
            )
    );

   return 0;
}

sub isWordNotInList {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-WORD_LIST,
                     -FIELD_NAME,-ERROR_MESSAGE,
                     -CASE_INSENSITIVE],
                    [-FIELD_VALUE,-WORD_LIST],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $word_list  = shift || [];
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not in " . 
                              "the list of words.";
    my $case_insensitive = shift || 0;

    my $word;
    my $word_in_list = 1;
    foreach $word (@$word_list) {
        if ($word eq $field ||
            ($case_insensitive &&
             $field =~ /^$word$/i)) {
            $word_in_list = 0;
            last;
        }
    }

    if (!$word_in_list) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
            )
        );
    }
    return $word_in_list;

} # end of isWordInList


# untaintWord basically untaints a word
# based on the regex from isWord
#
sub untaintWord {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE],[-FIELD_VALUE],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg  = shift || "%FIELD_NAME% field is not a valid word.";

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # if the isXXXX method has a more stringent way of
    # untainting then we check this as well as a double
    # check.

    if ($self->isWord(-FIELD_VALUE => $field,-ADD_ERROR => 0) &&
        $field =~ /^\s*([\w\-]+)\s*$/) {
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintWord

1;

