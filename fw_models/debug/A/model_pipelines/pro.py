
## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_fs as fs
import xarray as xr



fpy.get_into_netcdf()
ptr = fpy.get_FW_tri_paths()


#%% Animation
static_variables = [
    {'key': 'Xc_WK', 'color': 'tomato', 'label': 'Wavemaker'},
    {'key': 'Sponge_west_width', 'color': 'dodgerblue', 'label': 'Sponge'},
]

dynamic_variables = [
    {'key': 'eta', 'coord': 'X', 'color': 'firebrick', 'label': 'eta'},
]

attribute_labels = ['D3_TRIAL', 'lo','hi','Sponge_west_width','Xc_WK']

animation_variables = {'coarseness': 0.5, 
                       'speed': 10,
                       'path': ptr['eta_ani'],
                       'title_string': f'Trial {ptr["num_str"]}', 
                       'ylabel': 'eta'}

ds = xr.load_dataset(ptr['nc_file'])

ptr = fpy.get_FW_tri_paths()
fs.create_animation(ds,static_variables,
                     dynamic_variables,
                     attribute_labels,
                     animation_variables)