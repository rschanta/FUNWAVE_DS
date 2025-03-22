import os

## PATH SETUP
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
                    input_sum_dir = None,
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

    # Default directories that need to exist
    if log_dir is None:
        log_dir = os.path.join(main_dir,'logs')
        
    if env_dir is None:
        env_dir = os.path.join(main_dir,'envs')
    if batch_dir is None:
        batch_dir = os.path.join(main_dir,'batch_scripts')
        
    if input_sum_dir is None:
        input_sum_dir = os.path.join(main_dir,'input_sum')

    
    # Construct stuff within main_dir
    
    paths = {'in': input_dir,
             'is': input_sum_dir,
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
             'name': name,
             'PYTHONPATH': main_dir}
    
    
    # Make Directories
    for key,path_name in paths.items():
        if key not in {'FW_ex','conda','PYTHONPATH','name'}:
            if path_name:
                  print(f'\tSpecifying {key}: {path_name}')
                  os.makedirs(path_name, exist_ok=True)
            

    # Write to Environment File
    env_path = os.path.join(env_dir,f'{name}.env')
    print(env_path)
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
## WITHIN EACH

def get_key_dirs(tri_num=None):
    if tri_num is None:
        tri_num = os.getenv('TRI_NUM')
        
    # Get the base path files
    base_paths = {}
    for file_type in ['in','ba','or','sp','st','fr','bw','nc','ncs']:
        base_path = os.getenv(file_type)
        if base_path:
            base_paths[file_type] = base_path
    
    # Specify file names and extensions of the key files
    name_ext = {'in': ['input','.txt'], 
          'ba': ['bathy','.txt'],
          'or': ['out_raw','/'],
          'sp': ['spectra','.txt'],
          'nc': ['tri','.nc'],
          'ns': ['tri_sta_','.nc']
          }
    
    # Construct the path
    trial_paths = {}
    for key,name_ext in name_ext.items():
        if key in base_paths:
                name = f'{name_ext[0]}_{tri_num:05}{name_ext[1]}'
                trial_paths[key] = os.path.join(base_paths[key],name)

    # Add on time_dt
    trial_paths['time_dt'] = os.path.join(f"{trial_paths['or']}","time_dt.txt")
        
    return trial_paths