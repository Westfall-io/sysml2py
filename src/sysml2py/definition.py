#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:14:18 2023

@author: christophercox
"""

import uuid as uuidlib

from sysml2py.grammar.classes import Identification, PackageMember, PackageBody

from sysml2py.grammar.classes import Package as PackageGrammar


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
            v = abc.dump(child="PackageBody")
            if isinstance(v, list):
                for subchild in v:
                    body.append(PackageMember(subchild).get_definition())
            else:
                body.append(PackageMember(v).get_definition())
        if len(body) > 0:
            self.grammar.body = PackageBody(
                {"name": "PackageBody", "ownedRelationship": body}
            )
        return self

    def dump(self, child=None):
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
