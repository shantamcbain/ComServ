# $Id: App.pm,v 1.24 2002/03/07 06:14:28 jason Exp $
# Copyright (C) 1994 - 2001  eXtropia.com
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

package Extropia::Core::App;

use strict;
use Carp;
use Time::localtime;

use Extropia::Core::Base qw(
    _rearrange 
    _rearrangeAsHash
    _assignDefaults
    _dieIfRemainingParamsExist
);

use Extropia::Core::DataHandlerManager;
use Extropia::Core::Filter;
use Extropia::Config;

use vars qw(@ISA);
@ISA = qw(Extropia::Core::Base);

#################################################################
#                            create()                           #
#################################################################

sub create {
    my $package = shift;
    @_ = Extropia::Core::Base::_rearrange([-TYPE],[-TYPE],@_);
    my $type = shift || "Base";
    my @fields = @_;

    my $class = _getDriver("Extropia::Core::App", $type) or
        Carp::croak("Mail type '$type' is not supported");
    # hand-off to scheme specific implementation sub-class
    $class->new(@fields);
}

###################################################################
#                        new() Method                             #
###################################################################

sub new {
    my $package = shift;
    my $self;
    ($self, @_) = _rearrangeAsHash([
        -ACTION_HANDLER_ACTION_PARAMS,
        -ACTION_HANDLER_LIST,
        -ROOT_ACTION_HANDLER_DIRECTORY,
        -VIEW_DISPLAY_PARAMS,
            ],
            [
        -ACTION_HANDLER_ACTION_PARAMS,
        -ACTION_HANDLER_LIST
            ],
        @_);

    _dieIfRemainingParamsExist(@_);

    $self->{'_additional_param_array'} = [];
    return bless $self, $package;
}

###################################################################
#                         execute() Method                        #
###################################################################

sub execute {
    my $self = shift;

        if (Extropia::Config::DEBUG) {
            print STDERR "\n\n";
            print STDERR "--------------------------------------------------\n";
        }

    # META: shouldn't be hardcoded!!!
    my $root_action_handler_directory = 
        $self->{'-ROOT_ACTION_HANDLER_DIRECTORY'} || 'Extropia/ActionHandler';

    # loading these that early, because it's possible that email or
    # different templates will be processed from within the action
    # handler, and they need these args.
    my %action_params = @{$self->{-ACTION_HANDLER_ACTION_PARAMS}};
    $action_params{-VIEW_LOADER}->store_data($self->{-VIEW_DISPLAY_PARAMS});

    foreach my $action (@{$self->{'-ACTION_HANDLER_LIST'}||[]}) {
        next unless $action;

        my $source_file = "$root_action_handler_directory/$action.pm";
        $source_file =~ s|::|/|g;

        require $source_file or die $!;

        my $action_object = eval { return $action->create() };
        die $! if $@;
	
        if (Extropia::Config::DEBUG) {
            print STDERR "Trying $action ";
        }

        my $action_status = $action_object->execute(
            -APPLICATION_OBJECT         => $self,
            @{$self->{-ACTION_HANDLER_ACTION_PARAMS}||[]}
        );

        if (Extropia::Config::DEBUG) {
            # executed but didn't set view
            my $sign = "EXECUTED" if $action_status == 2;
            $sign    = "ACTIVE"   if $action_status == 1;
            $sign    = "DECLINED" if $action_status == 0;
            print STDERR " => $sign\n";
        }

        if ($action_status == 1) {
            return $self->_displayView(
               $self->_getAdditionalViewDisplayParams(),
              @{$self->{-VIEW_DISPLAY_PARAMS}},
              @{$self->{-ACTION_HANDLER_ACTION_PARAMS}}
            );
        }
    }
}


#
####################
sub executePlugin{
    my $self   = shift;
    my $plugin = shift;
    my @extra_args = @_;

    warn("no plugin specified"), return unless $plugin;

    my $root_action_handler_directory = 
        $self->{'-ROOT_ACTION_HANDLER_DIRECTORY'} || 'Extropia/ActionHandler';

    if (Extropia::Config::DEBUG) {
        print STDERR "\n\tRunning Plugin: $plugin\n";
    }

    # load plugin
    my $source_file = "$root_action_handler_directory/$plugin.pm";
    $source_file =~ s|::|/|g;
    require $source_file or die $!;

    my $plugin_object = eval { return $plugin->create() };
    die "failed to load plugin: $!" if $@;
	
    my $plugin_status = $plugin_object->execute
        (
         -APPLICATION_OBJECT => $self,
         @{$self->{-ACTION_HANDLER_ACTION_PARAMS}||[]},
         @extra_args
        );

}

