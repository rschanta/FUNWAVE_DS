# Add to system path
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb

# Animate a 1D Eta Profile
def animate_1D_Var(vars,plotvar):
    print(f"\t\tStarted Animation of {plotvar}...")

    #-----------------------------------------------------------------
    outvar = vars[plotvar]
    mask = vars['mask']
    bathy = vars['bathy_array']
    time = vars['time_dt']
    title = vars['TITLE']
    Xc_WK = vars['Xc_WK']
    Sponge_west_width = vars['Sponge_west_width']
    PLOT_INTV = vars['PLOT_INTV']
    #-----------------------------------------------------------------

    
    #timestep = vars['timestep']

    # Get/make necessary paths
    p = fpy.get_FW_paths()
    tri_num = int(os.getenv('TRI_NUM'))
    var_path = f'{p["ani"]}/{plotvar}'
    os.makedirs(var_path, exist_ok=True)
    avi_path = f'{var_path}/{plotvar}_{tri_num:05d}.avi'

    # Squeeze out y dimension
    outvar = np.squeeze(outvar[:,1,:])
    mask =  np.squeeze(mask[:,1,:])
    
    # Apply mask to eta
    outvar[mask == 0] = np.nan

    # Define bathymetry
    X = bathy[:,0]
    Z = -bathy[:,1]

    # Define time
    t = time[:,0]
    dt_av = np.mean(time[:,1]) # Use average dt to inform stride
    
    ## Frame rate and time coarseness
    speed = 10                       # model time displayed in 1 second of animation time                  
    coarseness = 0.5                 # model time between each frame in the animation
    fr = speed/coarseness            # required frame rate for this to work
    print('HERE')
    print(time[:,1])
    print('HERE')
    stride = int(coarseness/dt_av)   # space between indices for this to work

    # Set up plot
    fig, ax = plt.subplots(figsize=(6, 4), dpi=200)     # Set size and resolution
    width, height = fig.canvas.get_width_height()       # Plot dimensions

    # Set up plot elements for bathymetry and eta
    bathy_line, = ax.plot(X, Z, lw=2)
    outvar_line, = ax.plot(X, outvar[0,:], lw=2)
    
    # Add wavemaker and sponge positions as vertical lines
    ax.axvline(x=Xc_WK, color='red', linestyle='--', linewidth=2, label= 'Wavemaker')
    ax.axvline(x=Sponge_west_width, color='green', linestyle='--', linewidth=2, label= 'Sponge')

    # Formatting and labels
    plt.title(f'{title}: {plotvar}')
    plt.xlabel('Cross Shore position (m)')
    plt.ylabel(plotvar)
    plt.ylim(-3, 2)
    plt.grid(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=True, ncol=2)
    fig.tight_layout()

    # Set up a time counter box
    time_counter = ax.text(0.05, 0.95, 'time = 0.00',
                   transform=ax.transAxes,  # Use relative coordinates
                   fontsize=12,
                   verticalalignment='top',
                   horizontalalignment='left',
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    
    
    # Set up movie writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')   # '*XVID' = .avi file
    out = cv2.VideoWriter(avi_path, fourcc, fr, (width, height))

    # Loop through time steps
    for t_i in range(0, len(t), stride):
        print(f'\t\t\tplotting up to time {t[t_i]}')

        # Update outvar
        outvar_line.set_ydata(outvar[t_i,:])
        
        # Update time counter box
        time_counter.set_text(f'time = {t[t_i]:.2f}')  # Change the text content
        
        # Update movie
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape((height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
        out.write(image)

    # Finish the animation
    out.release()
    print(f"\t\t Finished Animation of {plotvar}...")
    return {}

## TODO: Animate 2D Var