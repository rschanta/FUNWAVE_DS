import numpy as np
import pandas as pd
from itertools import product
import xarray as xr

## NOTE: These must be here for compatibility reasons
from netCDF4 import Dataset
import h5py

#%% SUMMARY FILES FROM GENERATION
def make_pass_parquet(summary_data,p):
    '''
    Summarizes all the attribute data for the ensemble of runs that passed
    through the filters, including all strings, integers, booleans, and 
    floats after all processing pipelines have been applied.
    '''
    dataframes = []
    
    # Loops through objects in a var_dict
    for key, nc_data in summary_data.items():
        # Create a DataFrame row from the attributes
        df = pd.DataFrame(nc_data.attrs, index=[0])
        dataframes.append(df)
    
    ## Merge all dataframes, filling in columns that don't exist with NaNs
    merged_df = pd.concat(dataframes, axis=0, join="outer", ignore_index=True)
    merged_df.to_parquet(p['I_pass'], index=False)

    return merged_df

def make_fail_parquet(fail_data,p):
    '''
    Summarizes all the failed runs, should they exist
    '''
    if fail_data:
        merged_df = pd.concat(fail_data.values(), ignore_index=True)
        merged_df.to_parquet(p['I_fail'], index=False)
        return merged_df
    

#%% PRINTING AND PLOTTING
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