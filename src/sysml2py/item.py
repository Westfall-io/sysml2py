#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:28:48 2023

@author: christophercox
"""

import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from sysml2py.grammar.classes import ItemUsage, ItemDefinition
from sysml2py.usage import Usage


class Item(Usage):
    def __init__(self, definition=False, name=None):
        Usage.__init__(self)
        if definition:
            self.grammar = ItemDefinition()
        else:
            self.grammar = ItemUsage()
