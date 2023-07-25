#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 22:52:46 2023

@author: christophercox
"""

import pytest

<<<<<<< HEAD
from sysml2py.grammar.classes import RootNamespace
        
=======
from sysml2py.grammar import RootNamespace


>>>>>>> 8f1004fea06856f8fd79a4e91a37bdfc948461b3
def test_model_cannot_dump_error():
    with pytest.raises(TypeError):
        RootNamespace("string")


def test_grammar_invalid_dictionary():
    with pytest.raises(AttributeError):
        RootNamespace({})


def test_grammar_invalid_rootnamespace():
    with pytest.raises(ValueError):
        RootNamespace({"name": "invalid"})