#
###############
sub runPlugins{
    my $self = shift;
    my ($rh_args) = _rearrangeAsHash
        ([
          -ACTION_HANDLER_PLUGINS,
          -CATEGORY,
         ],
         [
         ],
         @_
        );
    
    print STDERR "\nTrying Plugins\n" if Extropia::Config::DEBUG;

    my $rh_plugins = $rh_args->{-ACTION_HANDLER_PLUGINS} || {};

    # don't continue if -ACTION_HANDLER_PLUGINS aren't specified
    return unless %$rh_plugins;

    my $category = $rh_args->{-CATEGORY};
    # Run plugins if any registered in the caller package. We use
    # caller() to get the package name of the caller and then look it
    # up in the $param_hash->{-ACTION_HANDLER_PLUGINS} hash, if the
    # entry exists, we check wether there are plugins that should be
    # executed for $category
    # 
    my @conversion_plugins = @{ $rh_plugins->{caller()}{$category} || [] };
    #E::dumper(\@conversion_plugins,$rh_args->{-ACTION_HANDLER_PLUGINS}{caller()},$category);
    for my $plugin (@conversion_plugins) {
        $self->executePlugin($plugin),
    }
}

###################################################################
#                     setAdditionalViewDisplayParam()             #
###################################################################

sub setAdditionalViewDisplayParam {
    my $self = shift;
        my (@params) = _rearrange([
        -PARAM_NAME,
        -PARAM_VALUE
            ],
            [
        -PARAM_NAME,
        -PARAM_VALUE
            ],
        @_
    );

    my $param_name  = shift (@params);
    my $param_value = shift (@params);

    my $additional_param_array = $self->{'_additional_param_array'};
    my @new_additional_param_array = (
        "$param_name" => $param_value,
        @$additional_param_array
    );
    $self->{'_additional_param_array'} = \@new_additional_param_array;
#print STDERR "called $param_name $param_value\n";
}

###################################################################
#                     setAdditionalViewDisplayParam()             #
###################################################################

sub setNextViewToDisplay {
    my $self = shift;
    my (@params) = _rearrange([
        -VIEW_NAME
            ],
            [
        -VIEW_NAME
            ],
        @_
    );

    $self->{'_next_view_to_display'} = shift (@params);
}

###################################################################
#                    _getAdditionalViewDisplayParam()             #
###################################################################

sub _getAdditionalViewDisplayParams {
    my $self = shift;
    return @{$self->{'_additional_param_array'}};
}

###################################################################
#                        _displayView()                           #
###################################################################

sub _displayView {
    my $self = shift;
    my $errors_ref = $self->getErrors();

    my @errors;
    my $error;
    foreach $error (@$errors_ref) {
        push (@errors, $error->getMessage());
    }
    return $self->_loadViewAndDisplay((
        -ERROR_MESSAGES => \@errors,
        -VIEW_NAME      => $self->{'_next_view_to_display'},
        @{$self->{'-VIEW_DISPLAY_PARAMS'}},
        @{$self->{'-ACTION_HANDLER_ACTION_PARAMS'}},
        @{$self->{'_additional_param_array'}},
    ));

}

#################################################################
#                      _loadViewAndDisplay                      #
#################################################################

sub _loadViewAndDisplay {
    my $self = shift;
    my $param_hash;
    ($param_hash, @_) = _rearrangeAsHash([
        -LOG_OBJECT,
        -VIEW_FILTERS_CONFIG_PARAMS,
        -VIEW_LOADER,
        -VIEW_NAME,
        -VALID_VIEWS,
            ],
            [
        -VIEW_LOADER,
        -VIEW_NAME,
        -VALID_VIEWS,
            ],
        @_);

    my @view_display_params = @_;
    my $log             = $param_hash->{'-LOG_OBJECT'};
    my $view_filters_config_params =
       $param_hash->{'-VIEW_FILTERS_CONFIG_PARAMS'};
    my $view_loader     = $param_hash->{'-VIEW_LOADER'};
    my $view_name       = $param_hash->{'-VIEW_NAME'};
    my $ra_valid_views  = $param_hash->{'-VALID_VIEWS'};

    my $view_is_valid = 0;
    my $valid_view;
    foreach $valid_view (@$ra_valid_views) {
        if ($view_name eq $valid_view) {
            $view_name     = $valid_view;
            $view_is_valid = 1;
            last;
        }
    }

    unless ($view_is_valid) {

        $log->log(
                  -EVENT => "VIEW_LOAD_ERROR: View=$view_name",
                  -SEVERITY => Extropia::Core::Log::ALERT()
                 ) if $log;

        die ("$view_name is not an authorized view!  Are you sure you " . 
             "spelled the name right?  Have you forgotten to add the " .
             "view to the \@VALID_VIEWS array in the Application " .
             "configuration?");
    }

#    $view_loader->store_data(\@view_display_params);
    my $content = $view_loader->process_html($view_name,\@view_display_params);

#print STDERR $content;

#    my $view = $view_loader->create($view_name);
#    my $content = $view->display(@view_display_params);

    my $filter_params;
    foreach $filter_params (@$view_filters_config_params) {
        my $filter = Extropia::Core::Filter->create(@$filter_params);

        $content = $filter->filter(
            -CONTENT_TO_FILTER => $content
        );
    }
    return $content;
}

