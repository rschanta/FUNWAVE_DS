import pandas as pd
#%% FILTERING
'''
The functions in this section are used to discard trials
of an ensemble that do not meet some criteria set by a 
filter function.
'''
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
    print('\nApplying FILTER functions')

    # Loop through all filter functions
    for func in functions_to_apply:
        print(f'\tApplying FILTER function: {func.__name__}')
        result = func(var_dict)
        
        # Record failure and key data
        if not result:
            
            # Record function name and what the iteration would have been
            print(f'\tFailed FILTER function: {func.__name__}')
            failed_checks.append(func.__name__)  
            failed_vars['PERM_I'] = var_dict['PERM_I']

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
    