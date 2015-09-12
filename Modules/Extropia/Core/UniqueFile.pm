#$Id: UniqueFile.pm,v 1.2 2001/06/08 13:01:23 stas Exp $
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

package Extropia::Core::UniqueFile;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::KeyGenerator;
use Fcntl; # loads Fcntl constants...

use vars qw(@ISA $VERSION $OS $SL $TEMPDIRECTORY);
@ISA = qw(Extropia::Core::Base);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# Initialize OS Specific Parameters
#
# Based on Code in CGI.pm by Lincoln Stein
#

# FIGURE OUT THE OS WE'RE RUNNING UNDER
# Some systems support the $^O variable.  If not
# available then require() the Config library
unless ($OS) {
    unless ($OS = $^O) {
        require Config;
        $OS = $Config::Config{'osname'};
    }
}
if ($OS=~/Win/i) {
    $OS = 'WINDOWS';
} elsif ($OS=~/vms/i) {
    $OS = 'VMS';
} elsif ($OS=~/^MacOS$/i) {
    $OS = 'MACINTOSH';
} elsif ($OS=~/os2/i) {
    $OS = 'OS2';
} else {
    $OS = 'UNIX';
}

# The path separator is a slash, backslash or semicolon, depending
# on the platform. 
$SL = {
    UNIX=>'/', OS2=>'\\', WINDOWS=>'\\', MACINTOSH=>':', VMS=>'/'
}->{$OS};

sub new {
    my $package = shift;
    if (ref($package)) {
        croak(ref($package) . " cannot be cloned.");
    }

    my $self;
    ($self, @_) = _rearrangeAsHash(
      [
       -KEY_GENERATOR_PARAMS,
       -EXTENSION,
       -DIRECTORY,
       -NUMBER_OF_TRIES,
       -SELF_DESTRUCT
      ],[],@_);

    $self = _assignDefaults($self, 
            {-KEY_GENERATOR_PARAMS => [-TYPE => 'POSIX'],
             -EXTENSION            => 'dat',
             -DIRECTORY            => findTempDirectory(),
             -NUMBER_OF_TRIES      => 5
            });

    my $key_generator = Extropia::Core::KeyGenerator->create(
            @{$self->{-KEY_GENERATOR_PARAMS}});

    $self->{_key_generator} = $key_generator;

    if ($self->{-DIRECTORY} !~ /(\Q$SL\E|\/)$/) {
        $self->{-DIRECTORY} .= $SL;
    }

    return bless $self, $package;
    
} # end of constructor (new)

# 
# getFile - get the unique filename and path
#
sub getFilePath {
    my $self = shift;

    if (!defined($self->{_unique_file_path})) {
        die("Unique file must be created before getting a file!");
    }
    return $self->{_unique_file_path};

} # end of getFilePath

#
# getFilename - get the unique filename alone
#
sub getFilename {
    my $self = shift;

    my $file = $self->{_unique_file_path};
    if (!defined($file)) {
        die("Unique file must be created before getting a file!");
    }

    my $filename;
    if ($file =~ /^.*(\Q$SL\E|\/)(.*)$/) {
        $filename = $2;
    } else {
        $filename = $file;
    }
    return $filename;
}

#
# setFile - set the unique filename (for cleanup utility)
#
sub setFile {
    my $self = shift;
    @_ = _rearrange([-FILE],[-FILE],@_);

    my $file = shift;

    if ($self->{_unique_file_path}) {
        die("Can't set unique file if one already exists!");
    } 
    $self->{_unique_file_path} = $file;

} # end of setFile

#
# create the unique file based on parameters
# set up in the constructor
#
sub createFile {
    my $self = shift;

    if ($self->{_unique_file_path}) {
        return $self->{_unique_file_path};
    }

    my $kg = $self->{_key_generator};

    my $number_of_tries = $self->{-NUMBER_OF_TRIES};
    my $extension       = $self->{-EXTENSION};
    my $directory       = $self->{-DIRECTORY};

    local(*TEMP);
    my $full_path;
    for (1..$number_of_tries) {
        my $key_value = $kg->createKey(-EXTRA_ELEMENT => $_);
        $full_path = $directory . $key_value;
        if ($extension) {
            $full_path =~ s/\.$//;
            $full_path .= "." . $extension;
        }
        if (sysopen(TEMP,$full_path,O_CREAT|O_EXCL)) {
            close(TEMP);
            $self->{_unique_file_path} = $full_path;
            return $full_path;
        }
    }
    confess("Could not create unique file. The last attempt used " .
            "the filename: $full_path and received the following " .
            "error: $!");

} # end of createFile

#
# destroy the unique file
#
sub destroyFile {
    my $self = shift;

    unlink($self->{_unique_file_path}) ||
        die("Error deleting file: " .
            $self->{_unique_file_path} . ": $!\n");
    $self->{_unique_file_path} = undef;

} # end of destroyFile

#
# If the self destruct flag is on, then we 
# destroy the temp file when this object
# goes out of scope.
#
sub DESTROY {
    my $self = shift;

    $self->destroyFile() if ($self->{-SELF_DESTRUCT});

} # end of DESTROY

#
# findTempDirectory
# Find a potential temp directory based on
# routine in CGI.pm by Lincoln Stein.
#
# Includes compatibility for MacPerl! 
#
sub findTempDirectory {

    my $MAC = $OS eq 'MACINTOSH';
    my ($vol) = $MAC ? MacPerl::Volumes() =~ /:(.*)/ : "";
    unless (defined($TEMPDIRECTORY)) {
        my @TEMP=("${SL}usr${SL}tmp","${SL}var${SL}tmp",
          "C:${SL}temp","${SL}tmp","${SL}temp",
          "${vol}${SL}Temporary Items",
          "${SL}WWW_ROOT");
        unshift(@TEMP,$ENV{'TMPDIR'}) if exists $ENV{'TMPDIR'};
        unshift(@TEMP,(getpwuid($<))[7].'/tmp') if $OS eq 'UNIX';

        foreach (@TEMP) {
            do {$TEMPDIRECTORY = $_; last} if -d $_ && -w _;
        }
    }

    $TEMPDIRECTORY = $MAC ? "" : "." unless (defined($TEMPDIRECTORY));
    return $TEMPDIRECTORY;

} # end of findTempDirectory

1;

