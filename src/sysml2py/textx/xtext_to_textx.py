#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:41:15 2023

@author: christophercox
"""
import re


def xtext_to_textx(rules):
    # Remove grammar
    rules = re.sub("grammar .*", "", rules)

    # Remove imports
    rules = re.sub("import .*", "", rules)

    # Remove returns
    rules = re.sub("returns .*", ":", rules)

    # Remove terminal
    rules = re.sub("terminal ", "", rules)

    # Remove fragments
    rules = re.sub("fragment", "", rules)
    rules = re.sub("enum", "", rules)
    rules = re.sub(" ->", "", rules)
    rules = re.sub("[\s]?=>", "", rules)
    rules = re.sub("@Override", "", rules)

    # Remove SysML object references
    rules = re.sub("{SysML::[a-zA-Z]*}", "", rules)
    rules = re.sub("{SysML::[a-zA-Z\.\+\=\s]*}", "", rules)

    # Remove more SysML object references
    # rules = re.sub('SysML::Membership\|QualifiedName', 'QualifiedName', rules)
    # rules = re.sub('SysML::Namespace\|QualifiedName', 'QualifiedName', rules)
    # rules = re.sub('SysML::Element\|QualifiedName', 'QualifiedName', rules)
    # rules = re.sub('SysML::Feature[\s]?\|[\s]?QualifiedName', 'QualifiedName', rules)
    rules = re.sub(
        "\[[\s]?SysML::[a-zA-Z]*[\s]?\|[\s]?QualifiedName[\s]?\]",
        "[QualifiedName]",
        rules,
    )
    rules = re.sub(
        "SysML::ConjugatedPortDefinition | ConjugatedQualifiedName",
        "ConjugatedQualifiedName",
        rules,
    )

    # Fix doubles
    rules = re.sub("\[QualifiedName | QualifiedName\]", "[QualifiedName]", rules)
    rules = re.sub("\[QualifiedName\|QualifiedName\]", "[QualifiedName]", rules)

    # Special cases
    good_str = r"""
MultiplicityRelatedElement :
    (LiteralExpression | FeatureReferenceExpression)
;
    
MultiplicityExpressionMember :
    ownedRelatedElement += MultiplicityRelatedElement
;"""

    rules = re.sub("MultiplicityExpressionMember :[\s\S]*?;", good_str, rules)

    good_str = r"""
ActionBodyItemTarget :
    ( BehaviorUsageMember | ActionNodeMember )
;

ActionBodyItem :
	  ownedRelationship += Import
	| ownedRelationship += AliasMember
	| ownedRelationship += DefinitionMember
	| ownedRelationship += VariantUsageMember
	| ownedRelationship += NonOccurrenceUsageMember
	| ( ownedRelationship += EmptySuccessionMember )?
	  ownedRelationship += StructureUsageMember
	| ownedRelationship += InitialNodeMember
	  ( ownedRelationship += TargetSuccessionMember )*
	| ( ownedRelationship += EmptySuccessionMember )?
	  ownedRelationship += ActionBodyItemTarget
	  ( ownedRelationship += TargetSuccessionMember )*
	| ownedRelationship += GuardedSuccessionMember
;
"""
    rules = re.sub("ActionBodyItem :[\s\S]*?;", good_str, rules)

    good_str = r"""    
IfNodeElseMember :
    ( ActionBodyParameterMember | IfNodeParameterMember )
;

IfNode :
	ActionNodePrefix 
	'if' ownedRelationship += ExpressionParameterMember
	ownedRelationship += ActionBodyParameterMember
	( 'else' ownedRelationship += IfNodeElseMember )?
;
"""
    rules = re.sub("IfNode :[\s\S]*?;", good_str, rules)

    good_str = r"""
( isOrdered ?= 'ordered' isNonunique ?= 'nonunique'
   | isNonunique2 ?= 'nonunique' isOrdered2 ?= 'ordered'
)
"""
    rules = re.sub("\( isOrdered[a-zA-Z0-9\?\=\s'\|]*\)", good_str, rules)

    # These are totally broken
    empty_rule = "LifeClass"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "EmptyTargetEnd"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "PortConjugation"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "EmptySourceEnd"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "EmptyUsage"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "EmptyActionUsage"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )
    empty_rule = "EmptyFeature"
    rules = re.sub(
        empty_rule + " :[\s\S]*?;",
        empty_rule + " ://This doesn't work.\n\t'" + empty_rule.lower() + "'\n;",
        rules,
    )

    # Base rules
    rules = re.sub(
        "DECIMAL_VALUE[\s]:[\s0-9\(\)'\*\.]*;", "DECIMAL_VALUE :\n   /[0-9]*/;", rules
    )
    rules = re.sub(
        "ID[\s]?:[\sa-zA-Z0-9_'|().*]*;", "ID :\n   /[a-zA-Z_][a-zA-Z_0-9]*/;", rules
    )
    # rules = re.sub("UNRESTRICTED_NAME[ ]?:[\sbtnfr\"!\\_'|().*]*;",
    #    "UNRESTRICTED_NAME: \n   /'\'' ('\\' ('b' | 't' | 'n' | 'f' | 'r' | '"' | "'" | '\\') | !('\\' | '\''))* '\''/;", rules)

    final_rules = """;
    
ID :
   /[a-zA-Z_][a-zA-Z_0-9]*/;

UNRESTRICTED_NAME :
	/'\'' ('\\' ('b' | 't' | 'n' | 'f' | 'r' | '"' | "'" | '\\') | !('\\' | '\''))* '\''/;

STRING_VALUE :
	/'"' ('\\' ('b' | 't' | 'n' | 'f' | 'r' | '"' | "'" | '\\') | !('\\' | '"'))* '"'/;

REGULAR_COMMENT:
	'/*''*/';

ML_NOTE:
	/'\/*'->'*\/'/;

SL_NOTE:
	/'\/\/' (!('\n' | '\r') !('\n' | '\r')*)? ('\r'? '\n')?/;

WS:
	/(' ' | '\t' | '\r' | '\n')+/;
"""
    rules = re.sub(";[\s]*ID[\s\S]*;", final_rules, rules)
    return rules


if __name__ == "__main__":
    with open("SysML.xtext", "r") as f:
        rules = f.read()
    f.close()

    rules = xtext_to_textx(rules)

    with open("SysML.tx", "w") as f:
        f.write("import KerML\nimport KerMLExpressions\n" + rules)
    f.close()

    with open("KerML.xtext", "r") as f:
        rules = f.read()
    f.close()

    rules = xtext_to_textx(rules)

    with open("KerML.tx", "w") as f:
        f.write("import KerMLExpressions\n" + rules)
    f.close()

    with open("KerMLExpressions.xtext", "r") as f:
        rules = f.read()
    f.close()

    rules = xtext_to_textx(rules)

    with open("KerMLExpressions.tx", "w") as f:
        f.write(rules)
    f.close()
