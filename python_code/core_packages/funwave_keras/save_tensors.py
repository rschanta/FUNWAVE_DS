'''
    SAVE_TENSORS
        - Module for saving binary FUNWAVE output files to numpy/tensorflow
            tensors
'''
from pathlib import Path
import numpy as np
from .utils import get_numbers


def get_MNglob(tri_str: str, In_d):
    '''
    gets Mglob and Nglob for a trial in the larger dictionary In_d
    
    ARGUMENTS:
        - tri_str (string): "tri_XXXXX" where XXXXX is the trial number
        - In_d (dictionary): The In_d dicitionary
    RETURNS:
        - Mglob (int)
        - Nglob (int)

    '''
    key = get_numbers(string=tri_str)['tri']
    Mglob = In_d[key]['Mglob']
    Nglob = In_d[key]['Nglob']
    
    return Mglob, Nglob


def load_array(var_XXXXX: Path, Mglob: int, Nglob: int):
    '''
    Loads in an array from a var_XXXXX binary output file or time_dt.txt
    '''
    # Deal with time_dt.txt separately: This is the only allowable ASCII file
    if var_XXXXX.name == 'time_dt.txt':
        return np.loadtxt(var_XXXXX,dtype=np.float32)
    else:
        return np.fromfile(var_XXXXX, dtype=np.float32).reshape(Nglob,Mglob)
    
    
def load_and_stack_to_tensors(all_var_dict,In_d,tri_str: str):
    '''
    Loads in an all the variable var_XXXXX as specified by the all_var_dict
    that was output from `get_list_var_output_paths` gor a given trial
    
    ARGUMENTS: 
        - all_var_dict (dict): output of `get_list_var_output_paths`
        - In_d (dict): master input dictionary
        - tri (str): string of the form `tri_XXXXX`
        
    RETURNS:
        - tri_tensor_dict (dict[np.array]): dictionary of compressed tensors
            for the trial specified
            
    '''
    
    # Get Mglob and Nglob
    Mglob, Nglob = get_MNglob(tri_str, In_d)
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