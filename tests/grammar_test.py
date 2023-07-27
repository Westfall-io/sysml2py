#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 22:52:46 2023

@author: christophercox
"""

import pytest

from sysml2py.grammar.classes import RootNamespace
from sysml2py import load_grammar as loads
from sysml2py.formatting import classtree

from .functions import strip_ws


def test_model_cannot_dump_error():
    with pytest.raises(TypeError):
        RootNamespace("string")


def test_grammar_invalid_dictionary():
    with pytest.raises(AttributeError):
        RootNamespace({})


def test_grammar_invalid_rootnamespace():
    with pytest.raises(ValueError):
        RootNamespace({"name": "invalid"})


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


def test_Training_Binding_Connectors_Example_1():
    text = """package 'Binding Connectors Example-1' {
    	import 'Port Example'::*;

    	part def Vehicle;
    	part def FuelPump;
    	part def FuelTank;

    	part vehicle : Vehicle {
    		part tank : FuelTankAssembly {
    			port redefines fuelTankPort {
    				out item redefines fuelSupply;
    				in item redefines fuelReturn;
    			}

    			bind fuelTankPort.fuelSupply = pump.pumpOut;
    			bind fuelTankPort.fuelReturn = tank.fuelIn;

    			 part pump : FuelPump {
    				out item pumpOut : Fuel;
    				in item pumpIn : Fuel;
    			}

    			part tank : FuelTank {
    				out item fuelOut : Fuel;
    				in item fuelIn : Fuel;
    			}
    		}
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Binding_Connectors_Example_2():
    text = """package 'Binding Connectors Example-2' {
    	import 'Port Example'::*;

    	part def Vehicle;
    	part def FuelPump;
    	part def FuelTank;

    	part vehicle : Vehicle {
    		part tank : FuelTankAssembly {
    			port redefines fuelTankPort {
    				out item redefines fuelSupply;
    				in item redefines fuelReturn;
    			}

    			part pump : FuelPump {
    				out item pumpOut : Fuel = fuelTankPort.fuelSupply;
    				in item pumpIn : Fuel;
    			}

    			part tank : FuelTank {
    				out item fuelOut : Fuel;
    				in item fuelIn : Fuel = fuelTankPort.fuelReturn;
    			}
    		}
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Flow_Connection_Definition_Example():
    text = """package 'Flow Connection Definition Example' {
    	import 'Port Example'::*;

    	part def Vehicle;

    	flow def FuelFlow {
    		ref :>> payload : Fuel;
    		end port supplierPort : FuelOutPort;
    		end port consumerPort : FuelInPort;
    	}

    	part vehicle : Vehicle {
    		part tankAssy : FuelTankAssembly;
    		part eng : Engine;

    		flow : FuelFlow
    		  from tankAssy.fuelTankPort.fuelSupply
    			to eng.engineFuelPort.fuelSupply;

    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Flow_Connection_Interface_Example():
    text = """package 'Flow Connection Interface Example' {
    	import 'Port Example'::*;

    	part def Vehicle;

    	interface def FuelInterface {
    		end supplierPort : FuelOutPort;
    		end consumerPort : FuelInPort;

    		flow supplierPort.fuelSupply to consumerPort.fuelSupply;
    		flow consumerPort.fuelReturn to supplierPort.fuelReturn;
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


def test_Training_Flow_Connection_Usage_Example():
    text = """package 'Flow Connection Usage Example' {
    	import 'Port Example'::*;

    	part def Vehicle;

    	part vehicle : Vehicle {
    		part tankAssy : FuelTankAssembly;
    		part eng : Engine;

    		flow of Fuel
    		  from tankAssy.fuelTankPort.fuelSupply
    			to eng.engineFuelPort.fuelSupply;

    		flow of Fuel
    		  from eng.engineFuelPort.fuelReturn
    			to tankAssy.fuelTankPort.fuelReturn;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Action_Definition_Example():
    text = """package 'Action Definition Example' {
     	item def Scene;
     	item def Image;
     	item def Picture;

     	action def Focus { in scene : Scene; out image : Image; }
     	action def Shoot { in image: Image; out picture : Picture; }

     	action def TakePicture { in scene : Scene; out picture : Picture;
    		bind focus.scene = scene;

    		action focus: Focus { in scene; out image; }

    		flow focus.image to shoot.image;

    		action shoot: Shoot { in image; out picture; }

    		bind shoot.picture = picture;
     	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Action_Shorthand_Example():
    text = """package 'Action Shorthand Example' {
    	item def Scene;
    	item def Image;
    	item def Picture;

    	action def Focus { in scene : Scene; out image : Image; }
    	action def Shoot { in image: Image; out picture : Picture; }

    	action def TakePicture {
    		in item scene : Scene;
    		out item picture : Picture;

    		action focus: Focus {
    			in item scene = TakePicture::scene;
    			out item image;
    		}

    		flow focus.image to shoot.image;

    		then action shoot: Shoot {
    			in item;
    			out item picture = TakePicture::picture;
    		}
    	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Action_Succession_Example_1():
    text = """package 'Action Succession Example-1' {
    	item def Scene;
    	item def Image;
    	item def Picture;

    	action def Focus { in scene : Scene; out image : Image; }
    	action def Shoot { in image: Image; out picture : Picture; }

    	action def TakePicture {
    		in item scene : Scene;
    		out item picture : Picture;

    		bind focus.scene = scene;

    		action focus: Focus { in scene; out image; }

    		flow focus.image to shoot.image;

    		first focus then shoot;

    		action shoot: Shoot { in image; out picture; }

    		bind shoot.picture = picture;
    	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Action_Succession_Example_2():
    text = """package 'Action Definition Example' {
    	item def Scene;
    	item def Image;
    	item def Picture;

    	action def Focus { in scene : Scene; out image : Image; }
    	action def Shoot { in image: Image; out picture : Picture; }

    	action def TakePicture {
    		in item scene : Scene;
    		out item picture : Picture;

    		bind focus.scene = scene;

    		action focus: Focus { in scene; out image; }

    		succession flow focus.image to shoot.image;

    		action shoot: Shoot { in image; out picture; }

    		bind shoot.picture = picture;
    	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Action_Decomposition():
    text = """package 'Action Decomposition' {
    	part def Scene;
    	part def Image;
    	part def Picture;
    	
    	action def Focus { in scene : Scene; out image : Image; }
    	action def Shoot { in image: Image; out picture : Picture; }	
    	action def TakePicture { in scene : Scene; out picture : Picture; }
    		
    	action takePicture : TakePicture {
    		in item scene;
    		out item picture;
    		
    		action focus : Focus {
    			in item scene = takePicture::scene; 
    			out item image;
    		}
    		
    		flow focus.image to shoot.image;

    		action shoot : Shoot {
    			in item; 
    			out item picture = takePicture::picture;
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
