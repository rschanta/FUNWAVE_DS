import pandas as pd
import numpy as np
from itertools import product
import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import pickle
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
import python_code as fp
#import tensorflow as tf



#%% GENERAL UTILITY
def dispersion(T, h):
    sigma = 2 * np.pi / T
    g = 9.81

    # Define the function for fsolve
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)

    # Find the root of the equation numerically
    k = fsolve(disp_relation, 0)[0]
    L = 2 * np.pi / k

    return k, L

def print_bathy(data, path):

    print('Started printing Bathymetry file...')
    np.savetxt(path, data, delimiter=' ', fmt='%f')
    print(f'Bathymetry file successfully saved to: {path}')
    
    return

#%% RUN SPECIFIC FUNCTIONS

    
## Calculate stability for regular waves
def stability_vars(vars):
    # Unpack vars needed
    T = vars['Tperiod']
    h = vars['DEPTH_FLAT']
    k, L = dispersion(T, h)
    
    # Use Torres stability limits for DX/DY amd Sponge
    DX_lo = h/15;
    DX_hi = L/60;
    DX = np.mean([DX_hi,DX_lo]);
    DY = DX
    Sponge_west_width = 2*L
    
    
    # Returning multiple variables and bonus variables
    return {'k_': k, 
            'L_': L,
            'DX': DX,
            'DY': DY,
            'Sponge_west_width': Sponge_west_width}

def get_bathy2(vars):
    data_path = vars['bathy_path']
    with open(data_path, 'rb') as file:
        bathy_raw = pickle.load(file)
        
    # Get variables needed
    bathy = bathy_raw['filtered_data']['bed_num_before']
    WG_x = bathy_raw['raw_data']['WG_loc_x']
    MWL = bathy_raw['raw_data']['MWL']
    bathyX = bathy[:,0]
    bathyh = bathy[:,1]
    
    L = 10
    DX = 0.35
    # Add propagation room
    bathyX = bathyX + 3*L
    bathyX = np.insert(bathyX, 0, 0)
    bathyh = np.insert(bathyh, 0, bathyh[0])
    
    # Convert to depth values
    MWL_mean = np.nanmean(MWL)
    Z_raw = MWL_mean - bathyh
    
    # Interpolate values
    X_out = np.arange(0, np.max(bathyX)+0.1, DX)
    f = interp1d(bathyX, Z_raw, kind='linear', fill_value="extrapolate")
    Z_out = f(X_out)
    
    # Arrange outputs
    bathy_out = {}
    bathy_out['array'] = np.stack((X_out, Z_out), axis=1)
    bathy_out['file'] = np.stack((Z_out,Z_out,Z_out),axis=0)
    bathy_out['WG_x'] = WG_x
    
    bathy_dict = {'bathy': bathy_out}
    
    return {'files': bathy_dict} 


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
    grouped_vars = matrix.groupby('VAR')
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
            variable_ranges[var_name] = sorted(set(values))  # Remove duplicates and sort
            
    return variable_ranges     
            

def add_extra_values(variable_ranges,extra_values):
    for var_name, extra in extra_values.items():
        if var_name in variable_ranges:
            # Ensure extra values are unique and combined with existing values
            variable_ranges[var_name] = sorted(set(variable_ranges[var_name] + extra))
        else:
            # If variable not already in ranges, add it directly
            variable_ranges[var_name] = sorted(extra)
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
    # Get super_path and run_name for naming
    super_path = all_vars['super_path']
    run_name = all_vars['run_name']
    
    # Check for bathymetry and spectra
    if 'files' in all_vars:
        
        # Bathymetry
        if 'bathy' in all_vars['files']:
            path = ptr['b_file']
            data = all_vars['files']['bathy']['file']
            print_bathy(data,path)
            
            
#%% WRITE FILES FUNCTION
def write_files(matrix, functions_to_apply, super_path, run_name, extra_values=None):
    
    all_dicts = {}
    # Group together variables
    variable_ranges = group_variables(matrix)
    
    ## Get paths needed
    variable_ranges['super_path'] = [super_path]
    variable_ranges['run_name'] = [run_name]
    p = fp.py.list_FW_dirs(super_path, run_name)
    print(p)
    # Add on extra values if provided
    if extra_values:
        variable_ranges = add_extra_values(variable_ranges,extra_values)
            
    
    # Get all permutations of variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    # Loop through each permutation
    for i, perm in enumerate(permutations, start=1):
        
        # Create dictionary of variable/value pairs
        var_dict = dict(zip(variable_ranges.keys(), perm))
        # Add on a title for the permutation
        var_dict['TITLE'] = f'input_{i:05}'
        # Calculate any parameters dependent on other ones         
        var_dict = add_dependent_values(var_dict,functions_to_apply)
        
        
        # Paths for trial files
        ptr = fp.py.list_FW_tri_dirs(i, p)
        
        # Print supporting files if found (ie- bathy, spectra)
        print_supporting(var_dict,ptr)
                
        # Print input.txt file
        with open(ptr['i_file'], 'w') as f:
            # Remove files
            if 'files' in var_dict:
                del var_dict['files']
                
            for var_name, value in var_dict.items():
                f.write(f"{var_name} = {value}\n")
            
        
        print(f"Generated file: {ptr['i_file']}")
        
        # Add to larger dictionary
        all_dicts[f'tri_{i:05}'] = var_dict
        
    # Save larger dictionary
        
    return all_dicts



#%% Where stuff actually happens
matrix = load_FW_design_matrix('matrix3.csv')
functions_to_apply = [stability_vars,get_bathy2]
extra_values = {'bathy_path': ['Trial05.pkl','Trial06.pkl']}
fp.py.mk_FW_dir('superr', 'runn')
dicta = write_files(matrix, functions_to_apply, 'superr', 'runn',extra_values)

foo = fp.py.list_FW_dirs('superr', 'runn')


