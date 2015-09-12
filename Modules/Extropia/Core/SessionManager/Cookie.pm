#$Id: Cookie.pm,v 1.2 2001/05/22 05:50:47 gunther Exp $
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

package Extropia::Core::SessionManager::Cookie;
use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::SessionManager;

use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::SessionManager);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new{
    my $package = shift;

    my $self;
    ($self,@_) = _rearrangeAsHash([
                    -CGI_OBJECT,
                    -COOKIE_NAME,
                    -INVALIDATE_OLD_SESSIONS,
                    -INVALIDATE_OLD_SESSIONS_AT_GET_SESSION,
                    -INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION,
                    -INVALIDATE_OLD_SESSIONS_PROBABILITY,
                    -SESSION_PARAMS,
                    -COOKIE_PATH,
                    -COOKIE_DOMAIN,
                    -COOKIE_EXPIRES,
                    -COOKIE_SECURE,
                    -PRINT_COOKIE
                    ],[
                    -CGI_OBJECT,
                    -SESSION_PARAMS
                    ],@_);
    
    bless $self, ref($package) || $package;

# the default cookie path is the name of the script minus
# the script itself...
    my $default_cookie_path = $self->{-CGI_OBJECT}->url(-absolute=>1);
    $default_cookie_path =~ s/(.+\/).+\/?/$1/;
    
    $self = _assignDefaults($self, {
                        -COOKIE_NAME             => 'EXTROPIA_SESSION_ID',
                        -INVALIDATE_OLD_SESSIONS => 0,
                        -INVALIDATE_OLD_SESSIONS_AT_CREATE_SESSION => 1,
                        -INVALIDATE_OLD_SESSIONS_AT_GET_SESSION    => 0,
                        -INVALIDATE_OLD_SESSIONS_PROBABILITY       => 1, # 1%
                        -COOKIE_PATH             => $default_cookie_path,
                        -PRINT_COOKIE            => 1
                        });

    return $self;
}

sub createSession { 
    my $self = shift;

    my $session = $self->SUPER::createSession();

    if ($session && $self->{-PRINT_COOKIE}) {
        $self->_printCookie(-SESSION_OBJECT => $session);
    }
    return $session;
    
} # end of createSession

sub _extractSessionId {
    my $self = shift;

    my $cgi         = $self->{-CGI_OBJECT};
    my $cookie_name = $self->{-COOKIE_NAME};

    return ($cgi->cookie($cookie_name));
}

sub _printCookie {
    my $self = shift;
    @_ = _rearrange([-SESSION_OBJECT],[-SESSION_OBJECT],@_);

    my $session = shift;

    my $cgi            = $self->{-CGI_OBJECT};
    my $cookie_name    = $self->{-COOKIE_NAME};
    my $cookie_path    = $self->{-COOKIE_PATH};
    my $cookie_domain  = $self->{-COOKIE_DOMAIN};
    my $cookie_expires = $self->{-COOKIE_EXPIRES};
    my $cookie_secure  = $self->{-COOKIE_SECURE};

    my @cookie_params = (
            -name    => $cookie_name,
            -value   => $session->getId(),
            -path    => $cookie_path
            );

    if ($cookie_domain) {
        push (@cookie_params, -domain, $cookie_domain);
    }
    if ($cookie_expires) {
        push (@cookie_params, -expires, $cookie_expires);
    }
    if ($cookie_secure) {
        push (@cookie_params, -secure, $cookie_secure);
    }
    
	my $cookie = $cgi->cookie(@cookie_params);

	my $cookie_header = $cgi->header(-cookie=>$cookie);
	$cookie_header =~ s/content\-type.*//si;

	print $cookie_header;
}

1;
