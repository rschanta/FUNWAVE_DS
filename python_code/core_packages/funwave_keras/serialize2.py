import os
import tensorflow as tf
import numpy as np
from typing import  Dict
from .utils import get_numbers
from .serialize_type import serialize_int,serialize_float
from .serialize_type import serialize_boolean,serialize_string,serialize_tensor
from .condense import get_list_var_output_paths
from .save_tensors import load_and_stack_to_tensors3, load_array
from pathlib import Path
import numpy as np
import pickle

def extract_prefixes(directory):
        prefixes = []
        for filename in os.listdir(directory):
            # Split at extension
            name, _ = os.path.splitext(filename)
            
            # Identify time step files (ends in XXXXX)
            if name[-5:].isdigit() and len(name) > 5:
                variable_ = name[:-5]
            # Identify non time-step files
            else:
                variable_ = name
            # Append to list
            prefixes.append(variable_)

        # Remove duplicates
        prefix_list = list(set(prefixes))
        return prefix_list

def serialize_all2(dicta,feature_dict):
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

def serialize_outputs2(RESULT_FOLDER,
                        In_d_i,
                        feature_dict=None,
                        var_list=None):
    print('\nStarted compressing outputs...')

    # Construct a feature dict if not given
    if feature_dict is None:
        feature_dict = {}
    # Get var_list if not given
    if var_list is None:
        var_list = extract_prefixes(RESULT_FOLDER)

    # Get dictionary of lists (this is where clean up of underscore happens)
    var_paths = get_list_var_output_paths(RESULT_FOLDER, var_list)
    # Compress to dictionary of tensors
    tensor_dict = load_and_stack_to_tensors3(var_paths,In_d_i)
    # Serialize
    serialized_outputs = serialize_all2(tensor_dict,feature_dict)
    print('Successfully compressed and serialized outputs!')
    return serialized_outputs


def serialize_inputs2(In_d_i,
                        feature_dict=None,
                        var_list=None):



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
    serialized_inputs = serialize_all2(trimmed_input_dict,feature_dict)
    print('Successfully compressed and serialized inputs!')
    return serialized_inputs

def get_MNglob2(In_d_i):
    # Get Mglob and Nglob and ensure they are ints
    try:
        Mglob = In_d_i['Mglob']
        Nglob = In_d_i['Nglob']
        assert isinstance(Mglob, int), "Mglob should be an integer"
        assert isinstance(Nglob, int), "Nglob should be an integer"
        return Mglob, Nglob
    except KeyError as e:
        raise KeyError(f"Missing key: {e.args[0]}")
    except AssertionError as e:
        raise ValueError(str(e))

def load_and_stack_to_tensors2(all_var_dict,In_d_i):
    Mglob, Nglob = get_MNglob2(In_d_i)
    tri_tensor_dict = {}
    # Loop through all variables
    for var, file_list in all_var_dict.items(): 
        var_arrays = []
        # Loop through all files of this variable
        for file_path in file_list:
            var_array = load_array(file_path,Mglob,Nglob)
            var_arrays.append(var_array)
        # Form into tensor, squeeze out any extra dimensions
        var_tensor = np.squeeze(np.stack(var_arrays, axis=0))
        tri_tensor_dict[var] = var_tensor
    
    return tri_tensor_dict


def load_input_dict(path,tri_num):
    with open(path, 'rb') as file:
        In_d = pickle.load(file)
    return In_d[f'tri_{tri_num:05}']