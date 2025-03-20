## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_fs as fs
import model_code as mod         # Model specific code
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Get into netcdf
fpy.get_into_netcdf()

ptr = fpy.get_FW_tri_paths()

ds = xr.load_dataset(ptr['nc_file'])

#%% Load Dataset
#ds = xr.load_dataset('tri_00001.nc')
mod.animate_eta(ds,save_to_avi=ptr['u_ani'])
mod.animate_eta(ds,save_to_avi=ptr['v_ani'])
mod.animate_eta(ds,save_to_avi=ptr['eta_ani'])


