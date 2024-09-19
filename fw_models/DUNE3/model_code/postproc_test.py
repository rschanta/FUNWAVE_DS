def get_bathy_post(vars):
    print('\t\tStarted post-processing bathymetry...')
    
    # Unpack Variables (note choice of bathy set by stability- get that later)
    bathy = vars['spectra_array']
    new_bathy = bathy*2

    # Update with new parameters
    output_vars = {'new_bathy':  new_bathy}

    print('\t\tSucessfully post-processed bathymetry...')
    return output_vars