#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:20:32 2023

@author: christophercox
"""
import re

def loads(sysml):
    out = {}
    m = sysml.split()
    #!TODO Check if proper
    stype = m[0]
    
    if m[1] == 'def' and m[3] == '{':
        # This is a definition
        sdef = True
        sname = m[2]
    elif m[2] == '{':
        sdef = False
        sname = m[1]
    else:
        raise NotImplementedError('TBD')
        
    out['type'] = stype
    out['def'] = sdef
    out['name'] = sname
    
    return out
    
if __name__ == '__main__':
    from examples import sysml
    out = loads(sysml)
    print(out)