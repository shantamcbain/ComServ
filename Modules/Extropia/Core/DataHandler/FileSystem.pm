#$Id: FileSystem.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
# Extropia::Core::DataHandler::FileSystem
#
####################################################
package Extropia::Core::DataHandler::FileSystem;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
        my $self = shift;

        return {
            -IS_FILENAME                => [$self,\&isFilename],
            -IS_PATH                    => [$self,\&isPath],
            -UNTAINT_FILENAME           => [$self,\&untaintFilename],
            -UNTAINT_PATH               => [$self,\&untaintPath]
        };
} # getHandlerRules

#
# isFilename returns true if the field passed is a filename.
#
# Of course, we could do more than just use a regex, but 
# for now this is powerful enough for a basic class.
#
sub isFilename {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg    = shift || "%FIELD_NAME% field is not a valid filename.";
    my $add_error  = shift;
    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid filename since it hasn't actually
    # failed a test.

    if ($field =~ /^\s*$/ ||
        $field =~ /^\s*[\w\-.]+\s*$/) {
        return 1;
    } else {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    }

} # end of isFilename

#
# untaintFilename basically untaints a raw filename. No
# directory characters should exist for a filename.
#
# Regex is based on isFilename method
#
sub untaintFilename {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE],@_);
    
    my $field      = shift;
    $field = "" if (!defined($field));
    my $field_name = shift || "unknown";
    my $error_msg    = shift || "%FIELD_NAME% field is not a valid filename.";

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an unitialized value

    return "" if ($field =~ /^\s*$/);

    # The first item is to check the filename
    # is valid.
    # 
    # The second item makes sure not more than
    # 2 periods in a row (to signify going up
    # the directory tree).
    #
    # After we cleared multiple dots, we
    # can allow the filename to consist of
    # any letters, digits, underscores (word chars)
    # dashs, and periods...
    #

    if ($self->isFilename(-FIELD_VALUE => $field,-ADD_ERROR => 0) &&
        $field !~ /(\\?\.){2,}/ &&  # remember that backslashed dots may
                                    # count as well in some shells.
        $field =~ /^\s*([\w\-.]+)\s*$/) {
        return $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }
} # untaintFilename


#
# isPath returns true if the field passed is a path which
# may optionally contain a filename.
#
# Of course, we could do more than just use a regex, but 
# for now this is powerful enough for a basic class.
#
# Note that an additional parameter: -EXIST_CHECK may be
# set to true if we want to perform an existence check
# on the file.
#
# Note that directories on a MacOS box may contain :'s.
#
# We disallow preceding /'s so that absolute paths will be
# rejected.
#
# The valid path prefix is set so that we can see if the
# path matches the path prefix list if it exists.
#
sub isPath {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-EXIST_CHECK,
                     -VALID_PATH_PREFIXES,
                     -ADD_PATH_PREFIX,
                     -FIELD_NAME,
                     -ERROR_MESSAGE,-ADD_ERROR],
                    [-FIELD_VALUE],@_);

    my $field           = shift;
    $field = "" if (!defined($field));
    my $exist_check     = shift;
    my $valid_path_list = shift;
    my $add_path_prefix = shift || "";
    my $field_name      = shift || "unknown";
    my $error_msg       = shift 
                          || "%FIELD_NAME% field is not a valid path.";
    my $add_error       = shift;
    $add_error = 1 if (!defined($add_error));

    # note that we consider nothing to be
    # a valid path since it hasn't actually
    # failed a test.

    if ($field =~ /^\s*$/ ||
        ($field !~ /(\\?\.){2,}/ &&  # remember that backslashed dots may
                                     # count as well in some shells.
        $field =~ /
                   ^          # from the start
                   \s*        # allow surrounding whitespace
                   [\w\-.]+    # start with any path char except no slashes
                   [\/:\w\-.]* # any path characters including slashes 
                   \s*        # allow surrounding whitespace
                   $          # to the end
                  /x &&
        $self->_isInPathPrefixList(-PATH => $field,
                                   -VALID_PATH_PREFIXES => 
                                       $valid_path_list) &&
        (!$exist_check || -e ($add_path_prefix . $field)))) {
        return 1;
    } else {
        if ($add_error) {
            $self->addError(
                new Extropia::Core::Error(
                -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
                )
            );
        }
        return undef;
    }

} # end of isPath

#
# _isInPathPrefixList is a helper method that
# takes a path and checks if it matches a list of
# possible path prefixes.
#
sub _isInPathPrefixList {
    my $self = shift;
    @_ = _rearrange([-PATH,-VALID_PATH_PREFIXES],
                    [-PATH],@_);

    my $path        = shift;
    my $prefix_list = shift;

    return 1 if !$prefix_list;

    my $prefix;
    foreach $prefix (@$prefix_list) {
        if ($path =~ /^$prefix/) {
            return 1;
        }
    } 
    return 0;

} # end of _isInPathPrefixList

#
# untaintPath basically untaints a path. This is
# like untaintFilename except that it allows directory
# characters to exist. Double ..'s are not allowed to 
# exist.
#
# Regex is based on isPath method
#
sub untaintPath {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,
                     -EXIST_CHECK,
                     -VALID_PATH_PREFIXES,
                     -ADD_PATH_PREFIX,
                     -FIELD_NAME,-ERROR_MESSAGE],
                    [-FIELD_VALUE],@_);
    
    my $field           = shift;
    $field = "" if (!defined($field));
    my $exist_check     = shift;
    my $valid_path_list = shift;
    my $add_path_prefix = shift || "";
    my $field_name      = shift || "unknown";
    my $error_msg       = shift  
                            || "%FIELD_NAME% field is not a valid path.";

    # if the field does not exist then
    # we assume it is untainted rather than
    # causing an error due to an uninitialized value

    return "" if ($field =~ /^\s*$/);
            
    # The first item is to check the path
    # is valid.
    # 
    # The second item makes sure not more than
    # 2 periods in a row (to signify going up
    # the directory tree).
    #
    # After we cleared multiple dots, we
    # can allow the filename to consist of
    # any letters, digits, underscores (word chars)
    # dashs, and periods...
    #
    # Note that in the case of untainting the path, we don't
    # wish to check the existence until it has passed
    # all other obvious taint checks.

    if ($self->isPath(-FIELD_VALUE => $field, -EXIST_CHECK => 0,
                      -ADD_ERROR => 0) &&
        $field !~ /(\\?\.){2,}/ &&  # remember that backslashed dots may
                                    # count as well in some shells.
        $field =~ /
                   ^           # from the start
                   \s*         # allow surrounding whitespace
                   ([\w\-.]+    # start with any path char except no slashes
                   [\/:\w\-.]*) # any path characters including slashes 
                   \s*         # allow surrounding whitespace
                   $           # to the end
                  /x &&
        $self->_isInPathPrefixList(-PATH => $field,
                                   -VALID_PATH_PREFIXES => 
                                       $valid_path_list) &&
        (!$exist_check || -e ($add_path_prefix . $field))) {
        return $add_path_prefix . $1;
    } else {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $error_msg)  
           )
        );
        return undef;
    }

} # end of untaintPath

1;

