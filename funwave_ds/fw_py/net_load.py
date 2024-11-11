
import numpy as np
import xarray as xr
import funwave_ds.fw_py as fpy
from pathlib import Path
## Note: Both of these are needed to load in properly!
from netCDF4 import Dataset
import h5py

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
    print('GOT HERE!')
    ds = xr.load_dataset(ptr['nc_file'])
    print('AND HERE!')

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




