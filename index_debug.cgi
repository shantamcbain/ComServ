#!/usr/bin/perl
use strict;
use warnings;
use Carp qw(carp croak);
use FindBin;
use lib "$FindBin::Bin/../lib";

# Set up error handling
$SIG{__DIE__} = sub {
    my $error = shift;
    my @call_info = caller(0);
    my $error_msg = "Package: $call_info[0]<br>File: $call_info[1]<br>Line: $call_info[2]<br>Error: $error";
    croak $error_msg;
};
$SIG{__WARN__} = sub {
    my $warning = shift;
    my @call_info = caller(0);
    my $warning_msg = "Package: $call_info[0]<br>File: $call_info[1]<br>Line: $call_info[2]<br>Warning: $warning";
    carp $warning_msg;
};

# Call the script you want to debug
eval {
    require "$FindBin::Bin/../cgi-bin/index.cgi";
    1;
} or do {
    my $error = $@;
    $error =~ s/\n/<br>/g;
    my @call_info = caller(0);
    my $error_msg = "Package: $call_info[0]<br>File: $call_info[1]<br>Line: $call_info[2]<br>Error: $error";
    print "Content-type: text/html\n\n";
    print "<html><head><title>Error Report</title></head><body>";
    print "<h2>Error Report</h2><p>$error_msg</p></body></html>";
    exit;
};

# Check if there was an error in the script
if ($@) {
    my $error = $@;
    $error =~ s/\n/<br>/g;
    my $trace = Carp::longmess($error);
    $trace =~ s/\n/<br>/g;
    my $error_msg = "";
    my $warning_msg = "";
    print "Content-type: text/html\n\n";
    print "<html><head><title>Error Report</title></head><body>";
    print "<h2>Error Report</h2><p>$error_msg</p><p>$warning_msg</p><p>$error</p><p>$trace</p></body></html>";
}
