# $Id: View.pm,v 1.30 2002/06/19 04:57:39 cyph Exp $

# Copyright (C) 1996  eXtropia.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.

package Extropia::Core::View;

use strict;
use Carp;
use Data::Dumper;
use Extropia::Core::Template::HTML;

use Extropia::Core::View::Helpers;
use Extropia::Config ();
use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::View::Dispatcher;

use vars qw($VERSION %LOADED_FILES @WARNINGS);
$VERSION = do { my @r = (q$Revision: 1.30 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };
%LOADED_FILES = ();
@WARNINGS = ();


#
# new creates a new Extropia::Core::View which basically becomes a
# viewloader...
#
# This must be created in the original script the views will be
# affecting due to the construction of a unique package for the
# individual script.
#
# Example:
#
# $view_loader = new Extropia::Core::View();
#
#######
sub new {
    my $package         = shift;
    my $ra_search_paths = shift || [];
    my $ra_tmpl_paths   = shift || [];
    my $cache_dir       = shift || '';

    # this hack tries to solve the problem of relative path in the
    # include path, since we have to supply the directory for the
    # caching, if we have ../.. it'll get out of this directory and
    # will either break things or just won't work. Therefore we
    # magically append a number of directories to the end of the cache
    # dir as specified by user so REAL_DIR/foo/bar/../../Templates
    # will become REAL_DIR/Templates. There is no other way to code
    # around it if the include path has a relative segments.
    if ($cache_dir) {
        my $segments = 0;
        for (@$ra_tmpl_paths) {
            my $c = 0;
            $c++ while m|\.\./|g;
            $segments = $c if $c > $segments;
        }
        $cache_dir .= "/" . join "/",('hack') x $segments if $segments;
    }

    my %options = 
        (
         HTML_ENCODE  => 1,
         INCLUDE_PATH => join(":",@{ $ra_tmpl_paths || []}),
         #  RELATIVE => 1, # META: security concern
        );

    $options{COMPILE_DIR} = $cache_dir if $cache_dir;

    my $tt_html = Extropia::Core::Template::HTML->new(\%options);

    my $self = bless
        {
         _search_path    => $ra_search_paths,
         _script_package => caller(),
         _tmpl_paths     => $ra_tmpl_paths,
         _tmpl_html      => $tt_html,
         _headers_opts   => {},  # extra HTTP headers can go here
        }, $package;

    $self->{_tmpl_html}->variables(view_obj => $self);

    return $self

} # end of new


# usually the email templating is not needed, so we will init it on
# demand
#####################
sub _init_tmpl_email{
    my $self = shift;

    my @tmpl_paths = $self->get_template_paths;

    require Extropia::Core::Template::Email;
    $self->{_tmpl_email} = Extropia::Core::Template::Email->new
        (
         # RELATIVE => 1, # META: security concern
         INCLUDE_PATH => join(":", @tmpl_paths),
         # TEXTWRAP => 1, #?
        );

    # META: templates caching for email? Grab
    # -TEMPLATES_CACHE_DIRECTORY from config

}


# this method stores the view data for a later peruse by other templates
# you can add and override data at any point
#
#  $self->store_data(\%data)
# or
#  $self->store_data(\@data)
#
#
# prepares the data ready for TT re-use, by converting the keys 
################
sub store_data{
    my $self = shift;

    my $r_data = shift;
    return unless $r_data && ref $r_data;

    my %data = ref $r_data eq 'HASH' ? %$r_data : @$r_data;

    for (keys %data){
        # store the data as is
        $self->{data}->{$_} = $data{$_};

        # remove the '-' prefix and lowercase the key
        (my $key = $_) =~ s/^-(.*)$/lc $1/e;
        $self->{tt_data}->{$key} = $data{$_};
    }
}

#
# 1. store newly passed arguments
#
# 2. prepares them for TT by converting the keys to remove '-' prefix
#    and lowercasing all the keys. returns a ref to a hash with these
#    new keys
#
#################
sub convert_keys{
    my $self = shift;

    my $r_data = shift;
    return unless $r_data && ref $r_data;

    my %data = ref $r_data eq 'HASH' ? %$r_data : @$r_data;

    for (keys %data){
        # store the data as is
        $self->{data}->{$_} = $data{$_};

        # remove the '-' prefix and lowercase the keys
        (my $key = $_) =~ s/^-(\w+)/lc $1/e;
        $data{$key} = $data{$_};
    }

    return \%data;
}

#
# get the ref to a hash of data
#
#############
sub get_data{
    my ($self) = @_;
    return $self->{data};
}

#
# get the ref to a hash of data mangled to be used in TT so all keys
# will be placed into the data. namespace (hash)
#
# 
# data => {}
#
################
#sub get_tt_data{
#    my ($self) = @_;
#    return (data => $self->{tt_data});
#}



# process is an alias for process_html and embed_html
# introduced for developers convenience
*process = *process_html;
*embed   = *embed_html;

#
# process the html template
#
# optionally you can pass a ref to a hash (or an array) with new args
# at this moment they will stick thru the life of the process may be
# we need to unset them in the end of request, so there are like
# localized variables.
# 
# returns the content of processed template
#
#################
sub process_html{
    my ($self,$tmpl_name,$rh_args) = @_;

    warn("view_name is undef"), return unless $tmpl_name;
    
    # add any extra args that were passed as a part of process() call.
    $self->store_data($rh_args) if $rh_args;

    my $default_charset = $self->{data}{-DEFAULT_CHARSET} || 'ISO-8859-1';
    
    $self->{_tmpl_html}->variables
        (
         data          => $self->{tt_data},
         view_obj      => $self,
         embed         => sub {$self->embed_html(@_)},
         embed_string  => sub {$self->embed_string(@_)},
         set_headers   => sub {$self->set_headers(@_); return ''},
         subs => {
                  is_authenticated => \&Extropia::Core::View::Helpers::is_authenticated,
                  sprintf => sub { sprintf(shift,@_); },
                  stderr  => sub { print STDERR "stderr: ","@_","\n"; return ''},
                  dumper  => sub { print STDERR Data::Dumper::Dumper(@_); return ''},
                 }
        );

    my $result = $self->{_tmpl_html}->get_processed($self->find_template($tmpl_name));

    # send HTTP header if wasn't sent already
    # 
    # any template can add new headers and it overrides all the
    # previous values for the same header. The headers will be flushed
    # only after all templates have been processed.
    unless ($self->{HEADER_SENT}){ #} || !$self->{SEND_HEADER}) {

        my %headers = %{ $self->{_headers_opts} };

        # the default header
        $headers{"content-type"} ||= "text/html; charset=$default_charset";

        if ($ENV{MOD_PERL}) {
            my $r = Apache->request;
            while (my ($k,$v) = each %headers) {
                $r->cgi_header_out($k,$v);
            }
            $r->send_http_header;
        } else {
            while (my ($k,$v) = each %headers) {
                print ucfirst($k).": $v\r\n";
            }
            print "\r\n";
        }
        $self->{HEADER_SENT} = 1;
    }


    return $result;
}

#
# this method is called from the templates themselves to embed string
# that includes template code and should be processed.
#
###############
sub embed_string{
    my ($self,$rs_string,$rh_args) = @_;

#print STDERR "process html: @_:\n\t",join " ", caller,"\n";

    warn("no ref to a scalar was passed"), 
        return unless $rs_string;

    # add any extra args that were passed as a part of process() call.
    $self->{_tmpl_html}->update_variable
        (
         data => $self->convert_keys($rh_args)
        ) if $rh_args;

    return $self->{_tmpl_html}->get_processed($rs_string);
}

#
# this method is called from the templates themselves to embed other
# templates. The reason for this method is not to repeat the setting
# of the variables that were set already and solves the problem where
# the same variable has been html encoded more than once
#
# note that the templates themselves call this method as 'embed',
# process_html() takes care of this "alias"
#
###############
sub embed_html{
    my ($self,$tmpl_name,$rh_args) = @_;

#print STDERR "process html: @_:\n\t",join " ", caller,"\n";

    warn("view_name is undef"), return unless $tmpl_name;
    
    # add any extra args that were passed as a part of process() call.
    $self->{_tmpl_html}->update_variable
        (
         data => $self->convert_keys($rh_args)
        ) if $rh_args;

    return $self->{_tmpl_html}->get_processed
        ($self->find_template($tmpl_name));
}


# set_headers($ra_headers);
# set_headers($rh_headers);
#
# pass a ref to an array or a hash with header pairs
#
################
sub set_headers{
    my ($self, $ref_header) = @_;

    return unless my $ref = ref $ref_header;

    my %headers = ();
    if ($ref eq 'ARRAY') {
        %headers = @$ref_header;
    }
    elsif ($ref eq 'HASH') {
        %headers = %$ref_header;
    }
    else {
        warn ("wrong ref: $ref"), return;
    }

    while (my ($k,$v) = each %headers ) {
        # strip the leading '-' if any
        $k =~ s/^-//; 
        # lowercase all the keys
        $self->{_headers_opts}->{lc $k} = $v;
    }
}




#
# process the email template
#
# optionally you can pass a ref to a hash (or an array) with new args
# at this moment they will stick thru the life of the process may be
# we need to unset them in the end of request, so there are like
# localized variables.
#
# returns the content of processed template
#
###################
sub process_email {
    my ($self,$tmpl_name,$rh_args) = @_;

    # init the email tmpl object the first time it's used.
    $self->_init_tmpl_email unless $self->{_tmpl_email};

    warn("view_name is undef"), return unless $tmpl_name;
    
    # add any extra args that were passed as a part of process() call.
    $self->store_data($rh_args) if $rh_args;
    
    $self->{_tmpl_email}->variables
        (
         data        => $self->{tt_data},
         view_obj    => $self,
         embed       => sub {$self->embed_email(@_)},
         subs => {
                  sprintf => sub { sprintf(shift,@_); },
                  stderr  => sub { print STDERR "stderr: ","@_","\n"; return ''},
                  dumper  => sub { print STDERR Data::Dumper::Dumper(@_); return ''},
                 }
        );

    my $email_body= $self->{_tmpl_email}->get_processed
        ($self->find_template($tmpl_name));

    # Have to unescape HTML otherwise the email message will have &#13; 
    $email_body =~ s/&lt;/</g;
    $email_body =~ s/&gt;/>/g;	
    $email_body =~ s/&quot;/"/g;	
    $email_body =~ s/&amp;/&/g;
    $email_body =~ s/&#13;/\n/g;
    return $email_body;
}


#
# this method is called from the templates themselves to embed other
# templates. The reason for this method is not to repeat the setting
# of the variables that were set already.
#
# note that the templates themselves call this method as 'embed',
# process_email() takes care of this "alias"
#
###############
sub embed_email{
    my ($self,$tmpl_name,$rh_args) = @_;

#print STDERR "process html: @_:\n\t",join " ", caller,"\n";

    warn("view_name is undef"), return unless $tmpl_name;
    
    # add any extra args that were passed as a part of process() call.
    $self->{_tmpl_email}->update_variable
        (
         data => $self->convert_keys($rh_args)
        ) if $rh_args;

    return $self->{_tmpl_email}->get_processed
        ($self->find_template($tmpl_name));
}


##################
sub find_template{
    my ($self,$name) = @_;
    die "no template name passed" unless $name;

#    return $name if $name =~ /^\.\./;

    my @paths = $self->get_template_paths;

    $name =~ s/(\.ttml)?$/.ttml/;
    return $name;

#    my $full_path = '';
#    for (@paths) {
#        next unless -e "$_/$name";
#        $full_path = "$_/$name";
#        last;
#    }
#
#    confess ("Could not find template $name in \n\t" .
#             join("\n\t",@paths) . "\n")
#        unless $full_path;
#
#
#    return $full_path;
}


#######################
sub get_template_paths{
    return @{shift->{_tmpl_paths}};
}




1;
__END__


