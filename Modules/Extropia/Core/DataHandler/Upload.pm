#$Id: Upload.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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
package Extropia::Core::DataHandler::Upload;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

use Extropia::Core::UploadManager;

sub getHandlerRules {
    my $self = shift;

    return {
        -UPLOAD_FILE => [$self,\&uploadFile]
    };
} # getHandlerRules

sub uploadFile {
    my $self = shift;
    @_ = _rearrange([
        -FIELD_VALUE,
        -FIELD_NAME,
        -UPLOAD_MANAGER_PARAMS
            ],
            [
        -FIELD_VALUE,
        -UPLOAD_MANAGER_PARAMS
            ],
        @_
    );

    my $field                  = shift;
    $field = "" if (!defined($field));
    my $field_name             = shift || "unknown";
    my $upload_manager_params  = shift;

    my $upload_manager = Extropia::Core::UploadManager->create(
                                @$upload_manager_params
                                );

    my $url = $upload_manager->storeUploadedFile();

    if ($url) {
        return $url;
    } else {
        if ($upload_manager->getErrorCount()) {
            $self->addError($upload_manager->getLastError());
        }
        return undef;
    }

} # end of uploadFile


1;

