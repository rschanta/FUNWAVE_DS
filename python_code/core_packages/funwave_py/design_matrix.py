import pickle
import os
import sys
import pandas as pd
import numpy as np
from itertools import product

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
import python_code as pc


#%% KEY HELPER FUNCTIONS
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


def group_variables(design_matrix):
    print(design_matrix)
    grouped_vars = design_matrix.groupby('VAR',sort=False)
    variable_ranges = {}
    print(grouped_vars)
    for var_name, group in grouped_vars:
        print(group)
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
    print(variable_ranges)
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

def print_supporting(all_vars,ptr):
    # Check for bathymetry and spectra
    if 'files' in all_vars:
        
        # Bathymetry
        if 'bathy' in all_vars['files']:
            path = ptr['b_file']
            data = all_vars['files']['bathy']['file']
            pc.co.py.print_bathy(data,path)

def plot_supporting(all_vars,ptr):
    # Check for bathymetry and spectra
    if 'files' in all_vars:
        
        # Bathymetry
        if 'bathy' in all_vars['files']:
            pc.co.py.plot_bathy(all_vars,ptr)

def save_input_file(var_dict,ptr):
    with open(ptr['i_file'], 'w') as f:
        # Remove files
        if 'files' in var_dict:
            del var_dict['files']
            
        for var_name, value in var_dict.items():
            f.write(f"{var_name} = {value}\n")
    
    print(f"Generated file: {ptr['i_file']}")
    return        
            
#%% MAIN PRINT FILES FUNCTION
def write_files(matrix, function_sets, super_path, run_name, extra_values=None):
    
    all_dicts = {}
    # Group together variables
    variable_ranges = group_variables(matrix)
    
    ## Get paths needed
    variable_ranges['super_path'] = [super_path]
    variable_ranges['run_name'] = [run_name]
    pc.co.py.mk_FW_dir(super_path, run_name)
    p = pc.co.py.list_FW_dirs(super_path, run_name)

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
            
            # Add on a title for the permutation
            var_dict['TITLE'] = f'input_{i:05}'
            var_dict['FUNCTION_SET'] = set_name
            
            # Calculate any parameters dependent on other ones         
            var_dict = add_dependent_values(var_dict,function_set)
            
            ## Writing Out Files
            # Paths for trial files
            ptr = pc.co.py.list_FW_tri_dirs(k, p)
            print(ptr['b_file'])
            # Print supporting files if found (ie- bathy, spectra)
            print_supporting(var_dict,ptr)
                    
            # Plot supporting
            plot_supporting(var_dict,ptr)
            
            # Plot input.txt file
            save_input_file(var_dict,ptr)
    
            # Add to larger dictionary
            all_dicts[f'tri_{k:05}'] = var_dict
            k = k + 1 
        
    # Save larger dictionary
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_dicts, f)
    return all_dicts





