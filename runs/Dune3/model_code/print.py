# Add to system path
import os
import sys
import numpy as np
sys.path.append("/work/thsu/rschanta/RTS-PY")
import funwave_ds.fw_py as fpy

def print_bathy(vars):
    # Unpack variables
    bathy_array = vars['bathy']['file']
    super_path = vars['super_path']
    run_name = vars['run_name']
    ITER = vars['ITER']

    fpy.make_FW_paths(super_path, run_name)
    p = fpy.get_FW_paths(super_path, run_name)
    ptr = fpy.get_FW_tri_paths(ITER, p)

    # Print
    print('Started printing Bathymetry file...')
    np.savetxt(ptr['b_file'], bathy_array, delimiter=' ', fmt='%f')
    print(f'Bathymetry file successfully saved to: {ptr["b_file"]}')
    return {'DEPTH_FILE': ptr['b_file']}


def print_time_series_spectra_file(vars):
    # Unpack variables
    per = vars['spectra']['per']
    enn = vars['spectra']['enn']
    cnn = vars['spectra']['cnn']
    ITER = vars['ITER']
    super_path = vars['super_path']
    run_name = vars['run_name']
    
    print('Started printing WaveCompFile file...')

    fpy.make_FW_paths(super_path, run_name)
    p = fpy.get_FW_paths(super_path, run_name)
    ptr = fpy.get_FW_tri_paths(ITER, p)
    # Save to file
    np.savetxt(ptr['sp_file'], np.column_stack((per, cnn, enn)), fmt='%12.8f')
    
    print(f'WaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}