package Plugin::Todo::Records2Display;

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use base qw(Extropia::Core::Action);

#
# This plugin is mainly used for translation between the database
# fields and user input definitions.
#
# This plugin accepts -RECORDS which always points to a reference to a
# list of references to hashes, where each hash is a record with
# key/values as they are coming out of the database.
#
# This plugin adjusts the data -RECORDS points to if needed.  If you
# modify this plugin make sure that you don't break $ra_records.
# 
#


sub getWidgetDefinition{
    my $self = shift;
    my $rh_input_definition = shift;
    my $field = shift;

    my @input_widget_def = _rearrange
        ([
          -BASIC_INPUT_WIDGET_DEFINITIONS,
          -BASIC_INPUT_WIDGET_DISPLAY_ORDER,
         ],
         [
          -BASIC_INPUT_WIDGET_DEFINITIONS,
          -BASIC_INPUT_WIDGET_DISPLAY_ORDER,
         ],
         @{ $rh_input_definition || [] }
        );
    
    my $input_widget_config = shift @input_widget_def;
    my %def = @{ $input_widget_config->{$field} };
    return \%def;
}


sub execute {
    my $self = shift;
    my ($rh_args) = _rearrangeAsHash
        ([
          -CGI_OBJECT,
          -RECORDS,
          -INPUT_WIDGET_DEFINITIONS, 
          -DATETIME_CONFIG_PARAMS,
         ],
         [
          -CGI_OBJECT,
          -RECORDS,
          -INPUT_WIDGET_DEFINITIONS,
          -DATETIME_CONFIG_PARAMS,
         ],
         @_
        );

    my $cgi        = $rh_args->{-CGI_OBJECT};
    my $ra_records = $rh_args->{-RECORDS};

    my $rh_priority_labels = getWidgetDefinition($self,
                                                 $rh_args->{-INPUT_WIDGET_DEFINITIONS},
                                                 'priority'
                                                )->{-LABELS};
    my $rh_status_labels   = getWidgetDefinition($self,
                                                 $rh_args->{-INPUT_WIDGET_DEFINITIONS},
                                                 'status'
                                                )->{-LABELS};

    my $datetime_config = $rh_args->{-DATETIME_CONFIG_PARAMS};

    for my $rh_record (@$ra_records) {

        # format dates to user readable format
        for my $field (qw(start_date due_date birth_date)) {
            if ($rh_record->{$field}) {
                my $date_obj = Extropia::Core::DateTime::create
                
                    (
                     @$datetime_config,
                     -DATETIME   => $rh_record->{$field},
                    );
                $rh_record->{$field} = $date_obj->date_string();
            }

        }

        # convert priority and status numbers into equivalent strings
        $rh_record->{priority} = $rh_priority_labels->{ $rh_record->{priority} } 
            if $rh_record->{priority} and $rh_priority_labels->{$rh_record->{priority}};

        $rh_record->{status} = $rh_status_labels->{ $rh_record->{status} } 
            if $rh_record->{status} and $rh_status_labels->{$rh_record->{status}};

        #E::dumper($rh_record);
    }

    return 2;
}


1;
__END__
