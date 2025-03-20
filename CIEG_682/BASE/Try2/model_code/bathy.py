import numpy as np
import funwave_ds.fw_py as fpy
import xarray as xr

def set_bathy(var_dict):
    ## UNPACK ----------------------------------------------------------------
    # Sloping Beach Geometry
    h_offshore = var_dict['h_offshore']
    h_onshore = var_dict['h_onshore']
    s = var_dict['slope']
    beach_LS_width = var_dict['beach_LS_width']
    # Bar Geometry
    bar_depth = var_dict['bar_depth']
    bar_height = var_dict['bar_height']
    bar_width = var_dict['bar_width']
    # Channel Geometry
    channel_depth = var_dict['channel_depth']
    channel_width = var_dict['channel_width']
    # Problem Grid
    DX = var_dict['DX']
    DY = var_dict['DY']
    # Stability add-on
    PI_1 = var_dict['PI_1']
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    L = var_dict['L']
    ## [END] UNPACK ----------------------------------------------------------
    print('\t\tStarting setting barred/channeled bathymetry...')
   
    # Calculate the required cross-shore width for slope and on/offshore heights
    beach_CS_width = (h_offshore + h_onshore) / s
    
    # Create axes and meshgrid
    x_axis = np.arange(0, beach_CS_width + DX, DX)
    y_axis = np.arange(0, beach_LS_width + DY, DY)
    X, Y = np.meshgrid(x_axis, y_axis)
    
    # Make the basic sloping beach, without bars/channels
    beach_sloping = -h_offshore +s*X;
    
    ## BAR  CONSTRUCTION ------------------------------------------------------
    # Find the x-location of the bar center for input bar height & depth
    M_bar = np.argmin(np.abs(beach_sloping[0, :] + bar_height + bar_depth))
    x_bar = x_axis[M_bar]
    
    # Find sigma corresponding to the bar width, construct unit Gaussian
    sigma = bar_width/2/2.575
    unit_hump = np.exp(-((X - x_bar) / sigma)**2)
    
    # Make beach with the bar
    bar = bar_height*unit_hump
    Z = beach_sloping + bar
    ## [END] BAR CONSTRUCTION  ------------------------------------------------


    # CHANNEL CONSTRUCTION ----------------------------------------------------
    # Center the bar in the longshore
    y_channel = beach_LS_width/2
    
    # Find sigma corresponding to the channel width, construct unit Gaussian
    sigma = channel_width/2/2.575;
    unit_channel = np.exp(-((Y - y_channel) / sigma)**2)
    
    # Make beach with the bar/channel
    Z = Z - channel_depth * unit_hump * unit_channel
    ## [END] CHANNEL CONSTRUCTION  --------------------------------------------
    
    
    # ADD ON DISTANCE ---------------------------------------------------------
    # Distance to add from Pi groups
    dist_to_add = (PI_1+PI_2+PI_3)*L

    
    # Determine the number of new cells needed (new_M)
    new_M = np.ceil(dist_to_add/DX)

    # X values we need to add, and length
    add_X = - np.flip(np.arange(1,new_M+1)*DX)
    add_M = len(add_X)
    
    # Make new X axis, get Mglob, get Nglob
    new_X = np.concatenate((add_X, x_axis))
    Mglob = len(new_X)
    Nglob = len(y_axis)
    
    # Add on repeated Z values 
    Z = Z.T
    add_Z = np.tile(Z[0, :], (add_M, 1))  
    new_Z = np.vstack((add_Z, Z))  

    
    # Get the distance actually added to shift over all cross-shore terms
    dist_add = np.abs(new_X[0])
    new_X = new_X + dist_add
    x_bar = x_bar  + dist_add
    M_bar = M_bar + add_M
    beach_CS_width= beach_CS_width + dist_add
    
    # [END] ADD ON DISTANCE ---------------------------------------------------
    
    # NOTE: Flip Z to align with FUNWAVE height conventions :)
    Z = -new_Z
    
    # MAKE THE DOMAIN OBJECT --------------------------------------------------
    DOM = fpy.DomainObject3(DX = DX,
                            DY = DY,
                            Mglob = Mglob,
                            Nglob = Nglob)
    DOM.z_from_2D_array(Z)
    
    print('\t\tStarting setting barred/channeled bathymetry...')
    
    return {'DOM': DOM,
            'beach_CS_width': beach_CS_width,
            'Mglob': int(Mglob),
            'Nglob': int(Nglob),
            'x_bar': x_bar,
            'M_bar': M_bar}
    
    
    