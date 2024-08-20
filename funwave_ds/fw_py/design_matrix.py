import pickle
import os
import sys
import copy
import pandas as pd
import numpy as np
from itertools import product

import funwave_ds.fw_ba as fwb
import funwave_ds.fw_py as fpy

from .path_tools import get_FW_paths, make_FW_paths,get_FW_tri_paths
from .path_tools import get_FW_paths2, make_FW_paths2,get_FW_tri_paths2
from .print_files import print_bathy_file, print_input_file
from .plots import plot_bathy2

#%% FUNCTION
def load_FW_design_matrix(path):
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

import funwave_ds.fw_ba as fba
def load_FW_design_matrix2():

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
            

def add_extra_values(variable_ranges,extra_values):
    for var_name, extra in extra_values.items():
        if var_name in variable_ranges:
            # Ensure extra values are unique and combined with existing values
            #variable_ranges[var_name] = list(set(variable_ranges[var_name] + extra))
            variable_ranges[var_name] = list(dict.fromkeys(variable_ranges[var_name] + extra))
        else:
            # If variable not already in ranges, add it directly
            variable_ranges[var_name] = list(extra)
    return variable_ranges

def add_dependent_values(var_dict,functions_to_apply):
    dependent_vars = {}
    for func in functions_to_apply:
        result = func(var_dict)
        if 'files' in result:
            if 'files' in dependent_vars:
                dependent_vars['files'].update(result['files'])
                var_dict = {**var_dict, **dependent_vars}
            else:
                dependent_vars['files'] = result['files']
                var_dict = {**var_dict, **dependent_vars}
        else:
            dependent_vars.update(result)
            var_dict = {**var_dict, **dependent_vars}
    return var_dict

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



            
#%% MAIN PRINT FILES FUNCTION
def write_files(matrix, function_sets, super_path, run_name, extra_values=None):
    
    all_dicts = {}
    # Group together variables
    variable_ranges = group_variables(matrix)
    
    ## Get paths needed
    variable_ranges['super_path'] = [super_path]
    variable_ranges['run_name'] = [run_name]
    make_FW_paths(super_path, run_name)
    p = get_FW_paths(super_path, run_name)

    # Add on extra values if provided
    if extra_values:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    
    # Get all permutations of variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    k = 1
    for set_name, function_set in function_sets.items():
        # Loop through each permutation
        for i, perm in enumerate(permutations, start=1):
            
            ## Getting the dictionaries
            # Create dictionary of variable/value pairs
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Paths for trial files
            ptr = get_FW_tri_paths(k, p)

            # Add on a title for the permutation
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['FUNCTION_SET'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Calculate any parameters dependent on other ones         
            var_dict = add_dependent_values(var_dict,function_set)
            all_dicts[f'tri_{k:05}'] = var_dict
            
            ## Writing Out Files
            # Print supporting files if found (ie- bathy, spectra)
            #plot_bathy2(var_dict,ptr)
            
            # Plot input.txt file
            print_input_file(var_dict,ptr)
    
            
            k = k + 1 
        
    # Save larger dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    return all_dicts


def write_files2(matrix, 
                function_sets = None, 
                print_sets = None, 
                plot_sets = None, 
                extra_values = {}):
    
    # Get Environment Variables
    d = fba.get_directories()

    all_dicts = {}

    # Group together variables
    variable_ranges = group_variables(matrix)

    ## Get paths needed
    make_FW_paths2()
    p = get_FW_paths2()

    # Add on extra values if provided
    if extra_values:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            

    # Get all permutations of variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    k = 1
    for set_name, pipeline in function_sets.items():
        # Loop through each permutation
        for i, perm in enumerate(permutations, start=1):
            
            ## Getting the dictionaries
            # Create dictionary of variable/value pairs
            var_dict = dict(zip(variable_ranges.keys(), perm))
            
            # Paths for trial files
            ptr = fpy.get_FW_tri_paths(k, p)

            # Add on a title for the permutation
            var_dict['TITLE'] = f'input_{k:05}'
            var_dict['DEP_PARAM_PIPELINE'] = set_name
            var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
            var_dict['ITER'] = k
            
            # Calculate any parameters dependent on other ones         
            var_dict = add_dependent_values(var_dict,pipeline)
            all_dicts[f'tri_{k:05}'] = var_dict
            
            # Plot input.txt file
            print_input_file(var_dict,ptr)
    
            
            k = k + 1 
        
    # Save larger dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    return all_dicts





def write_files3(matrix, 
                print_inputs = True,
                function_sets = None, 
                print_sets = None, 
                plot_sets = None, 
                extra_values = None):
    
    ## Get paths needed
    make_FW_paths2()
    p = get_FW_paths2()

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
            ptr = fpy.get_FW_tri_paths(k, p)

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