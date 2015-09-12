#$Id: PathInfo.pm,v 1.2 2001/05/22 05:50:47 gunther Exp $
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

package Extropia::Core::SessionManager::PathInfo;

use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::SessionManager;

use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::SessionManager);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;

    my $self;
    ($self,@_) = _rearrangeAsHash([
                    -CGI_OBJECT,
                    -PATH_INFO_FIELD_INDEX,
                    -PATH_INFO_FIELD_NAME,
                    -INVALIDATE_OLD_SESSIONS,
                    -INVALIDATE_OLD_SESSIONS_AT_GET_SESSION,
                    -INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION,
                    -INVALIDATE_OLD_SESSIONS_PROBABILITY,
                    -SESSION_PARAMS
                    ],[
                    -CGI_OBJECT,
                    -SESSION_PARAMS
                    ],@_);

    bless $self, ref($package) || $package;

    $self = _assignDefaults($self, {
                        -INVALIDATE_OLD_SESSIONS => 0,
                        -INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION => 1,
                        -INVALIDATE_OLD_SESSIONS_AT_GET_SESSION    => 0,
                        -INVALIDATE_OLD_SESSIONS_PROBABILITY       => 1 # 1%
                        });

    if (!$self->{-PATH_INFO_FIELD_INDEX} &&
        !$self->{-PATH_INFO_FIELD_NAME}) {
        $self->{-PATH_INFO_FIELD_INDEX} = 0;
    }

    if ($self->{-PATH_INFO_FIELD_INDEX} &&
        $self->{-PATH_INFO_FIELD_NAME}) {
        die("Cannot set both -PATH_INFO_FIELD_INDEX and " .
            "-PATH_INFO_FIELD_NAME at the same time!");
    }
         
    return $self;
}

sub _extractSessionId {
    my $self = shift;

    my $cgi         = $self->{-CGI_OBJECT};
    my $field_index = $self->{-PATH_INFO_FIELD_INDEX};
    my $field_name  = $self->{-PATH_INFO_FIELD_NAME};

    my $path_info = $cgi->path_info();
    my $session_id;
    
# extract session id based on the index number of which 
# subdirectory number in path info has the session id... eg
# /FDJJJDSKFJ/2/3/4/5/6/etc... for an index of 1.
    if ($field_index) {
        return (split(/\//,$path_info))[$field_index];
    } 

# extract session id based on a special subdirectory name
# preceding the subdirectory that contains the session id... eg
# /session_id/FDJJJDSKFJ
    if ($path_info =~ /$field_name\/(.+)\/)/i) {
        return $1;
    } else {
        return undef;
    }
}

1;
