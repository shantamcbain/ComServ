#$Id: BabelFish.pm,v 1.2 2001/05/19 12:17:12 gunther Exp $
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

####################################################
#
# Extropia::Core::DataHandler::BabelFish
#
####################################################
package Extropia::Core::DataHandler::BabelFish;

use Extropia::Core::Base qw(_rearrange);
use Extropia::Core::DataHandler;
use WWW::Babelfish;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::DataHandler);
$VERSION = do { my @r = (q$Revision: 1.2 $ =~ /\d+/g); sprintf  "%d."."%02d" x $#r, @r };

sub getHandlerRules {
    my $self = shift;

    return {
        -TRANSLATE_LANGUAGE  => [$self,\&translateLanguage]
    };

} # getHandlerRules

#
# translateLanguage translates a given language
# to another language using the WWW:Babelfish module
#
sub translateLanguage {
    my $self = shift;
    @_ = _rearrange([-FIELD_VALUE,-SOURCE,-DESTINATION,-FIELD_NAME,-AGENT,
                     -SOURCE_ERROR,
                     -DESTINATION_ERROR,
                     -TRANSLATION_ERROR],
                    [-FIELD_VALUE,-SOURCE,-DESTINATION],@_);

    my $field      = shift;
    return undef if (!defined($field));
    my $source     = shift || "English";
    my $dest       = shift || "French";
    my $field_name = shift || "Unknown";
    my $agent      = shift;
    my $source_err = shift || "$source is not a valid language.";
    my $dest_err   = shift || "$dest is not a valid language.";
    my $tran_err   = shift || "%field_name% had a translation error.";

    my @agent_param = ();
    @agent_param = ('agent' => $agent) if ($agent);

    my $babelfish = new WWW::Babelfish(@agent_param);
    
    my @valid_languages = $babelfish->languages;
    my %language_hash = map { $_ => '1'; } @valid_languages;

    if (!$language_hash{$source}) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $source_err)  
            )
        );
        return undef;
    } # source language not supported

    if (!$language_hash{$dest}) {
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $dest_err)  
            )
        );
        return undef;
    } # destination language not supported

    $field = $babelfish->translate('source'      => $source,
                                   'destination' => $dest,
                                   'text'        => $field);

    if (!$field) {
        $tran_err .= $babelfish->error;
        $self->addError(
            new Extropia::Core::Error(
            -MESSAGE => $self->_getMessage($field_name, $field, $tran_err)  
            )
        );
        return undef;
    } # could not translate

    return $field;

} # end of translateLanguage

1;
