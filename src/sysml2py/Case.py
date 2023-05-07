#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:05:48 2023

@author: christophercox
"""

class Case:
    def __init__(self, name, subject, doc, actor, objective):
        self.name = name
        self.subject = subject
        self.doc = doc
        self.actor = actor
        self.objective = objective
        
    def loads(self):
        pass