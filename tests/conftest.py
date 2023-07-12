#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:49:00 2023

@author: christophercox
"""

import pytest

@pytest.fixture
def single_package():
    return """package;"""
