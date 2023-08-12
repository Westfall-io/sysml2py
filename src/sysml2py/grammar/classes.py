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
                print(definition["name"])  # pragma: no cover
                raise ValueError(
                    "The name of the element did not match."
                )  # pragma: no cover

        else:
            raise AttributeError("This does not seem to be valid.")  # pragma: no cover
    else:  # pragma: no cover
        print("------------")
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
        # print("\n\n\n\n-----\n{}|\n".format(line))
        if len(line) > 0:
            if line[-1] == "{":
                # Last character is new bracket
                level += 1

    return "\n".join(ns)


class RootNamespace:
    def __init__(self, definition):
        self.children = []
        try:
            if valid_definition(definition, "PackageBodyElement"):
                # This is a SysML Element
                self.load_package_body(definition["ownedRelationship"])
        except ValueError:
            try:
                if valid_definition(definition, "NamespaceBodyElement"):
                    # This is a KerML Element
                    pass
            except ValueError:  # pragma: no cover
                print(definition)
                raise ValueError("Not expecting any other root node names.")

    def load_package_body(self, definition):
        for member in definition:
            if isinstance(member, dict):
                # Options here are PackageMember, ElementFilterMember, AliasMember, Import
                if member["name"] == "PackageMember":
                    memberclass = PackageMember(member)
                elif member["name"] == "ElementFilterMember":
                    raise NotImplementedError  # pragma: no cover
                elif member["name"] == "AliasMember":
                    raise NotImplementedError  # pragma: no cover
                elif member["name"] == "Import":
                    raise NotImplementedError  # pragma: no cover
                else:
                    print(member["name"])  # pragma: no cover
                    raise AttributeError("Error")  # pragma: no cover

                self.children.append(memberclass)
            else:
                print(member)  # pragma: no cover
                raise TypeError(
                    "Invalid definition, member was not type dict"
                )  # pragma: no cover

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
                print(definition["ownedRelatedElement"])  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

            de = definition["ownedRelatedElement"]["name"]
            if de == "Package":
                self.children.append(Package(definition["ownedRelatedElement"]))
            elif de == "PartDefinition":
                self.children.append(PartDefinition(definition["ownedRelatedElement"]))
            elif de == "AttributeDefinition":
                self.children.append(
                    AttributeDefinition(definition["ownedRelatedElement"])
                )
            elif de == "AnnotatingElement":
                self.children.append(
                    AnnotatingElement(definition["ownedRelatedElement"])
                )

            elif de == "EnumerationDefinition":
                self.children.append(
                    EnumerationDefinition(definition["ownedRelatedElement"])
                )
            elif de == "ItemDefinition":
                self.children.append(ItemDefinition(definition["ownedRelatedElement"]))
            elif de == "ConnectionDefinition":
                self.children.append(
                    ConnectionDefinition(definition["ownedRelatedElement"])
                )
            elif de == "PortDefinition":
                self.children.append(PortDefinition(definition["ownedRelatedElement"]))
            elif de == "InterfaceDefinition":
                self.children.append(
                    InterfaceDefinition(definition["ownedRelatedElement"])
                )
            elif de == "FlowConnectionDefinition":
                self.children.append(
                    FlowConnectionDefinition(definition["ownedRelatedElement"])
                )
            elif de == "ActionDefinition":
                self.children.append(
                    ActionDefinition(definition["ownedRelatedElement"])
                )
            elif de == "CalculationDefinition":
                self.children.append(
                    CalculationDefinition(definition["ownedRelatedElement"])
                )
            elif de == "StateDefinition":
                self.children.append(StateDefinition(definition["ownedRelatedElement"]))
            elif de == "ConstraintDefinition":
                self.children.append(
                    ConstraintDefinition(definition["ownedRelatedElement"])
                )
            elif de == "RequirementDefinition":
                self.children.append(
                    RequirementDefinition(definition["ownedRelatedElement"])
                )
            elif de == "AnalysisCaseDefinition":
                self.children.append(
                    AnalysisCaseDefinition(definition["ownedRelatedElement"])
                )
            else:
                print(de)  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

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


class AnalysisCaseDefinition:
    # AnalysisCaseDefinition :
    # 	prefix=OccurrenceDefinitionPrefix AnalysisCaseDefKeyword
    #   declaration=DefinitionDeclaration body=CaseBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "analysis def"
        self.declaration = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])
            if definition["declaration"] is not None:
                self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = CaseBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        if self.declaration is not None:
            output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class CaseBody:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.items = []
            for item in definition["item"]:
                self.items.append(CaseBodyItem(item))

            if definition["ownedRelationship"] is not None:
                self.child = ResultExpressionMember(definition["ownedRelationship"])
            else:
                self.child = None

    def dump(self):
        if len(self.items) == 0:
            return ";"
        else:
            if self.child is not None:
                output = [self.child.dump()]
            else:
                output = [None]
            return (
                "{\n"
                + "\n".join(
                    filter(None, [child.dump() for child in self.items] + output)
                )
                + "\n}"
            )


class CaseBodyItem:
    #  CaseBodyItem :
    # 	  ownedRelationship = CalculationBodyItem
    # 	| ownedRelationship = SubjectMember
    # 	| ownedRelationship = ActorMember
    # 	| ownedRelationship = ObjectiveMember
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            child = definition["ownedRelationship"]
            name = child["name"]
            if name == "CalculationBodyItem":
                self.child = CalculationBodyItem(child)
            elif name == "SubjectMember":
                self.child = SubjectMember(child)
            elif name == "ActorMember":
                self.child = ActorMember(child)
            elif name == "ObjectiveMember":
                self.child = ObjectiveMember(child)
            else:  # pragma: no cover
                raise ValueError("Invalid child name")

    def dump(self):
        return self.child.dump()


class ObjectiveMember:
    # ObjectiveMember :
    # 	prefix=MemberPrefix 'objective' ownedRelatedElement=ObjectiveRequirementUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "objective"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.child = ObjectiveRequirementUsage(definition["ownedRelatedElement"])

    def dump(self):
        if self.prefix is None:
            return " ".join([self.keyword, self.child.dump()])
        else:
            return " ".join([self.prefix.dump(), self.keyword, self.child.dump()])


class ObjectiveRequirementUsage:
    # ObjectiveRequirementUsage :
    # 	keyword+=UsageExtensionKeyword* declaration=CalculationUsageDeclaration body=RequirementBody
    # ;
    def __init__(self, definition):
        self.keyword = []
        if valid_definition(definition, self.__class__.__name__):
            for keyword in definition["keyword"]:
                self.keyword.append(UsageExtensionKeyword(keyword))
            self.declaration = CalculationUsageDeclaration(definition["declaration"])
            self.body = RequirementBody(definition["body"])

    def dump(self):
        output = []
        for keyword in self.keyword:
            output.append(keyword.dump())
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class RequirementDefinition:
    # RequirementDefinition :
    # 	prefix=OccurrenceDefinitionPrefix RequirementDefKeyword
    #   declaration=DefinitionDeclaration body=RequirementBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "requirement def"
        self.declaration = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])
            if definition["declaration"] is not None:
                self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = RequirementBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        if self.declaration is not None:
            output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class RequirementBody:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.items = []
            for item in definition["item"]:
                self.items.append(RequirementBodyItem(item))

    def dump(self):
        if len(self.items) == 0:
            return ";"
        else:
            return "{\n" + "\n".join([child.dump() for child in self.items]) + "\n}"


class RequirementBodyItem:
    # RequirementBodyItem :
    # 	  ownedRelationship = DefinitionBodyItem
    # 	| ownedRelationship = SubjectMember
    # 	| ownedRelationship = RequirementConstraintMember
    # 	| ownedRelationship = FramedConcernMember
    # 	| ownedRelationship = RequirementVerificationMember
    # 	| ownedRelationship = ActorMember
    # 	| ownedRelationship = StakeholderMember
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            child = definition["ownedRelationship"]
            name = child["name"]
            if name == "DefinitionBodyItem":
                self.child = DefinitionBodyItem(child)
            elif name == "SubjectMember":
                self.child = SubjectMember(child)
            elif name == "RequirementConstraintMember":
                self.child = RequirementConstraintMember(child)
            elif name == "FramedConcernMember":
                self.child = FramedConcernMember(child)
            elif name == "RequirementVerificationMember":
                self.child = RequirementVerificationMember(child)
            elif name == "ActorMember":
                self.child = ActorMember(child)
            elif name == "StakeholderMember":
                self.child = StakeholderMember(child)
            else:  # pragma: no cover
                raise ValueError("Invalid child name")

    def dump(self):
        return self.child.dump()


