
import pandas as pd
import sys
from itertools import product

# In-module imports
from ..utils import convert_to_number
from ..design_matrix import ranged_variables, nonranged_variables,combine_all_vars

#%% LOADING DESIGN MATRIX AND GROUPING
## Warnings and datachecking of design matrix
def process_dataframe(df):
    '''
    Looks through a loaded in design matrix to ensure that no definitions
    are ambiguous

    Arguments:
    - df (Pandas DataFrame): read-in from the csv of the design matrix

    Returns:
    - df: same as input if passes through
    - exits python otherwise
    '''
    warnings = []

    # Condition 1: ('CON' is not nan) and ('LO', 'HI', or 'NUM' are not nan)
    condition1 = (~df['CON'].isna()) & (~df[['LO', 'HI', 'NUM']].isna().all(axis=1))
    warnings.append((df[condition1], "Error: Variable must be either ranged or constant, not both!"))
    df = df[~condition1]  # Discard these rows


    # Condition 2: 'CON' is nan, but any of 'LO', 'HI', or 'NUM' is nan
    condition2 = (df['CON'].isna()) & (df[['LO', 'HI', 'NUM']].isna().any(axis=1))
    warnings.append((df[condition2], "Error: Ranged variable has invalid ranges"))
    df = df[~condition2]  # Discard these rows

    any_warnings = False
    for rows, message in warnings:
        if not rows.empty:
            any_warnings = True
            print(f"Error: {message}")
            print(rows, end="\n\n")

    if any_warnings:
        sys.exit(1)
    else:
        print("SUCCESS: Design matrix has valid ranges/values for all parameters")

    return df

## Loading the design matrix and ensuring proper formatting
def read_design_matrix(matrix_file):
    '''
    Reads in the design matrix from a CSV file, checks its validity, and
    converts everything to numbers as needed.
    '''
    df = pd.read_csv(matrix_file)
    df = process_dataframe(df)
    df['CON'] = df['CON'].apply(convert_to_number)
    return df


def load_group_matrix(matrix_file,function_sets,p):
    '''
    Loads in the design matrix, checks formatting, and finds all 
    permutations of the different variables in the design matrix csv file

    Arguments:
    - matrix_file (str): path to design matrix CSV
    - function_sets (Dict): dictionary defining a valid function set

    Returns:
    - df_permutations (Pandas DataFrame): Pandas dataframe of all of the 
        possible permutations in the design matrix
    '''
    
    # Read in design matrix, ensure formatting, raise warnings
    df = read_design_matrix(matrix_file)
    
    # Get ranged/nonranged parameters sorted out
    di_ranged = ranged_variables(df)
    di_nonranged = nonranged_variables(df)
    
    # Merge, and add in function sets
    di_params = combine_all_vars(di_ranged,di_nonranged,function_sets)
    
    # Get all permutations of variables/pipelines
    
    df_permutations = pd.DataFrame(
        product(*di_params.values()), columns=di_params.keys()
        )
    
    df_permutations.to_parquet(p['I_perm'],index=False)
    
    return df_permutations