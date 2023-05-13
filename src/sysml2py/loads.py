#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:20:32 2023

@author: christophercox
"""
import lark
import yaml
import ast

if __name__ == '__main__':
    from examples import sysml2
    
    sysml_parser = lark.Lark(r"""
        start: package 
            | type name dict2
            | definition name dict2
        
        
        package: "package" name dict2
        
        // Allow optional punctuation after each word
        type: WORD
        definition: type "def"
        name: WORD
        pointer: WORD
        
        dict2: "{" [pair+ | doc | "@" word dict2] "}"
        
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
        str2: ESCAPED_STRING
        keyv: word "=" str2 ";"
            | "in" variable ":" word dict2
            | "out" variable ":" word dict2
        
        pair: type name ":" pointer ";"
            | type dict2
            | import
            | type name dict2
            | definition name dict2
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
                c = _tree_to_json(child, level+1)
                if type(c) == type(dict()):
                    # A dictionary was found as a token pair
                    if type(b[str(item.data)]) == type(dict()):
                        # Empty
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
                        b = {str(item.data):{b[str(item.data)]:c}}
                else:
                    # A single value was brought back, this could mean it was
                    # just a WORD or ESCAPED_STRING
                    if type(b[str(item.data)]) == type(dict()):
                        b[str(item.data)] = c
                    elif type(b[str(item.data)]) == type(list()):
                        b[str(item.data)].append(c)
                    else:
                        v = b[str(item.data)]
                        b[str(item.data)] = [v]
                        b[str(item.data)].append(c)
            
            # Remove extra headers
            if str(item.data) == "word" or str(item.data) == 'str2' or str(item.data) == "dict2" or str(item.data) == 'iname':
                a = b[str(item.data)] # eliminate the extra step
            else:
                a = b
                
            if "keyv" in a:
                # Remove a key value pair heading
                if type(a["keyv"]) == type(list()):
                    if len(a["keyv"]) == 2:
                        a = {a["keyv"][0]:a["keyv"][1]}
            elif "pair" in a:
                # Remove a key value pair heading
                if type(a["pair"]) == type(list()):
                    if len(a["pair"]) == 2 and type(a["pair"][0]) == type(str()):
                        a = {a["pair"][0]:a["pair"][1]}
                        
            if "doc" in a:
                if type(a["doc"]) == type(list()):
                    a["doc"] = " ".join(a["doc"])
        
            # Removed, tried to keep headers to be objects
            # if type(a) == type(dict()):
            #     v = [k for k in a.keys()][0]
            #     if type(a[v]) == type(dict()):
            #         if len(a[v].keys()) == 2 and "name" in a[v].keys() and "pair" in a[v].keys():
            #             a = {v:{a[v]['name']:a[v]['pair']}}
                
            return a
        elif isinstance(item, lark.Token):
            #print("item: {}".format(item.type))
            if item.type == 'WORD':
                b = {str(item.type):"".join(item)}
                b = "".join(item)
            elif item.type == 'ESCAPED_STRING':
                b = str(item)
            else:
                b = {str(item.type):"".join(item)}
                
            if "doc" in b:
                pass
            
            return b
            
    a = _tree_to_json(tree)
    print(yaml.dump(a['start']))