## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_fs as fs
import model_code as mod         # Model specific code
import xarray as xr


# Get into netcdf
#fpy.get_into_netcdf()

ptr = fpy.get_FW_tri_paths()

ds = xr.load_dataset(ptr['nc_file'])

ptr = fpy.get_FW_tri_paths()
mod.animate_eta(ds,save_to_avi=ptr['eta_ani'])
