package Extropia::Core::Template;
require 5.004;

use strict;
#use base qw(Class::Singleton Template);
use base qw(Template);

#use Template;
#@Extropia::Core::Template::ISA = qw(Template);

#use Extropia::Core::Template::Parser ();

# this code allows you to force scalar or array context in tt templates.
# ideally this should be folded into the core TT and removed from here.
$Template::Stash::SCALAR_OPS = 
    {
     'array'  => sub { ref $_[0] eq "ARRAY" ? $_[0] : [$_[0]] },
     'scalar' => sub { ref $_[0] eq "ARRAY" ? $_[0][0] : $_[0] },
    };

$Template::Stash::LIST_OPS = 
    {
     'scalar' => sub { ref $_[0] eq "ARRAY" ? $_[0][0] : $_[0] },
     'array'  => sub { ref $_[0] eq "ARRAY" ? $_[0] : [$_[0]] },
    };

#$Template::Config::PROVIDER = 'Extropia::Core::Template::Provider';



## Class::Singleton::_new_instance override
####################
#sub _new_instance {
#    my ($class, $options) = @_;
#    my $self = $class->SUPER::new();
#    $self->_init(@_);
#    return $self;
#}


#sub new{
#    my ($class, $options) = @_;
#    my $self = $class->SUPER::new(
#                                 );
#}

#######################
# initialize
sub _init {
    my ($self, $options) = @_;

#    $options->{_TEMPLATE}   = $self;

#    $options->{COMPILE_EXT} = '.ttc';
#    $options->{COMPILE_DIR} = '/tmp/ttc/foo/bar/zoo';
#    $options->{CACHE_SIZE}  = 30;

    $self->{$_} = $options->{$_} for keys %$options;
    $self->SUPER::_init($options) or die error();
    # E::dumper($options);
    #$self->clear();
    return $self;
}

# resets ongoing vars
#######################
# clear template vars
sub clear {

# META: this looks like a mess, need to review

#return;
#    my $self = shift;
#    my @preserve_keys = qw(extropia);
#    my %preserve = ();
#    for (@preserve_keys) {
#        $preserve{$_} = $self->{vars}{$_};
#    }
#    # reset
#    $self->{vars} = {};
#    # restore
#    $self->{vars} = \%preserve;
}

#######################
# clear all template vars
sub full_clear {
    shift->{vars} = {};
}

########################
## add, retrieve template variables
#sub variables {
#    my $self = shift;
##print STDERR "@_\n";
#    @_ == 0 and return $self->{vars};
#    @_ == 1 and return $self->{vars}{$_[0]};
#    while (my ($key, $value) = splice(@_, 0, 2)) {
#        next unless defined $value;
#        _encode($value) if $self->{HTML_ENCODE};
#        $self->{vars}{$key} = $value;
#    }
#}

#*variables = \*svariables;

