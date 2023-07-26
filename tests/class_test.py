#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:46:28 2023

@author: christophercox
"""

import pytest

from sysml2py.formatting import classtree
from sysml2py import Package, Item, Model, Attribute, Part, Port
from sysml2py import load_grammar as loads


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


def test_package_load_grammar():
    p = Package()

    text = """package Rocket {
       item def Fuel ;
       item Hydrogen : Fuel;
    }"""
    q = Model().load(text)
    p.load_from_grammar(q._get_child("Rocket")._get_grammar())

    assert p.dump() == q.dump()


def test_model_cannot_dump_error():
    m = Model()
    with pytest.raises(ValueError, match="Base Model has no elements."):
        m.dump()


def test_model_load_error_not_package_def():
    text = """item def Fuel ;"""
    with pytest.raises(
        ValueError, match="Base Model must be encapsulated by a package."
    ):
        Model().load(text)


def test_model_load_error_not_package_usage():
    text = """item Fuel ;"""
    with pytest.raises(
        ValueError, match="Base Model must be encapsulated by a package."
    ):
        Model().load(text)


def test_model_add_child():
    m = Model()
    p1 = Package()._set_name("Rocket")
    p2 = Package()._set_name("Payload")
    m._set_child(p1)
    m._set_child(p2)

    text = """package Rocket; 
    package Payload;"""
    q = classtree(loads(text))
    assert m.dump() == q.dump()


def test_model_get_child():
    m = Model()
    p1 = Package()._set_name("Rocket")
    p2 = Package()._set_name("Payload")
    m._set_child(p1)
    m._set_child(p2)
    m2 = m._get_child("Rocket")

    text = """package Rocket;"""
    q = classtree(loads(text))
    assert m2.dump() == q.dump()


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

    assert i1.dump() == i2.dump()


def test_item_def():
    i1 = Item(definition=True)
    text = """item def;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_item_name():
    i1 = Item()._set_name("Fuel")
    text = """item Fuel;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_item_shortname():
    i1 = Item()._set_name("'3.1'", short=True)
    text = """item <'3.1'>;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_item_getname():
    name = "Fuel"
    i1 = Item()._set_name(name)

    assert i1._get_name() == name


