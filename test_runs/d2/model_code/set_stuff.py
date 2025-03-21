
def set_stuff(var_dict):
    
    PI_W = var_dict['PI_W']
    PI_D = var_dict['PI_D']
    h_offshore = var_dict['h_offshore']
    L = var_dict['L']
    
    Xc_WK = (PI_W+PI_D)*L
    Sponge_west_width = PI_W*L
    DEP_WK = h_offshore
    
    return {'Xc_WK': Xc_WK,
            'Sponge_west_width': Sponge_west_width,
            'DEP_WK': DEP_WK}
    
    