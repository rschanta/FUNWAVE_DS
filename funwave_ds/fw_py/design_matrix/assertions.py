

def assert_design_matrix_csv(df):
    '''
    Asserts that the design matrix loaded in from a csv is valid by checking 
    that if there is a value in CON, then LO,HI, and NUM must be nan, and vice 
    versa. Also checks that all entries in 'NUM' are valid integers by ensuring
    no '.' appears in the entry

    '''
    # Ensure Condition met
    condition = (
        (df['CON'].notna() & df[['LO', 'HI', 'NUM']].isna().all(axis=1)) |
        (df['CON'].isna() & df[['LO', 'HI', 'NUM']].notna().any(axis=1))
    )
    assert condition.all(),  "At least one row is both constant/ranged!"

    # Ensure that all NUM values are valid integers
    invalid = df['NUM'].apply(lambda x: isinstance(x, str) and '.' in x)
    if invalid.any():
        raise AssertionError("Float found in NUM- must contain only integers!")
    return df


def assert_design_matrix_dict(input_dict):
    '''
    Asserts that a design matrix specified by a dictionary is valid by checking
    that all the following are met:
        - Category Keys must contain a dictionary
        - Parameter Kets must contain either a string or a list
            - If a list, the list must contain:
                - strings
                - 3-entry tuples composed of ints/floats

    '''
    
    for category, category_dict in input_dict.items():
        # Assert that category is a dictionary
        assert isinstance(category_dict, dict), f"'{category}' must contain a dictionary."
        
        for FW_PARAM_NAME, FW_PARAM_VALUES in category_dict.items():
            # Strings are okay
            if isinstance(FW_PARAM_VALUES, str):
                continue
            # Tuples are okay if they meed the tuple condition
            elif isinstance(FW_PARAM_VALUES, tuple):
                if (
                    isinstance(FW_PARAM_VALUES, tuple)
                    and len(FW_PARAM_VALUES) == 3
                    and all(isinstance(x, (int, float)) for x in FW_PARAM_VALUES)
                ):
                    continue
            # Lists- must assert validity of strings/tuples
            elif isinstance(FW_PARAM_VALUES, list):
                for item in FW_PARAM_VALUES:
                    # Strings are okay
                    if isinstance(item, str):
                        continue
                    # Tuples must be numeric and length 3
                    elif (
                        isinstance(item, tuple)
                        and len(item) == 3
                        and all(isinstance(x, (int, float)) for x in item)
                    ):
                        continue
                    # Raise Errors Otherwise
                    else:
                        raise AssertionError(
                            f"Invalid item at {category}/{FW_PARAM_NAME}: {item}"
                        )
            # Raise error if not a list
            else:
                raise AssertionError(
                    f"Value at {category_dict}->{FW_PARAM_NAME} must be a string or a list, got {type(FW_PARAM_VALUES).__name__}"
                )
                
    return 