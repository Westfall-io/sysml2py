#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:23:31 2023

@author: christophercox
"""
import uuid as uuidlib

from sysml2py.grammar.classes import Identification, DefinitionBody, DefinitionBodyItem, FeatureSpecializationPart

class Usage:
    def __init__(self):
        self.name = str(uuidlib.uuid4())
        self.children = []
        self.typedby = None
        return self
    
    def usage_dump(self, child):
        # This is a usage.
        
        # Add children
        body = []
        for abc in self.children:
            body.append(DefinitionBodyItem(abc.dump(child=True)).get_definition())
            
        if len(body) > 0:
            self.grammar.usage.completion.body.body = DefinitionBody({'name':'DefinitionBody','ownedRelatedElement':body})
            
        # Add packaging
        package = {'name':'StructureUsageElement', 'ownedRelatedElement': self.grammar.get_definition()}
        package = {'name':'OccurrenceUsageElement', 'ownedRelatedElement': package}
        
        if child:
            package = {'name':'OccurrenceUsageMember', 'prefix': None, 'ownedRelatedElement': [package]}
            package = {'name': 'DefinitionBodyItem', 'ownedRelationship': [package]}
        else:
            # Add these packets to make this dump without parents
            package = {'name':'UsageElement', 'ownedRelatedElement': package}
            package = {'name':'PackageMember', 'ownedRelatedElement': package, 'prefix': None}
            package = {'name':'PackageBodyElement', 'ownedRelationship': [package], 'prefix' : None}
        return package
    
    def definition_dump(self, child):
        # This is a definition.
        
        # Add children
        body = []
        for abc in self.children:
            body.append(DefinitionBodyItem(abc.dump(child=True)).get_definition())
        if len(body) > 0:
            self.grammar.definition.completion.body.body = DefinitionBody({'name':'DefinitionBody','ownedRelatedElement':body})
        
        if child:
            package = {'name':'DefinitionElement', 'prefix': None, 'ownedRelatedElement': self.grammar.get_definition()}
            package = {'name':'DefinitionMember', 'prefix': None, 'ownedRelatedElement': [package]}
            package = {'name': 'DefinitionBodyItem', 'ownedRelationship': [package]}
            
            
        else:
            # Add these packets to make this dump without parents
            package = {'name':'DefinitionElement', 'ownedRelatedElement': self.grammar.get_definition()}
            package = {'name':'PackageMember', 'ownedRelatedElement': package, 'prefix': None}
            package = {'name':'PackageBodyElement', 'ownedRelationship': [package], 'prefix' : None}
            
            
        return package
    
    def dump(self, child=False):
        
        if 'usage' in self.grammar.__dict__:
            package = self.usage_dump(child)
        else:
            package = self.definition_dump(child)
        
        # Add the typed by definition to the package output
        if self.typedby is not None:
            package['ownedRelationship'].insert(0,self.typedby.dump(child)['ownedRelationship'][0])
        
        return package
    
    def _set_name(self, name, short=False):
        if hasattr(self.grammar, 'usage'):
            if short:
                if self.grammar.usage.declaration.declaration.identification is None:
                    self.grammar.usage.declaration.declaration.identification=Identification()
                self.grammar.usage.declaration.declaration.identification.declaredShortName = "<"+name+">"
            else:
                self.name = name
                if self.grammar.usage.declaration.declaration.identification is None:
                    self.grammar.usage.declaration.declaration.identification=Identification()
                self.grammar.usage.declaration.declaration.identification.declaredName = name
                
            return self
        else:
            if short:
                if self.grammar.definition.declaration.identification is None:
                    self.grammar.definition.declaration.identification=Identification()
                self.grammar.definition.declaration.identification.declaredShortName = "<"+name+">"
            else:
                self.name = name
                if self.grammar.definition.declaration.identification is None:
                    self.grammar.definition.declaration.identification=Identification()
                self.grammar.definition.declaration.identification.declaredName = name
                
            return self
    
    def _get_name(self):
        return self.grammar.usage.declaration.declaration.identification.declaredName
    
    def _set_child(self, child):
        self.children.append(child)
        return self
        
    def _get_child(self, featurechain):    
        # 'x.y.z'
        if isinstance(featurechain, str):
            fc = featurechain.split('.')
        else:
            raise TypeError
            
        if fc[0] == self.name:
            # This first one must match self name, otherwise pass it all
            featurechain = '.'.join(fc[1:])
            
        for child in self.children:
            fcs = featurechain.split('.')
            if child.name == fcs[0]:
                if len(fcs) == 1:
                    return child
                else:
                    return child._get_child(featurechain)
                
    def _set_typed_by(self, typed):
        # Only set if the pointed object is a definition
        if 'definition' in typed.grammar.__dict__:
            self.typedby = typed
            if 'definition' in self.grammar.__dict__:
                raise NotImplementedError
            else:
                if self.grammar.usage.declaration.declaration.specialization is None:
                    package = {'name': 'QualifiedName', 'name1' : typed.name, 'names': []}
                    package = {'name': 'FeatureType', 'type' : package, 'ownedRelatedElement': []}
                    package = {'name': 'OwnedFeatureTyping', 'type' : package}
                    package = {'name': 'FeatureTyping', 'ownedRelationship': package}
                    package = {'name': 'TypedBy', 'ownedRelationship': [package]}
                    package = {'name': 'Typings', 'typedby': package, 'ownedRelationship': []}
                    package = {'name': 'FeatureSpecialization', 'ownedRelationship': package}
                    package = {'name': 'FeatureSpecializationPart', 'specialization': [package], 'multiplicity': None, 'specialization2': [], 'multiplicity2': None}
                    self.grammar.usage.declaration.declaration.specialization = FeatureSpecializationPart(package)
        else:
            print(typed.grammar.__dict__)
            raise NotImplementedError
        return self