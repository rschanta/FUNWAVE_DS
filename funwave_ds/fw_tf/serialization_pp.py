import os
import pickle
import sys

import tensorflow as tf
import numpy as np

from typing import Dict
from pathlib import Path

import funwave_ds.fw_ba as fba
import funwave_ds.fw_py as fpy

# In-module imports
from .serialization_type import serialize_int,serialize_float, serialize_string, serialize_tensor
from .tensor_stacking import load_and_stack_to_tensors, load_array
from .serialization import serialize_dictionary
from .tf_pipe import apply_pipe

# Out-of-module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fw_py.path_tools import find_prefixes_path, get_vars_out_paths




    
def get_inputs(In_d_i):

    '''
        Gets inputs
    '''

    print('\nStarted getting input variables...')

    # Get dictionary values that are floats,ints, and strings
    in_dict = {}
    for key, value in In_d_i.items():

        # Ensure that it's a valid type
        if isinstance(value, (str, float, int,np.ndarray, tf.Tensor)):

            # Deal with arrays/tensors separetly
            if isinstance(value, (np.ndarray, tf.Tensor)):
                value = tf.convert_to_tensor(value, dtype=tf.float32)
                print(f'\tFinding: {key}=TENSOR', flush= True)
                in_dict[key] = value
            else:
                print(f'\tFinding: {key}={value}', flush= True)
                in_dict[key] = value
    return in_dict


def get_outputs(In_d_i):
    '''
        Gets outputs
    '''

    print('\nStarted getting outputs variables...')

    # Get result folder
    p = fpy.get_FW_paths()
    tri_num = os.getenv('TRI_NUM')
    ptr = fpy.get_FW_tri_paths()
    RESULT_FOLDER = ptr['RESULT_FOLDER']

    # Find which variables exist in the RESULT_FOLDER
    var_list = find_prefixes_path(RESULT_FOLDER)

    # Get dictionary of lists (this is where clean up of underscore happens)
    var_paths = get_vars_out_paths(RESULT_FOLDER, var_list)
    # Compress to dictionary of tensors
    out_dict = load_and_stack_to_tensors(var_paths,In_d_i)

    return out_dict


def internal_postprocess(In_d_i,
                        functions_to_apply,supp_dict={}):

    # Get the input variables
    in_dict = get_inputs(In_d_i)

    # Get the output variables
    out_dict = get_outputs(In_d_i)

    # Merge in the supplemental variables
    io_dict = {**in_dict, **out_dict, **supp_dict}

    # Perform post-processing functions
    pp_dict = apply_pipe(io_dict,functions_to_apply)

    # Serialize the dictionary
    print(f'\nStarted serialization of variables...')
    serialized_features = serialize_dictionary(pp_dict,{})
    print(f'Serialization complete!')
    return serialized_features

