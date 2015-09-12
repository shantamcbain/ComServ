package Extropia::Core::Template::HTML;
require 5.004;

use strict;

use Extropia::Config;

use Extropia::Core::Template;
use base qw(Extropia::Core::Template);

# get the encoding sub right
if ($ENV{MOD_PERL}) {
    require Apache::Util;
    *encode = \&Apache::Util::escape_html;
} else {
	require HTML::Entities;
	# fixed to resemble apache_1.3.26/src/main/util.c:ap_escape_html() exactly - HMS
	*encode = sub { HTML::Entities::encode($_[0], '<>&"') };
}

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
        $Extropia::Core::Template::HTML::recurs_level = 0;
    }

    $options ||= {};

    for (qw(HTML_ENCODE AUTOCLEAR AUTOFLUSH DIE_ON_ERROR)) {
        $options->{$_} = 1 unless defined $options->{$_};
    }

    # control the space trimming
    for (qw(TRIM PRE_CHOMP POST_CHOMP)) {
       $options->{$_} = 1 unless defined $options->{$_};
    }

    $options->{HEADER_SENT} = 0;
    $options->{AUTO_RESET} = 0;

#    $options->{HTML_ENCODE} = 0;

    # supply default caching params if anything is missing
    if ($options->{COMPILE_DIR} || $options->{COMPILE_EXT}) {
        $options->{COMPILE_EXT} ||= '.ttc';
        $options->{COMPILE_DIR} ||= '/tmp/ttc';
        $options->{CACHE_SIZE}  = 64 unless defined $options->{CACHE_SIZE};
    }

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

# add, retrieve template variables
#
# this function also handles HTML encoding
#######################
sub variables {
    my $self = shift;

    my $stash = $self->context->stash;
    @_ == 1 and return $stash->get($_[0]);
    while (my ($key, $value) = splice(@_, 0, 2)) {
        next unless defined $value;
       _encode($value) if $self->{HTML_ENCODE};
        $stash->set($key,$value);
    }
}

# update template variables
#
# this function allows you to add new data if the key has already
# existed, or create a new entry if it didn't exist before. Hash
# entries get updated with new key/value pairs, whereas arrays get
# extended.
#
# this function also handles HTML encoding
#
# currently handles only hashes and arrays
#
#######################
sub update_variable {
    my $self = shift;
    my $stash = $self->context->stash;
    warn("cannot update variable: @_ != 2"),return unless @_ == 2;
    _encode($_[1]) if $self->{HTML_ENCODE} and defined $_[1];
    my $r_data = $stash->get($_[0]);
    if (!$r_data) {
        # add a new entry if the key didn't exist before
        $stash->set($_[0],$_[1]);
    } else {
        # the key existed already, extend it
        my $ref = ref $r_data || '';
        if ($ref eq 'HASH') {
            $stash->set($_[0],{ %{ $stash->get($_[0]) },
                                %{ $_[1] }, # override or add new pairs
                              });
        } elsif ($ref eq 'ARRAY') {
            $stash->set($_[0],[ @{ $stash->get($_[0]) },
                                @{ $_[1] }, # add new entried
                              ]);
        }
    }
}




###################
sub get_processed {
    my ($self, $input, $stream) = @_;

    my $output = '';

    # pass a ref to the text to process it as is
    if (ref $input eq 'SCALAR') {
        $output = $self->SUPER::get_processed($input,$stream);
    } else {
        my $filename = $input;
        my $short_filename = '';
        if (Extropia::Config::PRINT_TMPL_PROCESS_TREE) {
            #($short_filename) = ($filename =~ m|/([^/]+/[^/]+\.ttml)$|);
            $short_filename = $filename;
            print STDERR "+++ view  : ". 
                (" " x (4*$Extropia::Core::Template::HTML::recurs_level+1)).
                    "< $short_filename>\n";
            $Extropia::Core::Template::HTML::recurs_level++;
        }

        # process the template and get the output
        $output = $self->SUPER::get_processed($filename,$stream);

        if (Extropia::Config::PRINT_TMPL_PROCESS_TREE) {
            $Extropia::Core::Template::HTML::recurs_level--;
            print STDERR "          : ".
                (" " x (4*$Extropia::Core::Template::HTML::recurs_level)).
                    " </$short_filename>\n";
        }
        
    }


    return $output;
}




###########
sub flush {
    my ($self, $r) = @_;

    # get ready for next request
    $self->{HEADER_SENT} = 0;

}



#######################
sub _encode {
    my $ref = ref $_[0];
    if (!$ref) {
        $_[0] = encode($_[0]) if defined $_[0];
    } elsif ($ref eq 'ARRAY') {
        _encode($_) for @{$_[0]};
    } elsif ($ref eq 'HASH') {
        _encode($_[0]->{$_}) for keys %{$_[0]};
    } else {
        # nothing
    }
}

1;
__END__

=head1 NAME

Extropia::Core::Template::HTML - Template class

=head1 SYNOPSIS

    use Extropia::Core::Template::HTML;
    
    my $t = Extropia::Core::Template::HTML->new
    (
     HTML_ENCODE  => 0,
     RELATIVE     => 1,
    );
    $t->variables(foo => 1,
                  bar => [1..5]);
    $t->get_processed($template_filename, $buffer_or_stream);

=head1 OVERVIEW

For a complete description, refer to Extropia::Core::Template embedded
documentation.

=over

=item new( [options] )

Available C<Extropia::Core::Template::HTML> specific options:

=over

=item HTML_ENCODE

HTML-encode all variable values set with C<variables()>.

=item other options

See the parent C<Extropia::Core::Template> class for rest of the options

=back



=cut
