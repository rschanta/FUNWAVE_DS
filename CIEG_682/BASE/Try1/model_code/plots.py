import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import funwave_ds.fw_py as fpy
import os


def make_surf_plot(var_dict):
    
    # UNPACK ------------------------------------------------------------------
    # Values and Coordinates
    X = var_dict['DOM'].X
    Y = var_dict['DOM'].Y
    Z = var_dict['DOM'].Z
    # Dimensions
    bar_width = var_dict['bar_width']
    channel_width = var_dict['channel_width']
    beach_CS_width = var_dict['beach_CS_width']
    # Values
    h_offshore = var_dict['h_offshore']
    h_onshore = var_dict['h_onshore']
    x_bar = var_dict['x_bar']
    ITER = var_dict['ITER']
    # [END] UNPACK ------------------------------------------------------------
    
    
    # Construct grid and get Z
    X,Y = np.meshgrid(X,Y)
    Z = Z.T
    
    
    # Initialize figure
    fig = plt.figure(figsize=(8, 6),dpi=400)
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot surface with colormap and shading
    surf = ax.plot_surface(X, Y, Z, 
                           cmap='twilight', 
                           edgecolor='none')
    
    
    
    ax.view_init(elev=30, azim=235)  # Adjust elevation & azimuth
    #fig.colorbar(surf, ax=ax,pad=0.1,shrink=0.75)
    
    # Labels and title
    ax.set_xlabel('Cross-Shore x (m)')
    ax.set_ylabel('Longshore y (m)')
    ax.set_zlabel('Depth h(x,y)')
    ax.set_title(
    f"Barred Bathymetry with Channel\n"
    f"Cross-shore Width: {beach_CS_width:.2f} m\n"
    f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
    f"Bar Position: x = {x_bar:.2f} (m)\n"
    f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
    f"Channel Width (in Longshore): {channel_width:.2f} m",
    fontsize=10,   
    )
    fig.tight_layout()
    
    # Get path to save, add `a` in front
    ptr = fpy.get_FW_tri_paths(tri_num=ITER)
    savepath = ptr['b_fig']
    new_path = f"{os.path.splitext(savepath)[0]}a.png"
    plt.savefig(new_path,dpi=300)
    plt.close()
    return 

def plot_cross_shore_slices(var_dict):
    # UNPACK ----------------------------------------------------------------------
    X = var_dict['DOM'].X
    Y = var_dict['DOM'].Y
    Z = var_dict['DOM'].Z
    LS_width = var_dict['beach_LS_width']
    bar_width = var_dict['bar_width']
    x_bar = var_dict['x_bar']
    channel_width = var_dict['channel_width']
    DY = var_dict['DY']
    ITER = var_dict['ITER']
    # [END] UNPACK ----------------------------------------------------------------
    
    # Calculate width of channel in indices
    channel_i_mid = int(LS_width/2/DY)
    channel_i_hi = int((LS_width + channel_width)/2/DY)
    
    # Choose indices of 4 slices on one side (it's symmetric)
    slice_indices = np.linspace(channel_i_mid,channel_i_hi,5).astype(int)
    
    
    fig,ax = plt.subplots(dpi=200)
    for i in slice_indices:
        ax.plot(X,Z[:,i],label=f'y = {Y[i]:.2f}')
    
    
    ax.set_title(
    f"Cross-Shore Slices of Sandbar\n"
    f"Longshore Width: {LS_width} m\n"
    f"Bar Position: x = {x_bar} (m)\n"
    f"Bar Width (in Cross-shore): {bar_width} m\n"
    f"Channel Width (in Long-shore): {channel_width} m",
    fontsize=10,  
    loc='center'  
)

    ax.axhline(0,c='blue',label='MWL')
    ax.grid()
    ax.set_xlabel('Cross-Shore x (m)')
    ax.set_ylabel('Depth h(x,y) (m)')
    ax.legend(title='Longshore Position (m)')
    fig.tight_layout()
    
    # Get path to save, add `a` in front
    ptr = fpy.get_FW_tri_paths(tri_num=ITER)
    savepath = ptr['b_fig']
    new_path = f"{os.path.splitext(savepath)[0]}b.png"
    plt.savefig(new_path,dpi=300)
    plt.close()
    
    return 



