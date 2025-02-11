


def check_required_params(var_dict,required_params):
    
    missing_params = [key for key in required_params if key not in var_dict]
    # Raise Error
    if len(missing_params) > 0:
        raise KeyError(f"Missing keys in dictionary: {', '.join(missing_params)}")
    
    return