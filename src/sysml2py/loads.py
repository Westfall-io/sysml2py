#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:20:32 2023

@author: christophercox
"""
import lark
import sys

def tree_to_json_str(item):
    output = []
    tree_to_json(tree, output.append)  # will build output in memory
    return ''.join(output)

def tree_to_json(item, write=None):
    """ Writes a Lark tree as a JSON dictionary. """
    if write is None: write = sys.stdout.write
    _tree_to_json(item, write, 0)

def _tree_to_json(item, write, level):
    indent = '  ' * level
    level += 1
    if isinstance(item, lark.Tree):
        #write(f'{indent}{{ "type": "{item.data}", "children": [\n')
        write(f'{indent}{{ "{item.data}": \n')
        sep = ''
        for child in item.children:
            write(indent)
            write(sep)
            _tree_to_json(child, write, level)
            sep = ',\n'
        write(f'{indent} }}\n')
    elif isinstance(item, lark.Token):
        # reminder: Lark Tokens are directly strings
        # token attrs include: line, end_line, column, end_column, pos_in_stream, end_pos
        write(f'{indent}{{ "type": "{item.type}", "text": "{item}" }}\n')
    else:
        assert False, item  # fall-through
    
if __name__ == '__main__':
    from examples import sysml2
    
    sysml_parser = lark.Lark(r"""
        // A bunch of words
        start: package 
            | type name dict
            | definition name dict
        
        
        package: "package" name dict
        
        // Allow optional punctuation after each word
        type: WORD
        definition: type "def"
        name: WORD
        pointer: WORD
        
        dict: "{" [pair+ | doc | "@" word dict] "}"
        
        all: "*"
        
        word: WORD ["," | "!" | "."]
        variable: (word ["_"])*
        
        import: "import" word [("::" word)* | ("::" all)*]* ";"
        keyv: word "=" ESCAPED_STRING ";"
            | "in" variable ":" word dict
            | "out" variable ":" word dict
        
        pair: type name ":" pointer ";"
            | type dict
            | import
            | type name dict 
            | definition name dict
            | keyv
            
        doc: "doc" "/*" [word* ("*" word*)*] "*/"
        
        // imports WORD from library
        %import common.ESCAPED_STRING
        %import common.WORD
        %import common.WS
        %ignore WS
        
        // Disregard spaces in text
        %ignore " "  
   
    
        """, start='start')
                        
    tree = sysml_parser.parse(sysml2)
    
    print(tree.pretty())
    
    

    # print with tree_to_json
    #tree_to_json(tree)  # will print to stdout
    
    # build JSON string with tree_to_json_str
    #json_str = tree_to_json_str(tree)

    # test that above JSON string is valid
    #import json
    #parsed_json = json.loads(json_str)
    #print(parsed_json)
   