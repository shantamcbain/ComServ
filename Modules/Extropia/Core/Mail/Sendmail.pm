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

package Extropia::Core::Mail::Sendmail;

use vars qw($VERSION @ISA);
$VERSION = "1.0";
@ISA = qw(Extropia::Core::Mail);

use strict;
use Extropia::Core::Base qw(
    _rearrange
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
        -MAIL_PROGRAM_PATH
            ],
            [],
        @_
    );

    _dieIfRemainingParamsExist(@_);

    if(!defined($self->{'-MAIL_PROGRAM_PATH'})) {
        $self->{'-MAIL_PROGRAM_PATH'}=_getMailerIfNotSpecified();
    }

    return bless $self, $package;
}

sub _getMailerIfNotSpecified {
    my $mailer  = '/usr/bin/sendmail';
    my $mailer1 = '/usr/lib/sendmail';
    my $mailer2 = '/usr/sbin/sendmail';

    if ( -e $mailer) { return $mailer; } 
    elsif ( -e $mailer1) { return $mailer1; } 
    elsif ( -e $mailer2) { return $mailer2; } 
    else {
        print "Content-type: text/html\n\n";
        print "I can't find sendmail, shutting down...<br>";
        print "Whoever set this machine up put it someplace weird.";
        die();
    }
}

sub send {
    my $self = shift;
    @_ = Extropia::Core::Mail::_rearrange([
        -FROM,
        -TO,
        -BODY,   
        -SUBJECT,
        -REPLY_TO,
        -CC,
        -BCC,
            ],
            [
        -FROM,
        -TO,
        -BODY,
        -SUBJECT
            ],
        @_
    );
      
    my $from    = shift || "";
    my $to      = shift || "";
    my $body    = shift || "";
    my $subject = shift || "";
    my $replyto = shift || "";
    my $cc      = shift || "";
    my $bcc     = shift || "";
    my $path    = $self->{'-MAIL_PROGRAM_PATH'};

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

    my $old_path = $ENV{"PATH"};
    $ENV{"PATH"} = "";

    local (*OUT, *IN, *ERR);

    use IPC::Open3 ();

    my ($stdin,$stdout);
    if ($ENV{MOD_PERL} and $] > 5.005) {
        # this is a quick hack for mod_perl/perl5.6+ suggested at:
        # http://forum.swarthmore.edu/epigone/modperl/thansnayi
        # META: it's not clean, generates warnings about untie...
        $stdin  = tied *STDIN;
        $stdout = tied *STDOUT;
        untie *STDIN;
        untie *STDOUT;
    }

    IPC::Open3::open3(*OUT, *IN, *ERR, "$path -t");
    # META: need to trap a possible failure, see the manpage

    $ENV{"PATH"} = $old_path;

my $mail =  qq!To: $to
From: $from
Replyto: $replyto
Cc: $cc
Bcc: $bcc
Subject: $subject

$body

!;

    print OUT $mail;
    close (OUT);
    close (IN);
    close (ERR);

    if ($ENV{MOD_PERL} and $] > 5.005) {
        # continued, the comment from identical if() above
        tie *STDIN,  ref $stdin,  $stdin;
        tie *STDOUT, ref $stdout, $stdout;
    }
}
1;
