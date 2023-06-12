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
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def strip_ws(text):
    text = remove_comments(text)
    return text.translate(str.maketrans('', '', string.whitespace))

def test_package():
    text = 'package Package1;'
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())

def test_subpackage():
    text = '''
    package Package1 {
        package Package2;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_package_owned_members():
    text = '''
    package Package1 {
        package Package2;
        part def Part2;
        part part2 : Part2;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_package_with_alias_member():
    text = '''package Package1 {
        package Package2;
        alias Package2Alias
            for Package2;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_package_with_imported_package():
    text = '''package Package1 {
        import Package2::*;
        private import Package3::*;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_attribute_definition():
    text = '''attribute def AttributeDef1;'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_attribute_usage():
    text = '''attribute attribute1 :
AttributeDef1;'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_attribute_def_subusage():
    text = '''attribute def SensorRecord {
        attribute Reading : Real;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
###################################################
# Examples from:
# https://github.com/Systems-Modeling/SysML-v2-Release/tree/master/sysml/src

def test_Training_Packages_Comment_Example():
    text = '''package 'Comment Example' {
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
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
    
def test_Training_Packages_Documentation_Example():
    text = '''package 'Documentation Example' {
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
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())

def test_Training_Packages_Package_Example():
    text = '''package 'Package Example' {
    	public import ISQ::TorqueValue;
    	private import ScalarValues::*;
    	 
    	private part def Automobile;
    	
    	public alias Car for Automobile;	                         
    	alias Torque for ISQ::TorqueValue;
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_Training_PartDefinition_PartDefinition_Example():
    text = '''package 'Part Definition Example' {
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
    }'''
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    