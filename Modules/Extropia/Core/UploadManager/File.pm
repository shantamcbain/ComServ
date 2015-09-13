# 	$Id: rv.cgi,v 1.1 2003/11/29 06:27:34 shanta Exp shanta $	
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

package Extropia::Core::UploadManager::File;

use Carp;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::UploadManager;

use strict;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::SessionManager);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.7 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;

    my $self;
    ($self,@_) = _rearrangeAsHash([
# Session has to be added so that info of the uploaded data can be stored in the session
# so that on 2nd execution of datahandler, it can be used.    		   
    		    -SESSION_OBJECT,
                    -CGI_OBJECT,
                    -UPLOAD_FIELD,
                    -UPLOAD_DIRECTORY,
                    -FIELD_TO_SET_UPLOAD_FILENAME,
                    -FIELD_TO_SET_UPLOAD_SIZE,
                    -KEY_GENERATOR_PARAMS,
                    -DEFAULT_FILE_EXTENSION,
                    -MIME_TYPES,
# The following was added because today's browsers know how to ungzip
# a file automatically...
                    -TREAT_GZ_EXTENSION_AS_CONTENT_ENCODING,
                    -ADD_SESSION_ID_TO_URL_AS_GET_PARAMETER,
                    -ACCEPT_MIME_TYPES,
],
                    [
                    -SESSION_OBJECT,
                    -CGI_OBJECT,
                    -UPLOAD_FIELD,
                    -ADD_SESSION_ID_TO_URL_AS_GET_PARAMETER,
                    -UPLOAD_DIRECTORY
                    ],@_);

    bless $self, ref($package) || $package;

    $self = _assignDefaults($self, {
                        -KEY_GENERATOR_PARAMS => [
                            -TYPE => 'Counter',
                            -COUNTER_FILE => 
                                $self->{-UPLOAD_DIRECTORY} . "/" .
                                "upload_file_counter.dat"
                                ],
                        -FIELD_TO_SET_UPLOAD_FILENAME => 'upload_filename',
                        -FIELD_TO_SET_UPLOAD_SIZE     => 'upload_size',
                        -DEFAULT_FILE_EXTENSION => ".dat",
                        -TREAT_GZ_EXTENSION_AS_CONTENT_ENCODING => 1
                        });

    if (!$self->{-MIME_TYPES}->{""}) {
        $self->{-MIME_TYPES} = {};
    }

    $self->{-MIME_TYPES} = _assignDefaults($self->{-MIME_TYPES},
                            {
                            'jpeg' => 'image/jpeg',
                            'jpg'  => 'image/jpeg',
                            'gif'  => 'image/gif',
                            'doc'  => 'application/msword',
                            'xls'  => 'application/vnd.ms-excel',
                            'ppt'  => 'application/vmd.ms-powerpoint',
                            'pdf'  => 'application/pdf',
                            'ps'   => 'application/postscript',
                            'rtf'  => 'application/rtf',
                            'tar'  => 'application/x-tar',
                            'zip'  => 'application/zip',
                            'au'   => 'audio/basic',
                            'snd'  => 'audio/basic',
                            'mp3'  => 'audio/mpeg',
                            'ra'   => 'audio/x-readaudio',
                            'wav'  => 'audio/x-wav',
                            'bmp'  => 'image/bmp',
                            'png'  => 'image/png',
                            'ram'  => 'audio/x-pn-readaudio',
                            'htm'  => 'text/html',
                            'html' => 'text/html',
                            'txt'  => 'text/plain',
                            'xml'  => 'text/xml',
                            'mpg'  => 'video/mpeg',
                            'mpeg' => 'video/mpeg',
                            'qt'   => 'video/quicktime',
                            'mov'  => 'video/quicktime',
                            'avi'  => 'video/x-msvideo',
                            'gz'   => 'application/x-gzip',
                            ''     => 'application/octet-stream'
                            });

    my @accept_mime_types = @{ $self->{-ACCEPT_MIME_TYPES} || [] };
    my @valid_exts = ();
    # since the mapping is not 1:1 we cannot just reverse the hash
    while (my ($k,$v) = each %{ $self->{-MIME_TYPES} || {} } ) {
        for (@accept_mime_types){
            push @valid_exts, $k if $_ && $k && $v && $v eq $_;
        }
    }

    $self->{-VALID_EXTS} = \@valid_exts;

    return $self;
}