class SubjectMember:
    # SubjectMember :
    # 	prefix=MemberPrefix ownedRelatedElement = SubjectUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.child = SubjectUsage(definition["ownedRelatedElement"])

    def dump(self):
        if self.prefix is None:
            return self.child.dump()
        else:
            return " ".join([self.prefix.dump(), self.child.dump()])


class SubjectUsage:
    # SubjectUsage :
    # 	'subject' keyword+=UsageExtensionKeyword* usage=Usage
    # ;
    def __init__(self, definition):
        self.subject = "subject"
        self.keyword = []
        if valid_definition(definition, self.__class__.__name__):
            for keyword in definition["keyword"]:
                self.keyword.append(UsageExtensionKeyword(keyword))
            self.child = Usage(definition["usage"])

    def dump(self):
        return " ".join(
            [self.subject] + [x.dump() for x in self.keyword] + [self.child.dump()]
        )


class RequirementConstraintMember:
    # RequirementConstraintMember :
    # 	prefix=MemberPrefix kind = RequirementConstraintKind
    # 	ownedRelatedElement = RequirementConstraintUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.kind = RequirementConstraintKind(definition["kind"])
            self.child = RequirementConstraintUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.kind.dump())
        output.append(self.child.dump())
        return " ".join(output)


class RequirementConstraintKind:
    #  RequirementConstraintKind :
    # 	assumption = 'assume' | requirement = 'require'
    # ;
    def __init__(self, definition):
        self.requirement = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["assumption"] == "assume" and definition["requirement"] == "":
                self.requirement = False
            elif (
                definition["assumption"] == ""
                and definition["requirement"] == "require"
            ):
                self.requirement = True
            else:  # pragma: no cover
                print(
                    definition["assumption"] == ""
                    and definition["requirement"] == "require"
                )
                raise ValueError

    def dump(self):
        if self.requirement is not None:
            if self.requirement:
                return "require"
            else:
                return "assume"
        else:  # pragma: no cover
            raise ValueError


class RequirementConstraintUsage:
    # RequirementConstraintUsage :
    #     (
    #       ownedRelationship = OwnedReferenceSubsetting fs+=FeatureSpecialization*
    #       body=RequirementBody
    #     )
    #     |
    #     (
    #       (
    #         keyword+=UsageExtensionKeyword* ConstraintUsageKeyword
    #         |
    #         keyword+=UsageExtensionKeyword+
    #       )
    #       declaration=CalculationUsageDeclaration body=CalculationBody
    #     )
    # ;
    def __init__(self, definition):
        self.reference = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelationship"] is not None:
                # Type 1
                self.reference = OwnedReferenceSubsetting(
                    definition["ownedRelationship"]
                )
                self.fs = []
                for child in definition["fs"]:
                    self.fs.append(FeatureSpecialization(child))
                self.body = RequirementBody(definition["body"])

            else:
                self.keyword = []
                self.declaration = None
                if len(definition["keyword2"]) == 0:
                    for keyword in definition["keyword1"]:
                        self.keyword.append(UsageExtensionKeyword(keyword))
                    self.constraint = "constraint"
                else:
                    for keyword in definition["keyword2"]:
                        self.keyword.append(UsageExtensionKeyword(keyword))
                    self.constraint = None
                if definition["declaration"] is not None:
                    self.declaration = CalculationUsageDeclaration(
                        definition["declaration"]
                    )
                self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.reference is not None:
            output.append(self.reference.dump())
            for fs in self.fs:
                output.append(fs.dump())
            output.append(self.body.dump())
        else:
            for keyword in self.keyword:
                output.append(keyword.dump())
            output.append(self.constraint)
            if self.declaration is not None:
                output.append(self.declaration.dump())
            output.append(self.body.dump())
        return " ".join(filter(None, output))


class ConstraintDefinition:
    # ConstraintDefinition :
    # 	prefix=OccurrenceDefinitionPrefix ConstraintDefKeyword declaration=DefinitionDeclaration body=CalculationBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "constraint def"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])
            self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class StateDefinition:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "state def"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])

            self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = StateDefBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class StateDefBody:
    #     StateDefBody :
    # 	';' | ( isParallel ?= 'parallel' )? '{' part=StateBodyPart '}'
    # ;
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["part"] is not None:
                self.children = StateBodyPart(definition["part"])
                self.isParallel = definition["isParallel"]

    def dump(self):
        if self.children is None:
            return ";"
        else:
            output = []
            if self.isParallel is not None:
                if self.isParallel:
                    output.append("parallel")

            output.append("{\n")
            output.append(self.children.dump())
            output.append("\n}")
            return " ".join(output)


class StateBodyPart:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["item"]:
                self.children.append(StateBodyItem(child))

    def dump(self):
        return "\n".join([x.dump() for x in self.children])


class StateBodyItem:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                self.children.append(globals()[child["name"]](child))

    def dump(self):
        return "\n".join([x.dump() for x in self.children])


class StateUsage:
    # prefix=OccurrenceUsagePrefix StateUsageKeyword
    # declaration=ActionUsageDeclaration body=StateUsageBody
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "state"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = ActionUsageDeclaration(definition["declaration"])
            self.body = StateUsageBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class StateUsageBody:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = StateDefBody(definition["body"])

    def dump(self):
        return self.children.dump()


class DoActionMember:
    # DoActionMember :
    # 	prefix=MemberPrefix DoActionKind ownedRelatedElement=StateActionUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "do"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            self.children = StateActionUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.children.dump())
        return " ".join(output)


class ExitActionMember:
    # ExitActionMember :
    # 	prefix=MemberPrefix DoActionKind ownedRelatedElement=StateActionUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "exit"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            self.children = StateActionUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.children.dump())
        return " ".join(output)


class EntryActionMember:
    # EntryActionMember :
    # 	prefix=MemberPrefix EntryActionKind ownedRelatedElement=StateActionUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "entry"
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            self.children = StateActionUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        output.append(self.children.dump())
        return " ".join(output)


class StateActionUsage:
    # StateActionUsage :
    # 	';' | pau=PerformedActionUsage body=ActionBody
    # ;
    def __init__(self, definition):
        self.body = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["body"] is not None:
                self.body = ActionBody(definition["body"])

            if definition["pau"] is not None:
                self.pau = PerformedActionUsage(definition["pau"])

    def dump(self):
        if self.body is None:
            return ";"
        else:
            return "".join([self.pau.dump(), self.body.dump()])


class AssignmentNode:
    # AssignmentNode :
    # 	prefix=OccurrenceUsagePrefix declaration=AssignmentNodeDeclaration body=ActionBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = AssignmentNodeDeclaration(definition["declaration"])
            self.body = ActionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return "".join(output)


class AssignmentNodeDeclaration:
    #  AssignmentNodeDeclaration :
    # 	declaration=ActionNodeUsageDeclaration? 'assign'
    # 	ownedRelationship1 = FeatureChainMember ':='
    # 	ownedRelationship2 = NodeParameterMember
    # ;
    def __init__(self, definition):
        self.declaration = None
        self.keyword = "assign"
        self.keyword2 = ":="
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = ActionNodeUsageDeclaration(definition["declaration"])
            self.fcm = FeatureChainMember(definition["ownedRelationship1"])
            self.npm = NodeParameterMember(definition["ownedRelationship2"])

    def dump(self):
        output = []
        if self.declaration is not None:
            output.append(self.declaration.dump())
        output.append(self.keyword)
        output.append(self.fcm.dump())
        output.append(self.keyword2)
        output.append(self.npm.dump())
        return " ".join(output)


class ActionNodeUsageDeclaration:
    #  ActionNodeUsageDeclaration :
    # 	ActionUsageKeyword declaration=UsageDeclaration?
    # ;
    def __init__(self, definition):
        self.declaration = None
        self.keyword = "action"
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

    def dump(self):
        if self.declaration is not None:
            return " ".join([self.keyword, self.declaration.dump()])
        else:
            return self.keyword


