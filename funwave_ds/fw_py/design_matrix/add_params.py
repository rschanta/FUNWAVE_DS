from ..configs import get_key_dirs


def add_dependent_values(var_dict,
                         functions_to_apply):
    '''
    Add on dependency parameters defined by a pipeline. This is applied to
    each ROW of the design matrix

    Arguments:
    - var_dict (dictionary): dictionary of FUNWAVE parameters
    - functions_to_apply (list): list of functions defining the pipeline

    Returns:
    - var_dict (dictionary): dictionary of FUNWAVE parameters, with dependent
        parameters added on
    '''
    print('\nApplying DEPENDENCY functions')
    
    
    # Loop through to apply each dependency function
    dependent_vars = {}
    for func in functions_to_apply:
        print(f'\tApplying DEPENDENCY function: {func.__name__}')

        # Calculate
        result = func(var_dict)
        # Update
        dependent_vars.update(result)
        # Merge
        var_dict = {**var_dict, **dependent_vars}

    print('All DEPENDENCY functions completed successfully!')
    return var_dict



def add_required_params(var_dict,k):
    '''
    Add in parameters that FUNWAVE either needs or that we need to keep track
    of everything. This is applied to each ROW of the design matrix
    '''
    
    ptr = get_key_dirs(k)
    # Title of Run- use iteration number to keep things tidy
    var_dict['TITLE'] = f'input_{k:05}'
    # Result Folder
    var_dict['RESULT_FOLDER'] = ptr['or']        
    # Permutation Number
    var_dict['COMBO_NUM'] = k                                  
    
    return var_dict


def add_load_params(var_dict,functions_to_apply):
    '''
    Load in parameters upfront that may be needed in any of the design matrix
    permutations. This is applied BEFORE the core loop.
    '''
    
    load_vars = {}
    for func in functions_to_apply:
        result = func(var_dict)
        load_vars.update(result)
        var_dict = {**var_dict, **load_vars}
    return var_dict
