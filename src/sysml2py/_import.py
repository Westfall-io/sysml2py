#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 23:34:21 2023

@author: christophercox
"""

import yaml

from base import BaseNode

class Import(BaseNode):
    def __init__(self, yaml_config):
        a = yaml.safe_load(yaml_config)
        
        if 'import' in a:
            self.text = "import " + "::".join(a['import']) + ";"
        else:
            raise AttributeError
            
    