class NodeParameterMember:
    # NodeParameterMember :
    # 	ownedRelatedElement = NodeParameter
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = NodeParameter(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class NodeParameter:
    # NodeParameter :
    # 	 ownedRelationship = FeatureBinding
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = FeatureBinding(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class FeatureBinding:
    # FeatureBinding :
    # 	ownedRelatedElement = OwnedExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class PerformedActionUsage:
    # PerformedActionUsage :
    # 	   declaration=PerformActionUsageDeclaration
    # 	|  declaration=AcceptNodeDeclaration
    # 	|  declaration=SendNodeDeclaration
    # 	|  declaration=AssignmentNodeDeclaration
    # ;
    def __init__(self, definition):
        self.declaration = None
        if valid_definition(definition, self.__class__.__name__):
            self.declaration = globals()[definition["declaration"]["name"]](
                definition["declaration"]
            )

    def dump(self):
        return self.declaration.dump()


class PerformActionUsageDeclaration:
    # PerformActionUsageDeclaration :
    #    	( ownedRelationship = OwnedReferenceSubsetting fspart=FeatureSpecializationPart?
    #    	| ActionUsageKeyword declaration=UsageDeclaration? )
    #     valuepart=ValuePart?
    # ;
    def __init__(self, definition):
        self.valuepart = None
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelationship"] is not None:
                self.children.append(
                    OwnedReferenceSubsetting(definition["ownedRelationship"])
                )
                if definition["fspart"] is not None:
                    self.children.append(
                        FeatureSpecializationPart(definition["fspart"])
                    )
            else:
                if definition["declaration"] is not None:
                    self.children.append(UsageDeclaration(definition["declaration"]))

            if definition["valuepart"] is not None:
                self.valuepart = ValuePart(definition["valuepart"])

    def dump(self):
        if self.valuepart is not None:
            vpdump = " " + self.valuepart.dump()
        else:
            vpdump = ""

        if len(self.children) == 0:
            return "action" + vpdump
        else:
            if self.children[0].__class__.__name__ == "UsageDeclaration":
                return "action " + self.children[0].dump() + vpdump
            else:
                return " ".join([x.dump() for x in self.children]) + vpdump


class EntryTransitionMember:
    # EntryTransitionMember :
    # 	prefix=MemberPrefix
    # 	( ownedRelatedElement=GuardedTargetSuccession
    # 	| 'then' ownedRelatedElement=TransitionSuccession
    # 	) ';'
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.body = ";"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            if definition["ownedRelatedElement"]["name"] == "GuardedTargetSuccession":
                self.children = GuardedTargetSuccession(
                    definition["ownedRelatedElement"]
                )
            else:
                self.children = TransitionSuccession(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        if self.children.__class__.__name__ == "TransitionSuccession":
            output.append("then")
        output.append(self.children.dump())
        output.append(self.body)
        return " ".join(output)


class GuardedTargetSuccession:
    # GuardedTargetSuccession :
    # 	ownedRelationship += GuardExpressionMember
    # 	'then' ownedRelationship += TransitionSuccessionMember
    # ;
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                if child["name"] == "GuardExpressionMember":
                    self.children.append(GuardExpressionMember(child))
                else:
                    self.children.append(TransitionSuccessionMember(child))

    def dump(self):
        return " then ".join([x.dump() for x in self.children])


class GuardExpressionMember:
    # GuardExpressionMember :
    # 	GuardFeatureKind ownedRelatedElement=OwnedExpression
    # ;
    def __init__(self, definition):
        self.keyword = "if"
        if valid_definition(definition, self.__class__.__name__):
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        return " ".join([self.keyword, self.children.dump()])


class TransitionSuccessionMember:
    # TransitionSuccessionMember :
    # 	ownedRelatedElement = TransitionSuccession
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = TransitionSuccession(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class TransitionSuccession:
    # TransitionSuccession :
    # 	ownedRelationship = ConnectorEndMember
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = ConnectorEndMember(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class TransitionUsageMember:
    # TransitionUsageMember :
    # 	prefix=MemberPrefix ownedRelatedElement=TransitionUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])

            self.children = TransitionUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.children.dump())
        return " ".join(output)


class TargetTransitionUsageMember:
    # This is a special class version of the previous, but it assumes the
    # previous node as a target
    # TargetTransitionUsageMember :
    # 	prefix=MemberPrefix ownedRelatedElement = TargetTransitionUsage
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.children = TargetTransitionUsage(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.children.dump())
        return " ".join(output)


class TargetTransitionUsage:
    # TargetTransitionUsage :
    # 	TransitionUsageKeyword?
    # 	(
    #     (ownedRelationship1 = TriggerActionMember)
    # 	  (ownedRelationship2 = GuardExpressionMember)?
    # 	  (ownedRelationship3 = EffectBehaviorMember)?
    #   ) | (
    #     (ownedRelationship2 = GuardExpressionMember)
    #     (ownedRelationship3 = EffectBehaviorMember)?
    #   ) | (
    #     (ownedRelationship3 = EffectBehaviorMember)
    #   )
    # 	'then' ownedRelationship4 = TransitionSuccessionMember
    # 	body=ActionBody
    # ;
    # Here transition is optional
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            child = definition["ownedRelationship1"]
            if child is not None:
                self.children.append(TriggerActionMember(child))

            child = definition["ownedRelationship2"]
            if child is not None:
                self.children.append(GuardExpressionMember(child))
            child = definition["ownedRelationship3"]
            if child is not None:
                self.children.append(EffectBehaviorMember(child))
            child = definition["ownedRelationship4"]
            if child is not None:
                self.children.append(TransitionSuccessionMember(child))

            self.body = ActionBody(definition["body"])

    def dump(self):
        output = []
        # Skip the transition keyword here.
        for child in self.children:
            if child.__class__.__name__ == "TransitionSuccessionMember":
                output.append("\n   then")
            output.append(child.dump())
        output.append(self.body.dump())
        return " ".join(output)


class TransitionUsage:
    # TransitionUsage :
    # 	TransitionUsageKeyword ( declaration=UsageDeclaration? 'first' )?
    # 	ownedRelationship += TransitionSourceMember
    # 	( ownedRelationship += TriggerActionMember )?
    # 	( ownedRelationship += GuardExpressionMember )?
    # 	( ownedRelationship += EffectBehaviorMember )?
    # 	'then' ownedRelationship += TransitionSuccessionMember
    # 	body=ActionBody
    # ;
    def __init__(self, definition):
        self.keyword = "transition"
        self.declaration = None
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

            self.body = ActionBody(definition["body"])

            for child in definition["ownedRelationship"]:
                if child["name"] == "TransitionSourceMember":
                    self.children.append(TransitionSourceMember(child))
                elif child["name"] == "TriggerActionMember":
                    self.children.append(TriggerActionMember(child))
                elif child["name"] == "GuardExpressionMember":
                    self.children.append(GuardExpressionMember(child))
                elif child["name"] == "EffectBehaviorMember":
                    self.children.append(EffectBehaviorMember(child))
                else:
                    self.children.append(TransitionSuccessionMember(child))

    def dump(self):
        output = [self.keyword]
        if self.declaration is not None:
            output.append(self.declaration.dump())
            output.append("\n   first")

        for child in self.children:
            if child.__class__.__name__ == "TransitionSuccessionMember":
                output.append("\n   then")
            output.append(child.dump())

        output.append(self.body.dump())
        return " ".join(output)


class EffectBehaviorMember:
    # EffectBehaviorMember :
    # 	EffectFeatureKind ownedRelatedElement=EffectBehaviorUsage
    # ;
    def __init__(self, definition):
        self.keyword = "do"
        if valid_definition(definition, self.__class__.__name__):
            self.children = EffectBehaviorUsage(definition["ownedRelatedElement"])

    def dump(self):
        return " ".join([self.keyword, self.children.dump()])


class EffectBehaviorUsage:
    # EffectBehaviorUsage :
    # 	  usage=PerformedActionUsage ( '{' item+=ActionBodyItem* '}' )?
    # ;
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            self.usage = PerformedActionUsage(definition["usage"])
            for item in definition["item"]:
                self.children.append(ActionBodyItem(item))

    def dump(self):
        output = [self.usage.dump()]
        if len(self.children) > 0:
            output.append("{\n")
            for child in self.children:
                output.append(child.dump())
            output.append("\n}")
        return " ".join(output)


class TransitionSourceMember:
    # TransitionSourceMember :
    # 	  ownedRelatedElement += OwnedFeatureChain
    # 	| memberElement = QualifiedName
    # ;
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["memberElement"] is not None:
                self.children.append(QualifiedName(definition["memberElement"]))
            else:
                for child in definition["ownedRelatedElement"]:
                    self.children.append(OwnedFeatureChain(child))

    def dump(self):
        return "".join([x.dump() for x in self.children])


class TriggerActionMember:
    # TriggerActionMember :
    # 	TriggerFeatureKind ownedRelatedElement=TriggerAction
    # ;
    def __init__(self, definition):
        self.keyword = "accept"
        if valid_definition(definition, self.__class__.__name__):
            self.children = TriggerAction(definition["ownedRelatedElement"])

    def dump(self):
        return " ".join([self.keyword, self.children.dump()])


class TriggerAction:
    # TriggerAction :
    # 	part=AcceptParameterPart
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = AcceptParameterPart(definition["part"])

    def dump(self):
        return self.children.dump()


class AcceptParameterPart:
    # AcceptParameterPart :
    # 	ownedRelationship += PayloadParameterMember 'via'
    #   ownedRelationship += NodeParameterMember
    # ;
    def __init__(self, definition):
        self.keyword = "via"
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                if child["name"] == "PayloadParameterMember":
                    self.children.append(PayloadParameterMember(child))
                else:
                    self.children.append(NodeParameterMember(child))

    def dump(self):
        return (" " + self.keyword + " ").join([x.dump() for x in self.children])


class PayloadParameterMember:
    # PayloadParameterMember :
    # 	ownedRelatedElement = PayloadParameter
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = PayloadParameter(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class PayloadParameter:
    # PayloadParameter :
    # 	  feature=PayloadFeature
    # 	| identification=Identification? pfsp=PayloadFeatureSpecializationPart? tvp=TriggerValuePart
    # ;
    def __init__(self, definition):
        self.identification = None
        self.pfsp = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["feature"] is not None:
                self.children = PayloadFeature(definition["feature"])
            else:
                if definition["identification"] is not None:
                    self.identification = Identification(definition["identification"])

                if definition["pfsp"] is not None:
                    self.pfsp = PayloadFeatureSpecializationPart(definition["pfsp"])

                self.children = TriggerValuePart(definition["tvp"])

    def dump(self):
        output = []
        if self.identification is not None:
            output.append(self.identification.dump())
        if self.pfsp is not None:
            output.append(self.pfsp.dump())

        output.append(self.children.dump())
        return " ".join(output)


class TriggerValuePart:
    # TriggerValuePart :
    # 	ownedRelationship = TriggerFeatureValue
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = TriggerFeatureValue(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class TriggerFeatureValue:
    # TriggerFeatureValue :
    # 	ownedRelatedElement = TriggerExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = TriggerExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class TriggerExpression:
    # TriggerExpression :
    # 	  kind = TimeTriggerKind
    # 	  ownedRelationship = OwnedExpressionMember
    # 	| ChangeTriggerKind
    # 	  ownedRelationship = ChangeExpressionMember
    # ;
    def __init__(self, definition):
        self.kind = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelationship"]["name"] == "OwnedExpressionMember":
                self.kind = TimeTriggerKind(definition["kind"])
                self.children = OwnedExpressionMember(definition["ownedRelationship"])
            else:
                self.kind = "when"
                self.children = ChangeExpressionMember(definition["ownedRelationship"])

    def dump(self):
        if isinstance(self.kind, str):
            kind = self.kind
        else:
            kind = self.kind.dump()

        return " ".join([kind, self.children.dump()])


class TimeTriggerKind:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.isAt = definition["isAt"]
            self.isAfter = definition["isAfter"]

    def dump(self):
        if self.isAt:
            return "at"
        else:
            return "after"


class OwnedExpressionMember:
    # OwnedExpressionMember :
    # 	ownedRelatedElement = OwnedExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class ChangeExpressionMember:
    # ChangeExpressionMember :
    # 	ownedRelatedElement = ChangeExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = ChangeExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class ChangeExpression:
    # ChangeExpression :
    # 	ownedRelationship = ChangeResultExpressionMember
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = ChangeResultExpressionMember(
                definition["ownedRelationship"]
            )

    def dump(self):
        return self.children.dump()


class ChangeResultExpressionMember:
    # ChangeResultExpressionMember :
    # 	ownedRelatedElement = OwnedExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class CalculationDefinition:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "calc def"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceDefinitionPrefix(definition["prefix"])

            self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class ActionDefinition:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "action def"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                raise NotImplementedError  # pragma: no cover

            self.declaration = DefinitionDeclaration(definition["declaration"])
            self.body = ActionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class ActionBody:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for item in definition["items"]:
                self.children.append(ActionBodyItem(item))

    def dump(self):
        if len(self.children) == 0:
            return ";"
        else:
            return " {\n" + "\n".join([x.dump() for x in self.children]) + "\n}"


class ActionBodyItem:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if isinstance(definition["ownedRelationship"], list):
                for child in definition["ownedRelationship"]:
                    self.children.append(globals()[child["name"]](child))
            else:
                self.children.append(
                    globals()[definition["ownedRelationship"]["name"]](
                        definition["ownedRelationship"]
                    )
                )

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
            if child.__class__.__name__ != "EmptySuccessionMember":
                # Add a new line
                output.append("\n")
            else:
                # Otherwise add a space
                output.append(" ")

        if output[-1] == "\n":
            # Remove a extra new line
            output = output[:-1]
        return "".join(output)


class ActionBodyItemTarget:
    # ActionBodyItemTarget :
    #     ( member=BehaviorUsageMember | member=ActionNodeMember )
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["member"]["name"] == "BehaviorUsageMember":
                self.children = BehaviorUsageMember(definition["member"])
            else:
                self.children = ActionNodeMember(definition["member"])

    def dump(self):
        return self.children.dump()


class ActionNodeMember:
    # ActionNodeMember :
    # 	prefix=MemberPrefix ownedRelatedElement = ActionNode
    # ;
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.children = ActionNode(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.children.dump())
        return " ".join(output)


class ActionNode:
    # ActionNode :
    # 	  node=SendNode
    #   | node=AcceptNode
    #   | node=AssignmentNode
    # 	| node=IfNode
    #   | node=WhileLoopNode
    #   | node=ForLoopNode
    # 	| node=ControlNode
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = globals()[definition["node"]["name"]](definition["node"])

    def dump(self):
        return self.children.dump()


class EmptySuccessionMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = EmptySuccession(definition["ownedRelatedElement"][0])

    def dump(self):
        return self.children.dump()


class EmptySuccession:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if len(definition["ownedRelationship"]) > 0:
                self.children = MultiplicitySourceEndMember(
                    definition["ownedRelationship"]
                )

    def dump(self):
        output = ["then"]
        for child in self.children:
            output.append(child.dump())
        return " ".join(output)


class MultiplicitySourceEndMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = MultiplicitySourceEnd(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class MultiplicitySourceEnd:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelatedElement"]:
                self.children = OwnedMultiplicity(child)

    def dump(self):
        return " ".join([x.dump() for x in self.children])


class StructureUsageMember:
    def __init__(self, definition):
        self.prefix = None
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            for child in definition["ownedRelatedElement"]:
                self.children.append(StructureUsageElement(child))

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        o2 = []
        for child in self.children:
            o2.append(child.dump())
        output.append("\n".join(o2))
        return "".join(output)


class BehaviorUsageMember:
    def __init__(self, definition):
        self.prefix = None
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.children.append(
                BehaviorUsageElement(definition["ownedRelatedElement"])
            )

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        for child in self.children:
            output.append(child.dump())
        return " ".join(output)


class ConstraintUsage:
    # ConstraintUsage :
    # 	prefix=OccurrenceUsagePrefix ConstraintUsageKeyword declaration=CalculationUsageDeclaration body=CalculationBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.declaration = None
        self.keyword = "constraint"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            if definition["declaration"] is not None:
                self.declaration = CalculationUsageDeclaration(
                    definition["declaration"]
                )
            self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        if self.declaration is not None:
            output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class AssertConstraintUsage:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "assert"
        self.keyword_constraint = "constraint"
        self.children = []
        self.fsp = None
        self.declaration = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])

            self.isNegated = definition["isNegated"]
            if len(definition["ownedRelationship"]) > 0:
                if definition["featurespecializationpart"] is not None:
                    self.fsp = FeatureSpecializationPart(
                        definition["featurespecializationpart"]
                    )
                for child in definition["ownedRelationship"]:
                    self.children.append(OwnedReferenceSubsetting(child))
            else:
                if definition["declaration"] is not None:
                    self.declaration = UsageDeclaration(definition["declaration"])
            self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        output.append(self.keyword)
        if self.isNegated:
            output.append("not")

        if len(self.children) == 0:
            output.append(self.keyword_constraint)
            if self.declaration is not None:
                output.append(self.declaration.dump())
        else:
            for child in self.children:
                output.append(child.dump())
            if self.fsp is not None:
                output.append(self.fsp.dump())

        output.append(self.body.dump())

        return " ".join(output)


class CalculationBody:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["part"]:
                self.children.append(CalculationBodyPart(child))

    def dump(self):
        if len(self.children) == 0:
            return ";"
        else:
            return "{\n" + "\n".join([x.dump() for x in self.children]) + "\n}"


class CalculationBodyPart:
    def __init__(self, definition):
        self.children = []
        self.rem = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["item"]:
                self.children.append(CalculationBodyItem(child))
            for child in definition["ownedRelationship"]:
                self.rem.append(ResultExpressionMember(child))

    def dump(self):
        output = []
        for child in self.children:
            output.append(child.dump())
        for child in self.rem:
            output.append(child.dump())
        return "\n".join(output)


class CalculationBodyItem:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["item"] is not None:
                self.children.append(ActionBodyItem(definition["item"]))
            else:
                self.children.append(
                    ReturnParameterMember(definition["ownedRelationship"])
                )

    def dump(self):
        return "".join([x.dump() for x in self.children])


class ReturnParameterMember:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "return"
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.children.append(UsageElement(definition["ownedRelatedElement"]))

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        for child in self.children:
            output.append(child.dump())
        return " ".join(output)


class ResultExpressionMember:
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = MemberPrefix(definition["prefix"])
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.children.dump())
        return "".join(output)


class AnalysisCaseUsage:
    # AnalysisCaseUsage :
    # 	prefix=OccurrenceUsagePrefix AnalysisCaseUsageKeyword
    #   declaration=CalculationUsageDeclaration body=CaseBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "analysis"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = CalculationUsageDeclaration(definition["declaration"])
            self.body = CaseBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class BehaviorUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = globals()[definition["ownedRelationship"]["name"]](
                definition["ownedRelationship"]
            )

    def dump(self):
        return self.children.dump()


class RequirementUsage:
    # RequirementUsage :
    # 	prefix=OccurrenceUsagePrefix RequirementUsageKeyword declaration=CalculationUsageDeclaration body=RequirementBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "requirement"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = CalculationUsageDeclaration(definition["declaration"])
            self.body = RequirementBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class PerformActionUsage:
    # PerformActionUsage :
    # 	prefix=OccurrenceUsagePrefix 'perform' declaration=PerformActionUsageDeclaration body=ActionBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "perform"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = PerformActionUsageDeclaration(definition["declaration"])
            self.body = ActionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class CalculationUsage:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "calc"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.declaration = CalculationUsageDeclaration(definition["declaration"])
            self.body = CalculationBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class CalculationUsageDeclaration:
    def __init__(self, definition):
        self.declaration = None
        self.valuepart = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])
            if definition["valuepart"] is not None:
                self.valuepart = ValuePart(definition["valuepart"])

    def dump(self):
        output = []
        if self.declaration is not None:
            output.append(self.declaration.dump())
        if self.valuepart is not None:
            output.append(self.valuepart.dump())
        return "".join(output)


class ActionUsage:
    def __init__(self, definition):
        self.prefix = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            self.keyword = "action"
            self.declaration = ActionUsageDeclaration(definition["declaration"])
            self.body = ActionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class ActionUsageDeclaration:
    def __init__(self, definition):
        self.declaration = None
        self.valuepart = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

            if definition["valuepart"] is not None:
                self.valuepart = ValuePart(definition["valuepart"])

    def dump(self):
        output = []
        if self.declaration is not None:
            output.append(self.declaration.dump())
        if self.valuepart is not None:
            output.append(self.valuepart.dump())
        return " ".join(output)


class FlowConnectionDefinition:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "flow def"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                raise NotImplementedError  # pragma: no cover

            self.definition = Definition(definition["definition"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.definition.dump())
        return " ".join(output)


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
                    raise NotImplementedError  # pragma: no cover
                elif relationship["name"] == "InterfaceNonOccurrenceUsageMember":
                    raise NotImplementedError  # pragma: no cover
                elif relationship["name"] == "EmptySuccessionMember":
                    raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover

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
                    raise AttributeError("Definition is required.")  # pragma: no cover
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
            raise NotImplementedError  # pragma: no cover


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
                raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover

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
                import re

                return re.sub("\n[\s]*", "\n", self.body)


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
                    raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover

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
            raise NotImplementedError  # pragma: no cover

    def dump(self):
        raise NotImplementedError  # pragma: no cover


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
                        print(definition)  # pragma: no cover
                        raise NotImplementedError  # pragma: no cover

    def dump(self):
        return "\n".join([x.dump() for x in self.children])

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
                raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover
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
                raise AttributeError(
                    "This does not seem to be valid."
                )  # pragma: no cover

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
        if valid_definition(definition, self.__class__.__name__):
            if definition["ownedRelatedElement"]["name"] == "DefaultReferenceUsage":
                self.children = DefaultReferenceUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "AttributeUsage":
                self.children = AttributeUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "BindingConnector":
                self.children = BindingConnector(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "Succession":
                self.children = Succession(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "ReferenceUsage":
                self.children = ReferenceUsage(definition["ownedRelatedElement"])
            else:
                print(definition["ownedRelatedElement"]["name"])  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["ownedRelatedElement"] = self.children.get_definition()
        return output


class ReferenceUsage:
    # ReferenceUsage :
    # 	prefix=RefPrefix ReferenceUsageKeyword usage=Usage
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "ref"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = RefPrefix(definition["prefix"])
            self.child = Usage(definition["usage"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.child.dump())
        return " ".join(output)


class SatisfyRequirementUsage:
    # SatisfyRequirementUsage :
    # 	prefix=OccurrenceUsagePrefix (isAssert ?= 'assert')? ( isNegated ?= 'not' )? 'satisfy'
    # 	( ors = OwnedReferenceSubsetting fsp=FeatureSpecializationPart?
    #     | RequirementUsageKeyword declaration=UsageDeclaration?
    #   )
    #   valuepart=ValuePart? ( 'by' ssm = SatisfactionSubjectMember )?
    #   body=RequirementBody
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = ["satisfy"]
        self.ors = None
        self.valuepart = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])
            if definition["isAssert"]:
                self.keyword.append("assert")
            else:
                self.keyword.append(None)

            if definition["isNegated"]:
                self.keyword.append("not")
            else:
                self.keyword.append(None)

            if definition["declaration"] is not None:
                self.keyword.append("requirement")
                self.declaration = UsageDeclaration(definition["declaration"])
            else:
                self.keyword.append(None)
                self.ors = OwnedReferenceSubsetting(definition["ors"])
                if definition["fsp"] is not None:
                    self.fsp = FeatureSpecializationPart(definition["fsp"])
                else:
                    self.fsp = None
            if definition["valuepart"] is not None:
                self.valuepart = ValuePart(definition["valuepart"])
            if definition["ssm"] is not None:
                self.keyword.append("by")
                self.ssm = SatisfactionSubjectMember(definition["ssm"])
            else:
                self.keyword.append(None)
                self.ssm = None
            self.body = RequirementBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword[1])
        output.append(self.keyword[2])
        output.append(self.keyword[0])
        output.append(self.keyword[3])
        if self.ors is not None:
            output.append(self.ors.dump())
            if self.fsp is not None:
                output.append(self.fsp.dump())
        else:
            if self.declaration is not None:
                output.append(self.declaration.dump())
        if self.valuepart is not None:
            output.append(self.valuepart.dump())
        output.append(self.keyword[4])
        if self.ssm is not None:
            output.append(self.ssm.dump())
        output.append(self.body.dump())
        return " ".join(filter(None, output))


class SatisfactionSubjectMember:
    # SatisfactionSubjectMember :
    # 	ownedRelatedElement = SatisfactionParameter
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = SatisfactionParameter(definition["ownedRelatedElement"])

    def dump(self):
        return self.child.dump()


class SatisfactionParameter:
    # SatisfactionParameter :
    # 	ownedRelationship = SatisfactionFeatureValue
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = SatisfactionFeatureValue(definition["ownedRelationship"])

    def dump(self):
        return self.child.dump()


class SatisfactionFeatureValue:
    # SatisfactionFeatureValue :
    # 	ownedRelatedElement = SatisfactionReferenceExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = SatisfactionReferenceExpression(
                definition["ownedRelatedElement"]
            )

    def dump(self):
        return self.child.dump()


class SatisfactionReferenceExpression:
    # SatisfactionReferenceExpression :
    # 	ownedRelationship = FeatureChainMember
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = FeatureChainMember(definition["ownedRelatedElement"])

    def dump(self):
        return self.child.dump()


class Succession:
    def __init__(self, definition):
        self.prefix = None
        self.declaration = None
        self.keyword = "succession"
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                raise NotImplementedError  # pragma: no cover

            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])

            for child in definition["ownedRelationship"]:
                self.children.append(ConnectorEndMember(child))

            self.body = DefinitionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())

        if self.declaration is not None:
            output.append(self.keyword)
            output.append(self.declaration.dump())

        output.append("first")
        output.append(self.children[0].dump())
        output.append("then")
        output.append(self.children[1].dump())

        output.append(self.body.dump())

        return " ".join(output)


