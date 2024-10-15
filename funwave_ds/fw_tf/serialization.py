import tensorflow as tf
import numpy as np

# Out of module imports
import funwave_ds.fw_py as fpy

# In-module imports
from .get_io import get_inputs, get_outputs
from .save_tf_record import save_tfrecord
from .serialization_type import serialize_int,serialize_float, serialize_string, serialize_tensor



def serialize_dictionary(dicta,feature_dict):
    '''
    Convert a dictionary of tensors, floats, strings, and integers
    to serialized features for a tfrecord

    Arguments:
    - dicta (dictionary): dictionary of FUNWAVE inputs/outputs
    - feature_dict (dictionary): feature description dictionaries

    Returns:
    - feature_dict (dictionary): feature description dictionaries
    '''

    print(f'\nStarted serialization of variables...')
    for key, value in dicta.items():
        # Check if tensor
        if isinstance(value, (np.ndarray, tf.Tensor)):
            print(f'\tSerializing: {key} = TENSOR', flush= True)
            serialize_tensor(feature_dict,key,value)
        # Check if float
        elif isinstance(value, float): 
            print(f'\tSerializing: {key}={value}', flush= True)
            serialize_float(feature_dict,key,value)
        # Check if string
        elif isinstance(value, str):
            print(f'\tSerializing: {key}={value}', flush= True)
            serialize_string(feature_dict,key,value)
        # Check if int
        elif isinstance(value, int):
            print(f'\tSerializing: {key}={value}', flush= True)
            serialize_int(feature_dict,key,value)
    print(f'Serialization complete!')

    return feature_dict

    

def postprocess(functions_to_apply,supp_dict={}):
    '''
    Postprocess the FUNWAVE outputs
    '''

    # Get input dictionary and variables
    In_d_i = fpy.load_input_dict_i()
    in_dict = get_inputs(In_d_i)

    # Get the output variables
    out_dict = get_outputs(In_d_i)

    # Merge in the supplemental variables
    io_dict = {**in_dict, **out_dict, **supp_dict}

    # Apply Post-processing functions
    print(f'\nApplying post-processing functions')
    for func in functions_to_apply:
        print(f'\tApplying function: {func.__name__}')
        post_vars = func(io_dict)
        pp_dict = {**io_dict, **post_vars}
    print(f'\nPost-processing functions successful!')

    # Serialize the dictionary
    serialized_features = serialize_dictionary(pp_dict,{})
    
    # Save out the tfrecord
    save_tfrecord(serialized_features)

    return serialized_features












