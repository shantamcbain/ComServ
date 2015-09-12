# $Id: Error.pm,v 1.1.1.1 2001/03/12 05:38:30 stas Exp $
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

package Extropia::Core::Error;

use Carp;
use strict;
#
# we will use _rearrangeAsHash and _assignDefaults from Base,
# but we cannot import them because Base relies on Error. Therefore
# we cannot import statements from Base until Error has been
# fully compiled. But Error will not fully compile until the
# statements have been imported.
#
# Therefore, the routines in Base will be prefixed with
# Extropia::Core::Base:: to reference them in that package directly from
# this module.
#


use vars qw($VERSION);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my ($self) = Extropia::Core::Base::_rearrangeAsHash(
                    [-MESSAGE,
                     -CODE,
                     -DESCRIPTION,
                     -SOURCE,
                     -CALLER],
                    [-MESSAGE],
                    @_);

    $self = Extropia::Core::Base::_assignDefaults($self,{
                              -CODE                 => 0,
                              -MESSAGE              => "",
                              -DESCRIPTION => "",
                              -SOURCE               => "",
                              -CALLER               => ""
                             });

    return bless $self, $package;

}

sub getCode {
    my $self = shift;
    return $self->{-CODE};
}

sub getMessage {
    my $self = shift;
    return $self->{-MESSAGE};
}

sub getDescription {
    my $self = shift;
    return $self->{-DESCRIPTION};
}

sub getSource {
    my $self = shift;
    return $self->{-SOURCE};
}

sub getCaller {
    my $self = shift;
    return $self->{-CALLER};
}

sub setMessage {
    my ($self,$msg) = @_;
    $self->{-MESSAGE} = $msg;
}

1;

__END__

