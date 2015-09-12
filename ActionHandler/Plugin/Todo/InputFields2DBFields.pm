package Plugin::Todo::InputFields2DBFields;

use strict;
use Extropia::Core::Base qw(_rearrangeAsHash);

use base qw(Extropia::Core::Action);
use Extropia::Core::DateTime;


#
# This plugin is mainly used for translation between user input
# definitions and the database fields. For example you can add to cgi
# object database fields, which weren't filled by user. (i.e. think of
# last_modified_by, etc.)
#
# Notice that all fields are forwarded from the action hanler, so you
# can basically access any field.
#
# Basically this plugin mungles the CGI_OBJECT. But you can think
# about other possible uses as well.
#
#############
sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash
        ([
          -CGI_OBJECT,
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         [
          -CGI_OBJECT,
          -APPLICATION_OBJECT,
          -SESSION_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         @_
        );

    my $cgi     = $params->{-CGI_OBJECT};
    my $app     = $params->{-APPLICATION_OBJECT};
    my $session = $params->{-SESSION_OBJECT};
    my $datetime_config = $params->{-DATETIME_CONFIG_PARAMS};

    # set start_date and due_date db fields (and also original_ and
    # search_ values if available)
    for my $prefix ( qw(start due original_start original_due search_start search_due birth) ) {
        # set the date only if all values were set. Note that since
        # none of this can be 0, we don't need to use defined().
        if ($cgi->param("${prefix}_day") and 
            $cgi->param("${prefix}_mon") and
            $cgi->param("${prefix}_year")) {

            $cgi->param("${prefix}_date",
                        sprintf "%04d-%02d-%02d",
                        $cgi->param("${prefix}_year"),
                        $cgi->param("${prefix}_mon"),
                        $cgi->param("${prefix}_day"),
                       );
        }


    }

    # META: is owner is not the same who modifies?
    if (!defined $cgi->param('owner')) {
        my $username = $session->getAttribute(-KEY => 'auth_username');
        $cgi->param('owner',$username);
        $cgi->param('last_mod_by',$username);
    }

    my $date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => 'now',
        );
    $cgi->param('last_mod_date',
                $date_obj->get(-FORMAT => "%Y-%m-%d %H:%M:%S")
               );

    #############################
    # User Input Error checking
    #############################

    my $errors = 0;
    my $fatal_errors = 0;

    # I wish I had easier access to fields names definitions, this is
    # a hack (duplicate the info from .cgi)
    my %labels =
        (
         due_date         => 'Due Date',
         start_date       => 'Start Date',
         birth_date       => 'Birth Date',
        );

    # initialize date objects if we have the data.
    ### check: compare that the dates are valid
    my %date_objs = ();
    for my $prefix ( qw(start due birth) ) {
        my $key = "${prefix}_date";
        next unless $cgi->param($key);
        ($date_objs{$key},my $error) = Extropia::Core::DateTime::create
            (
             @$datetime_config,
             -DATETIME   => $cgi->param($key),
            );
        if ($error) {
            $fatal_errors = 1;
            $app->addError("$labels{$key} is $error");
        }
    }

    # check whether we can proceed
    return 2 if $fatal_errors;

    ### check: compare the dates against the start_date
    if ($date_objs{start_date}) {

        for my $prefix (qw(due)) {
            my $key = "${prefix}_date";
            next unless $date_objs{$key};
            # start_date should always be smaller than the other dates
            if ($date_objs{start_date}->compare_date(-WITH_OBJECT=>$date_objs{$key}) > 0 ) {
                $errors++;
                $app->addError("$labels{$key} can't be earlier than $labels{start_date}");
            }

        }
    }

    return 2;
}


1;
__END__
