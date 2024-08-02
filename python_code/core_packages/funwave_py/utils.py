import numpy as np
import os
#%% Basic Cutting Function

def cut_between(arrays: list[np.array], cutting_array: np.array, lower: float = None, upper: float = None, mode: str = "between", axis: int = 0):
    """
    Cut multiple numpy arrays based on the indices of a cutting array closest to the specified bounds.
    
    Parameters:
    - arrays: List of 1D numpy arrays of the same length
    - cutting_array: 1D numpy array used to determine cut indices
    - lower: Lower bound value (optional, required if mode is 'between' or 'end')
    - upper: Upper bound value (optional, required if mode is 'between' or 'start')
    - mode: Mode of cutting ('between', 'start', 'end')
    
    Returns:
    - List of 1D numpy arrays cut according to the specified bounds and mode
    """
    if mode == "between":
        if lower is None or upper is None:
            raise ValueError("Both lower and upper bounds must be specified for mode 'between'.")
        lower_i = np.abs(cutting_array - lower).argmin()
        upper_i = np.abs(cutting_array - upper).argmin()
        start_i = min(lower_i, upper_i)
        end_i = max(lower_i, upper_i) + 1
    elif mode == "start":
        if upper is None:
            raise ValueError("Upper bound must be specified for mode 'start'.")
        end_i = np.abs(cutting_array - upper).argmin() + 1
        start_i = 0
    elif mode == "end":
        if lower is None:
            raise ValueError("Lower bound must be specified for mode 'end'.")
        start_i = np.abs(cutting_array - lower).argmin()
        end_i = len(cutting_array)
    else:
        raise ValueError("Invalid mode. Use 'between', 'start', or 'end'.")
    cut_arrays = []
    for arr in arrays:
        if arr.ndim == 1:
            cut_arrays.append(arr[start_i:end_i])
        if arr.ndim == 2:
            if axis == 0:
                cut_arrays.append(arr[start_i:end_i,:])
            elif axis == 1:
                cut_arrays.append(arr[:,start_i:end_i])
    return cut_arrays

def get_all_paths_in_dir(path):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