class BindingConnector:
    def __init__(self, definition=None):
        self.prefix = None
        self.declaration = None
        self.keyword = "bind"
        self.children = []
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["prefix"] is not None:
                    # self.prefix = UsagePrefix(definition['prefix'])
                    pass
                if definition["declaration"] is not None:
                    self.declaration = UsageDeclaration(definition["declaration"])

                if len(definition["ownedRelationship"]) == 0:
                    pass
                elif len(definition["ownedRelationship"]) == 2:
                    for child in definition["ownedRelationship"]:
                        self.children.append(ConnectorEndMember(child))
                else:
                    raise NotImplementedError  # pragma: no cover

                self.body = DefinitionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        if self.declaration is not None:
            output.append("binding")
            output.append(self.declaration.dump())
        output.append(self.keyword)

        connectors = []
        for child in self.children:
            connectors.append(child.dump())
        output.append(" = ".join(connectors))

        output.append(self.body.dump())

        return " ".join(output)


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
                raise NotImplementedError  # pragma: no cover
            else:
                self.relationships = []
                for relationship in definition["ownedRelationship"]:
                    if relationship["name"] == "FeatureValue":
                        self.relationships.append(FeatureValue(relationship))
                    elif relationship["name"] == "FeatureValueExpression":
                        raise NotImplementedError  # pragma: no cover
                    elif relationship["name"] == "EmptyAssignmentActionMember":
                        raise NotImplementedError  # pragma: no cover
                    else:
                        raise NotImplementedError  # pragma: no cover

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
            self.element = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        output = []
        if self.isDefault:
            output.append("default")
            if self.isEqual:
                output.append("=")
            elif self.isInitial:
                output.append(":=")
        else:
            output.append("=")
        output.append(self.element.dump())
        return " ".join(output)

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["ownedRelatedElement"] = self.element.get_definition()
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
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError  # pragma: no cover

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


