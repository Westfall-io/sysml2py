#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:14:18 2023

@author: christophercox
"""

import uuid as uuidlib

from typing import TypeVar
from textx import TextXSyntaxError

from sysml2py.formatting import classtree
from sysml2py.grammar.classes import (
    Identification,
    PackageMember,
    PackageBody,
    RootNamespace,
)
from sysml2py.grammar.classes import Package as PackageGrammar

from sysml2py import Part, Item

ModelType = TypeVar("Model", bound="Model")


class Model:
    def __init__(self):
        self.name = str(uuidlib.uuid4())
        self.children = []
        self.typedby = None
        self.grammar = None

    def load(self: type[ModelType], s: str) -> ModelType:
        from sysml2py import load_grammar

        # Try to load the grammar from the string
        try:
            definition = load_grammar(s)
        except TextXSyntaxError:
            import sys

            print("Invalid SysML input, please correct the error.")
            sys.exit()

        # Ensure this is valid
        if definition["name"] == "PackageBodyElement":
            # This is a root element
            definition = definition["ownedRelationship"]
        else:
            import sys

            print("SysML does not match a base model.")
            sys.exit()

        # Add each sub-element to children.
        member_grammar = []
        for member in definition:
            if member["ownedRelatedElement"]["name"] == "DefinitionElement":
                de = member["ownedRelatedElement"]
                if de["ownedRelatedElement"]["name"] == "Package":
                    p = Package().load_from_grammar(
                        PackageGrammar(de["ownedRelatedElement"])
                    )
                    self.children.append(p)
                    member_grammar.append(p._get_definition(child="PackageBody"))
                else:
                    raise NotImplementedError

        self.grammar = RootNamespace(
            {"name": "PackageBodyElement", "ownedRelationship": member_grammar}
        )

        return self

    def _ensure_body(self):
        # Add children
        body = []
        for abc in self.children:
            v = abc._get_definition(child="PackageBody")
            if isinstance(v, list):
                for subchild in v:
                    body.append(PackageMember(subchild).get_definition())
            else:
                body.append(PackageMember(v).get_definition())

        if len(body) > 0:
            self.grammar = RootNamespace(
                {"name": "PackageBodyElement", "ownedRelationship": body}
            )

        return self

    def _get_definition(self):
        return self.grammar.get_definition()

    def dump(self):
        self._ensure_body()
        return classtree(self._get_definition()).dump()

    def _set_child(self, child):
        self.children.append(child)
        return self

    def _get_child(self, featurechain):
        # 'x.y.z'
        if isinstance(featurechain, str):
            fc = featurechain.split(".")
        else:
            raise TypeError

        if fc[0] == self.name:
            # This first one must match self name, otherwise pass it all
            featurechain = ".".join(fc[1:])

        for child in self.children:
            fcs = featurechain.split(".")
            if child.name == fcs[0]:
                if len(fcs) == 1:
                    return child
                else:
                    return child._get_child(featurechain)


class Package:
    def __init__(self):
        self.name = str(uuidlib.uuid4())
        self.children = []
        self.typedby = None
        self.grammar = PackageGrammar()

    def _set_name(self, name, short=False):
        if short:
            if self.grammar.declaration.identification is None:
                self.grammar.declaration.identification = Identification()
            self.grammar.declaration.identification.declaredShortName = "<" + name + ">"
        else:
            self.name = name
            if self.grammar.declaration.identification is None:
                self.grammar.declaration.identification = Identification()
            self.grammar.declaration.identification.declaredName = name

        return self

    def _get_name(self):
        return self.grammar.declaration.identification.declaredName

    def _set_child(self, child):
        self.children.append(child)
        return self

    def _get_child(self, featurechain):
        # 'x.y.z'
        if isinstance(featurechain, str):
            fc = featurechain.split(".")
        else:
            raise TypeError

        if fc[0] == self.name:
            # This first one must match self name, otherwise pass it all
            featurechain = ".".join(fc[1:])

        for child in self.children:
            fcs = featurechain.split(".")
            if child.name == fcs[0]:
                if len(fcs) == 1:
                    return child
                else:
                    return child._get_child(featurechain)

    def _ensure_body(self):
        # Add children
        body = []
        for abc in self.children:
            v = abc._get_definition(child="PackageBody")
            if isinstance(v, list):
                for subchild in v:
                    body.append(PackageMember(subchild).get_definition())
            else:
                body.append(PackageMember(v).get_definition())
        if len(body) > 0:
            self.grammar.body = PackageBody(
                {"name": "PackageBody", "ownedRelationship": body}
            )

    def _get_definition(self, child=None):
        self._ensure_body()

        package = {
            "name": "DefinitionElement",
            "ownedRelatedElement": self.grammar.get_definition(),
        }
        package = {
            "name": "PackageMember",
            "ownedRelatedElement": package,
            "prefix": None,
        }
        if not child:
            package = {
                "name": "PackageBodyElement",
                "ownedRelationship": [package],
                "prefix": None,
            }

        # Add the typed by definition to the package output
        if self.typedby is not None:
            # Packages cannot be typed, they should import from other packages
            raise NotImplementedError

        return package

    def dump(self, child=None):
        return classtree(self._get_definition(child=False)).dump()

    def load_from_grammar(self, grammar):
        self.name = grammar.declaration.identification.declaredName
        self.grammar = grammar
        for child in grammar.body.children:
            if child.children[0].__class__.__name__ == "UsageElement":
                # PackageMember -> UsageElement
                if (
                    child.children[0].children.children.children.__class__.__name__
                    == "ItemUsage"
                ):
                    self.children.append(
                        Item().load_from_grammar(
                            child.children[0].children.children.children
                        )
                    )
                else:
                    print(child.children[0].children[0].__class__.__name__)
                    raise NotImplementedError
            else:
                # Not a UsageElement
                if child.children[0].children[0].__class__.__name__ == "Package":
                    self.children.append(
                        Package().load_from_grammar(child.children[0].children[0])
                    )
                elif (
                    child.children[0].children[0].__class__.__name__ == "ItemDefinition"
                ):
                    self.children.append(
                        Item().load_from_grammar(child.children[0].children[0])
                    )
                else:
                    print(child.children[0].children[0].__class__.__name__)
                    raise NotImplementedError

        # self.children.append()
        return self
