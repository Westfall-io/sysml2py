#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 23:23:31 2023

@author: christophercox
"""


# import os

# os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import uuid as uuidlib

import astropy.units as u

from sysml2py.formatting import classtree

from sysml2py.grammar.classes import (
    Identification,
    DefinitionBody,
    DefinitionBodyItem,
    FeatureSpecializationPart,
)

from sysml2py.grammar.classes import (
    AttributeUsage,
    AttributeDefinition,
    ValuePart,
    PartUsage,
    PartDefinition,
    ItemUsage,
    ItemDefinition,
    PortUsage,
    PortDefinition,
    DefaultReferenceUsage,
    RefPrefix,
)


class Usage:
    def __init__(self):
        self.name = str(uuidlib.uuid4())
        self.children = []
        self.typedby = None
        return self

    def _ensure_body(self, subgrammar="usage"):
        # Add children
        body = []
        for abc in self.children:
            body.append(
                DefinitionBodyItem(abc.dump(child="DefinitionBody")).get_definition()
            )

        if len(body) > 0:
            getattr(self.grammar, subgrammar).completion.body.body = DefinitionBody(
                {"name": "DefinitionBody", "ownedRelatedElement": body}
            )
        return self

    def usage_dump(self, child):
        # This is a usage.

        self._ensure_body("usage")

        # Add packaging
        package = {
            "name": "StructureUsageElement",
            "ownedRelatedElement": self.grammar.get_definition(),
        }
        package = {"name": "OccurrenceUsageElement", "ownedRelatedElement": package}

        if child == "DefinitionBody":
            package = {
                "name": "OccurrenceUsageMember",
                "prefix": None,
                "ownedRelatedElement": [package],
            }

            package = {"name": "DefinitionBodyItem", "ownedRelationship": [package]}
        elif "PackageBody":
            package = {"name": "UsageElement", "ownedRelatedElement": package}
            package = {
                "name": "PackageMember",
                "ownedRelatedElement": package,
                "prefix": None,
            }

        return package

    def definition_dump(self, child):
        # This is a definition.

        self._ensure_body("definition")

        package = {
            "name": "DefinitionElement",
            "ownedRelatedElement": self.grammar.get_definition(),
        }

        if child == "DefinitionBody":
            package = {
                "name": "DefinitionMember",
                "prefix": None,
                "ownedRelatedElement": [package],
            }

            package = {"name": "DefinitionBodyItem", "ownedRelationship": [package]}

        elif child == "PackageBody":
            # Add these packets to make this dump without parents

            package = {
                "name": "PackageMember",
                "ownedRelatedElement": package,
                "prefix": None,
            }

        return package

    def _get_definition(self, child=None):
        if "usage" in self.grammar.__dict__:
            package = self.usage_dump(child)
        else:
            package = self.definition_dump(child)

        if child is None:
            package = {
                "name": "PackageBodyElement",
                "ownedRelationship": [package],
                "prefix": None,
            }

        # Add the typed by definition to the package output
        if self.typedby is not None:
            if child is None:
                package["ownedRelationship"].insert(
                    0, self.typedby._get_definition(child="PackageBody")
                )
            elif child == "PackageBody":
                package = [self.typedby._get_definition(child="PackageBody"), package]
            else:
                package["ownedRelationship"].insert(
                    0, self.typedby._get_definition(child=child)["ownedRelationship"][0]
                )

        return package

    def dump(self, child=None):
        return classtree(self._get_definition(child)).dump()

    def _set_name(self, name, short=False):
        if hasattr(self.grammar, "usage"):
            path = self.grammar.usage.declaration.declaration
        elif hasattr(self.grammar, "definition"):
            path = self.grammar.definition.declaration
        else:
            if hasattr(self.grammar.declaration, "declaration"):
                path = self.grammar.declaration.declaration
            else:
                path = self.grammar.declaration

        if path.identification is None:
            path.identification = Identification()

        if short:
            path.identification.declaredShortName = "<" + name + ">"
        else:
            self.name = name
            path.identification.declaredName = name

        return self

    def _get_name(self):
        return self.grammar.usage.declaration.declaration.identification.declaredName

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

    def _set_typed_by(self, typed):
        # Only set if the pointed object is a definition
        if "definition" in typed.grammar.__dict__:
            self.typedby = typed
            if "definition" in self.grammar.__dict__:
                raise NotImplementedError
            else:
                if self.grammar.usage.declaration.declaration.specialization is None:
                    package = {
                        "name": "QualifiedName",
                        "name1": typed.name,
                        "names": [],
                    }
                    package = {
                        "name": "FeatureType",
                        "type": package,
                        "ownedRelatedElement": [],
                    }
                    package = {"name": "OwnedFeatureTyping", "type": package}
                    package = {"name": "FeatureTyping", "ownedRelationship": package}
                    package = {"name": "TypedBy", "ownedRelationship": [package]}
                    package = {
                        "name": "Typings",
                        "typedby": package,
                        "ownedRelationship": [],
                    }
                    package = {
                        "name": "FeatureSpecialization",
                        "ownedRelationship": package,
                    }
                    package = {
                        "name": "FeatureSpecializationPart",
                        "specialization": [package],
                        "multiplicity": None,
                        "specialization2": [],
                        "multiplicity2": None,
                    }
                    self.grammar.usage.declaration.declaration.specialization = (
                        FeatureSpecializationPart(package)
                    )
        else:
            print(typed.grammar.__dict__)
            raise NotImplementedError
        return self

    def load_from_grammar(self, grammar):
        #!TODO Typed By
        self.__init__()
        self.grammar = grammar
        children = []
        if "usage" in self.grammar.__dict__:
            # This is a usage
            u_name = grammar.usage.declaration.declaration.identification.declaredName
            a_children = grammar.usage.completion.body.body.children

            if len(a_children) > 0:
                children = a_children[0].children[0].children
        else:
            # This is a definition
            u_name = grammar.definition.declaration.identification.declaredName
            a_children = grammar.definition.body.children
            if len(a_children) > 0:
                children = a_children

        if u_name is not None:
            self.name = u_name

        for child in children:
            if child.children.__class__.__name__ == "AttributeUsage":
                self.children.append(Attribute().load_from_grammar(child.children))
            elif child.children.__class__.__name__ == "StructureUsageElement":
                if child.children.children.__class__.__name__ == "PartUsage":
                    self.children.append(
                        Part().load_from_grammar(child.children.children)
                    )
                elif child.children.children.__class__.__name__ == "ItemUsage":
                    self.children.append(
                        Item().load_from_grammar(child.children.children)
                    )
                else:
                    print(child.children.children.__class__.__name__)
                    raise NotImplementedError
            else:
                print(child.children.__class__.__name__)
                raise NotImplementedError

        return self

    def add_directed_feature(self, direction, name=str(uuidlib.uuid4())):
        self._set_child(DefaultReference()._set_name(name).set_direction(direction))
        return self

    def modify_directed_feature(self, direction, name):
        child = self._get_child(name)
        if child is not None:
            pass
        else:
            raise AttributeError("Invalid Feature Name or Chain")


class Attribute(Usage):
    def __init__(self, definition=False, name=None):
        Usage.__init__(self)

        if definition:
            self.grammar = AttributeDefinition()
        else:
            self.grammar = AttributeUsage()

    def usage_dump(self, child):
        # Override - base output

        # Add children
        body = []
        for abc in self.children:
            body.append(DefinitionBodyItem(abc.dump(child=True)).get_definition())
        if len(body) > 0:
            self.grammar.usage.completion.body.body = DefinitionBody(
                {"name": "DefinitionBody", "ownedRelatedElement": body}
            )

        # Add packaging
        package = {
            "name": "NonOccurrenceUsageElement",
            "ownedRelatedElement": self.grammar.get_definition(),
        }

        if child:
            package = {
                "name": "NonOccurrenceUsageMember",
                "prefix": None,
                "ownedRelatedElement": [package],
            }
            package = {"name": "DefinitionBodyItem", "ownedRelationship": [package]}
        else:
            # Add these packets to make this dump without parents
            package = {"name": "UsageElement", "ownedRelatedElement": package}
            package = {
                "name": "PackageMember",
                "ownedRelatedElement": package,
                "prefix": None,
            }
            package = {
                "name": "PackageBodyElement",
                "ownedRelationship": [package],
                "prefix": None,
            }
        return package

    def set_value(self, value):
        if isinstance(value, u.quantity.Quantity):
            package_units = {
                "name": "QualifiedName",
                "name1": str(value.unit),
                "names": [],
            }
            package_units = {
                "name": "FeatureReferenceMember",
                "memberElement": package_units,
            }
            package_units = {
                "name": "FeatureReferenceExpression",
                "ownedRelationship": [package_units],
            }
            package_units = {
                "name": "BaseExpression",
                "ownedRelationship": package_units,
            }
            package_units = {
                "name": "PrimaryExpression",
                "operand": [],
                "base": package_units,
                "operator": [],
                "ownedRelationship": [],
            }
            package_units = {
                "name": "ExtentExpression",
                "operator": "",
                "ownedRelationship": [],
                "primary": package_units,
            }
            package_units = {
                "name": "UnaryExpression",
                "operand": [],
                "operator": None,
                "extent": package_units,
            }
            package_units = {
                "name": "ExponentiationExpression",
                "operand": [],
                "operator": [],
                "unary": package_units,
            }
            package_units = {
                "name": "MultiplicativeExpression",
                "operand": [],
                "operator": [],
                "exponential": package_units,
            }
            package_units = {
                "name": "AdditiveExpression",
                "operand": [],
                "operator": [],
                "multiplicitive": package_units,
            }
            package_units = {
                "name": "RangeExpression",
                "operand": [],
                "operator": "",
                "additive": package_units,
            }
            package_units = {
                "name": "RelationalExpression",
                "operand": [],
                "operator": [],
                "range": package_units,
            }
            package_units = {
                "name": "ClassificationExpression",
                "operand": [],
                "operator": None,
                "ownedRelationship": [],
                "relational": package_units,
            }
            package_units = {
                "name": "EqualityExpression",
                "operand": [],
                "operator": [],
                "classification": package_units,
            }
            package_units = {
                "name": "AndExpression",
                "operand": [],
                "operator": [],
                "equality": package_units,
            }
            package_units = {
                "name": "XorExpression",
                "operand": [],
                "operator": [],
                "and": package_units,
            }
            package_units = {
                "name": "OrExpression",
                "xor": package_units,
                "operand": [],
                "operator": [],
            }
            package_units = {
                "name": "ImpliesExpression",
                "operand": [],
                "operator": [],
                "or": package_units,
            }
            package_units = {
                "name": "NullCoalescingExpression",
                "implies": package_units,
                "operator": [],
                "operand": [],
            }
            package_units = {
                "name": "ConditionalExpression",
                "operator": None,
                "operand": [package_units],
            }
            package_units = {"name": "OwnedExpression", "expression": package_units}
            package_units = {
                "name": "SequenceExpression",
                "operand": [],
                "operator": "",
                "ownedRelationship": package_units,
            }

            package = {
                "name": "BaseExpression",
                "ownedRelationship": {
                    "name": "LiteralInteger",
                    "value": str(value.value),
                },
            }
            package = {
                "name": "PrimaryExpression",
                "operand": [package_units],
                "base": package,
                "operator": ["["],
                "ownedRelationship": [],
            }
            package = {
                "name": "ExtentExpression",
                "operator": "",
                "ownedRelationship": [],
                "primary": package,
            }
            package = {
                "name": "UnaryExpression",
                "operand": [],
                "operator": None,
                "extent": package,
            }
            package = {
                "name": "ExponentiationExpression",
                "operand": [],
                "operator": [],
                "unary": package,
            }
            package = {
                "name": "MultiplicativeExpression",
                "operand": [],
                "operator": [],
                "exponential": package,
            }
            package = {
                "name": "AdditiveExpression",
                "operand": [],
                "operator": [],
                "multiplicitive": package,
            }
            package = {
                "name": "RangeExpression",
                "operand": [],
                "operator": "",
                "additive": package,
            }
            package = {
                "name": "RelationalExpression",
                "operand": [],
                "operator": [],
                "range": package,
            }
            package = {
                "name": "ClassificationExpression",
                "operand": [],
                "operator": None,
                "ownedRelationship": [],
                "relational": package,
            }
            package = {
                "name": "EqualityExpression",
                "operand": [],
                "operator": [],
                "classification": package,
            }
            package = {
                "name": "AndExpression",
                "operand": [],
                "operator": [],
                "equality": package,
            }
            package = {
                "name": "XorExpression",
                "operand": [],
                "operator": [],
                "and": package,
            }
            package = {
                "name": "OrExpression",
                "xor": package,
                "operand": [],
                "operator": [],
            }
            package = {
                "name": "ImpliesExpression",
                "operand": [],
                "operator": [],
                "or": package,
            }
            package = {
                "name": "NullCoalescingExpression",
                "implies": package,
                "operator": [],
                "operand": [],
            }
            package = {
                "name": "ConditionalExpression",
                "operator": None,
                "operand": [package],
            }
            package = {"name": "OwnedExpression", "expression": package}
            package = {
                "name": "FeatureValue",
                "isDefault": False,
                "isEqual": False,
                "isInitial": False,
                "ownedRelatedElement": [package],
            }
            package = {"name": "ValuePart", "ownedRelationship": [package]}
            self.grammar.usage.completion.valuepart = ValuePart(package)
            # value.unit

        return self

    def get_value(self):
        realpart = (
            self.grammar.usage.completion.valuepart.relationships[0]
            .elements[0]
            .expression.operands[0]
            .implies.orexpression.xor.andexpression.equality.classification.relational.range.additive.multiplicitive.exponential.unary.extent.primary
        )
        real = float(realpart.base.relationship.dump())
        unit = (
            realpart.operand[0]
            .child.expression.operands[0]
            .implies.orexpression.xor.andexpression.equality.classification.relational.range.additive.multiplicitive.exponential.unary.extent.primary.base.relationship.children[
                0
            ]
            .memberElement.dump()
        )
        return real * u.Unit(unit)


class Part(Usage):
    def __init__(self, definition=False, name=None):
        Usage.__init__(self)
        if definition:
            self.grammar = PartDefinition()
        else:
            self.grammar = PartUsage()


class Item(Usage):
    def __init__(self, definition=False, name=None):
        Usage.__init__(self)
        if definition:
            self.grammar = ItemDefinition()
        else:
            self.grammar = ItemUsage()


class Port(Usage):
    def __init__(self, definition=False, name=None):
        Usage.__init__(self)
        if definition:
            self.grammar = PortDefinition()
        else:
            self.grammar = PortUsage()


class DefaultReference(Usage):
    def __init__(self):
        Usage.__init__(self)
        self.grammar = DefaultReferenceUsage()

    def set_direction(self, direction):
        r = RefPrefix()
        if direction == "in":
            r.direction.isIn = True
        elif direction == "out":
            r.direction.isOut = True
        elif direction == "inout":
            r.direction.isInOut = True
        else:
            raise NotImplementedError
        self.grammar.prefix = r
        return self

    def usage_dump(self, child):
        # This is a usage.

        self._ensure_body("definition")

        # Add packaging
        package = {
            "name": "NonOccurrenceUsageElement",
            "ownedRelatedElement": self.grammar.get_definition(),
        }

        if child == "DefinitionBody":
            package = {
                "name": "NonOccurrenceUsageMember",
                "prefix": None,
                "ownedRelatedElement": [package],
            }

            package = {"name": "DefinitionBodyItem", "ownedRelationship": [package]}
        elif "PackageBody":
            package = {"name": "UsageElement", "ownedRelatedElement": package}
            package = {
                "name": "PackageMember",
                "ownedRelatedElement": package,
                "prefix": None,
            }

        return package

    def dump(self, child=None):
        package = self.usage_dump(child)

        if child is None:
            package = {
                "name": "PackageBodyElement",
                "ownedRelationship": [package],
                "prefix": None,
            }

        # Add the typed by definition to the package output
        if self.typedby is not None:
            if child is None:
                package["ownedRelationship"].insert(
                    0, self.typedby.dump(child="PackageBody")
                )
            elif child == "PackageBody":
                package = [self.typedby.dump(child="PackageBody"), package]
            else:
                package["ownedRelationship"].insert(
                    0, self.typedby.dump(child=child)["ownedRelationship"][0]
                )

        return package
