## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import sys
import os
from dotenv import load_dotenv
## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import funwave_ds.fw_py as fpy
import processing_code as pcode
import xarray as xr
import os
# Get into NetCDF -------------------------------------------------------------
fpy.get_into_netcdf()
# -----------------------------------------------------------------------------


# Post-process -------------------------------------------------------------
ptr = fpy.get_key_dirs()

# Get outputs at station files
ds = xr.load_dataset(ptr['ns'])

# Apply energy processing code
ds = pcode.clean_and_interpolate(ds)
ds = pcode.calculate_spectra(ds,50)

# Get base path and tri_num from environment
base_path = os.getenv('energy')
tri_num = int(os.getenv('TRI_NUM'))

# Name/path of file
file_name = f'nc_energy_{tri_num:05}.nc'
file_path = os.path.join(base_path,file_name)

# Save out
ds.to_netcdf(file_path)
# Post-process -------------------------------------------------------------