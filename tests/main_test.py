#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import pytest
import yaml
import re

import os
import sys

print("CWD:")
print(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "./src")))

from sysml2py import load, loads
from sysml2py.formatting import classtree

import string


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return ""  # so we will return empty to remove the comment
        else:  # otherwise, we will return the 1st group
            return match.group(1)  # captured quoted-string

    return regex.sub(_replacer, string)


def strip_ws(text):
    text = remove_comments(text)
    text = text.replace('specializes', ':>')
    text = text.replace('subsets', ':>')
    text = text.replace('redefines', ':>>')
    return text.translate(str.maketrans("", "", string.whitespace))


def test_package():
    text = "package Package1;"
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_subpackage():
    text = """
    package Package1 {
        package Package2;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_package_owned_members():
    text = """
    package Package1 {
        package Package2;
        part def Part2;
        part part2 : Part2;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_package_with_alias_member():
    text = """package Package1 {
        package Package2;
        alias Package2Alias
            for Package2;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_package_with_imported_package():
    text = """package Package1 {
        import Package2::*;
        private import Package3::*;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_attribute_definition():
    text = """attribute def AttributeDef1;"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_attribute_usage():
    text = """attribute attribute1 :
AttributeDef1;"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_attribute_def_subusage():
    text = """attribute def SensorRecord {
        attribute Reading : Real;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


###################################################
# Examples from:
# https://github.com/Systems-Modeling/SysML-v2-Release/tree/master/sysml/src


def test_Training_Packages_Comment_Example():
    text = """package 'Comment Example' {
    	/* This is a comment, which is a part of the model, 
    	 * annotating (by default) it's owning namespace. */
    	
    	comment Comment1 /* This is a named comment. */
    	
    	comment about Automobile
    	/* This is an unnamed comment, annotating an 
    	 * explicitly specified element. 
    	 */
    	 
    	part def Automobile;
    	
    	alias Car for Automobile {
    		/*
    		 * This is a comment annotating its owning
    		 * element.
    		 */
    	}	                         
    	
    	// This is a note. It is in the text, but not part 
    	// of the model.
    	alias Torque for ISQ::TorqueValue;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Packages_Documentation_Example():
    text = """package 'Documentation Example' {
    	doc /* This is documentation of the owning 
    	     * package.
    	     */
    	
    	part def Automobile {
    		doc Document1 /* This documentation of Automobile. */
    	}
    	
    	alias Car for Automobile {
    		doc /* This is documentation of the alias. */
    	}
    	alias Torque for ISQ::TorqueValue;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Packages_Package_Example():
    text = """package 'Package Example' {
    	public import ISQ::TorqueValue;
    	private import ScalarValues::*;
    	 
    	private part def Automobile;
    	
    	public alias Car for Automobile;	                         
    	alias Torque for ISQ::TorqueValue;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_PartDefinition_PartDefinition_Example():
    text = """package 'Part Definition Example' {
    	import ScalarValues::*;
    	
    	part def Vehicle {
    		attribute mass : Real;
    		attribute status : VehicleStatus;
    		
    		part eng : Engine;
    		
    		ref part driver : Person;
    	}
    	
    	attribute def VehicleStatus {
    		gearSetting : Integer;
    		acceleratorPosition : Real;
    	}
    	
    	part def Engine;	
    	part def Person;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())

def test_Training_Generalization_Generalization_Example():
    text = """package 'Generalization Example' {

    	abstract part def Vehicle;
    	
    	part def HumanDrivenVehicle specializes Vehicle {
    		ref part driver : Person;
    	}
    	
    	part def PoweredVehicle :> Vehicle {
    		part eng : Engine;
    	}
    	
    	part def HumanDrivenPoweredVehicle :> 
    		HumanDrivenVehicle, PoweredVehicle;
    	
    	part def Engine;	
    	part def Person;
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())

# The following test was removed, as the grammar from sysml doesn't make sense
# to parse this correctly.

# def test_Training_Subsetting_Subsetting_Example():
#     text = """package 'Subsetting Example' {
# 	
#     	part def Vehicle {
#     		part parts : VehiclePart[*];
    		
#     		part eng : Engine subsets parts;
#     		part trans : Transmission subsets parts;
#     		part wheels : Wheel[4] :> parts;
#     	}
    	
#     	abstract part def VehiclePart;
#     	part def Engine :> VehiclePart;
#     	part def Transmission :> VehiclePart;
#     	part def Wheel :> VehiclePart;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())

def test_Training_Redefinition_Redefinition_Example():
    text = """package 'Redefinition Example' {
    
    	part def Vehicle {
    		part eng : Engine;
    	}
    	part def SmallVehicle :> Vehicle {
    		part smallEng : SmallEngine redefines eng;
    	}
    	part def BigVehicle :> Vehicle {
    		part bigEng : BigEngine :>> eng;
    	}
    
    	part def Engine {
    		part cyl : Cylinder[4..6];
    	}
    	part def SmallEngine :> Engine {
    		part redefines cyl[4];
    	}
    	part def BigEngine :> Engine {
    		part redefines cyl[6];
    	}
    
    	part def Cylinder;
    }"""
    
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    

def test_Training_Parts_Parts_Example_1():
    text = """package 'Parts Example-1' {
	
    	// Definitions
    	
    	part def Vehicle {
    		part eng : Engine;
    	}
    	
    	part def Engine {
    		part cyl : Cylinder[4..6];
    	}
    	
    	part def Cylinder;
    	
    	// Usages
    	
    	part smallVehicle : Vehicle {
    		part redefines eng {
    			part redefines cyl[4];
    		}
    	}
    	
    	part bigVehicle : Vehicle {
    		part redefines eng {
    			part redefines cyl[6];
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_Training_Parts_Parts_Example_2():
    text = """package 'Parts Example-2' {
    	
    	// Definitions
    	
    	part def Vehicle;	
    	part def Engine;	
    	part def Cylinder;
    	
    	// Usages
    	
    	part vehicle : Vehicle {
    		part eng : Engine {
    			part cyl : Cylinder[4..6];
    		}
    	}
    	
    	part smallVehicle :> vehicle {
    		part redefines eng {
    			part redefines cyl[4];
    		}
    	}
    	
    	part bigVehicle :> vehicle {
    		part redefines eng {
    			part redefines cyl[6];
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_Training_EnumerationDefinitions_Enumeration_Example():
    text = """package 'Enumeration Definitions-1' {
    	import ScalarValues::Real;
    	
    	enum def TrafficLightColor {
    		enum green;
    		enum yellow;
    		enum red;
    	}
    	
    	part def TrafficLight {
    		attribute currentColor : TrafficLightColor;
    	}
    	
    	part def TrafficLightGo specializes TrafficLight {
    		attribute redefines currentColor = TrafficLightColor::green;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())