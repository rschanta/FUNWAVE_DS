'''
    path_tools
        - Any function that deals with the getting of paths, the making of
            directories, finding what is in a directory, and similar 
            operations
            - All function names end with "path(s)" and begin with either:
                - "get"
                - "make"
                - "find"
                or something similarly descriptive

'''

import os
from pathlib import Path
from typing import  Dict, Any, Optional
from pathlib import Path
import funwave_ds.fw_py as fpy
import funwave_ds.fw_ba as fwb

#%% Path functions from global key variables
def get_FW_paths():
    """
    Returns a dictionary with all the paths associated with a FUNWAVE run within the super_path directory.

    Arguments:
    - super_path: Path to the super directory.
    - run_name: Name of the FUNWAVE run.

    Returns:
    - p: Dictionary containing all paths.
    """

    d = fwb.get_directories()
    temp_dir = d['TEMP_DIR']
    data_dir = d['DATA_DIR']
    fw_model = d['FW_MODEL']
    run_name = d['RUN_NAME']

    ##
    p = {'TD': temp_dir,
        'RN': os.path.join(temp_dir, fw_model, run_name),
        'RN_str': run_name,

        ###################################################################
        # Files to go to temp_dir (intended to eventually be deleted)
        ###################################################################
        # INPUTS: `input.txt` TEXT FILES 
        'i': os.path.join(temp_dir, fw_model, run_name, 'inputs'),
        'i_': os.path.join(temp_dir, fw_model, run_name, 'inputs', 'input_'),
        # OUTPUTS: DIRECTORY FOR RAW TIME SERIES OUTPUT
        'o': os.path.join(temp_dir, fw_model, run_name, 'outputs-raw'),
        'o_': os.path.join(temp_dir, fw_model, run_name, 'outputs-raw', 'out_'),
        # BATHYMETRY FILES
        'b': os.path.join(temp_dir, fw_model, run_name, 'bathy'),
        'b_': os.path.join(temp_dir, fw_model, run_name, 'bathy', 'bathy_'),
        # SPECTRA FILES
        'sp': os.path.join(temp_dir, fw_model, run_name, 'spectra'),
        'sp_': os.path.join(temp_dir, fw_model, run_name, 'spectra', 'spectra_'),

        ###################################################################
        # Files to go to data_dir (intended to keep)
        ###################################################################
        # INPUTS: PROCESSED INPUT FILES
        'I': os.path.join(data_dir, fw_model, run_name, 'inputs-proc'),
        'Id': os.path.join(data_dir, fw_model, run_name, 'inputs-proc', 'In_d.pkl'),
        'Im': os.path.join(data_dir, fw_model, run_name, 'inputs-proc', 'Im.csv'),
        'If': os.path.join(data_dir, fw_model, run_name, 'inputs-proc', 'If.csv'),
        # OUTPUTS: DIRECTORY FOR PROCESSED/CONDENSED TIME SERIES OUTPUT
        'O': os.path.join(data_dir, fw_model, run_name, 'outputs-proc'),
        'O_': os.path.join(data_dir, fw_model, run_name, 'outputs-proc', 'Out_'),
        # LOG DATA: CODE USED TO GENERATE/PROCESS DATA
        'L': os.path.join(data_dir, fw_model, run_name, 'log'),
        # BATHYMETRY FIGURES
        'bF': os.path.join(data_dir, fw_model, run_name, 'bathy_fig'),
        'bF_': os.path.join(data_dir, fw_model, run_name, 'bathy_fig', 'bathy_fig_'),
        # SPECTRA FIGURES
        'spF': os.path.join(data_dir, fw_model, run_name, 'spectra_fig'),
        'spF_': os.path.join(data_dir, fw_model, run_name, 'spectra_fig', 'spectra_fig_'),
        # ANIMATIONS
        'ani': os.path.join(data_dir, fw_model, run_name, 'animations')
    }

    return p


def make_FW_paths():
    # Get list of directories from list_FW_dirs
    p = get_FW_paths()
    # RUN_NAME
    os.makedirs(p['RN'], exist_ok=True)
    # INPUTS: `input.txt` TEXT FILES 
    os.makedirs(p['i'], exist_ok=True)
    # INPUTS: PROCESSED INPUT FILES
    os.makedirs(p['I'], exist_ok=True)
    # OUTPUTS: DIRECTORY FOR RAW TIME SERIES OUTPUT
    os.makedirs(p['o'], exist_ok=True)
    # OUTPUTS: DIRECTORY FOR PROCESSED/CONDENSED TIME SERIES OUTPUT
    os.makedirs(p['O'], exist_ok=True)
    # LOG DATA: CODE USED TO GENERATE/PROCESS DATA
    os.makedirs(p['L'], exist_ok=True)
    # BATHYMETRY FILES
    os.makedirs(p['b'], exist_ok=True)
    # BATHYMETRY FIGURES
    os.makedirs(p['bF'], exist_ok=True)
    # SPECTRA
    os.makedirs(p['sp'], exist_ok=True)
    # SPECTRA FIGURES
    os.makedirs(p['spF'], exist_ok=True)
    # ANIMATIONS
    os.makedirs(p['ani'], exist_ok=True)

    print('Directories successfully created!')


