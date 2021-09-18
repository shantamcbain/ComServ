#!/usr/bin/perl -w

# Copyright (C) 1994 - 2001  eXtropia.com
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

#
# This is a DEBUG version of the app. It's meant to be
# called in place of [app].cgi if you are debugging
# the configuration of your script
#
# It is a wrapper around the original webcal.
#
# Of course, if you use this, you must remember to 
# change the path to perl in both scripts if you
# wish to call the main [app].cgi directly after you
# are done debugging with the debug version of the script.
# 
#######################################################
# WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#######################################################
#
# You should turn off $DEBUG_MODE in this script 
# when the script is in production
# because allowing crackers to see your error messages
# can sometimes give them access to information
# that would further allow compromise to your system.
#
my $DEBUG_MODE = 1; # Turn this OFF ($DEBUG_MODE = 0) in production.

# We "eval" the entire code to catch errors
my $script;
eval {  
    # The following couple lines are based on
    # the mod_perl guide SUID section. 
    # with some changes for NT compatibility...
    #
    # Do different things depending on our name
    my ($name) = $0 =~ m|([^/\\]+)$|;
    if ($name =~ /(.*)_debug\.cgi$/) {
       $script = "$1\.cgi"; 
    } else {
        die ("The debugger script name: " . $name . " must be in the form of \"[app]_debug.cgi\"\n");
    }
    
    require "./client.cgi";
}; # End of eval'ing code to catch errors

#
# DON'T LET THE FOLLOWING CODE SCARE YOU...
# 
# It's just code to check the error and
# print it out. You should not have to 
# ever change this.
#
if ($@ && $DEBUG_MODE) { # if there was an error print it out
    #
    # the following is based on code from Lincoln Stein's CGI::Carp
    #
    # It takes any error and prints out a friendly message to the user
    # browser
    #

    my $msg = $@;
    if ($msg =~ /Can.?t locate \.\/[\w-_]+\.cgi in \@INC/i) {
        require Cwd;
        $msg = "The script: $script could not be found in the path. \n" . 
               "The debug script thinks that the current" .
               " working directory is " . Cwd::getcwd() . 
                    "\n\n" . $msg; 
    }
    $msg =~ s|&|&amp;|g;
    $msg =~ s|>|&gt;|g;
    $msg =~ s|<|&lt;|g;
    $msg =~ s|\"|&quot;|g;
    my($wm) = $ENV{SERVER_ADMIN} ?
    qq[the webmaster (<a href="mailto:$ENV{SERVER_ADMIN}">$ENV{SERVER_ADMIN}</a>)] :
    "this site's webmaster";
    my ($outer_message) = <<END;
For help, please send mail to $wm, giving this error message
and the time and date of the error.
END
    ;
    my $mod_perl = exists $ENV{MOD_PERL};
    print STDOUT "Content-type: text/html\n\n"
    unless $mod_perl;

    my $mess = <<END;
<H1>Software error:</H1>
<PRE>$msg</PRE>
<P>
$outer_message
END
    ;

    if ($mod_perl && (my $r = Apache->request)) {
        # If bytes have already been sent, then
        # we print the message out directly.
        # Otherwise we make a custom error
        # handler to produce the doc for us.
        if ($r->bytes_sent) {
            $r->print($mess);
            $r->exit;
        } else {
            $r->status(500);
            $r->custom_response(500,$mess);
        }
    } else {
        print STDOUT $mess;
    }

} elsif ($@) { # If not in $DEBUG_MODE rethrow error
    die ($@);
}
  
#
# SOME EXTRA TECHNICAL NOTES FOR THOSE INTERESTED:
#
# This script was inspired from Matt Sergeant's 
# addition to the mod_perl guide where he
# explained why catching $SIG{__DIE__} as 
# well as using CGI::Carp qw(fatalsToBrowser) 
# does not really work except in the simplest
# of situations.
#
# Thus, we have switched to using this debug script
# as a means to catching exceptions on the fly
# and outputting them to the browser.
#
# The mod_perl guide can be found at
# http://perl.apache.org/
#
# 
