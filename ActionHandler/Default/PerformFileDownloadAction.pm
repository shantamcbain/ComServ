package Default::PerformFileDownloadAction;

# Copyright (C) 1994 - 2001  eXtropia.com
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

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::View;
use vars qw(@ISA);
@ISA = qw(Extropia::Core::View);

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use Extropia::Core::Action;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Action);

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash([
        -CGI_OBJECT,
        -UPLOAD_MANAGER_CONFIG_PARAMS
            ],
            [
        -CGI_OBJECT
            ],
        @_
    );

    my $cgi     = $params->{'-CGI_OBJECT'};

    if (defined($cgi->path_info()) &&
            $cgi->path_info() =~ /download/i) {

        if (!$params->{-UPLOAD_MANAGER_CONFIG_PARAMS}) {
            die("You forgot to include -UPLOAD_MANAGER_CONFIG_PARAMS " .
                "in the app config");
        }

        require Extropia::Core::UploadManager;
        my $upload_manager = Extropia::Core::UploadManager->create(
                @{$params->{-UPLOAD_MANAGER_CONFIG_PARAMS}});
        $upload_manager->displayUploadedFile(-URL =>
                                            $cgi->path_info());
        exit(0);
    }
    return 0;
}
