#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:26:47 2023

@author: christophercox
"""
import yaml

from textx import metamodel_from_file

def remove_classes(model):
    
    if type(model) == type(dict()):
        output = {}
        for element in model:
            if not '_' in element[0] and not 'parent' in element:
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
        output = {'name':model.__class__.__name__}
        model_out = remove_classes(model.__dict__)
        output.update(model_out) 
    
    return output

def reformat(model):
    # Convert to dictionary format
    try:
        model_out = {'name':model.__class__.__name__}
        model_out.update(remove_classes(model.__dict__))
    except Exception as e:
        print(e)
        print('Error in printing')
        
    return model_out
    

def loads(in_str):
    if not type(in_str) == type(str()):
        return None
    print(__file__)
    meta = metamodel_from_file(__file__.replace('/types.py', '/SysML.tx'))
    
    model = meta.model_from_str(in_str)
    
    model_out = reformat(model)
    
    return reformat(model_out)
    

def main(filepath='../../tests/multipackage.text'):
    # Load Grammar
    meta = metamodel_from_file(__file__.replace('/types.py', '/SysML.tx'))
    
    # Parse file
    try:
        model = meta.model_from_file(filepath)
    except Exception as e:
        print('Error in parsing: {}'.format(e))
        raise(e)
    
    model_out = reformat(model)
        
    return model, model_out

if __name__ == '__main__':
    def write_test_data(name):
        model, model_out = main('../../tests/'+name+'.text')
        with open('../../tests/out_'+name+'.text', 'w') as f:
            f.write(yaml.dump(model_out))
        f.close()
    
    #write_test_data('multipackage')
    #write_test_data('subpackage')
    #write_test_data('ownedpackage')
    #write_test_data('aliaspackage')
    write_test_data('importpackage')