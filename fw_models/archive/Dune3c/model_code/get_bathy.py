import numpy as np

def get_bathy(vars):
    print('\tStarted processing bathymetry data...')
    # Unpack Variables (note choice of bathy set by stability)
    DX = vars['DX']
    bathyX = vars['bathyX']
    bathyZ = vars['bathyZ']

    # Remove duplicate X values (issue for some trials)
    unique_X, indices = np.unique(bathyX, return_index=True)
    sorted_indices = np.sort(indices)
    bathyX = bathyX[sorted_indices]
    bathyZ = bathyZ[sorted_indices]

    # Interpolate to grid
    X_out = np.arange(0, np.max(bathyX) + DX, DX)
    Z_out = np.interp(X_out, bathyX, bathyZ)

    # Prepare outputs
    bathy_array = np.column_stack((X_out, Z_out))
    bathy_file = np.tile(Z_out, (3, 1))

    # Output
    bathy = {'array': bathy_array,
            'file': bathy_file}
    print('\tSuccessfully processed bathymetry data!\n')

    return {'bathy': bathy,
            'Mglob': int(len(X_out))}
