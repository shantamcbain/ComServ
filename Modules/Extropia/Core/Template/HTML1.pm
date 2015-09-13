package JV::Site::Template::HTML;

require 5.005;

use strict;
use JV::Site::Config;
use JV::Site::Runtime;
use base qw(JV::Template::HTML);

use enum qw(NAME URI HANDLER);
my @main_uris =
    map { 'url_'.$_->[NAME] =>
            join '/',$JV::Site::Config::c{uri_site},$_->[URI]
        }
    @{$JV::Site::Config::c{urimap}};

# initialize
#######################
sub _init {
    my ($self, $options) = @_;
    $self->SUPER::_init($options, \@main_uris,
                        'JV::Site::Config','JV::Site::Runtime');

    return $self;
}

1;
__END__

=head1 NAME

JV::Site::Template::HTML - Template class

=head1 SYNOPSIS

    use JV::Site::Template::HTML;

    my $t = JV::Site::Template::HTML->new;
    $t->variables(name => 'Dodo Marmarosa', instrument => 'piano');
    $t->process('musician', $r);

=head1 OVERVIEW

For a complete description, refer to JV::Template embedded
documentation.

=over

=cut
