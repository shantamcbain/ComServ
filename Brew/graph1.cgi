#!/usr/bin/perl -wT

use DBI;
use CGI::Carp qw(fatalsToBrowser);
use Chart::Lines;
use DBIx::Chart;

$|=1;
$ENV{PATH}="";
my $pw  = "UA=nPF8*m+T#";
my $dsn = "DBI:mysql:shanta_forager";
my $user = "shanta_forager";
my $batchcode = "tbb1";

print <<'END';
Content-Type: text/html

<HTML>
  <HEAD>
    <TITLE>MySql Test</TITLE>
  </HEAD>
  <BODY>
END

#open connection to MySql database
$dbh = DBIx::Chart->connect($dsn ,$user,$pw)
   or die "Error connecting to database: $DBI::errstr";

#prepare and execute SQL statement
#SELECT time, spargtemp,mastuntemp, linetemp 
#                      FROM brew_temp_tb 
#                      WHERE batchnumber = '$batchcode'
#                      ORDER BY time
#                      RETURNING linegraph(*)
#                      WHERE WIDTH=400 AND HEIGHT=400 AND
# TITLE = 'Temperature graph' AND
# COLOR IN ('red', 'green', 'blue', 'lyellow', 'lpurple') AND
# BACKGROUND='lgray'

$rsth = $dbh->prepare (select * from brew_temp_tb
                       WHERE batchnumber = '$batchcode'
        returning linegraph(*)      
        where color=red) spargtemp

      (select * from from brew_temp_tb
                       WHERE batchnumber = '$batchcode
    returning linegraph(*)
        where color=blue) mastuntemp
    returning image
    where WIDTH=500
    AND HEIGHT=500
    AND TITLE='Composite Dense Linegraph Test'
    AND SIGNATURE='(C)2002, GOWI Systems'
    AND X_AXIS='Angle (Radians)'
    AND Y_AXIS="Sin/Cos"
    AND FORMAT='PNG'
);
 $rsth->execute;
$rsth->bind_col(1, \$buf);
$rsth->fetch;
#$sth->execute ||
      die "Could not execute SQL statement ... maybe invalid?";

print "<center><table border>";
#output database results
while (@row=$sth->fetchrow_array)
{
print "<tr>";
foreach (@row)
{
#$chart->add_dataset($_);
print "<td>$_</td>";
}
print "</tr>\n";
}

print "</table></center>";
my $chart = new Chart::Lines(600, 400);
$chart->png('temps.png', @data);
$chart->set('title' => 'temperature chart');
$dbh->disconnect or warn $dbh->errstr;

print "</body></html>";
exit;
