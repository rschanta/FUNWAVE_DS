


def get_stable_grid(var_dict):
    ## UNPACK ----------------------------------------------------------------
    L = var_dict['L']
    h_offshore = var_dict['h_offshore']
    ## [END] UNPACK ----------------------------------------------------------
    print('\t\tStarted getting hydrodynamic variables...')
    
    DX_from_h = h_offshore/15
    DX_from_l = L/60
    DX = (DX_from_h + DX_from_l)/2
    DY = DX
    print(DX)
    
    print('\t\tSuccessfully calculated grid size!')
    return {
            'DX': DX,
            'DY': DY}