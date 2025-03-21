import os

def setup_key_dirs(name='NAME',
                    main_dir = None,
                    input_dir = None,
                    log_dir = None,
                    env_dir = None,
                    result_folder_dir = None,
                    batch_dir = None,
                    bathy_dir = None,
                    spectra_dir = None,
                    station_dir = None,
                    friction_dir = None,
                    breakwater_dir=None,
                    nc_dir = None,
                    nc_sta_dir = None,
                    conda = None,
                    FW_ex = None):
    
    
    # main_dir
    if main_dir is None:
        raise ValueError("`main_dir` must be specified")
    else:
        print(f'main_dir Directory set as: {main_dir}')
    
    # input.txt files
    if input_dir is None:
        raise ValueError("`input_dir` must be specified")
    else:
        print(f'Directory for input.txt files set to: {input_dir}')
        
    # RESULT_FOLDER files
    if result_folder_dir is None:
        raise ValueError("`result_folder_dir` must be specified")
    else:
        print(f'Directory for RESULT_FOLDER directories set to: {result_folder_dir}')
        
    # NetCDF
    if nc_dir is None:
        raise ValueError("`nc_dir` must be specified")
    else:
        print(f'Directory for NetCDF outputs set to: {nc_dir}')
        
    # Need NetCDF station directory if specified
    if station_dir:
        if nc_sta_dir is None:
            raise ValueError("`nc_sta_dir` must be specified")
        else:
            print(f'Directory for NetCDF outputs at stations set to: {nc_dir}')
            
    if log_dir is None:
        log_dir = os.path.join(main_dir,'logs')
        
    if env_dir is None:
        env_dir = os.path.join(main_dir,'envs')
    if batch_dir is None:
        batch_dir = os.path.join(main_dir,'batch_scripts')
    # Construct stuff within main_dir
    
    paths = {'in': input_dir,
             'or': result_folder_dir,
             'ba': bathy_dir,
             'sp': spectra_dir,
             'st': station_dir,
             'fr': friction_dir,
             'bw': breakwater_dir,
             'nc': nc_dir,
             'ns': nc_sta_dir,
             'main': main_dir,
             'batch': batch_dir,
             'envs': env_dir,
             'logs': log_dir,
             'FW_ex': FW_ex,
             'conda': conda,
             'PYTHONPATH': main_dir}
    
    
    # Make Directories
    for key,path_name in paths.items():
        if key not in {'FW_ex','conda','PYTHONPATH'}:
            if path_name:
                  print(f'\tSpecifying {key}: {path_name}')
                  os.makedirs(path_name, exist_ok=True)
            

    # Write to Environment File
    env_path = os.path.join(env_dir,f'{name}.env')
    with open(env_path, "w") as f:
        for key,path_name in paths.items():
            if path_name:
                f.write(f"{key}={path_name}\n")


    
    return paths

def add_dirs_to_path(env_file,dirs_to_add):
    with open(env_file, "a") as f:
        for key,path_name in dirs_to_add.items():
                f.write(f"{key}={path_name}\n")
                os.makedirs(path_name, exist_ok=True)


#%% MAIN
d = setup_key_dirs(name='Try1',
                   main_dir = '/work/thsu/rschanta/RTS-PY/test_runs/d2', 
                   input_dir = '/lustre/scratch/rschanta/test_runs/d2/inputs', 
                   result_folder_dir = '/lustre/scratch/rschanta/test_runs/d2/outputs_raw',
                   nc_dir = '/lustre/scratch/rschanta/test_runs/d2/nc_files',
                   FW_ex = "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
                   conda = "tf_env")

stuff_to_add = {'ba_fig': './lustre/DUNE3/Test1/fig/bathy',
                'sp_fig': './lustre/DUNE3/Test1/fig/spectra'}

env_file = '/work/thsu/rschanta/RTS-PY/test_runs/d2/envs/Try1.env'

add_dirs_to_path(env_file,stuff_to_add)  