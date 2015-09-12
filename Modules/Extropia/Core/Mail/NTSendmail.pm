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

package Extropia::Core::Mail::NTSendmail;

use vars qw($VERSION @ISA);
$VERSION = "1.0";
@ISA = qw(Extropia::Core::Mail);

use strict;
use Extropia::Core::Base qw(
    _rearrange
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

$|=1;

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
        -MAIL_PROGRAM_PATH
            ],
            [],
        @_
    );

    if(!defined($self->{'-MAIL_PROGRAM_PATH'})) {
        $self->{'-MAIL_PROGRAM_PATH'}=_getMailerIfNotSpecified();
    }

    _dieIfRemainingParamsExist(@_);

    return bless $self, $package;
}

sub _getMailerIfNotSpecified {
    my $mailer  = 'c:\\inetpub\\scripts\\sendmail.exe';
    my $mailer1 = 'c:\\cgi\\scripts\\sendmail.exe';
    my $mailer2 = 'c:\\Progra~1\\sendmail\\sendmail.exe';
  
    if ( -e $mailer) { return $mailer; } 
    elsif ( -e $mailer1) { return $mailer1; } 
    elsif ( -e $mailer2) { return $mailer2; } 
    else {
        print "Content-type: text/html\n\n";
        print "I can't find NT sendmail, shutting down...<br>";
        print "Please set up the \$mailer variable in the NTSendmail.pm";
        die();
    }
}

sub send {
    my $self = shift;
    @_ = _rearrange([
        -FROM,
        -TO,
        -CC,
        -BCC,
        -REPLY_TO,
        -SUBJECT,
        -BODY,
           ],
           [
        -FROM,
        -TO,
        -SUBJECT,
        -BODY
            ], 
        @_
    );

    my $from     = shift;
    my $to       = shift;
    my $cc       = shift;
    my $bcc      = shift;
    my $reply_to = shift;
    my $subject  = shift;
    my $body     = shift;
    my $path     = $self->{'-MAIL_PROGRAM_PATH'};

    _dieIfRemainingParamsExist(@_);

    if(ref $to eq "ARRAY") {
        $to = join",",@$to;
    }

    if($cc ne "") {
        if(ref $cc eq "ARRAY") {
            $cc = join",",@$cc;
        }
    }

    if($bcc ne "") {
        if(ref $bcc eq "ARRAY") {
            $cc = join",",@$bcc;
        }
    }


    my $old_path = $ENV{"PATH"};
    $ENV{"PATH"} = "";

    open (MAIL, "|$path -t");
    $ENV{"PATH"} = $old_path;

# entering From before To, and using the -t option, overrides
# the value set up in the sendmail.ini file

my $mail =  qq!From: $from
To: $to
Cc: $cc
Bcc: $bcc
Subject: $subject

$body

!;
    print MAIL $mail;
    close (MAIL);
}
1;
