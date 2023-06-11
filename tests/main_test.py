#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import pytest
import yaml

import os
import sys

print("CWD:")
print(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "./src")))

from sysml2py import load, loads
from sysml2py.formatting import classtree

import string

# def name_fn(name):
#     model = main("./tests/" + name + ".text")
#     with open("./tests/out_" + name + ".text", "r") as f:
#         test_data = f.read()
#     f.close()
#     return test_data, yaml.dump(model)


def strip_ws(text):
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


# def test_multipackage():
#     test_data, response = name_fn("multipackage")
#     assert response == test_data


# def test_ownedpackage():
#     test_data, response = name_fn("ownedpackage")
#     assert response == test_data


# def test_aliaspackage():
#     test_data, response = name_fn("aliaspackage")
#     assert response == test_data


# def test_importpackage():
#     test_data, response = name_fn("importpackage")
#     assert response == test_data
