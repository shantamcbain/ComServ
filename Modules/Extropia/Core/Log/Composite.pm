#$Id: Composite.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Log::Composite;

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
# create a new Composite Logger 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([-LIST_OF_LOG_PARAMS,
                                   -SEVERITY_CRITERIA,
                                   -EVENT_ID_CRITERIA,
                                   -DEFAULT_EVENT_ID,
                                   -DEFAULT_SEVERITY],
                                  [-LOG_PARAMS],
                                  @_);

    $self = _assignDefaults($self,
                            {-DEFAULT_SEVERITY => Extropia::Core::Log::INFO});
    
    return bless $self, ref($package) || $package;

} # end of new

#
# Log via dispatching to other log objects...
#
sub _log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift;
    my $event_id = shift;

    my $log_params;
    if ($self->{-SEVERITY_CRITERIA_LOG_PARAMS}) {
        my $rh_criteria = $self->{-SEVERITY_CRITERIA_LOG_PARAMS};
        my $criteria;
        foreach $criteria (sort {$b <=> $a} (keys %$rh_criteria)) {
            if ($severity >= $criteria) {
                $log_params = $rh_criteria->{$criteria};
                last;
            }
        }
    } elsif ($self->{-EVENT_ID_CRITERIA_LOG_PARAMS}) {
        my $rh_criteria = $self->{-EVENT_ID_CRITERIA_LOG_PARAMS};
        my $criteria;
        foreach $criteria (sort {$b <=> $a} (keys %$rh_criteria)) {
            if ($event_id >= $criteria) {
                $log_params = $rh_criteria->{$criteria};
                last;
            }
        }
    }
    $log_params = $self->{-DEFAULT_LOG_PARAMS} if (!$log_params);

    my @EVENT_PARAM    = (-EVENT => $event);
    my @EVENT_ID_PARAM = ();
    my @SEVERITY_PARAM = ();

    if ($severity) {
        @SEVERITY_PARAM = (-SEVERITY => $severity);
    }

    if ($event_id) {
        @EVENT_ID_PARAM = (-EVENT_ID => $event_id);
    }

    my $log;
    if (ref($log_params->[0]) eq "ARRAY") {
        my $log_param_set;
        foreach $log_param_set (@$log_params) {
            $log = Extropia::Core::Log->create(@$log_param_set);
            $log->log(@EVENT_PARAM, @SEVERITY_PARAM, @EVENT_ID_PARAM);
        }
    } else {
        $log = Extropia::Core::Log->create(@$log_params);
        $log->log(@EVENT_PARAM, @SEVERITY_PARAM, @EVENT_ID_PARAM);
    }

} # end of _log

1;
