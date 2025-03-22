
import numpy as np

import funwave_ds.fw_py as fpy
import funwave_ds.fw_hpc as fwb

## PRINT BATHYMETRY
def print_bathy(vars):
    print('\t\tStarted printing bathymetry file (DEPTH_FILE)...')

    # Unpack variables
    bathy_array = vars['DOM']['Z'].values.T
    ITER = int(vars['ITER'])

    # Get path for bathymetry file- this is DEPTH_FILE
    ptr = fpy.get_key_dirs(tri_num = ITER)
    bathy_path = ptr['ba']

    # Print
    np.savetxt(bathy_path, bathy_array, delimiter=' ', fmt='%f')
    
    print(f'\t\tDEPTH_FILE file successfully saved to: {bathy_path}')
    return {'DEPTH_FILE': bathy_path}

## PRINT FRICTION
def print_friction(vars):
    print('\t\tStarted printing friction file (FRICTION_FILE)...')

    # Unpack variables
    friction_array = vars['DOM']['friction'].values.T
    ITER = int(vars['ITER'])

    # Get path for bathymetry file- this is DEPTH_FILE
    ptr = fpy.get_key_dirs(tri_num = ITER)
    friction_path = ptr['fr']

    # Print
    np.savetxt(friction_path, friction_array, delimiter=' ', fmt='%f')
    
    print(f'\t\tFRICTION_FILE file successfully saved to: {friction_path}')
    return {'FRICTION_FILE': friction_path}


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
    # Get path for bathymetry file- this is DEPTH_FILE
    ptr = fpy.get_key_dirs(tri_num = ITER)
    station_path = ptr['st']

    # Print
    np.savetxt(station_path, station_array, delimiter=' ', fmt='%d')
    
    print(f'\t\tSTATION file successfully saved to: {station_path}')
    return {'STATIONS_FILE':station_path}



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
'''
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
'''

## PRINT SPECTRA
def print_WK_TIME_SERIES_SPECTRA(var_dict):
    print('\t\tStarted printing spectra file (WaveCompFile)...')
    
    # Unpack variables
    WKK = var_dict['WK_Object']
    per = WKK['period'].values
    amp = WKK['amp'].values
    pha = WKK['phase'].values
    ITER = var_dict['ITER']
    
    # Get directories
    ptr = fpy.get_FW_tri_paths(tri_num = ITER)
    
    # Print
    np.savetxt(ptr['sp_file'], np.column_stack((per, amp, pha)), fmt='%12.8f')
    print(f'\t\tWaveCompFile successfully saved to: {ptr["sp_file"]}')
    
    return {'WaveCompFile': ptr['sp_file']}