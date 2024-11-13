import xarray as xr
'''
This file contains the functions needed to extract the variables needed from
FUNWAVE output netcdf files for animation

    `unpack*` functions work to extract netcdf variables as needed
    `extract_variables_out` returns all of the variables needed
'''

#%% UNPACK VARIABLES BY XARRAY TYPE
# Coordinate Variables
def unpack_coords(ds,coord_list):
    coords_dict = {}
    for coord in coord_list:
        try:
            coords_dict[coord] = ds[coord].values   
        except:
            print(f'Warning: {coord} not found. Will not be displayed in animation.')
    return coords_dict

# Variables
def unpack_variables(ds,variable_list):
    variable_dict = {}
    for variable in variable_list:
        try:
            variable_dict[variable] = ds[variable].values   
        except:
            print(f'Warning: {variable} not found. Will not be displayed in animation.')
    return variable_dict

# Attributes
def unpack_attributes(ds,attr_list):
    attr_dict = {}
    for attr in attr_list:
        
        try:
            attr_dict[attr] = ds.attrs[attr]  
        except:
            print(f'Warning: {attr} not found. Will not be displayed in animation.')
    return attr_dict


 
#%% EXTRACT THE VARIABLES AS NEEDED
def extract_variables_out(ds,
                          static_variables, 
                          dynamic_variables, 
                          attribute_labels):
    
    # Get the coordinates
    all_variables = static_variables + dynamic_variables
    coord_list = list({var['coord'] for var in all_variables if 'coord' in var})
    coord_list = coord_list + ['Z','t_FW']
    
    # Get the variables
    var_list = list({var['key'] for var in dynamic_variables if 'key' in var})
    var_list = var_list + ['mask'] 

    # Unpack them and combine
    c_ = unpack_coords(ds,coord_list)                           
    v_ = unpack_coords(ds,var_list)                                     
    a_ = unpack_attributes(ds,attribute_labels)  
    variables  = {**c_, **v_, **a_}
    
    return variables