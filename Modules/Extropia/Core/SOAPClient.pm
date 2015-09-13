# $Id: SOAPClient.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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
# Defines routines to help Extropia objects send SOAP Requests
# and get data back.
# 
package Extropia::Core::SOAPClient;

use Carp;
use strict;
#
# we will use _rearrangeAsHash and _assignDefaults from Base,
# but we cannot import them because Base relies on Error. Therefore
# we cannot import statements from Base until Error has been
# fully compiled. But Error will not fully compile until the
# statements have been imported.
#
# Thererfore, the routines in Base will be prefixed with 
# Extropia::Core::Base:: to reference them in that package directly from
# this module.
#
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults); 
use IO::Socket;

use vars qw($VERSION @ISA);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::Base);

sub new {
    my $package = shift;
    my ($self) = Extropia::Core::Base::_rearrangeAsHash(
                    [-SOAP_URI,
                     -SOAP_URN,
                     -SOAP_HOST,
                     -SOAP_PORT,
                     -SOAP_TIMEOUT],
                    [-SOAP_HOST, -SOAP_PORT, -SOAP_URN, -SOAP_URI],
                    @_);

    $self = Extropia::Core::Base::_assignDefaults($self,{
                              -SOAP_TIMEOUT => 20
                             });

    return bless $self, $package;

}

sub sendSOAPRequest {
    my $self = shift;
    @_ = _rearrange([-METHOD,-REQUEST_XML,-SEND_SOAP_FAULT],
                    [-METHOD,-REQUEST_XML],@_);

    my $method          = shift;
    my $request_xml     = shift;
    my $send_soap_fault = shift || 0;

    my $host    = $self->{-SOAP_HOST};
    my $port    = $self->{-SOAP_PORT};
    my $timeout = $self->{-SOAP_TIMEOUT};
    my $urn     = $self->{-SOAP_URN};
    my $uri     = $self->{-SOAP_URI};

    my $soap_envelope = "<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" SOAP-ENV:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:xsi=\"http://www.w3.org/1999/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/1999/XMLSchema\" >
<SOAP-ENV:Body>
<m:$method xmlns:m=\"urn:$urn\">
$request_xml
</m:$method> 
</SOAP-ENV:Body> 
</SOAP-ENV:Envelope>
";

    my $soap_length = length($soap_envelope);

    my $request = qq{POST $uri HTTP/1.1
Content-Type: text/xml
Content-length: $soap_length
SOAPAction: urn:$urn

$soap_envelope};

    my $socket_msg;

    my $socket = IO::Socket::INET->new(PeerAddr => $host,
                                    PeerPort => $port,
                                    Proto    => 'tcp',
                                    Type     => SOCK_STREAM,
                                    Timeout  => $timeout)
    or $socket_msg = "Couldn't connect to $host: $@\n";

    if ($socket_msg) {
        die($socket_msg);
    }

    my $response = "";
    print $socket $request;
#print $request;
    while (<$socket>) {
        $response .= $_;
    }
    close($socket);

    if (defined($response)) {
        my $soap_fault = $self->__getSOAPFault($response);
        if (defined($soap_fault)) {
            $self->addError(
                    -MESSAGE => $soap_fault
                    );
            if ($send_soap_fault) {
                return $response;
            } else {
                return undef;
            }
        }
    }
    return $response;

} # end of sendSOAPRequest

sub __getSOAPFault {
    my $self = shift;

    my $soap_response = shift;

    if ($soap_response =~ /<\s*SOAP-ENV:Fault\s*>/i) {
        if ($soap_response 
                =~ /<\s*faultstring\s*>(.*)<\s*\/faultstring\s*>/i) {
            return $1;
        } else {
            die("Problem reading SOAP FaultString in response: $soap_response");
        }
    } 
    return undef;

} # end of __getSOAPFault

1;

__END__