class EqualityExpressionReference:
    # EqualityExpressionReference :
    # 	ownedRelationship = EqualityExpressionMember
    # ;
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            self.children.append(
                EqualityExpressionMember(definition["ownedRelationship"])
            )

    def dump(self):
        return "".join([x.dump() for x in self.children])


class EqualityExpressionMember:
    # EqualityExpressionMember :
    # 	ownedRelatedElement = EqualityExpression
    # ;
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            self.children.append(EqualityExpression(definition["ownedRelatedElement"]))

    def dump(self):
        return "\n".join([x.dump() for x in self.children])


class AndOperand:
    def __init__(self, definition):
        self.operations = []
        if valid_definition(definition, self.__class__.__name__):
            self.operator = definition["operator"]
            if self.operator == "&":
                self.operand = EqualityExpression(definition["operand"])
            else:
                self.operand = EqualityExpressionReference(definition["operand"])

    def dump(self):
        return "".join([self.operator, "\n   ", self.operand.dump()])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": self.operator,
            "operand": self.operand.get_definition(),
        }
        return output


class AndExpression:
    def __init__(self, definition):
        self.operations = []
        if valid_definition(definition, self.__class__.__name__):
            self.equality = EqualityExpression(definition["equality"])
            for op in definition["operation"]:
                self.operations.append(AndOperand(op))

    def dump(self):
        output = [self.equality.dump()]
        for op in self.operations:
            output.append(" ")
            output.append(op.dump())

        return "".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operation": [x.get_definition() for x in self.operations],
            "equality": self.equality.get_definition(),
        }
        return output


