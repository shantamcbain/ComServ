#$Id: File.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Log::File;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::Log;

use vars qw($VERSION @ISA);
@ISA = qw(Extropia::Core::Log);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new File Logger 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([
                                   -LOG_FILE,
                                   -LOG_FORMAT,
                                   -LOG_FORMAT_DEFAULTS,
                                   -LOG_FORMAT_DEFAULT_FIELD,
                                   -LOG_FILTER_CHARS,
                                   -DEFAULT_EVENT_ID,
                                   -DEFAULT_SEVERITY,
                                   -DISABLE_SEVERITY_LIST,
                                   -ENABLE_SEVERITY_LIST
                                  ],[-LOG_FILE],
                                  @_);

    bless $self, ref($package) || $package;

    $self->_baseInit();

    return $self;

} # end of new

#
# Log to a file...
#
sub _log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift;
    my $event_id = shift;

    if (ref($event) eq "ARRAY") {
# Take out delimiters...
        my $i;
        for ($i = 0; $i < scalar(@$event); $i++) {
            $event->[$i] =~ s/\|/%PIPE%/g;
            $event->[$i] = $self->_filterLogChars($event->[$i]);
            $event->[$i] =~ s/%PIPE%/\|/g;
        }
        push(@$event, "severity");
        push(@$event, $self->_getSeverityDescription(-SEVERITY => $severity));
    } else {
# Take out delimiters...
        $event = $self->_filterLogChars($event);
        $event =  
         $self->_getSeverityDescription(-SEVERITY => $severity) . "|$event";
    }

    local(*LOG);
    my $log_file = $self->{-LOG_FILE};
    open(LOG,">>" . $self->{-LOG_FILE}) ||
        die("Could not open file: $log_file for writing: $!");
    print LOG 
        $self->_createLogEntry(-EVENT => $event, -EVENT_ID => $event_id);
    close(LOG);

} # end of log

1;
