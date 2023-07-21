#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 12:37:27 2023

@author: christophercox
"""

import json


def valid_definition(definition, name):
    if isinstance(definition, dict):
        if "name" in definition:
            if definition["name"] == name:
                return True
            else:
                print(definition["name"])
                raise NotImplementedError

        else:
            raise AttributeError("This does not seem to be valid.")
    else:
        print("\n\nDefinition: {}".format(definition))
        raise TypeError("This does not seem to be valid.")


def beautify(string):
    level = 0
    lines = string.split("\n")
    ns = []
    # print(lines)
    for line in lines:
        line = line.rstrip()
        if line == "}":
            level += -1

        ns.append(level * "   " + line)

        if line[-1] == "{":
            # Last character is new bracket
            level += 1

    return "\n".join(ns)


class RootNamespace:
    def __init__(self, definition):
        self.children = []
        if "name" in definition:
            if definition["name"] == "PackageBodyElement":
                # This is a SysML Element
                self.load_package_body(definition["ownedRelationship"])
            elif definition["name"] == "NamespaceBodyElement":
                # This is a KerML Element
                pass
            else:
                print(definition)
                raise NotImplementedError("Not expecting any other root node names.")
        else:
            raise AttributeError("This does not seem to be valid.")

    def load_package_body(self, definition):
        for member in definition:
            if isinstance(member, dict):
                # Options here are PackageMember, ElementFilterMember, AliasMember, Import
                if member["name"] == "PackageMember":
                    memberclass = PackageMember(member)
                elif member["name"] == "ElementFilterMember":
                    raise NotImplementedError
                elif member["name"] == "AliasMember":
                    raise NotImplementedError
                elif member["name"] == "Import":
                    raise NotImplementedError
                else:
                    print(member["name"])
                    raise AttributeError("Error")

                self.children.append(memberclass)
            else:
                print(member)
                raise TypeError("Invalid definition, member was not type dict")

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return beautify("\n".join(output))

    def get_definition(self):
        output = {
            "name": "PackageBodyElement",  # !TODO This isn't always the case
            "ownedRelationship": [],
        }
        for member in self.children:
            output["ownedRelationship"].append(member.get_definition())
        return output


class DefinitionElement:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, "DefinitionElement"):
            # This is a SysML Element
            if isinstance(definition["ownedRelatedElement"], str):
                raise NotImplementedError
            if definition["ownedRelatedElement"]["name"] == "Package":
                self.children.append(Package(definition["ownedRelatedElement"]))
            elif definition["ownedRelatedElement"]["name"] == "PartDefinition":
                self.children.append(PartDefinition(definition["ownedRelatedElement"]))
            elif definition["ownedRelatedElement"]["name"] == "AttributeDefinition":
                self.children.append(
                    AttributeDefinition(definition["ownedRelatedElement"])
                )
            elif definition["ownedRelatedElement"]["name"] == "AnnotatingElement":
                self.children.append(
                    AnnotatingElement(definition["ownedRelatedElement"])
                )

            elif definition["ownedRelatedElement"]["name"] == "EnumerationDefinition":
                self.children.append(
                    EnumerationDefinition(definition["ownedRelatedElement"])
                )
            elif definition["ownedRelatedElement"]["name"] == "ItemDefinition":
                self.children.append(ItemDefinition(definition["ownedRelatedElement"]))
            elif definition["ownedRelatedElement"]["name"] == "ConnectionDefinition":
                self.children.append(
                    ConnectionDefinition(definition["ownedRelatedElement"])
                )
            elif definition["ownedRelatedElement"]["name"] == "PortDefinition":
                self.children.append(PortDefinition(definition["ownedRelatedElement"]))
            elif definition["ownedRelatedElement"]["name"] == "InterfaceDefinition":
                self.children.append(
                    InterfaceDefinition(definition["ownedRelatedElement"])
                )
            else:
                raise NotImplementedError

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())

        return " ".join(filter(None, (output)))

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelatedElement": []}

        for item in self.children:
            output["ownedRelatedElement"] = item.get_definition()
        return output


class InterfaceDefinition:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.prefix = None
            self.keyword = "interface def"
            self.declaration = None
            self.body = None

            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])

            if definition["declaration"] is not None:
                self.declaration = DefinitionDeclaration(definition["declaration"])

            if definition["body"] is not None:
                self.body = InterfaceBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        if self.declaration is not None:
            output.append(self.declaration.dump())
        if self.body is not None:
            output.append(self.body.dump())
        return " ".join(output)


class InterfaceBody:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.items = []
            for item in definition["item"]:
                self.items.append(InterfaceBodyItem(item))

    def dump(self):
        if len(self.items) == 0:
            return ";"
        else:
            return "{\n" + "\n".join([child.dump() for child in self.items]) + "\n}"


class InterfaceBodyItem:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                if relationship["name"] == "DefinitionMember":
                    self.children.append(DefinitionMember(relationship))
                elif relationship["name"] == "VariantUsageMember":
                    raise NotImplementedError
                elif relationship["name"] == "InterfaceNonOccurrenceUsageMember":
                    raise NotImplementedError
                elif relationship["name"] == "EmptySuccessionMember":
                    raise NotImplementedError
                elif relationship["name"] == "InterfaceOccurrenceUsageMember":
                    self.children.append(InterfaceOccurrenceUsageMember(relationship))
                elif relationship["name"] == "AliasMember":
                    self.children.append(AliasMember(relationship))
                elif relationship["name"] == "Import":
                    self.children.append(Import(relationship))

    def dump(self):
        return "\n".join([child.dump() for child in self.children])


class InterfaceOccurrenceUsageMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.prefix = None
            self.elements = []
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            for element in definition["ownedRelatedElement"]:
                self.elements.append(InterfaceOccurrenceUsageElement(element))

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        for element in self.elements:
            output.append(element.dump())

        return "\n".join(output)


class InterfaceOccurrenceUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["element"]["name"] == "DefaultInterfaceEnd":
                self.element = DefaultInterfaceEnd(definition["element"])
            elif definition["element"]["name"] == "StructureUsageElement":
                self.element = StructureUsageElement(definition["element"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.element.dump()


class DefaultInterfaceEnd:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.direction = None
            self.isAbstract = definition["isAbstract"]
            self.isVariation = definition["isVariation"]
            self.isEnd = definition["isEnd"]
            self.usage = None

            if definition["direction"] is not None:
                self.direction = FeatureDirection(definition["direction"])

            if definition["usage"] is not None:
                self.usage = Usage(definition["usage"])

    def dump(self):
        output = []
        if self.direction is not None:
            output.append(self.direction.dump())
        if self.isAbstract:
            output.append("abstract")
        elif self.isVariation:
            output.append("variation")
        if self.isEnd:
            output.append("end")
        if self.usage is not None:
            output.append(self.usage.dump())
        return " ".join(output)


class PortDefinition:
    def __init__(self, definition=None):
        self.keyword = "port def"
        self.prefix = None
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["prefix"] is not None:
                    self.prefix = DefinitionPrefix(definition["prefix"])

                if definition["definition"] is not None:
                    self.definition = Definition(definition["definition"])
                else:
                    raise AttributeError("Definition is required.")
        else:
            self.definition = Definition()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)

        if self.definition is not None:
            output.append(self.definition.dump())

        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        output["definition"] = self.definition.get_definition()
        return output


class DefinitionPrefix:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.prefix = None
            self.keywords = []

            if definition["prefix"] is not None:
                self.prefix = BasicDefinitionPrefix(definition["prefix"])

            for keyword in definition["keyword"]:
                self.keywords.append(DefinitionExtensionKeyword(keyword))

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        for keyword in self.keywords:
            output.append(keyword.dump())
        return "".join(output)


class DefinitionExtensionKeyword:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.relationships = []
            for relationship in definition["ownedRelationship"]:
                self.relationships.append(PrefixMetadataMember(relationship))

    def dump(self):
        return "".join([child.dump() for child in self.relationships])


class PrefixMetadataMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            raise NotImplementedError


class ConnectionDefinition:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.keyword = "connection def"
            self.prefix = None
            self.definition = None

            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])

            if definition["definition"] is not None:
                self.definition = Definition(definition["definition"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        if self.definition is not None:
            output.append(self.definition.dump())

        return " ".join(output)


class ItemDefinition:
    def __init__(self, definition=None):
        self.keyword = "item def"
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["prefix"] is not None:
                    self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])
                else:
                    self.prefix = None
                self.definition = Definition(definition["definition"])
        else:
            self.prefix = None
            self.definition = Definition()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        output.append(self.definition.dump())
        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()
        output["definition"] = self.definition.get_definition()
        return output


class EnumerationDefinition:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.keyword = "enum def"
            self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = EnumerationBody(definition["body"])

    def dump(self):
        return " ".join([self.keyword, self.declaration.dump() + self.body.dump()])


class EnumerationBody:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if len(definition["ownedRelationship"]) == 0:
                self.relationships = None
            else:
                self.relationships = []
                for relationship in definition["ownedRelationship"]:
                    if relationship["name"] == "AnnotatingMember":
                        self.relationships.append(AnnotatingMember(relationship))
                    else:
                        self.relationships.append(EnumerationUsageMember(relationship))

    def dump(self):
        if self.relationships is None:
            return ";"
        else:
            return (
                "{\n"
                + "\n".join([child.dump() for child in self.relationships])
                + "\n}"
            )


class EnumerationUsageMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            else:
                self.prefix = None

            if len(definition["ownedRelatedElement"]) == 0:
                raise NotImplementedError
            else:
                self.relationships = []
                for element in definition["ownedRelatedElement"]:
                    self.relationships.append(EnumeratedValue(element))

    def dump(self):
        output = [child.dump() for child in self.relationships]
        if self.prefix is not None:
            output.insert(0, self.prefix.dump())

        return " ".join(output)


class EnumeratedValue:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["keyword"] is not None:
                self.keyword = definition["keyword"]
            else:
                self.keyword = None
            self.usage = Usage(definition["usage"])

    def dump(self):
        if self.keyword is not None:
            return self.keyword + " " + self.usage.dump()
        else:
            return self.usage.dump()


class AnnotatingMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if len(definition["ownedRelatedElement"]) == 0:
                raise NotImplementedError
            else:
                self.children = []
                for element in definition["ownedRelatedElement"]:
                    self.children.append(AnnotatingElement(element))

    def dump(self):
        return " ".join([child.dump() for child in self.children])


class AnnotatingElement:
    def __init__(self, definition):
        if valid_definition(definition, "AnnotatingElement"):
            if definition["ownedRelatedElement"]["name"] == "Documentation":
                self.children = Documentation(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "CommentSysML":
                self.children = CommentSysML(definition["ownedRelatedElement"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.children.dump()


class CommentSysML:
    def __init__(self, definition):
        if valid_definition(definition, "CommentSysML"):
            self.body = definition["body"]
            if definition["identification"] is not None:
                self.identification = Identification(definition["identification"])
            else:
                self.identification = None

            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(Annotation(relationship))

    def dump(self):
        if len(self.children) > 0:
            if self.identification is not None:
                id_str = self.identification.dump()
            else:
                id_str = ""
            return (
                "comment "
                + id_str
                + "about "
                + ", ".join([child.dump() for child in self.children])
                + self.body
            )
        else:
            if self.identification is not None:
                return "comment " + self.identification.dump() + " " + self.body
            else:
                return self.body


class Annotation:
    def __init__(self, definition):
        if valid_definition(definition, "Annotation"):
            self.annotation = QualifiedName(definition["annotatedElement"])

    def dump(self):
        return self.annotation.dump()


class Documentation:
    def __init__(self, definition):
        if valid_definition(definition, "Documentation"):
            self.keyword = "doc"
            if definition["identification"] is not None:
                self.identification = Identification(definition["identification"])
            else:
                self.identification = None

            self.body = definition["body"]

    def dump(self):
        if self.identification is not None:
            return " ".join([self.keyword, self.identification.dump(), self.body])
        else:
            return " ".join([self.keyword, self.body])


class AttributeDefinition:
    def __init__(self, definition=None):
        self.keyword = "attribute def"
        if definition is not None:
            if valid_definition(definition, "AttributeDefinition"):
                if definition["prefix"] is not None:
                    raise NotImplementedError
                self.prefix = None
                self.definition = Definition(definition["definition"])
        else:
            self.prefix = None
            self.definition = Definition()

    def dump(self):
        return " ".join(
            filter(None, (self.prefix, self.keyword, self.definition.dump()))
        )

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()
        output["definition"] = self.definition.get_definition()
        return output


class PartDefinition:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "PartDefinition"):
                if definition["prefix"] is not None:
                    self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])
                else:
                    self.prefix = None
                self.keyword = "part def"
                self.definition = Definition(definition["definition"])
        else:
            self.prefix = None
            self.keyword = "part def"
            self.definition = Definition()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        output.append(self.definition.dump())

        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        output["definition"] = self.definition.get_definition()

        return output


class OccurrenceDefinitionPrefix:
    def __init__(self, definition):
        if valid_definition(definition, "OccurrenceDefinitionPrefix"):
            if definition["prefix"] is not None:
                self.prefix = BasicDefinitionPrefix(definition["prefix"])
            else:
                self.prefix = None

            self.isIndividual = definition["isIndividual"]

            self.children = []
            if len(definition["ownedRelationship"]) > 0:
                for relationship in definition["ownedRelationship"]:
                    self.children.append(LifeClassMembership(relationship))

            if len(definition["keyword"]) > 0:
                raise NotImplementedError

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        if self.isIndividual:
            output.append("individual")

        for child in self.children:
            output.append(child.dump())

        return " ".join(output)


class BasicDefinitionPrefix:
    def __init__(self, definition):
        if valid_definition(definition, "BasicDefinitionPrefix"):
            self.isAbstract = definition["isAbstract"]
            self.isVariation = definition["isVariation"]

    def dump(self):
        # Only one or the other
        if self.isAbstract:
            output = "abstract"
        if self.isVariation:
            output = "variation"
        return output


class LifeClassMembership:
    def __init__(self, definition):
        if valid_definition(definition, "LifeClassMembership"):
            raise NotImplementedError

    def dump(self):
        raise NotImplementedError


class Definition:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "Definition"):
                self.declaration = DefinitionDeclaration(definition["declaration"])
                self.body = DefinitionBody(definition["body"])
        else:
            self.declaration = DefinitionDeclaration()
            self.body = DefinitionBody()

    def dump(self):
        return " ".join([self.declaration.dump(), self.body.dump()])

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "body": self.body.get_definition(),
            "declaration": self.declaration.get_definition(),
        }


class DefinitionDeclaration:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if "identification" in definition:
                    if definition["identification"] is not None:
                        self.identification = Identification(
                            definition["identification"]
                        )
                    else:
                        self.identification = None
                else:
                    self.identification = None

                if "subclassificationpart" in definition:
                    if definition["subclassificationpart"] is not None:
                        self.subclassificationpart = SubclassificationPart(
                            definition["subclassificationpart"]
                        )
                    else:
                        self.subclassificationpart = None
                else:
                    self.subclassificationpart = None

        else:
            self.identification = Identification()
            self.subclassificationpart = None

    def dump(self):
        output = []
        if self.identification is not None:
            output.append(self.identification.dump())
        if self.subclassificationpart is not None:
            output.append(self.subclassificationpart.dump())
        return " ".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "identification": None,
            "subclassificationpart": None,
        }
        if self.identification is not None:
            output["identification"] = self.identification.get_definition()

        if self.subclassificationpart is not None:
            output[
                "subclassificationpart"
            ] = self.subclassificationpart.get_definition()

        return output


class SubclassificationPart:
    def __init__(self, definition):
        if valid_definition(definition, "SubclassificationPart"):
            self.keyword = ":> "
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(OwnedSubclassification(relationship))

    def dump(self):
        return self.keyword + ", ".join([child.dump() for child in self.children])


class OwnedSubclassification:
    def __init__(self, definition):
        if valid_definition(definition, "OwnedSubclassification"):
            self.name = QualifiedName(definition["superclassifier"])

    def dump(self):
        return self.name.dump()


class DefinitionBody:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "DefinitionBody"):
                self.children = []
                if len(definition["ownedRelatedElement"]) > 0:
                    for item in definition["ownedRelatedElement"]:
                        self.children.append(DefinitionBodyItem(item))
        else:
            self.children = []

    def dump(self):
        if len(self.children) == 0:
            return ";"
        else:
            output = []
            for child in self.children:
                output.append(child.dump())
            return " {\n" + "\n".join(output) + "\n}"

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelatedElement": []}
        for child in self.children:
            output["ownedRelatedElement"].append(child.get_definition())

        return output


class DefinitionBodyItem:
    def __init__(self, definition):
        if valid_definition(definition, "DefinitionBodyItem"):
            self.children = []
            if len(definition["ownedRelationship"]) > 0:
                for item in definition["ownedRelationship"]:
                    if item["name"] == "OccurrenceUsageMember":
                        self.children.append(OccurrenceUsageMember(item))
                    elif item["name"] == "NonOccurrenceUsageMember":
                        self.children.append(NonOccurrenceUsageMember(item))
                    elif item["name"] == "DefinitionMember":
                        self.children.append(DefinitionMember(item))
                    else:
                        print(definition)
                        raise NotImplementedError

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return "\n".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        items = []
        for item in self.children:
            items.append(item.get_definition())
        output["ownedRelationship"] = items
        return output


class DefinitionMember:
    def __init__(self, definition):
        if valid_definition(definition, "DefinitionMember"):
            if definition["prefix"] is not None:
                raise NotImplementedError
            else:
                self.prefix = None

            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(DefinitionElement(element))

    def dump(self):
        return "\n".join([child.dump() for child in self.children])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "prefix": None,
            "ownedRelatedElement": [],
        }
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        for item in self.children:
            output["ownedRelatedElement"].append(item.get_definition())
        return output


class OccurrenceUsageMember:
    def __init__(self, definition):
        if valid_definition(definition, "OccurrenceUsageMember"):
            if definition["prefix"] is not None:
                raise NotImplementedError
            else:
                self.prefix = None

            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(OccurrenceUsageElement(element))

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return "\n".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "prefix": None,
            "ownedRelatedElement": [],
        }
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        for child in self.children:
            output["ownedRelatedElement"].append(child.get_definition())

        return output


class NonOccurrenceUsageMember:
    def __init__(self, definition):
        if valid_definition(definition, "NonOccurrenceUsageMember"):
            if definition["prefix"] is not None:
                raise NotImplementedError
            else:
                self.prefix = None

            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(NonOccurrenceUsageElement(element))

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return "\n".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "prefix": None,
            "ownedRelatedElement": [],
        }
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        for child in self.children:
            output["ownedRelatedElement"].append(child.get_definition())

        return output


class UsageElement:
    def __init__(self, definition):
        if valid_definition(definition, "UsageElement"):
            if definition["ownedRelatedElement"]["name"] == "NonOccurrenceUsageElement":
                self.children = NonOccurrenceUsageElement(
                    definition["ownedRelatedElement"]
                )
            elif definition["ownedRelatedElement"]["name"] == "OccurrenceUsageElement":
                self.children = OccurrenceUsageElement(
                    definition["ownedRelatedElement"]
                )
            else:
                raise AttributeError("This does not seem to be valid.")

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelatedElement": self.children.get_definition(),
        }
        return output


class NonOccurrenceUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, "NonOccurrenceUsageElement"):
            if definition["ownedRelatedElement"]["name"] == "DefaultReferenceUsage":
                self.children = DefaultReferenceUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "AttributeUsage":
                self.children = AttributeUsage(definition["ownedRelatedElement"])
            else:
                print(definition["ownedRelatedElement"]["name"])
                raise NotImplementedError

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["ownedRelatedElement"] = self.children.get_definition()
        return output


class DefaultReferenceUsage:
    def __init__(self, definition=None):
        self.prefix = None
        self.valuepart = None
        if definition is not None:
            if valid_definition(definition, "DefaultReferenceUsage"):
                if definition["prefix"] is not None:
                    self.prefix = RefPrefix(definition["prefix"])

                self.declaration = UsageDeclaration(definition["declaration"])
                if definition["valuepart"] is not None:
                    self.valuepart = ValuePart(definition["valuepart"])

                self.body = UsageBody(definition["body"])
        else:
            self.declaration = UsageDeclaration()
            self.body = UsageBody()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.declaration.dump())
        if self.valuepart is not None:
            output.append(self.valuepart.dump())
        output.append(self.body.dump())

        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None, "valuepart": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        if self.valuepart is not None:
            output["valuepart"] = self.valuepart.get_definition()
        output["declaration"] = self.declaration.get_definition()
        output["body"] = self.body.get_definition()
        return output


class ValuePart:
    def __init__(self, definition):
        if valid_definition(definition, "ValuePart"):
            if len(definition["ownedRelationship"]) == 0:
                raise NotImplementedError
            else:
                self.relationships = []
                for relationship in definition["ownedRelationship"]:
                    if relationship["name"] == "FeatureValue":
                        self.relationships.append(FeatureValue(relationship))
                    elif relationship["name"] == "FeatureValueExpression":
                        raise NotImplementedError
                    elif relationship["name"] == "EmptyAssignmentActionMember":
                        raise NotImplementedError
                    else:
                        raise NotImplementedError

    def dump(self):
        return "".join([child.dump() for child in self.relationships])

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelationship": []}
        for child in self.relationships:
            output["ownedRelationship"].append(child.get_definition())
        return output


class FeatureValue:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.isDefault = definition["isDefault"]
            self.isInitial = definition["isInitial"]
            self.isEqual = definition["isEqual"]
            self.elements = []
            for element in definition["ownedRelatedElement"]:
                self.elements.append(OwnedExpression(element))

    def dump(self):
        output = ["="]
        if self.isDefault:
            output.append("default")
        if self.isEqual:
            output.append("=")
        elif self.isInitial:
            output.append(":=")
        for child in self.elements:
            output.append(child.dump())
        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelatedElement": []}
        for child in self.elements:
            output["ownedRelatedElement"].append(child.get_definition())
        output["isEqual"] = self.isEqual
        output["isInitial"] = self.isInitial
        output["isDefault"] = self.isDefault
        return output


class OwnedExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.expression = ConditionalExpression(definition["expression"])

    def dump(self):
        return self.expression.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "expression": self.expression.get_definition(),
        }


class ConditionalExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["operand"] is not None:
                self.operands = []
                for op in definition["operand"]:
                    self.operands.append(NullCoalescingExpression(op))
            else:
                raise NotImplementedError

    def dump(self):
        return "".join(child.dump() for child in self.operands)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "operator": [], "operand": []}
        for child in self.operands:
            output["operand"].append(child.get_definition())
        return output


class NullCoalescingExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["implies"] is not None:
                self.implies = ImpliesExpression(definition["implies"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.implies.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "implies": self.implies.get_definition(),
        }
        return output


class ImpliesExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["or"] is not None:
                self.orexpression = OrExpression(definition["or"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.orexpression.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "or": self.orexpression.get_definition(),
        }
        return output


class OrExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["xor"] is not None:
                self.xor = XorExpression(definition["xor"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.xor.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "xor": self.xor.get_definition(),
        }
        return output


class XorExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["and"] is not None:
                self.andexpression = AndExpression(definition["and"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.andexpression.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "and": self.andexpression.get_definition(),
        }
        return output


class AndExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["equality"] is not None:
                self.equality = EqualityExpression(definition["equality"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.equality.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "equality": self.equality.get_definition(),
        }
        return output


class EqualityExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["classification"] is not None:
                self.classification = ClassificationExpression(
                    definition["classification"]
                )
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.classification.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "classification": self.classification.get_definition(),
        }
        return output


class ClassificationExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["relational"] is not None:
                self.relational = RelationalExpression(definition["relational"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] is None):
                raise NotImplementedError

    def dump(self):
        return self.relational.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": None,
            "operand": [],
            "relational": self.relational.get_definition(),
        }
        return output


class RelationalExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["range"] is not None:
                self.range = RangeExpression(definition["range"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.range.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "range": self.range.get_definition(),
        }
        return output


class RangeExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["additive"] is not None:
                self.additive = AdditiveExpression(definition["additive"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == ""):
                raise NotImplementedError

    def dump(self):
        return self.additive.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": "",
            "operand": [],
            "additive": self.additive.get_definition(),
        }
        return output


class AdditiveExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["multiplicitive"] is not None:
                self.multiplicitive = MultiplicativeExpression(
                    definition["multiplicitive"]
                )
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.multiplicitive.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "multiplicitive": self.multiplicitive.get_definition(),
        }
        return output


class MultiplicativeExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["exponential"] is not None:
                self.exponential = ExponentiationExpression(definition["exponential"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.exponential.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "exponential": self.exponential.get_definition(),
        }
        return output


class ExponentiationExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["unary"] is not None:
                self.unary = UnaryExpression(definition["unary"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError

    def dump(self):
        return self.unary.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "unary": self.unary.get_definition(),
        }
        return output


class UnaryExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["extent"] is not None:
                self.extent = ExtentExpression(definition["extent"])
            else:
                raise NotImplementedError

            if not (definition["operand"] == [] and definition["operator"] is None):
                raise NotImplementedError

    def dump(self):
        return self.extent.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": None,
            "operand": [],
            "extent": self.extent.get_definition(),
        }
        return output


class ExtentExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["primary"] is not None:
                self.primary = PrimaryExpression(definition["primary"])
            else:
                raise NotImplementedError

            if not (definition["operator"] == ""):
                raise NotImplementedError

    def dump(self):
        return self.primary.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": "",
            "operand": [],
            "primary": self.primary.get_definition(),
            "ownedRelationship": [],
        }
        return output


class PrimaryExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["base"] is not None:
                self.base = BaseExpression(definition["base"])
            else:
                raise NotImplementedError

            if len(definition["ownedRelationship"]) > 0:
                raise NotImplementedError

            self.operator = []
            self.operand = []

            if not (definition["operand"] == [] and definition["operator"] == []):
                for child in definition["operator"]:
                    self.operator.append(child)
                for child in definition["operand"]:
                    if child["name"] == "SequenceExpression":
                        self.operand.append(SequenceExpression(child))

    def dump(self):
        output = [self.base.dump()]
        for k, v in enumerate(self.operator):
            if v == "#":
                output.append("# ({})".format(self.operand[k].dump()))

            if v == "[":
                output.append("[{}]".format(self.operand[k].dump()))

            if v == "." or v == ".?":
                raise NotImplementedError
        if len(output) == 1:
            return str(output[0])
        else:
            return " ".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "base": self.base.get_definition(),
            "ownedRelationship": [],
        }
        for child in self.operand:
            output["operand"].append(child.get_definition())

        for child in self.operator:
            output["operator"].append(child)
        return output


class SequenceExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if not (definition["operand"] == [] and definition["operator"] == ""):
                raise NotImplementedError

            self.child = None
            if definition["ownedRelationship"] is not None:
                if definition["ownedRelationship"]["name"] == "OwnedExpression":
                    self.child = OwnedExpression(definition["ownedRelationship"])

    def dump(self):
        return self.child.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": "",
            "operand": [],
            "ownedRelationship": self.child.get_definition(),
        }
        return output


class BaseExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelationship"]["name"] == "FeatureReferenceExpression":
                self.relationship = FeatureReferenceExpression(
                    definition["ownedRelationship"]
                )
            elif definition["ownedRelationship"]["name"] == "LiteralInteger":
                self.relationship = LiteralInteger(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "LiteralString":
                self.relationship = LiteralString(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "LiteralReal":
                self.relationship = LiteralReal(definition["ownedRelationship"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.relationship.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": self.relationship.get_definition(),
        }
        return output


class FeatureReferenceExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(FeatureReferenceMember(relationship))

    def dump(self):
        return "".join([child.dump() for child in self.children])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": [],
        }
        for child in self.children:
            output["ownedRelationship"].append(child.get_definition())
        return output


class FeatureReferenceMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.memberElement = QualifiedName(definition["memberElement"])

    def dump(self):
        return self.memberElement.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "memberElement": self.memberElement.get_definition(),
        }
        return output


class OccurrenceUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, "OccurrenceUsageElement"):
            if definition["ownedRelatedElement"]["name"] == "StructureUsageElement":
                self.children = StructureUsageElement(definition["ownedRelatedElement"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "ownedRelatedElement": self.children.get_definition(),
        }


class StructureUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, "StructureUsageElement"):
            if definition["ownedRelatedElement"]["name"] == "ItemUsage":
                self.children = ItemUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "PartUsage":
                self.children = PartUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "ConnectionUsage":
                self.children = ConnectionUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "PortUsage":
                self.children = PortUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "InterfaceUsage":
                self.children = InterfaceUsage(definition["ownedRelatedElement"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "ownedRelatedElement": self.children.get_definition(),
        }


class InterfaceUsage:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.prefix = None
            self.keyword = "interface"
            self.declaration = None
            self.body = None

            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])

            if definition["declaration"] is not None:
                self.declaration = InterfaceUsageDeclaration(definition["declaration"])

            if definition["body"] is not None:
                self.body = InterfaceBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        if self.declaration is not None:
            output.append(self.declaration.dump())
        if self.body is not None:
            output.append(self.body.dump())

        return " ".join(output)


class InterfaceUsageDeclaration:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.declaration = None
            self.keyword = None
            self.part = None

            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

            if definition["part1"] is not None:
                self.part = InterfacePart(definition["part1"])
                # The connect usage was optional and it was used here.
                self.keyword = "connect\n"
            elif definition["part2"] is not None:
                self.part = InterfacePart(definition["part2"])

    def dump(self):
        output = []
        if self.declaration is not None:
            output.append(self.declaration.dump())

        if self.keyword is not None:
            output.append(self.keyword)

        if self.part is not None:
            output.append(self.part.dump())

        return " ".join(output)


class InterfacePart:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["binarypart"] is not None:
                self.children = BinaryInterfacePart(definition["binarypart"])
            elif definition["narypart"] is not None:
                raise NotImplementedError
            else:
                raise NotImplementedError

    def dump(self):
        return self.children.dump()


class BinaryInterfacePart:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(InterfaceEndMember(relationship))

    def dump(self):
        # Assume this is only ever 2 long
        if len(self.children) > 2:
            raise NotImplementedError

        return self.children[0].dump() + " to " + self.children[1].dump()


class InterfaceEndMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = InterfaceEnd(definition["ownedRelatedElement"])

    def dump(self):
        return self.child.dump()


class InterfaceEnd:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaredName"] is not None:
                self.name = definition["declaredName"]
                self.keyword = "::>"
            else:
                self.name = None

            self.relationships = []
            for relationship in definition["ownedRelationship"]:
                if relationship["name"] == "OwnedReferenceSubsetting":
                    self.relationships.append(OwnedReferenceSubsetting(relationship))
                elif relationship["name"] == "OwnedMultiplicity":
                    self.relationships.append(OwnedMultiplicity(relationship))
                else:
                    return NotImplementedError

    def dump(self):
        output = []
        if self.name is not None:
            output.append(self.name)
            output.append(self.keyword)

        for relationship in self.relationships:
            output.append(relationship.dump())

        return " ".join(output)


class PortUsage:
    def __init__(self, definition=None):
        self.keyword = "port"
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                self.prefix = None
                self.usage = None

                if definition["prefix"] is not None:
                    self.prefix = OccurrenceUsagePrefix(definition["prefix"])

                if definition["usage"] is not None:
                    self.usage = Usage(definition["usage"])
        else:
            self.prefix = None
            self.usage = Usage()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)

        if self.usage is not None:
            output.append(self.usage.dump())

        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        output["usage"] = self.usage.get_definition()

        return output


class ConnectionUsage:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.prefix = None
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])

            self.declaration = None
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

            self.keyword = "connection"
            self.keyword2 = "connect\n"

            self.part = None
            if definition["part"] is not None:
                self.part = ConnectorPart(definition["part"])

            self.body = UsageBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        if self.declaration is not None:
            output.append(self.keyword)
            output.append(self.declaration.dump())

        if self.part is not None:
            output.append(self.keyword2)
            output.append(self.part.dump())

        output.append(self.body.dump())

        return " ".join(output)


class ConnectorPart:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["part"]["name"] == "BinaryConnectorPart":
                self.part = BinaryConnectorPart(definition["part"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.part.dump()


class BinaryConnectorPart:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(ConnectorEndMember(relationship))

    def dump(self):
        return " to ".join([child.dump() for child in self.children])


class ConnectorEndMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(ConnectorEnd(element))

    def dump(self):
        return "".join([child.dump() for child in self.children])


class ConnectorEnd:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.declaredName = None
            if definition["declaredName"] is not None:
                self.declaredName = definition["declaredName"]

            self.children = []
            for relationship in definition["ownedRelationship"]:
                if relationship["name"] == "OwnedReferenceSubsetting":
                    self.children.append(OwnedReferenceSubsetting(relationship))
                else:
                    self.children.append(OwnedMultiplicity(relationship))

    def dump(self):
        output = []
        if self.declaredName is not None:
            output.append(self.declaredName)
            output.append("references")

        for child in self.children:
            output.append(child.dump())

        return " ".join(output)


class OwnedReferenceSubsetting:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.referencedFeature = None
            if definition["referencedFeature"] is not None:
                self.referencedFeature = QualifiedName(definition["referencedFeature"])

            self.elements = []
            for element in definition["ownedRelatedElement"]:
                self.elements.append(OwnedFeatureChain(element))

    def dump(self):
        if self.referencedFeature is not None:
            return self.referencedFeature.dump()
        else:
            return "".join([child.dump() for child in self.elements])


class AttributeUsage:
    def __init__(self, definition=None):
        self.keyword = "attribute"
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["prefix"] is not None:
                    raise NotImplementedError
                else:
                    self.prefix = None
                self.usage = Usage(definition["usage"])
        else:
            self.prefix = None
            self.usage = Usage()

    def dump(self):
        return self.keyword + " " + self.usage.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        output["usage"] = self.usage.get_definition()

        return output


class PartUsage:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "PartUsage"):
                if definition["prefix"] is not None:
                    self.prefix = OccurrenceUsagePrefix(definition["prefix"])
                else:
                    self.prefix = None

                self.keyword = "part"
                self.usage = Usage(definition["usage"])
        else:
            self.prefix = None
            self.keyword = "part"
            self.usage = Usage()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        output.append(self.usage.dump())
        return " ".join(output)

    def get_definition(self):
        pre = None
        if self.prefix is not None:
            pre = self.prefix.get_definition()

        u = None
        if self.usage is not None:
            u = self.usage.get_definition()

        return {"name": self.__class__.__name__, "prefix": pre, "usage": u}


class OccurrenceUsagePrefix:
    def __init__(self, definition):
        if valid_definition(definition, "OccurrenceUsagePrefix"):
            self.prefix = BasicUsagePrefix(definition["prefix"])
            self.isIndividual = definition["isIndividual"]
            if definition["portionKind"] is not None:
                self.portionKind = PortionKind(definition["portionKind"])
            else:
                self.portionKind = None

            if len(definition["usageExtension"]) > 0:
                raise NotImplementedError

    def dump(self):
        output = []
        output.append(self.prefix.dump())
        if self.isIndividual:
            output.append("individual")

        if self.portionKind is not None:
            output.append(self.portionKind.dump())

        return " ".join(output)


class PortionKind:
    def __init__(self, definition):
        if valid_definition(definition, "PortionKind"):
            raise NotImplementedError

    def dump(self):
        raise NotImplementedError


class BasicUsagePrefix:
    def __init__(self, definition):
        if valid_definition(definition, "BasicUsagePrefix"):
            if definition["prefix"] is not None:
                self.prefix = RefPrefix(definition["prefix"])
            else:
                # This happens when nothing was found in RefPrefix.
                self.prefix = None
            self.isReference = definition["isReference"]

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        if self.isReference:
            output.append("ref")

        return " ".join(output)


class RefPrefix:
    def __init__(self, definition=None):
        self.direction = None
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["direction"] is not None:
                    self.direction = FeatureDirection(definition["direction"])

                self.isAbstract = definition["isAbstract"]
                self.isVariation = definition["isVariation"]
                self.isReadOnly = definition["isReadOnly"]
                self.isDerived = definition["isDerived"]
                self.isEnd = definition["isEnd"]

        else:
            self.direction = FeatureDirection()
            self.isAbstract = False
            self.isVariation = False
            self.isReadOnly = False
            self.isDerived = False
            self.isEnd = False

    def dump(self):
        output = []
        if self.direction is not None:
            direction = self.direction.dump()
            if not direction == "":
                output.append(direction)

        if self.isAbstract:
            output.append("abstract")
        elif self.isVariation:
            output.append("variation")

        if self.isReadOnly:
            output.append("readonly")

        if self.isDerived:
            output.append("derived")

        if self.isEnd:
            output.append("end")

        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["isAbstract"] = self.isAbstract
        output["isVariation"] = self.isVariation
        output["isReadOnly"] = self.isReadOnly
        output["isDerived"] = self.isDerived
        output["isEnd"] = self.isEnd
        output["direction"] = self.direction.get_definition()
        return output


class FeatureDirection:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                self.isIn = definition["in"] == "in "
                self.isOut = definition["out"] == "out"
                self.isInOut = definition["inout"] == "inout"
        else:
            self.isIn = False
            self.isOut = False
            self.isInOut = False

    def dump(self):
        if self.isInOut:
            return "inout"
        elif self.isIn:
            return "in"
        elif self.isOut:
            return "out"
        else:
            return ""

    def get_definition(self):
        output = {"name": self.__class__.__name__, "in": "", "out": "", "inout": ""}
        if self.isIn:
            output["in"] = "in "

        if self.isOut:
            output["out"] = "out"

        if self.isInOut:
            output["inout"] = "inout"
        return output


class ItemUsage:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "ItemUsage"):
                self.prefix = None
                if definition["prefix"] is not None:
                    self.prefix = OccurrenceUsagePrefix(definition["prefix"])
                self.keyword = "item"
                self.usage = Usage(definition["usage"])
        else:
            # Create an empty item
            self.prefix = None
            self.keyword = "item"
            self.usage = Usage()

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.usage.dump())
        return " ".join(output)

    def get_definition(self):
        output = {}
        output["name"] = self.__class__.__name__
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()
        else:
            output["prefix"] = None
        output["usage"] = self.usage.get_definition()
        return output


class Usage:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "Usage"):
                self.declaration = UsageDeclaration(definition["declaration"])
                self.completion = UsageCompletion(definition["completion"])
        else:
            self.declaration = UsageDeclaration()
            self.completion = UsageCompletion()

    def dump(self):
        return "".join([self.declaration.dump(), self.completion.dump()])

    def get_definition(self):
        output = {}
        output["name"] = self.__class__.__name__
        output["declaration"] = self.declaration.get_definition()
        output["completion"] = self.completion.get_definition()
        return output


class UsageDeclaration:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "UsageDeclaration"):
                self.declaration = FeatureDeclaration(definition["declaration"])
        else:
            self.declaration = FeatureDeclaration()

    def dump(self):
        return self.declaration.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "declaration": self.declaration.get_definition(),
        }


class FeatureDeclaration:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "FeatureDeclaration"):
                if definition["identification"] is not None:
                    self.identification = Identification(definition["identification"])
                else:
                    self.identification = None

                if definition["specialization"] is not None:
                    self.specialization = FeatureSpecializationPart(
                        definition["specialization"]
                    )
                else:
                    self.specialization = None
        else:
            self.identification = None
            self.specialization = None

    def dump(self):
        output = []
        if self.identification is not None:
            output.append(self.identification.dump())

        if self.specialization is not None:
            output.append(self.specialization.dump())

        return "".join(output)

    def get_definition(self):
        iden = None
        spec = None
        if self.identification is not None:
            iden = self.identification.get_definition()

        if self.specialization is not None:
            spec = self.specialization.get_definition()

        return {
            "name": self.__class__.__name__,
            "identification": iden,
            "specialization": spec,
        }


class FeatureSpecializationPart:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "FeatureSpecializationPart"):
                if definition["multiplicity"] is not None:
                    # We found the set where one specialization came first
                    # ( specialization+=FeatureSpecialization )+
                    #    multiplicity=MultiplicityPart?
                    #    specialization2+=FeatureSpecialization*
                    self.multiplicity = MultiplicityPart(definition["multiplicity"])
                elif definition["multiplicity2"] is not None:
                    # We found the set where the multiplicity came first
                    # multiplicity2=MultiplicityPart specialization+=FeatureSpecialization*
                    self.multiplicity = MultiplicityPart(definition["multiplicity2"])
                else:
                    # We found the case where none were specified
                    self.multiplicity = None

                self.specializations = []
                for specialization in definition["specialization"]:
                    self.specializations.append(FeatureSpecialization(specialization))

                self.specializations2 = []
                if definition["specialization2"] is not None:
                    for specialization in definition["specialization2"]:
                        self.specializations2.append(
                            FeatureSpecialization(specialization)
                        )
        else:
            self.multiplicity = None
            self.specializations = []
            self.specializations2 = []

    def dump(self):
        if len(self.specializations2) > 0:
            # Multiplicity in between
            output = [child.dump() for child in self.specializations]
            if self.multiplicity is not None:
                output.append(self.multiplicity.dump())

            for child in self.specializations2:
                output.append(child.dump())

        elif len(self.specializations) == 1 and self.multiplicity is not None:
            # Case 1 - modified for the case where specializations2 would be empty
            output = [child.dump() for child in self.specializations]
            output.append(self.multiplicity.dump())

        else:
            # Multiplicity at start or no multiplicity found
            output = []
            if self.multiplicity is not None:
                output.append(self.multiplicity.dump())

            for child in self.specializations:
                output.append(child.dump())

        return "".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "multiplicity": None,
            "multiplicity2": None,  # This is never used in this fashion.
            "specialization": [],
            "specialization2": [],
        }

        if self.multiplicity is not None:
            output["multiplicity"].get_definition()

        if len(self.specializations) > 0:
            for child in self.specializations:
                output["specialization"].append(child.get_definition())

        if len(self.specializations2) > 0:
            for child in self.specializations2:
                output["specialization2"].append(child.get_definition())

        return output


class MultiplicityPart:
    def __init__(self, definition):
        if valid_definition(definition, "MultiplicityPart"):
            self.isOrdered = definition["isOrdered"]
            self.isNonunique = definition["isNonunique"]
            self.isOrdered2 = definition["isOrdered"]
            self.isNonunique2 = definition["isNonunique"]

            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(OwnedMultiplicity(relationship))

    def dump(self):
        output = [child.dump() for child in self.children]

        if self.isOrdered and not self.isOrdered2:
            output.append("ordered")

        if self.isNonunique or self.isNonunique2:
            output.append("nonunique")

        if self.isOrdered2 and not self.isOrdered:
            output.append("ordered")

        return " ".join(output)


class OwnedMultiplicity:
    def __init__(self, definition):
        if valid_definition(definition, "OwnedMultiplicity"):
            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(MultiplicityRange(element))

    def dump(self):
        output = [child.dump() for child in self.children]
        return "".join(output)


class MultiplicityRange:
    def __init__(self, definition):
        if valid_definition(definition, "MultiplicityRange"):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(MultiplicityExpressionMember(relationship))

    def dump(self):
        output = [child.dump() for child in self.children]
        return "[" + "..".join(output) + "]"


class MultiplicityExpressionMember:
    def __init__(self, definition):
        if valid_definition(definition, "MultiplicityExpressionMember"):
            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(MultiplicityRelatedElement(element))

    def dump(self):
        return "".join([child.dump() for child in self.children])


class MultiplicityRelatedElement:
    def __init__(self, definition):
        if valid_definition(definition, "MultiplicityRelatedElement"):
            if "name" in definition["ownedRelatedElement"]:
                if definition["ownedRelatedElement"]["name"] == "LiteralInteger":
                    self.element = LiteralInteger(definition["ownedRelatedElement"])
                elif definition["ownedRelatedElement"]["name"] == "LiteralInfinity":
                    self.element = LiteralInfinity(definition["ownedRelatedElement"])
                else:
                    raise NotImplementedError

    def dump(self):
        return str(self.element.dump())


class LiteralString:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.element = definition["value"]

    def dump(self):
        return self.element


class LiteralInteger:
    def __init__(self, definition):
        if valid_definition(definition, "LiteralInteger"):
            self.element = definition["value"]

    def dump(self):
        return self.element

    def get_definition(self):
        return {"name": self.__class__.__name__, "value": self.element}


class LiteralReal:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.element = definition["value"]

    def dump(self):
        return self.element


class LiteralInfinity:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.element = "*"

    def dump(self):
        return self.element


class FeatureSpecialization:
    def __init__(self, definition):
        if valid_definition(definition, "FeatureSpecialization"):
            if definition["ownedRelationship"]["name"] == "Typings":
                self.relationship = Typings(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "Subsettings":
                self.relationship = Subsettings(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "References":
                raise NotImplementedError
            elif definition["ownedRelationship"]["name"] == "Redefinitions":
                self.relationship = Redefinitions(definition["ownedRelationship"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.relationship.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": self.relationship.get_definition(),
        }
        return output


class Redefinitions:
    def __init__(self, definition):
        if valid_definition(definition, "Redefinitions"):
            if len(definition["ownedRelationship"]) > 0:
                raise NotImplementedError

            self.children = Redefines(definition["redefines"])

    def dump(self):
        return self.children.dump()


class Redefines:
    def __init__(self, definition):
        if valid_definition(definition, "Redefines"):
            self.keyword = " :>>"
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(OwnedRedefinition(relationship))

    def dump(self):
        output = [child.dump() for child in self.children]
        output.insert(0, self.keyword)
        return " ".join(output)


class OwnedRedefinition:
    def __init__(self, definition):
        if valid_definition(definition, "OwnedRedefinition"):
            if len(definition["ownedRelatedElement"]) > 0:
                raise NotImplementedError

            self.redefinedFeature = QualifiedName(definition["redefinedFeature"])

    def dump(self):
        return self.redefinedFeature.dump()


class Subsettings:
    def __init__(self, definition):
        if valid_definition(definition, "Subsettings"):
            # Subsets ( ',' ownedRelationship += OwnedSubsetting )*
            self.keyword = ":>"
            if len(definition["ownedRelationship"]) > 0:
                self.children = []
                for relationship in definition["ownedRelationship"]:
                    self.children.append(OwnedSubsetting(relationship))
            else:
                raise NotImplementedError

    def dump(self):
        return self.keyword + ", ".join([child.dump() for child in self.children])


class OwnedSubsetting:
    def __init__(self, definition):
        if valid_definition(definition, "OwnedSubsetting"):
            # subsettedFeature = QualifiedName | ownedRelatedElement += OwnedFeatureChain
            if definition["subsettedFeature"] is not None:
                self.elements = [QualifiedName(definition["subsettedFeature"])]
            else:
                self.elements = []
                for element in definition["ownedRelatedElement"]:
                    self.elements.append(OwnedFeatureChain(element))

    def dump(self):
        return " ".join([child.dump() for child in self.elements])


class OwnedFeatureChain:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.feature = FeatureChain(definition["feature"])

    def dump(self):
        return self.feature.dump()


class FeatureChain:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = []
            for relationship in definition["ownedRelationship"]:
                self.children.append(OwnedFeatureChaining(relationship))

    def dump(self):
        return ".".join([child.dump() for child in self.children])


class OwnedFeatureChaining:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.chainingFeature = QualifiedName(definition["chainingFeature"])

    def dump(self):
        return self.chainingFeature.dump()


class Typings:
    def __init__(self, definition):
        if valid_definition(definition, "Typings"):
            if len(definition["ownedRelationship"]) > 0:
                raise NotImplementedError
            else:
                self.relationships = []

            self.typing = TypedBy(definition["typedby"])

    def dump(self):
        return self.typing.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": self.relationships,
            "typedby": self.typing.get_definition(),
        }
        return output


class TypedBy:
    def __init__(self, definition):
        if valid_definition(definition, "TypedBy"):
            self.keyword = " : "

            self.relationships = []
            for relationship in definition["ownedRelationship"]:
                if "FeatureTyping" == relationship["name"]:
                    self.relationships.append(FeatureTyping(relationship))
                else:
                    raise NotImplementedError

    def dump(self):
        output = []
        for relationship in self.relationships:
            output.append(relationship.dump())
        return self.keyword + "".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelationship": []}
        for child in self.relationships:
            output["ownedRelationship"].append(child.get_definition())

        return output


class FeatureTyping:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelationship"]["name"] == "OwnedFeatureTyping":
                self.relationship = OwnedFeatureTyping(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "ConjugatedPortTyping":
                self.relationship = ConjugatedPortTyping(
                    definition["ownedRelationship"]
                )
            else:
                raise NotImplementedError

    def dump(self):
        return self.relationship.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": self.relationship.get_definition(),
        }

        return output


class ConjugatedPortTyping:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.keyword = "~"
            # We skip a step in the grammar here.
            self.name = QualifiedName(definition["conjugatedPortDefinition"])

    def dump(self):
        return self.keyword + self.name.dump()


class OwnedFeatureTyping:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["type"]["name"] == "FeatureType":
                self.type = FeatureType(definition["type"])
            else:
                raise NotImplementedError

    def dump(self):
        return self.type.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__, "type": self.type.get_definition()}

        return output


class FeatureType:
    def __init__(self, definition):
        if valid_definition(definition, "FeatureType"):
            if len(definition["ownedRelatedElement"]) > 0:
                raise NotImplementedError
            else:
                self.type = QualifiedName(definition["type"])

    def dump(self):
        return self.type.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelatedElement": [],
            "type": self.type.get_definition(),
        }
        return output


class UsageCompletion:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "UsageCompletion"):
                if definition["valuepart"] is None:
                    self.valuepart = None
                else:
                    self.valuepart = ValuePart(definition["valuepart"])
                self.body = UsageBody(definition["body"])
        else:
            self.valuepart = None
            self.body = UsageBody()

    def dump(self):
        output = []
        if self.valuepart is not None:
            output.append(self.valuepart.dump())

        output.append(self.body.dump())
        return "".join(output)

    def get_definition(self):
        vp = None
        if self.valuepart is not None:
            vp = self.valuepart.get_definition()

        return {
            "name": self.__class__.__name__,
            "valuepart": vp,
            "body": self.body.get_definition(),
        }


class UsageBody:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "UsageBody"):
                self.body = DefinitionBody(definition["body"])
        else:
            self.body = DefinitionBody()

    def dump(self):
        return self.body.dump()

    def get_definition(self):
        return {"name": self.__class__.__name__, "body": self.body.get_definition()}


class PackageMember:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, "PackageMember"):
            # This is a SysML Element
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            else:
                self.prefix = None

            if definition["ownedRelatedElement"]["name"] == "DefinitionElement":
                self.children.append(
                    DefinitionElement(definition["ownedRelatedElement"])
                )
            elif definition["ownedRelatedElement"]["name"] == "UsageElement":
                self.children.append(UsageElement(definition["ownedRelatedElement"]))
            else:
                raise AttributeError("This does not seem to be valid.")

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())

        if self.prefix is not None:
            return " ".join(filter(None, (self.prefix.dump(), "".join(output))))
        else:
            return "".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "prefix": None,
            "ownedRelationship": [],
        }
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        for child in self.children:
            output["ownedRelatedElement"] = child.get_definition()

        return output


class MemberPrefix:
    def __init__(self, definition):
        if valid_definition(definition, "MemberPrefix"):
            self.visibility = VisibilityIndicator(definition["visibility"])

    def dump(self):
        return self.visibility.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["visibility"] = self.visibility.get_definition()
        return output


class Package:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                # Elements inside of a package
                # ownedRelationship += PrefixMetadataMember
                # declaration = PackageDeclaration
                # body = PackageBody
                self.relationships = []
                for rel in definition["ownedRelationship"]:
                    self.relationships.append(json.dumps(rel))
                self.declaration = PackageDeclaration(definition["declaration"])
                self.body = PackageBody(definition["body"])
        else:
            self.relationships = []
            self.declaration = PackageDeclaration()
            self.body = PackageBody()

    def dump(self):
        return "".join([self.declaration.dump(), self.body.dump()])

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelationship": []}
        for rel in self.relationships:
            output["ownedRelationship"] = rel.get_definition()
        output["declaration"] = self.declaration.get_definition()
        output["body"] = self.body.get_definition()

        return output


class Identification:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "Identification"):
                if definition["declaredShortName"] == None:
                    self.declaredShortName = None
                else:
                    if definition["declaredShortName"][0] == "<":
                        definition["declaredShortName"] = definition[
                            "declaredShortName"
                        ][1:]
                    if definition["declaredShortName"][-1] == ">":
                        definition["declaredShortName"] = definition[
                            "declaredShortName"
                        ][:-1]
                    self.declaredShortName = "<" + definition["declaredShortName"] + ">"
                self.declaredName = definition["declaredName"]
        else:
            self.declaredName = None
            self.declaredShortName = None

    def dump(self):
        return " ".join(filter(None, (self.declaredShortName, self.declaredName)))

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["declaredShortName"] = self.declaredShortName
        output["declaredName"] = self.declaredName
        return output


class PackageDeclaration:
    def __init__(self, definition=None):
        if definition is not None:
            if valid_definition(definition, "PackageDeclaration"):
                self.identification = Identification(definition["identification"])
        else:
            self.identification = Identification()

    def dump(self):
        return "package " + self.identification.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "identification": self.identification.get_definition(),
        }


class PackageBody:
    def __init__(self, definition=None):
        self.children = []
        if definition is not None:
            if valid_definition(definition, "PackageBody"):
                if "ownedRelationship" in definition:
                    for relationship in definition["ownedRelationship"]:
                        if "name" in relationship:
                            if relationship["name"] == "PackageMember":
                                self.children.append(PackageMember(relationship))
                            elif relationship["name"] == "ElementFilterMember":
                                raise NotImplementedError
                            elif relationship["name"] == "AliasMember":
                                self.children.append(AliasMember(relationship))
                            elif relationship["name"] == "Import":
                                self.children.append(Import(relationship))
                            else:
                                raise AttributeError(
                                    "Failed to match this relationship"
                                )
                        else:
                            raise NotImplementedError
                else:
                    raise NotImplementedError
            # else: handled inside function
        # else: no new definitions needed

    def dump(self):
        #!TODO This won't work
        if len(self.children) == 0:
            return ";"
        else:
            output = []
            for child in self.children:
                output.append(child.dump())
            return " { \n" + "\n".join(output) + "\n}"

    def get_definition(self):
        output = {"name": self.__class__.__name__, "ownedRelationship": []}
        for child in self.children:
            output["ownedRelationship"].append(child.get_definition())
        return output


class AliasMember:
    def __init__(self, definition):
        if valid_definition(definition, "AliasMember"):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            else:
                self.prefix = None

            self.body = RelationshipBody(definition["body"])

            self.memberShortName = definition["memberShortName"]
            self.memberName = definition["memberName"]
            self.memberElement = QualifiedName(definition["memberElement"])

    def dump(self):
        if self.memberShortName is None:
            shortName = ""
        else:
            shortName = "<" + self.memberShortName + "> "

        if self.prefix is None:
            prefix = ""
        else:
            prefix = self.prefix.dump() + " "

        return (
            prefix
            + "alias "
            + shortName
            + self.memberName
            + " for "
            + self.memberElement.dump()
            + self.body.dump()
        )


class RelationshipBody:
    def __init__(self, definition):
        self.children = []
        for relationship in definition["ownedRelationship"]:
            if relationship["name"] == "OwnedAnnotation":
                self.children.append(OwnedAnnotation(relationship))
            else:
                raise NotImplementedError

    def dump(self):
        if len(self.children) == 0:
            return ";"
        else:
            return "{" + "\n".join([child.dump() for child in self.children]) + "}"


class OwnedAnnotation:
    def __init__(self, definition):
        if valid_definition(definition, "OwnedAnnotation"):
            self.children = []
            for element in definition["ownedRelatedElement"]:
                self.children.append(AnnotatingElement(element))

    def dump(self):
        return "\n".join([child.dump() for child in self.children])


class Import:
    def __init__(self, definition):
        if valid_definition(definition, "Import"):
            self.body = RelationshipBody(definition["body"])
            self.children = []
            relationship = definition["ownedRelationship"]
            if relationship["name"] == "NamespaceImport":
                self.children.append(NamespaceImport(relationship))
            elif relationship["name"] == "MembershipImport":
                self.children.append(MembershipImport(relationship))
            else:
                raise AttributeError("This does not seem to be valid")

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        return "".join(output) + self.body.dump()


class MembershipImport:
    def __init__(self, definition):
        if valid_definition(definition, "MembershipImport"):
            self.prefix = ImportPrefix(definition["prefix"])
            self.membership = ImportedMembership(definition["membership"])

    def dump(self):
        return " ".join([self.prefix.dump(), self.membership.dump()])


class ImportedMembership:
    def __init__(self, definition):
        if valid_definition(definition, "ImportedMembership"):
            self.name = QualifiedName(definition["importedMembership"])
            self.isRecursive = definition["isRecursive"]

    def dump(self):
        if not self.isRecursive:
            return self.name.dump()
        else:
            return self.name.dump() + "::**"


class NamespaceImport:
    def __init__(self, definition):
        if valid_definition(definition, "NamespaceImport"):
            self.prefix = ImportPrefix(definition["prefix"])

            if len(definition["ownedRelatedElement"]) > 0:
                raise NotImplementedError
            else:
                self.children = []

            self.namespace = ImportedNamespace(definition["namespace"])

    def dump(self):
        return self.prefix.dump() + self.namespace.dump()


class ImportPrefix:
    def __init__(self, definition):
        if valid_definition(definition, "ImportPrefix"):
            if definition["visibility"] is not None:
                self.visibility = VisibilityIndicator(definition["visibility"])
            else:
                self.visibility = None

            if definition["isImportAll"]:
                self.keyword = "import all "
            else:
                self.keyword = "import "

    def dump(self):
        if self.visibility is None:
            return self.keyword
        else:
            return self.visibility.dump() + self.keyword


class ImportedNamespace:
    # The grammar for this file is currently broken.
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.namespaces = QualifiedName(definition["namespace"])

    def dump(self):
        return self.namespaces.dump() + "::*"


class QualifiedName:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.names = [definition["name1"]]
            for name in definition["names"]:
                self.names.append(name)

    def dump(self):
        return "::".join(self.names)

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["name1"] = self.names[0]
        output["names"] = self.names[1:]
        return output


class VisibilityIndicator:
    def __init__(self, definition):
        if valid_definition(definition, "VisibilityIndicator"):
            if (
                definition["private"] == "private"
                and definition["protected"] == ""
                and definition["public"] == ""
            ):
                self.keyword = "private "
            elif (
                definition["private"] == ""
                and definition["protected"] == "protected"
                and definition["public"] == ""
            ):
                self.keyword = "protected "
            elif (
                definition["private"] == ""
                and definition["protected"] == ""
                and definition["public"] == "public"
            ):
                self.keyword = "public "
            else:
                self.keyword = ""

    def dump(self):
        return self.keyword
