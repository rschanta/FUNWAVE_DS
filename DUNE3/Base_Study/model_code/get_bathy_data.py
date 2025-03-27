def get_bathy_data(var_dict):
    D3_Trial = int(var_dict['D3_Trial'])
    X = var_dict['data'][f'tri_{D3_Trial:02}']['f_X_before']
    Z = var_dict['data'][f'tri_{D3_Trial:02}']['f_bed_before']
    MWL_left = var_dict['data'][f'tri_{D3_Trial:02}']['r_MWL'][0]
    
    return {'X': X,
            'Z': Z,
            'MWL_left': MWL_left}