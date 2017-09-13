#!/usr/bin/perl
use strict;
use DBI;
use GD::Graph::Data;
use GD::Graph::bars;
use CGI qw(:standard);
use DBI;
my $CGI = new CGI() or
    die("Unable to construct the CGI object" .
        ". Please contact the webmaster.");

foreach ($CGI->param()) {
    $CGI->param($1,$CGI->param($_)) if (/(.*)\.x$/);
}
 my $SiteName = $CGI->param('site') ;
 my $batchnumber = $CGI ->param('batchnumber')||"20170903nervana" ;

my $dsn = "dbi:mysql:shanta_forager";
my $usr  = 'shanta_forager';
my $pw = 'UA=nPF8*m+T#'; 

my $sql = '
  SELECT time, mastuntemp, LineTemp, spargtemp 
  FROM brew_temp_tb 
  WHERE sitename = ? 
    AND batchnumber = ?
  ORDER BY time';

my $dbh = dbh(); # connect
my $sth = $dbh->prepare($sql);
$sth->execute('Brew',$batchnumber);           
           
my $data = GD::Graph::Data->new();
while (my @row = $sth->fetchrow_array){
  $data->add_point(@row);
}

my $chart = GD::Graph::bars->new();
my $gd = $chart->plot($data);
open(IMG, '>','/images/Brew/$batchnumber.png') or die $!;
binmode IMG;
print IMG $gd->png;

# connect
sub dbh{

my $dsn = "dbi:mysql:shanta_forager";
my $usr  = 'shanta_forager';
my $pw = 'UA=nPF8*m+T#'; 
  my $dbh = DBI->connect($dsn, $usr, $pw, 
     { RaiseError=>1, AutoCommit=>1 } );
  return $dbh;
} 
