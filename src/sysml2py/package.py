#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 23:31:01 2023

@author: christophercox
"""

import yaml

from _import import Import
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
                node_type = list(a['package']['pair'][subnode].keys())[0]
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
    y = '''
package:
    name: AnalysisAnnotation
    pair:
    - import:
      - ScalarValues
      - Real
    - import:
      - AnalysisTooling
      - '*'
    - import:
      - ISQ
      - '*'
    - definition:
        type: action
      name: ComputeDynamics
      pair:
      - name: ToolExecution
        pair:
        - toolName: '"ModelCenter"'
        - uri: '"aserv://localhost/Vehicle/Equation1"'
        type: metadata
      - keyv:
          TimeValue:
            ToolVariable:
              pair:
                name: '"deltaT"'
      - keyv:
          PowerValue:
            ToolVariable:
              pair:
                name: '"power"'
      - keyv:
          Real:
            ToolVariable:
              pair:
                name: '"C_D"'
      - keyv:
          Real:
            ToolVariable:
              pair:
                name: '"C_F"'
      - keyv:
          MassValue:
            ToolVariable:
              pair:
                name: '"mass"'
      - keyv:
          SpeedValue:
            ToolVariable:
              pair:
                name: '"v0"'
      - keyv:
          LengthValue:
            ToolVariable:
              pair:
                name: '"x0"'
      - keyv:
          AccelerationValue:
            ToolVariable:
              pair:
                name: '"a"'
      - keyv:
          SpeedValue:
            ToolVariable:
              pair:
                name: '"v"'
      - keyv:
          LengthValue:
            ToolVariable:
              pair:
                name: '"x"'
'''
                  
    p = Package(y)
    p.dump()