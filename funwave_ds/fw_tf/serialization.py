import os
import pickle
import sys

import tensorflow as tf
import numpy as np

from typing import Dict
from pathlib import Path

# In-module imports
from .serialization_type import serialize_int,serialize_float, serialize_string, serialize_tensor
from .tensor_stacking import load_and_stack_to_tensors, load_array

# Out-of-module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fw_py.path_tools import find_prefixes_path, get_vars_out_paths


def serialize_dictionary(dicta,feature_dict):
    for key, value in dicta.items():
        # Check if tensor
        if isinstance(value, (np.ndarray, tf.Tensor)):
            serialize_tensor(feature_dict,key,value)
        # Check if float
        elif isinstance(value, float): 
            serialize_float(feature_dict,key,value)
        # Check if string
        elif isinstance(value, str):
            serialize_string(feature_dict,key,value)
        # Check if int
        elif isinstance(value, int):
            serialize_int(feature_dict,key,value)
    return feature_dict

    
def serialize_inputs(In_d_i,
                        feature_dict=None,
                        var_list=None):

    '''
        Serializes inputs
    '''

    print('\nStarted compressing inputs...')
    # Construct a feature dict if not given
    if feature_dict is None:
        feature_dict = {}

    ## CASE 1: Get all valid input variables
    if var_list is None:
        # Get dictionary values that are floats,ints, and strings
        trimmed_input_dict = {}
        for key, value in In_d_i.items():
            if isinstance(value, (str, float, int)):
                print(f'Serializing: {key}={value}')
                trimmed_input_dict[key] = value

    ## CASE 2: Get only the input variables in var_list
    elif var_list is not None:
        # Get dictionary values of keys specified
        trimmed_input_dict = {}
        for key in var_list:
            if key in greater_dict:
                if isinstance(value, (str, float, int)):
                    print(f'Serializing: {key}={In_d_i[key]}')
                    trimmed_input_dict[key] = In_d_i[key]
                else:
                    print(f'{key} found in inputs, not but a string,float, or int, so ignored!')

    # Serialize
    serialized_inputs = serialize_dictionary(trimmed_input_dict,feature_dict)
    print('Successfully compressed and serialized inputs!')
    return serialized_inputs


def serialize_outputs(RESULT_FOLDER,
                        In_d_i,
                        feature_dict=None,
                        var_list=None):
    print('\nStarted compressing outputs...')

    # Construct a feature dict if not given
    if feature_dict is None:
        feature_dict = {}
    # Get var_list if not given
    if var_list is None:
        var_list = find_prefixes_path(RESULT_FOLDER)

    # Get dictionary of lists (this is where clean up of underscore happens)
    var_paths = get_vars_out_paths(RESULT_FOLDER, var_list)
    # Compress to dictionary of tensors
    tensor_dict = load_and_stack_to_tensors(var_paths,In_d_i)
    # Serialize
    serialized_outputs = serialize_dictionary(tensor_dict,feature_dict)
    print('Successfully compressed and serialized outputs!')
    return serialized_outputs














