import pickle
import shutil
import numpy as np
import pandas as pd
from itertools import product
import xarray as xr

# In-module imports
from .path_tools import get_FW_paths, make_FW_paths,get_FW_tri_paths
from .print_files import print_input_file
from .record import log_function_call, save_logs_to_file
from .utils import convert_to_number
from .netcdf import *

#%% LOAD IN VARIABLES AND GROUP VARIABLES

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
    Find every possible permutation of variables (Cartesian Product) to generate
    the ranges of variables in the ensemble of runs

    Arguments:
    - design_matrix (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting [output of `load_FW_design_matrix`]

    Returns:
    - variable_ranges (Pandas DataFrame): DataFrame of design matrix with valid
        FORTRAN formatting
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
            

#%% ADDING ON VALUES TO THE MATRIX
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

#%% FILTERING OUT CASES
def apply_filters(var_dict,functions_to_apply):
    '''
    Applies the defined filter functions to knock out trials that are not 
    valid.

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of functions defining the filter functions

    Returns:
    - var_dict (df_failed_vars/None): DataFrame of failed variables
    '''

    failed_checks = []  # List to keep track of functions that return False
    failed_vars = {}    # Dictionary to keep track of variables causing the failure
    print(f'\nApplying FILTER functions')

    # Loop through all filter functions
    for func in functions_to_apply:
        print(f'\tApplying FILTER function: {func.__name__}')
        result = func(var_dict)
        
        # Record failure and key data
        if not result:
            print(f'\tFailed FILTER function: {func.__name__}')
            # Record function name and what the iteration would have been
            failed_checks.append(func.__name__)  
            failed_vars['failed_checks'] = func.__name__ 
            failed_vars['ITER'] = var_dict['ITER']

            # Loop through variables
            for k, v in var_dict.items():
                if isinstance(v, (str, int, float)):
                    failed_vars[k] = v

    # Record failures out 
    if failed_checks:
        # Record which functions trigger the failure
        failed_vars['failed_checks'] = ', '.join(failed_checks)
        # Create the dataframe
        df_failed_vars = pd.DataFrame(failed_vars, index=[0])

        return df_failed_vars


    else:
        print("All FILTER functions passed successfully!")
        return None

#%% Print/output files

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




#%% Work through the design matrix
def process_design_matrix(matrix_file, 
                print_inputs = True,
                function_sets = None, 
                filter_sets = None,
                print_sets = None, 
                plot_sets = None, 
                extra_values = None):
    
    '''
    Works through the design matrix process
    '''

    ## SETUP AND INITIALIZE
    # Paths
    make_FW_paths()
    p = get_FW_paths()

    # Initialize structures for summary files
    complete_matrix = []
    all_dicts = {}
    filter_failures = pd.DataFrame()

    ## LOAD IN THE MATRIX
    matrix = load_design_matrix(matrix_file)

    ## FIND PERMUTATIONS OF ALL VARIABLES
    # Get the range of all parameters provided in the matrix
    variable_ranges = group_variables(matrix)

    # Add on extra values if provided
    if extra_values is not None:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    # Get all possible permutations
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    

    ## LOOP THROUGH ALL PERMUTATIONS OF VARIABLES
    k = 1
    # Loop: Processing Pipeline
    for set_name, pipeline in function_sets.items():
        # Loop: Permutation of variables
        for i, perm in enumerate(permutations, start=1):

            print(f'\nSTARTED GENERATING TRIAL: {k:05}')
            
            ## SETUP
            # Create dictionary for parameters and values in permutation
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Get all paths needed
            ptr = get_FW_tri_paths(tri_num=k)

            ## ADD PARAMETERS
            # Add on iteration-dependent values
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['DEP_PARAM_PIPELINE'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Add on dependent parameters        
            var_dict = add_dependent_values(var_dict,pipeline)

            ## APPLY FILTER FUNCTIONS
            failed_params = None
            if filter_sets is not None:
                failed_params = apply_filters(var_dict,filter_sets)

            # Record failure if triggered
            if failed_params is not None:
                filter_failures = pd.concat([filter_failures, failed_params], ignore_index=True, sort=False)
                print(f'PERMUTATION DOES NOT PASS FILTER: SKIP')
            # Proceed otherwise
            elif failed_params is None:

                ## OUTPUT FILES/PLOTS
                # Print supporting files if indicated
                if print_sets is not None:
                    var_dict = print_supporting_file(var_dict,print_sets)

                # Plot supporting plots if indicated
                if plot_sets is not None:
                    plot_supporting_file(var_dict,plot_sets)

                # Print input.txt files if indicated
                if print_inputs == True:
                    print_input_file(var_dict,ptr)

                ## UPDATE SUMMARIES
                # Dictionary for individual trial
                with open(ptr['i_file_pkl'], 'wb') as f:
                    pickle.dump(var_dict, f)

                # Update expanded CSV
                var_dict = {k: v for k, v in var_dict.items() if isinstance(v, (str, int, float))}
                complete_matrix.append(pd.DataFrame([var_dict]))

                # Update the larger summary dictionary, move on to next trial
                all_dicts[f'tri_{k:05}'] = ptr['RESULT_FOLDER']

                # End loop iteration
                print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
                print('#'*40)
                k = k + 1 
                
    ## SAVE SUMMARY FILES
    # Save the big dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    

    ## TODO: Save as NETCDF instead
    # Save the completed matrix
    complete_matrix = pd.concat(complete_matrix, ignore_index=True, sort=False)
    complete_matrix.to_csv(p['Im'], index=False)

    # Save the failure functions (to logs)
    filter_failures.to_csv(f"{p['L']}/failures.txt", index=False)

    # Save record of function calls (to logs)
    save_logs_to_file(f"{p['L']}/generation_function_log.py")
    save_logs_to_file(f"{p['L']}/generation_function_log.txt")

    # Save copy of design matrix (to logs)
    shutil.copy(matrix_file, f"{p['L']}/design_matrix.csv")

    return


#%% Work through the design matrix
def process_design_matrix_NC(matrix_file, 
                print_inputs = True,
                function_sets = None, 
                filter_sets = None,
                print_sets = None, 
                plot_sets = None, 
                extra_values = None):
    
    '''
    Works through the design matrix process
    '''

    ## SETUP AND INITIALIZE
    # Paths
    make_FW_paths()
    p = get_FW_paths()

    # Initialize structures for summary files
    complete_matrix = []
    all_dicts = {}
    filter_failures = pd.DataFrame()

    ## LOAD IN THE MATRIX
    matrix = load_design_matrix(matrix_file)

    ## FIND PERMUTATIONS OF ALL VARIABLES
    # Get the range of all parameters provided in the matrix
    variable_ranges = group_variables(matrix)

    # Add on extra values if provided
    if extra_values is not None:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    # Get all possible permutations
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    

    ## LOOP THROUGH ALL PERMUTATIONS OF VARIABLES
    k = 1
    # Loop: Processing Pipeline
    for set_name, pipeline in function_sets.items():
        # Loop: Permutation of variables
        for i, perm in enumerate(permutations, start=1):

            print(f'\nSTARTED GENERATING TRIAL: {k:05}')
            
            ## SETUP
            # Create dictionary for parameters and values in permutation
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Get all paths needed
            ptr = get_FW_tri_paths(tri_num=k)

            ## ADD PARAMETERS
            # Add on iteration-dependent values
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['DEP_PARAM_PIPELINE'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Add on dependent parameters        
            var_dict = add_dependent_values(var_dict,pipeline)

            ## APPLY FILTER FUNCTIONS
            failed_params = None
            if filter_sets is not None:
                failed_params = apply_filters(var_dict,filter_sets)

            # Record failure if triggered
            if failed_params is not None:
                filter_failures = pd.concat([filter_failures, failed_params], ignore_index=True, sort=False)
                print(f'PERMUTATION DOES NOT PASS FILTER: SKIP')
            
            # Proceed otherwise
            elif failed_params is None:

                


                ## OUTPUT FILES/PLOTS
                # Print supporting files if indicated
                if print_sets is not None:
                    var_dict = print_supporting_file(var_dict,print_sets)

                # Plot supporting plots if indicated
                if plot_sets is not None:
                    plot_supporting_file(var_dict,plot_sets)

                # Print input.txt files if indicated
                if print_inputs == True:
                    print_input_file(var_dict,ptr)


                ## MAKE NETCDF FILE
                ds = xr.Dataset()
                # catch-all dictionary
                dic = {}
                
                # Loop through to assemble everything
                for key, value in var_dict.items():
                    
                    # Deal with the Coordinate Objects
                    if isinstance(value, CoordinateObject):
                        ds = add_coords(value,ds)
                        ds = add_data_vars(value,ds)
                        ds = add_attr_vars(value,ds)
                    
                    # Deal with everything else
                    elif is_valid_netcdf_attribute(value):
                        ds.attrs[key] = value
                        
                    # Else: Is some invalid datatype, will just be merged into the dictionary
                    else:
                        print((f'Warning: `{key}` not a valid type for net-cdf storage,'
                            ' although it will be stored to a pickable dictionary'))
                        dic[key] = value 

                # Dump netcdf to dictionary and add others
                ds_dict = ds.to_dict()
                ds_dict['NON_CDF'] = dic


                ## UPDATE SUMMARIES
                # Dictionary for individual trial
                with open(ptr['i_file_pkl'], 'wb') as f:
                    pickle.dump(ds_dict['attrs'], f)

                # Update expanded CSV
                ds_dict['attrs'] = {k: v for k, v in var_dict.items() if isinstance(v, (str, int, float))}
                complete_matrix.append(pd.DataFrame([var_dict]))                

                # Update the larger summary dictionary, move on to next trial
                all_dicts[f'tri_{k:05}'] = ptr['RESULT_FOLDER']

                # End loop iteration
                print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
                print('#'*40)
                k = k + 1 
                
    ## SAVE SUMMARY FILES
    # Save the big dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    
    # Save the completed matrix
    complete_matrix = pd.concat(complete_matrix, ignore_index=True, sort=False)
    complete_matrix.to_csv(p['Im'], index=False)

    # Save the failure functions (to logs)
    filter_failures.to_csv(f"{p['L']}/failures.txt", index=False)

    # Save record of function calls (to logs)
    save_logs_to_file(f"{p['L']}/generation_function_log.py")
    save_logs_to_file(f"{p['L']}/generation_function_log.txt")

    # Save copy of design matrix (to logs)
    shutil.copy(matrix_file, f"{p['L']}/design_matrix.csv")

    return