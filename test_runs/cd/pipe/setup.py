import os
import funwave_ds as fds



#%% MAIN
d = fds.setup_key_dirs(name='Fric1',
                   main_dir = '/work/thsu/rschanta/RTS-PY/test_runs/cd', 
                   input_dir = '/lustre/scratch/rschanta/test_runs/cd/inputs', 
                   log_dir='/lustre/scratch/rschanta/test_runs/cd/logs',
                   bathy_dir = '/lustre/scratch/rschanta/test_runs/cd/bathy',
                   station_dir = '/lustre/scratch/rschanta/test_runs/cd/stations',
                   friction_dir= '/lustre/scratch/rschanta/test_runs/cd/friction',
                   result_folder_dir = '/lustre/scratch/rschanta/test_runs/cd/output_raw',
                   nc_dir = '/lustre/scratch/rschanta/test_runs/cd/nc_files',
                   nc_sta_dir='/lustre/scratch/rschanta/test_runs/cd/nc_sta_files',
                   FW_ex = "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
                   conda = "tf_env")

