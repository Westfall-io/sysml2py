#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 23:31:01 2023

@author: christophercox
"""

import yaml

from _import import Import
from action import Action
from base import BaseNode

node_factory = {cls.__name__.lower(): cls for cls in BaseNode.__subclasses__()}

class Package(BaseNode):
    def __init__(self, yaml_config):
        a = yaml.safe_load(yaml_config)
        
        # Ensure this is configured correctly
        if 'package' in a:
            if 'name' in a['package']:
                self.name = a['package']['name']
            else:
                raise AttributeError
        else:
            raise AttributeError
        
        # Load all nodes
        subnodes = len(a['package']['pair'])
        if subnodes > 0:
            self.subnodes = []
            
            for subnode in range(subnodes):
                if not list(a['package']['pair'][subnode].keys())[0] == 'definition':
                    node_type = list(a['package']['pair'][subnode].keys())[0]
                else:
                    # Subnode is definition
                    if 'type' in a['package']['pair'][subnode]['definition']:
                        node_type = a['package']['pair'][subnode]['definition']['type']
                    else:
                        # WARNING
                        pass
                    
                new_node_fn = node_factory.get(node_type, None)
                
                if new_node_fn is None:
                    print(node_factory)
                    pass
                    #raise AttributeError(
                    #    "ERROR: Node type {} not loaded in Factory".format(node_type)
                    #)
                
                else:
                    new_node = new_node_fn(yaml.dump(a['package']['pair'][subnode]))
                    self.subnodes.append(new_node)
        
        # Make the text for this node
        self.text = "package " + self.name + " {"
        for subnode in self.subnodes:
            self.text += "\n   " + subnode.text
        self.text += "\n}"
            
if __name__ == '__main__':
    from examples import sysml2
    from loads import loads
    y = yaml.dump(loads(sysml2)['start'])              
    p = Package(y)
    p.dump()