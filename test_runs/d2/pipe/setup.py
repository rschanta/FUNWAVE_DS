import os
import funwave_ds as fds



#%% MAIN
d = fds.setup_key_dirs(name='Try1',
                   main_dir = '/work/thsu/rschanta/RTS-PY/test_runs/d2', 
                   input_dir = '/lustre/scratch/rschanta/test_runs/d2/inputs', 
                   log_dir='/lustre/scratch/rschanta/test_runs/d2/logs',
                   bathy_dir = '/lustre/scratch/rschanta/test_runs/d2/bathy',
                   friction_dir= '/lustre/scratch/rschanta/test_runs/d2/friction',
                   result_folder_dir = '/lustre/scratch/rschanta/test_runs/d2/outputs_raw',
                   nc_dir = '/lustre/scratch/rschanta/test_runs/d2/nc_files',
                   FW_ex = "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
                   conda = "tf_env")

stuff_to_add = {'ba_fig': '/lustre/scratch/rschanta/test_runs/d2/fig_bathy/',
                'sp_fig': '/lustre/scratch/rschanta/test_runs/d2/fig_spectra'}

env_file = '/work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env'

fds.add_dirs_to_path(env_file,stuff_to_add)  