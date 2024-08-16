###

import copy
## TODO: Just remove entirely?
'''
def FW_in_SLP():
    FW = {
        # TITLE
            'TITLE': 'input_SLP.txt',
        # PARALLEL INFO
            'PX': 16,
            'PY': 2,
        # DEPTH
            'DEPTH_TYPE': 'SLOPE',
            'DEPTH_FLAT': 5.0,
            'SLP': 0.1,
            'Xslp': 800.0,
        # PRINT
            'RESULT_FOLDER': 'output/',
        # DIMENSION
            'Mglob': 1024,
            'Nglob': 3,
        # TIME
            'TOTAL_TIME': 100.0,
            'PLOT_INTV': 1.0,
            'PLOT_INTV_STATION': 0.5,
            'SCREEN_INTV': 10.0,
            'PLOT_START_TIME': 0.0,
        # GRID
            'DX': 1.0,
            'DY': 1.0,
        # WAVEMAKER
            'WAVEMAKER': 'WK_REG',
            'DEP_WK': 5.0,
            'Xc_WK': 250.0,
            'Yc_WK': 0.0,
            'Tperiod': 8.0,
            'AMP_WK': 0.5,
            'Theta_WK': 0.0,
            'Delta_WK': 3.0,
        # PERIODIC BOUNDARY CONDITION
            'PERIODIC': 'F',
        # SPONGE LAYER
            'DIFFUSION_SPONGE': 'F',
            'FRICTION_SPONGE': 'T',
            'DIRECT_SPONGE': 'T',
            'Csp': '0.0',
            'CDsponge': '1.0',
            'Sponge_west_width': 180.0,
            'Sponge_east_width': 0.0,
            'Sponge_south_width': 0.0,
            'Sponge_north_width': 0.0,
        # PHYSICS
            'Cd': 0.0,
        # NUMERICS
            'CFL': 0.5,
            'FroudeCap': 3.0,
        # WET-DRY
            'MinDepth': 0.01,
        # BREAKING
            'VISCOSITY_BREAKING': 'T',
            'Cbrk1': 0.65,
            'Cbrk2': 0.35,
        # WAVE AVERAGE
            'T_INTV_mean': 20.0,
            'STEADY_TIME': 20.0,
        # OUTPUT
            'DEPTH_OUT': 'T',
            'FIELD_IO_TYPE': 'BINARY',
            'ETA': 'T',
            'MASK': 'T',
            'WaveHeight': 'T'
    }
    
    return FW


def FW_in_bathy():
    FW = {
        # TITLE
            'TITLE': 'input_bathy.txt',
        # PARALLEL INFO
            'PX': 16,
            'PY': 2,
        # DEPTH
            'DEPTH_TYPE': 'DATA',
            'DEPTH_FILE': 'bathy_DATA.txt',
        # DIMENSION
            'Mglob': 1024,
            'Nglob': 3,
        # TIME
            'TOTAL_TIME': 100.0,
            'PLOT_INTV': 1.0,
            'PLOT_INTV_STATION': 0.5,
            'SCREEN_INTV': 100.0,
            'PLOT_START_TIME': 0.0,
        # GRID
            'DX': 1.0,
            'DY': 1.0,
        # WAVEMAKER
            'WAVEMAKER': 'WK_REG',
            'DEP_WK': 5.0,
            'Xc_WK': 250.0,
            'Yc_WK': 0.0,
            'Tperiod': 8.0,
            'AMP_WK': 0.5,
            'Theta_WK': 0.0,
            'Delta_WK': 3.0,
        # PERIODIC BOUNDARY CONDITION
            'PERIODIC': 'F',
        # SPONGE LAYER
            'DIFFUSION_SPONGE': 'F',
            'FRICTION_SPONGE': 'T',
            'DIRECT_SPONGE': 'T',
            'Csp': '0.0',
            'CDsponge': '1.0',
            'Sponge_west_width': 0.0,
            'Sponge_east_width': 0.0,
            'Sponge_south_width': 0.0,
            'Sponge_north_width': 0.0,
        # PHYSICS
            'Cd': 0.0,
        # NUMERICS
            'CFL': 0.5,
            'FroudeCap': 3.0,
        # WET-DRY
            'MinDepth': 0.01,
        # BREAKING
            'VISCOSITY_BREAKING': 'T',
            'Cbrk1': 0.65,
            'Cbrk2': 0.35,
        # WAVE AVERAGE
            'T_INTV_mean': 20.0,
            'STEADY_TIME': 20.0,
        # OUTPUT
            'DEPTH_OUT': 'T',
            'FIELD_IO_TYPE': 'BINARY',
            'ETA': 'T',
            'MASK': 'T',
            'WaveHeight': 'T',
            'RESULT_FOLDER' : 'RESULT_FOLDER',
            
    }
    
    print('Successfully created FW_in_bathy template dictionary!')
    
    return FW
'''