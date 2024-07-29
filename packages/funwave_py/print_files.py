import copy
import numpy as np
#%% Print an input.txt file

def print_FW_in(dictionary, file_path):
    print('Started printing input.txt file...')
    dict1 = copy.deepcopy(dictionary)
    dict1.pop('files')
    with open(file_path, 'w') as file:
        for key, value in dict1.items():
            file.write(f"{key} = {value}\n")
    print(f'WaveCompFile successfully saved to: {file_path}')
    return
            
            
def print_time_series_spectra(data, path):
    print('Started printing WaveCompFile file...')
    
    # Pull out data
    per = data['per']
    enn = data['enn']
    cnn = data['cnn']
    
    # Save to file
    np.savetxt(path, np.column_stack((per, cnn, enn)), fmt='%12.8f')
    
    print(f'WaveCompFile successfully saved to: {path}')
    
    return


def print_bathy(data, path):

    print('Started printing Bathymetry file...')
    np.savetxt(path, data, delimiter=' ', fmt='%f')
    print(f'Bathymetry file successfully saved to: {path}')
    
    return