#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:46:28 2023

@author: christophercox
"""

import pytest

from sysml2py.formatting import classtree
from sysml2py import Package, Item, Model, Attribute
from sysml2py import load_grammar as loads

from .functions import strip_ws


def test_package():
    p = classtree(Package()._get_definition()).dump()

    text = """package ;"""
    q = classtree(loads(text)).dump()

    assert p == q


def test_package_name():
    name = "Rocket"
    p = classtree(Package()._set_name(name)._get_definition()).dump()

    text = "package " + name + ";"
    q = classtree(loads(text)).dump()

    assert p == q


def test_package_shortname():
    name = "'3.1'"
    p = classtree(Package()._set_name(name, short=True)._get_definition()).dump()

    text = "package <" + name + ">;"
    q = classtree(loads(text)).dump()

    assert p == q


def test_package_setbothnames():
    name = "Rocket"
    shortname = "'3.1'"
    p = classtree(
        Package()._set_name(name)._set_name(shortname, short=True)._get_definition()
    ).dump()

    text = "package <" + shortname + "> " + name + ";"
    q = classtree(loads(text)).dump()

    assert p == q


def test_package_getname():
    name = "Rocket"
    p = Package()._set_name(name)
    assert p._get_name() == name


def test_package_addchild():
    p1 = Package()._set_name("Rocket")
    p2 = Package()._set_name("Engine")
    p1._set_child(p2)
    p = classtree(p1._get_definition()).dump()

    text = """package Rocket {
       package Engine;
    }"""

    q = classtree(loads(text)).dump()

    assert p == q


def test_package_get_child():
    p1 = Package()._set_name("Rocket")
    p2 = Package()._set_name("Engine")
    p1._set_child(p2)
    p = classtree(p1._get_child("Rocket.Engine")._get_definition()).dump()

    text = """package Engine;"""

    q = classtree(loads(text)).dump()

    assert p == q


def test_package_get_child_method2():
    p1 = Package()._set_name("Rocket")
    p2 = Package()._set_name("Engine")
    p1._set_child(p2)
    p = classtree(p1._get_child("Engine")._get_definition()).dump()

    text = """package Engine;"""

    q = classtree(loads(text)).dump()

    assert p == q


def test_package_typed_child():
    p1 = Package()._set_name("Rocket")
    i1 = Item(definition=True)._set_name("Fuel")
    i2 = Item()._set_name("Hydrogen")
    p1._set_child(i2)
    i2._set_typed_by(i1)
    p = classtree(p1._get_definition()).dump()

    text = """package Rocket {
       item def Fuel ;
       item Hydrogen : Fuel;
    }"""

    q = classtree(loads(text)).dump()

    assert p == q


def test_model_cannot_dump_error():
    m = Model()
    with pytest.raises(ValueError, match="Base Model has no elements."):
        m.dump()


def test_model_load():
    p1 = Package()._set_name("Rocket")
    i1 = Item(definition=True)._set_name("Fuel")
    i2 = Item()._set_name("Hydrogen")
    p1._set_child(i2)
    i2._set_typed_by(i1)
    p = classtree(p1._get_definition())

    text = """package Rocket {
       item def Fuel ;
       item Hydrogen : Fuel;
    }"""

    q = Model().load(text)

    assert p.dump() == q.dump()
    
def test_item():
    i1 = Item()
    text = """item;"""
    i2 = classtree(loads(text))
    
    assert strip_ws(i1.dump()) == strip_ws(i2.dump())
    
def test_item_name():
    i1 = Item()._set_name("Fuel")
    text = """item Fuel;"""
    i2 = classtree(loads(text))
    
    assert strip_ws(i1.dump()) == strip_ws(i2.dump())
    
def test_item_child():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()
    i1._set_child(ic1)
    text = """item Fuel
        item;
    }"""
    i2 = classtree(loads(text))
    
    assert strip_ws(i1.dump()) == strip_ws(i2.dump())
    

def test_attribute_units():
    import astropy.units as u
    a = Attribute()._set_name('mass')
    a.set_value(100*u.kg)

    text = """attribute mass= 100.0 [kg];"""

    q = classtree(loads(text))

    assert a.dump() == q.dump()


def test_attribute_nounits():
    a = Attribute()._set_name("mass")
    a.set_value(100)

    text = """attribute mass= 100.0;"""

    q = classtree(loads(text))

    assert a.dump() == q.dump()
