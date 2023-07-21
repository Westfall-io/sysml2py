#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:26:16 2023

@author: christophercox
"""

__all__ = ["load", "loads"]
__author__ = "Christopher Cox"

from sysml2py.usage import Item, Attribute, Part, Port
from sysml2py.definition import Model, Package


def load_grammar(fp, formatting="json"):
    """SysML load from file pointer

    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a SysML v2.0 document) or ``s`` (a ``str`` instance containing a SysML
    v2.0 document) to a Python dictionary object.

    Parameters
    ----------
    fp : _io.TextIOWrapper or str
        File pointer to SysML v2.0 document or string instance of SysML v2.0
        document

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

    """SysML load from string

    Deserialize
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
    import io

    if isinstance(fp, io.TextIOWrapper):
        s = fp.read()
    elif isinstance(fp, str):
        s = fp
    else:
        raise TypeError(
            f"the SysML object must be _io.TextIOWrapper or str "
            f"not {fp.__class__.__name__}"
        )

    import importlib.resources as pkg_resources

    from textx import metamodel_from_file, TextXSyntaxError

    import sysml2py
    from sysml2py.formatting import reformat

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
    try:
        model = meta.model_from_str(s, debug=False)
    except TextXSyntaxError as e:
        print(e)
        import sys

        sys.exit()

    if formatting == "json":
        return reformat(model)
    else:
        return model


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
    import io

    if not isinstance(fp, io.TextIOWrapper):
        raise TypeError(
            f"the SysML object must be _io.TextIOWrapper, "
            f"not {fp.__class__.__name__}"
        )

    return loads(fp.read())


def loads(s: str):
    return Model().load(s)
