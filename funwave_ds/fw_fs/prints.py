import os
import sys
import numpy as np

import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb


## PRINT BATHYMETRY
def print_bathy(vars):
    print('\t\tStarted printing bathymetry file (DEPTH_FILE)...')

    # Unpack variables
    DOM = vars['DOM']
    bathy_array = DOM['Z'].values.T
    ITER = int(vars['ITER'])

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    # Print
    np.savetxt(ptr['b_file'], bathy_array, delimiter=' ', fmt='%f')
    
    print(f'\t\tDEPTH_FILE file successfully saved to: {ptr["b_file"]}')
    return {'DEPTH_FILE': ptr['b_file']}


## PRINT SPECTRA
def print_TS_spectra(vars):
    print('\t\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    WKK = vars['WKK']
    per = WKK.coords['period'].values
    cnn = WKK['amp2'].values
    enn = WKK['phase2'].values
    ITER = vars['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    np.savetxt(ptr['sp_file'], np.column_stack((per, cnn, enn)), fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}