# $Id: Dispatcher.pm,v 1.2 2001/03/12 06:23:20 selena Exp $

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
####################################################
#
# Extropia::Core::View::Dispatcher acts as a dispatching
# agent for views. It wraps the display() method
# inside of an eval so that error checking can
# be performed for easier troubleshooting.
#
####################################################

package Extropia::Core::View::Dispatcher;

use strict;
use Carp;
use Extropia::Core::Base qw(_rearrangeAsHash);
use Extropia::Config ();

use vars qw($VERSION $WARNING);
$VERSION = '1.0';
$WARNING = '';

#
# new dispatcher
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash(
                    [-VIEW_OBJECT],
                    [-VIEW_OBJECT],@_);

    return bless $self, $package;

} # end of new dispatcher

#
# getViewObject returns the view object from
# the dispatcher
#
sub getViewObject {
    my $self = shift;

#    use Data::Dumper;
#  print Dumper "----",$self->{-VIEW_OBJECT};
    return $self->{-VIEW_OBJECT};

} # end of getViewObject

#
# We use a separate dispatch display() method to
# actually eval the display in the raw view object. We do this
# because we want to make sure that runtime errors are reported
# as having come from the view instead of from within some anonymous
# eval block
#
sub display {
    my $self = shift;

    if (Extropia::Config::DEBUG) {
        my $value = eval {$self->getViewObject()->display(@_)};
#        my $value = $self->getViewObject()->display(@_);
        Carp::croak("view: $@") if $@;
#        die("view: $@") if $@;
        return $value;
    } else {
        return $self->getViewObject()->display(@_);
    }



#print STDERR "[ ", scalar (@_), " ]\n" if @_;

#    my $old_warn = $SIG{'__WARN__'};
#    $WARNING = "";
#    $SIG{'__WARN__'} = sub { $WARNING .= "\n$_[0]"; };

#print STDERR "[[ ", $self->getViewObject(), " ]]\n";

 #   use Data::Dumper;
  #  warn Dumper $self->{-VIEW_OBJECT};

#   my $value = eval { $self->getViewObject()->display(@_) };
#    Carp::confess("view: $@") if $@;

#    $SIG{'__WARN__'} = $old_warn;
#    if ($@) {
#        Carp::confess("view: $@")
##        die("Error occurred while calling display() method on " .
##            ref($self->getViewObject()) . " view: $@");
#    }
#    if ($WARNING) {
#        Carp::cluck("view: $WARNING")
##        die("Warning occurred while calling display() method on " .
##            ref($self->getViewObject()) . " view: $WARNING");
#    }
#    return $value;

} # end of display

#
# create is just a plain dispatch method
#
sub create {
    my $self = shift;

    return $self->getViewObject()->create(@_);

} # end of create

1;
__END__
