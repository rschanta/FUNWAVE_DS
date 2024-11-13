import numpy as np
from pathlib import Path
import tensorflow as tf

'''
    tensor_stacking
        -Function to load in 2D arrays for time series outputs and stack to tensors 
'''

def load_array(var_XXXXX: Path, Mglob: int, Nglob: int):
    '''
        Loads in an array from a var_XXXXX binary output file or time_dt.txt
    '''
    # Deal with time_dt.txt separately: This is the only allowable ASCII file
    try:
        if var_XXXXX.name == 'time_dt.txt':
            return np.loadtxt(var_XXXXX,dtype=np.float32)
        else:
            return np.fromfile(var_XXXXX, dtype=np.float32).reshape(Nglob,Mglob)
    except:
        print('Some issue with dimensions! Substitute with zeros to avoid crashing')
        return np.zeros((Nglob, Nglob))
    
def get_MNglob(In_d_i):
    '''
    Finds Mglob and Nglob for an output, and ensures that they are ints. 
    This is important for loading in binaries to tensors correctly.
    '''
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


def load_and_stack_to_tensors(all_var_dict,In_d_i):
    '''
        Loads in and stacks all the time series array outputs
        into a tensor
    '''

    Mglob, Nglob = get_MNglob(In_d_i)

    tri_tensor_dict = {}
    # Loop through all variables
    for var, file_list in all_var_dict.items(): 
        print(f'\tCompressing: {var}')
        var_arrays = []
        # Loop through all files of this variable
        for file_path in file_list:
            var_array = load_array(file_path,Mglob,Nglob)
            var_arrays.append(var_array)
        # Form into tensor, squeeze out any extra dimensions
        try:
            var_tensor = np.squeeze(np.stack(var_arrays, axis=0))
            tri_tensor_dict[var] = var_tensor
        except:
            print('Issue!')
    return tri_tensor_dict

def deserialize_tensor(parsed_features,var:str):
    '''
    Deserialize a tensor
    '''
    shape = tf.cast(parsed_features[f'{var}_shape'], tf.int64)
    tensor = tf.io.parse_tensor(parsed_features[var], out_type=tf.float32)
    parsed_features[var] = tf.reshape(tensor, shape)
    return parsed_features