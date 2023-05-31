#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:26:47 2023

@author: christophercox
"""
import yaml

from textx import metamodel_from_file

from sysml2py import load


def main(filepath="../../tests/multipackage.text"):
    """An example docstring for a class definition."""
    # Parse file
    fp = open(filepath, "r")
    model = load(fp)

    return model


if __name__ == "__main__":

    def write_test_data(name):
        model = main("../../tests/" + name + ".text")
        with open("../../tests/out_" + name + ".text", "w") as f:
            f.write(yaml.dump(model))
        f.close()

    # write_test_data('multipackage')
    # write_test_data('subpackage')
    # write_test_data('ownedpackage')
    # write_test_data('aliaspackage')
    write_test_data("importpackage")
