#$Id: FormVar.pm,v 1.3 2001/05/22 05:50:47 gunther Exp $
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

package Extropia::Core::SessionManager::FormVar;
use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::SessionManager;

use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::SessionManager);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.3 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;

    my $self;
    ($self,@_) = _rearrangeAsHash([
                    -CGI_OBJECT,
                    -FORM_VAR_NAME,
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
                        -FORM_VAR_NAME           => 'session_id',
                        -INVALIDATE_OLD_SESSIONS => 0,
                        -INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION => 1,
                        -INVALIDATE_OLD_SESSIONS_AT_GET_SESSION    => 0,
                        -INVALIDATE_OLD_SESSIONS_PROBABILITY       => 1 # 1%
                        });

    return $self;
}

sub _extractSessionId {
    my $self = shift;

    my $cgi           = $self->{-CGI_OBJECT};
    my $form_var_name = $self->{-FORM_VAR_NAME};

    return($cgi->param($form_var_name));
}

sub _changeSessionId {
    my $self = shift;
    my $new_session_id = shift;

    my $cgi           = $self->{-CGI_OBJECT};
    my $form_var_name = $self->{-FORM_VAR_NAME};


    $cgi->delete($form_var_name);
    $cgi->param($form_var_name, $new_session_id);
}

1;
