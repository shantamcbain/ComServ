#!/usr/bin/perl -wT

use strict;
use GD::Graph::bars;
use GD::Graph::colour;
use GD::Graph::Data;

my $data = GD::Graph::Data->new([["1st","2nd","3rd","4th",
                                  "5th","6th","7th", "8th"],
                                 [ 1, 2, 5, 6, 3, 1.7, 1, 3], 
]) or die GD::Graph::Data->error;

my $graph = GD::Graph::bars->new();

$graph->set(
    x_label         => 'X Axis',
    y_label         => 'Y Axis',
    title           => 'Enron Stock Valuations',
    y_max_value     => 8,
    y_tick_number   => 8,
    y_label_skip    => 2,
    bar_spacing     => 4,
    shadow_depth    => 4,
    shadowclr       => 'steelblue',
    transparent     => 0,
)
or warn $graph->error;

print STDOUT header("image/jpeg");
binmode STDOUT;
print STDOUT $my_graph->plot($data)->jpeg();
