# $Id: SQL92.pm,v 1.3 2001/12/19 05:52:11 janet Exp $

package DBIx::SQL92;

use strict;
use Carp;
use vars qw($VERSION @ISA @EXPORT_OK $AUTOLOAD);

# require Exporter;
# require AutoLoader;
# 
# @ISA = qw(Exporter AutoLoader);
$VERSION = do { my @r = q$Revision: 1.3 $ =~ /\d+/g; sprintf "0.%d"."%02d" x $#r,@r };

#
# new(dbd_driver)
#   Loads the specified SQL92::DBD module and instantiates and returns a
#   new object of this class
#
sub new {
    my ($package, $dbd, $self) = @_;
    $package = ref $package || $package || 'DBIx::SQL92';

    my $dbh;
    $dbh = $dbd if ref $dbd;
    $self = {} unless $self && $self =~ /HASH/;
    $self->{_dbh} = $dbh;

    if ($dbd && $dbd ne 'SQL92') {
        if ($dbh) {
            $dbd = $dbh->{Driver}->{Name};
        }
        if ($dbd =~ /^dbi:(\w+):/i) {
            $dbd = $1;
        }
        my $driver = $package . '::' . $dbd;
        eval "use $driver;";
        if ($@) {
            warn "Warning: $driver module not found; using SQL92 default\n";
        }
        else {
            return $driver->new($self);
        }
    }
    return bless $self, $package;
}

sub get_dbh {
    my $self = shift;
    return $self->{'_dbh'};
}

sub _say_or_do {
    my ($self, $sql) = @_;
    my $dbh = $self->get_dbh;
    if ($dbh) {
        return $dbh->do( $sql ) if $sql;
        return "0E0";   # True, but zero
    }
    return $sql;
}

sub can_rollback { 
    return 1; 
}

sub _begin_transaction {
    return "begin transaction";
}
sub begin_transaction { 
    my $self = shift;
    return $self->_say_or_do( $self->_begin_transaction() );
}
sub _commit { return "commit"; }
sub commit { 
    my $self = shift;
    return $self->_say_or_do( $self->_commit() );
}
sub _rollback { return "rollback"; }
sub rollback {
    my $self = shift;
    return $self->_say_or_do( $self->_rollback() );
}

sub _get_last_auto_id {
    return '';
}
sub get_last_auto_id {
    my $self = shift;
    my $id;
    my $sql = $self->_get_last_auto_id();
    my $dbh = $self->get_dbh();
    if ($dbh) {
        ($id) = $dbh->selectrow_array($sql) if $sql;
    }
    else {
        $id = $sql;
    }
    return $id;
}

sub AUTOLOAD {
    my $self = shift;
    my $dbh = $self->get_dbh;
    my $function;
    ($function = $AUTOLOAD) =~ s/.+:://;

    if ( my $ref = $dbh->can($function) ) {
        return wantarray ? ($dbh->$ref(@_)) : scalar ($dbh->$ref(@_));
    } else {
        my ($package, $file, $line) = caller;
        die qq(Can't locate object method "$function" via package) .
            qq( "$package" at $file line $line.\n);
    }
}

sub DESTROY { }

sub function {
    my ($self, $func) = @_;
    return $func;
}

sub allows_like_for_all_fields { return 0; }

1;
__END__

=head1 NAME

DBIx::SQL92 - Perl extension for handling differences between DBD drivers
and SQL implementations

=head1 SYNOPSIS

Use as a wrapper:

  use DBI;
  use DBIx::SQL92;

  my $dbd = DBI->connect($dsn, $user, $password);
  my $dbh = new DBIx::SQL92( $dbd );

  $dbh->begin_transaction;
  ...
  # Use just as you would a regular DBI handle
  $dbh->do( $sql );
  ...
  if ($success) {
      $dbh->commit;
  }
  else {
      $dbh->rollback;
  }

Or just use as an information source:

  use DBIx::SQL92;

  my $std_sql = new DBIx::SQL92('mysql');

  my $sql = "select " 
    . $std_sql->function('lower') . "(Field1) ";
    . "from TABLE";

=head1 DESCRIPTION

I love the DBI interface, but have long been frustrated that the
differences in the SQL code accepted by the various databases supported by
DBI and DBD drivers make it very difficult to write code that will work
with more than one database.

DBIx::SQL92 is written to help solve this problem.  The intent is to
encapsulate the differences by returning SQL code appropriate to a given
platform.  It is called SQL92 because it uses SQL92-sanctioned syntax and
becuase I hope this module--when paired with DBI and the many excellent DBD
drivers--achieves the real promise of SQL92, namely truly universal data
access.

The architecture is simple.  Like any good object-oriented design, we take
advantage of polymorphism.  Thus DBIx::SQL92 will have default
implementations and database specific modules (e.g. DBIx::SQL92::Sybase)
will have alternative code that is application specific.  I've focused here
on the databases that I know and use.  Additional modules can be added for
your favorite database.

=head1 AUTHOR

Peter Santo Chines, pchines@nhgri.nih.gov

Thanks to Tim Bunce for DBI, G. Richter for the ideas in DBIx::Compat, and
Larry Wall and the Perl5 Porters for Perl.  

Thanks also to the many good folks at Extropia.com and NHGRI who shared
ideas and gave me the interesting projects that called for this module.

=head1 SEE ALSO

=item L<DBI>

=cut
# Autoload methods go after =cut, and are processed by the autosplit program.

