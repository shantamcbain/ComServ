#$Id: DataHandler.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::DataHandler;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _getDriver _rearrangeAsHash);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub create {
    my $package = shift;
    
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift;
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::DataHandler", $type) or
        Carp::croak("DataHandler type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

#
# Addtl methods to inherit in driver packages
#
sub new {
    my $package = shift;
    $package = ref($package) || $package;
    
    my ($self) = _rearrangeAsHash([-DATAHANDLER_MANAGER_OBJECT],[],@_);

    bless $self, $package;
    $self->_setDataHandlerManagerObject(
            -DATAHANDLER_MANAGER_OBJECT => shift);
    return $self;
} # end of new

#
# _getMessage creates an error message
# out of a message string and field value/name
# parameters
#
sub _getMessage {
    my $self = shift;
    @_ = _rearrange([-FIELD_NAME,-FIELD_VALUE,-MESSAGE],
                    [-FIELD_NAME,-FIELD_VALUE,-MESSAGE],@_);

    my $field_name  = shift || "";
    my $field_value = shift || "";
    my $msg         = shift || "";

    if (!ref($field_name)) {
        $msg =~ s/%FIELD_NAME%/$field_name/gi;
        $msg =~ s/%FIELD_VALUE%/$field_value/gi;
    } else {
        my %field_name_hash = @$field_name;
        my %field_value_hash = @$field_value;
        my $key;
        foreach $key (keys %field_name_hash) {
            my $value = $field_name_hash{$key};
            $key = substr($key,1);
            $msg =~ s/%$key%/$value/gi;
        }
        foreach $key (keys %field_value_hash) {
            my $value = $field_value_hash{$key} || "";
            $key = substr($key,1);
            $msg =~ s/%$key%/$value/gi;
        }
    }

    return $msg;

} # end of _getMessage

#
# addError() adds the error to the original DataHandler
# factory object.
# 
# This overrides the base object. If a DataHandler
# did not create this datahandler, then getError
# will simply call the superclass (in Extropia::Core::Base)
#
sub addError {
    my $self = shift;

    if ($self->_getDataHandlerManagerObject()) {
        $self->_getDataHandlerManagerObject()->addError(@_);
    } else {
        $self->SUPER::addError(@_);
    }

} # end of addError

#
# _getDataHandlerManagerObject gets the datahandler
# manager that created this datahandler object.
#
sub _getDataHandlerManagerObject {
    my $self = shift;

    return $self->{-DATAHANDLER_MANAGER_OBJECT};
} # end of _getDataHandlerManagerObject

#
# _setDataHandlerManagerObject sets the datahandler
# manager that created this datahandler object.
#
sub _setDataHandlerManagerObject {
    my $self = shift;
    @_ = _rearrange([-DATAHANDLER_MANAGER_OBJECT],[],@_);
    
    $self->{-DATAHANDLER_MANAGER_OBJECT} = shift;
} # end of _setDataHandlerManagerObject

1;
