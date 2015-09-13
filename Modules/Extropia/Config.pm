# $Id: Config.pm,v 1.11 2001/12/05 02:00:54 janet Exp $

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

package Extropia::Config;

# enforce 5.005x from a central place
require 5.005_03;

#Extropia::Debug is required after eval Extropia::Local::Config
#so that the methods in Extropia::Debug will get the correct value of 
#Extropia::Config::DEBUG
#use Extropia::Debug;

$ENV{'PATH'} = '/bin:/usr/bin';
delete @ENV{'IFS', 'CDPATH', 'ENV', 'BASH_ENV'};

#
# This file specifies configurations which influence all Extropia::
# modules and applications.
#

#
# IMPORTANT: If you mess up with variables and you don't know anymore
# what was the original settings, use the default values as specified
# for each configuration variable.
#


# This variable allows you to optimize the speed of your applications,
# by reusing compiled view packaged if used under persistent engines
# like mod_perl.
#
# By default we assume that more than one user may run the same
# application on the same server. Therefore if two users have two
# identical view package names, but different contents, there will be
# a problem here. The solution is to use a unique namespace, which in
# case of mod_perl provided by Apache::Registry (based on the script's
# URI). Since we still want to allow users to use the same package
# names, what we do is loading user's view package, compiling it,
# copying it into a unique namespace and then destroying it. 
#
# If you know that you have only one occurence of the same view
# packages, and you run under mod_perl or another persistent engine,
# you may want to reuse the originally loaded package by setting the
# following variable to 1.
#
# you can access this variable as Extropia::Config::PACKAGE_REUSE in other packages
#
# Values:  0|1
# Default: 0
#use constant PACKAGE_REUSE => 0;

# Enable debug hooks at compile time. Which means that if you set it
# to 0, all the debug code will be removed at compile time including
# the conditionals.
#
# Values:  0|1
# Default: 0
# you can access this variable as Extropia::Config::DEBUG in other packages
use constant DEBUG => 0;

#
#
# development constant to use cluck and confess instead of carp and croak
# to get a full stack trace when needed
#
#use constant FULL_TRACE => 1;
#use constant FULL_TRACE => 0;

# this forces a reload of files which will be cached otherwise (useful
# during development)
#use constant FORCE_RELOAD => 1;

#use Carp;
#$SIG{__DIE__} = \&Carp::confess;

#
# This option prints the trace of the executed temlates using a nested
# tree, so one can see what templates call what other templates.
#
# not to be used in production
#
use constant PRINT_TMPL_PROCESS_TREE => 0;

# enable DataSource debugging with 1
use constant DATASOURCE_DEBUG => 0;

eval {require Extropia::Local::Config};

# now load the debug methods using the constants
require Extropia::Debug;
1;
__END__
