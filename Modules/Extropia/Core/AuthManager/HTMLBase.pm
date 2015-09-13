#$Id: HTMLBase.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::AuthManager::HTMLBase;

use Extropia::Core::Base qw(_rearrange);
use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub generateHiddenTagsToPreservePreviousFormVars {
    my $self = shift;
    @_ = _rearrange([-CGI_OBJECT],[-CGI_OBJECT],@_);

    my $cgi = shift;

    my @tags = $cgi->param();
    my $tag;
    my $hidden_tags = "";
    foreach $tag (@tags) {
        if ($tag !~ /^auth/i) {
            my @values = $cgi->param($tag);
            my $value;
            foreach $value (@values) {
                $hidden_tags .=
                    qq{<INPUT TYPE="HIDDEN" NAME="$tag" VALUE="$value">};
            }
        }
    }
    return $hidden_tags;

} # end of generateHiddenTagsToPreservePreviousFormVars

1;

