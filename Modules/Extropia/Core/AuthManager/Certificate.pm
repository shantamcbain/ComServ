#$Id: Certificate.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::AuthManager::Certificate;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);

use Extropia::Core::Auth;
use Extropia::Core::AuthManager;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::AuthManager);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -CLIENT_CERTIFICATE_VARIABLE,
       -DECODE_BASE64_CERTIFICATE,
       -USERNAME_MAPPING,
       -USER_FIELDS,
       -USER_FIELD_TYPES,
    ],
    [
       -AUTH_PARAMS,
    ],@_);

    $self = _assignDefaults($self,{-DECODE_BASE64_CERTIFICATE => 0});
    bless $self, ref($package) || $package;
    my $auth = $self->getAuthObject();
    $auth->setUsername($self->_getClientCertificateUser());

    return $self;

}

#
# isAuthenticated returns true if the user has successfully
# entered this application with a valid client-side certificate.
#
sub isAuthenticated {
    my $self = shift;

    if ($self->_getClientCertificateUser()) {
        return 1;
    }
    return 0;
}

#
# Authenticate.  In AuthManager::ClientCertificate
# we authenticate against a client certificate environment variable.
# This variable has been set if the Web Server has already
# figured out who the user is based on the client certificate.
#
# We've already authenticated via the certificate on the web server!
#
sub authenticate {
    my $self = shift;

    return 1;
  
} # end of authenticate

#
# _getClientCertificateUser obtains the remote user information (the user
# logged in via a client certificate authentication
#
sub _getClientCertificateUser {
    my $self = shift;

    my $cert_var         = $ENV{$self->{-CLIENT_CERTIFICATE_VARIABLE}};
    my $username_mapping = $self->{-USERNAME_MAPPING};

    if ($self->{-DECODE_BASE64_CERTIFICATE}) {
        require MIME::base64;
        $cert_var = MIME::base64::decode($cert_var);
    }

#
# Define certificate data defaults...
#
# Apache + mod_ssl can store the client certificate id in
# SSL_CLIENT_S_DN_UID as an x509 variable.
#
# Netscape Enterprise Server is a bit more inconsistent so
# a couple choices are tried. First, CLIENT_CERT_SUBJECT_UID
# is tried. If that is not defiend, we try the whole DN and
# provide a mapping to pull out the UID.
#
# http://www.inetmi.com/pubs/Netscape/enterprise contains
# a sample list of client cert variables for 
    if (!defined($cert_var)) {
        my $server_software = $ENV{'SERVER_SOFTWARE'};
        if ($server_software =~ /Apache/i) {
            $cert_var = $ENV{'SSL_CLIENT_S_DN_UID'};
        } else {
            $cert_var = $ENV{'CLIENT_CERT_SUBJECT_UID'};
            if (!$cert_var) {
                $cert_var = $ENV{'CLIENT_CERT_SUBJECT_DN'};
                $username_mapping =
                    "uid\s*=\s*\"\s*(.*)\s*\"*";
            }
        }
        if (!defined($cert_var)) {
            die ("No Certificate variable was defined.");
        }
    }
    if (!defined($username_mapping)) {
        return $cert_var;
    } else {
        $cert_var =~ /$username_mapping/i;
        return $1;
    }

} # end of _getClientCertificateUser

1;
