#$Id: ApacheDBI.pm,v 1.2 2001/05/21 08:45:31 gunther Exp $
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

package Extropia::Core::Session::ApacheDBI;

use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Session qw(CACHE_NOTHING CACHE_READS CACHE_READS_AND_WRITES
                         NO_LOCK DATA_STORE_LOCK ATTRIBUTE_LOCK);

use Carp;
use strict;
use DBI;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Session);
# $VERSION line must be on one line for MakeMaker
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub new {
    my $package = shift;
    my $self; 
    ($self,@_) = _rearrangeAsHash (
        [
            -SESSION_ID,
            -DATASOURCE,
            -USERNAME,
            -PASSWORD,    
            -DATA_POLICY,
            -TRACK_ACCESS_TIME,
            -TRACK_MODIFY_TIME,
            -TRACK_CREATION_TIME,
            -MAX_ACCESS_TIME,
            -MAX_MODIFY_TIME,
            -MAX_CREATION_TIME,
            -LOCK_PARAMS,
            -LOCK_POLICY,
            -FATAL_TIMEOUT,
            -FATAL_SESSION_NOT_FOUND
        ],[-DATASOURCE],@_);

    $self = _assignDefaults($self,{
                    -MAX_ACCESS_TIME          => 3600, # 1 hr
                    -MAX_MODIFY_TIME          => 3600, # 1 hr
                    -MAX_CREATION_TIME        => 3600, # 1 hr
                    -TRACK_ACCESS_TIME        => 1,
                    -TRACK_MODIFY_TIME        => 1,
                    -TRACK_CREATION_TIME      => 0,
                    -DATA_POLICY              => CACHE_NOTHING,
                    -LOCK_POLICY              => DATA_STORE_LOCK
                   },@_);
    
# define the datastore type: sybase or plain apache dbi?
    if ($self->{-DATASOURCE} =~ /dbi\:sybase/i) {
        $self->{_apache_datastore}='Apache::Session::DBI::Sybase';
        eval "use @{[$self->{_apache_datastore}]}";
    } else {
        $self->{_apache_datastore}='Apache::Session::DBI';
        eval "use @{[$self->{_apache_datastore}]}";
    }

    if ($self->{-LOCK_POLICY} == ATTRIBUTE_LOCK &&
        !$self->{-LOCK_PARAMS}) {
        die ("You must specify -LOCK_PARAMS if your lock policy " .
                "is set to ATTRIBUTE_LOCK.");
    }
    my %tied_hash;
    tie %tied_hash, $self->{_apache_datastore},
                    $self->{-SESSION_ID},{
                    DataSource => $self->{-DATASOURCE},
                    UserName   => $self->{-USERNAME},
                    Password   => $self->{-PASSWORD},
                    };
    $self->{_session_hash}=\%tied_hash;

    if (!defined $self->{_session_hash}) {
        confess("failed to create DBI connection. Error Was: $@");
    }

    if(!defined $self->{-SESSION_ID}) {
        $self->{-SESSION_ID} = $self->{_session_hash}->{_session_id};
        $self->{_is_new} = 1;
    }

    bless $self, ref($package) || $package;
    $self->_init();
    return($self);
}

sub invalidate {
    my $self = shift;

    eval {
        tied(%{$self->{_session_hash}})->delete();
    };
    if ($@) {
        die("Unable to invalidate ApacheDBI session object: Error $@");
    }
}

sub _readSession {
    my $self = shift;

    return(\%{$self->{_session_hash}});
}

sub _writeSession {
    my $self = shift;

    %{$self->{_session_hash}} = %{$self->{_data_cache}};
}

sub _getSessions {
    my $package = shift;

    my ($session_params, @other_args) = 
        _rearrangeAsHash ([-DATASOURCE,-USERNAME,-PASSWORD],
                          [-DATASOURCE,-USERNAME,-PASSWORD],@_);

    my $datasource = $session_params->{-DATASOURCE};
    my $username   = $session_params->{-USERNAME};
    my $password   = $session_params->{-PASSWORD};

    my @sessions;
    
    my $dbh = DBI->connect
                  (
            $datasource,
            $username,
            $password,
            { RaiseError => 1, AutoCommit => 1 }
           ) || 
            confess ("failed to create DB connection to " .
                     "_getSessions. Error Was: $DBI::errstr");
    my $ra_session_ids = 
        $dbh->selectall_arrayref("SELECT id FROM sessions ");
    $dbh->disconnect();

    my $ra_session_id;
    foreach $ra_session_id (@{$ra_session_ids}) {
        my $session_id = $ra_session_id->[0];
        eval {
            my $new_session = Extropia::Core::Session->create(
                                      -SESSION_ID => $session_id,
                                      -DATASOURCE => $datasource,
                                      -USERNAME   => $username,
                                      -PASSWORD   => $password,
                                      @other_args
                                      );
             push(@sessions, $new_session);
        };
        if(($@) and($@!~/^TIMEOUT/)){
            confess("Unknown error in _getSessions " . 
                     "for DBI session $session_id. Error: $@");
        }
    }
    return(@sessions);
}

1;
