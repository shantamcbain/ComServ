package Extropia::Debug;

require Data::Dumper;
require Carp;

sub Apache::FETCH {} # a hack to let Dumper work if a ref to an object is passed to it
# Please note that to enable the printing of the message,
# you have to set DEBUG to 1 in Extropia/Local/Config.pm

sub E::todo   { if(Extropia::Config::DEBUG){ print STDERR "\n!!! todo: @_\n";}}
sub E::print  { if(Extropia::Config::DEBUG){ print STDERR "@_"; }             }
sub E::lprint { if(Extropia::Config::DEBUG){ print STDERR "@_\n";}            }
sub E::dumper {
   if(Extropia::Config::DEBUG) {
    print STDERR "<--dump-start:-->\n",
                 Data::Dumper::Dumper(@_),
                 "<--dump-end-->\n";
    }                 
}

sub E::carp    {Carp::carp(@_)   }
sub E::cluck   {Carp::cluck(@_)  }
sub E::confess {Carp::confess(@_)}
sub E::croak   {Carp::croak(@_)  }

# ("filepath",@args_to_dump);
#####################
sub E::dumper_to_file {
    my $filename = shift;

    open OUT, ">$filename" or die "cannot open $filename: $!";
    print OUT Data::Dumper::Dumper(@_);
    close OUT;
}


# try to load the local debug functions if any, which mainly should be
# used to overloading the functions, constants in this file.
eval {require Extropia::Local::Debug};

1;