#######################
# add, retrieve template variables
sub variables {
    my $self = shift;

    my $stash = $self->context->stash;
    @_ == 1 and return $stash->get($_[0]);
    while (my ($key, $value) = splice(@_, 0, 2)) {
        next unless defined $value;
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
# currently handles only hashes and arrays
#
#######################
sub update_variable {
    my $self = shift;

    my $stash = $self->context->stash;
    warn("cannot update variable: @_ != 2"),return unless @_ == 2;
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

#######################
# process a template, output the results
sub process {
    my ($self, $filename, $r) = @_;

#    use Data::Dumper;
#print STDERR Dumper $self->{vars};

#    $r ||= undef;

    # default extension for template files
#    $filename .= '.ttml' unless ref $filename;
    # process and output
    my $success;
    unless ($success = $self->SUPER::process($filename, $self->{vars})) {
        die $self->error()." in $filename" if $self->{DIE_ON_ERROR};
    }
    $self->clear if $self->{AUTOCLEAR};
    return $success;
}

# process the template and return the generated content
#################
sub get_processed {
    my ($self, $filename) = @_;


#    use Data::Dumper;
#print STDERR Dumper $self;

    # default extension for template files
#    $filename .= '.ttml' unless ref $filename;

    my $content = '';
    unless ($self->SUPER::process($filename, $self->{vars},\$content)) {
        die $self->error()." in $filename" if $self->{DIE_ON_ERROR};
    }

    return $content;
}



1;
__END__

=head1 NAME

Extropia::Core::Template - Template class

=head1 SYNOPSIS

    use Extropia::Core::Template;
    
    my $t = Extropia::Core::Template->new;
    $t->variables(name => 'Dodo Marmarosa', instrument => 'piano');
    $t->process('musician', $r);

=head1 OVERVIEW

For a complete description, refer to the Template Toolkit's
documentation.

=over

=item Simple variable substitution

  <p>[% name %] plays the [% instrument %].</p>

  $t->variables(name => 'Elmo Hope', instrument => 'piano');

=item branching

  [% IF url %]<a href="[% url %]">[% url %]</a>[% END %]
  [% UNLESS dead %]upcoming show: [% upshow %][% END %]

=item loops

  <table>
  [% FOREACH musicians %]
  <tr><td>[% name %]</td>
      <td>[% instrument %]</td></tr>
  [% END %]
  </table>

  $t->variables(musicians => [
        { name => 'Lennie Tristano', instrument => 'piano', },
        { name => 'Scott LaFaro',    instrument => 'bass',  },
    ]);

=item blocks

  [% BLOCK navbar %]
   <tr><td><a href="/next">Next</a></td>
       <td><a href="/prev">Previous</a></td>
   </tr>
  [% END %]

  ...
  [% PROCESS navbar %]

Blocks can also have settable variables:

  [% BLOCK header %]
   <head>
    <title>[% title %]</title>
   </head>
  [% END %]

These variables can be set in the calling template:

  [% PROCESS header title = 'foo' %]

Or in the code:

  [% PROCESS header title = [% title %] %]


If C<INCLUDE> is used instead of C<PROCESS>, all variables
used in the included block are localized.

=item filters

Display $foo, encoding HTML entities:

  [% foo FILTER html %]

Alternate syntax for large blocks:

  [% FILTER html %]
    [% foo %]
    [% bar %]
    [% baz %]
  [% END %]

=head1 JV SPECIFIC FEATURES

=item Wrapper template

The current template's output can optionnally be wrapped in
a wrapper template, for example to include common UI elements.
The wrapper is triggered by the presence of a <jvui> section
at the beginning of the template:

  <jvui>
    title = "the title"
  </jvui>

The <jvui> section contains variable definitions in standard
Template Toolkit syntax. These variables will be passed to
the wrapper template.

=item Automatic language handling

  <jvl><fr>Bonjour</fr>
       <en>Hello</en>
  </jvl>

Only strings in the current language will be output.

=head1 METHODS

=over

=item new( [options] )

Creates a new Extropia::Core::Template object. mod_perl scripts can use
a single persistent object. Options are a list of zero or
more key-value pairs. Reasonable defaults are used when no
options are specified.

Available options:

=over

=item AUTOCLEAR

Automatically calls C<clear()> after each call to C<process()>.
This makes it easy to write scripts that use one persistent
template object, and call C<process()> once per request.


=item INCLUDE_PATH

Root directory where template files will be searched for.


=item WRAPPER

A template to be used as a wrapper around the current template
when C<process()> is called. This can be the name of a template
block or file, or a reference to a string containing the template
itself (I<inline> template).

=back

=item variables([name1, [value1, [name2, value2, ...]]])

When called with no argument, returns a reference to a hash of
currently set variables.
When called with one argument, returns the value for that variable.
name
When called with more than one argument, sets the name-value pairs.

  my $hashref = $t->variables;
  
  my $name = $t->variables('name');
  
  $t->variables(name => 'Art Blakey');
  $t->variables(fullname   => [ qw(Art Blakey) ],
                instrument => 'drums',
                style      => { family => 'jazz',
                                name   => 'bebop',
                              },
               );

=item clear

Clears (empties) the template's variable list.

=item process($name[, $r])

Builds the page by processing the template and associated data, and
outputs the page to the supplied destination.

$name can be a file name (relative to our root template directory), or
a reference to a string containing template text.

$r is the destination. It can be a reference to a mod_perl request
object, a filehandle, or a reference to a string. If not supplied
output goes to STDOUT.

=back

=cut
