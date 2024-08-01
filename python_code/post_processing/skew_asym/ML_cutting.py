

#%% Basic Cutting Function
'''
MOVED TO UTILS
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
'''

'''
MOVED TO POST-PROCESSING/skew_assymmetry
#%% Calculation of Skew and Asymmetry
def calculate_ska(eta):
    eta_n = eta - np.mean(eta)
    denom = (np.mean(eta_n**2))**(1.5); 
    # Numerator for skew
    sk_num = np.mean(eta_n**3)
    # Numerator for Asymmetry
    hn = np.imag(hilbert(eta_n))
    hnn = hn - np.mean(hn)
    asy_num = np.mean(hnn ** 3)
    # Calculate and output
    skew = sk_num/denom;
    asy = asy_num/denom;
    return skew, asy
'''
#%% Other Processing Helpers
'''
MOVED TO PREPROCESSING
# Remove Gradients
def calculate_gradients_and_cut(array_list, cutting_array,DX, threshold):
    grad = np.diff(cutting_array) / DX
    # Find first instance where gradient exceeds the threshold
    idx = np.argmax(np.abs(grad) > threshold) if np.any(np.abs(grad) > threshold) else None
    loc = cutting_array[idx]
    # If the threshold is not exceeded, return the original array
    if idx is None:
        cut_arrays = array_list
    else:
        cut_arrays = cut_between(array_list,cutting_array,upper=loc,mode="start",axis = 0)
    return cut_arrays

'''
'''
MOVED TO PREPROCESSING
def movmean(data, window_size):
    return uniform_filter1d(data, size=window_size, mode='nearest')


def interpolate_cubic_splines(arr_list,grid_arr):
    new_grid = np.linspace(grid_arr.min(), grid_arr.max(), 100)
    
    interp_arr_list = []
    for arr in arr_list:
        cubic_spline_function = CubicSpline(grid_arr, arr)
        cubic_spline_fit = cubic_spline_function(new_grid)
        interp_arr_list.append(cubic_spline_fit)
    return interp_arr_list
'''

#%% The pipeline
'''
MOVED TO PREPROCESSING
def preprocessing_pipeline(small_dict,steady_time):
    
    # Unpack Variables
    #Make sure to adjust this back
    #eta = small_dict['eta'][:,1,:]
    eta = np.squeeze(small_dict['eta'][:,1,:])
    time = small_dict['time_dt'][:,0]
    bathyX = small_dict['bathy'][:,0]
    bathyZ = small_dict['bathy'][:,1]
    Xc_WK = small_dict['Xc_WK']
    DX = small_dict['DX']

    # Slice to steady time
    [time, eta] = cut_between([time, eta],time,steady_time,mode="end",axis = 0)
    #print(time)
    #print(eta)
    ## Slice to wet beach
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyZ,upper=0,mode="start",axis = 1)
    ## Slice to Wavemaker
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyX,lower=Xc_WK,mode="end",axis = 1)
    ## Calculate skew and asyemmetry
    skew, asy =  np.apply_along_axis(calculate_ska, 0, eta)
    skew = np.nan_to_num(skew, nan=0.1)
    asy = np.nan_to_num(asy, nan=0.1)
    arrays = [bathyX, bathyZ, skew, asy]
    ## Cut off extreme gradients
    [bathyX, bathyZ, skew, asy] = calculate_gradients_and_cut(arrays, skew,DX, 1.5)
    [bathyX, bathyZ, skew, asy] = calculate_gradients_and_cut(arrays, asy,DX, 1.5)
    ## Moving average smoothing
    skew = movmean(skew, 25)
    asy = movmean(asy, 25)
    ## Interpolation
    arr_list = [bathyX,bathyZ,skew,asy]
    [bathyX,bathyZ,skew,asy] = interpolate_cubic_splines(arr_list,bathyX)
    bathyX = bathyX.reshape(1,-1).astype(np.float32)
    skew = skew.reshape(1,-1).astype(np.float32)
    bathyZ = bathyZ.reshape(1,-1).astype(np.float32)
    asy = asy.reshape(1, -1).astype(np.float32)
    return bathyX,bathyZ,skew,asy
'''
