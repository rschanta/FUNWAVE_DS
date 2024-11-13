
import pickle
import shutil
import numpy as np
import pandas as pd
from itertools import product
import xarray as xr

## NOTE: These must be here for compatibility reasons
from netCDF4 import Dataset
import h5py


def print_supporting_file(var_dict,functions_to_apply):
    '''
    Applies the functions of print functions for supporting files

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of print functions

    Returns:

    '''

    print_path_vars = {}
    print(f'\nApplying PRINT functions')
    for func in functions_to_apply:
        print(f'\tApplying PRINT function: {func.__name__}')
        print_paths = func(var_dict)
        # Merge path variables back into input
        print_path_vars.update(print_paths)
        var_dict = {**var_dict, **print_path_vars}
    print(f'All PRINT functions completed successfully!')
    return var_dict

def plot_supporting_file(var_dict,functions_to_apply):
    '''
    Applies the functions of plot functions for supporting files

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of plot functions

    Returns:
    - var_dict (df_failed_vars/None): DataFrame of failed variables
    '''

    print(f'\nApplying PLOT functions')
    for func in functions_to_apply:
        print(f'\tApplying PLOT function: {func.__name__}')
        func(var_dict)
    print(f'All PLOT functions completed successfully!')
    
    return