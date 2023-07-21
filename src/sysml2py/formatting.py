#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:26:53 2023

@author: christophercox
"""

from sysml2py.grammar.classes import RootNamespace

# from sysml2py import Part


def remove_classes(model):
    """An example docstring for a class definition."""
    if type(model) == type(dict()):
        output = {}
        for element in model:
            if not "_" in element[0] and not "parent" in element:
                # Remove internal parsing elements
                output[element] = remove_classes(model[element])
    elif type(model) == type(list()):
        # List of classes
        output = []
        for member in model:
            output.append(remove_classes(member))
    elif type(model) == type(None):
        return None
    elif type(model) == type(bool()) or type(model) == type(str()):
        return model
    else:
        output = {"name": model.__class__.__name__}
        model_out = remove_classes(model.__dict__)
        output.update(model_out)

    return output


def reformat(model):
    """An example docstring for a class definition."""
    # Convert to dictionary format
    try:
        model_out = {"name": model.__class__.__name__}
        model_out.update(remove_classes(model.__dict__))
    except Exception as e:
        print(e)
        print("Error in printing")

    return model_out


def classtree(model):
    return RootNamespace(model)


# def collapse(model):
#     """Take a classtree and collapse it into our special classes that
#     package all of the sub-grammar classes."""
#     output = []
#     if model.__class__.__name__ == "RootNamespace":
#         for child in model.children[0].children:
#             if child.__class__.__name__ == "UsageElement":
#                 ue = child.children
#                 if ue.__class__.__name__ == "OccurrenceUsageElement":
#                     se = ue.children
#                     if se.children.__class__.__name__ == "PartUsage":
#                         output.append(Part().load_from_grammar(se.children))
#                     else:
#                         pass
#                 else:
#                     # OccurrenceUsageElement
#                     pass
#             else:
#                 pass
#     else:
#         print("no")
#     return output
