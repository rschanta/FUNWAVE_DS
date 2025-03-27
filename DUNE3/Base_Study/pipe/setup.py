import os
import funwave_ds as fds



#%% MAIN
stuff_to_add = {'ba_fig': './lustre/DUNE3/Base_Study/fig_bathy/',
                'sp_fig': './lustre/DUNE3/Base_Study/fig_spectra'}

d = fds.setup_key_dirs(name='BASE1',
                   main_dir = './work/DUNE3/Base_Study', 
                   input_dir = './lustre/DUNE3/Base_Study/inputs', 
                   log_dir='./lustre/DUNE3/Base_Study/logs',
                   bathy_dir = './lustre/DUNE3/Base_Study/bathy',
                   station_dir = './lustre/DUNE3/Base_Study/stations',
                   friction_dir= './lustre/DUNE3/Base_Study/friction',
                   result_folder_dir = './lustre/DUNE3/Base_Study/output_raw',
                   nc_dir = './lustre/DUNE3/Base_Study/nc_files',
                   nc_sta_dir='./lustre/DUNE3/Base_Study/nc_sta_files',
                   FW_ex = "./work/funwave/FW_ds/executables/FW-STANDARD",
                   conda = "tf_env",
                   dir_add_ons = stuff_to_add)

