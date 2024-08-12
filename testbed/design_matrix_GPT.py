import pandas as pd
import numpy as np
from itertools import product
import numpy as np
from scipy.optimize import fsolve


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


# Modify the write_files function
def write_files(matrix, functions_to_apply, super_path, run_name):
    
    # List to store ranges or constants for each variable
    variable_ranges = []

    # Store variable names for easier lookup
    variable_names = matrix['VAR'].tolist()

    # Process each row to determine the values to use
    for _, row in matrix.iterrows():
        
        # Set constant value
        if pd.notna(row['CON']):
            variable_ranges.append([row['CON']])
        else:
            values = np.linspace(row['LO'], row['HI'], int(row['NUM']))
            variable_ranges.append(values)

    # Get all permutations of variables
    permutations = list(product(*variable_ranges))

    # Go through each permutation
    for i, perm in enumerate(permutations):
        
        # Dictionary of variable/value pairs
        var_dict = dict(zip(variable_names, perm))
        
        # Add on input name
        var_dict['TITLE'] = f'input_{i:05}'

        # Apply dependent functions
        dependent_vars = {}
        for func in functions_to_apply:
            result = func(var_dict)
            dependent_vars.update(result)
        
        # Merge with original variables
        all_vars = {**var_dict, **dependent_vars}

        # Print to file
        filename = f"input{i:05}.txt"
        with open(filename, 'w') as f:
            for var_name, value in all_vars.items():
                f.write(f"{var_name} = {value}\n")
        print(f"Generated file: {filename}")


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
    

matrix = pd.read_csv('matrix3.csv', na_values=[''])
matrix['CON'] = matrix['CON'].apply(convert_to_number)
# Define functions to apply as a list
functions_to_apply = [stability_vars]
write_files(matrix, functions_to_apply, '', '')

