## FUNWAVE_DS Modules
import funwave_ds.fw_py as fpy
import sys
import os
from dotenv import load_dotenv
sys.path.append(r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\test_runs\d2')
load_dotenv(r'C:/Users/rschanta/OneDrive - University of Delaware - o365/Desktop/Research/FUNWAVE_DS/FUNWAVE_DS/test_runs/d2/envs/Try1.env')


#
dee = os.getenv('in')
tri_num = 5
lor = fpy.get_key_dirs(tri_num=tri_num)
# Get into netcdf
fpy.get_into_netcdf()