from pathlib import Path
from typing import  Dict, Any, Optional


def list_all_trial_subdirectories(outputs_raw_str: str)-> list[Path]:
    '''
    Lists all out_XXXX files in the outputs_raw directory specified
    '''
    p = Path(outputs_raw_str)
    if not p.is_dir():
        raise ValueError(f"{outputs_raw_str} could not be found")
    return [d for d in p.iterdir() if d.is_dir() and d.name.startswith('out_')]




def get_var_outputh_paths(out_XXXXX_path: Path, var: str) -> list[Path]:
    '''
    Gets a list of paths to all of the output files who have names that begin
    with the string specified by `var`. For example, use `eta_` to get the eta
    files. Note that 
    
    ARGUMENTS:
        - var (str): substring to search for at the beginning of file names. 
            Best to use up to last underscore (ie- `eta_`, `U_undertow`) to 
            avoid issues with similarly named variables
    RETURNS: 
        -path_of_vars (List(Path)): all the paths to the variables 
            searched for

    '''
    var_files = []
    for file in out_XXXXX_path.iterdir():
        if file.name.startswith(var):
                var_files.append(file)
                
    path_of_vars = sorted(var_files, key=lambda p: p.name)            
    return path_of_vars

def get_list_var_output_paths(out_XXXXX: Path, var_search: list[str])-> Dict[str,list[Path]]:
    '''
    Applies `get_var_output_paths` to the path specified for the variables 
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
        all_var_paths[varname] = get_var_outputh_paths(out_XXXXX,var)
    return all_var_paths


'''
def get_all_output_paths(outpurs_raw_str: str, var_search: list[str])-> Dict[str,Dict[str,list[Path]]]:
  
    Applies get_all_var_output_paths to all out_XXXXX files in outputs_raw to
    return a directory
    
    trial_paths = list_trial_subdirectories(outpurs_raw_str)
    output_paths = {}
    for trial_path in trial_paths:
        output_name = trial_path.parts[-1]
        output_paths[output_name] = get_all_var_output_paths(trial_path, var_search)
    
    return output_paths
'''




