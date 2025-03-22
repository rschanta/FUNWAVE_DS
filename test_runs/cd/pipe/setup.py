import os
import funwave_ds as fds



#%% MAIN
d = fds.setup_key_dirs(name='Try1',
                   main_dir = './work//cd', 
                   input_dir = './lustre/cd/inputs', 
                   log_dir='./lustre/cd/logs',
                   bathy_dir = './lustre/cd/bathy',
                   station_dir = './lustre/cd/stations',
                   friction_dir= './lustre/cd/friction',
                   result_folder_dir = './lustre/cd/outputs_raw',
                   nc_dir = './lustre/cd/nc_files',
                   nc_sta_dir='./lustre/cd/nc_sta_files',
                   FW_ex = "./work/FW-STANDARD",
                   conda = "tf_env")

stuff_to_add = {'ba_fig': '/lustre/scratch/rschanta/test_runs/cd/fig_bathy/',
                'sp_fig': '/lustre/scratch/rschanta/test_runs/cd2/fig_spectra'}

env_file = '/work/thsu/rschanta/RTS-PY/test_runs/cd/envs/Try1.env'

fds.add_dirs_to_path(env_file,stuff_to_add) 