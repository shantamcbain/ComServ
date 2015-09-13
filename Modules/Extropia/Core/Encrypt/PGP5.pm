#$Id: PGP5.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Encrypt::PGP5;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash
                      _dieIfRemainingParamsExist);

use IPC::Open3;

use vars qw(@ISA $VERSION @POSSIBLE_PGP_BINARY_LOCATIONS);
@ISA = qw(Extropia::Core::Encrypt);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
@POSSIBLE_PGP_BINARY_LOCATIONS = (
        '/usr/local/bin/pgpe',
        '/usr/bin/pgpe',
        '/opt/bin/pgpe',
        '/bin/pgpe'
        );

# $encrypt = new Extropia::Core::Encrypt(-TYPE => "PGP5",
#
#
# $encrypted_text = $encrypt->encrypt($some_text);
# if ($encrypt->compare($some_text,$encrypted_text)) {
#   print "It matches\n";
# }
sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
            -PGP_PUBLIC_KEY_NAME,
            -PGP_BINARY_PATH,
            -PGP_CONFIG_PATH,
            -PGP_TEMP_DIR
           ],
           [-PGP_PUBLIC_KEY_NAME],@_);

    if (!$self->{-PGP_BINARY_PATH}) {
        my $binary_path;
        foreach $binary_path (@POSSIBLE_PGP_BINARY_LOCATIONS) {
            if (-e $binary_path && -x $binary_path) {
                $self->{-PGP_BINARY_PATH} = $binary_path;
                last;
            }
        }
    }
    if (!$self->{-PGP_BINARY_PATH}) {
        die("Could not determine path to PGP Binary: pgpe.");
    }
    if (!-e $self->{-PGP_BINARY_PATH}) {
        die($self->{-PGP_BINARY_PATH} . " does not exist.");
    }
    if (!-x $self->{-PGP_BINARY_PATH}) {
        die($self->{-PGP_BINARY_PATH} . " is not executable.");
    }
    
    _dieIfRemainingParamsExist(@_);

    return bless $self, $package;

} # end of constructor

sub encrypt {
    my $self = shift;
    @_ = _rearrange([-CONTENT_TO_ENCRYPT],[-CONTENT_TO_ENCRYPT],@_);

    my $content_to_encrypt = shift;
    my $encrypted_content  = "";

# Set the PGPPATH environment to tell
# PGP *not* to go to the Web Server User's
# home directory by default to look for key
# files and public keys
#
  if ($self->{-PGP_CONFIG_PATH}) {
    $ENV{"PGPPATH"} = $self->{-PGP_CONFIG_PATH};
  }

# Generate the command that needs to be used
# to execute PGP. This consists of the PGP
# executable followed by command line options
# which is followed by the user id which you
# want to use a public key for and then output
# the encrypted results to an output file.
#
  my $pgp_path    = $self->{-PGP_BINARY_PATH};
  my $pgp_options = "-atz -f -r";
  my $pgp_public_key_user_id = $self->{-PGP_PUBLIC_KEY_NAME};

  my $pgp_command =  "$pgp_path $pgp_options ";
  $pgp_command   .= "$pgp_public_key_user_id ";

#  We removed output files when we went with IPC::Open3
#  method of launching the pgp command...
#
#  $pgp_command   .= "-o $output_file";

# The command is opened using the special
# file open PIPE command which EXECUTES the
# command and then allows PERL to print to
# it as input for the command.
#
# The path manipulation is to satisfy taint mode
#

    local *PGPREAD;
    local *PGPWRITE;
    local *PGPERR;
    
    local $ENV{"PATH"} = "";
    local $ENV{"ENV"} = "";
    local $ENV{"IFS"} = "";

    #
    # use IPC::Open3 to open three streams to the file...
    #
    my $pid = open3 (\*PGPWRITE, \*PGPREAD, \*PGPERR, "$pgp_command"); 
    if (!$pid) {
        die("$pgp_command did not open: $!\n");
    }

    # The text you want to encrypt is sent to
    # the command.
    print PGPWRITE $content_to_encrypt;

    close (PGPWRITE);

    while (<PGPREAD>) {
        $encrypted_content .= $_;
    }
    close (PGPREAD);

    my $error_messages = "";
    while (<PGPERR>) {
        $error_messages .= $_;
    }
    close PGPERR;

    if (!$encrypted_content) {
        $encrypted_content = "No data was returned from PGP.\n";
        if ($error_messages) {
            $error_messages = "Error output from PGP showed " .
                                  "the following:\n\n$error_messages";
            die($error_messages);
        }
    }

    # we return pgp output

    return $encrypted_content;

} # end of encrypt

sub compare {
    my $self = shift;

    die("compare is not implemented in the Extropia::Core::Encrypt::PGP5 driver");
}


1;

