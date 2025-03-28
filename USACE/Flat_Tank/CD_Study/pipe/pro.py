## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import sys
import os
from dotenv import load_dotenv
import xarray as xr
import processing_code as pcode
#sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\test_runs\d2')
#load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/test_runs/d2/envs/Try1.env')


#fpy.get_into_netcdf()

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