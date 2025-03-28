import numpy as np
import xarray as xr
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

    # VARIABLES
    for var_name in nc_data.data_vars:
        # Make sure all floats are float32
        if nc_data[var_name].dtype == 'float64':
            nc_data[var_name] = nc_data[var_name].astype('float32')

    # COORDINATES
    for coord_name in nc_data.coords:
        # Make sure all floats are float32
        if nc_data.coords[coord_name].dtype == 'float64':
            nc_data.coords[coord_name] = nc_data.coords[coord_name].astype('float32')

    # ATTRIBUTES
    for attr_name, attr_value in nc_data.attrs.items():
        # If numeric, convert to float
        if isinstance(attr_value, (float, np.float64)):
            nc_data.attrs[attr_name] = float(attr_value)  

        # If anything else, coerce into string
        elif not isinstance(attr_value, (str, int, float)):
            nc_data.attrs[attr_name] = str(attr_value)  
            print(f"\tUnsupported Type: Converted attribute '{attr_name}' to string")


    print('\tFinished type enforcement on NETCDF')
    return nc_data


def get_net_cdf(var_dict):
    '''
    Coerces input data into a NETCDF file
    '''
    print('\nStarted compressing data to NETCDF...')
    
    # Initialize a list of xarray objects
    xr_datasets = []  

    # Loop through all variables
    for key, value in var_dict.items():
        # Make list of xarrays (ie- domain, spectra, etc.)
        if isinstance(value, xr.Dataset):
            xr_datasets.append(value)
        # Raise warning for things that aren't xarrays/ints/floats/strings
        elif not isinstance(value, (int, float, str)):
            print(f'Warning: {key} cannot be saved to NetCDF since it is of type {type(value)}')

    # Merge any datasets that may exist
    nc_data = xr.merge(xr_datasets) 
    
    # Add ints,floats,strings as attributes to the xarray
    for key, value in var_dict.items():
        if isinstance(value, (int, float, str)):
            nc_data.attrs[key] = value

    # Ensure type compatability for everything
    nc_data = ensure_net_cdf_type(nc_data)
    ITER = int(var_dict['ITER'])
    
    # Get the file path and save
    ptr = fpy.get_key_dirs(tri_num = ITER)
    nc_path = ptr['nc']
    nc_data.to_netcdf(nc_path)
    
    print('NETCDF for input data successful!')
    return nc_data



#%% OUTPUT PROCESSING

def load_array(var_XXXXX: Path, Mglob: int, Nglob: int):
    '''
        Loads in an array from a var_XXXXX binary output file or time_dt.txt
    '''
    
    try:
        # Deal with time_dt.txt separately: This is the only allowable ASCII file
        if var_XXXXX.name == 'time_dt.txt':
            return np.loadtxt(var_XXXXX,dtype=np.float32)
        elif var_XXXXX.name.startswith('sta_'):
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
    # Acess necessary paths
    ptr = fpy.get_key_dirs()

    # Get the NETCDF Created in the input phase
    ds = xr.load_dataset(ptr['nc'])
    # Get dimensions needed from inputs
    Mglob, Nglob = ds.attrs['Mglob'], ds.attrs['Nglob']

    # Stations
    try:
        NumberStations = ds.attrs['NumberStations']
    except:
        print('No stations specified')

    # Get paths to outputs
    RESULT_FOLDER = ptr['or']

    # Get list of all variables found in the result folder (eta, u, sta, time_dt, etc.)
    var_list = fpy.find_prefixes_path(RESULT_FOLDER)
    
    # Dictionary with keys for each variable type (eta,u,sta,etc.) and values a sorted list of all files
        # for each one (ie- {'eta': ['eta_00000','eta_00001', 'eta_00002' ...]})
    var_paths = fpy.get_vars_out_paths(RESULT_FOLDER, var_list)

    ## Get all outputs
    output_variables = load_and_stack_to_tensors(Mglob,Nglob,var_paths)
    
    # Pop off some problematic ones
    for key in ['dep','dep_Xco','dep_Yco','time_dt']:
        output_variables.pop(key, None)
        
    ## Get time and add
    time_dt = np.loadtxt(ptr['time_dt'])


    t_FW = time_dt[:,0]
    ds = ds.assign_coords({"t_FW": ("t_FW", t_FW)})

    
    ## Add other variables
    for var_name, var_value in output_variables.items():
        
        # TIME STEP FILES
        if (var_value.ndim == 3 and var_value.shape == (t_FW.size,Nglob,Mglob)):
            # Create variable with specified dimensions
            ds = ds.assign( {var_name: ( ['t_FW','Y','X'], var_value)})
        
        # STATION FILES
        elif (var_name=='sta'):
            print('\t\tCreating new NetCDF for stations...')
            print(var_value.shape)
            # Separate out eta,u,v
            t_station = np.squeeze(var_value[0,:,0])
            eta_station = np.squeeze(var_value[:,:,1])
            u_station = np.squeeze(var_value[:,:,2])
            v_station = np.squeeze(var_value[:,:,3])

            # Create a station NetCDF
            ds_station= xr.Dataset(
                coords={
                    'GAGE_NUM': ds.coords['GAGE_NUM'],  
                    't_station': ('t_station', t_station),
                    'X': ds.coords['X'],
                    'Y': ds.coords['Y'],
                },
                data_vars={
                    'eta_sta': (['GAGE_NUM', 't_station'], eta_station),
                    'u_sta': (['GAGE_NUM', 't_station'], u_station),
                    'v_sta': (['GAGE_NUM', 't_station'], v_station),
                    'Mglob_gage': (['GAGE_NUM'], ds['Mglob_gage'].values),
                    'Nglob_gage': (['GAGE_NUM'], ds['Nglob_gage'].values),
                    'Z': (['X','Y'], ds['Z'].values)  
                }
            )

            ds_station.attrs = ds.attrs.copy()
            # Save to netcdf
            ds_station.to_netcdf(ptr['ns'])
            print(f"Printed station .nc to {ptr['ns']}")

        # TIME AVERAGE FILES
        elif (var_value.ndim == 3 and var_value.shape[1:] == (Nglob,Mglob)):
            # Create dimension if not there
            if "t_AVE" not in ds.coords:
                ave_dim = var_value.shape[0]
                t_AVE = np.arange(0,ave_dim)
                ds = ds.assign_coords({"t_AVE": ("t_AVE", t_AVE)})
                
            # Add variable
            ds = ds.assign( {var_name: ( ['t_AVE','Y','X'], var_value)})

    # EDIT 3-17
    comp = dict(zlib=True, complevel=4)  # Compression level 1 (low) to 9 (high)
    encoding = {var: comp for var in ds.data_vars}  # Apply to all variables

    # Save to netcdf
    ds.to_netcdf(ptr['nc'],mode='w', encoding=encoding)
    print('NET-CDF Successfully saved!')
    return ds
