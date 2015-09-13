package Extropia::Core::Auth::SMB;

#use strict;
use Carp;
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash _assignDefaults);
use Extropia::Core::Auth;

use Authen::Smb;

use vars qw(@ISA $VERSION);
@ISA = qw(Extropia::Core::Auth);
$VERSION = do { my @r = (q$Revision: 1.1.1.1 $ =~ /\d+/g); sprintf "%d."."%02d" x $#r, @r };

sub new {
  my $package = shift;
  my $self;
  ( $self, @_ ) = _rearrangeAsHash(
				   [
				    -USER_FIELDS,
				    -USER_FIELD_TYPES,
				    -DEFAULT_GROUPS,
				    -AUTH_CACHE_PARAMS,

				    -SMB_PDC_HOSTNAME,
				    -SMB_BDC_HOSTNAME,
				    -SMB_NT_DOMAIN,
				    
				    -USERNAME_NOT_FOUND_ERROR,
				    -PASSWORD_NOT_MATCHED_ERROR,
				    -DUPLICATE_USERNAME_ERROR
				   ],
				   [
				    -USER_FIELDS,
				    -USER_FIELD_TYPES,
				    -SMB_PDC_HOSTNAME,
				    -SMB_BDC_HOSTNAME,
				    -SMB_NT_DOMAIN
				   ],
				   @_);

  $self = _assignDefaults($self,
			  {
			  });

  bless $self, ref($package) || $package;

  $self->_init();

  return $self;
}

#
# Public entry points
# 
sub authenticate {
  my $self = shift;

  my ($params) = _rearrangeAsHash(
				  [-USERNAME, -PASSWORD],
				  [-USERNAME],
				  @_
				 );

  my $authResult = Authen::Smb::authen($params->{-USERNAME},
				       $params->{-PASSWORD},
				       $self->{-SMB_PDC_HOSTNAME},
				       $self->{-SMB_BDC_HOSTNAME},
				       $self->{-SMB_NT_DOMAIN});

  if ($authResult == Authen::Smb::NO_ERROR) {
    return 1; # Success
  }

  # There doesn't appear to be a way to distinguish between a user
  # not existing error, and a password incorrect error.
  #
  if ($authResult == Authen::Smb::LOGON_ERROR) {
    $self->addError("Login failed.");
  } else {
    $self->addError("NT Server/protocol error ($authResult)");
  } 

  return undef;
}

sub _getRawUserField {
  die("_getRawUserField is not implemented for this driver.");
}

sub register {
  die("User registration is not implemented for this driver.");
}

sub search {
  die("Searching is not implemented for this driver.");
}
			   
1;