###################################################################
#                        handleIncomingData                       #
###################################################################

sub handleIncomingData {
    my $self = shift;
    my ($param_hash) = _rearrangeAsHash([
        -DATA_HANDLER_CONFIG_PARAMS,
        -LOG_OBJECT,
        -CGI_OBJECT,
        -ACTION_HANDLER_PLUGINS,
            ],
            [
        -DATA_HANDLER_CONFIG_PARAMS,
        -CGI_OBJECT
            ],
        @_);

    my $data_handler_config_params_ref =
       $param_hash->{'-DATA_HANDLER_CONFIG_PARAMS'};
    my $log = $param_hash->{'-LOG_OBJECT'};
    my $cgi = $param_hash->{'-CGI_OBJECT'};

    # Run plugins if any registered in the caller package. We use
    # caller() to get the package name of the caller and then look it
    # up in the $param_hash->{-ACTION_HANDLER_PLUGINS} hash, if the
    # entry exists, we check wether there are plugins that should be
    # executed for -handleIncomingData_BEGIN
    # 
    # note that this _BEGIN plugin, so we run it as early as possible
    # in this function

    my @conversion_plugins = @{ $param_hash->{-ACTION_HANDLER_PLUGINS}{caller()}{-handleIncomingData_BEGIN} || [] };
    #E::dumper(\@conversion_plugins);
    for my $plugin (@conversion_plugins) {
        $self->executePlugin($plugin);
    }

    my $data_handler =
        Extropia::Core::DataHandlerManager->create(@$data_handler_config_params_ref)
           or confess("Whoopsy!  I was unable to " .
                      "construct the DataHandler " .
                      "object in WebGuestbook.pm. Please contact " .
                      "the webmaster."
           );

    $data_handler->transform($cgi);

    $data_handler->validate($cgi);
    my $found_errors = 0;
    if ($data_handler->getErrorCount()) {
        foreach my $error (@{$data_handler->getErrors()}) {
            if ($log) {
                $log->log(
                    -EVENT => "DATA_HANDLER_ERROR:" .
                              $error->getMessage(), 
                    -SEVERITY => Extropia::Core::Log::INFO()
                );
            }
        $self->_addDataHandlerError($error);
        }
        $found_errors = 1;
    }

    if ($self->getErrorCount()) {
        foreach my $error (@{$self->getErrors()}) {
            if ($log) {
                $log->log(
                    -EVENT => "DATA_HANDLER_ERROR:" .
                              $error->getMessage(), 
                    -SEVERITY => Extropia::Core::Log::INFO()
                );
            }
        $self->_addDataHandlerError($error);
        }
        $found_errors = 1;
    }

    if ($found_errors) {
        return undef;
    }

    $data_handler->untaint($cgi);
    if ($data_handler->getErrorCount()) {
        foreach my $error (@{$data_handler->getErrors()}) {
            if ($log) {
                $log->log(
                    -EVENT => "DATA_HANDLER_ERROR:" .
                              $error->getMessage(),
                    -SEVERITY => Extropia::Core::Log::INFO()
                );
            }
        $self->_addDataHandlerError($error);
        }
        return undef;
    }
    return 1;
}

###################################################################
#                    _addDataHandlerError()                       #
###################################################################

sub _addDataHandlerError {
    my $self   = shift;
    my $error  = shift;

    my $errors_ref = $self->{'_data_handler_errors'} || [];
    my @errors = @$errors_ref;

    push (@errors, $error);
    $self->{'_data_handler_errors'} = \@errors;
}

