import pickle
import shutil
import numpy as np
import pandas as pd
from itertools import product
## NOTE: The order in which these are imported DOES matter
# due to a tangled web of dependencies
import xarray as xr
from netCDF4 import Dataset
import h5py

import funwave_ds.fw_py as fpy
from pathlib import Path

#%% INPUT PROCESSING
def ensure_net_cdf_type(nc_data):
    '''
    Enforces type compatability for NETCDF
    '''
    print('\tStarting type enforcement on NETCDF')

    # Display Type
    #for var_name in nc_data.data_vars:
    #    print(f"Variable '{var_name}' has data type: {nc_data[var_name].dtype}")

    # Work through variables
    for var_name in nc_data.data_vars:
        if nc_data[var_name].dtype == 'float64':
            nc_data[var_name] = nc_data[var_name].astype('float32')
            #print(f"Converted '{var_name}' to float32")

    # Work through coordinates
    for coord_name in nc_data.coords:
        if nc_data.coords[coord_name].dtype == 'float64':
            nc_data.coords[coord_name] = nc_data.coords[coord_name].astype('float32')
            #print(f"Converted coordinate '{coord_name}' to float32")

    # Work through attributes
    for attr_name, attr_value in nc_data.attrs.items():
        if isinstance(attr_value, (float, np.float64)):
            nc_data.attrs[attr_name] = float(attr_value)  # Standardize to Python float
            #print(f"Converted attribute '{attr_name}' to float32")
        # Unsupported type: Convert to string
        elif not isinstance(attr_value, (str, int, float)):
            nc_data.attrs[attr_name] = str(attr_value)  
            print(f"\tUnsupported Type: Converted attribute '{attr_name}' to string")


    print('\tFinished type enforcement on NETCDF')
    return nc_data


def get_net_cdf(var_dict,ptr):
    '''
    Coerces input data into a NETCDF file
    '''
    print('\nStarted compressing data to NETCDF...')
    ## Initialization
    xr_datasets = []  # List of xarray objects
    non_nc_data = {}  # Dictionary of non-netcdf compatible variables                
    
    # Loop through all variables
    for key, value in var_dict.items():
        
        # If the value is an xarray Dataset, add it directly to the list
        if isinstance(value, xr.Dataset):
            xr_datasets.append(value)

            
        # If the value is incompatible with NetCDF, store in non_nc_data
        elif not isinstance(value, (int, float, str)):
            print(f"\tWarning: `{key}` is not a valid type for NetCDF storage. "
                  "It will be stored in a pickable dictionary instead.")
            non_nc_data[key] = value  # Add to non-NetCDF data dictionary

    ## Merge the dataset
    try:
        nc_data = xr.merge(xr_datasets)
    except ValueError as e:
        print("Error during merging: ", e)
        return None, non_nc_data  
    
    ## Add attributes as strings to the dataset
    for key, value in var_dict.items():
        if isinstance(value, (int, float, str)):
            nc_data.attrs[key] = value

    # Ensure type compatability for everything
    nc_data = ensure_net_cdf_type(nc_data)
    # Note: It's really finicky about the h5netcdf engine, this gets weird quickly
    nc_data.to_netcdf(ptr['nc_file'])
    
    print('NETCDF for input data successful!')
    return (nc_data, non_nc_data)



#%% OUTPUT PROCESSING

def load_array(var_XXXXX: Path, Mglob: int, Nglob: int):
    '''
        Loads in an array from a var_XXXXX binary output file or time_dt.txt
    '''
    
    try:
        # Deal with time_dt.txt separately: This is the only allowable ASCII file
        if var_XXXXX.name == 'time_dt.txt':
            return np.loadtxt(var_XXXXX,dtype=np.float32)
        # Everything else must be binary
        else:
            return np.fromfile(var_XXXXX, dtype=np.float32).reshape(Nglob,Mglob)

    # Pad with zeros otherwise if error
    except:
        print('Some issue with dimensions! Substitute with zeros to avoid crashing')
        return np.zeros((Nglob, Nglob))
    
    
    
def load_and_stack_to_tensors(Mglob,Nglob,all_var_dict):
    '''
        Loads in and stacks all the time series array outputs
        into a tensor
    '''

    tri_tensor_dict = {}
    
    # Loop through all variables
    for var, file_list in all_var_dict.items(): 
        print(f'\tCompressing: {var}')
        
        var_arrays = []
        # Loop through all files of this variable
        for file_path in file_list:
            var_array = load_array(file_path,Mglob,Nglob)
            var_arrays.append(var_array)
        
        # Form into tensor, squeeze out any extra dimensions
        try:
            var_tensor = np.squeeze(np.stack(var_arrays, axis=0))
            tri_tensor_dict[var] = var_tensor
        except:
            print('Issue!')
    return tri_tensor_dict



def get_into_netcdf():

    ptr = fpy.get_FW_tri_paths()
    

    # Get the NETCDF Data
    ds = xr.load_dataset(ptr['nc_file'])

    Mglob, Nglob = ds.attrs['Mglob'], ds.attrs['Nglob']
    
    # Get paths to outputs
    RESULT_FOLDER = (ptr['RESULT_FOLDER'])
    var_list = fpy.find_prefixes_path(RESULT_FOLDER)
    var_paths = fpy.get_vars_out_paths(RESULT_FOLDER, var_list)
    
    ## Get all outputs
    output_variables = load_and_stack_to_tensors(Mglob,Nglob,var_paths)
    for key in ['dep','dep_Xco','dep_Yco','time_dt']:
        output_variables.pop(key, None)
        
    ## Get time and add
    time_dt = np.loadtxt(ptr['t_file'])


    t_FW = time_dt[:,0]
    ds = ds.assign_coords({"t_FW": ("t_FW", t_FW)})

    
    ## Add other variables
    for var_name, var_value in output_variables.items():
        
        # TIME STEP FILES
        if (var_value.ndim == 3 and var_value.shape == (t_FW.size,Nglob,Mglob)):
            # Create variable with specified dimensions
            ds = ds.assign( {var_name: ( ['t_FW','Y','X'], var_value)})
        
        # TIME AVERAGE FILES
        elif (var_value.ndim == 3 and var_value.shape[1:] == (Nglob,Mglob)):
            # Create dimension if not there
            if "t_AVE" not in ds.coords:
                ave_dim = var_value.shape[0]
                t_AVE = np.arange(0,ave_dim)
                ds = ds.assign_coords({"t_AVE": ("t_AVE", t_AVE)})
                
            # Add variable
            ds = ds.assign( {var_name: ( ['t_AVE','Y','X'], var_value)})

    print('AND HERE TOO!')
    ds.to_netcdf(ptr['nc_file'],mode='w')
    print('NET-CDF Successfully saved!')
    return ds
