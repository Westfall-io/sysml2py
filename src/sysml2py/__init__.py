#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:26:16 2023

@author: christophercox
"""
import io

from textx import metamodel_from_file

import importlib.resources as pkg_resources

import sysml2py
from sysml2py.formatting import reformat

__all__ = ["load", "loads"]
__author__ = "Christopher Cox"


def load(fp):
    """SysML load from file pointer

    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a SysML v2.0 document) to a Python dictionary object.

    Parameters
    ----------
    fp : _io.TextIOWrapper
        File pointer to SysML v2.0 document

    Returns
    -------
    dict
        Dictionary version structured utilizing SysML v2.0 grammar with some
        modifications to support available python libraries.

    Raises
    ------
    TypeError
        Input was not _io.TextIOWrapper

    """
    if not isinstance(fp, io.TextIOWrapper):
        raise TypeError(
            f"the SysML object must be _io.TextIOWrapper, "
            f"not {fp.__class__.__name__}"
        )

    return loads(fp.read())


def loads(s, formatting="json"):
    """SysML load from string

    Deserialize ``s`` (a ``str`` instance containing a SysML v2.0 document)
    to a Python dictionary object.

    Parameters
    ----------
    fp : str
        String-format SysML v2.0 document

    Returns
    -------
    dict
        Dictionary version structured utilizing SysML v2.0 grammar with some
        modifications to support available python libraries.

    Raises
    ------
    TypeError
        Input was not str

    """

    if not isinstance(s, str):
        raise TypeError(f"the SysML object must be str, " f"not {s.__class__.__name__}")

    try:
        grammar = str((pkg_resources.files(sysml2py) / "grammar/SysML.tx"))
    except:
        try:
            grammar = "./src/sysml2py/grammar/SysML.tx"
        except:
            grammar = "./grammar/SysML.tx"
    meta = metamodel_from_file(grammar)
    model = meta.model_from_str(s, debug=True)

    if formatting == "json":
        return reformat(model)
    else:
        return model
