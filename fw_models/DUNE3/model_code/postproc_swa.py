"""
Purpose- do the postprocessing steps needed to give the inputs/outputs to 
Venky for time series prediction
"""

import funwave_ds.fw_tf as ftf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import h5py
import os


def process_trial(tri_num):
    #%% Parse out needed variables
    data = ftf.parse_spec_var([f'/work/thsu/rschanta/DATA/DUNE3/SW1/fw_outputs/Out_{tri_num:05}.tfrecord'],
                       tensors_3D=['eta','mask','dep'],
                       tensors_2D = ['time_dt'],
                       floats=['Xc_WK','DX','D3_trial','Tperiod','AMP_WK'],
                       ints=['Mglob'])
    
    #%% Pull out variables
    Xc_WK = data[f'tri_{tri_num:05}']['Xc_WK']
    DX = data[f'tri_{tri_num:05}']['DX']
    Mglob = data[f'tri_{tri_num:05}']['Mglob']
    eta = data[f'tri_{tri_num:05}']['eta']
    mask = data[f'tri_{tri_num:05}']['mask']
    dep = data[f'tri_{tri_num:05}']['dep']
    time_dt = data[f'tri_{tri_num:05}']['time_dt']
    D3_trial = data[f'tri_{tri_num:05}']['D3_trial']
    Tperiod = data[f'tri_{tri_num:05}']['Tperiod']
    AMP_WK = data[f'tri_{tri_num:05}']['AMP_WK']
    
    #%% Apply masks and cut to 1D
    eta[mask==0]= np.nan
    eta_1D = eta[:,1,:]
    eta_wet = eta_1D[:, ~np.isnan(eta_1D).any(axis=0)]
    
    #%% Get time
    t = time_dt[:,0]
    
    #%% Get time series at the wavemaker
    i_WK = int(Xc_WK/DX)
    eta_WK = eta_1D[:,i_WK]
    
    
    #%% Get time series at the swash
    eta_SW = eta_wet[:,-1]
    # Find eta minimum
    SW_min_i = np.argmin(eta_SW)
    SW_start_t = t[SW_min_i]
    # Cut off time series and eta
    t_SW = t[SW_min_i:]
    eta_SW = eta_SW[SW_min_i:]
    
    #%% Make dataframes
    WK_series = pd.DataFrame({'time': t, 'eta_WK': eta_WK})
    SW_series = pd.DataFrame({'time': t_SW, 'eta_SW': eta_SW})
    
    #%% Get bathymetry
    bathyZ = dep[0,1,:]


    with h5py.File(f'/work/thsu/rschanta/DATA/DUNE3/SW1/swash_ML/SWASH_{tri_num:05}.h5', 'w') as hdf:
            hdf.create_dataset('WK_series', data=WK_series.values)
            hdf.create_dataset('SW_series', data=SW_series.values)
            hdf.create_dataset('bathyZ', data=bathyZ)
            hdf.attrs['Tperiod'] = Tperiod
            hdf.attrs['AMP_WK'] = AMP_WK
            hdf.attrs['D3_trial'] = D3_trial
            hdf.attrs['DX'] = DX
            hdf.attrs['SW_start_t'] = SW_start_t
            
    return

tri_num = int(os.getenv('TRI_NUM'))
#%% Test out
process_trial(tri_num)