def plot_long_shore_slices(var_dict):
    # UNPACK ------------------------------------------------------------------
    # Values and Coordinates
    X = var_dict['DOM'].X
    Y = var_dict['DOM'].Y
    Z = var_dict['DOM'].Z
    # Dimensions
    bar_width = var_dict['bar_width']
    channel_width = var_dict['channel_width']
    beach_CS_width = var_dict['beach_CS_width']
    x_bar = var_dict['x_bar']
    # Grid spacing
    DX = var_dict['DX']
    # Index of bar
    M_bar = var_dict['M_bar']
    ITER = var_dict['ITER']
    # [END] UNPACK ------------------------------------------------------------
    
    # Calculate width of bar in indices
    bar_i_mid = M_bar
    bar_i_hi = int(M_bar +  bar_width/2/DX)
    
    # Choose indices of 5 slices on one side (it's symmetric)
    slice_indices = np.linspace(bar_i_mid,bar_i_hi,5).astype(int)
    fig,ax = plt.subplots(dpi=200)
    for i in slice_indices:
        ax.plot(Y,Z[i,:],label=f'X = {X[i]:.2f}')
    
    ax.set_title(
    f"Longshore Slices of Sandbar\n"
    f"Cross-shore Width: {beach_CS_width} m\n"
    f"Bar Position: x = {x_bar} (m)\n"
    f"Bar Width (in Cross-shore): {bar_width} m\n"
    f"Channel Width (in Longshore): {channel_width} m",
    fontsize=10,  
    loc='center'  
    )
    
    ax.grid()
    ax.legend(title='Cross-shore Position (m)',loc='lower left',fontsize=8)
    ax.set_xlabel('Longshore y (m)')
    ax.set_ylabel('Depth h(x,y) (m)')
    
    
    fig.tight_layout()
    
    # Get path to save, add `a` in front
    ptr = fpy.get_FW_tri_paths(tri_num=ITER)
    savepath = ptr['b_fig']
    new_path = f"{os.path.splitext(savepath)[0]}c.png"
    plt.savefig(new_path,dpi=300)
    plt.close()

    return 

def make_contour_plot(var_dict):
    
    # UNPACK ------------------------------------------------------------------
    # Values and Coordinates
    X = var_dict['DOM'].X
    Y = var_dict['DOM'].Y
    Z = var_dict['DOM'].Z
    ITER = var_dict['ITER']
    # Dimensions
    bar_width = var_dict['bar_width']
    channel_width = var_dict['channel_width']
    beach_CS_width = var_dict['beach_CS_width']
    # Values
    h_offshore = var_dict['h_offshore']
    h_onshore = var_dict['h_onshore']
    x_bar = var_dict['x_bar']
    Xc_WK = var_dict['Xc_WK']
    Sponge_west_width = var_dict['Sponge_west_width']
    a = var_dict['AMP_WK']
    Tperiod = var_dict['Tperiod']
    # [END] UNPACK ------------------------------------------------------------
    
    
    # Construct grid and get Z
    X,Y = np.meshgrid(X,Y)
    Z = Z.T
    
    
    # Initialize figure
    fig = plt.figure(figsize=(8, 6),dpi=400)
    ax = fig.add_subplot()
    
    # Create filled contour plot
    contour = ax.contourf(X, Y, Z, cmap='twilight', levels=20)  
    contour_lines = ax.contour(X, Y, Z, colors='black', linewidths=0.5) 
    
    # Add wavemaker/sponge
    ax.axvline(Xc_WK,
               label=f'WK: a = {a:.2f} m, T = {Tperiod:.2f} s',
               lw=2,c='MidnightBlue',ls='--')
    ax.axvline(Sponge_west_width,
               label='Sponge',
               lw=2,c='DarkGreen',ls='--')
    
    # Add colorbar
    cbar = fig.colorbar(contour, ax=ax, pad=0.1, shrink=0.75)
    cbar.set_label('Depth h(x,y)')
    
    # Labels and title
    ax.set_xlabel('Cross-Shore x (m)')
    ax.set_ylabel('Longshore y (m)')
    ax.set_title(
    f"Barred Bathymetry with Channel\n"
    f"Cross-shore Width: {beach_CS_width:.2f} m\n"
    f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
    f"Bar Position: x = {x_bar:.2f} (m)\n"
    f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
    f"Channel Width (in Longshore): {channel_width:.2f} m",
    fontsize=10,   
    )
    fig.tight_layout()
    ax.legend(loc='lower left')
    
    # Get path to save, add `a` in front
    ptr = fpy.get_FW_tri_paths(tri_num=ITER)
    savepath = ptr['b_fig']
    new_path = f"{os.path.splitext(savepath)[0]}d.png"
    plt.savefig(new_path,dpi=300)
    plt.close()
    return 