#$Id: Win32EventLog.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Log::Win32EventLog;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::Log;
use Win32::EventLog;

use vars qw($VERSION @ISA);
@ISA = qw(Extropia::Core::Log);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new Win32 EventLog Logger 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([-SOURCE,
                                   -CATEGORY,
                                   -DEFAULT_EVENT_ID,
                                   -DEFAULT_SEVERITY,
                                   -DISABLE_SEVERITY_LIST,
                                   -ENABLE_SEVERITY_LIST
                                  ],[],@_);

    bless $self, ref($package) || $package;

    $self->_baseInit();

    $self = _assignDefaults($self,
                            {
                             -SOURCE           => 'Application',
                             -CATEGORY         => 'Extropia::Core::App');
    return $self;
    
} # end of new

#
# Log to Win32 Event Log...
#
sub _log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift;
    my $event_id = shift;
    
    my $source = $self->{-SOURCE};
    $handle = Win32::EventLog->new($source) 
        or die "Can't open application EventLog\n";

    my $win32_severity;
    if ($severity <= Extropia::Core::Log::NOTICE) {
        $win32_severity = EVENTLOG_INFORMATION_TYPE;
    } elsif ($severity <= Extropia::Core::Log::WARN) {
        $win32_severity = EVENTLOG_WARNING_TYPE;
    } else {
        $win32_severity = EVENTLOG_ERROR_TYPE;
    }
    $event = $self->_createLogEntry(-EVENT => $event,
                                    -EVENT_ID => $event_id);
    %event_hash = ( 
                    'EventType' => $win32_severity,
                    'Category'  => $self->{-CATEGORY},
                    'Strings'   => $event
                  );

    if ($event_id) {
        $event_hash->{'EventID'} = $event_id;
    }
         
    $handle->Report(\%event_hash);
    $handle->Close();

} # end of _log

1;
