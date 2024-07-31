import copy
import sys
import os
import pickle
import numpy as np
from pathlib import Path

## Custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../packages')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model_runs')))
import funwave_py as fp
import time_spectra_a_f as ts


def generate_in(super_path,run_name,trial_path):
    # Open pickle
    with open(trial_path, 'rb') as file:
        # Load the pickled dictionary
        trial_dict = pickle.load(file)
        
    # Naming/Setup
    fp.mk_FW_dir(super_path,run_name)
    p = fp.list_FW_dirs(super_path,run_name)
    
    # Template to use and common parameters
    temp = fp.FW_in_bathy();

    tri = 1
    all_inps = {}
    
    for num in [1]:
        # Copy the template
        inp = copy.deepcopy(temp)
        
        # Get paths/names for trial
        ptr = fp.list_FW_tri_dirs(tri,p);
        
        # Set paths
        inp['TITLE'] = ptr['input_name']
        inp['ALT_TITLE'] = 'Dune 3 Trial 5: Spectral'
        inp['DEPTH_FILE'] = Path(ptr['b_file'])
        inp['WaveCompFile'] = Path(ptr['sp_file'])
        inp['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
        
        
        # Set Time parameters
        inp['PLOT_INTV'] = 1.0
        inp['TOTAL_TIME'] = 75.0
        
        # Get spectra 
        spectra = fp.get_TS_spectra(trial_dict['filtered_data']['t'],trial_dict['filtered_data']['eta'][:,0],0.1 ,2)
        inp['files'] = {}
        inp['files']['spectra'] = spectra 
        
        # Calculate stability criteria
        L, DX, h,Xc_WK = ts.get_stability_limits(trial_dict,spectra['peak_per'])
        
        # Get bathy
        bathy = ts.prep_D3_bathy_trial_5(trial_dict,DX)
        inp['files']['bathy'] = bathy 
        
        # Set spatial parameters
        inp['DX'] = DX
        inp['DY'] = DX
        inp['Mglob'] = np.size(bathy['file'],1)
        inp['Nglob'] = np.size(bathy['file'],0)
        
        # Set sponge
        inp['FRICTION_SPONGE'] = 'F'
        inp['DIRECT_SPONGE'] = 'F'
        inp['Sponge_west_width'] = 0.0

        # Set Wavemaker parameters
        inp['WAVEMAKER'] = 'WK_TIME_SERIES'
        inp['Xc_WK'] = Xc_WK
        inp['DEP_WK'] = h
        inp['NumWaveComp'] = spectra['num_components']
        inp['PeakPeriod'] = spectra['peak_per']
        inp['GammaTMA'] = 3.3
        
        # Print input files
        fp.print_FW_in(inp,ptr['i_file']);
        fp.print_time_series_spectra(spectra,ptr['sp_file'])
        fp.print_bathy(bathy['file'],ptr['b_file'])
        
        # Make plots
        fp.plot_bathy(inp,ptr)
        fp.plot_TS_spectra(inp,ptr)
        
        # Save to larger input dict
        all_inps[ptr['tri_name']] = inp
        tri = tri + 1

    # Save out dictionary of inputs
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_inps, f)
        
    return all_inps