#
# actually stores the file away somewhere...
#
#
# You can specify 
# -ACCEPT_MIME_TYPES => [qw(image/jpeg image/gif)],
# in @UPLOAD_MANAGER_CONFIG_PARAMS to accept only certain mime types
#
sub storeUploadedFile {
    my $self = shift;

    my $cgi              = $self->{-CGI_OBJECT};
    my $upload_field     = $self->{-UPLOAD_FIELD};
    my $upload_directory = $self->{-UPLOAD_DIRECTORY};
    my $kg_params        = $self->{-KEY_GENERATOR_PARAMS};
    my $upload_filename_field = $self->{-FIELD_TO_SET_UPLOAD_FILENAME};
    my $upload_size_field     = $self->{-FIELD_TO_SET_UPLOAD_SIZE};
    my $extension        = $self->{-DEFAULT_FILE_EXTENSION};
    my $session		 = $self->{-SESSION_OBJECT};	
	
    my $upload_filehandle = $cgi->upload($upload_field);

    if (!defined($upload_filehandle)) {

# URL check....................................................
# It will check if the file data has a valid URL 
# if it does it will return the url instead of undef.

# These codes are written to allow the files to upload even when 
# data handlers for upload file is executed 2 times.
# (one in the confirmation action, the other in the process action)
# The 2nd execution for the data handler does not work previously
# because the file data has the generated URL string instead of the 
# file directory and filename. And thus the 2nd upload always fail
# and this causes all upload file not able to work with confirmation.
# With this code, it will solve the problem.

	my $check_url = $cgi->param($upload_field);
	
	#Get the filename 
	my $upload_filename = $session->getAttribute(-KEY =>"upload_field_$upload_field");
	
	#Check if the filename is the same as the previous upload.
	if(defined($upload_filename) && defined($check_url)){
		
 	    if($upload_filename eq $check_url) {
	  
	        #Get the filename and filesize from the sesion 
	        my $filename = $session->getAttribute("-KEY"=>"$upload_filename_field");
    	        my $filesize = $session->getAttribute("-KEY"=>"$upload_size_field");
    	   
    	        $cgi->param($upload_filename_field, $filename);
    	        $cgi->param($upload_size_field, $filesize);
    	   
                return $check_url;
            }
               
	}
       

# End of URL check ...............................................       
        return undef;
    }

    my $upload = $cgi->param($upload_field) || '';
    my $filename;
    my $cd;

    if(ref($upload)) {
        my $cd;
        $cd = $cgi->uploadInfo($upload)->{'Content-Disposition'};
        $cd =~ /filename\s*=\s*"(.+)"/;
        $filename = $1;
    } else {
        $filename = $upload;
    }

    # if we have a restriction of what MIME_TYPES to accept, check for
    # ACCEPT_MIME_TYPES:
    if (my %accept_mime_types = map {$_ => 1} @{$self->{-ACCEPT_MIME_TYPES} || []}) {
        my $mime_type = $cgi->uploadInfo()->{'Content-Type'} || '';

        unless ($accept_mime_types{$mime_type}){
            my $error  = "The uploaded file $filename has an unacceptable format: $mime_type.";
            if (my @valid_exts = @{ $self->{-VALID_EXTS} || [] }) {
                $error .= "Valid extensions are: ". join(", ", @valid_exts) . ".";
            }
            $self->addError($error);
            return undef;
        }
    }

    my $key_generator = Extropia::Core::KeyGenerator->create(@$kg_params);
    my $counter       = $key_generator->createKey();

    binmode($upload_filehandle);
    local(*FILE);

    my $stripped_filename = 
        $self->stripFilename(-FILENAME => $filename);

    if ($upload_filename_field) {
        $cgi->param($upload_filename_field, $stripped_filename);
    } 
    
    open(FILE,">" . $upload_directory . "/" . $counter . $extension) or 
        die ("Tried to create $upload_directory/$counter$extension: $!");
    binmode(FILE);

    my $bytecount = 0;
    my $buffer;
    my $bytesread;
    while($bytesread = read($upload_filehandle,$buffer,1024)) {
        print FILE $buffer;
        $bytecount += $bytesread;
    }
    close($upload_filehandle);
    close(FILE);

    if ($upload_size_field) {
        $cgi->param($upload_size_field,$bytecount);
    }

    my $url = $cgi->script_name() ."?session_id=%SESSION_ID%". "&/download/" . $counter;
    $url .= "/" . $stripped_filename;
    if ($self->{-ADD_SESSION_ID_TO_URL_AS_GET_PARAMETER}) {
        $url .= "?session_id=%SESSION_ID%";
# Add file extension to session URL
#
#
# NOTE THAT THIS MUST BE DONE TO MAKE IT WORK WITH IE 5.0 on 
# WINDOWS 2000!
#
        if ($stripped_filename =~ /.*\.(.+)/) {
            $url .= "&.$1";
        }
    }

# Added these 3 fields into the session so that on 2nd execution of the upload data handler,
# the apps is able to capture the first generated url , the filename and the filesize without
# regenerating the url and upload the file.
    $session->setAttribute("-KEY"=>"upload_field_$upload_field","-VALUE"=>"$url");
    $session->setAttribute("-KEY"=>"$upload_filename_field","-VALUE"=>"$stripped_filename");
    $session->setAttribute("-KEY"=>"$upload_size_field","-VALUE"=>"$bytecount");
    $session->setAttribute("-KEY"=>"$site","-VALUE"=>"$bytecount");

    return $url;

} # end of storeUploadedFile

