def get_grid(var_dict):
    # Unpack
    L = var_dict['L']
    
    return {'DX': L/60,
            'DY': L/60}
    