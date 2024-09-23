'''
    tensor_stacking
        -Function to load in 2D arrays for time series outputs and stack to tensors 
'''

import numpy as np
from pathlib import Path


def load_array(var_XXXXX: Path, Mglob: int, Nglob: int):
    '''
        Loads in an array from a var_XXXXX binary output file or time_dt.txt
    '''
    # Deal with time_dt.txt separately: This is the only allowable ASCII file
    try:
        if var_XXXXX.name == 'time_dt.out':
            return np.loadtxt(var_XXXXX,dtype=np.float32)
        else:
            return np.fromfile(var_XXXXX, dtype=np.float32).reshape(Nglob,Mglob)
    except:
        print('Some issue with dimensions! Substitute with zeros to avoid crashing')
        return np.zeros((Nglob, Nglob))
    
def get_MNglob(In_d_i):
    '''
        Finds Mglob and Nglob for an output, and ensures that they are ints
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

    