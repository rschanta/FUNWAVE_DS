import numpy as np

def ranged_variables(df):
    '''
    Finds all permutations of the ranged variables
    
    Arguments:
    - df (Pandas DataFrame): output of read_design_matrix

    Returns:
    - di_ranged (Dict): dict of {param_name (str): List (obj)} for 
        the ranged parameters in the design matrix using` np.linspace`
    '''
    
    # Split out ranged variables from nonranged variables 
    df_ranged = df[df['CON'].isna()]
    
    # Dictionary: key = name, value- list of values
    di_ranged = {}  
    for _, row in df_ranged.iterrows():
        var = row['VAR']
        if var not in di_ranged:
            di_ranged[var] = []
            
        # Linspace and add to variable value list
        var_range = np.linspace(row['LO'], row['HI'], int(row['NUM'])).tolist()
        di_ranged[var].extend(var_range)
        di_ranged[var] = list(set(di_ranged[var]))
        
    return di_ranged

def nonranged_variables(df):
    '''
    Finds all permutations of the nonranged variables
    
    Arguments:
    - df (Pandas DataFrame): output of read_design_matrix

    Returns:
    - di_nonranged (Dict): dict of {param_name (str): List (obj)} for 
        the nonranged parameters in the design matrix, including list/repeated 
        parameters
    '''
    df_nonranged = df[df['CON'].notna()]
    di_nonranged = df_nonranged.groupby('VAR')['CON'].apply(list).to_dict()
    return di_nonranged

def combine_all_vars(di_ranged,di_nonranged,function_sets):
    '''
    Loads in the design matrix, checks formatting, and finds all 
    permutations of the different variables in the design matrix csv file

    Arguments:
    - di_ranged (Dict): output of ranged_variables
    - di_nonranged (Dict): output of nonranged_variables
    - function_sets (Dict): valid function set 

    Returns:
    - di_params (Dict): dict of {param_name (str): List (obj)} for 
        all variables/pipelines in the design matrix and generation file.
    '''
    # MERGE DICTIONARIES AND COMBINED LISTS FOR CONFLICTS
    di_params = {}
    # Get all keys
    all_keys = set(di_ranged.keys()).union(set(di_nonranged.keys()))
    for key in all_keys:
        # Merge lists for each param.
        di_params[key] = di_ranged.get(key, []) + di_nonranged.get(key, [])


    # Add in function sets
    di_params['PIPELINE'] = list(function_sets.keys())
    
    return di_params