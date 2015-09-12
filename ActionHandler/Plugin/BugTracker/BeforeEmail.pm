package Plugin::BugTracker::BeforeEmail;

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
    	 
         ],
         [
          -CGI_OBJECT,
          
         ],
         @_
        );

    my $cgi     = $params->{-CGI_OBJECT};
 
    if($cgi->param('abstract')) {
    		$cgi->param('override_subject', $cgi->param('abstract'));
     }
   
    return 2;
}


1;
__END__ 
