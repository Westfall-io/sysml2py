#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import pytest
import yaml

from src.sysml2py.types import main

def test_subpackage():
    model, model_out = main('./tests/subpackage.text')
    with open('./tests/out_subpackage.text', 'r') as f:
        test_data = f.read()
    f.close()
    assert yaml.dump(model_out) == test_data