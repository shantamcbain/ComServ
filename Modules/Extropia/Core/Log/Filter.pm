package Extropia::Core::Log::Filter;
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

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::Log;

use vars qw($VERSION @ISA);
@ISA = qw(Extropia::Core::Log);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([
                                    -LOG_PARAMS,
                                    -DEFAULT_EVENT_ID,
                                    -DEFAULT_SEVERITY,
                                    -ENABLE_SEVERITY_LIST,
                                    -ENABLE_CALLER_LIST,
                                    -ENABLE_EVENT_ID_LIST,
                                    -DISABLE_SEVERITY_LIST,
                                    -DISABLE_CALLER_LIST,
                                    -DISABLE_EVENT_ID_LIST
                                  ],[-LOG_PARAMS],@_);

    $self = _assignDefaults($self,
                            {-DEFAULT_SEVERITY => Extropia::Core::Log::INFO});

    return bless $self, ref($package) || $package;

} # end of new

sub _log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift;
    my $event_id = shift;

    if (!$self->_checkSeverity(-SEVERITY => $severity) ||
        !$self->_checkCaller() ||
        !$self->_checkEventId(-EVENT_ID => $event_id)) {
        return;
    }
    
    my $log = $self->{_log_object};
    if (!$log) {
        $log = new Extropia::Core::Log(@{$self->{-LOG_PARAMS}});
        $self->{_log_object} = $log;
    }

    $log->log(-EVENT    => $event,
              -SEVERITY => $severity,
              -EVENT_ID => $event_id);

} # end of _log

sub _checkEventId {
    my $self = shift;
    @_ = _rearrange([-EVENT_ID],[-EVENT_ID],@_);

    my $item = shift;

    $self->_checkItem(-ITEM         => $item,
                      -DISABLE_LIST => $self->{-DISABLE_EVENT_ID_LIST},
                      -ENABLE_LIST  => $self->{-ENABLE_EVENT_ID_LIST);

} # end of _checkEventId

sub _checkCaller {
    my $self = shift;

    my $item = $self->_getCallingSubroutineNotInLog();

    $self->_checkItem(-ITEM         => $item,
                      -DISABLE_LIST => $self->{-DISABLE_CALLER_LIST},
                      -ENABLE_LIST  => $self->{-ENABLE_CALLER_LIST);

} # end of _checkCaller

# 
# _getCallingSubroutineNotInLog
#
sub _getCallingSubroutineNotInLog {
    my $self = shift;

    my $frame_index = 1;
    my ($package, $filename, $line, $subroutine);
    while (1) {
        ($package, $filename, $line, $subroutine) =
            caller($frame_index);
        if ($package !~ /^Extropia::Core::Log/) {
            return $subroutine;
        }
        if (!defined($package)) {
            return undef;
        }
        $frame_index++;
    }

} # end of _getCallingSubroutineNotInLog

1;
