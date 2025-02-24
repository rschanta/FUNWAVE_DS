from ..configs import log_function_call, save_logs_to_file

#%% ADD VALUES ONTO DESIGN MATRIX
def add_dependent_values(var_dict,functions_to_apply):
    '''
    Add on dependency parameters defined by some dependency pipeline

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of functions defining the pipeline

    Returns:
    - df_failed_vars (dictionary): dictionary of FUNWAVE parameters, with dependent
        parameters added
    '''

    dependent_vars = {}
    print(f'\nApplying DEPENDENCY functions')
    for func in functions_to_apply:
        print(f'\tApplying DEPENDENCY function: {func.__name__}')
        # Add to log
        decorated_func = log_function_call(func)
        result = decorated_func(var_dict)
        # Update
        dependent_vars.update(result)
        var_dict = {**var_dict, **dependent_vars}
    print(f'All DEPENDENCY functions completed successfully!')
    return var_dict

def add_required_params(var_dict,k,ptr):
    var_dict['TITLE'] = f'input_{k:05}'                     # Title is iteration number
    var_dict['RESULT_FOLDER'] = ptr['RESULT_FOLDER']        # RESULT_FOLDER for FUNWAVE
    var_dict['PERM_I'] = k                                  # Permutation Number
    return var_dict


def add_load_params(var_dict,functions_to_apply):
    load_vars = {}
    for func in functions_to_apply:
        result = func(var_dict)
        load_vars.update(result)
        var_dict = {**var_dict, **load_vars}
    return var_dict
