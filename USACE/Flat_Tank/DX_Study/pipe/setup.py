import os
import funwave_ds as fds



#%% MAIN
d = fds.setup_key_dirs(name='BASE1',
                   main_dir = '/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Study', 
                   input_dir = '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/inputs', 
                   log_dir='/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/logs',
                   bathy_dir = '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/bathy',
                   station_dir = '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/stations',
                   friction_dir= '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/friction',
                   result_folder_dir = '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/output_raw',
                   nc_dir = '/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/nc_files',
                   nc_sta_dir='/lustre/scratch/rschanta/USACE/Flat_Tank/DX_Study/nc_sta_files',
                   FW_ex = "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
                   conda = "tf_env")

