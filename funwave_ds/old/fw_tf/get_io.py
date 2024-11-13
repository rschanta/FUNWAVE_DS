import tensorflow as tf
import numpy as np

# Out of module imports
import funwave_ds.fw_py as fpy

# In-module imports
from .tensor_stacking import load_and_stack_to_tensors


def get_inputs(In_d_i):
    '''
    Get the dictionary of FUNWAVE input.txt parameters for a given
    trial and check valid types

    Arguments:
    - In_d_i (dictionary): dictionary of FUNWAVE input parameters

    Returns:
    - in_dict (dictionary): type-checked dictionary of FUNWAVE input parameters
    '''

    print('\nStarted getting input variables...')
    in_dict = {}   
    # Loop through all possible parameters
    for key, value in In_d_i.items():
        # Ensure that value is a supported type
        if isinstance(value, (str, float, int,np.ndarray, tf.Tensor)):
            # Process tensors
            if isinstance(value, (np.ndarray, tf.Tensor)):
                value = tf.convert_to_tensor(value, dtype=tf.float32)
                print(f'\tFinding: {key}=TENSOR', flush= True)
                in_dict[key] = value
            # Process non-tensors
            else:
                print(f'\tFinding: {key}={value}', flush= True)
                in_dict[key] = value
    return in_dict


def get_outputs(In_d_i):
    '''
    Compress the FUNWAVE outputs from raw binary timestep files to 
    tensorflow tensors

    Arguments:
    - In_d_i (dictionary): dictionary of FUNWAVE input parameters

    Returns:
    - out_dict (dictionary): dictionary of compressed output parameter
    '''

    print('\nStarted getting outputs variables...')

    # Get result folder
    ptr = fpy.get_FW_tri_paths()
    RESULT_FOLDER = ptr['RESULT_FOLDER']

    # Find which variables exist in the RESULT_FOLDER
    var_list = fpy.find_prefixes_path(RESULT_FOLDER)

    # Get dictionary of lists (this is where clean up of underscore happens)
    var_paths = fpy.get_vars_out_paths(RESULT_FOLDER, var_list)
    # Compress to dictionary of tensors
    out_dict = load_and_stack_to_tensors(var_paths,In_d_i)

    return out_dict
