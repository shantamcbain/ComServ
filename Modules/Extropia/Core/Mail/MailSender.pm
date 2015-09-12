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

package Extropia::Core::Mail::MailSender;

use vars qw($VERSION @ISA);

$VERSION = "1.0";
@ISA = qw(Extropia::Core::Mail);

use strict;
use Mail::Sender;
use Extropia::Core::Base qw(
    _rearrange
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
        -SMTP_ADDRESS
            ],
            [
        -SMTP_ADDRESS
            ],
        @_
    );

    _dieIfRemainingParamsExist(@_);

    return bless $self, $package;
}

sub send {
    my $self = shift;
    my $sender;

    @_ = Extropia::Core::Mail::_rearrange([
        -FROM,
        -TO,
        -BODY,
        -SUBJECT,
        -REPLY_TO,
        -CC,
        -BCC,
        -ATTACH
            ],
            [
        -FROM,
        -TO,
        -BODY,
        -SUBJECT
            ],
        @_
    );

    my $from    = shift;
    my $to      = shift;
    my $message = shift;
    my $subject = shift;
    my $replyto = shift || $from;
    my $cc      = shift || "";
    my $bcc     = shift || "";
    my $file    = shift || "";

    _dieIfRemainingParamsExist(@_);

    if(ref $to eq "ARRAY") {
        $to = join",",@$to;
    }

    if(ref $cc eq "ARRAY") {
        $cc = join",",@$cc;
    }

    if(ref $bcc eq "ARRAY") {
        $bcc = join",",@$bcc;
    }

# for Mail::Sender we must untaint the mail address
# because the smtp address gets tainted in a roundabout way.
# So this is a kludge to fix it.
#
# 
    $to =~ /(.*)/;
    $to = $1;

    ref ($sender = Mail::Sender->new({
        from	=> $from,
        to	=> $to,
        smtp	=> $self->{'-SMTP_ADDRESS'},
        subject	=> $subject,
        replyto	=> $replyto,
        cc	=> $cc,
        bcc	=> $bcc,
        file    => $file
    })) or die("$Mail::Sender::Error");

    if ($file ne '') {
        ref($sender->MailFile({msg=>$message,file=>$file})) or
            die($Mail::Sender::Error);
    }

    else {

        ref($sender->MailMsg({msg=>$message})) or
            die($Mail::Sender::Error);
    }

    $sender->Close();
}
1;
