#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:20:32 2023

@author: christophercox
"""
import lark
import json

if __name__ == '__main__':
    from examples import sysml2
    
    sysml_parser = lark.Lark(r"""
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
        
        word: WORD ["," | "!" | "." | ":"]
        variable: (word ["_"])*
        
        iname3: "::" word
        iname2: "::" word [iname3]
        iname: word ("::" word)*
        
        LCASE_LETTER: "a".."z" | "*"
        UCASE_LETTER: "A".."Z"

        LETTER: UCASE_LETTER | LCASE_LETTER
        WORD: LETTER+
        
        import: "import" iname ";"
        str: ESCAPED_STRING
        keyv: word "=" str ";"
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
        //%import common.WORD
        //%import common.LETTER
        %import common.WS
        %import lark.STRING
        %ignore WS
        
        // Disregard spaces in text
        %ignore " "   
   
    
        """, start='start', maybe_placeholders=False)
        
        
    tree = sysml_parser.parse(sysml2)
    
    def _tree_to_json(item, level=0):
            
        if isinstance(item, lark.Tree):
            #print("tree {}".format(level))
            b = {str(item.data):{}}
            for child in item.children:
                #print("child: {}".format(level))
                #a[item][child.type] = child
                c = _tree_to_json(child, level+1)
                if type(c) == type(dict()):
                    for key in c.keys():
                        if not key in b[str(item.data)]:
                            # Key did not exist
                            b[str(item.data)][key] = c[key]
                        elif type(b[str(item.data)][key]) == type(list()):
                            b[str(item.data)][key].append(c[key])
                        else:
                            # Don't overwrite values, make a list
                            v = b[str(item.data)][key]
                            b[str(item.data)][key] = [v]
                            b[str(item.data)][key].append(c[key])
                else:
                    b[str(item.data)] = c
            return b
        elif isinstance(item, lark.Token):
            #print("item: {}".format(item.type))
            if item.type == 'WORD':
                b = {str(item.type):"".join(item)}
                b = "".join(item)
            elif item.type == 'ESCAPED_STRING':
                b = str(item)
            else:
                b = {str(item.type):"".join(item)}
            return b
            
    a = _tree_to_json(tree)
    print(json.dumps(a['start']))