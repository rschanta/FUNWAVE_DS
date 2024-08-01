import copy
import sys
import os
import pickle
import numpy as np
from pathlib import Path

## Custom modules
import python_code as fp



def generate_in(super_path,run_name,tri_path):
    
    # Naming/Setup
    fp.py.mk_FW_dir(super_path,run_name)
    p = fp.py.list_FW_dirs(super_path,run_name)
    
    # Template to use and common parameters
    temp = fp.py.FW_in_bathy();

    tri = 1
    all_inps = {}
    
    for tri_num in range(5,25):
        print(f'Started Generation for Trial: {tri_num}', flush=True)
        # Open pickle
        trial_path = f'{tri_path}Trial{tri_num:02}.pkl'
        with open(trial_path, 'rb') as file:
            # Load the pickled dictionary
            trial_dict = pickle.load(file)
        
        
        
        # Set paths
        for AMP in np.linspace(0.2,0.5,7):
            for PER in np.linspace(4,12,9):
                # Copy the template
                inp = copy.deepcopy(temp)
                
                # Get paths/names for trial
                ptr = fp.py.list_FW_tri_dirs(tri,p)
                inp['TITLE'] = ptr['input_name']
                inp['ALT_TITLE'] = trial_dict['filtered_data']['trial_name']
                inp['DEPTH_FILE'] = Path(ptr['b_file'])
                #inp['WaveCompFile'] = Path(ptr['sp_file'])
                inp['RESULT_FOLDER'] = ptr['RESULT_FOLDER']
        
        
                # Set Time parameters
                inp['PLOT_INTV'] = 0.05
                inp['TOTAL_TIME'] = 400
        
                # Get spectra 
                #spectra = fp.py.get_TS_spectra(trial_dict['filtered_data']['t'],trial_dict['filtered_data']['eta'][:,0],0.1 ,2)
                inp['files'] = {}
                #inp['files']['spectra'] = spectra 
        
                # Calculate stability criteria
                L, DX, h,Xc_WK = fp.mr.test1.get_stability_limits(trial_dict,PER)
                
                # Get bathy
                bathy = fp.mr.test1.prep_D3_bathy_trial_5(trial_dict,DX,L)
                inp['files']['bathy'] = bathy 
        
                # Set spatial parameters
                inp['DX'] = DX
                inp['DY'] = DX
                inp['Mglob'] = np.size(bathy['file'],1)
                inp['Nglob'] = np.size(bathy['file'],0)
        
                # Set sponge
                inp['FRICTION_SPONGE'] = 'T'
                inp['DIRECT_SPONGE'] = 'T'
                inp['Sponge_west_width'] = L

                # Set Wavemaker parameters
                inp['WAVEMAKER'] = 'WK_REG'
                inp['Xc_WK'] = 2*L
                inp['DEP_WK'] = h
                inp['AMP_WK'] = AMP
                inp['Tperiod'] = PER
                #inp['NumWaveComp'] = spectra['num_components']
                #inp['PeakPeriod'] = spectra['peak_per']
                #inp['GammaTMA'] = 3.3
        
                # Print input files
                fp.py.print_FW_in(inp,ptr['i_file']);
                #fp.py.print_time_series_spectra(spectra,ptr['sp_file'])
                fp.py.print_bathy(bathy['file'],ptr['b_file'])
                
                # Make plots
                fp.py.plot_bathy(inp,ptr)
                #fp.py.plot_TS_spectra(inp,ptr)
                
                # Save to larger input dict
                all_inps[ptr['tri_name']] = inp
                tri = tri + 1


        print(f'Finished Generation for Trial: {tri_num}', flush=True)

    # Save out dictionary of inputs
    with open(p['Id'], 'wb') as f:
        pickle.dump(all_inps, f)
        
    return all_inps
