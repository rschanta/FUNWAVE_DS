import numpy as np
import funwave_ds.fw_py as fpy
from .add_domain import *
'''
Note- this is 
'''



#%% FUNCTIONS TO CONSTRUCT THE BAR/CHANNEL
def bar_channel_bathy(var_dict):
    '''
    Constructs the bathymetry with the sandbar and the channel BEFORE any room
    is added on for sponges/propagation
    '''
    # Unpack Variables-------------------------------------------------
    # Beach geometry
    h_o = var_dict['h_offshore']
    h_b = var_dict['h_onshore']
    s = var_dict['s']
    w_L = var_dict['beach_LS_width']
    # Bar geometry
    d_bar = var_dict['bar_depth']
    h_bar = var_dict['bar_height']
    w_bar = var_dict['bar_width']
    # Channel geometry
    w_cha = var_dict['channel_width']
    d_cha = var_dict['channel_depth']
    # Grid Size
    DX = var_dict['DX']
    DY = var_dict['DY']
    # Booleans
    T_bar = bool(var_dict['T_bar'])
    T_slp = bool(var_dict['T_slp'])
    T_cha = bool(var_dict['T_cha'])
    # [END] UNPACK VARIABLES---------------------------------------------------
    
    
    # Calculate cross-shore width
    w_C = (h_o + h_b) / s
    
    # Create axes and meshgrid
    x_axis = np.arange(0, w_C + DX, DX)
    y_axis = np.arange(0, w_L + DY, DY)
    X, Y = np.meshgrid(x_axis, y_axis)
    
    # Calculate x_bar and its index (M_bar)
    M_bar = np.argmin(
                    np.abs(-h_o + s*x_axis + d_bar + h_bar)
                            )
    x_bar = x_axis[M_bar]
    
    # Take y_cha as half of the width
    y_cha = w_L/2
    N_cha = len(y_axis)/2
    
    # Calculate sigmas
    sigma_bar = w_bar /(2*2.33)
    sigma_cha = w_cha /(2*2.33)
    
    # Calculate Gaussians
    G_bar = np.exp( -((X-x_bar)/sigma_bar)**2)
    G_cha = np.exp(-((Y-y_cha)/sigma_cha)**2)
    
    # Adjust if bar not present
    if T_bar is False:
        G_bar = 1
        
    # Total bathymetry
    Z = (
        -h_o +                 # Flat offshore depth
        T_slp*s*X +                  # Add the sloping beach
        T_bar*h_bar*G_bar            # Add the sandbar
        -T_cha*d_cha*G_bar*G_cha     # Add the channel through the sloping sandbar
        
        )
    
    
    return {'beach_CS_width': w_C,
            'M_bar': M_bar,
            'x_bar': x_bar,
            'y_cha': y_cha,
            'N_cha': N_cha,
            'Z': Z}

#%% FUNCTIONS TO ADD ON THE DISTANCE
def add_on_distance(var_dict,Z):
    '''
    This function adds on the distance for the sponges
    '''
    # Unpack Variables-------------------------------------------------
    # Grid Size
    DX = var_dict['DX']
    DY = var_dict['DY']
    # PI Parameters
    PI_W = var_dict['PI_W']
    PI_S = var_dict['PI_S']
    PI_N = var_dict['PI_N']
    PI_F = var_dict['PI_F']
    PI_D = var_dict['PI_D']
    # Lambda
    L = var_dict['L']
    # [END] UNPACK VARIABLES---------------------------------------------------
    
    # ADD ON DISTANCE
    west_add = (PI_W+PI_F+PI_D)*L
    north_add = PI_N*L
    south_add = PI_S*L
    
    # Get distances in terms of indices
    west_add_i = int(west_add/DX)
    north_add_i = int(north_add/DY)
    south_add_i = int(south_add/DY)
    
    # Add on
    if west_add_i != int(0):
        Z = append_data_west(Z,west_add_i)
    if south_add_i != int(0):
        Z = append_data_south(Z,south_add_i)
    if north_add_i != int(0):
        Z = append_data_north(Z,north_add_i)
        
    return {'west_add_i': west_add_i,
            'south_add_i': south_add_i,
            'north_add_i': north_add_i,
            'Z': Z}

#%% DOMAIN OBJECT
def make_domain_object(Z,DX,DY):
    # Get new Mglob and Nglob
    Mglob = Z.shape[1]
    Nglob = Z.shape[0]
    
    # Make the Domain Object
    DOM = fpy.DomainObject3(DX = DX,
                            DY = DY,
                            Mglob = Mglob,
                            Nglob = Nglob)
    
    DOM.z_from_2D_array(-Z.T)
    
    return {'DOM': DOM,
            'Mglob': Mglob,
            'Nglob': Nglob,}

#%% GATHER
def gather_vars(var_dict,bar_stuff,add_stuff,dom_stuff):
    
    # Get the distance added to each side
    west_add = var_dict['DX']*add_stuff['west_add_i']
    south_add = var_dict['DY']*add_stuff['south_add_i']
    north_add = var_dict['DY']*add_stuff['north_add_i']
    print(south_add)
    print(north_add)
    # Update the cross-shore and longshore widths
    beach_CS_width = bar_stuff['beach_CS_width'] + west_add
    beach_LS_width = var_dict['beach_LS_width'] + north_add + south_add
    
    # Update the position of the sandbar and channel
    M_bar = bar_stuff['M_bar'] + add_stuff['west_add_i']
    x_bar = bar_stuff['x_bar'] + west_add
    y_cha = bar_stuff['y_cha'] + south_add
    
    return {'DOM': dom_stuff['DOM'],
            'west_add': west_add,
            'south_add': south_add,
            'north_add': north_add,
            'beach_CS_width': beach_CS_width,
            'beach_LS_width': beach_LS_width,
            'M_bar': M_bar,
            'x_bar': x_bar,
            'y_cha': y_cha,
            'Mglob': dom_stuff['Mglob'],
            'Nglob': dom_stuff['Nglob']}
    
#%% MAIN
'''
Main
'''
def make_bar_channel_bathy(var_dict):
    # Unpack Variables-------------------------------------------------
    DX = var_dict['DX']
    DY = var_dict['DY']
    # [END] UNPACK VARIABLES---------------------------------------------------
    
    
    # MAKE STANDARD BATHYMETRY 
    bar_stuff = bar_channel_bathy(var_dict)
    Z = bar_stuff['Z']
    
    # ADD ON ROOM FOR SPONGES
    add_stuff = add_on_distance(var_dict,Z)
    Z = add_stuff['Z']
    
    # MAKE THE DOMAIN OBJECT
    dom_stuff = make_domain_object(Z,DX,DY)
    
    
    # Gather everything
    gather = gather_vars(var_dict,bar_stuff,add_stuff,dom_stuff)
    
    return gather