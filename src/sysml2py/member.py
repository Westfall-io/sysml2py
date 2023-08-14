#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 22:02:57 2023

@author: christophercox
"""
import uuid as uuidlib

from sysml2py.formatting import classtree
from sysml2py.grammar.classes import AliasMember, OwnedAnnotation, RelationshipBody, QualifiedName

class Alias:
    """ Alias used to indicate other names for members of this or
    imported packages.
    
    Attributes
    ----------
    name : str
        The name of this object, used only for internal.
    children : list
        A list of child members for this object.
    grammar : AliasMember
        The main grammar member for this class
        
    Methods
    -------
    dump(child=None)
        Output the text based version of this model.
    set_name(short=False)
        Set the name of the primary alias, whether in short or long form
    get_name()
        Get the long name of the alias
    set_alias_element()
        Set the element name that will have an alias.
    
    """
    def __init__(self):
        self.name = str(uuidlib.uuid4())
        self.children = []
        self.grammar = AliasMember()
        
    def _ensure_body(self):
        # Add children
        body = []
        for abc in self.children:
            body.append(
                OwnedAnnotation(
                    abc._get_definition(child="RelationshipBody")
                ).get_definition()
            )

        if len(body) > 0:
            self.grammar.body = RelationshipBody(
                {"name": "RelationshipBody", "ownedRelationship": body}
            )
        return self
    
    def _get_definition(self, child=None):
        self._ensure_body()
        package = self.grammar.get_definition()
            
        if child is None:
            
            package = {
                "name": "PackageBodyElement",
                "ownedRelationship": [package],
                "prefix": None,
            }

        return package
    
    def dump(self, child=None):
        """
        Output the text based version of this model.
        
        Parameters
        ----------
        child : str, optional
            Determines whether this object is a child or primary 
            element when outputting text. The default is None.

        Returns
        -------
        str
            Text-based SysML model.

        """
        return classtree(self._get_definition(child)).dump()
    
    def set_name(self, name:str, short=False):
        """
        Sets the name of this element which is an alias for another to
        be named with the :func:`~sysml2py.Alias.set_alias_element` 
        function.

        Parameters
        ----------
        name : str
            Name to be set.
        short : bool, optional
            Whether the short name should be set instead. The default
            is False.

        Returns
        -------
        Alias
            Returns self so that a continuous line of operations can
            be set.

        """
        if short:
            self.grammar.memberShortName = "<" + name + ">"
        else:
            self.name = name
            self.grammar.memberName = name

        return self

    def get_name(self):
        """
        Return the name of the alias.

        Returns
        -------
        str
            Name of the alias.

        """
        return self.grammar.memberName
    
    def set_alias_element(self, name:str):
        """
        Sets the name of the aliased element.

        Parameters
        ----------
        name : str
            Name of the aliased element.

        Returns
        -------
        Alias
            Returns self so that a continuous line of operations can
            be set.

        """
        definition = {'name': "QualifiedName",
                      'names': name.split('::')}
        self.grammar.memberElement = QualifiedName(definition)
        return self
    
    