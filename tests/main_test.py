#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:20:18 2023

@author: christophercox
"""
import pytest

from sysml2py import load, loads, load_grammar
from sysml2py.formatting import classtree

from .functions import strip_ws


def test_grammar_load_fromfile(single_package):
    with open("temp.txt", "w") as f:
        f.write(single_package)
    f.close()

    f = open("temp.txt", "r")
    grammar = load_grammar(f)
    assert strip_ws(classtree(grammar).dump()) == strip_ws(single_package)

def test_grammar_invalid_input():
    with pytest.raises(TypeError):
        load_grammar({})

def test_load_fromfile(single_package):
    with open("temp.txt", "w") as f:
        f.write(single_package)
    f.close()

    f = open("temp.txt", "r")
    model = load(f)
    assert strip_ws(model.dump()) == strip_ws(single_package)

def test_load_fromfile_error(single_package):
    with pytest.raises(TypeError):
        load('string')

def test_load_fromstr(single_package):
    model = loads(single_package)
    assert strip_ws(model.dump()) == strip_ws(single_package)

def test_load_fromstr_error(single_package):
    with pytest.raises(TypeError):
        model = loads({})