def get_FW_tri_paths(tri_num=None):

    p = get_FW_paths()
    if tri_num is None:
        tri_num = int(os.getenv('TRI_NUM'))
        
    ptr = {
        # Trial number
            'num_str': f"{tri_num:05}",
        # Run Name
            'RN': p['RN_str'],
        # Input Name/Title
            'input_name': f"input_{tri_num:05d}",
        # Input Name/Title
            'tri_name': f"tri_{tri_num:05d}",
        # Path to the input_XXXXX.txt file
            'i_file': f"{p['i_']}{tri_num:05d}.txt",
        # Path to input_XXXXX.pkl file
            'i_file_pkl': f"{p['I']}/tri_{tri_num:05d}.pkl",
        # Path to out_XXXXX folder (RESULT_FOLDER) to put into FUNWAVE 
            'RESULT_FOLDER': f"{p['o_']}{tri_num:05d}/",
        # Path to bathy_XXXXX.txt file
            'b_file': f"{p['b_']}{tri_num:05d}.txt",
        # Path to spectra_XXXXX.txt file
            'sp_file': f"{p['sp_']}{tri_num:05d}.txt",
        # Path to condensed output structure
            'out_file': f"{p['O_']}{tri_num:05d}.mat",
            'out_record': f"{p['O_']}{tri_num:05d}.tfrecord",
        # Path to dep.out
            'dep_file': f"{p['o_']}{tri_num:05d}/dep.out",
        # Path to cd_breakwater.out
            'cd_breakwater_file': f"{p['o_']}{tri_num:05d}/cd_breakwater.out",
        # Path to time_dt.out
            'time_dt_file': f"{p['o_']}{tri_num:05d}/time_dt.txt",
        # Path to bathymetry figure
            'b_fig': f"{p['bF_']}{tri_num:05d}.png",
        # Path to spectra figure
            'sp_fig': f"{p['spF_']}{tri_num:05d}.png",
    }

    return ptr



#%% Path functions useful in compression stages
def find_prefixes_path(directory):
        prefixes = []
        for filename in os.listdir(directory):
            # Split at extension
            name, _ = os.path.splitext(filename)
            
            # Identify time step files (ends in XXXXX)
            if name[-5:].isdigit() and len(name) > 5:
                variable_ = name[:-5]
            # Identify non time-step files
            else:
                variable_ = name
            # Append to list
            prefixes.append(variable_)

        # Remove duplicates
        prefix_list = list(set(prefixes))
        return prefix_list


def get_var_out_paths(RESULT_FOLDER: Path, var: str) -> list[Path]:
    '''
    Gets a list of paths to all of the output files in RESULT_FOLDER that have 
    names that begin with the string specified by `var`. For example, use `eta_` 
    to get the eta files.
    
    ARGUMENTS:
        - var (str): substring to search for at the beginning of file names. 
            Best to use up to last underscore (ie- `eta_`, `U_undertow`) to 
            avoid issues with similarly named variables
    RETURNS: 
        -path_of_vars (List(Path)): all the paths to the variables 
            searched for

    '''
    out_XXXXX_path = Path(RESULT_FOLDER)
    var_files = []
    for file in out_XXXXX_path.iterdir():
        if file.name.startswith(var):
                var_files.append(file)
                
    path_of_vars = sorted(var_files, key=lambda p: p.name)            
    return path_of_vars

def get_vars_out_paths(RESULT_FOLDER: Path, var_search: list[str])-> Dict[str,list[Path]]:
    '''
    Applies `get_var_in_path` to the path specified for the variables 
    specified in var_search to output a dictionary of path lists. Cleans up 
    name a bit (trailing _)
    
    ARGUMENTS:
        - out_XXXXX (Path): Path to out_XXXXX file
    RETURNS: 
        - var_search (List[str]): list of substrings for `get_var_output_paths`
    '''
    
    all_var_paths = {}
    for var in var_search:
        varname = var[:-1] if var.endswith('_') else var  # Remove trailing _ if they exist
        all_var_paths[varname] = get_var_out_paths(RESULT_FOLDER,var)
    return all_var_paths

def get_all_paths_in_path(path):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


