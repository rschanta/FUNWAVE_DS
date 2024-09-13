import pickle
import os
import sys
import copy
import pandas as pd
import numpy as np
from itertools import product

import funwave_ds.fw_ba as fwb
import funwave_ds.fw_py as fpy

from .path_tools import get_FW_tri_paths
from .path_tools import get_FW_paths, make_FW_paths,get_FW_tri_paths
from .print_files import print_bathy_file, print_input_file
from .plots import plot_bathy2

#%% FUNCTION
import funwave_ds.fw_ba as fba

#%% Loading and grouping variables
def load_FW_design_matrix():

    d = fba.get_directories()

    path = os.path.join(d['WORK_DIR'], 
                        'fw_models', 
                        d['FW_MODEL'], 
                        'design_matrices', 
                        f"{d['RUN_NAME']}.csv")

    design_matrix = pd.read_csv(path, na_values=[''])
    
    # Helper function to convert to valid FORTRAN
    def convert_to_number(value):
        try:
            # Try conversion to float (will work for ints/floats)
            float_value = float(value)
            
            # Case to return float: if a decimal point is provided
            if '.' in str(value).strip():
                return float_value
            # Case to return int: if no decimal point is provided
            else: 
                return int(float_value)
            
        # Case to return string: if conversion to float fails
        except ValueError:
            return value
        
    # Apply to constant column
    design_matrix['CON'] = design_matrix['CON'].apply(convert_to_number)

    return design_matrix

def load_FW_design_matrix2(matrix):
    
    design_matrix = pd.read_csv(matrix, na_values=[''])
    # Helper function to convert to valid FORTRAN
    def convert_to_number(value):
        try:
            # Try conversion to float (will work for ints/floats)
            float_value = float(value)
            
            # Case to return float: if a decimal point is provided
            if '.' in str(value).strip():
                return float_value
            # Case to return int: if no decimal point is provided
            else: 
                return int(float_value)
            
        # Case to return string: if conversion to float fails
        except ValueError:
            return value
        
    # Apply to constant column
    design_matrix['CON'] = design_matrix['CON'].apply(convert_to_number)

    return design_matrix


def group_variables(design_matrix):
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
            
###########################################################
# Adding parameters to the matrix
###########################################################
# Adding Values: Extra and Dependent
def add_extra_values(variable_ranges,extra_values):
    for var_name, extra in extra_values.items():
        if var_name in variable_ranges:
            # Ensure extra values are unique and combined with existing values
            variable_ranges[var_name] = list(dict.fromkeys(variable_ranges[var_name] + extra))
        else:
            # If variable not already in ranges, add it directly
            variable_ranges[var_name] = list(extra)
    return variable_ranges


# Dependent Parameters
def add_dependent_values(var_dict,functions_to_apply):
    dependent_vars = {}
    for func in functions_to_apply:
        print(f'\tApplying DEPENDENCY function: {func.__name__}')
        result = func(var_dict)
        dependent_vars.update(result)
        var_dict = {**var_dict, **dependent_vars}
    return var_dict

###########################################################
# Filter functions
###########################################################
def apply_filters(var_dict,functions_to_apply):

    failed_checks = []  # List to keep track of functions that return False
    failed_vars = {}    # Dictionary to keep track of variables causing the failure

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
        print("\tAll filter functions passed successfully!")
        return None

###########################################################
# Print/Output files
###########################################################
def print_supporting_file(var_dict,functions_to_apply):
    print_path_vars = {}
    for func in functions_to_apply:
        print(f'\tApplying PRINT function: {func.__name__}')
        print_paths = func(var_dict)
        # Merge path variables back into input
        print_path_vars.update(print_paths)
        var_dict = {**var_dict, **print_path_vars}
    return var_dict


def plot_supporting_file(var_dict,functions_to_apply):
    for func in functions_to_apply:
        print(f'\tApplying PLOT function: {func.__name__}')
        func(var_dict)
    return


