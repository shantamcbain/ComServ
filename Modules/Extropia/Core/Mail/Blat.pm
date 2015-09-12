package Extropia::Core::Mail::Blat;
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


use vars qw($VERSION @ISA);
$VERSION = "1.0";
@ISA = qw(Extropia::Core::Mail);

use Carp;
use strict;

use Extropia::Core::DataHandler;
use Extropia::Core::UniqueFile;
use Extropia::Core::Base qw(
    _rearrange 
    _rearrangeAsHash
    _dieIfRemainingParamsExist
);

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
        -MAIL_PROGRAM_PATH,
        -UNIQUE_FILE_PARAMS
            ],
            [
            ],
        @_
    ); 

    _dieIfRemainingParamsExist(@_);
	
    if(!defined($self->{'-MAIL_PROGRAM_PATH'})) {
        $self->{'-MAIL_PROGRAM_PATH'}=_getMailerIfNotSpecified();
    }

    return bless $self, $package;
}

sub _getMailerIfNotSpecified {
    my $mailer  = 'c:\\Progra~1\\Blat\\blat.exe';
    my $mailer1 = 'c:\\Blat\\blat.exe';
    my $mailer2 = 'c:\\Progra~1\\Mail\\Blat\\blat.exe';

    if    (-e $mailer)  { return $mailer; } 
    elsif (-e $mailer1) { return $mailer1; } 
    elsif (-e $mailer2) { return $mailer2; } 
    else {
        print "Content-type: text/html\n\n";
        print "I can't find blat.exe, shutting down...<br>";
        print "Whoever set this machine up put it someplace weird.";
        die();
    }
}

sub send {
    my $self = shift;
    @_ = _rearrange([
        -FROM,
        -TO,
        -REPLY_TO,
        -CC,
        -BCC,
        -SUBJECT,
        -BODY,
        -ATTACH
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
    my $reply_to = shift;
    my $cc       = shift;
    my $bcc      = shift;
    my $subject  = shift;
    my $body     = shift;
    my $attach   = shift;

    _dieIfRemainingParamsExist(@_);

    my $path     = $self->{'-MAIL_PROGRAM_PATH'};

    my $uf = Extropia::Core::UniqueFile->new(
        @{$self->{-UNIQUE_FILE_CONFIG_PARAMS}}
    );

    my $fileName = $uf->createFile();
    defined($fileName) or 
        confess("Failed to create unique file in Blat->send()");
	
    open (MAIL_BODY, ">$fileName");
    print MAIL_BODY $body;
    close (MAIL_BODY);

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

    my @blatCommand = (
        $path,
        "$fileName",
        '-q',
        '-t',
        $to,
        '-f',
        $from,
        '-s',
        "\"$subject\""
    );
	
    if($attach ne "") {
        push(@blatCommand,"-attach");
        push(@blatCommand,"$attach");
    }

    if($cc ne "") {
        push(@blatCommand,"-c");
        push(@blatCommand,"$cc");
    }
	
    if($bcc ne "") {
        push(@blatCommand,"-b");
        push(@blatCommand,"$bcc");
    }

    system(@blatCommand);
    eval {
        $uf->destroyFile()
    };

    if($@) {
        confess("ERROR: $@ while trying to destroy " .
                "unique file in Blat->send()");
    }
}

1;
