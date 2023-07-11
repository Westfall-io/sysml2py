#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import re
import string
import os
import sys

print("CWD:")
print(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "./src")))

from sysml2py import loads
from sysml2py.formatting import classtree


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
    text = text.replace("specializes", ":>")
    text = text.replace("subsets", ":>")
    text = text.replace("redefines", ":>>")
    return text.translate(str.maketrans("", "", string.whitespace))


# def test_package():
#     text = "package Package1;"
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_subpackage():
#     text = """
#     package Package1 {
#         package Package2;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_package_owned_members():
#     text = """
#     package Package1 {
#         package Package2;
#         part def Part2;
#         part part2 : Part2;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_package_with_alias_member():
#     text = """package Package1 {
#         package Package2;
#         alias Package2Alias
#             for Package2;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_package_with_imported_package():
#     text = """package Package1 {
#         import Package2::*;
#         private import Package3::*;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_attribute_definition():
#     text = """attribute def AttributeDef1;"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_attribute_usage():
#     text = """attribute attribute1 :
# AttributeDef1;"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


# def test_attribute_def_subusage():
#     text = """attribute def SensorRecord {
#         attribute Reading : Real;
#     }"""
#     a = loads(text)
#     b = classtree(a)
#     assert strip_ws(text) == strip_ws(b.dump())


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


def test_Training_Subsetting_Subsetting_Example():
    text = """package 'Subsetting Example' {

     	part def Vehicle {
    		part parts : VehiclePart[*];

    		part eng : Engine subsets parts;
    		part trans : Transmission subsets parts;
    		part wheels : Wheel[4] :> parts;
     	}

     	abstract part def VehiclePart;
     	part def Engine :> VehiclePart;
     	part def Transmission :> VehiclePart;
     	part def Wheel :> VehiclePart;
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


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


def test_Training_EnumerationDefinitions_Enumeration_Example_1():
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


def test_Training_EnumerationDefinitions_Enumeration_Example_2():
    text = """package 'Enumeration Definitions-2' {
    	import ScalarValues::*;
    	import 'Enumeration Definitions-1'::*;
    	
    	attribute def ClassificationLevel {
    		attribute code : String;
    		attribute color : TrafficLightColor;
    	}
    	
    	enum def ClassificationKind specializes ClassificationLevel {
    		unclassified {
    			:>> code = "uncl";
    			:>> color = TrafficLightColor::green;
    		}
    		confidential {
    			:>> code = "conf";
    			:>> color = TrafficLightColor::yellow;
    		}
    		secret {
    			:>> code = "secr";
    			:>> color = TrafficLightColor::red;
    		}
    	}
    	
    	enum def GradePoints :> Real {
    		A = 4.0;
    		B = 3.0;
    		C = 2.0;
    		D = 1.0;
    		F = 0.0;
    	}
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


def test_Training_Items_Items_Example():
    text = """package 'Items Example' {
    	import ScalarValues::*;
    	
    	item def Fuel;
    	item def Person;
    	
    	part def Vehicle {
    		attribute mass : Real;
    		
    		ref item driver : Person;
    
    		part fuelTank {
    			item fuel: Fuel;
    		}		
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Connections_Connections_Example():
    text = """package 'Connections Example' {
	
    	part def WheelHubAssembly;
    	part def WheelAssembly;
    	part def Tire;
    	part def TireBead;
    	part def Wheel;
    	part def TireMountingRim;
    	part def LugBoltMountingHole;
    	part def Hub;
    	part def LugBoltThreadableHole;
    	part def LugBoltJoint;
    	
    	connection def PressureSeat {
    		end bead : TireBead[1];
    		end mountingRim : TireMountingRim[1];
    	}
    	
    	part wheelHubAssembly : WheelHubAssembly {
    		
    		part wheel : WheelAssembly[1] {
    			part t : Tire[1] {
    				part bead : TireBead[2];			
    			}
    			part w: Wheel[1] {
    				part rim : TireMountingRim[2];
    				part mountingHoles : LugBoltMountingHole[5];
    			}						
    			connection : PressureSeat 
    				connect bead references t.bead 
    				to mountingRim references w.rim;		
    		}
    		
    		part lugBoltJoints : LugBoltJoint[0..5];
    		part hub : Hub[1] {
    			part h : LugBoltThreadableHole[5];
    		}
    		connect lugBoltJoints[0..1] to wheel.w.mountingHoles[1];
    		connect lugBoltJoints[0..1] to hub.h[1];
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Ports_Port_Conjugation_Example():
    text = """package 'Port Conjugation Example' {
	
    	attribute def Temp;
    	
    	part def Fuel;
    	
    	port def FuelPort {
    		attribute temperature : Temp;
    		out item fuelSupply : Fuel;
    		in item fuelReturn : Fuel;
    	}
    	
    	part def FuelTank {
    		port fuelTankPort : FuelPort;
    	}
    	
    	part def Engine {
    		port engineFuelPort : ~FuelPort;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Ports_Port_Example():
    text = """package 'Port Example' {
	
    	attribute def Temp;
    	
    	part def Fuel;
    	
    	port def FuelOutPort {
    		attribute temperature : Temp;
    		out item fuelSupply : Fuel;
    		in item fuelReturn : Fuel;
    	}
    	
    	port def FuelInPort {
    		attribute temperature : Temp;
    		in item fuelSupply : Fuel;
    		out item fuelReturn : Fuel;
    	}
    	
    	part def FuelTankAssembly {
    		port fuelTankPort : FuelOutPort;
    	}
    	
    	part def Engine {
    		port engineFuelPort : FuelInPort;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Interfaces_InterfaceDecomposition_Example():
    text = """package 'Interface Decomposition Example' {
    	
    	port def SpigotBank;
    	port def Spigot;
    	
    	port def Faucet;
    	port def FaucetInlet;
    	
    	interface def WaterDelivery {
    		end suppliedBy : SpigotBank[1] {
    			port hot : Spigot;
    			port cold : Spigot;
    		}
    		end deliveredTo : Faucet[1..*] {
    			port hot : FaucetInlet;
    			port cold : FaucetInlet;
    		}
    		
    		connect suppliedBy.hot to deliveredTo.hot;
    		connect suppliedBy.cold to deliveredTo.cold;
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Interfaces_Interface_Example():
    text = """package 'Interface Example' {
    	import 'Port Example'::*;
    	
    	part def Vehicle;
    	
    	interface def FuelInterface {
    		end supplierPort : FuelOutPort;
    		end consumerPort : FuelInPort;
    	}
    	
    	part vehicle : Vehicle {	
    		part tankAssy : FuelTankAssembly;		
    		part eng : Engine;
    		
    		interface : FuelInterface connect 
    			supplierPort ::> tankAssy.fuelTankPort to 
    			consumerPort ::> eng.engineFuelPort;
    	} 
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
