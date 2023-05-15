#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 22:50:48 2023

@author: christophercox
"""

import yaml

from base import BaseNode

class Action(BaseNode):
    def __init__(self, yaml_config):
        a = yaml.safe_load(yaml_config)
        
        if 'action' in a:
            self.name = a['name']
            self.text = 'action ' + self.name + ' {'
        elif 'definition' in a:
            if 'type' in a['definition']:
                if a['definition']['type'] == 'action':
                    self.name = a['name']
                    self.text = 'action def ' + self.name + ' {'
                else:
                    raise AttributeError
            else:
                raise AttributeError
        else:
            raise AttributeError
        
        for p in a['pair']:
            if 'type' in p:
                # Create a subnode
                pass
            elif 'keyv' in p:
                if 'input' in p['keyv']:
                    self.text += '\n      in ' + list(p['keyv']['input'].keys())[0]
                    
        
        self.text += "\n   }"