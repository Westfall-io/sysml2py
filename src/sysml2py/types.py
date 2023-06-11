#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:26:47 2023

@author: christophercox
"""

import yaml

# import sys
# sys.stdout = open('./log.txt', 'w')

def main(filepath="../../tests/multipackage.text"):
    from sysml2py import load, loads
    """An example docstring for a class definition."""
    # Parse file
    fp = open(filepath, "r")
    model = load(fp)

    return model


if __name__ == "__main__":
    import os
    import yaml
    
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
    from sysml2py import load, loads
    from sysml2py.formatting import classtree

    def write_test_data(name):
        model = main("../../tests/" + name + ".text")
        with open("../../tests/out_" + name + ".text", "w") as f:
            f.write(yaml.dump(model))
        f.close()

    # write_test_data('multipackage')
    # write_test_data('subpackage')
    # write_test_data('ownedpackage')
    # write_test_data('aliaspackage')
    #write_test_data("importpackage")
    
    #a = loads("package < '1.1.1' > Salad; package Saldanbas;")
    #a = loads("package Salads {\npackage Dump2 {\npart def Part2;\nitem A;\n}\n}")#, formatting=False)
    a = loads('''package Package1 {
        package Package2;
        part def Part2;
        part part2 : Part2;
    }''')#, formatting=False)
    print(yaml.dump(a))
    
    b = classtree(a)
    import string
    print('\n\n'+b.dump().translate(str.maketrans('', '', string.whitespace)))
    
    # sys.stdout = sys.__stdout__
    # sys.stdout.close()
    
    