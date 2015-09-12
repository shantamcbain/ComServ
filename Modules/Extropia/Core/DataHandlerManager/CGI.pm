#$Id: CGI.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::DataHandlerManager::CGI;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::Error;
use Extropia::Core::DataHandlerManager qw(VALIDATE UNTAINT TRANSFORM);

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandlerManager);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# construct a new datahandler manager
#
sub new {
    my $package = shift;
    $package = ref($package) || $package;

    my $self;
    ($self,@_) = _rearrangeAsHash([
                    -CGI_OBJECT,
                    -DATAHANDLERS,
                    -FIELD_MAPPINGS,
                    -RULES
                    ],[
                    -CGI_OBJECT,
                    -DATAHANDLERS
                    ],@_); 

    bless $self, $package;
    if ($self->{-RULES}) {
        $self->init(-RULES => $self->{-RULES});
    } else {
# must do the following to create a true copy of @_
        my @rules = @_;
        $self->init(-RULES => \@rules);
    }
    return $self;

} # end of constructor

sub _getDataStoreFieldList {
    my $self = shift;

    my $cgi = $self->{-CGI_OBJECT};

    return $cgi->param();

} # end of _getDataStoreFieldList

sub _getDataStoreValueList {
    my $self = shift;
    @_ = _rearrange([-FIELD],[-FIELD],@_);

    my $field = shift;

    my $cgi = $self->{-CGI_OBJECT};

    return $cgi->param($field);

} # end of _getDataStoreValues

sub _setDataStoreValueList {
    my $self = shift;
    @_ = _rearrange([-FIELD,-VALUE_LIST],[-FIELD,-VALUE_LIST],@_);

    my $field      = shift;
    my $value_list = shift;

    my $cgi = $self->{-CGI_OBJECT};

# If the returned information is undefined, it means 
# we want to clear the field completely ...
    my $val_list_length = @{$value_list};
    if ($val_list_length == 0 ||
        ($val_list_length == 1 && !defined($value_list->[0]))) {
        $cgi->delete($field);
    } else {
        $cgi->param($field,@{$value_list});
    }

} # end of _setDataStoreValueList

1;

