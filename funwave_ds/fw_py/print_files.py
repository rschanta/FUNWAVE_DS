import copy
import numpy as np


def print_input_file(var_dict,ptr):
    var_dict_copy = copy.deepcopy(var_dict)
    with open(ptr['i_file'], 'w') as f:
        # Remove files
        if 'files' in var_dict_copy:
            del var_dict_copy['files']
        for var_name, value in var_dict_copy.items():
            f.write(f"{var_name} = {value}\n")
    
    print(f"Generated file: {ptr['i_file']}", flush=True)
    return     
            
def print_time_series_spectra_file(data, path):
    print('Started printing WaveCompFile file...')
    
    # Pull out data
    per = data['per']
    enn = data['enn']
    cnn = data['cnn']
    
    # Save to file
    np.savetxt(path, np.column_stack((per, cnn, enn)), fmt='%12.8f')
    
    print(f'WaveCompFile successfully saved to: {path}')
    
    return


def print_bathy_file(data, path):

    print('Started printing Bathymetry file...')
    np.savetxt(path, data, delimiter=' ', fmt='%f')
    print(f'Bathymetry file successfully saved to: {path}')
    
    return