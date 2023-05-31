#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import pytest
import yaml

from src.sysml2py.types import main


def name_fn(name):
    model, model_out = main("./tests/" + name + ".text")
    with open("./tests/out_" + name + ".text", "r") as f:
        test_data = f.read()
    f.close()
    return test_data, yaml.dump(model_out)


def test_subpackage():
    test_data, response = name_fn("subpackage")
    assert response == test_data


def test_multipackage():
    test_data, response = name_fn("multipackage")
    assert response == test_data


def test_ownedpackage():
    test_data, response = name_fn("ownedpackage")
    assert response == test_data


def test_aliaspackage():
    test_data, response = name_fn("aliaspackage")
    assert response == test_data


def test_importpackage():
    test_data, response = name_fn("importpackage")
    assert response == test_data
