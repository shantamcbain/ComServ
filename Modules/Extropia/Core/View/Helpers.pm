package Extropia::Core::View::Helpers;


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

#
# $ra_args = remap_args(\@args,\%new_map);
# or
# $ra_args = remap_args(\%args,\%new_map);
#
# accepts a reference to a hash or list (which is supposedly
# equivalent to a hash) and remaps the old keys into new keys, so in
# %new_map: (from_key => to_key)
#
# returns a reference to a hash which is a remapped hash (or list)
#
sub remap_args{
    my %args = ref $_[0] eq 'HASH' ? %{$_[0]} : @{$_[0]};

    my %map = %{$_[1]};
    my %new_args = ();
    while (my ($key,$val) = each %args) {
        $new_args{$map{$key}} = $val;
    }

    return \%new_args;
}



use Extropia::Core::AuthManager;
sub is_authenticated{
    my $ra_auth_manager_config_params = shift;

    if ($ra_auth_manager_config_params) {
        my $auth_manager = Extropia::Core::AuthManager->create(@$ra_auth_manager_config_params)
            or die("Whoopsy!  I was unable to construct the " .
                   "Authentication object in the DefaultAction ActionHandler. " .
                   "Please contact the webmaster."
        );
        return $auth_manager->isAuthenticated();
    }
}

1;
__END__

