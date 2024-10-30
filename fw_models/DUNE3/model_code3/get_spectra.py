import pandas as pd
import pickle
import numpy as np
import funwave_ds.fw_fs as fws

def get_spectra(vars):
    print('\t\tStarted processing spectra data...')
    
    # Unpack Variables
    lo = vars['lo']                     # Lower Cutoff Frequency
    hi = vars['hi']                     # Upper Cutoff Frequency
    pickle_file = vars['pickle_file']
    
    # Open pickled file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
        f.close()
    
    ## Unpack variables from data
    t = data['filtered_data']['t']    
    t0 = data['filtered_data']['t0']  
    t_end = data['filtered_data']['t_end']     
    eta = data['filtered_data']['eta']    
    
    # Select which wave gauge to use
    eta = np.squeeze(eta[:,0])
    
    # Slice between start and end time, get to numpy
    teta = pd.DataFrame(t,index=t,columns=['time'])
    teta['eta'] = eta
    teta = teta.loc[t0:t_end]
    
    # Get the spectra, peak period, and number of wave components
    spectra = fws.calculate_spectra(teta,lo,hi)
    PeakPeriod = spectra.loc[spectra['amplitude'].idxmax(), 'period']
    NumWaveComp = len(spectra)
    spectra = spectra.to_numpy()

    print('\t\tSuccessfully processed spectra data!')
    
    return {'PeakPeriod': PeakPeriod,
            'NumWaveComp': int(NumWaveComp),
            'spectra_array': spectra}