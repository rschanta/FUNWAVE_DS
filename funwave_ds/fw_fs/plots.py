# Add to system path
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb

def plot_1D_bathy(vars):
    print('\t\tStarted plotting bathymetry file...')

    # Unpack variables
    bathy_array = vars['bathy_array']
    ITER = vars['ITER']
    DX = vars['DX']
    DY = vars['DY']
    Mglob = vars['Mglob']
    Nglob = vars['Nglob']
    Xc_WK = vars['Xc_WK']
    Sponge_W = vars['Sponge_west_width']

    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = int(ITER))

    
    
    # Get X and Z, plot
    X = bathy_array[:,0]
    Z = -bathy_array[:,1]
    plt.plot(X,Z,label='Bathymetry',color='black')

    # Add wavemaker and sponge
    plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')

    # Title, legend, and text
    plt.title('Input Bathymetry: ' +  f'Trial: {ITER}')
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    plt.legend()

    # Formatting
    plt.grid()
    plt.xlabel('Cross-shore Position (x)')
    plt.ylabel('Depth (z)')
    plt.show()

    # Saving
    plt.savefig(ptr['b_fig'], dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tBathymetry file successfully saved to: {ptr["b_fig"]}')
    return 

def plot_1D_bathy_nc(vars):
    print('\t\tStarted plotting bathymetry file...')
    #-----------------------------------------------------------------
    # Unpack Coordinate Objects
    DOM = vars['DOM']           # Domain Object
    # Coordinates
    X = DOM.coords.X
    Y = DOM.coords.Y
    # Variables
    Z = DOM.vars.Z.value
    # Attributes
    DX = DOM.attrs.DX
    DY = DOM.attrs.DY
    Mglob = DOM.attrs.Mglob
    Nglob = DOM.attrs.Nglob

    # Other
    ITER = vars['ITER']
    Xc_WK = vars['Xc_WK']
    Sponge_W = vars['Sponge_west_width']

    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = int(ITER))

    
    
    # Plot X and Z
    plt.plot(X,-Z,label='Bathymetry',color='black')

    # Add wavemaker and sponge
    plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')

    # Title, legend, and text
    plt.title('Input Bathymetry: ' +  f'Trial: {ITER}')
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}', 
             fontsize=12, 
             bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.5'),
             transform=plt.gca().transAxes,
             verticalalignment='center')
    plt.legend()

    # Formatting
    plt.grid()
    plt.xlabel('Cross-shore Position (x)')
    plt.ylabel('Depth (z)')
    plt.show()

    # Saving
    plt.savefig(ptr['b_fig'], dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tBathymetry file successfully saved to: {ptr["b_fig"]}')
    return 


'''
plot_TS_spectra
    - plots a time series spectra, for WK_TIME_SERIES assuming
        some user-defined parameter `spectra` that is a dictionary
        with 'per', 'enn', 'cnn' arrays
'''

'''
plot_TS_spectra
    - plots a time series spectra, for WK_TIME_SERIES assuming
        some user-defined parameter `spectra` that is a dictionary
        with 'per', 'enn', 'cnn' arrays
'''
def plot_TS_spectra_new(vars):
    print('\t\tStarted plotting spectra...')
    #-----------------------------------------------------------------
    per = vars['spectra_array'][:,1]
    cnn = vars['spectra_array'][:,2]
    ITER = vars['ITER']
    
    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    

    # Plot period and amplitude
    plt.plot(per,cnn)

    # Formatting
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Amplitude')
    plt.title('Input Spectra: ' +  f'Trial: {ITER}')
    plt.show()

    # Saving
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tSpectra file successfully saved to: {ptr["sp_fig"]}')
    
    return



def plot_TS_spectra_nc(vars):
    print('\t\tStarted plotting spectra...')

    #-----------------------------------------------------------------
    WKK = vars['WKK']
    per = WKK.coords.period
    amp = WKK.vars.amp2.value
    ITER = vars['ITER']
    #-----------------------------------------------------------------


    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    

    # Plot period and amplitude
    plt.plot(per,amp)

    # Formatting
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Amplitude')
    plt.title('Input Spectra: ' +  f'Trial: {ITER}')
    plt.show()

    # Saving
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tSpectra file successfully saved to: {ptr["sp_fig"]}')
    
    return