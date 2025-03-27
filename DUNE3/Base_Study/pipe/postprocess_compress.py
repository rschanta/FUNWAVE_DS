import os 
import processing_code as pcode
import glob


# Get path to datasets
data_path = os.getenv('energy')
datasets = glob.glob(f'{data_path}/*nc')
# Run Compression
ds = pcode.compress_all_outputs(datasets)

# Construct name/path of output
base_path = os.getenv('processed')
file_name = 'processed_energy.nc'
file_path = os.path.join(base_path,file_name)

# Save out
ds.to_netcdf(file_path)