import os
import sys
import numpy as np

import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb

'''
print_bathy
    - prints a DEPTH_FILE, assuming a numpy array that is the DEPTH_FILE
'''
def print_bathy(vars):
    print('\t\tStarted printing bathymetry file (DEPTH_FILE)...')
    # Unpack variables
    bathy_array = vars['bathy_file']
    ITER = int(vars['ITER'])

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    # Print
    np.savetxt(ptr['b_file'], bathy_array, delimiter=' ', fmt='%f')

    print(f'\t\tDEPTH_FILE file successfully saved to: {ptr["b_file"]}')
    return {'DEPTH_FILE': ptr['b_file']}


'''
print_bathy
    - prints a DEPTH_FILE, assuming a numpy array that is the DEPTH_FILE
'''
def print_bathy_nc(vars):
    print('\t\tStarted printing bathymetry file (DEPTH_FILE)...')

    # Unpack variables
    bathy_array = vars['DOM'].vars.Z.value.T
    ITER = int(vars['ITER'])

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    # Print
    np.savetxt(ptr['b_file'], bathy_array, delimiter=' ', fmt='%f')
    
    print(f'\t\tDEPTH_FILE file successfully saved to: {ptr["b_file"]}')
    return {'DEPTH_FILE': ptr['b_file']}


'''
print_TS_spectra
    - prints a time series spectra for WK_TIME_SERIES assuming
        some user-defined parameter `spectra` that is a dictionary
        with 'per', 'enn', 'cnn' arrays
'''
def print_TS_spectra(vars):
    print('\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    per = vars['spectra']['per']
    enn = vars['spectra']['enn']
    cnn = vars['spectra']['cnn']
    ITER = vars['ITER']
    
    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    # TODO: user-defined key in ptr
    np.savetxt(ptr['sp_file'], np.column_stack((per, cnn, enn)), fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}


'''
print_TS_spectra
    - prints a time series spectra for WK_TIME_SERIES assuming
        some user-defined parameter `spectra` that is a dictionary
        with 'per', 'enn', 'cnn' arrays
'''
def print_TS_spectra_new(vars):
    print('\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    spectra = vars['spectra_array'][:,1:]
    ITER = vars['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    # TODO: user-defined key in ptr
    np.savetxt(ptr['sp_file'], spectra, fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}



def print_TS_spectra_nc(vars):
    print('\t\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    WKK = vars['WKK']
    per = WKK.coords.per
    cnn = WKK.vars.amp.value
    enn = WKK.vars.phase.value
    ITER = vars['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    np.savetxt(ptr['sp_file'], np.column_stack((per, cnn, enn)), fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}