###################################################################
#                     getDataHandlerError()                       #
###################################################################

sub getDataHandlerErrors {
    my $self = shift;
    my $errors_ref =  $self->{'_data_handler_errors'} || [];
    return @$errors_ref;
}

###################################################################
#                       sendMail()                                #
###################################################################

sub sendMail {
    my $self = shift;
    @_ = _rearrange([
        -MAIL_CONFIG_PARAMS,
        -FROM,
        -TO,
        -SUBJECT,
        -BODY,
        -REPLY_TO,
        -CC,
        -BCC,
            ],
            [
        -MAIL_CONFIG_PARAMS,
        -FROM,
        -TO,
        -SUBJECT,
        -BODY
            ],
        @_
    );

    my $mail_config_params_ref = shift;
    my $from                   = shift;
    my $to_list_ref            = shift;
    my $subject                = shift;
    my $body                   = shift;
    my $reply_list_ref         = shift;
    my $cc_list_ref            = shift;
    my $bcc_list_ref           = shift;

    my $mailer = Extropia::Core::Mail->create(@$mail_config_params_ref)
       or confess("Whoopsy!  I was unable to construct the Mail " .
                  "object in the _sendReceipt() method of " .
                  "WebDB.pm. Please contact the webmaster.");

    return $mailer->send((
        -FROM    => $from,
        -TO      => $to_list_ref,
        -SUBJECT => $subject,
        -BODY    => $body,
        -REPLY_TO => $reply_list_ref,
        -CC       => $cc_list_ref,
        -BCC      => $bcc_list_ref
    ));
}

###################################################################
#                           getDate()                            #
###################################################################

sub getDate {
    my $self   = shift;
    my $format = shift || "";

    my $month  = localtime->mon();
    my $year   = localtime->year();
    my $day    = localtime->mday();
    my $hour   = localtime->hour();
    my $minute = localtime->min();
    my $second = localtime->sec();

    my @proper_month_names_short = qw(JAN FEB MAR APR MAY 
        JUN JUL AUG SEP OCT NOV DEC);

    my @proper_month_names_long = qw(January February March
        April May June July August September October November 
        December);
 
    my @weekday_names_short = qw(MON TUE WED THU FRI SAT SUN);

    $second = "0$second" if ($second < 10);
    $minute = "0$minute" if ( $minute< 10);
    $hour   = "0$hour" if ($hour < 10);
    $day    = "0$day" if ($day < 10);
    $month  = "0$month" if ($month < 10);
    $year   = $year+1900;

    if ($format eq "DDMONTHYYYY") {
        return $day .
               $proper_month_names_long[$month] .
               $year;
    }

    elsif ($format eq "DDMONTHYYYY") {
        return $day .
               $proper_month_names_long[$month] .
               $year;
    }

    elsif ($format eq "YYYYMONDD") {
        return $year .
               $proper_month_names_short[$month] .
               $day;
    }

    elsif ($format eq "YYYYMONDD HH:MM:SS") {
        return $year .
               $proper_month_names_short[$month] .
               $day .
               $hour . ":" .
               $minute . ":" .
               $second;
    }

    elsif ($format eq "YYYYMONTHDD HH:MM:SS") {
        return $year .
               $proper_month_names_long[$month] .
               $day .
               $hour . ":" .
               $minute . ":" .
               $second;
    }

    else {
        $month = $month +1;
        return "$year-$month-$day $hour:$minute:$second";
    }
}

###################################################################
#                         getCurrentTime()                       #
###################################################################

sub getCurrentTime{
    my $self   = shift;
    use Time::localtime;
    my $current_time = localtime();

    my $year  = $current_time->year() + 1900;

    my $month = $current_time->mon() + 1;
    if (length($month) <2) {
        $month = "0" . $month;
    }

    my $day = $current_time->mday();
    if (length($day) <2) {
        $day = "0" . $day;
    }

    my $hour = $current_time->hour();
    if (length($hour) <2) {
        $hour = "0" . $hour;
    }

    my $min = $current_time->min();
    if (length($min) <2) {
        $min = "0" . $min;
    }
    my $sec = $current_time->sec();
    if (length($sec) <2) {
        $sec = "0" . $sec;
    }

    return ($year   . "-" .
            $month  . "-" .
            $day    . " " .
            $hour   . ":" .
            $min   . ":" .
            $sec);
}

1;
__END__
