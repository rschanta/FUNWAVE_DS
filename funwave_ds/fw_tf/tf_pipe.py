def apply_pipe(io_dict,functions_to_apply):

    # Loop through all post-processing functions
    print(f'\nApplying post-processing functions')
    for func in functions_to_apply:

        print(f'\tApplying function: {func.__name__}')
        post_vars = func(io_dict)
        var_dict = {**io_dict, **post_vars}

    return var_dict