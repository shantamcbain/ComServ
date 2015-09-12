#$Id: Mail.pm,v 1.1.1.1 2001/03/12 05:38:31 stas Exp $
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

package Extropia::Core::Log::Mail;

use strict;
use Carp;

use Extropia::Core::Base qw(_rearrangeAsHash
                      _rearrange
                      _assignDefaults);

use Extropia::Core::Log;
use Extropia::Core::Mail;

use vars qw($VERSION @ISA);
@ISA = qw(Extropia::Core::Log);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

#
# create a new Extropia::Core::Mail Logger 
#
sub new {
    my $package = shift;
    my ($self) = _rearrangeAsHash([
                                   -MAIL_PARAMS,
                                   -MAIL_SEND_PARAMS,
                                   -DEFAULT_EVENT_ID,
                                   -DEFAULT_SEVERITY,
                                   -DISABLE_SEVERITY_LIST,
                                   -ENABLE_SEVERITY_LIST
                                  ],[-MAIL_PARAMS,-MAIL_SEND_PARAMS],@_);

    bless $self, ref($package) || $package;

    $self->_baseInit();

    return $self;

} # end of new

#
# Log to Email...
#
sub _log {
    my $self = shift;
    @_ = _rearrange([-EVENT,-SEVERITY,-EVENT_ID],[-EVENT],@_);

    my $event    = shift;
    my $severity = shift;
    my $event_id = shift;

    my $mail = Extropia::Core::Mail->create(@{$self->{-MAIL_PARAMS}});
    my $body = $self->_createLogEntry(-EVENT => $event,
                                      -EVENT_ID => $event_id);

    my @send_params = @{$self->{-MAIL_SEND_PARAMS}};
    $mail->send(@send_params, -BODY => $body);

} # end of _log

1;
