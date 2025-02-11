# Add to system path
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb


## BATHYMETRY PLOTS

def plot_1D_bathy(vars):
    print('\t\tStarted plotting bathymetry file...')

    #-----------------------------------------------------------------
    # Unpack Coordinate Objects
    DOM = vars['DOM']          
    # Coordinates
    X = DOM.coords['X']
    Y = DOM.coords['Y']
    # Variables
    Z = DOM['Z'].values
    # Attributes
    DX = DOM.attrs['DX']
    DY = DOM.attrs['DY']
    Mglob = DOM.attrs['Mglob']
    Nglob = DOM.attrs['Nglob']

    # Other
    ITER = vars['ITER']
    Xc_WK = vars['Xc_WK']
    Sponge_W = vars['Sponge_west_width']

    try:
        L = vars['L_']
        kh = vars['kh']
    except:
        pass
    #-----------------------------------------------------------------


    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = int(ITER))

    # Plot X and Z
    plt.plot(X,-Z[:,0],label='Bathymetry',color='black')

    # Add wavemaker and sponge
    plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')

    # Title, legend, and text
    try:
        plt.title('Input Bathymetry: ' +  f'Trial: {ITER} \n' + f'L: {L:.2f}' + f' kh: {kh:.2f}')
    except:   
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
    plt.savefig(ptr['b_fig'], dpi=200, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tBathymetry file successfully saved to: {ptr["b_fig"]}')
    return 



def plot_1D_bathy_FRF(vars):
    print('\t\tStarted plotting bathymetry file...')

    #-----------------------------------------------------------------
    # Unpack Coordinate Objects
    DOM = vars['DOM']          
    # Coordinates
    X = DOM.coords['X']
    Y = DOM.coords['Y']
    # Variables
    Z = DOM['Z'].values
    # Attributes
    DX = DOM.attrs['DX']
    DY = DOM.attrs['DY']
    Mglob = DOM.attrs['Mglob']
    Nglob = DOM.attrs['Nglob']

    # Other
    ITER = vars['ITER']
    Xc_WK = vars['Xc_WK']
    Sponge_W = vars['Sponge_west_width']
    date = vars['date']
    year = vars['year']
    month = vars['month']
    day = vars['day']
    try:
        L = vars['L_']
        kh = vars['kh']
    except:
        pass
    #-----------------------------------------------------------------


    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = int(ITER))

    # Plot X and Z
    plt.plot(X,-Z[:,0],label='Bathymetry',color='black')

    # Add wavemaker and sponge
    plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')

    # Title, legend, and text
    try:
        plt.title('Input Bathymetry: ' +  f'Trial: {ITER} \n' + f'L: {L:.2f}' + f' kh: {kh:.2f}')
    except:   
        plt.title('Input Bathymetry: ' +  f'Trial: {ITER}')
   
    plt.text(1.05, 0.5, f'DX = {DX:.2f} DY = {DY:.2f}\nMglob = {Mglob} Nglob = {Nglob}\nDATE: {date}', 
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
    plt.savefig(ptr['b_fig'], dpi=200, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tBathymetry file successfully saved to: {ptr["b_fig"]}')
    return 



## SPECTRAL PLOTS
def plot_TS_spectra(vars):
    print('\t\tStarted plotting spectra...')

    #-----------------------------------------------------------------
    WKK = vars['WKK']
    per = WKK.coords['period'].values
    amp = WKK['amp2'].values
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


## SPECTRAL PLOTS
def plot_WK_TIME_SERIES(vars):
    print('\t\tStarted plotting spectra...')

    #-----------------------------------------------------------------
    df_spectra = vars['df_spectra']
    per = df_spectra['per'].values
    amp = df_spectra['amp'].values
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