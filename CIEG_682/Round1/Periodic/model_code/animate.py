import numpy as np
import matplotlib.pyplot as plt
import cv2
def animate_eta(ds,
                speed = 10,
                coarseness=0.5,
                save_to_avi='test.mp4'):
    
    # UNPACK ----------------------------------------------------------------------
    # Time and space grid
    t = ds['t_FW'].values
    X = ds['X'].values
    Y = ds['Y'].values
    Z = ds['Z'].values
    
    # Dimensions
    bar_width = ds.attrs['bar_width']
    channel_width = ds.attrs['channel_width']
    beach_CS_width = ds.attrs['beach_CS_width']
    
    # Beach geometry
    h_offshore = ds.attrs['h_offshore']
    h_onshore = ds.attrs['h_onshore']
    x_bar = ds.attrs['x_bar']
    
    # FUNWAVE Parameters
    Xc_WK = ds.attrs['Xc_WK']
    Sponge_west_width = ds.attrs['Sponge_west_width']
    AMP_WK = ds.attrs['AMP_WK']
    Tperiod = ds.attrs['Tperiod']
    # UNPACK ----------------------------------------------------------------------
    
    
    # Make Grid
    Z = Z.T
    X, Y = np.meshgrid(X, Y)
    
    
    # Apply mask to eta
    eta = ds['eta'].values
    mask = ds['mask'].values
    eta[mask == 0] = np.nan 
    
    ## Min and max of eta for scaling purposes
    eta_max = np.nanmax(eta)
    eta_min = np.nanmin(eta)
    
    ## SET UP FIRST PLOT ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
    
    # Contour plot of eta (initial)
    contour = ax.contourf(X, Y, eta[0, :, :], 
                          cmap='coolwarm',
                          levels=20, 
                          vmin=eta_min, vmax=eta_max)
    # Contour plot of bathymetry
    contour_lines = ax.contour(X, Y, Z, 
                               colors='black', linewidths=0.5) 
    
    ## Time text box
    ax.text(0.95, 0.05, "t = 0.0 s",
            transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
            fontsize=14, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  # Box styling
    
    ## Title
    ax.set_title(
        f"Barred Bathymetry with Channel\n"
        f"Cross-shore Width: {beach_CS_width:.2f} m\n"
        f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
        f"Bar Position: x = {x_bar:.2f} (m)\n"
        f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
        f"Channel Width (in Longshore): {channel_width:.2f} m",
        fontsize=10,   
        )
    
    # Axis Labels
    ax.set_xlabel('Cross-shore x (m)')
    ax.set_ylabel('Longshore y (m)')
    
    # Lines for wavemaker and sponge
    ax.axvline(Xc_WK,
               c='MidnightBlue',lw=2,ls='--',
               label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
    ax.axvline(Sponge_west_width,
               c='DarkGreen',lw=2,ls='--',
               label='Sponge')
    
    
    # Formatting
    ax.legend(loc='lower left')
    fig.tight_layout()
    ## [END] SET UP FIRST PLOT ----------------------------------------------------
    
    ## SET UP MOVIE WRITER --------------------------------------------------------          
    fr = speed/coarseness            
    stride = int(coarseness/0.1)
    width, height = fig.canvas.get_width_height()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_to_avi, fourcc, fr, (width, height))
    ## [END] SET UP MOVIE WRITER --------------------------------------------------
    
    ## ANIMATION LOOP -------------------------------------------------------------
    time_counter = 't = 0.0 s'
    
    # Loop through time at the desired stride
    for t_i in range(0, len(t), stride):
        print(f'\t\t\tplotting up to time {t[t_i]}')
    
        # Get eta
        eta_frame = ds['eta'].values[t_i, :, :]
    
        # Clear axes
        ax.clear()
    
        # Update eta contours
        contour = ax.contourf(X, Y, eta_frame, 
                              cmap='coolwarm',
                              levels=20, 
                              vmin=eta_min, vmax=eta_max)
        
        # Re-add bathy contours
        contour_lines = ax.contour(X, Y, Z, 
                                   colors='black', linewidths=0.5)
        ax.clabel(contour_lines, inline=True, fontsize=8, fmt="%.2f")
    
    
        # Update time counter
        if t_i%10 == 0:
            time_counter = f't = {t[t_i]:.2f} s'
            
        ax.text(0.95, 0.05, time_counter,
                transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
                fontsize=14, 
                verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  
            
        # Re-add title
        ax.set_title(
            f"Barred Bathymetry with Channel\n"
            f"Cross-shore Width: {beach_CS_width:.2f} m\n"
            f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
            f"Bar Position: x = {x_bar:.2f} (m)\n"
            f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
            f"Channel Width (in Longshore): {channel_width:.2f} m",
            fontsize=10,   
            )
        
        # Re-add labels
        ax.set_xlabel('Cross-shore x (m)')
        ax.set_ylabel('Longshore y (m)')
        
        # Re-add lines for wavemaker and sponge
        ax.axvline(Xc_WK,c='MidnightBlue',lw=2,ls='--',label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
        ax.axvline(Sponge_west_width,c='DarkGreen',lw=2,ls='--',label='Sponge')
        
        # Formatting
        ax.legend(loc='lower left')
        fig.tight_layout()
        
        # DRAW FRAME AND OUTPUT TO WRITER -----------------------------------------
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape((height, width, 4))
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        out.write(image)
        # [END] DRAW FRAME AND OUTPUT TO WRITER -----------------------------------
        
    ## [END] ANIMATION LOOP -------------------------------------------------------
    ## Release the video writer
    out.release()
    
    return out



def animate_v(ds,
                speed = 10,
                coarseness=0.5,
                save_to_avi='test.mp4'):
    
    # UNPACK ----------------------------------------------------------------------
    # Time and space grid
    t = ds['t_FW'].values
    X = ds['X'].values
    Y = ds['Y'].values
    Z = ds['Z'].values
    
    # Dimensions
    bar_width = ds.attrs['bar_width']
    channel_width = ds.attrs['channel_width']
    beach_CS_width = ds.attrs['beach_CS_width']
    
    # Beach geometry
    h_offshore = ds.attrs['h_offshore']
    h_onshore = ds.attrs['h_onshore']
    x_bar = ds.attrs['x_bar']
    
    # FUNWAVE Parameters
    Xc_WK = ds.attrs['Xc_WK']
    Sponge_west_width = ds.attrs['Sponge_west_width']
    AMP_WK = ds.attrs['AMP_WK']
    Tperiod = ds.attrs['Tperiod']
    # UNPACK ----------------------------------------------------------------------
    
    
    # Make Grid
    Z = Z.T
    X, Y = np.meshgrid(X, Y)
    
    
    # Apply mask to eta
    eta = ds['v'].values
    mask = ds['mask'].values
    eta[mask == 0] = np.nan 
    
    ## Min and max of eta for scaling purposes
    eta_max = np.nanmax(eta)
    eta_min = np.nanmin(eta)
    
    ## SET UP FIRST PLOT ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
    
    # Contour plot of eta (initial)
    contour = ax.contourf(X, Y, eta[0, :, :], 
                          cmap='coolwarm',
                          levels=20, 
                          vmin=eta_min, vmax=eta_max)
    # Contour plot of bathymetry
    contour_lines = ax.contour(X, Y, Z, 
                               colors='black', linewidths=0.5) 
    
    ## Time text box
    ax.text(0.95, 0.05, "t = 0.0 s",
            transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
            fontsize=14, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  # Box styling
    
    ## Title
    ax.set_title(
        f"Barred Bathymetry with Channel\n"
        f"Cross-shore Width: {beach_CS_width:.2f} m\n"
        f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
        f"Bar Position: x = {x_bar:.2f} (m)\n"
        f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
        f"Channel Width (in Longshore): {channel_width:.2f} m",
        fontsize=10,   
        )
    
    # Axis Labels
    ax.set_xlabel('Cross-shore x (m)')
    ax.set_ylabel('Longshore y (m)')
    
    # Lines for wavemaker and sponge
    ax.axvline(Xc_WK,
               c='MidnightBlue',lw=2,ls='--',
               label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
    ax.axvline(Sponge_west_width,
               c='DarkGreen',lw=2,ls='--',
               label='Sponge')
    
    
    # Formatting
    ax.legend(loc='lower left')
    fig.tight_layout()
    ## [END] SET UP FIRST PLOT ----------------------------------------------------
    
    ## SET UP MOVIE WRITER --------------------------------------------------------          
    fr = speed/coarseness            
    stride = int(coarseness/0.1)
    width, height = fig.canvas.get_width_height()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_to_avi, fourcc, fr, (width, height))
    ## [END] SET UP MOVIE WRITER --------------------------------------------------
    
    ## ANIMATION LOOP -------------------------------------------------------------
    time_counter = 't = 0.0 s'
    
    # Loop through time at the desired stride
    for t_i in range(0, len(t), stride):
        print(f'\t\t\tplotting up to time {t[t_i]}')
    
        # Get eta
        eta_frame = ds['eta'].values[t_i, :, :]
    
        # Clear axes
        ax.clear()
    
        # Update eta contours
        contour = ax.contourf(X, Y, eta_frame, 
                              cmap='coolwarm',
                              levels=20, 
                              vmin=eta_min, vmax=eta_max)
        
        # Re-add bathy contours
        contour_lines = ax.contour(X, Y, Z, 
                                   colors='black', linewidths=0.5)
        ax.clabel(contour_lines, inline=True, fontsize=8, fmt="%.2f")
    
    
        # Update time counter
        if t_i%10 == 0:
            time_counter = f't = {t[t_i]:.2f} s'
            
        ax.text(0.95, 0.05, time_counter,
                transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
                fontsize=14, 
                verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  
            
        # Re-add title
        ax.set_title(
            f"Barred Bathymetry with Channel\n"
            f"Cross-shore Width: {beach_CS_width:.2f} m\n"
            f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
            f"Bar Position: x = {x_bar:.2f} (m)\n"
            f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
            f"Channel Width (in Longshore): {channel_width:.2f} m",
            fontsize=10,   
            )
        
        # Re-add labels
        ax.set_xlabel('Cross-shore x (m)')
        ax.set_ylabel('Longshore y (m)')
        
        # Re-add lines for wavemaker and sponge
        ax.axvline(Xc_WK,c='MidnightBlue',lw=2,ls='--',label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
        ax.axvline(Sponge_west_width,c='DarkGreen',lw=2,ls='--',label='Sponge')
        
        # Formatting
        ax.legend(loc='lower left')
        fig.tight_layout()
        
        # DRAW FRAME AND OUTPUT TO WRITER -----------------------------------------
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape((height, width, 4))
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        out.write(image)
        # [END] DRAW FRAME AND OUTPUT TO WRITER -----------------------------------
        
    ## [END] ANIMATION LOOP -------------------------------------------------------
    ## Release the video writer
    out.release()
    
    return out


def animate_u(ds,
                speed = 10,
                coarseness=0.5,
                save_to_avi='test.mp4'):
    
    # UNPACK ----------------------------------------------------------------------
    # Time and space grid
    t = ds['t_FW'].values
    X = ds['X'].values
    Y = ds['Y'].values
    Z = ds['Z'].values
    
    # Dimensions
    bar_width = ds.attrs['bar_width']
    channel_width = ds.attrs['channel_width']
    beach_CS_width = ds.attrs['beach_CS_width']
    
    # Beach geometry
    h_offshore = ds.attrs['h_offshore']
    h_onshore = ds.attrs['h_onshore']
    x_bar = ds.attrs['x_bar']
    
    # FUNWAVE Parameters
    Xc_WK = ds.attrs['Xc_WK']
    Sponge_west_width = ds.attrs['Sponge_west_width']
    AMP_WK = ds.attrs['AMP_WK']
    Tperiod = ds.attrs['Tperiod']
    # UNPACK ----------------------------------------------------------------------
    
    
    # Make Grid
    Z = Z.T
    X, Y = np.meshgrid(X, Y)
    
    
    # Apply mask to eta
    eta = ds['u'].values
    mask = ds['mask'].values
    eta[mask == 0] = np.nan 
    
    ## Min and max of eta for scaling purposes
    eta_max = np.nanmax(eta)
    eta_min = np.nanmin(eta)
    
    ## SET UP FIRST PLOT ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
    
    # Contour plot of eta (initial)
    contour = ax.contourf(X, Y, eta[0, :, :], 
                          cmap='coolwarm',
                          levels=20, 
                          vmin=eta_min, vmax=eta_max)
    # Contour plot of bathymetry
    contour_lines = ax.contour(X, Y, Z, 
                               colors='black', linewidths=0.5) 
    
    ## Time text box
    ax.text(0.95, 0.05, "t = 0.0 s",
            transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
            fontsize=14, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  # Box styling
    
    ## Title
    ax.set_title(
        f"Barred Bathymetry with Channel\n"
        f"Cross-shore Width: {beach_CS_width:.2f} m\n"
        f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
        f"Bar Position: x = {x_bar:.2f} (m)\n"
        f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
        f"Channel Width (in Longshore): {channel_width:.2f} m",
        fontsize=10,   
        )
    
    # Axis Labels
    ax.set_xlabel('Cross-shore x (m)')
    ax.set_ylabel('Longshore y (m)')
    
    # Lines for wavemaker and sponge
    ax.axvline(Xc_WK,
               c='MidnightBlue',lw=2,ls='--',
               label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
    ax.axvline(Sponge_west_width,
               c='DarkGreen',lw=2,ls='--',
               label='Sponge')
    
    
    # Formatting
    ax.legend(loc='lower left')
    fig.tight_layout()
    ## [END] SET UP FIRST PLOT ----------------------------------------------------
    
    ## SET UP MOVIE WRITER --------------------------------------------------------          
    fr = speed/coarseness            
    stride = int(coarseness/0.1)
    width, height = fig.canvas.get_width_height()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(save_to_avi, fourcc, fr, (width, height))
    ## [END] SET UP MOVIE WRITER --------------------------------------------------
    
    ## ANIMATION LOOP -------------------------------------------------------------
    time_counter = 't = 0.0 s'
    
    # Loop through time at the desired stride
    for t_i in range(0, len(t), stride):
        print(f'\t\t\tplotting up to time {t[t_i]}')
    
        # Get eta
        eta_frame = ds['eta'].values[t_i, :, :]
    
        # Clear axes
        ax.clear()
    
        # Update eta contours
        contour = ax.contourf(X, Y, eta_frame, 
                              cmap='coolwarm',
                              levels=20, 
                              vmin=eta_min, vmax=eta_max)
        
        # Re-add bathy contours
        contour_lines = ax.contour(X, Y, Z, 
                                   colors='black', linewidths=0.5)
        ax.clabel(contour_lines, inline=True, fontsize=8, fmt="%.2f")
    
    
        # Update time counter
        if t_i%10 == 0:
            time_counter = f't = {t[t_i]:.2f} s'
            
        ax.text(0.95, 0.05, time_counter,
                transform=ax.transAxes,  # Places text relative to the axes (0 to 1)
                fontsize=14, 
                verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=1, edgecolor='black'))  
            
        # Re-add title
        ax.set_title(
            f"Barred Bathymetry with Channel\n"
            f"Cross-shore Width: {beach_CS_width:.2f} m\n"
            f"Depth Range: z $\\in$ [-{h_offshore:.2f},{h_onshore:.2f}] (m)\n"
            f"Bar Position: x = {x_bar:.2f} (m)\n"
            f"Bar Width (in Cross-shore): {bar_width:.2f} m\n"
            f"Channel Width (in Longshore): {channel_width:.2f} m",
            fontsize=10,   
            )
        
        # Re-add labels
        ax.set_xlabel('Cross-shore x (m)')
        ax.set_ylabel('Longshore y (m)')
        
        # Re-add lines for wavemaker and sponge
        ax.axvline(Xc_WK,c='MidnightBlue',lw=2,ls='--',label=f'Wavemaker a = {AMP_WK}, T = {Tperiod}')
        ax.axvline(Sponge_west_width,c='DarkGreen',lw=2,ls='--',label='Sponge')
        
        # Formatting
        ax.legend(loc='lower left')
        fig.tight_layout()
        
        # DRAW FRAME AND OUTPUT TO WRITER -----------------------------------------
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8).reshape((height, width, 4))
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        out.write(image)
        # [END] DRAW FRAME AND OUTPUT TO WRITER -----------------------------------
        
    ## [END] ANIMATION LOOP -------------------------------------------------------
    ## Release the video writer
    out.release()
    
    return out
