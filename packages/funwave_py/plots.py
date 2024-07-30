import numpy as np
import matplotlib.pyplot as plt

def plot_bathy(dicta,ptr):
    # Pull out params
    X = dicta['files']['bathy']['array'][:,0]
    Z = -dicta['files']['bathy']['array'][:,1]
    Xc_WK = dicta['Xc_WK']
    DX = dicta['DX']
    DY = dicta['DY']
    Mglob = dicta['Mglob']
    Nglob = dicta['Nglob']
    
        
    
    plt.plot(X,Z,label='Bathymetry',color='black')
    # Add wavemaker
    if 'WAVEMAKER' in dicta:
        plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    # Check sponge
    for key in ['DIRECT_SPONGE','FRICTION_SPONGE','DIFFUSION_SPONGE']:
            if key in dicta and dicta[key] == 'T':
                Sponge_W = dicta['Sponge_west_width']
                Sponge_E = dicta['Sponge_east_width']
                plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')
                plt.axvline(x=Sponge_E, color='lightgreen', linestyle='--', label='East Sponge')
                
    # Check if the key exists
    if 'ALT_TITLE' in dicta:
        plt.title('INPUT BATHYMETRY: ' + dicta['ALT_TITLE'] + '\n' + dicta['TITLE'] )
    else:
        plt.title('INPUT BATHYMETRY: ' +  dicta['TITLE'])
        
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    
    # Adjust the plot's x and y limits to make space for the textbox
    #plt.xlim(x.min(), x.max() + 2)
    plt.grid()
    plt.xlabel('Cross-shore Position (x)')
    plt.ylabel('Depth (z)')
    plt.legend()
    plt.savefig(ptr['b_fig'], dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return


def plot_TS_spectra(dicta,ptr):
    # Pull out params
    period = dicta['files']['spectra']['per']
    amp = dicta['files']['spectra']['cnn']
    peak = dicta['files']['spectra']['peak_per']
    num_comp = dicta['files']['spectra']['num_components']
    # Check if the key exists
    if 'ALT_TITLE' in dicta:
        plt.title('INPUT SPECTRA: ' + dicta['ALT_TITLE'] + '\n' + dicta['TITLE'] )
    else:
        plt.title('INPUT SPECTRA: ' + dicta['TITLE'])
    plt.plot(period,amp)
    
    plt.text(1.05, 0.5, f'Peak Period = {peak:.2f}\n Components = {num_comp}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Magnitude')
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return