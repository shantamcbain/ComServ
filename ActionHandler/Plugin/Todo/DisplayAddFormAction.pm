package Plugin::Todo::DisplayAddFormAction;

use strict;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);
use base qw(Extropia::Core::Action);

#
# This plugin is used for presetting data in add form
#

sub execute {
    my $self = shift;
    my ($params) = _rearrangeAsHash
        ([
          -CGI_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         [
          -CGI_OBJECT,
          -DATETIME_CONFIG_PARAMS,
         ],
         @_
        );

    my $cgi     = $params->{-CGI_OBJECT};
    # we arrive to this form by two pathes:
    # 1. when the add form is rendered for the first time
    # 2. when user clicks 'back' image instead of 'submit' because he
    #    wants to fix something, in the later case we don't have to
    #    set anything

    # I think that just checking for one bit is enough
    return 2 if $cgi->param('start_year');

    my $datetime_config = $params->{-DATETIME_CONFIG_PARAMS};

    my $date_obj = Extropia::Core::DateTime::create
        (
         @$datetime_config,
         -DATETIME   => 'now',
        );
    for my $prefix (qw(start due birth)) {
        $cgi->param("${prefix}_day", $date_obj->mday);
        $cgi->param("${prefix}_mon", $date_obj->month);
        $cgi->param("${prefix}_year",$date_obj->year);
    }

    $cgi->param("status",1);

    return 2;
}


1;
__END__ 
