import pandas as pd
import pickle
import numpy as np
import funwave_ds.fw_fs as fws
import funwave_ds.fw_py as fpy
def set_WAVEMAKER(vars):

    print('\t\tStarted setting wavemaker...')
    #----------------------------------------------------------------- 
    D3Object = vars['D3Object']   
    t = D3Object.coords.tD3
    eta = D3Object.vars.etaD3.value
    #-----------------------------------------------------------------
    # Make Wavemaker object and add Benjamin's Spectra
    WKK = fpy.WavemakerObject(vars) 
    '''
    WKK.add_1D_spectra(period= D3Object.coords.per,
                    amplitude= D3Object.vars.amplitude.value,
                    phase= D3Object.vars.phase.value)
    '''

    WKK.calc_time_series_1D(time=t,eta=eta,lo=0.1,hi=2.0)
    print(WKK.attrs.NumWaveComp)
    print('\t\tSuccessfully set wavemaker!')
    
    return {'WKK': WKK}