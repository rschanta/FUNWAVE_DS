import os
import tensorflow as tf
import numpy as np
from typing import  Dict
from .utils import get_numbers
from .serialize_type import serialize_int,serialize_float
from .serialize_type import serialize_boolean,serialize_string,serialize_tensor


def serialize_inputs(In_d,tri_str: str,feature_dict: Dict[str,tf.train.Feature]):
    '''
    Serializes the variables in the input.txt file for a given trial, returning
    their Feature Dictionary
    
    ARGUMENTS:
        - In_d (dict): master input dictionary 
        - tri (str): string of the form `tri_XXXXX`
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
    RETURNS:
        - feature_dict (dict): feature dictionary with the input.txt parameters
            serialized and added
    '''
    numbers = get_numbers(string=tri_str)
    input_dict = In_d[numbers['tri']]
    
    # Loop through all input variables and handle accordingly
    for var, value in input_dict.items():
        if isinstance(value, int):
            feature_dict = serialize_int(feature_dict,var,value)
        elif isinstance(value, float):
            feature_dict = serialize_float(feature_dict,var,value)
        elif isinstance(value, str):
            if value in {'T', 'F'}:
                feature_dict = serialize_boolean(feature_dict,var,value)
            if value == 'files':
                pass
            else:
                feature_dict = serialize_string(feature_dict,var,value)
    return feature_dict

def serialize_outputs(tri_tensor_dict,feature_dict: Dict[str,tf.train.Feature]):
    '''
    Serializes the all of the outputs from a FUNWAVE run, which are assumed
    to be tensors found in `tri_tensor_dict`
    
    ARGUMENTS:
        - tri_tensor_dict (dict): output from `load_and_stack_to_tensors`
        - feature_dict (dict): dictionary we're storing serialized features to,
            can be empty or contain others
    RETURNS:
        - feature_dict (dict): feature dictionary with the outputs serialized
            and added
    '''
    for var, tensor in tri_tensor_dict.items():
        feature_dict = serialize_tensor(feature_dict,var,tensor)
    return feature_dict

'''
def serialize_bathy_array(In_d,tri_str,feature_dict):

    numbers = get_numbers(string=tri_str)
    input_dict = In_d[numbers['tri']]
    try:
    
        bathy = input_dict['files']['bathy']['array'].astype(np.float32)
        print(bathy)
        feature_dict = serialize_tensor(feature_dict,'bathy',bathy)
    except Exception:
        print('Bathy Array Not Found!')
    return feature_dict

def serialize_all_old(dicta):
    feature_dict = {}
    for key, value in dicta.items():
        print(value)
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

'''
def serialize_all24(dicta,feature_dict):
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
