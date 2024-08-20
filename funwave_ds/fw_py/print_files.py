import copy
import numpy as np


def print_input_file(var_dict,ptr):
    print('\tStarted printing input file...')
    # Changed 8/19 to remove 'file' check and check by type instead
    var_dict_copy = copy.deepcopy(var_dict)
    with open(ptr['i_file'], 'w') as f:
        # Remove files
        for var_name, value in var_dict_copy.items():
            if isinstance(value, (str, int, float)):
                f.write(f"{var_name} = {value}\n")
    
    print(f"\tinput.txt file successfully saved to: {ptr['i_file']}\n", flush=True)
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

    print('\tStarted printing bthymetry file...')
    np.savetxt(path, data, delimiter=' ', fmt='%f')
    print(f'\tDEPTH_FILE file successfully saved to: {path}')
    
    return