def test_item_setchild():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()
    i1._set_child(ic1)
    text = """item Fuel {
        item;
    }"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_item_getchild():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()._set_name("Fuel_child")
    i1._set_child(ic1)
    text = """item Fuel_child;"""
    i2 = classtree(loads(text))

    assert i1._get_child("Fuel.Fuel_child").dump() == i2.dump()


def test_item_getchild_skipelement():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()._set_name("Fuel_child")
    i1._set_child(ic1)
    text = """item Fuel_child;"""
    i2 = classtree(loads(text))

    assert i1._get_child("Fuel_child").dump() == i2.dump()


def test_item_getchild_threelevel():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()._set_name("child")
    ic2 = Item()._set_name("subchild")
    i1._set_child(ic1)
    ic1._set_child(ic2)
    text = """item subchild;"""
    i2 = classtree(loads(text))

    assert i1._get_child("Fuel.child.subchild").dump() == i2.dump()


def test_item_getchild_error_int():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()._set_name("Fuel_child")
    i1._set_child(ic1)
    with pytest.raises(TypeError):
        i1._get_child(1)


def test_item_getchild_error_str():
    i1 = Item()._set_name("Fuel")
    ic1 = Item()._set_name("Fuel_child")
    i1._set_child(ic1)
    assert i1._get_child("Fuel.error") == None


def test_item_typedby():
    p1 = Package()._set_name("Store")
    i1 = Item()._set_name("apple")
    i2 = Item(definition=True)._set_name("Fruit")
    p1._set_child(i1)
    i1._set_typed_by(i2)

    text = """package Store {
       item def Fruit ;
       item apple : Fruit;
    }"""
    p2 = classtree(loads(text))

    assert p1.dump() == p2.dump()


def test_item_typedby_invalidusage_twousage():
    i1 = Item()._set_name("apple")
    i2 = Item()._set_name("Fruit")
    with pytest.raises(ValueError):
        i1._set_typed_by(i2)


def test_item_typedby_invalidusage_twodef():
    i1 = Item(definition=True)._set_name("apple")
    i2 = Item(definition=True)._set_name("Fruit")
    with pytest.raises(ValueError):
        i1._set_typed_by(i2)


def test_part_load_grammar():
    p = Part()

    text = """package Rocket {
        package EngineAssembly;
        part Tank {
            item def Fuel ;
            item Hydrogen : Fuel;
        }
    }"""
    q = Model().load(text)._get_child("Rocket.Tank")
    p.load_from_grammar(q._get_grammar())

    assert p.dump() == q.dump()


def test_part():
    i1 = Part()
    text = """part;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_part_def():
    i1 = Part(definition=True)
    text = """part def;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_part_name():
    i1 = Part()._set_name("Fuel")
    text = """part Fuel;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_part_shortname():
    i1 = Part()._set_name("'3.1'", short=True)
    text = """part <'3.1'>;"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_part_getname():
    name = "Fuel"
    i1 = Part()._set_name(name)

    assert i1._get_name() == name


def test_part_setchild():
    i1 = Part()._set_name("Fuel")
    ic1 = Part()
    i1._set_child(ic1)
    text = """part Fuel {
        part;
    }"""
    i2 = classtree(loads(text))

    assert i1.dump() == i2.dump()


def test_part_getchild():
    i1 = Part()._set_name("Fuel")
    ic1 = Part()._set_name("Fuel_child")
    i1._set_child(ic1)
    text = """part Fuel_child;"""
    i2 = classtree(loads(text))

    assert i1._get_child("Fuel.Fuel_child").dump() == i2.dump()


def test_part_getchild_error_int():
    i1 = Part()._set_name("Fuel")
    ic1 = Part()._set_name("Fuel_child")
    i1._set_child(ic1)
    with pytest.raises(TypeError):
        i1._get_child(1)


def test_part_getchild_error_str():
    i1 = Part()._set_name("Fuel")
    ic1 = Part()._set_name("Fuel_child")
    i1._set_child(ic1)
    assert i1._get_child("Fuel.error") == None


def test_part_typedby():
    p1 = Package()._set_name("Store")
    i1 = Part()._set_name("apple")
    i2 = Part(definition=True)._set_name("Fruit")
    p1._set_child(i1)
    i1._set_typed_by(i2)

    text = """package Store {
       part def Fruit ;
       part apple : Fruit;
    }"""
    p2 = classtree(loads(text))

    assert p1.dump() == p2.dump()


def test_part_typedby_invalidusage_twousage():
    i1 = Part()._set_name("apple")
    i2 = Part()._set_name("Fruit")
    with pytest.raises(ValueError):
        i1._set_typed_by(i2)


def test_part_typedby_invalidusage_twodef():
    i1 = Part(definition=True)._set_name("apple")
    i2 = Part(definition=True)._set_name("Fruit")
    with pytest.raises(ValueError):
        i1._set_typed_by(i2)


def test_port():
    o1 = Port()
    text = """port;"""
    o2 = classtree(loads(text))

    assert o1.dump() == o2.dump()


def test_port_def():
    o1 = Port(definition=True)
    text = """port def;"""
    o2 = classtree(loads(text))

    assert o1.dump() == o2.dump()


def test_port_directed_in():
    o1 = Port()._set_name("FuelHose")
    o1.add_directed_feature("in", "Fuel")
    text = """port FuelHose {
       in Fuel ;
    }"""
    o2 = classtree(loads(text))
    assert o1.dump() == o2.dump()


def test_port_directed_out():
    o1 = Port()._set_name("FuelHose")
    o1.add_directed_feature("out", "Fuel")
    text = """port FuelHose {
       out Fuel ;
    }"""
    o2 = classtree(loads(text))
    assert o1.dump() == o2.dump()


def test_port_directed_inout():
    o1 = Port()._set_name("FuelHose")
    o1.add_directed_feature("inout", "Fuel")
    text = """port FuelHose {
       inout Fuel ;
    }"""
    o2 = classtree(loads(text))
    assert o1.dump() == o2.dump()


def test_port_directed_error():
    o1 = Port()
    with pytest.raises(ValueError):
        o1.add_directed_feature("error", "Fuel")


# This test doesn't work right now
# def test_item_def_subchild():
#     i = Item(definition=True)._set_name("Engine")
#     import astropy.units as u

#     a = Attribute()._set_name("mass")
#     a.set_value(100 * u.kg)
#     i._set_child(a)

#     text = """item Engine {
#         attribute mass= 100.0 [kg];
#     }"""

#     q = classtree(loads(text))

#     assert i.dump() == q.dump()


def test_attribute_definition():
    import astropy.units as u

    a = Attribute(definition=True)._set_name("mass")

    text = """attribute def mass;"""

    q = classtree(loads(text))

    assert a.dump() == q.dump()
    
def test_attribute_units():
    import astropy.units as u

    a = Attribute()._set_name("mass")
    a.set_value(100 * u.kg)

    text = """attribute mass= 100.0 [kg];"""

    q = classtree(loads(text))

    assert a.dump() == q.dump()


def test_attribute_getunits():
    import astropy.units as u

    value = 100 * u.kg

    a = Attribute()._set_name("mass")
    a.set_value(value)

    assert value == a.get_value()


def test_attribute_nounits():
    a = Attribute()._set_name("mass")
    a.set_value(100)

    text = """attribute mass= 100.0;"""

    q = classtree(loads(text))

    assert a.dump() == q.dump()
