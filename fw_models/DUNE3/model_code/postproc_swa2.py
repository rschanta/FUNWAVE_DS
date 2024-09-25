
import numpy as np
import pandas as pd
import h5py

# Create a larger HDF5 file to store all trials
with h5py.File('/work/thsu/rschanta/DATA/DUNE3/SW1/databases/swash_ml_data.h5', 'w') as combined_hdf:
    for trial in range(1, 1261):  # Assuming 3 trials

        try:
            trial_filename = f'/work/thsu/rschanta/DATA/DUNE3/SW1/swash_ML/SWASH_{trial:05}.h5'
            
            # Open the individual trial file
            with h5py.File(trial_filename, 'r') as trial_hdf:
                # Create a group for each trial in the combined file
                trial_group = combined_hdf.create_group(f'tri_{trial:05}')
                
                # Copy datasets from the trial file to the group
                for dataset_name in trial_hdf.keys():
                    trial_group.create_dataset(dataset_name, data=trial_hdf[dataset_name][...])
                
                # Copy attributes from the trial file to the group
                for attr_name, attr_value in trial_hdf.attrs.items():
                    trial_group.attrs[attr_name] = attr_value
        except:
            print(f'Problem with Trial: {trial}')

print("Combined HDF5 file created successfully with all trials.")