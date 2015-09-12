package Extropia::Core::Template::Email;
require 5.004;

use strict;

use Extropia::Config;

use Extropia::Core::Template;
use base qw(Extropia::Core::Template);

#sub new{
#    my ($class, $options) = @_;
#    my $self = $class->SUPER::new();
#
#    return $self;
#}


# initialize
###########
sub _init {
    my ($self,$options) = @_;

    if (Extropia::Config::PRINT_TMPL_PROCESS_TREE) {
        $Extropia::Core::Template::Email::recurs_level = 0;
    }

    $options ||= {};

    for (qw(AUTOCLEAR AUTOFLUSH DIE_ON_ERROR)) {
        $options->{$_} = 1 unless defined $options->{$_};
    }
    $options->{HEADER_SENT} = 0;
    $options->{AUTO_RESET} = 0;

#    $options->{START_TAG} = quotemeta('<+');
#    $options->{END_TAG}   = quotemeta('+>');

#    $options->{OUTPUT}   = \*STDERR;

    $options->{EVAL_PERL}   = 1;

#    $options->{BLOCKS} = {
#                          foobar => sub {"This is foo"},
#                         };

    $self->SUPER::_init($options)
        or die error();
    return $self;
}


#############
sub get_processed {
    my ($self, $filename, $stream) = @_;

    my $short_filename = '';
    if (Extropia::Config::PRINT_TMPL_PROCESS_TREE) {
        # ($short_filename) = ($filename =~ m|/((?:[^/]+/)?[^/]+\.ttml)$|);
        $short_filename = $filename;
        print STDERR "+++ view  : ". 
            (" " x (4*$Extropia::Core::Template::Email::recurs_level+1)).
                "< $short_filename>\n";
        $Extropia::Core::Template::Email::recurs_level++;
    }



    # process and output
    my $output = $self->SUPER::get_processed($filename,$stream);

    # META: Later need to filter the output text through Text::Wrap or
    # Text::Autoformat

    if (Extropia::Config::PRINT_TMPL_PROCESS_TREE) {
        $Extropia::Core::Template::Email::recurs_level--;
        print STDERR "          : ".
            (" " x (4*$Extropia::Core::Template::Email::recurs_level)).
                " </$short_filename>\n";
    }

    return $output;
}




###########
sub flush {
    my ($self, $r) = @_;

}

#############
1;
__END__

=head1 NAME

Extropia::Core::Template::Email - Template class

=head1 SYNOPSIS

    use Extropia::Core::Template::Email;

    my $t = Extropia::Core::Template::Email->new;
    (
     RELATIVE     => 1,
    );
    $t->variables(foo => 1,
                  bar => [1..5]);
    $t->get_processed($template_filename, $buffer_or_stream);

=head1 OVERVIEW

For a complete description, refer to Extropia::Core::Template embedded
documentation.

=over

=cut
