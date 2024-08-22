# Add to system path
import os
import sys
import numpy as np
sys.path.append("/work/thsu/rschanta/RTS-PY")
import funwave_ds.fw_py as fpy
import funwave_ds.fw_ba as fwb


def print_bathy(vars):
    print('\tStarted printing bathymetry file (DEPTH_FILE)...')
    # Unpack variables
    bathy_array = vars['bathy']['file']
    ITER = int(vars['ITER'])

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    # Print
    np.savetxt(ptr['b_file'], bathy_array, delimiter=' ', fmt='%f')

    print(f'\tDEPTH_FILE file successfully saved to: {ptr["b_file"]}\n')
    return {'DEPTH_FILE': ptr['b_file']}


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
    np.savetxt(ptr['sp_file'], np.column_stack((per, cnn, enn)), fmt='%12.8f')
    print(f'\tWaveCompFile successfully saved to: {ptr["sp_file"]}\n')
    
    return {'WaveCompFile': ptr['sp_file']}