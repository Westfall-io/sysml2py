#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:18:03 2023

@author: christophercox
"""

sysml = '''case def FaultRecovery {
    subject system : AutomationSystem;
    actor engineer : Person;
    objective {
        doc
        /* The engineer determines the cause of the system
        * fault and resolves it returning the system to
        * nominal operation.
        */
    }
}'''

