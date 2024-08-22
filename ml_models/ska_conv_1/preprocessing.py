import sys
import os
import numpy as np
import tensorflow as tf
from scipy.ndimage import uniform_filter1d
from scipy.interpolate import CubicSpline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from funwave_ds.fw_py.utils import cut_between
from postprocessing.skew_asymmetry.skew_asymmetry import calculate_ska_1D



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

def preprocessing_pipeline3(small_dict,steady_time):

    # Unpack Variables
    eta = np.squeeze(small_dict['eta'][:,1,:])
    time = small_dict['time_dt'][:,0]
    bathyX = small_dict['bathy'][:,0]
    bathyZ = small_dict['bathy'][:,1]
    Xc_WK = small_dict['Xc_WK']
    DX = small_dict['DX']
    ALT_TITLE = small_dict['ALT_TITLE']
    TITLE = small_dict['TITLE']
    AMP_WK = tf.reshape(small_dict['AMP_WK'], [1,1]) 
    Tperiod = tf.reshape(small_dict['Tperiod'], [1,1]) 

    # Slice to steady time
    [time, eta] = cut_between([time, eta],time,steady_time,mode="end",axis = 0)

    ## Slice to wet beach
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyZ,upper=0,mode="start",axis = 1)
    
    ## Slice to Wavemaker
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyX,lower=Xc_WK,mode="end",axis = 1)
    
    ## Calculate skew and asyemmetry
    skew, asy =  np.apply_along_axis(calculate_ska_1D, 0, eta)
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

    ## Form dictionary output
    out_dict = {'bathyX':bathyX,
               'bathyZ': bathyZ,
               'skew':  skew,
               'asy': asy,
               'AMP_WK': AMP_WK,
                'Tperiod': Tperiod,
                'ALT_TITLE': ALT_TITLE,
                'TITLE': TITLE}

    return out_dict

def preprocessing_pipeline3(small_dict,steady_time):

    # Unpack Variables
    eta = np.squeeze(small_dict['eta'][:,1,:])
    time = small_dict['time_dt'][:,0]
    bathyX = small_dict['bathy'][:,0]
    bathyZ = small_dict['bathy'][:,1]
    Xc_WK = small_dict['Xc_WK']
    DX = small_dict['DX']
    TITLE = small_dict['TITLE']
    Hmo = tf.reshape(small_dict['Hmo'], [1,1]) 
    Tperiod = tf.reshape(small_dict['Tperiod'], [1,1]) 

    # Slice to steady time
    [time, eta] = cut_between([time, eta],time,steady_time,mode="end",axis = 0)

    ## Slice to wet beach
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyZ,upper=0,mode="start",axis = 1)
    
    ## Slice to Wavemaker
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyX,lower=Xc_WK,mode="end",axis = 1)
    
    ## Calculate skew and asyemmetry
    skew, asy =  np.apply_along_axis(calculate_ska_1D, 0, eta)
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

    ## Form dictionary output
    out_dict = {'bathyX':bathyX,
               'bathyZ': bathyZ,
               'skew':  skew,
               'asy': asy,
               'Hmo': Hmo,
                'Tperiod': Tperiod,
                'ALT_TITLE': ALT_TITLE,
                'TITLE': TITLE}

    return out_dict


def preprocessing_pipeline4(small_dict,steady_time):

    # Unpack Variables
    eta = np.squeeze(small_dict['eta'][:,1,:])
    time = small_dict['time_dt'][:,0]
    bathyX = small_dict['bathy'][:,0]
    bathyZ = small_dict['bathy'][:,1]
    Xc_WK = small_dict['Xc_WK']
    DX = small_dict['DX']
    TITLE = small_dict['TITLE']
    Hmo = tf.reshape(small_dict['Hmo'], [1,1]) 
    Tperiod = tf.reshape(small_dict['Tperiod'], [1,1]) 

    # Slice to steady time
    [time, eta] = cut_between([time, eta],time,steady_time,mode="end",axis = 0)

    ## Slice to wet beach
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyZ,upper=0,mode="start",axis = 1)
    
    ## Slice to Wavemaker
    [bathyX, bathyZ, eta] = cut_between([bathyX, bathyZ, eta],bathyX,lower=Xc_WK,mode="end",axis = 1)
    
    ## Calculate skew and asyemmetry
    skew, asy =  np.apply_along_axis(calculate_ska_1D, 0, eta)
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

    ## Form dictionary output
    out_dict = {'bathyX':bathyX,
               'bathyZ': bathyZ,
               'skew':  skew,
               'asy': asy,
               'Hmo': Hmo,
                'Tperiod': Tperiod,
                'TITLE': TITLE}

    return out_dict