class EqualityOperand:
    # EqualityOperand:
    #   operator=EqualityOperator operand=ClassificationExpression
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.operator = definition["operator"]
            self.operand = ClassificationExpression(definition["operand"])

    def dump(self):
        return " ".join([self.operator, self.operand.dump()])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": self.operator,
            "operand": self.operand.get_definition(),
        }
        return output


class EqualityExpression:
    def __init__(self, definition):
        self.operations = []
        if valid_definition(definition, self.__class__.__name__):
            self.classification = ClassificationExpression(definition["classification"])
            for op in definition["operation"]:
                self.operations.append(EqualityOperand(op))

    def dump(self):
        output = [self.classification.dump()]
        for op in self.operations:
            output.append(op.dump())
        return " ".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operation": [x.get_definition() for x in self.operations],
            "classification": self.classification.get_definition(),
        }
        return output


class ClassificationExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["relational"] is not None:
                self.relational = RelationalExpression(definition["relational"])
            else:
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] is None):
                raise NotImplementedError  # pragma: no cover

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


class RelationalOperand:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.operator = definition["operator"]
            self.operand = RangeExpression(definition["operand"])

    def dump(self):
        return " ".join([self.operator, self.operand.dump()])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": self.operator,
            "operand": self.operand.get_definition(),
        }
        return output


class RelationalExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.range = RangeExpression(definition["range"])
            self.operations = []
            for child in definition["operation"]:
                self.operations.append(RelationalOperand(child))

    def dump(self):
        output = [self.range.dump()]
        for child in self.operations:
            output.append(child.dump())

        return " ".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operation": [x.get_definition() for x in self.operations],
            "range": self.range.get_definition(),
        }
        return output


class RangeExpression:
    # RangeExpression :
    # 	additive=AdditiveExpression ('..' operand = AdditiveExpression )?
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.additive = AdditiveExpression(definition["additive"])
            self.operator = ".."
            if definition["operand"] is not None:
                self.operand = AdditiveExpression(definition["operand"])
            else:
                self.operand = None

    def dump(self):
        if self.operand is None:
            return self.additive.dump()
        else:
            return " ".join([self.additive.dump(), self.operator, self.operand.dump()])

    def get_definition(self):
        if self.operand is not None:
            output = {
                "name": self.__class__.__name__,
                "operand": self.operand.get_definition(),
                "additive": self.additive.get_definition(),
            }
        else:
            output = {
                "name": self.__class__.__name__,
                "operand": None,
                "additive": self.additive.get_definition(),
            }
        return output


class AdditiveOperand:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.operator = definition["operator"]
            self.operand = MultiplicativeExpression(definition["operand"])

    def dump(self):
        return "".join([self.operator, self.operand.dump()])


class AdditiveExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            # This is the left hand statement
            self.left_hand = MultiplicativeExpression(definition["multiplicitive"])
            self.operations = []
            if len(definition["operation"]) > 0:
                for child in definition["operation"]:
                    self.operations.append(AdditiveOperand(child))

    def dump(self):
        if len(self.operations) == 0:
            return self.left_hand.dump()
        else:
            output = [self.left_hand.dump()]
            output.append(" ".join([x.dump() for x in self.operations]))
            return " ".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "multiplicitive": self.left_hand.get_definition(),
            "operation": [x.get_definition() for x in self.operations],
        }
        return output


class MultiplicativeOperand:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.operator = definition["operator"]
            self.operand = ExponentiationExpression(definition["operand"])

    def dump(self):
        return " ".join([self.operator, self.operand.dump()])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": self.operator,
            "operand": self.operand.get_definition(),
        }
        return output


class MultiplicativeExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.exponential = ExponentiationExpression(definition["exponential"])
            self.operators = []
            for child in definition["operation"]:
                self.operators.append(MultiplicativeOperand(child))

    def dump(self):
        return "".join([self.exponential.dump()] + [x.dump() for x in self.operators])

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operation": [x.get_definition() for x in self.operators],
            "exponential": self.exponential.get_definition(),
        }
        return output


class ExponentiationExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["unary"] is not None:
                self.unary = UnaryExpression(definition["unary"])
            else:
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] == []):
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operand"] == [] and definition["operator"] is None):
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

            if not (definition["operator"] == ""):
                raise NotImplementedError  # pragma: no cover

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


class ReferenceTyping:
    # ReferenceTyping :
    # 	  type = QualifiedName
    # ;
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.child = QualifiedName(definition["type"])

    def dump(self):
        return self.child.dump()


class PrimaryExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.base = BaseExpression(definition["base"])

            self.children1 = None
            self.children2 = None

            if len(definition["ownedRelationship1"]) > 0:
                self.children1 = FeatureChainMember(definition["ownedRelationship1"][0])

            if len(definition["ownedRelationship2"]) > 0:
                self.children2 = FeatureChainMember(definition["ownedRelationship2"][0])

            self.operator = []
            self.operand = []

            if not (definition["operand"] == [] and definition["operator"] == []):
                for k, child in enumerate(definition["operator"]):
                    self.operator.append(child)
                    if child == "->":
                        self.reference = ReferenceTyping(
                            definition["ownedRelationship"][k]
                        )
                    operand = definition["operand"][k]
                    if operand["name"] == "SequenceExpression":
                        self.operand.append(SequenceExpression(operand))
                    elif operand["name"] == "BodyExpression":
                        self.operand.append(BodyExpression(operand))
                    elif operand["name"] == "ArgumentList":
                        self.operand.append(ArgumentList(operand))

    def dump(self):
        output = [self.base.dump()]
        if self.children1 is not None:
            output.append("." + self.children1.dump())
        for k, v in enumerate(self.operator):
            if v == "#":
                output.append("# ({})".format(self.operand[k].dump()))

            if v == "[":
                output.append("[{}]".format(self.operand[k].dump()))

            if v == "." or v == ".?":
                output.append("{}{}".format(v, self.operand[k].dump()))

            if v == "->":
                output.append(
                    "{}{}{}".format(v, self.reference.dump(), self.operand[k].dump())
                )

        if self.children2 is not None:
            output.append("." + self.children2.dump())

        return "".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operator": [],
            "operand": [],
            "base": self.base.get_definition(),
            "ownedRelationship1": [],
            "ownedRelationship2": [],
        }
        for child in self.operand:
            output["operand"].append(child.get_definition())

        for child in self.operator:
            output["operator"].append(child)

        if self.children1 is not None:
            output["ownedRelationship1"].append(self.children1.get_definition())

        if self.children2 is not None:
            output["ownedRelationship2"].append(self.children2.get_definition())
        return output


