#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 00:16:30 2023

@author: christophercox
"""

import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import astropy.units as u

from sysml2py.grammar.classes import (
    AttributeUsage,
    AttributeDefinition,
    DefinitionBodyItem,
    DefinitionBody,
    ValuePart,
)
from sysml2py.usage import Usage


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