###########################################################
# Write files
###########################################################
#%% Writing out the files: La pièce de résistance
def write_files(matrix, 
                print_inputs = True,
                function_sets = None, 
                print_sets = None, 
                plot_sets = None, 
                extra_values = None):
    
    ## Get paths needed
    make_FW_paths()
    p = get_FW_paths()

    # Initialize large dictionary
    all_dicts = {}

    # Get the range of all parameters provided in the matrix
    variable_ranges = group_variables(matrix)

    # Add on extra values if provided
    if extra_values is not None:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    # Get all permutations of input variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    k = 1
    # Loop through each pipeline in the function set
    for set_name, pipeline in function_sets.items():

        # Loop through each permutation of variables in the design matrix
        for i, perm in enumerate(permutations, start=1):
            print(f'\nSTARTED PRINTING FILES FOR TRIAL: {k:05}')
            ## Getting the dictionaries
            # Create dictionary of variable/value pairs
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Paths for trial files
            ptr = fpy.get_FW_tri_paths(tri_num=k)

            # Add on iteration-dependent values
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['DEP_PARAM_PIPELINE'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Add on dependent parameters        
            var_dict = add_dependent_values(var_dict,pipeline)
    
            # Print supporting files if given
            if print_sets is not None:
                var_dict = print_supporting_file(var_dict,print_sets)

            # Plot supporting plots if given
            if plot_sets is not None:
                plot_supporting_file(var_dict,plot_sets)

            # Print input.txt files if indicated
            if print_inputs == True:
                print_input_file(var_dict,ptr)

            # Update the larger summary dictionary, move on to next trial
            all_dicts[f'tri_{k:05}'] = var_dict
            print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
            k = k + 1 
        
    # Save larger dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    return all_dicts




def write_files2(matrix, 
                print_inputs = True,
                function_sets = None, 
                filter_sets = None,
                print_sets = None, 
                plot_sets = None, 
                extra_values = None):
    
    ###########################################################
    # Setup
    ###########################################################
    # Get paths needed
    make_FW_paths()
    p = get_FW_paths()

    # Initialize structures for summary files
    complete_matrix = []
    all_dicts = {}
    filter_failures = pd.DataFrame()

    ###########################################################
    # Finding permutations of all variables
    ###########################################################
    # Get the range of all parameters provided in the matrix
    variable_ranges = group_variables(matrix)

    # Add on extra values if provided
    if extra_values is not None:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    # Get all possible permutations
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    ###########################################################
    # Looping through all permutations
    ###########################################################
    k = 1
    # Loop: Processing Pipeline
    for set_name, pipeline in function_sets.items():
        # Loop: Permutation of variables
        for i, perm in enumerate(permutations, start=1):

            print(f'\nSTARTED GENERATING TRIAL: {k:05}')
            
            ###########################################################
            # Setup
            ###########################################################
            # Create dictionary for parameters and values in permutation
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Get all paths needed
            ptr = fpy.get_FW_tri_paths(tri_num=k)

            ###########################################################
            # Add parameters
            ###########################################################
            # Add on iteration-dependent values
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['DEP_PARAM_PIPELINE'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Add on dependent parameters        
            var_dict = add_dependent_values(var_dict,pipeline)

            ###########################################################
            # Apply filter functions, proceed if none fail
            ###########################################################
            failed_params = None
            if filter_sets is not None:
                failed_params = apply_filters(var_dict,filter_sets)

            # Record failure if triggered
            if failed_params is not None:
                filter_failures = pd.concat([filter_failures, failed_params], ignore_index=True, sort=False)
                print(f'PERMUTATION DOES NOT PASS FILTER: SKIP')
            # Proceed otherwise
            elif failed_params is None:
                ###########################################################
                # Output files and plots
                ###########################################################
                # Print supporting files if indicated
                if print_sets is not None:
                    var_dict = print_supporting_file(var_dict,print_sets)

                # Plot supporting plots if indicated
                if plot_sets is not None:
                    plot_supporting_file(var_dict,plot_sets)

                # Print input.txt files if indicated
                if print_inputs == True:
                    print_input_file(var_dict,ptr)

                ###########################################################
                # Update summaries
                ###########################################################
                # Dictionary for individual trial
                with open(ptr['i_file_pkl'], 'wb') as f:
                    pickle.dump(var_dict, f)

                # Update expanded CSV
                var_dict = {k: v for k, v in var_dict.items() if isinstance(v, (str, int, float))}
                complete_matrix.append(pd.DataFrame([var_dict]))

                # Update the larger summary dictionary, move on to next trial
                all_dicts[f'tri_{k:05}'] = ptr['RESULT_FOLDER']

                ###########################################################
                print(f'SUCCESSFULLY PRINTED FILES FOR TRIAL: {k:05}')
                k = k + 1 
                
    ###########################################################
    # Save summary files
    ########################################################### 
    # Big dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    
    # Completed matrix
    complete_matrix = pd.concat(complete_matrix, ignore_index=True, sort=False)
    complete_matrix.to_csv(p['Im'], index=False)

    # Failure functions
    filter_failures.to_csv(p['If'], index=False)

    return