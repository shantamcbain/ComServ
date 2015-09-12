package Extropia::Env;

use strict;
use constant MOD_PERL   =>  1;

#use constant MOD_PERL   => $ENV{MOD_PERL} ? 1 : 0;
use constant SPEEDY_CGI => 0;
use constant FAST_CGI   => 0;
use constant VELOCIGEN  => 0;


# this constant tells us whether we are running under persistent
# enviroment or not
use constant PERSISTENT => MOD_PERL || SPEEDY_CGI || FAST_CGI || VELOCIGEN;



1;

__END__

=head1 NAME

Extropia::Env - Environment detection module

=head1 SYNOPSIS

    use Extropia::Env;
    
    do_something if Extropia::Env::PERSISTENT;

=head1 DESCRIPTION



=cut




