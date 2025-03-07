import xarray as xr
import os

num = 5

base_path  = r'C:\Users\rschanta\DATABASE\Dune 3\Net_CDF'

dsf = xr.load_dataset(os.path.join(base_path,'filtered',f'Trial{num:02}.nc'))
dsr = xr.load_dataset(os.path.join(base_path,'raw',f'Trial{num:02}.nc'))