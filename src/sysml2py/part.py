#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:12:33 2023

@author: christophercox
"""

import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from sysml2py.grammar.classes import PartUsage, PartDefinition
from sysml2py.usage import Usage

class Part(Usage):
    def __init__(self,definition=False,name=None):
        Usage.__init__(self)
        if definition:
            self.grammar = PartDefinition()
        else:
            self.grammar = PartUsage()