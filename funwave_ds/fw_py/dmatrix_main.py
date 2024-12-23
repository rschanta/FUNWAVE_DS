import pickle
import shutil
import numpy as np
import pandas as pd
from itertools import product
import xarray as xr

## NOTE: These must be here for compatibility reasons
from netCDF4 import Dataset
import h5py

# In-module imports
from .config_paths import get_FW_paths, make_FW_paths,get_FW_tri_paths
from .utils_general import print_input_file
from .config_record import log_function_call, save_logs_to_file
from .utils_general import convert_to_number
from .dmatrix_filter import apply_filter_set
from .dmatrix_pipeline import print_supporting_file, plot_supporting_file
from .nc_io import get_net_cdf

#%% LOADING DESIGN MATRIX 
'''
    The functions in this section are used to load in the 
    design matrix and get all the possible combination of 
    variables in the test ensemble.
'''

def load_design_matrix(matrix):
    '''
    Load in a design matrix from a .csv file, ensuring valid formatting

    Arguments:
    - matrix (string): Path to the design matrix csv file

    Returns:
    - design_matrix (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting
    '''

    # Load in Design Matric from CSV file
    design_matrix = pd.read_csv(matrix, na_values=[''])

    # Convert to valid FORTRAN formatting of numbers
    design_matrix['CON'] = design_matrix['CON'].apply(convert_to_number)

    return design_matrix

def group_variables(design_matrix):
    '''
    Find all of the variables represented in the design matrix

    Arguments:
    - design_matrix (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting [output of `load_FW_design_matrix`]

    Returns:
    - variable_ranges (Dictionary): 
        - key: name of variable
        - value: list of values it assumed
    '''

    grouped_vars = design_matrix.groupby('VAR',sort=False)
    variable_ranges = {}
    for var_name, group in grouped_vars:

        # Case 1: there are multiple rows for a variable (ie- CFL = 0.5, CFL = 0.3)
        if pd.notna(group['CON']).all():  
            variable_ranges[var_name] = group['CON'].tolist()

        # Case 2: there is only one row specified for a variable
        else:
            # List of value(s) for the variable
            values = []
            for _, row in group.iterrows():
                # Case 2a: single constant parameter
                if pd.notna(row['CON']):
                    values.append(row['CON'])
                # Case 2b: range of parameters specified by LO, HI, NUM
                else:
                    values.extend(np.linspace(row['LO'], row['HI'], int(row['NUM'])))
            #variable_ranges[var_name] = list(set(values))  # Remove duplicates and sort
            variable_ranges[var_name] = list(dict.fromkeys(values))
    return variable_ranges     
            
def get_variable_permutations(matrix_file):
    '''
    Find all possible permutations (the cartesidan product) of the input
    variables in the design matrix

    Arguments:
    - matrix_file (string): path to the design matrix csv

    Returns:
    - variable_ranges (Dictionary): 
        - key: names of variable
        - permutations: all possible permutations
    '''

    matrix = load_design_matrix(matrix_file)   # Pandas dataframe
    variable_ranges = group_variables(matrix)  # Dictionary of lists

    # List of lists (all possible combinations)
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))    

    return variable_ranges,permutations

#%% ADDING VALUES
'''
The functions in this section are used to add values to FUNWAVE
and calculate other information needed for a trial.
'''
def add_extra_values(variable_ranges,extra_values):
    '''
    Add on extra variables to the design matrix

    Arguments:
    - variable_ranges (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting [output of `group_variables`]
    - extra_values (dictionary): dicitionary of variables to add

    Returns:
    - variable_ranges (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting, extra values added
    '''

    for var_name, extra in extra_values.items():
        if var_name in variable_ranges:
            # Ensure extra values are unique and combined with existing values
            variable_ranges[var_name] = list(dict.fromkeys(variable_ranges[var_name] + extra))
        else:
            # If variable not already in ranges, add it directly
            variable_ranges[var_name] = list(extra)
    return variable_ranges

