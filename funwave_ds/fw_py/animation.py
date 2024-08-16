import numpy as np
import matplotlib.pyplot as plt
import cv2
def animate_eta_1D(results,name,timestep,bathy=True,dep=True,fr = 5,WK=True):
    # Deal with bathy
    if bathy == True:
        # Use available 1D bathymetry data provided
        bathyX = results['bathy'][:,0]
        bathyZ = -results['bathy'][:,1]
    elif dep == True:
        # Use dep.out data and DX
        bathyZ = -results['dep'][0,0,:]
        bathyX = np.arange(len(bathyZ))*results['DX']

    # Pull out eta (1D)
    eta = np.squeeze(results['eta'][:,1,:])
    
    # Pull out time
    time = np.squeeze(results['time_dt'][:,0])
    # Set up plot
    dpi = 200
    fig, ax = plt.subplots(figsize=(6, 4), dpi=dpi)
    plt.grid(True)
    
    
    # Set up lines
    bathy_line, = ax.plot(bathyX, bathyZ, lw=2)
    eta_line, = ax.plot(bathyX, eta[0,:], lw=2)
    
    
    
    
    # Set title
    title_str = results['TITLE'].decode('utf-8')
    alt_title_str = results['ALT_TITLE'].decode('utf-8')
    plt.title(f'{title_str}\n{alt_title_str}')
    
    # Add axis lines
    plt.xlabel('Cross Shore position (m)')
    plt.ylabel('eta')
    # Add wavemaker position
    if WK == True:
        ax.axvline(x=results['Xc_WK'], color='red', linestyle='--', linewidth=2, label= 'Wavemaker')
        
    # Add sponge
    if 'Sponge_west_width' in results:
        if results['Sponge_west_width'] != 0:
            ax.axvline(x=results['Sponge_west_width'], color='green', linestyle='--', linewidth=2, label= 'Sponge')
    
    # Add time
    time_counter = ax.text(0.05, 0.95, 'time = 0.00',
                   transform=ax.transAxes,  # Use relative coordinates
                   fontsize=12,
                   verticalalignment='top',
                   horizontalalignment='left',
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    
    # Add legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), frameon=True, ncol=2)
    
    # Set up movie writer
    width, height = fig.canvas.get_width_height()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'XVID' for AVI
    out = cv2.VideoWriter(f'{name}.avi', fourcc, fr, (width, height))
    fig.tight_layout()
    # Loop through times
    for t in range(0, len(time), timestep):
        print(f'plotting up to time {time[t]}')
        # Update data
        eta_line.set_ydata(eta[t,:])
        time_counter.set_text(f'time = {time[t]:.2f}')  # Change the text content
        
        # Update movie
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape((height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
        out.write(image)
    return

    out.release()
    plt.show()
    
    return