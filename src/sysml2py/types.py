#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:26:47 2023

@author: christophercox
"""

import yaml

# import sys
# sys.stdout = open('./log.txt', 'w')

if __name__ == "__main__":
    import os
    import yaml

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from sysml2py import load, loads
    from sysml2py.formatting import classtree

    a = loads(
        """package 'Port Example' {
    	
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
    )  # , formatting=False)
    print(yaml.dump(a))

    b = classtree(a)

    print("\n\n" + b.dump())
    import string

    print("\n\n" + b.dump().translate(str.maketrans("", "", string.whitespace)))

    # sys.stdout = sys.__stdout__
    # sys.stdout.close()
