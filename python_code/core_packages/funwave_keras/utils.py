import pickle
from pathlib import Path
from typing import  Dict, Any, Optional
import os
import pathlib
import numpy as np
def get_numbers(filepath: Optional[Path] = None, 
                tri_num: Optional[int] = None,
                string: Optional[str] = None) -> Dict[str,Any]:
    '''
    Gets the numbers for a trial and useful names for them. Can use any
    string of the form foo_XXXXX, a filepath to an output ./foo_XXXXX, or 
    an integer number.
    '''
    # Get number and/or name
    if filepath is not None:
        name  = filepath.parts[-1]
        tri_num = int(name[-5:])
    elif tri_num is not None:
        tri_num = tri_num
    elif string is not None:
        tri_num = int(string[-5:])
    return {'tri': f'tri_{tri_num:05}',
            'in': f'in_{tri_num:05}',
            'out': f'out_{tri_num:05}',
            'tri_num': tri_num}


def load_In_d(path_str: str):
    with open(path_str, 'rb') as file:
        In_d = pickle.load(file)
    return In_d


def load_In_d_windows(path_str: str):
    '''
    Same function as load_In_d, adjust for windows?
    '''
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath 
    with open(path_str, 'rb') as file:
        In_d = pickle.load(file)
    pathlib.PosixPath = temp

    return In_d


def get_all_filepaths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def filter_dict(original_dict, keys):
    """
    Create a new dictionary with only the specified keys from the original dictionary.
    If the original dictionary contains other dictionaries as values, apply the filtering
    to each of those inner dictionaries as well.

    Parameters:
    - original_dict (dict): The original dictionary from which to filter keys.
    - keys (list): The list of keys to include in the new dictionary.

    Returns:
    - dict: A new dictionary containing only the specified keys, with filtering applied
            to inner dictionaries if present.
    """
    def filter_inner_dict(inner_dict):
        """Filter keys in an inner dictionary."""
        return {key: inner_dict[key] for key in keys if key in inner_dict}

    if all(isinstance(v, dict) for v in original_dict.values()):
        # Case: Dictionary of dictionaries
        return {outer_key: filter_inner_dict(inner_dict)
                for outer_key, inner_dict in original_dict.items()}
    else:
        # Case: Simple dictionary
        return {key: original_dict[key] for key in keys if key in original_dict}