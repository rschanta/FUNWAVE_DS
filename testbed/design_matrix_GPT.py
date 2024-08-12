import pandas as pd
import numpy as np
from itertools import product
import numpy as np
from scipy.optimize import fsolve

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

#%% Standard Variables
def compute_D(vars):
    A = vars['A']
    B = vars['B']
    return A * B

## Calculate stability for regular waves
def compute_E(vars):
    # Pull out period and offshore depth
    T = vars['Tperiod']
    h = vars['DEPTH_FLAT']
    
    # Solve the linear dispersion relation
    k, L = dispersion(T, h)
    
    # Use Torres et al (2022) stability relation
    
    
    # solve the linear dispersion relation
    
    return A ** 2

# Mapping functions to variable names
functions_to_apply = {
    'D': compute_D,
    'E': compute_E,
}


#%% Loop through table
def write_files(matrix, functions_to_apply,super_path,run_name):
    
    # List to store ranges or constants for each variable
    variable_ranges = []

    # Store variable names for easier lookup
    variable_names = matrix['VAR'].tolist()

    # Process each row to determine the values to use
    for _, row in matrix.iterrows():
        
        # Set constant value
        if pd.notna(row['CON']):
            # Check constant value
            variable_ranges.append([row['CON']])
        # Set range of values
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
        dependent_vars = {key: func(var_dict) for key, func in functions_to_apply.items()}
        
        # Merge with original variables
        all_vars = {**var_dict, **dependent_vars}

        # Print to file
        filename = f"input{i:05}.txt"
        with open(filename, 'w') as f:
            for var_name, value in all_vars.items():
                f.write(f"{var_name} = {value}\n")
        print(f"Generated file: {filename}")

# Example DataFrame
matrix = pd.DataFrame({
    'VAR': ['A', 'B', 'C'],
    'CON': [10, None, None],  # Use None for variables with ranges
    'LO': [None, 1, 5],
    'HI': [None, 10, 15],
    'NUM': [None, 5, 3]  # Number of points for linspace
})

# Define functions to apply
functions_to_apply = {
    'D': compute_D,
    'E': compute_E,
}

generate_permutations(matrix, functions_to_apply)
