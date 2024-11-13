import copy
import numpy as np

# Helper function to convert to valid FORTRAN
def convert_to_number(value):
    try:
        # Try conversion to float (will work for ints/floats)
        float_value = float(value)
        
        # Case to return float: if a decimal point is provided
        if '.' in str(value).strip():
            return float_value
        # Case to return int: if no decimal point is provided
        else: 
            return int(float_value)
        
    # Case to return string: if conversion to float fails
    except ValueError:
        return value
        
def print_input_file(var_dict,ptr):
    print('\nPRINTING input.txt...')
    print('\tStarted printing input file...')

    var_dict_copy = copy.deepcopy(var_dict)
    with open(ptr['i_file'], 'w') as f:
        for var_name, value in var_dict_copy.items():
            if isinstance(value, (str, int, float)):
                f.write(f"{var_name} = {value}\n")
    
    print(f"\tinput.txt file successfully saved to: {ptr['i_file']}", flush=True)
    return     