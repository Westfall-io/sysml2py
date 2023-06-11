#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 12:37:27 2023

@author: christophercox
"""

import json

def valid_definition(definition, name):
    if isinstance(definition, dict):
        if 'name' in definition:
            if definition['name'] == name:
                return True
            else:
                raise NotImplementedError
                    
        else:
            raise AttributeError('This does not seem to be valid.')
    else:
        print(definition)
        raise TypeError('This does not seem to be valid.')
        
class RootNamespace:
    def __init__(self, definition):
        self.children = []
        if 'name' in definition:
            if definition['name'] == 'PackageBodyElement':
                # This is a SysML Element
                self.load_package_body(definition['ownedRelationship'])
            elif definition['name'] == 'NamespaceBodyElement':
                # This is a KerML Element
                pass
            else:
                raise NotImplementedError('Not expecting any other root node names.')
        else:
            raise AttributeError('This does not seem to be valid.')
    
    def load_package_body(self, definition):
        for member in definition:
            # Options here are PackageMember, ElementFilterMember, AliasMember, Import
            if member['name'] == 'PackageMember':
                memberclass = PackageMember(member)
            elif member['name'] == 'ElementFilterMember':
                raise NotImplementedError
            elif member['name'] == 'AliasMember':
                raise NotImplementedError
            elif member['name'] == 'Import':
                raise NotImplementedError
            else:
                raise AttributeError('Error')
                
            self.children.append(memberclass)
            
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return '\n'.join(output)
        
class DefinitionElement:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, 'DefinitionElement'):
            # This is a SysML Element
            if definition['ownedRelatedElement']['name'] == 'Package':
                self.children.append(Package(definition['ownedRelatedElement']))
            elif definition['ownedRelatedElement']['name'] == 'PartDefinition':
                self.children.append(PartDefinition(definition['ownedRelatedElement']))
            else:
                raise NotImplementedError
            
            
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
            
        return ' '.join(filter(None, (output)))
    
class PartDefinition:
    def __init__(self, definition):
        if valid_definition(definition, 'PartDefinition'):
            self.prefix = OccurrenceDefinitionPrefix(definition['prefix'])
            self.keyword = 'part def'
            self.definition = Definition(definition['definition'])
        
    def dump(self):
        return ' '.join(filter(None, (self.prefix.dump(), self.keyword, self.definition.dump())))
    
class OccurrenceDefinitionPrefix:
    def __init__(self, definition):
        if definition == None:
            self.basicdefinitionprefix = None
            self.individual = None
            self.children = None
            self.definitionextensionkeyword = None
            
    def dump(self):
        if self.children is not None:
            output = []
            for child in self.children:
                output.append(child.dump())
        else:
            output = None
            
        return ' '.join(filter(None, (self.basicdefinitionprefix, 
            self.individual, output, self.definitionextensionkeyword)))
    
class Definition:
    def __init__(self, definition):
        if valid_definition(definition, 'Definition'):
            self.declaration = DefinitionDeclaration(definition['declaration'])
            self.body = DefinitionBody(definition['body'])
    def dump(self):
        return ''.join([self.declaration.dump(), self.body.dump()])

class DefinitionDeclaration:
    def __init__(self, definition):
        if valid_definition(definition, 'DefinitionDeclaration'):
            self.identification = Identification(definition['identification'])
            #self.subclassificationpart = SubclassificationPart(definition['subclassificationpart'])
    def dump(self):
        return self.identification.dump()#, self.subclassificationpart.dump())))
    
class SubclassificationPart:
    def __init__(self, definition):
        self.a = None
    
    def dump(self):
        return None
    
class DefinitionBody:
    def __init__(self, definition):
        if valid_definition(definition, 'DefinitionBody'):
            self.children = []
            if len(definition['ownedRelatedElement']) > 0:
                for item in definition['ownedRelatedElement']:
                    self.children.append(DefinitionBodyItem(item))
    
    def dump(self):
        if len(self.children) == 0:
            return ';'
        else:
            output = []
            for child in self.children:
                output.append(child.dump())
            return ' {\n' + '\n'.join(output) + '\n}'
        
class DefinitionBodyItem:
    def __init__(self, definition):
        if valid_definition(definition, 'DefinitionBodyItem'):
            self.children = []
            if len(definition['ownedRelationship']) > 0:
                for item in definition['ownedRelationship']:
                    if item['name'] == 'OccurrenceUsageMember':
                        self.children.append(OccurrenceUsageMember(item))
                    else:
                        raise NotImplementedError
    
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return ''.join(output)
        
class OccurrenceUsageMember:
    def __init__(self, definition):
        if valid_definition(definition, 'OccurrenceUsageMember'):
            if definition['prefix'] is not None:
                raise NotImplementedError
            else:
                self.prefix = None
            
            self.children = []
            for element in definition['ownedRelatedElement']:
                self.children.append(OccurrenceUsageElement(element))
                
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return '\n'.join(output)
    
class UsageElement:
    def __init__(self,definition):
        if valid_definition(definition, 'UsageElement'):
            if definition['ownedRelatedElement']['name'] == 'NonOccurrenceUsageElement':
                raise NotImplementedError
            elif definition['ownedRelatedElement']['name'] == 'OccurrenceUsageElement':
                self.children = OccurrenceUsageElement(definition['ownedRelatedElement'])
            else:
                raise AttributeError('This does not seem to be valid.')
    
    def dump(self):
        return self.children.dump()
    
class OccurrenceUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, 'OccurrenceUsageElement'):
            if definition['ownedRelatedElement']['name'] == 'StructureUsageElement':
                self.children = StructureUsageElement(definition['ownedRelatedElement'])
            else:
                raise NotImplementedError 
    def dump(self):
        return self.children.dump()

class StructureUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, 'StructureUsageElement'):
            if definition['ownedRelatedElement']['name'] == 'ItemUsage':
                self.children = ItemUsage(definition['ownedRelatedElement'])
            elif definition['ownedRelatedElement']['name'] == 'PartUsage':
                self.children = PartUsage(definition['ownedRelatedElement'])
            else:
                raise NotImplementedError
    def dump(self):
        return self.children.dump()
    
class PartUsage:
    def __init__(self, definition):
        if valid_definition(definition, 'PartUsage'):
            self.prefix = definition['prefix']
            self.keyword = 'part'
            self.usage = Usage(definition['usage'])
            
    def dump(self):
        return self.keyword + ' ' + self.usage.dump()
    
class ItemUsage:
    def __init__(self, definition):
        if valid_definition(definition, 'ItemUsage'):
            self.prefix = definition['prefix']
            self.keyword = 'item'
            self.usage = Usage(definition['usage'])
            
    def dump(self):
        return self.keyword + ' '+ self.usage.dump()

class Usage:
    def __init__(self, definition):
        if valid_definition(definition, 'Usage'):
            self.declaration = UsageDeclaration(definition['declaration'])
            self.completion = UsageCompletion(definition['completion'])
    
    def dump(self):
        return ''.join([self.declaration.dump(), self.completion.dump()])
    
class UsageDeclaration:
    def __init__(self, definition):
        if valid_definition(definition, 'UsageDeclaration'):
            self.declaration = FeatureDeclaration(definition['declaration'])
            
    def dump(self):
        return self.declaration.dump()
            
class FeatureDeclaration:
    def __init__(self, definition):
        if valid_definition(definition, 'FeatureDeclaration'):
            self.identification = Identification(definition['identification'])
            if definition['specialization'] is not None:
                self.specialization = FeatureSpecializationPart(definition['specialization'])
            else:
                self.specialization = None
    
    def dump(self):
        if self.specialization is not None:
            specialization = self.specialization.dump()
        else:
            specialization = None
        return ''.join(filter(None, (self.identification.dump(), specialization)))
                
class FeatureSpecializationPart:
    def __init__(self,definition):
        if valid_definition(definition, 'FeatureSpecializationPart'):
            if definition['multiplicity'] is not None:
                raise NotImplementedError
            else:
                self.multiplicity = None
                
            self.specializations = []
            for specialization in definition['specialization']:
                self.specializations.append(FeatureSpecialization(specialization))
    
    def dump(self):
        output = []
        for specialization in self.specializations:
            output.append(specialization.dump())
        return ''.join(output)
    
class FeatureSpecialization:
    def __init__(self, definition):
        if valid_definition(definition, 'FeatureSpecialization'):
            
            if 'Typings' == definition['ownedRelationship']['name']:
                self.relationship = Typings(definition['ownedRelationship'])
            else:
                raise NotImplementedError
                
    def dump(self):
        return self.relationship.dump()

class Typings:
    def __init__(self, definition):
        if valid_definition(definition, 'Typings'):
            if len(definition['ownedRelationship']) > 0:
                raise NotImplementedError
            else:
                self.relationships = []
            
            self.typing = TypedBy(definition['typedby'])
            
    def dump(self):
        return self.typing.dump()

class TypedBy:
    def __init__(self, definition):
        if valid_definition(definition, 'TypedBy'):
            self.keyword = ' : '
            
            self.relationships = []
            for relationship in definition['ownedRelationship']:
                if 'FeatureTyping' == relationship['name']:
                    self.relationships.append(FeatureTyping(relationship))
                else:
                    raise NotImplementedError
                    
    def dump(self):
        output = []
        for relationship in self.relationships:
            output.append(relationship.dump())
        return self.keyword + ''.join(output)
    
class FeatureTyping:
    def __init__(self, definition):
        if valid_definition(definition, 'FeatureTyping'):
            if definition['ownedRelationship']['name'] == 'OwnedFeatureTyping':    
                self.relationship = OwnedFeatureTyping(definition['ownedRelationship'])
            
    def dump(self):
        return self.relationship.dump()
    
class OwnedFeatureTyping:
    def __init__(self, definition):
        if valid_definition(definition, 'OwnedFeatureTyping'):
            if definition['type']['name'] == 'FeatureType':
                self.type = FeatureType(definition['type'])
            else:
                raise NotImplementedError
                
    def dump(self):
        return self.type.dump()
    
class FeatureType:
    def __init__(self, definition):
        if valid_definition(definition, 'FeatureType'):
            if len(definition['ownedRelatedElement']) > 0:
                raise NotImplementedError
            else:
                self.type = QualifiedName(definition['type'])
    
    def dump(self):
        return self.type.dump()
    
class UsageCompletion:
    def __init__(self, definition):
        if valid_definition(definition, 'UsageCompletion'):
            self.valuepart = definition['valuepart']
            self.body = UsageBody(definition['body'])
    
    def dump(self):
        return ''.join(filter(None, (self.valuepart, self.body.dump())))
            
class UsageBody:
    def __init__(self, definition):
        if valid_definition(definition, 'UsageBody'):
            self.body = None#DefinitionBody(definition['body'])
    
    def dump(self):
        return ';'

class PackageMember:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, 'PackageMember'):
            # This is a SysML Element
            self.prefix = definition['prefix']
            if definition['ownedRelatedElement']['name'] == 'DefinitionElement':
                self.children.append(DefinitionElement(definition['ownedRelatedElement']))
            elif definition['ownedRelatedElement']['name'] == 'UsageElement':
                self.children.append(UsageElement(definition['ownedRelatedElement']))
            else:
                raise AttributeError('This does not seem to be valid.')
            
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return ' '.join(filter(None, (self.prefix, ''.join(output))))
    
class Package:
    def __init__(self, definition):
        if valid_definition(definition, 'Package'):
            # Elements inside of a package
            # ownedRelationship += PrefixMetadataMember
            # declaration = PackageDeclaration
            # body = PackageBody
            self.relationships = []
            for rel in definition['ownedRelationship']:
                self.relationships.append(json.dumps(rel))
            self.declaration = PackageDeclaration(definition['declaration'])
            self.body = PackageBody(definition['body'])
            
    def dump(self):
        return ''.join([self.declaration.dump(),self.body.dump()])
    
class Identification:
    def __init__(self, definition):
        if valid_definition(definition, 'Identification'):
            if definition['declaredShortName'] == None:
                self.declaredShortName = None
            else:
                self.declaredShortName = '<'+definition['declaredShortName']+'>'
            self.declaredName = definition['declaredName']
        
    def dump(self):
        return ' '.join(filter(None, (self.declaredShortName, self.declaredName)))

class PackageDeclaration:
    def __init__(self, definition):
        if valid_definition(definition, 'PackageDeclaration'):
            self.identification = Identification(definition['identification'])
            
    def dump(self):
        return 'package '+self.identification.dump()
            
            
class PackageBody:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, 'PackageBody'):
            if 'ownedRelationship' in definition:
                for relationship in definition['ownedRelationship']:
                    if 'name' in relationship:
                        if relationship['name'] == 'PackageMember':
                            self.children.append(PackageMember(relationship))
                        elif relationship['name'] == 'ElementFilterMember':
                            raise NotImplementedError
                        elif relationship['name'] == 'AliasMember':
                            self.children.append(AliasMember(relationship))
                        elif relationship['name'] == 'Import':
                            self.children.append(Import(relationship))
                        else:
                            raise AttributeError('Failed to match this relationship')
                    else:
                        raise NotImplementedError
            else:
                raise NotImplementedError
        else:
            raise AttributeError('This does not seem to be valid.')
            
    def dump(self):
        #!TODO This won't work
        if len(self.children) == 0:
            return ';'
        else:
            output = []
            for child in self.children:
                output.append(child.dump())
            return ' { \n' + '\n'.join(output) + '\n}'
        
class AliasMember:
    def __init__(self, definition):
        if valid_definition(definition, 'AliasMember'):
            if definition['prefix'] is not None:
                raise NotImplementedError
            
            self.body = RelationshipBody(definition['body'])
                
            self.memberShortName = definition['memberShortName']
            self.memberName = definition['memberName']
            self.memberElement = QualifiedName(definition['memberElement'])
    
    def dump(self):
        if self.memberShortName is None:
            shortName = ''
        else:
            shortName = '<'+self.memberShortName+'> '
        return 'alias ' + shortName + self.memberName + 'for ' +self.memberElement.dump() + self.body.dump()
    
class RelationshipBody:
    def __init__(self, definition):
        if len(definition['ownedRelationship']) > 0:
            raise NotImplementedError
        else:
            self.children = []
            
    def dump(self):
        if len(self.children) == 0:
            return ';'
        else:
            raise NotImplementedError
            
class Import:
    def __init__(self, definition):
        if valid_definition(definition, 'Import'):
            self.body = RelationshipBody(definition['body'])
            self.children = []
            relationship = definition['ownedRelationship']
            if relationship['name'] == 'NamespaceImport':
                self.children.append(NamespaceImport(relationship))
            elif relationship['name'] == 'MembershipImport':
                raise NotImplementedError
            else:
                raise AttributeError('This does not seem to be valid')
                    
    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return ''.join(output)+self.body.dump()
    
class NamespaceImport:
    def __init__(self, definition):
        if valid_definition(definition, 'NamespaceImport'):
            self.prefix = ImportPrefix(definition['prefix'])
                
            if len(definition['ownedRelatedElement']) > 0:
                raise NotImplementedError
            else:
                self.children = []
                
            self.namespace = ImportedNamespace(definition['namespace'])
            
    def dump(self):
        return self.prefix.dump() + self.namespace.dump()
    
class ImportPrefix:
    def __init__(self, definition):
        if valid_definition(definition, 'ImportPrefix'):
            if definition['visibility'] is not None:
                self.visibility = VisibilityIndicator(definition['visibility'])
            else:
                self.visibility = None
            
            if definition['isImportAll']:
                self.keyword = 'import all '
            else:
                self.keyword = 'import '
            
    def dump(self):
        if self.visibility is None:
            return self.keyword
        else:
            return self.visibility.dump() + self.keyword

class ImportedNamespace:
    # The grammar for this file is currently broken.
    def __init__(self, definition):
        if valid_definition(definition, 'ImportedNamespace'):
            self.namespaces = QualifiedName(definition['namespace'])
            
    def dump(self):
        return self.namespaces.dump()+'::*'
    
class QualifiedName:
    def __init__(self, definition):
        if valid_definition(definition, "QualifiedName"):
            self.names = []
            for name in definition['names']:
                self.names.append(name)
    
    def dump(self):
        return '::'.join(self.names)
    
class VisibilityIndicator:
    def __init__(self, definition):
        if valid_definition(definition, 'VisibilityIndicator'):
            if definition['private']=='private' and definition['protected']=='' and definition['public']=='':
                self.keyword = 'private '
            elif definition['private']=='' and definition['protected']=='protected' and definition['public']=='':
                self.keyword = 'protected '
            elif definition['private']=='' and definition['protected']=='' and definition['public']=='public':
                self.keyword = 'public '
            else:
                self.keyword = ''
    def dump(self):
        return self.keyword