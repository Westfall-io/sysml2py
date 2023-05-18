#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:26:47 2023

@author: christophercox
"""

try:
    from textx import metamodel_from_file
    hello_meta = metamodel_from_file('types.type')
    hello_model = hello_meta.model_from_file('types.text')
except Exception as e:
    print('Error in parsing')
    print(e)
    
try:
    print("\n".join([package.declaredName for package in hello_model.package]))
except:
    print('Error in printing')