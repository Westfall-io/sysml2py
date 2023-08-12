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


# 16. Conditional Succession
# 17. Control
# 18. Action Performance
# 19. Assignment Actions
# 20. Asynchronous Messaging
# 21. Opaque Actions
# 22. State Definitions
def test_Training_State_Definitions_State_Definition_Example():
    text = """package 'State Definition Example-1' {
	
	attribute def VehicleStartSignal;
	attribute def VehicleOnSignal;
	attribute def VehicleOffSignal;
		
	state def VehicleStates {
		entry; then off;
		
		state off;
		
		transition off_to_starting
			first off
			accept VehicleStartSignal 
			then starting;
			
		state starting;
		
		transition starting_to_on
			first starting
			accept VehicleOnSignal
			then on;
			
		state on;
		
		transition on_to_off
			first on
			accept VehicleOffSignal
			then off;
	}
	
}"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_State_Definitions_State_Definition_Example_2():
    text = """package 'State Definition Example-2' {

     	attribute def VehicleStartSignal;
     	attribute def VehicleOnSignal;
     	attribute def VehicleOffSignal;

     	state def VehicleStates {
    		entry; then off;

    		state off;
    		accept VehicleStartSignal
     			then starting;

    		state starting;
    		accept VehicleOnSignal
     			then on;

    		state on;
    		accept VehicleOffSignal
     			then off;
     	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


# 23. States
def test_Training_States_State_Actions():
    text = """package 'State Actions' {

     	attribute def VehicleStartSignal;
     	attribute def VehicleOnSignal;
     	attribute def VehicleOffSignal;

     	part def Vehicle;

     	action performSelfTest { in vehicle : Vehicle; }

     	state def VehicleStates { in operatingVehicle : Vehicle; }

     	state vehicleStates : VehicleStates {
    		in operatingVehicle : Vehicle;

    		entry; then off;

    		state off;
    		accept VehicleStartSignal
     			then starting;

    		state starting;
    		accept VehicleOnSignal
     			then on;

    		state on {
     			entry performSelfTest{ in vehicle = operatingVehicle; }
     			do action providePower { /* ... */ }
     			exit action applyParkingBrake { /* ... */ }
    		}
    		accept VehicleOffSignal
     			then off;
     	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_States_State_Decomp1():
    text = """package 'State Decomposition-1' {
    	
    	attribute def VehicleStartSignal;
    	attribute def VehicleOnSignal;
    	attribute def VehicleOffSignal;
    	
    	state def VehicleStates;
    		
    	state vehicleStates : VehicleStates {
    		entry; then off;
    		
    		state off;
    		accept VehicleStartSignal 
    			then starting;
    			
    		state starting;
    		accept VehicleOnSignal
    			then on;
    			
    		state on;
    		accept VehicleOffSignal
    			then off;
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_States_State_Decomp2():
    text = """package 'State Decomposition-1' {
	
    	attribute def VehicleStartSignal;
    	attribute def VehicleOnSignal;
    	attribute def VehicleOffSignal;
    	
    	state def VehicleStates;
    		
    	state vehicleStates : VehicleStates parallel {
    		
    		state operationalStates {
    			entry; then off;
    			
    			state off;
    			accept VehicleStartSignal 
    				then starting;
    				
    			state starting;
    			accept VehicleOnSignal
    				then on;
    				
    			state on;
    			accept VehicleOffSignal
    				then off;
    		}
    		
    		state healthStates { 
    			/* ... */
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


# 24. Transitions
# 25. State Exhibition
# 26. Occurrences
# 27. Individual
# 28. Expressions
def test_Training_Expressions_Car_Mass_Rollup_Example():
    text = """package 'Car Mass Rollup Example 1' {
    	import ScalarValues::*;
    	import MassRollup1::*;
    	
    	part def CarPart :> MassedThing {			
    		attribute serialNumber: String;
    	}
    	
    	part car: CarPart :> compositeThing {	
    		attribute vin :>> serialNumber;
    		
    		part carParts: CarPart[*] :>> subcomponents;
    		
    		part engine :> simpleThing, carParts;
    		
    		part transmission :> simpleThing, carParts;
    	}
    	
    	import SI::kg;
    	part c :> car {
    		attribute :>> simpleMass = 1000[kg];
    		part :>> engine {
    			attribute :>> simpleMass = 100[kg];
    		}
    		
    		part redefines transmission {
    			attribute :>> simpleMass = 50[kg];
    		}	
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Expressions_Car_Mass_Rollup_Example_2():
    text = """package 'Car Mass Rollup 1' {
    	import ScalarValues::*;
    	import MassRollup2::*;
    	
    	part def CarPart :> MassedThing {			
    		attribute serialNumber: String;
    	}
    	
    	part car: CarPart :> compositeThing {	
    		attribute vin :>> serialNumber;
    		
    		part carParts: CarPart[*] :>> subcomponents;
    		
    		part engine :> carParts;
    		
    		part transmission :> carParts;
    	}
    	
    	import SI::kg;
    	part c :> car {
    		attribute :>> simpleMass = 1000[kg];
    		part :>> engine {
    			attribute :>> simpleMass = 100[kg];
    		}
    		
    		part redefines transmission {
    			attribute :>> simpleMass = 50[kg];
    		}	
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Expressions_Mass_Rollup_1():
    text = """package MassRollup1 {
    	import NumericalFunctions::*;
    	
    	part def MassedThing {
    		attribute simpleMass :> ISQ::mass; 
    		attribute totalMass :> ISQ::mass;
    	}
    	
    	part simpleThing : MassedThing {
    		attribute :>> totalMass = simpleMass;
    	}
    	
    	part compositeThing : MassedThing {
    		part subcomponents: MassedThing[*];		
    		attribute :>> totalMass =
    			simpleMass + sum(subcomponents.totalMass); 
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Expressions_Mass_Rollup_2():
    text = """package MassRollup2 {
    	import NumericalFunctions::*;
    	
    	part def MassedThing {
    		attribute simpleMass :> ISQ::mass; 
    		attribute totalMass :> ISQ::mass default simpleMass;
    	}
    	
    	part compositeThing : MassedThing {
    		part subcomponents: MassedThing[*];		
    		attribute :>> totalMass default
    			simpleMass + sum(subcomponents.totalMass); 
    	}
    	
    	part filteredMassThing :> compositeThing {
    		attribute minMass :> ISQ::mass;		
    		attribute :>> totalMass =
    			simpleMass + sum(subcomponents.totalMass.?{in p:>ISQ::mass; p >= minMass});
    	}
    
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


# 29. Calculations
def test_Training_Calculations_Calculation_Definitions():
    text = """package 'Calculation Definitions' {
    	import ScalarValues::Real;
    	import ISQ::*;
    	
    	calc def Power { in whlpwr : PowerValue; in Cd : Real; in Cf : Real; in tm : MassValue; in v : SpeedValue;
    		attribute drag = Cd * v;
    		attribute friction = Cf * tm * v;
    		
    		return : PowerValue = whlpwr - drag - friction;
    	}
    	
    	calc def Acceleration { in tp: PowerValue; in tm : MassValue; in v : SpeedValue;
    		return : AccelerationValue = tp / (tm * v);
    	}
    	
    	calc def Velocity { in dt : TimeValue; in v0 : SpeedValue; in a : AccelerationValue;
    		return : SpeedValue = v0 + a * dt;
     	}
     	
    	calc def Position { in dt : TimeValue; in x0 : LengthValue; in v : SpeedValue;
    		return : LengthValue = x0 + v * dt;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Calculations_Calculation_Usages_1():
    text = """package 'Calculation Usages-1' {
    	import 'Calculation Definitions'::*;
    	
    	part def VehicleDynamics {
    		attribute C_d : Real;
    		attribute C_f : Real;
    		attribute wheelPower : PowerValue;
    		attribute mass : MassValue;
    		
    		action straightLineDynamics {
    			in delta_t : TimeValue;
    			in v_in : SpeedValue;
    			in x_in : LengthValue;
    			out v_out : SpeedValue;
    			out x_out : LengthValue;
    		
    			calc acc : Acceleration {
    				in tp = Power(wheelPower, C_d, C_f, mass, v_in);
    				in tm = mass;
    				in v = v_in;
    				return a;
    			}
    			
    			calc vel : Velocity {
    				in dt = delta_t;
    				in v0 = v_in;
    				in a = acc.a;
    				return v = v_out;
    			}
    			
    			calc pos : Position {
    				in dt = delta_t;
    				in x0 = x_in;
    				in v0 = vel.v;
    				return x = x_out;	
    			}
    		}
    	} 
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Calculations_Calculation_Usages_2():
    text = """package 'Calculation Usages-2' {
	import 'Calculation Definitions'::*;
	
	attribute def DynamicState {
		attribute v: SpeedValue;
		attribute x: LengthValue;
	}
	
	part def VehicleDynamics {
		attribute C_d : Real;
		attribute C_f : Real;
		attribute wheelPower : PowerValue;
		attribute mass : MassValue;
		
		calc updateState { 
			in delta_t : TimeValue; 
			in currState : DynamicState;
			attribute totalPower : PowerValue = Power(wheelPower, C_d, C_f, mass, currState.v);
			
			return attribute newState : DynamicState {
				:>> v = Velocity(delta_t, currState.v, Acceleration(totalPower, mass, currState.v));
				:>> x = Position(delta_t, currState.x, currState.v);
			}
		}
	} 
	
}"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


# 30. Constraints
def test_Training_Constraints_Analytical_Constraints():
    text = """package 'Analytical Constraints' {
    	import 'Calculation Definitions'::*;
    	
    	constraint def StraightLineDynamicsEquations {
    		in p : PowerValue;
    		in m : MassValue;
    		in dt : TimeValue;
    		in x_i : LengthValue;
    		in v_i : SpeedValue;
    		in x_f : LengthValue;
    		in v_f : SpeedValue;
    		in a : AccelerationValue;
    	
    		attribute v_avg : SpeedValue = (v_i + v_f)/2;
    		
    		a == Acceleration(p, m, v_avg) and
    		v_f == Velocity(dt, v_i, a) and
    		x_f == Position(dt, x_i, v_avg)
    	}
    	
    	action def StraightLineDynamics {
    		in power : PowerValue;
    		in mass : MassValue;
    		in delta_t : TimeValue;
    		in x_in : LengthValue;
    		in v_in : SpeedValue;
    		out x_out : LengthValue;
    		out v_out : SpeedValue;
    		out a_out : AccelerationValue;
    	
    	    assert constraint dynamics : StraightLineDynamicsEquations {
    			in p = power;
    			in m = mass;
    			in dt = delta_t;
    			in x_i = x_in;
    			in v_i = v_in;
    			in x_f = x_out;
    			in v_f = v_out;
    			in a = a_out;
    	    }
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Constraint_Assertions_1():
    text = """package 'Constraint Assertions-1' {
    	import ISQ::*;
    	import SI::*;
    	import NumericalFunctions::*;
    	
    	part def Engine;
    	part def Transmission;
    	
    	constraint def MassConstraint {
    		in partMasses : MassValue[0..*];
    		in massLimit : MassValue;
    			
    		sum(partMasses) <= massLimit
    	}
    	
    	part def Vehicle {
    		assert constraint massConstraint : MassConstraint {
    			in partMasses = (chassisMass, engine.mass, transmission.mass);
    			in massLimit = 2500[kg];
    		}
    		
    		attribute chassisMass : MassValue;
    		
    		part engine : Engine {
    			attribute mass : MassValue;
    		}
    		
    		part transmission : Engine {
    			attribute mass : MassValue;
    		}
    	}	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Constraint_Assertions_2():
    text = """package 'Constraint Assertions-2' {
    	import ISQ::*;
    	import SI::*;
    	import NumericalFunctions::*;
    	
    	part def Engine;
    	part def Transmission;
    	
    	constraint def MassConstraint {
    		in partMasses : MassValue[0..*];
    		in massLimit : MassValue;
    	}
    	
    	constraint massConstraint : MassConstraint {
    		in partMasses : MassValue[0..*];
    		in massLimit : MassValue;
    			
    		sum(partMasses) <= massLimit
    	}
    	
    	part def Vehicle {
    		assert massConstraint {
    			in partMasses = (chassisMass, engine.mass, transmission.mass);
    			in massLimit = 2500[kg];
    		}
    		
    		attribute chassisMass : MassValue;
    		
    		part engine : Engine {
    			attribute mass : MassValue;
    		}
    		
    		part transmission : Engine {
    			attribute mass : MassValue;
    		}
    	}	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Constraints_Example_1():
    text = """package 'Constraints Example-1' {
    	import ISQ::*;
    	import SI::*;
    	import NumericalFunctions::*;
    	
    	part def Engine;
    	part def Transmission;
    	
    	constraint def MassConstraint {
    		in partMasses : MassValue[0..*];
    		in massLimit : MassValue;
    			
    		sum(partMasses) <= massLimit
    	}
    	
    	part def Vehicle {
    		constraint massConstraint : MassConstraint {
    			in partMasses = (chassisMass, engine.mass, transmission.mass);
    			in massLimit = 2500[kg];
    		}
    		
    		attribute chassisMass : MassValue;
    		
    		part engine : Engine {
    			attribute mass : MassValue;
    		}
    		
    		part transmission : Engine {
    			attribute mass : MassValue;
    		}
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Constraints_Example_2():
    text = """package 'Constraints Example-2' {
    	import ISQ::*;
    	import SI::*;
    	import NumericalFunctions::*;
    	
    	part def Engine;
    	part def Transmission;
    	
    	constraint def MassConstraint {
    		attribute partMasses : MassValue[0..*];
    		attribute massLimit : MassValue;
    			
    		sum(partMasses) <= massLimit
    	}
    	
    	part def Vehicle {
    		constraint massConstraint : MassConstraint {
    			redefines partMasses = (chassisMass, engine.mass, transmission.mass);
    			redefines massLimit = 2500[kg];
    		}
    		
    		attribute chassisMass : MassValue;
    		
    		part engine : Engine {
    			attribute mass : MassValue;
    		}
    		
    		part transmission : Engine {
    			attribute mass : MassValue;
    		}
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Derivation_Constraints():
    text = """package 'Derivation Constraints' {
    	import 'Constraints Example-1'::*;
    	
    	part vehicle1 : Vehicle {
    		attribute totalMass : MassValue;			
    		assert constraint {totalMass == chassisMass + engine.mass + transmission.mass}	
    	}
    	
    	part vehicle2 : Vehicle {
    		attribute totalMass : MassValue = chassisMass + engine.mass + transmission.mass;
    	}
    	
    	constraint def Dynamics {
    		in mass: MassValue;
    		in initialSpeed : SpeedValue;
    		in finalSpeed : SpeedValue;
    		in deltaT : TimeValue;
    		in force : ForceValue;
    
    		force * deltaT == mass * (finalSpeed - initialSpeed) and
    		mass > 0[kg]
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Constraints_Time_Constraints():
    text = """package 'Time Constraints' {
    	import ISQ::TemperatureValue;
    	import ISQ::DurationValue;
    	import Time::TimeInstantValue;
    	import Time::TimeOf;
    	import Time::DurationOf;
    	import SI::h;
    	import SI::s;

    	attribute def MaintenanceDone;
    	
    	part def Vehicle {
    		attribute maintenanceTime : TimeInstantValue;
    		attribute maintenanceInterval : DurationValue;
    		attribute maxTemperature : TemperatureValue;
    	}
    	
    	state healthStates {
    		in vehicle : Vehicle;
    		
    		entry; then normal;
    		
    		state normal;
    		accept at vehicle.maintenanceTime
    			then maintenance;
    		
    		state maintenance {
    			assert constraint { TimeOf(maintenance) > vehicle.maintenanceTime }
    			assert constraint { TimeOf(maintenance) - TimeOf(normal.done) < 2 [s] }
    			entry assign vehicle.maintenanceTime := vehicle.maintenanceTime + vehicle.maintenanceInterval;
    		}
    		accept MaintenanceDone
    			then normal;
    		
    		constraint { DurationOf(maintenance) <= 48 [h] }
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


# 31. Requirements
def test_Training_Requirements_Requirement_Definitions():
    text = """package 'Requirement Definitions' {
    	import ISQ::*;
    	import SI::*;

    	requirement def MassLimitationRequirement {
    		doc /* The actual mass shall be less than or equal to the required mass. */
    		
    		attribute massActual: MassValue;
    		attribute massReqd: MassValue;
    		
    		require constraint { massActual <= massReqd }
    	}
    	
    	part def Vehicle {
    		attribute dryMass: MassValue;
    		attribute fuelMass: MassValue;
    		attribute fuelFullMass: MassValue;
    	}
    	
    	requirement def <'1'> VehicleMassLimitationRequirement :> MassLimitationRequirement {
    		doc /* The total mass of a vehicle shall be less than or equal to the required mass. */
    		
    		subject vehicle : Vehicle;
    		
    		attribute redefines massActual = vehicle.dryMass + vehicle.fuelMass;
    		
    		assume constraint { vehicle.fuelMass > 0[kg] }
    	}
    	
    	port def ClutchPort;
    	action def GenerateTorque;
    	
    	requirement def <'2'> DrivePowerInterface {
    		doc /* The engine shall transfer its generated torque to the transmission via the clutch interface. */
    		subject clutchPort: ClutchPort;
    	}
    		
    	requirement def <'3'> TorqueGeneration {
    		doc /* The engine shall generate torque as a function of RPM as shown in Table 1. */
    		subject generateTorque: GenerateTorque;
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Requirements_Requirement_Groups():
    text = """package 'Requirement Groups' {
    	import 'Requirement Definitions'::*;
    	import 'Requirement Usages'::*;
    	
    	part def Engine {
    		port clutchPort: ClutchPort;
    		perform action generateTorque: GenerateTorque;
    	}
    	
    	requirement vehicleSpecification {
    		doc /* Overall vehicle requirements group */
    		
    		subject vehicle : Vehicle;
    		
    		require fullVehicleMassLimit;
    		require emptyVehicleMassLimit;
    	}
    	
    	requirement engineSpecification {
    		doc /* Engine power requirements group */
    		
    		subject engine : Engine;
    		
    		requirement drivePowerInterface : DrivePowerInterface {
    			subject = engine.clutchPort;
    		}
    		
    		requirement torqueGeneration : TorqueGeneration {
    			subject = engine.generateTorque;	
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Requirements_Requirement_Satisfaction():
    text = """package 'Requirement Satisfaction' {
    	import 'Requirement Groups'::*;
    	
    	action 'provide power' {
    		action 'generate torque';
    	}
    	
    	part vehicle_c1 : Vehicle {
    		perform 'provide power';
    			
    		part engine_v1: Engine {
    			port :>> clutchPort;
    			perform 'provide power'.'generate torque' :>> generateTorque;
    		}	
    	}
    	
    	part 'Vehicle c1 Design Context' {
    		
    		ref vehicle_design :> vehicle_c1;
    	
    		satisfy vehicleSpecification by vehicle_design;
    		satisfy engineSpecification by vehicle_design.engine_v1;
    	
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())


def test_Training_Requirements_Requirement_Usages():
    text = """package 'Requirement Usages' {
    	import SI::*;
    	import 'Requirement Definitions'::*;
    	
    	requirement <'1.1'> fullVehicleMassLimit : VehicleMassLimitationRequirement {
    		subject vehicle : Vehicle;
    		attribute :>> massReqd = 2000[kg];
    		
    		assume constraint {
    			doc /* Full tank is full. */
    			vehicle.fuelMass == vehicle.fuelFullMass
    		}
    	}
    	
    	requirement <'1.2'> emptyVehicleMassLimit : VehicleMassLimitationRequirement {
    		subject vehicle : Vehicle;
    		attribute :>> massReqd = 1500[kg];
    		
    		assume constraint {
    			doc /* Full tank is empty. */
    			vehicle.fuelMass == 0[kg]
    		}
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
#32. Analysis
def test_Training_Analysis_Analysis_Case_Definition_Example():
    text = """package 'Analysis Case Definition Example' {
    	import 'Calculation Definitions'::*;
    	import 'Analytical Constraints'::*;
    	import USCustomaryUnits::*;
    	import SequenceFunctions::size;
    	import Quantities::ScalarQuantityValue;
    	import ControlFunctions::*;
    	import ScalarValues::Positive;
    	
    	attribute def DistancePerVolumeValue :> ScalarQuantityValue;
    
    	part def Vehicle {
            attribute mass : MassValue;
            attribute cargoMass : MassValue;
            
            attribute wheelDiameter : LengthValue;
            attribute driveTrainEfficiency : Real;
            
            attribute fuelEconomy_city : DistancePerVolumeValue;
            attribute fuelEconomy_highway : DistancePerVolumeValue;
        }
        
        attribute def WayPoint {
    		time : TimeValue;
    		position : LengthValue;
    		speed : SpeedValue;    	
    	}
        
    	analysis def FuelEconomyAnalysis {
    		subject vehicle : Vehicle;
    		return fuelEconomyResult : DistancePerVolumeValue;
    		
    		objective fuelEconomyAnalysisObjective {
    			/*
    			 * The objective of this analysis is to determine whether the
    			 * subject vehicle can satisfy the fuel economy requirement.
    			 */
    			
    			assume constraint {
    				vehicle.wheelDiameter == 33 ['in'] &
    				vehicle.driveTrainEfficiency == 0.4
    			}
    			
    			require constraint {
    				fuelEconomyResult > 30 [mi / gal]
    			}
    		}
    		in attribute scenario : WayPoint[*];
    	
    		action solveForPower {
    			out power : PowerValue[*];
    			out acceleration : AccelerationValue[*];
    		
    			/*
    			 * Solve for the required engine power as a function of time
    			 * to support the scenario.
    			 */
    			assert constraint {
    				(1..size(scenario)-1)->forAll {in i: Positive;
    					StraightLineDynamicsEquations (
    						power#(i),
    						vehicle.mass,
    						scenario.time#(i+1) - scenario.time#(i),
    						scenario.position#(i),
    						scenario.speed#(i),
    						scenario.position#(i+1),
    						scenario.speed#(i+1),
    						acceleration#(i+1)                    
    					)
    				}
    			}
    		}
    		
    		then action solveForFuelConsumption {
    			in power : PowerValue[*] = solveForPower.power;
    			out fuelEconomy : DistancePerVolumeValue = fuelEconomyResult;
    		
    			/*
    			 * Solve the engine equations to determine how much fuel is
    			 * consumed.
    			 */
    		}
    	}
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_Training_Analysis_Analysis_Case_Usage_Example():
    text = """package 'Analysis Case Usage Example' {
    	import 'Analysis Case Definition Example'::*;
    	
    	part vehicleFuelEconomyAnalysisContext {
    		requirement vehicleFuelEconomyRequirements {
    			subject vehicle : Vehicle;
    		}
    		
    		attribute cityScenario : WayPoint[*];
    		attribute highwayScenario : WayPoint[*];
    		
    		analysis cityAnalysis : FuelEconomyAnalysis {
    			subject vehicle = vehicle_c1;
    			in scenario = cityScenario;
    		}
    		
    		analysis highwayAnalysis : FuelEconomyAnalysis {
    			subject vehicle = vehicle_c1;
    			in scenario = highwayScenario;
    		}
    		
    		part vehicle_c1 : Vehicle {
    			
    			attribute :>> fuelEconomy_city = cityAnalysis.fuelEconomyResult;
    			attribute :>> fuelEconomy_highway = highwayAnalysis.fuelEconomyResult;
    		}
    		
    		satisfy vehicleFuelEconomyRequirements by vehicle_c1;
    	}

    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
    
def test_Training_Analysis_Trade_Study_Analysis_Example():
    text = """package 'Trade Study Analysis Example' {
    	import ScalarValues::Real;
    	import TradeStudies::*;
    	
    	part def Engine;
    	part engine4cyl : Engine;
    	part engine6cyl : Engine;
    	
    	calc def PowerRollup { in engine : Engine; return : ISQ::PowerValue; }
    	calc def MassRollup { in engine : Engine; return : ISQ::MassValue; }
    	calc def EfficiencyRollup { in engine : Engine; return : Real; }
    	calc def CostRollup { in engine : Engine; return : Real; }
    	
    	calc def EngineEvaluation { 
    		in power : ISQ::PowerValue;
    		in mass : ISQ::MassValue;
    		in efficiency : Real;
    		in cost : Real;
    		return evaluation : Real;
    	}
    		
    	analysis engineTradeStudy : TradeStudy {
    		subject : Engine = (engine4cyl, engine6cyl);
    		objective : MaximizeObjective;

    		calc :>> evaluationFunction {
    			in part anEngine :>> alternative : Engine;
    			
    			calc powerRollup: PowerRollup { in engine = anEngine; return power; }
    			calc massRollup: MassRollup { in engine = anEngine; return mass; }
    			calc efficiencyRollup: EfficiencyRollup { in engine = anEngine; return efficiency; }
    			calc costRollup: CostRollup { in engine = anEngine; return cost; }
    			
    			return :>> result : Real = EngineEvaluation(
    				powerRollup.power, massRollup.mass, efficiencyRollup.efficiency, costRollup.cost
    			);
    		}
    		
    		return part :>> selectedAlternative : Engine;
    	}
    	
    }"""
    a = loads(text)
    b = classtree(a)
    assert strip_ws(text) == strip_ws(b.dump())
