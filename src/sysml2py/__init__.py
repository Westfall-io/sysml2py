#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 23:26:16 2023

@author: christophercox
"""

__all__ = ["load", "loads", "load_grammar"]
__author__ = "Christopher Cox"
__version__ = "0.1.0"

from sysml2py.usage import Item, Attribute, Part, Port
from sysml2py.definition import Model, Package


def enforce_grammar():  # pragma: no cover
    import re

    comments_strip_rule = r"(?:(?:(?<!\\)(\/\/.*\n))|(?:\/\*(?:.|\n)*?\*\/))"
    regex_rule = "\n[ ]*([\w]*)[ ]*:((?:(?:'[^']*')|(?:[^;']*))*;)"

    g_list = []
    rule_files = ["KerMLExpressions", "KerML", "SysML"]
    for file in rule_files:
        with open("grammar/" + file + ".tx", "r") as f:
            g_list = (
                re.findall(regex_rule, re.sub(comments_strip_rule, "", f.read()))
                + g_list
            )

    # Make a new list and only add it if it's not already there
    rules = []
    [rules.append(x) for x in g_list if x[0] not in [x[0] for x in rules]]
    grammar = "\n\n".join([":".join(x) for x in rules])
    with open("grammar/SysML_compiled.tx", "w") as f:
        f.write(grammar)
    return grammar


def load_grammar(fp, debug=False, enforce=False):
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

    from sysml2py.formatting import reformat

    if enforce:  # pragma: no cover
        # This can only be run in development mode.
        from textx import metamodel_from_str, TextXSyntaxError

        grammar = enforce_grammar()
        meta = metamodel_from_str(grammar)
    else:
        import importlib.resources as pkg_resources
        import sysml2py
        from textx import metamodel_from_file, TextXSyntaxError

        grammar = str((pkg_resources.files(sysml2py) / "grammar/SysML_compiled.tx"))
        meta = metamodel_from_file(grammar)

    try:
        model = meta.model_from_str(s, debug=debug)
    except TextXSyntaxError as e:
        print("TextX returned the following error: {}".format(e))
        raise TextXSyntaxError("Invalid SysML")

    return reformat(model)


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
