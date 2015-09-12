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

package Extropia::Core::DataSource::SimpleXMLFile;
use strict;
use vars qw($VERSION @ISA);

use Carp;
use XML::DOM;
use XML::Simple;
use Data::Dumper; # Not just debugging... see sub _writeFile()
use Extropia::Core::Base qw(_rearrange _rearrangeAsHash);

$VERSION = do { my @r = q$Revision: 1.1.1.1 $ =~ /\d+/g; sprintf "%d."."%02d" x $#r, @r };
@ISA = qw(Extropia::Core::DataSource);



############################################################
#	Remember to install: 
#	[i]	XML-Simple
#	[ii] 	Parse-Yapp
#	[iii]	libxml-enno
#	[iv]	XML-Parser
############################################################

# the constructor. ROOT_NODE_NAME is the name of the topmost node in the XML doc that is
# going to be manipulated. PATH_SEPARATOR is the separator used to separate the paths 
# for a field mapping in the XML [ by default '::' - eg a::b::c::d ]. FIELD_SEPARATOR 
# is the pattern that is used to separate multiple values within an XML tag - by default ','
# The other parameters are the usual suspects. Bear in mind that the module, for the moment,
# only deals with XML for of the style <TAG>VALUE</TAG>

sub new
{
	my $package = shift;
	my %rev;
	my $self=$package->SUPER::new(@_);
	my ($hashref)=_rearrangeAsHash([-XML_FILE,-FIELD_MAPPINGS,-ROOT_NODE_NAME,-PATH_SEPARATOR,-CREATE_IF_MISSING,-LOCK_PARAMS,-FIELD_SEPARATOR,-FIELD_NAMES],[-XML_FILE,-FIELD_MAPPINGS,-ROOT_NODE_NAME,-FIELD_NAMES],@_); 


	$self->{'-XML_FILE'}=$hashref->{'-XML_FILE'};
	$self->{'-FIELD_MAPPINGS'}=$hashref->{'-FIELD_MAPPINGS'};
	$self->{'-ROOT_NODE_NAME'}=$hashref->{'-ROOT_NODE_NAME'};
	$self->{'-PATH_SEPARATOR'}=$hashref->{'-PATH_SEPARATOR'};
	$self->{'-FIELD_SEPARATOR'}=$hashref->{'-FIELD_SEPARATOR'};
	$self->{'-CREATE_IF_MISSING'}=$hashref->{'-CREATE_IF_MISSING'};
	$self->{'-LOCK_PARAMS'}=$hashref->{'-LOCK_PARAMS'};
	$self->{'-FIELD_NAMES'}=$hashref->{'-FIELD_NAMES'};

	(defined $self->{'-PATH_SEPARATOR'})||($self->{'-PATH_SEPARATOR'}='::');
	(defined $self->{'-FIELD_SEPARATOR'})||($self->{'-FIELD_SEPARATOR'}=',');
	(defined $self->{'-CREATE_IF_MISSING'})||($self->{'-CREATE_IF_MISSING'}=0);
	(defined $self->{'-LOCK_PARAMS'}) || ($self->{'-LOCK_PARAMS'} =
	[
		-TYPE    => "File",
       		-FILE    => "@{[$self->{'-XML_FILE'}]}.lck",
       		-TIMEOUT => 120,
       		-TRIES   => 20
	]);

	$self->{'autoincPath'} = $self->{'-FIELD_MAPPINGS'}->{$self->getAutoincrementFieldName()};
	if(defined($self->{'autoincPath'}))
	{
		%rev = reverse %{$self->{'-FIELD_MAPPINGS'}};
		$self->{'countFieldSimpleName'} = $rev{$self->{'autoincPath'}};
	}
	eval
	{
		$self->_validateMappings();
	};
	if($@)
	{
		$self->addError
		(
			-MESSAGE => $@, 
			-SOURCE  => 'DataSource::SimpleXMLFile',
			-CALLER  => (caller)[0]		
		)
	}
	$self->_initialiseParser();
	return($self);
}


# this is the method that slurps the XML document into the DOM structure. Alternatively, if the XML_FILE that
# has been specified in the constructor does not exist, this method either dies if CREATE_IF_MISSING is false, 
# or sets on internal flag to denote that the object contains no data as yet.

sub _initialiseParser
{
	my($self)=@_;

	if(! -f $self->{'-XML_FILE'})
	{
		if(! ($self->{-CREATE_IF_MISSING}))
		{
			confess("could not find @{[$self->{'-XML_FILE'}]} in XMLFILE->_initialiseParser(), and param -CREATE_IF_MISSING is set to false");
		}
		else
		{
			$self->{'_no_data'}=1;
		}
	}
	else
	{
# Setting the tag compression this way ensures that the parser prints out XML of the form <TAG>VALUE</TAG>, 
# instead of in any other XML style.

		XML::DOM::setTagCompression(sub{return 1;});
		$self->{'xml_parser'} = XML::DOM::Parser->new()->parsefile($self->{'-XML_FILE'});
		$self->{'original_data'}=$self->{'xml_parser'}->toString();
		$self->{'root_node'} = $self->{xml_parser}->getElementsByTagName($self->{'-ROOT_NODE_NAME'})->item(0);
	}
}


# this method checks that a full path mapping for every XML field name has been provided

sub _validateMappings
{
	my($self)=@_;

	foreach(@{$self->{'-FIELD_NAMES'}})
	{
		if(!exists($self->{'-FIELD_MAPPINGS'}->{$_}))
		{
			die("the full XML path for field $_ has not been provided");
		}
	}
}


# this method takes a hash of the format
#%hash =
#	(
#		A::B::C		=> 'D',
#		A::B::E::F	=> 'G',
#      	);
# [ just by way of example ] and transforms it into XML like:
# <A>
#	<B>
#		<E>
#			<F>G</F>
#		</E>
#		<C>D</C>
#	</B>
#  </A>
# Thank god for eval, that's all i can say.

sub _xmlFromHash
{
	my($self,%fields)=@_;

	my @path;
	my $evalString;
	my $hashref={};
	my $string;
	my $rootName="";
	my $key;
	my $value;
	my $valueString;
	my $fieldSep;

	$rootName = $self->{'-ROOT_NODE_NAME'};
	$fieldSep = $self->_getFieldSeparator();

	while(($key,$value)=each %fields)
	{
		$evalString="";
		@path=$self->_pathToArray($key);
# DEBUG
#		print Data::Dumper->Dump([\@path],["*path"]);
# END DEBUG
		foreach(@path)
		{
			$evalString.="\{$_\}->";
		}
		$evalString=~s/\-\>$//;
		if(defined $value)
		{
			$evalString.='=[$value]';
		}
# DEBUG
#		print "evalString is $evalString\n";
#		print Data::Dumper->Dump([$hashref],["*hashref"]);
#		print "$string";
# END DEBUG
		eval "\$hashref->$evalString;";
	}
	$string = XMLout($hashref,(keyattr=>[],rootname=>""));
	return($string);
}


# writes out the XML string it is given. The regexp stuff is because the underlying Parser module
# insists on printing XML as a single string, with no newline characters at all - anywhere. This is
# fine programatically, but aesthetically harsh. What the regexp does is to feed the string into the
# XMLin function of XML::Simple, which turns the XML into a hashref. This string representation of this
# hashref is then manipulated  by a regexp, and fed back into the XMLout XML::Simple function to produce
# nicely formatted XML. once again, all hail eval. 

sub _writeFile
{
	my($self,$fileName,$string)=@_;

	my %test = %{XMLin($string)};
	my $cheat = Data::Dumper->Dump([\%test],["*test"]);
	$cheat=~s/\=\>\s*[^\{]\'?(.+?)\'?(.)$/\=\>\[\'$1\'\]\,/gm;

# DEBUG
#	print $cheat;
# END DEBUG

	eval "\%test=$cheat";
# DEBUG
#	print Data::Dumper->Dump([\%test],["*test"]);
# END DEBUG

	$string = XMLout(\%test,(keyattr=>[],rootname=>$self->{'-ROOT_NODE_NAME'}));

	local *aFile;
	open(aFile,">$fileName") or confess("failed to open $fileName in SimpleXMLFile->_writeFile()");
	print aFile $string;
	close(aFile);	
}

# returns a string representation of the internal DOM

sub _documentToString
{
    my($self)=@_;
    my $string = $self->{'xml_parser'}->toString();
    return($string);
}

# A driver method. Performs all the deletes, modifications and adds that have been
# specified by the user [ in that order ]. The changes are treated as a transaction - a 
# failure at any stage will result in the underlying XML file not being altered

sub doUpdate
{
	my $self = shift;
	@_ = _rearrange([-RETURN_ORIGINAL],[],@_);
	my $returnOriginal = shift || 0;
	my $updated=0;

	my $lockObj;
	my $originalRecords = [];
	my $pendingAdds = $self->_optimizeAdds();
	my $pendingUpdates = $self->_getPendingUpdates();

	my $pendingDeletes = $self->_getPendingActionsOfType("DELETE");
	my $pendingModifications = $self->_getPendingActionsOfType("UPDATE");
	

	eval
	{
		if(!$self->{'_no_data'})
		{
			if(@{$pendingDeletes})
			{
				$self->_deleteRecords($pendingDeletes,$originalRecords);
				$updated=1;
			}
			if(@{$pendingModifications})
			{
				$self->_updateRecords($pendingModifications,$originalRecords);
				$updated=1;
			}
		}
		if(@{$pendingAdds})
		{
			$self->_addRecords($pendingAdds);
			$updated=1;
		}
	};
	if($@)
	{
		$self->addError
		(
			-MESSAGE => $@, 
			-SOURCE  => 'DataSource::SimpleXMLFile',
			-CALLER  => (caller)[0]	
		);
	}
	elsif($updated)
	{
		$lockObj = Extropia::Core::Lock->create(@{$self->{'-LOCK_PARAMS'}});
        	$lockObj->obtainLock();	
		$self->_writeFile($self->{'-XML_FILE'},$self->_getXML());
		$lockObj->releaseLock();
	
		if($returnOriginal)
		{
			return Extropia::Core::DataSource::RecordSet->create
			(
				-TYPE => 'Static',
				-DATA_BUFFER => $originalRecords,
				-FIELD_NAMES => [$self->getFieldNames()],
				-DATA_TYPES  => {%{$self->_getAllDataTypes()}},
				-FIELD_SORTS => {%{$self->_getAllSorts()}}
			);
		}
	}
}


# simple utility method to loop through the list of all pending actions for the datasource, and return
# an array of all those of a particular type.

sub _getPendingActionsOfType
{
	my($self,$actionType)=@_;
	my $allPendingUpdates = $self->_getPendingUpdates();

# DEBUG
#	print Data::Dumper->Dump([\$allPendingUpdates],["*allPendingUpdates"]);
#	exit;
# END DEBUG

	my $item;
	my @actions=();

	foreach $item(@{$allPendingUpdates})
	{
		if($item->[0] eq $actionType)
		{
			push(@actions,$item);	
		}
	}
# DEBUG
#	print "actionType $actionType\n";
#	print Data::Dumper->Dump([\@actions],["*actions"]);
# END DEBUG
	return(\@actions);
}

# add new records to DOM

sub _addRecords
{
	my($self,$pendingAdds)=@_;
	my $anAdd;
	my %addParams;
	my $key;
	my $value;
	my $fullPath;
	my $childNode;
	my $parentNode;
	my $ancestorNodeRef={};
	my %new;
	my $newString;
	my $lockObj;
	my $ancestorPath;
	my $ancestorNode;
	my @keys;
	my @allPaths;
	my $fieldSep;
	my $textNode;
	my $countNode;
	my $valueString;

	$fieldSep = $self->_getFieldSeparator();
	
# DEBUG
#	print Data::Dumper->Dump([$pendingUpdates],["*pendingUpdates"]);
#	print Data::Dumper->Dump([$pendingAdds],["*pendingAdds"]);
# END DEBUG


	foreach $anAdd(@{$pendingAdds})
	{
		%addParams = %{$anAdd->[1]};
# DEBUG
#		print Data::Dumper->Dump([\%addParams],["*addParams"]);
# END DEBUG

# if the object contains no data, [ ie the underlying XML file does not yet exist ], then all
# we need to do is construct a hash of the format [ for example ]:
#%hash =
#	(
#		A::B::C		=> 'D',
#		A::B::E::F	=> 'G',
#      	);
# where A::B::C represent the absolute paths of the fields to be updated, and then feed this
# data structure to sub _xmlFromHash [ see ante ]. This will result in XML being generated, which can
# then be printed to the XML file as the first data within it.

		if($self->{'_no_data'})
		{
			if(defined $self->{'countFieldSimpleName'})
			{
				$addParams{$self->{'countFieldSimpleName'}}=1;
			}
			while(($key,$value)=each(%addParams))
			{
				$fullPath = $self->{'-FIELD_MAPPINGS'}->{$key};

				if(ref $value eq "ARRAY")
				{
					$valueString =join $fieldSep,@{$value}; 
					$new{$fullPath}=$valueString;
				}
				else
				{
					$new{$fullPath}=$value;
				}
			}
			$newString = $self->_xmlFromHash(%new);		
# DEBUG
#			print "newString is $newString\n";
# END DEBUG
			$self->{'_no_data'}=0;
			$self->_writeFile($self->{'-XML_FILE'},$newString);
			$self->_initialiseParser();
		}

# otherwise the DOM already contains data, and we are going to have to perform additions the hard way....
		else
		{
			@keys = keys %addParams;

# for each field that the user has specified making an addition for, retrieve its fully qualified path.
			foreach $key(@keys)
			{
				push(@allPaths,[$self->_pathToArray($self->{'-FIELD_MAPPINGS'}->{$key})]);
			}
# DEBUG
#			print Data::Dumper->Dump([\@allPaths],["*allPaths"]);
# END DEBUG

# retrieve the root of a record within the XML document. This is the node from which point down new values
# [ nodes ] are going to have to be added.
 
			$ancestorPath = $self->_getSharedAncestorPath(@allPaths);
# DEBUG
#			print "shared ancestor path is $ancestorPath";
#			exit;
# END DEBUG

# now that we know what the path to a new record is, we need to create one to hold the new information that
# we are going to be putting into the XML

			$ancestorNode = $self->_createChildNode($self->{'root_node'},$ancestorPath,1,1);

# if the datasource has an autoincrement field, then we have to create a node to represent this, and attach it to the 
# new record node that we have created above. 

			if(defined $self->{'countFieldSimpleName'})
			{
				$countNode = $self->_createChildNode($ancestorNode,$self->{'autoincPath'},scalar @{[$self->_pathToArray($ancestorPath)]},0);

# set the value of the new count field to one greater than the greatest value of the current autoincrement fields in
# the DOM
				$self->_setNodeText($countNode,($self->_getRecordCount()+1));
			}
# DEBUG
#			print $self->_getXML();
#			exit;
# END DEBUG


# now that we have created a node to represent the root of a record within the DOM, we need to iterate through all the
# paths that need to be added to that node. For each path, we need to create a child node, attach it to the new recordset
# root, and then set the value of the child.
  
			ADD: while(($key,$value)=each %addParams)
			{
# DEBUG		
#				print "$key is  $value\n";
# END DEBUG
				if((defined $self->{'countFieldSimpleName'}) and ($key eq $self->{'countFieldSimpleName'}))
				{
					next ADD;
				}
				$fullPath = $self->{'-FIELD_MAPPINGS'}->{$key};
				$childNode = $self->_createChildNode($ancestorNode,$fullPath,scalar @{[$self->_pathToArray($ancestorPath)]},0);
				if(ref $value eq "ARRAY")
				{
					$valueString =join $fieldSep,@{$value}; 
# DEBUG
#					print "key is $key\n";
#					print "value is @$value\n";
#					print "valueString is $valueString\n";
# END DEBUG
					$self->_setNodeText($childNode,$valueString);
				}
				else
				{
					$self->_setNodeText($childNode,$value);
				}
			}
# DEBUG
#			print $self->_getXML();
#			exit;
# END DEBUG
		}
	}
}


# delete all records that match any delete condition.

sub _deleteRecords
{
	my($self,$deletes,$originalRecords)=@_;
	my $count;
	my $aDelete;
	my $node;
	my @fields;
	my $fieldsAsHash;
# DEBUG
#	print Data::Dumper->Dump([\$deletes],["*deletes"]);
# END DEBUG	

# this hashref now contains a mapping between a DOM node object, and the array representation
# of its fields. The logic from here on is very simple. For each node object, match its array
# against the delete criteria that have been provided. If there is a match, remove the node from the DOM.
 
	my $records = $self->_getNodesAsFields();

	foreach $count(keys %{$records})
	{
		$node = $records->{$count}->{"NODE"};
		@fields = @{$records->{$count}->{"FIELDS"}};
		$fieldsAsHash = $self->_recordStorage2Internal(\@fields);
# DEBUG
#		print "count is $count\n";
#		print Data::Dumper->Dump([\$fieldsAsHash],["*fieldsAsHash"]);
# END DEBUG
		DELETERECORD: foreach $aDelete(@{$deletes})
		{
			if($self->_matches($aDelete->[1], $fieldsAsHash))
			{
				push(@{$originalRecords},[@fields]);
				$node->getParentNode()->removeChild($node);
				last DELETERECORD;
			}
		}
	}
}

# update node in accordance with all of the update criteria and resultant action that it matches

sub _updateRecords
{
	my($self,$updates,$originalRecords)=@_;
	my $recordRoot;
	my $count;
	my $aUpdate;
	my $node;
	my @fields;
	my $fieldsAsHash;
	my $updateHash;
	my $field;
	my $fieldPath;
	my $value;
	my $nodeToUpdate;
	my $records;
	my $nodeToUpdateRef={};
	my $dataDepth;
	
# DEBUG
#	print Data::Dumper->Dump([\$updates],["*updates"]);
# END DEBUG

	$records = $self->_getNodesAsFields();
	$recordRoot = $self->_getRecordRoot();
	$dataDepth = scalar @{[$self->_pathToArray($recordRoot)]};
	
	foreach $count(keys %{$records})
	{
		$node = $records->{$count}->{"NODE"};
		@fields = @{$records->{$count}->{"FIELDS"}};
		$fieldsAsHash = $self->_recordStorage2Internal(\@fields);


# the logic here is very similar to the logic for the delete method. For all nodes 
# whose array representation matches the update predicate, change the value of the node to 
# match the update action

		UPDATERECORD: foreach $aUpdate(@{$updates})
		{
			if($self->_matches($aUpdate->[1], $fieldsAsHash))
			{
				$updateHash = $aUpdate->[2];
				push(@{$originalRecords},[@fields]);
# DEBUG
#				print Data::Dumper->Dump([\$updateHash],["*updateHash"]);
# END DEBUG
				while (($field,$value)=each %{$updateHash})
				{
# DEBUG
#					print "field is $field\n";
#					print "value is $value\n";
# END DEBUG
					$nodeToUpdateRef={};
					$fieldPath = $self->{'-FIELD_MAPPINGS'}->{$field};
					$self->_getNode($fieldPath,$nodeToUpdateRef,$node,$dataDepth);
					foreach(@{$nodeToUpdateRef->{[$self->_pathToArray($fieldPath)]->[-1]}})
					{
						$self->_setNodeText($_,$value);
					}

				}		
			}
		}
	}
}


# debug method
sub _getXML
{
	my($self)=@_;
	return($self->{'xml_parser'}->toString());
}

# accessor method

sub _getPathSeparator
{
	my($self)=@_;
	return ($self->{'-PATH_SEPARATOR'});
}


# what this method does is to take a node [eg 'A'], and then take a path [ eg A::B::C::D ] , and create
# child nodes B C and D all attached to DOM node A. The value returned by the sub is the final child created, ie D.
# The allowDuplicate flag determines whether a node can have multiple children of the same name, eg:
# <A>
#	<B></B>
#	<B></B>
# </A>
# although at the moment the only time that this is allowed is in the case of children of the root node representing
# multiple records. In other cases, the multiple value is represented as a string separated by the values of the objects
# FIELD_SEPARATOR flag ie:
# 	<ROOT>
#		<RECORD>
#			<PARENT>
#				<CHILD>
#					here,is,a,csv,separated,multi,value,field
#				</CHILD>
#		</RECORD>
#		<RECORD>
#			bla...bla.....bla......	
#		</RECORD>
#	</ROOT>
# the point to note of course, is that the parent node is the only one that has children of the same name
# at the same level
	

sub _createChildNode
{
	my($self,$parent,$childPath,$childLevel,$allowDuplicate)=@_;

# DEBUG
#	print "childPath is $childPath\n";
#	print "childLevel is $childLevel\n";
# END DEBUG

	my @children;
	my $pathSep;
	my $childNode;

	@children =$self->_pathToArray($childPath);

# DEBUG
#	print "parent is @{[$parent->getTagName()]}\n";
#	print "child is $children[$childLevel]\n";
# END DEBUG

	if(($allowDuplicate)||((!$allowDuplicate)&&(!$parent->getElementsByTagName($children[$childLevel],0)->getLength())))
	{
		$childNode = $self->{'xml_parser'}->createElement($children[$childLevel]);
		$parent->appendChild($childNode);
	}
	else
	{
		$childNode = $parent->getElementsByTagName($children[$childLevel],0)->item(0);
	}

	if($childLevel<$#children)
	{
		$childLevel++;
		$self->_createChildNode($childNode,$childPath,$childLevel,$allowDuplicate);
	}
	else
	{
# DEBUG
#		print "returning @{[$childNode->getTagName()]}\n";
# END DEBUG
		return $childNode;
	}
}

# accessor method

sub _getFieldSeparator
{
	my($self)=@_;
	return($self->{'-FIELD_SEPARATOR'});
}

# takes a fully qualified path, and splits it into an array depending on the
# PATH_SEPARATOR instance variable of the object. by default, A::B::C::D becomes
# qw(A B C D)

sub _pathToArray
{
	my($self,$string)=@_;
	my $pathSep = $self->_getPathSeparator();
	my @path = split/$pathSep/,$string; 
	return(@path);
	
}


# takes an array of arrays . Each array within the array contains a fully qualified path. The method then
# determines the most recent ancestor of all the paths. This method is basically to determine the record
# root of an XML dom. Eg
# [[A B C D],[A B C E],[A B A F]]
# would lead this method to conclude that the path to a record root in the DOM is A::B, as all the records have
# at least that much of their path in common 

sub _getSharedAncestorPath
{

	my($self,@allArrays)=@_;
	my $pathSep;
# DEBUG
#	print Data::Dumper->Dump([\@allArrays],["*allArrays"]);
# END DEBUG

	$pathSep = $self->_getPathSeparator();

        my %lengths;
        my @longestArray;
        my @common;
        my $item;
        my $count=0;
        foreach(@allArrays)
        {
                @{$lengths{scalar @{$_}}}=@{$_};
        }
        foreach(sort{$b<=>$a}keys %lengths)
        {
                @longestArray=@{$lengths{$_}};
                last;
        }
        COMMON: foreach $item(@longestArray)
        {
                foreach(values %lengths)
                {
                        if((!defined $_->[$count])or($_->[$count] ne $item))
                        {
                                last COMMON;
                        }
                }
                $count++;
                push(@common,$item);
        }
        return (join $pathSep,@common);
}


# this method creates an array representation of all the nodes in the DOM, and returns it as an indexed
# hashref. So, for example:
#	
#	<PEOPLE>
#		<PERSON>
#			<NAME>
#				Nikhil
#			</NAME>
#			<AGE>
#				27
#			</AGE>
#		</PERSON>
#		<PERSON>
#			<NAME>
#				Eric
#			</NAME>
#			<AGE>
#				666
#			</AGE>
#		</PERSON>
#	</PEOPLE>
# Would become: 
# 	{
#		0	=>
#			{
#				'NODE'		=>	[ reference to DOM node ],
#				'FIELDS'	=>	[Nikhil,27]
#			},
#		1	=>
#			{
#				'NODE'		=>	[ reference to DOM node ],
#				'FIELDS'	=>	[Eric,666]
#			}
#	};
# which of course, facilitates searching across the "FIELDS" associated with a node in the case of
# search,update or delete operations
	

sub _getNodesAsFields
{
	my($self)=@_;
	my $recordRoot = $self->_getRecordRoot();
	my $recordNodeRef={};
	my $recordNode;
	my $fieldRef={};
	my $recordFieldRef={};
	my @fields;
	my $field;
	my $fullPath;
	my $recordRootLastName;
	my $sep;
	my $dataDepth;
	my @nodeValue;
	my $nodeValueLastName;
	my $valueNode;
	my @values;
	my $valueString;
	my $count=0;

	$sep = $self->_getPathSeparator();
	$recordRootLastName = [$self->_pathToArray($recordRoot)]->[-1];
	$dataDepth = scalar @{[split/$sep/,$recordRoot]};

	@fields = @{$self->{"-FIELD_NAMES"}};
# DEBUG
#	print "recordRoot is $recordRoot\n";
#	print "recordRootLastName is $recordRootLastName\n";
#	exit;
# END DEBUG

	$self->_getNode($recordRoot,$recordNodeRef,$self->{root_node},1);
	
	foreach $recordNode(@{$recordNodeRef->{$recordRootLastName}})
	{
		foreach $field(@fields)
		{
			$valueString="";
			@values=();
			$fieldRef={};

			$fullPath = $self->{'-FIELD_MAPPINGS'}->{$field};
			$nodeValueLastName = [$self->_pathToArray($fullPath)]->[-1];
# DEBUG
#			print "fullpath is $fullPath\n";
#			print "nodeValueLastName is $nodeValueLastName\n";
# END DEBUG
			$self->_getNode($fullPath,$fieldRef,$recordNode,scalar @{[$self->_pathToArray($recordRoot)]});
			foreach $valueNode(@{$fieldRef->{$nodeValueLastName}})
			{
# DEBUG
#				print $valueNode->getNodeName(),"\n";
# END DEBUG
				@values=(@values,$self->_getNodeText($valueNode));
			}
			$valueString=join $self->_getFieldSeparator(),@values;
			$recordFieldRef->{$count}->{'NODE'}=$recordNode;
			push(@{$recordFieldRef->{$count}->{'FIELDS'}},$valueString);
		}
		$count++;
	}
# DEBUG
#	print Data::Dumper->Dump([\$recordFieldRef],["*recordFieldRef"]);
#	exit;
# END DEBUG
	return($recordFieldRef);
}


# When provided a path to a node that is being looked for, this method returns all instances of that node within the DOM.
# It is returned as a hashref indexed by node last name. thus, looking for PEOPLE::PERSON in the XML sample given just above
# would result in the return of
#	
#	{
#		"PERSON"	=>	[reference to the 2 PERSON nodes in the XML example above]
#	}

sub _getNode
{
	my($self,$path,$fields,$element,$seekLevel)=@_;
	my @path;
	@path =$self->_pathToArray($path);
# DEBUG
#	print Data::Dumper->Dump([\@path],["*path"]);
# END DEBUG
	my $currentTag;
	my @children;
	my $packageName;
	my $child;
	my $seekTag;
	my $package;

	$currentTag = $element->getTagName();
# DEBUG
#	print "currentTag is $currentTag\n";
#	print "seekLevel is $seekLevel";
#	print "last item in chain is $path[-1]\n";
# END DEBUG

	if($currentTag ne $path[-1])
	{
 		@children = $element->getElementsByTagName($path[$seekLevel],0);
		$seekLevel++;
		foreach $child(@children)
		{
			$self->_getNode($path,$fields,$child,$seekLevel);
		}
	}
	else
	{
		push(@{$fields->{$path[-1]}},$element);
	}
}

# iterate through all the autoincrement fields in the DOM, and return the value of the highest one

sub _getRecordCount
{
	my($self)=@_;
	my $autoincPath;
	my $countNodeRef={};
	my $countFieldSimpleName;
	my %rev;
	my @numbers;
	my $key;
	my $countNode;
	my $currentCount=0;
	my @countVal;
	
	$autoincPath = $self->{'autoincPath'};
	$countFieldSimpleName = $self->{'countFieldSimpleName'};
	
# DEBUG
#	print "autoincPath = $autoincPath\n";
#	print "countFieldSimpleName = $countFieldSimpleName\n";
# END DEBUG
	
	$self->_getNode($autoincPath,$countNodeRef,$self->{root_node},1);

# DEBUG	
#	print Data::Dumper->Dump([\$countNodeRef],["*countNodeRef"]);
#	print keys %{$countNodeRef};
# END DEBUG

	COUNT: foreach $countNode(@{$countNodeRef->{$countFieldSimpleName}})
	{
		@countVal = $self->_getNodeText($countNode);
# DEBUG
#		print Data::Dumper->Dump([\@countVal],["*countVal"]);
# END DEBUG
		if($#countVal>-1)
		{
			if($countVal[0]>$currentCount)
			{
				$currentCount = $countVal[0];
			}
		}
		else
		{
			last COUNT;
		}	
	}
	return($currentCount);
}


# return [ all ] the text data associated with a node. 
sub _getNodeText
{
	my($self,$node)=@_;
	my @text;
	foreach($node->getChildNodes())
	{
		push(@text,$_->getData());
	}
# DEBUG
#	print "node name is ",$node->getNodeName(),"\n";
#	print Data::Dumper->Dump([\@text],["*text"]);
# END DEBUG
	return(@text);
}

# set the node text for a node, first removing the pre exisiting child node. It is assumed that
# a node has only 1 child representing text, seeing as multiple values are represented as a single 
# delimited string, as opposed to separate child nodes.

sub _setNodeText
{
	my($self,$node,$data)=@_;

# DEBUG
#	print $node->getNodeName(),"\n";
# END DEBUG

	my $textNode = $self->{'xml_parser'}->createTextNode($data);
	my @childNodes =$node->getChildNodes(); 
	if(scalar @childNodes)
	{
		$node->replaceChild($textNode,$node->getChildNodes()->item(0));
	}
	else
	{
		$node->appendChild($textNode);
	}
	return($node);
}

# sets the full path to the root of a record within the context of the DOM
sub _setRecordRoot
{
	my($self)=@_;
	my @fields;
	my $field;
	my @allPaths;

	@fields = @{$self->{'-FIELD_NAMES'}};
# DEBUG
#	print Data::Dumper->Dump([\@fields],["*fields"]);
# END DEBUG
	foreach $field(@fields)
	{
		push(@allPaths,[$self->_pathToArray($self->{'-FIELD_MAPPINGS'}->{$field})]);
	}
	$self->{'recordRoot'}=$self->_getSharedAncestorPath(@allPaths);
}

# accessor method
sub _getRecordRoot
{
	my($self)=@_;
	if(!defined $self->{'recordRoot'})
	{
		$self->_setRecordRoot();
	}
	return($self->{'recordRoot'});

}

# interface method. Doesn't do a lot.
sub _realSearch
{
	my($self,$raSearch,$lastRecordRetrieved,$maxRecordsToRetrieve,$order,$rsData)=@_;
	my $recordSet = Extropia::Core::DataSource::RecordSet->create
	(
		 @$rsData,
		-DATASOURCE 			=> $self,
		-KEY_FIELDS 			=> $self->_getKeyFields(),
		-UPDATE_STRATEGY 		=> $self->getUpdateStrategy(),
		-REAL_SEARCH_QUERY 		=> $raSearch,
		-LAST_RECORD_RETRIEVED 		=> $lastRecordRetrieved,
		-MAX_RECORDS_TO_RETRIEVE	=> $maxRecordsToRetrieve,
		-ORDER => $order
	);
# DEBUG
#	print Data::Dumper->Dump([\$recordSet],["*recordSet"]);
# END DEBUG
	return $recordSet;
}


# iterates through all the nodes in the DOM [ and their associated data, displayed as an array ] until
# values are found that match the search predicate. Returns undef on reaching the end of the records available
# for searching

sub _searchForNextRecord
{
	my($self,$search)=@_;

	return if ($self->{'_no_data'});

	my $records;
	my $node;
	my $count;
	my @fields;
	my $fieldsAsHash;
	my $retVal;
	my $key;

# DEBUG
#	print Data::Dumper->Dump([\$search],["*search"]);
#	print Data::Dumper->Dump([\$self->{_base_active_query}],["*base_active_query"]);
# END DEBUG

	$records = $self->_getNodesAsFields();
	$count = $self->{'currentSearchRow'};

	(defined($count)) or ($count=$self->{'currentSearchRow'}=-1);

	if(($count==-1) or (exists $records->{$count}))
	{
		RECORD: foreach $key(sort{$a<=>$b}keys %{$records})
		{
			if($key<=$count)
			{
				next RECORD;
			}
			$self->{'currentSearchRow'}=$key;

			$node = $records->{$key}->{"NODE"};
			@fields = @{$records->{$key}->{"FIELDS"}};
			$fieldsAsHash = $self->_recordStorage2Internal(\@fields);
			
# DEBUG
#			print Data::Dumper->Dump([$fieldsAsHash],["*fieldsAsHash"]);
# END DEBUG

			if($self->_matches($search,$fieldsAsHash))
			{
				$retVal = $self->_recordInternal2Display($fieldsAsHash);
				last RECORD;
			}
		}
	}
	else
	{
		$self->{'currentSearchRow'}=-1;
	}
	return $retVal;
}

1;
