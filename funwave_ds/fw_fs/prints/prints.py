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


## PRINT STATION
def print_stations(var_dict):
    print('\t\tStarted printing station file (STATIONS_FILE)...')

    # Unpack variables
    DOM = var_dict['DOM']
    Mglob_pos = DOM['Mglob_gage'].values
    Nglob_pos = DOM['Nglob_gage'].values
    station_array = np.column_stack((Mglob_pos, Nglob_pos))
    station_array = station_array
    ITER = int(var_dict['ITER'])

    # Get directories
    d = fwb.get_directories()
    p = fpy.get_FW_paths()
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)

    # Print
    np.savetxt(ptr['st_file'], station_array, delimiter=' ', fmt='%d')
    
    print(f'\t\tSTATION file successfully saved to: {ptr["st_file"]}')
    return {'STATIONS_FILE': ptr['st_file']}



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

## PRINT SPECTRA
def print_WK_TIME_SERIES_SPECTRA(var_dict):
    print('\t\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    df_spectra = var_dict['df_spectra']
    per = df_spectra['per'].values
    amp = df_spectra['amp'].values
    pha = df_spectra['pha'].values
    ITER = var_dict['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    np.savetxt(ptr['sp_file'], np.column_stack((per, amp, pha)), fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}