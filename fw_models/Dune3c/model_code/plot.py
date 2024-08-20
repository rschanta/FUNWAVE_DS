# Add to system path
import os
import sys
sys.path.append("/work/thsu/rschanta/RTS-PY")
import funwave_ds.fw_py as fpy
import funwave_ds.fw_ba as fwb
import numpy as np
import matplotlib.pyplot as plt

def plot_bathy(vars):
    print('\tStarted plotting bathymetry file...')

    # Unpack variables
    bathy_array = vars['bathy']['array']
    ITER = vars['ITER']
    DX = vars['DX']
    DY = vars['DY']
    Mglob = vars['Mglob']
    Nglob = vars['Nglob']
    Xc_WK = vars['Xc_WK']
    #Sponge_W = vars['Sponge_W']
    D3_trial = vars['D3_trial']

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths2()
    ptr = fpy.get_FW_tri_paths(ITER, p)

    
    
    # Get X and Z, plot
    X = bathy_array[:,0]
    Z = -bathy_array[:,1]
    plt.plot(X,Z,label='Bathymetry',color='black')

    # Add wavemaker and sponge
    plt.axvline(x=Xc_WK, color='red', linestyle='--', label='Wavemaker')
    #plt.axvline(x=Sponge_W, color='darkgreen', linestyle='--', label='West Sponge')

    # Title, legend, and text
    plt.title('INPUT BATHYMETRY: ' +  f'Dune 3 Trial: {D3_trial}')
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
    print(f'\tBathymetry file successfully saved to: {ptr["b_fig"]}\n')
    return 

def plot_TS_spectra(vars):
    print('\tStarted plotting spectra...')
    # Unpack variables
    per = vars['spectra']['per']
    enn = vars['spectra']['enn']
    cnn = vars['spectra']['cnn']
    ITER = vars['ITER']
    
    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths2()
    ptr = fpy.get_FW_tri_paths(ITER, p)

    

    # Plot period and amplitude
    plt.plot(per,enn)

    # Formatting
    plt.grid()
    plt.xlabel('Period (s)')
    plt.ylabel('Amplitude')
    plt.show()

    # Saving
    plt.savefig(ptr['sp_fig'], dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\tSpectra file successfully saved to: {ptr["sp_fig"]}\n')
    
    return