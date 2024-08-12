import pandas as pd
import numpy as np
from itertools import product
import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import pickle

#%% Linear Dispersion Relation
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

#%% Dependent Variable functions

    
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

def print_bathy(data, path):

    print('Started printing Bathymetry file...')
    np.savetxt(path, data, delimiter=' ', fmt='%f')
    print(f'Bathymetry file successfully saved to: {path}')
    
    return

def print_supporting(all_vars,i):
    # Get super_path and run_name for naming
    super_path = all_vars['super_path']
    run_name = all_vars['run_name']
    
    # Check for bathymetry and spectra
    if 'files' in all_vars:
        
        # Bathymetry
        if 'bathy' in all_vars['files']:
            path = f'{super_path}/{run_name}/bathy_{i:05}.txt'
            data = all_vars['files']['bathy']['file']
            print_bathy(data,path)

#%% WRITE FILES FUNCTION
def write_files(matrix, functions_to_apply, super_path, run_name, extra_values=None):
    
    # Find all "groups" of variables
    grouped_vars = matrix.groupby('VAR')
    
    # Dictionary of variable parameters
    variable_ranges = {}
    
    # Loop through each variable group
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
            
    # Add on super_path and run_name
    variable_ranges['super_path'] = [super_path]
    variable_ranges['run_name'] = [run_name]

    # Incorporate extra values if provided
    if extra_values:
        for var_name, extra in extra_values.items():
            if var_name in variable_ranges:
                # Ensure extra values are unique and combined with existing values
                variable_ranges[var_name] = sorted(set(variable_ranges[var_name] + extra))
            else:
                # If variable not already in ranges, add it directly
                variable_ranges[var_name] = sorted(extra)
    
    # Get all permutations of variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))
    
    # Get all permutations of variables
    permutations = list(product(*[variable_ranges[var] for var in variable_ranges]))



    # Process each permutation
    for i, perm in enumerate(permutations):
        
        # Create dictionary of variable/value pairs
        var_dict = dict(zip(variable_ranges.keys(), perm))
        
        # Add on input name
        var_dict['TITLE'] = f'input_{i:05}'

        # Apply dependent functions
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
        
        # Print supporting files if found
        print_supporting(var_dict,i)
        
                
        # Print to input.txt
        filename = f"{super_path}/{run_name}/input{i:05}.txt"
        with open(filename, 'w') as f:
            for var_name, value in var_dict.items():
                f.write(f"{var_name} = {value}\n")
            
        
        print(f"Generated file: {filename}")


#%% CONVERT TO NUMBER FUNCTION
def convert_to_number(value):
    try:
        # Convert to float to check if it can be a number
        float_value = float(value)
        # Convert float_value back to string to check if it contains a decimal
        value_str = str(value).strip()
        if '.' in value_str:
            # If the original string had a decimal point, keep it as a float
            return float_value
        return int(float_value)
    except ValueError:
        # Return the original value if it's not a number
        return value
extra_values = {
     'DEPTH_FILE': ['foo', 'fee']  # Extra values for CFL
 }

def get_bathy(vars):
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
    DX = vars['DX']
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
    
    bathy_dict = {'bathy2': bathy_out}
    
    return {'files': bathy_dict} 

#%% Where stuff actually happens
# Read in CSV
matrix = pd.read_csv('matrix3.csv', na_values=[''])
# Convert to numbers
matrix['CON'] = matrix['CON'].apply(convert_to_number)

# Define functions to apply as a list
functions_to_apply = [stability_vars,get_bathy,get_bathy2]
# Define any extra values we need
extra_values = {'bathy_path': ['Trial05.pkl','Trial06.pkl']}
# Write the files
write_files(matrix, functions_to_apply, 'superr', 'runn',extra_values)
#%%



