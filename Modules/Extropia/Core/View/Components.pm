package Extropia::Core::View::Components;

# this package provides generic components that are to be used in the
# view templates. These components are themselves use templates.

use vars qw(%components);

use Extropia::Core::Template::HTML;

%components = (
              );

$components{top}    = 
    sub {
        my $template = Extropia::Core::Template::HTML->instance();
        $template->get_processed('Core/top');
    };
$components{bottom} = 
    sub { 
        my $template = Extropia::Core::Template::HTML->instance();
        $template->get_processed('Core/bottom');
    };

sub left{}

sub right{}

sub form_fields{

}


#$template->variables(
#                     mycomponent => sub {  "hello" },
#                     );


1;
