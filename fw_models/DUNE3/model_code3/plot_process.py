
'''
plot_process
    - Get the paths to the pickled data of Dune 3 Runs 5-24
        and pull out the bathymetry and MWL from the files
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import funwave_ds.fw_py as fpy

def plot_process(vars):
    print('\t\tStarted plotting the process...')

    # Unpack Variables
    raw_bathy = vars['raw_bathy']
    filt_bathy = vars['filt_bathy']
    FW_bathy = vars['bathy_array']
    Xc_WK = vars['Xc_WK']
    WGR = vars['WGR']
    MWLR = vars['MWLR']
    WGF = vars['WGF']
    XR = raw_bathy[:,0]
    ZR = raw_bathy[:,1]
    XF = filt_bathy[:,0]
    ZF = filt_bathy[:,1]
    X_FW = FW_bathy[:,0]
    Z_FW = FW_bathy[:,1]
    ITER = vars['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    plt.plot(XR,-ZR,label='Raw',color='blue')
    plt.plot(XF,-ZF,label='Filtered',color='red')
    plt.plot(X_FW,-Z_FW,label='FUNWAVE (Interpolated)',color='black')
    plt.grid()
    plt.title('Bathymetry: Original vs. Adjusted')
    plt.axvline(Xc_WK,ls=':',color='red',label='Wavemaker Gauge')
    plt.scatter(WGR,MWLR,color='blue',label='Wave Gauge Position (Raw)')
    plt.scatter(WGF,-0.5*np.ones(len(WGF)),label='Spectra Positions (Filtered)',color='red')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.75))
    plt.show()
    
    # Saving
    p = fpy.get_FW_paths()
    plt.savefig(f'{p["bF"]}/process_plot_{ITER}.png', dpi=300, bbox_inches='tight')
    
    # Close and exit
    plt.close()
    print(f'\t\tSuccessfully plotted data!')
    return {}



