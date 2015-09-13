package Extropia::Core::Template::Provider;
require 5.005;

use strict;
use base qw(Template::Provider);

sub fetch {
    my ($self, $name) = @_;
    my ($data, $error) = $self->SUPER::fetch($name);
    $self->{_GLOBAL} = $data->{_GLOBAL}
        if !$error && defined $data->{_GLOBAL};
    return ($data, $error);
}

1;