sub stripFilename {
    my $self = shift;
    @_ = _rearrange([-FILENAME],[-FILENAME],@_);
    
    my $filename = shift;

    my $newname = $filename;

# First check for forward slashes and then backslashes...
    if ($newname =~ m!.*/(.*)!) {
        $newname = $1;
    } 
    if ($newname =~ m!.*\\(.*)!) {
        $newname = $1;
    }

# Now clean out other unsavory stuff such as embedded whitespaces and double
# dots

    $newname =~ s/\s//g;
    $newname =~ s/\.\.//g;
    $newname =~ s/\.\\\.//g;

    return $newname;

} # end of stripFilename
  
sub displayUploadedFile {
    my $self = shift;
    @_ = _rearrange([-URL],[-URL],@_);

    my $cgi = $self->{-CGI_OBJECT};
    my $url = shift;

# *******************************************
# NOTE: THE FOLLOWING LINE IS VERY IMPORTANT
# IT MAKES SURE THAT THE FILENAME IS 
# DEFINITELY CONTAINS ONLY WORD CHARACTERS OR
# A DASH. THUS, NO FUNNY META CHARACTER
# PATH REDIRECTION (eg ..) CAN BE INSERTED 
# MALICIOUSLY.
#
# MODIFY AT YOUR OWN RISK.
# *******************************************
    if ($url =~ m!(.+)/([\w\-]+)/(.+)!) {
        my $filename = $2 . $self->{-DEFAULT_FILE_EXTENSION};
        my $original_filename = $3;
        my $mime_ext;
        if ($original_filename =~ /(.+)\.(.+)/) {
            $mime_ext = $2;
        } else {
            $mime_ext = "";
        }
        $mime_ext =~ tr/A-Z/a-z/;

        my @content_encoding_param = ();
        if (($mime_ext eq "gz") && 
            $self->{-TREAT_GZ_EXTENSION_AS_CONTENT_ENCODING}) {
            
            if ($original_filename =~ /(.+)\.(.+)\.(.+)/) {
                $mime_ext = $2;
                $mime_ext =~ tr/A-Z/a-z/;
                @content_encoding_param = (
                        '-content-encoding' => 'x-gzip'
                        );
            }
        }
        my $mime_type = $self->{-MIME_TYPES}->{$mime_ext};

        $filename = $self->{-UPLOAD_DIRECTORY} . "/" . $filename;
        my $filesize;
        my $filetime;
        ($filesize, $filetime) = (stat($filename))[7,9];

        $filetime    = scalar(gmtime($filetime)) . " GMT"; 
        my $currenttime = scalar(gmtime(time)) . " GMT";

# 
# The HTTP Header for Uploaded files is different than most.
# Since we know that this file is a raw file, we can output
# additional information such as the content-length and the
# age of the document so that proxies understand how to cache
# the data.
#
        local(*FILE);
        open(FILE, "<$filename") ||
            die("Could not open $filename for reading: $!");

        $| = 1;
        binmode(FILE);
        print $cgi->header(
                           -type => $mime_type,
                           '-content-length' => $filesize,
                           -date => $currenttime,
                           '-last-modified' => $filetime,
#'-accept-ranges' => 'bytes',
                           -charset => undef,
                           @content_encoding_param
                           );

        my $buffer;
        my $bytesread;
        while($bytesread = read(FILE, $buffer, 1024)) {
            print $buffer;
        }
        close (FILE);

    } else {
# Take care of CSS Security issue
        $url =~ s/\</&gt;/;
        die("The download URL: $url is not recognized by the Upload Mgr.");
    }

} # end of displayUploadedFile

sub deleteUploadedFile {
    my $self = shift;
    @_ = _rearrange([-URL],[-URL],@_);

    my $cgi = $self->{-CGI_OBJECT};
    my $url = shift;

    if ($url =~ m!(.+)/(.+)/(.+)\.?(.*)!) {
        my $filename = $2 . $self->{-DEFAULT_FILE_EXTENSION};
        $filename = $self->{-UPLOAD_DIRECTORY} . "/" . $filename;
        unlink($filename);
    }

} # end of deleteUploadedFile