class BodyExpression:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = ExpressionBodyMember(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class ExpressionBodyMember:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = ExpressionBody(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class ExpressionBody:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = CalculationBody(definition["body"])

    def dump(self):
        return self.children.dump()


class FeatureChainMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["memberElement"] is not None:
                self.children = QualifiedName(definition["memberElement"])
            else:
                self.children = OwnedFeatureChain(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class SequenceOperand:
    # SequenceOperand:
    #   (',' operand = OwnedExpression)
    #   |
    #   ','
    # ; // Allow trailing comma
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.operand = OwnedExpression(definition["operand"])

    def dump(self):
        return ", " + self.operand.dump()

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operand": self.operand.get_definition(),
        }
        return output


class SequenceExpression:
    # SequenceExpression :
    # 	ownedRelationship=OwnedExpression operation+=SequenceOperand*
    # ;
    def __init__(self, definition):
        self.operations = []
        if valid_definition(definition, self.__class__.__name__):
            self.relationship = OwnedExpression(definition["ownedRelationship"])
            for op in definition["operation"]:
                self.operations.append(SequenceOperand(op))

    def dump(self):
        output = [self.relationship.dump()]
        for op in self.operations:
            output.append(op.dump())
        return "".join(output)

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "operation": [x.get_definition() for x in self.operations],
            "ownedRelationship": self.relationship.get_definition(),
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
            elif definition["ownedRelationship"]["name"] == "SequenceExpression":
                self.relationship = SequenceExpression(definition["ownedRelationship"])
            elif definition["ownedRelationship"]["name"] == "InvocationExpression":
                self.relationship = InvocationExpression(
                    definition["ownedRelationship"]
                )
            else:
                print(definition["ownedRelationship"]["name"])  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

    def dump(self):
        if self.relationship.__class__.__name__ != "SequenceExpression":
            return self.relationship.dump()
        else:
            return "(" + self.relationship.dump() + ")"

    def get_definition(self):
        output = {
            "name": self.__class__.__name__,
            "ownedRelationship": self.relationship.get_definition(),
        }
        return output


class InvocationExpression:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.relationship = OwnedFeatureTyping(definition["ownedRelationship"])
            self.children = ArgumentList(definition["arg_list"])

    def dump(self):
        return "".join([self.relationship.dump(), self.children.dump()])


class ArgumentList:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["pos_list"] is not None:
                self.children = PositionalArgumentList(definition["pos_list"])
            elif definition["named_list"] is not None:
                # Only one, the other, or none
                self.children = NamedArgumentList(definition["named_list"])
            else:
                self.children = None

    def dump(self):
        output = ["("]
        if self.children is not None:
            output.append(self.children.dump())
        output.append(")")
        return "".join(output)


class PositionalArgumentList:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                self.children.append(ArgumentMember(child))

    def dump(self):
        return ",".join([x.dump() for x in self.children])


class ArgumentMember:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = Argument(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class Argument:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = ArgumentValue(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class ArgumentValue:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = OwnedExpression(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class NamedArgumentList:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                self.children.append(NamedArgumentMember(child))

    def dump(self):
        return ",".join([x.dump() for x in self.children])


class NamedArgumentMember:
    def __init__(self, definition):
        self.children = None
        if valid_definition(definition, self.__class__.__name__):
            self.children = NamedArgument(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class NamedArgument:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.redefinition = ParameterRedefinition(definition["redefinition"])
            self.value = ArgumentValue(definition["value"])

    def dump(self):
        return "".join([self.redefinition.dump(), self.value.dump()])


class ParameterRedefinition:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = QualifiedName(definition["redefinedFeature"])

    def dump(self):
        return self.children.dump()


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
            elif definition["ownedRelatedElement"]["name"] == "BehaviorUsageElement":
                self.children = BehaviorUsageElement(definition["ownedRelatedElement"])
            else:
                print(definition["ownedRelatedElement"]["name"])  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "ownedRelatedElement": self.children.get_definition(),
        }


class StructureUsageElement:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
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
            elif definition["ownedRelatedElement"]["name"] == "FlowConnectionUsage":
                self.children = FlowConnectionUsage(definition["ownedRelatedElement"])
            elif definition["ownedRelatedElement"]["name"] == "IndividualUsage":
                self.children = IndividualUsage(definition["ownedRelatedElement"])
            elif (
                definition["ownedRelatedElement"]["name"]
                == "SuccessionFlowConnectionUsage"
            ):
                self.children = SuccessionFlowConnectionUsage(
                    definition["ownedRelatedElement"]
                )
            else:
                print(definition["ownedRelatedElement"]["name"])  # pragma: no cover
                raise NotImplementedError  # pragma: no cover

    def dump(self):
        return self.children.dump()

    def get_definition(self):
        return {
            "name": self.__class__.__name__,
            "ownedRelatedElement": self.children.get_definition(),
        }


class SuccessionFlowConnectionUsage:
    def __init__(self, definition):
        self.keyword = "succession flow"
        self.prefix = None
        self.declaration = None
        self.body = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = OccurrenceUsagePrefix(definition["prefix"])

            if definition["declaration"] is not None:
                self.declaration = FlowConnectionDeclaration(definition["declaration"])

            if definition["body"] is not None:
                self.body = DefinitionBody(definition["body"])

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


class IndividualUsage:
    def __init__(self, definition):
        self.prefix = None
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = BasicUsagePrefix(definition["prefix"])
            self.isIndividual = definition["isIndividual"]
            for child in definition["usageExtension"]:
                self.children.append(UsageExtensionKeyword(child))
            self.usage = Usage(definition["usage"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        if self.isIndividual:
            output.append("individual")
        for child in self.children:
            output.append(child.dump())
        output.append(self.usage.dump())

        return " ".join(output)


class UsageExtensionKeyword:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = PrefixMetadataMember(definition["ownedRelationship"])

    def dump(self):
        return self.children.dump()


class FlowConnectionUsage:
    def __init__(self, definition):
        self.prefix = None
        self.keyword = "flow"
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                raise NotImplementedError  # pragma: no cover
            self.declaration = FlowConnectionDeclaration(definition["declaration"])
            self.body = DefinitionBody(definition["body"])

    def dump(self):
        output = []
        if self.prefix is not None:
            output.append(self.prefix.dump())
        output.append(self.keyword)
        output.append(self.declaration.dump())
        output.append(self.body.dump())
        return " ".join(output)


class FlowConnectionDeclaration:
    def __init__(self, definition):
        self.declaration = None
        self.valuepart = None
        self.children = [None, None, None]
        if valid_definition(definition, self.__class__.__name__):
            if definition["declaration"] is not None:
                self.declaration = UsageDeclaration(definition["declaration"])
            if definition["valuepart"] is not None:
                self.declaration = ValuePart(definition["valuepart"])

            if definition["ownedRelationship_of"] is not None:
                self.children[0] = ItemFeatureMember(definition["ownedRelationship_of"])

            if definition["ownedRelationship_from"] is not None:
                self.children[1] = FlowEndMember(definition["ownedRelationship_from"])

            if definition["ownedRelationship_to"] is not None:
                self.children[2] = FlowEndMember(definition["ownedRelationship_to"])

    def dump(self):
        output = []
        if self.declaration is not None:
            output.append(self.declaration.dump())
        if self.valuepart is not None:
            output.append(self.valuepart.dump())

        if self.children[0] is not None:
            output.append("of")
            output.append(self.children[0].dump())

        if self.children[1] is not None:
            if len(output) > 0:
                output.append("from")
            output.append(self.children[1].dump())
            output.append("to")
            output.append(self.children[2].dump())

        return " ".join(output)


class ItemFeatureMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = ItemFeature(definition["ownedRelatedElement"][0])

    def dump(self):
        return self.children.dump()


class ItemFeature:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = PayloadFeature(definition["ownedRelatedElement"])

    def dump(self):
        return self.children.dump()


class PayloadFeature:
    def __init__(self, definition):
        self.identification = None
        self.valuepart = None
        self.multiplicity1 = None
        self.multiplicity2 = None
        self.children = None
        self.pfsp = None
        if valid_definition(definition, self.__class__.__name__):
            if definition["identification"] is not None:
                self.identification = Identification(definition["identification"])

            if definition["valuepart"] is not None:
                self.identification = ValuePart(definition["valuepart"])

            if definition["multiplicity1"] is not None:
                self.multiplicity1 = OwnedMultiplicity(definition["multiplicity1"])

            if definition["multiplicity2"] is not None:
                self.multiplicity2 = OwnedMultiplicity(definition["multiplicity2"])

            if definition["ownedRelationship"] is not None:
                self.children = OwnedFeatureTyping(definition["ownedRelationship"])

            if definition["pfsp"] is not None:
                self.pfsp = PayloadFeatureSpecializationPart(definition["pfsp"])

    def dump(self):
        output = []
        if self.pfsp is not None:
            if self.identification is not None:
                output.append(self.identification.dump())
            output.append(self.pfsp.dump())
            if self.valuepart is not None:
                output.append(self.valuepart.dump())
        elif self.valuepart is not None:
            if self.identification is not None:
                output.append(self.identification.dump())
            output.append(self.valuepart.dump())
        else:
            if self.multiplicity1 is None:
                output.append(self.children.dump())
                if self.multiplicity2 is not None:
                    output.append(self.multiplicity2.dump())
            else:
                output.append(self.multiplicity1.dump())
                output.append(self.children.dump())
        return "".join(output)


class PayloadFeatureSpecializationPart:
    def __init__(self, definition):
        self.children = []
        self.children2 = []
        self.mp = None
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                self.children.append(FeatureSpecialization(child))

            for child in definition["ownedRelationship2"]:
                self.children2.append(FeatureSpecialization(child))

            if definition["mp"] is not None:
                self.mp = MultiplicityPart(definition["mp"])

    def dump(self):
        output = []
        if self.mp is None:
            for child in self.children:
                output.append(child.dump())
        else:
            if len(self.children2) == 0:
                output.append(self.mp.dump())
                for child in self.children:
                    output.append(child.dump())
            else:
                for child in self.children:
                    output.append(child.dump())
                output.append(self.mp.dump())
                for child in self.children2:
                    output.append(child.dump())
        return "".join(output)


class FlowEndMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = FlowEnd(definition["ownedRelatedElement"][0])

    def dump(self):
        return self.children.dump()


class FlowEnd:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["fes"]:
                self.children.append(FlowEndSubsetting(child))

            for child in definition["ffm"]:
                self.children.append(FlowFeatureMember(child))

    def dump(self):
        return "".join([x.dump() for x in self.children])


class FlowEndSubsetting:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            if definition["referencedFeature"] is not None:
                self.children = QualifiedName(definition["referencedFeature"])
            else:
                self.children = FeatureChainPrefix(definition["ownedRelatedElement"])

    def dump(self):
        if self.children.__class__.__name__ == "QualifiedName":
            return self.children.dump() + "."
        else:
            return self.children.dump()


class FeatureChainPrefix:
    def __init__(self, definition):
        self.children = []
        if valid_definition(definition, self.__class__.__name__):
            for child in definition["ownedRelationship"]:
                self.children.append(
                    OwnedFeatureChaining(definition["ownedRelationship"])
                )

    def dump(self):
        return "".join([x.dump() + "." for x in self.children])


class FlowFeatureMember:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = FlowFeature(definition["ownedRelatedElement"][0])

    def dump(self):
        return self.children.dump()


class FlowFeature:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = FlowRedefinition(definition["ownedRelationship"][0])

    def dump(self):
        return self.children.dump()


class FlowRedefinition:
    def __init__(self, definition):
        if valid_definition(definition, self.__class__.__name__):
            self.children = QualifiedName(definition["redefinedFeature"])

    def dump(self):
        return self.children.dump()


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
                raise NotImplementedError  # pragma: no cover
            else:
                raise NotImplementedError  # pragma: no cover

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
            raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

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
        self.prefix = None
        self.keyword = "attribute"
        if definition is not None:
            if valid_definition(definition, self.__class__.__name__):
                if definition["prefix"] is not None:
                    self.prefix = UsagePrefix(definition["prefix"])
                else:
                    self.prefix = None
                self.usage = Usage(definition["usage"])
        else:
            self.usage = Usage()

    def dump(self):
        if self.prefix is None:
            return " ".join([self.keyword, self.usage.dump()])
        else:
            return " ".join([self.prefix.dump(), self.keyword, self.usage.dump()])

    def get_definition(self):
        output = {"name": self.__class__.__name__, "prefix": None}
        if self.prefix is not None:
            output["prefix"] = self.prefix.get_definition()

        output["usage"] = self.usage.get_definition()

        return output


class UsagePrefix:
    #  UsagePrefix :
    # 	prefix=BasicUsagePrefix usageKeyword += UsageExtensionKeyword*
    # ;
    def __init__(self, definition):
        self.prefix = None
        self.keyword = []
        if valid_definition(definition, self.__class__.__name__):
            if definition["prefix"] is not None:
                self.prefix = BasicUsagePrefix(definition["prefix"])
            for keyword in definition["usageKeyword"]:
                self.keyword.append(UsageExtensionKeyword(keyword))

    def dump(self):
        if self.prefix is not None:
            return " ".join([self.prefix.dump()] + [x.dump() for x in self.keyword])
        else:
            return " ".join([x.dump() for x in self.keyword])


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
                raise NotImplementedError  # pragma: no cover

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
            raise NotImplementedError  # pragma: no cover

    def dump(self):
        raise NotImplementedError  # pragma: no cover


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
                    raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover
            elif definition["ownedRelationship"]["name"] == "Redefinitions":
                self.relationship = Redefinitions(definition["ownedRelationship"])
            else:
                raise NotImplementedError  # pragma: no cover

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
        if valid_definition(definition, self.__class__.__name__):
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
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover
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
                    raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover

    def dump(self):
        return self.type.dump()

    def get_definition(self):
        output = {"name": self.__class__.__name__, "type": self.type.get_definition()}

        return output


class FeatureType:
    def __init__(self, definition):
        if valid_definition(definition, "FeatureType"):
            if len(definition["ownedRelatedElement"]) > 0:
                raise NotImplementedError  # pragma: no cover
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
                raise AttributeError(
                    "This does not seem to be valid."
                )  # pragma: no cover

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
                                raise NotImplementedError  # pragma: no cover
                            elif relationship["name"] == "AliasMember":
                                self.children.append(AliasMember(relationship))
                            elif relationship["name"] == "Import":
                                self.children.append(Import(relationship))
                            else:
                                raise AttributeError(
                                    "Failed to match this relationship"
                                )  # pragma: no cover
                        else:
                            raise NotImplementedError  # pragma: no cover
                else:
                    raise NotImplementedError  # pragma: no cover
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
                raise NotImplementedError  # pragma: no cover

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
                raise AttributeError(
                    "This does not seem to be valid"
                )  # pragma: no cover

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
                raise NotImplementedError  # pragma: no cover
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
        self.names = []
        if valid_definition(definition, self.__class__.__name__):
            for name in definition["names"]:
                self.names.append(name)

    def dump(self):
        return "::".join(self.names)

    def get_definition(self):
        output = {"name": self.__class__.__name__}
        output["names"] = self.names
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
