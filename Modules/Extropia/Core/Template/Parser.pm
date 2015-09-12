package Extropia::Core::Template::Parser;
require 5.005;

use strict;
use base qw(Template::Parser);

#######################
# constructor
sub new {
    my ($class, $options) = @_;
    my $self = $class->SUPER::new();
    $self->init($options);
    return $self;
}

#######################
sub init {
    my ($self, $options) = @_;
    $self->{$_} = $options->{$_} for keys %$options;
}
