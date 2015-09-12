# $Id: XBase.pm,v 1.1.1.1 2001/03/12 05:38:34 stas Exp $
package DBIx::SQL92::XBase;

use strict;
use Carp;
use DBIx::SQL92;
use vars qw($VERSION @ISA %FUNCTION_NAME);

@ISA = ('DBIx::SQL92');
$VERSION = do { my @r = q$Revision: 1.1.1.1 $ =~ /\d+/g; sprintf "0.%d"."%02d" x $#r, @r };
%FUNCTION_NAME = ();

#
# new()
#   Instantiates and returns a new object of this class
#
sub new {
    my ($package, $self) = @_;
    if (ref $package) {
        $self = $package;
    }
    $self ||= {};
    return bless $self, ref $package || $package || 'DBIx::SQL92::XBase';
}

sub can_rollback       { return 0; }
sub _begin_transaction { return ""; }
sub _commit            { return ""; }

sub _rollback { 
    croak "DBD::XBase cannot rollback\n"; 
}

sub _get_last_auto_id  { 
    croak "DBD::XBase does not support autoincrement fields\n"; 
}

sub function {
    my ($self, $func) = @_;
    croak "DBD::XBase does not support function '$func'\n";
}

1;
__END__

=head1 NAME

DBIx::SQL92::XBase - XBase-specific DBD and SQL implementations

=head1 SYNOPSIS

  use DBIx::SQL92;
  my $std_sql = new DBIx::SQL92('XBase');


=head1 DESCRIPTION

This is the XBase-specific component to DBIx::SQL92.  See L<DBIx::SQL92>
for a complete description of the intent and usage of this module.

=head1 AUTHOR

Peter Santo Chines, pchines@nhgri.nih.gov

Thanks to Tim Bunce for DBI, G. Richter for the ideas in DBIx::Compat, and
Larry Wall and the Perl5 Porters for Perl.

=head1 SEE ALSO

=item L<DBIx::SQL92>

=item L<DBI>

=cut