def add_dependent_values(var_dict,functions_to_apply):
    '''
    Add on dependeny parameters defined by some dependency pipeline

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of functions defining the pipeline

    Returns:
    - df_failed_vars (dictionary): dictionary of FUNWAVE parameters, with dependent
        parameters added
    '''

    dependent_vars = {}
    print(f'\nApplying DEPENDENCY functions')
    for func in functions_to_apply:
        print(f'\tApplying DEPENDENCY function: {func.__name__}')
        # Add to log
        decorated_func = log_function_call(func)
        result = decorated_func(var_dict)
        # Update
        dependent_vars.update(result)
        var_dict = {**var_dict, **dependent_vars}
    print(f'All DEPENDENCY functions completed successfully!')
    return var_dict

def add_required_params(var_dict,k,set_name,ptr):
    var_dict['TITLE'] = f'input_{k:05}'                     # Title is iteration number
    var_dict['DEP_PARAM_PIPELINE'] = set_name               # Name of the pipeline used
    var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']        # RESULT_FOLDER for FUNWAVE
    var_dict['ITER'] = k                                    # Iteration number
    return var_dict


#%% SUMMARY FILES
def get_pandas_df(summary_data,p):
        dataframes = []

        for key, value in summary_data.items():
            nc_data = value
            
            # Create a DataFrame from the data part of the tuple
            df = pd.DataFrame(nc_data.attrs, index=[0])
            dataframes.append(df)
        
        ## Merge all dataframes, filling in columns that don't exist with NaNs
        merged_df = pd.concat(dataframes, axis=0, join="outer", ignore_index=True)
        merged_df.to_csv(p['Im'], index=False)

        return merged_df



#%% PROCESS THE DESIGN MATRIX
def process_design_matrix_NC2(matrix_file, 
                print_inputs = True,
                function_sets = None, 
                filter_sets = None,
                print_sets = None, 
                plot_sets = None):
    
    '''
    Works through the design matrix process
    '''

    ## Paths needed
    make_FW_paths()
    p = get_FW_paths()

    # Initialization of data structures
    summary_data = {}

    
    ## Load in design matrix and parse variables
    variable_ranges,permutations = get_variable_permutations(matrix_file)
    
    #------------------------ Beginning of Loop-----------------------------#   
    ## Loop through all possible permutations and pipelines
    k = 1
    
    # Loop 1: Account for different processing pipelines
    for set_name, pipeline in function_sets.items():

        # Loop 2: Loop through every possible permutation of values
        for i, perm in enumerate(permutations, start=1):
            try:
                print(f'\nSTARTED GENERATING TRIAL: {k:05}',flush=True)
                ptr = get_FW_tri_paths(tri_num=k)                           # Paths needed

                # Dictionary of parameters (keys) and values (values) for this trial
                var_dict = dict(zip(variable_ranges.keys(), perm))
            
                ## Add on parameters
                var_dict = add_required_params(var_dict,k,set_name,ptr)     # Required parameters
                var_dict = add_dependent_values(var_dict,pipeline)          # Dependent parameters based on pipeline   

                ## Filtering conditions
                failed_params = apply_filter_set(var_dict,filter_sets)      # Apply filter sets
                if failed_params:
                    pass # TODO: implement failure condition
            
                ## No failures: proceed to output
                elif failed_params is None:    

                    ## Create other files and plots needed
                    # Files other than input.txt    
                    if print_sets:                                                                                    
                        var_dict = print_supporting_file(var_dict,print_sets)
                    # Plots to generate
                    if plot_sets:                                               
                        plot_supporting_file(var_dict,plot_sets)

                    ## Storing for summaries
                    data_proc,non_cdf_stuff = get_net_cdf(var_dict,ptr)       # Split data into netCDF-able and non-netCDF-able 
                    summary_data = {f'trial_{k:05}': data_proc}

                    ## Print `input.txt` for this given trial
                    if print_inputs:
                        print_input_file(data_proc.attrs,ptr)

                    ## End loop iteration
                    print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
                    print('#'*40)
                    k = k + 1
            except:
                print(f'Problem with Trial {k}')
                k = k + 1 
    #------------------------ End of Loop------------------------------#      
      
    ## Final Actions
    get_pandas_df(summary_data,p)     # DataFrame of scalar inputs
    
    ## Logs
    # Save the failure functions (to logs)
    # TODO: Filter tracking

    # Save record of function calls (to logs)
    save_logs_to_file(f"{p['L']}/generation_function_log.py")
    save_logs_to_file(f"{p['L']}/generation_function_log.txt")

    # Save copy of design matrix (to logs)
    shutil.copy(matrix_file, f"{p['L']}/design_matrix.csv")

    return
