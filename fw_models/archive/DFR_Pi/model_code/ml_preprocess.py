import tensorflow as tf
import numpy as np
from scipy.signal import hilbert
tf.experimental.numpy.experimental_enable_numpy_behavior()
#%% Masking function
def mask_eta(eta, mask,bathy):
    
    # Squeeze out extra dimensions
    eta = tf.squeeze(eta[:, 1, :])
    mask = tf.squeeze(mask[:, 1, :])

    # Prepare the mask
    mask_condition = tf.reduce_all(mask != 0, axis=0)
    mask_condition = tf.ensure_shape(mask_condition, [None])

    # Apply the mask
    eta = tf.boolean_mask(eta, mask_condition, axis=1)
    bathy = tf.boolean_mask(bathy, mask_condition, axis=0)
    
    # Slice out X and Z
    X = bathy[:, 0]
    Z = bathy[:, 1]
    
    return X, Z, eta

#%% Cut to steady time function
def cut_to_steady_time(eta, time_dt):
    # Cut to steady time
    steady_time = 100
    steady_index = tf.argmin(tf.abs(time_dt[:, 0] - steady_time))
    eta = eta[steady_index:, :]
    time_dt = time_dt[steady_index:, :]
    return eta

#%% Calculate skewness and asymmetry- function and warpper
def calculate_ska_1D_(eta):
    eta = eta.T
    # Number of time steps
    num_time_steps = eta.shape[0]
    
    # Initialize arrays to store results
    skew = np.zeros(num_time_steps)
    asy = np.zeros(num_time_steps)
    
    # Calculate skewness and asymmetry for each time step
    for i in range(num_time_steps):
        eta_n = eta[i, :] - np.mean(eta[i, :])
        denom = (np.mean(eta_n**2))**(1.5)
        
        # Numerator for skew
        sk_num = np.mean(eta_n**3)
        
        # Numerator for Asymmetry
        hn = np.imag(hilbert(eta_n))
        hnn = hn - np.mean(hn)
        asy_num = np.mean(hnn**3)
        
        # Calculate and store results
        skew[i] = sk_num / denom
        asy[i] = asy_num / denom
    
    return skew, asy


def calculate_ska_1D(eta):
    return tf.py_function(func=calculate_ska_1D_, inp=[eta], Tout=[tf.float32, tf.float32])

#%% Cut to Wavemaker, or Xslp, whatever
def cut_arrays_at_value_tf(X, Z, skew, asy, Xslp):
    # Ensure inputs are TensorFlow tensors
    X = tf.convert_to_tensor(X, dtype=tf.float32)
    Z = tf.convert_to_tensor(Z, dtype=tf.float32)
    skew = tf.convert_to_tensor(skew, dtype=tf.float32)
    asy = tf.convert_to_tensor(asy, dtype=tf.float32)
    #Xslp = tf.convert_to_tensor(Xslp, dtype=tf.float32)

    # Find the index of the value in X closest to Xslp
    abs_diff = tf.abs(X - Xslp)
    index = tf.argmin(abs_diff)

    # Use tf.gather to slice from the found index to the end
    index = tf.cast(index, tf.int32)

    X_cut = X[index:]
    Z_cut = Z[index:]
    skew_cut = skew[index:]
    asy_cut = asy[index:]
    
    return X_cut, Z_cut, skew_cut, asy_cut
    
#%% Perform interpolation
def interpolate_to_grid(X, Z, skew, asy, num_points=100):
    """
    Interpolate Z, skew, and asy to a new grid of num_points based on X.

    Parameters:
    - X: 1D tensor of x-values (monotonically increasing).
    - Z: 1D tensor of z-values to be interpolated.
    - skew: 1D tensor of skew values to be interpolated.
    - asy: 1D tensor of asymmetry values to be interpolated.
    - num_points: Number of grid points for interpolation.

    Returns:
    - new_grid: 1D tensor of new x-values for interpolation.
    - Z_interp: 1D tensor of interpolated Z values.
    - skew_interp: 1D tensor of interpolated skew values.
    - asy_interp: 1D tensor of interpolated asy values.
    """
    # Ensure tensors are float32
    X = tf.convert_to_tensor(X, dtype=tf.float32)
    Z = tf.convert_to_tensor(Z, dtype=tf.float32)
    skew = tf.convert_to_tensor(skew, dtype=tf.float32)
    asy = tf.convert_to_tensor(asy, dtype=tf.float32)

    # Define new grid points
    X_min = tf.reduce_min(X)
    X_max = tf.reduce_max(X)
    new_grid = tf.linspace(X_min, X_max, num_points)

    # Define interpolation function
    def interpolate(values, X, new_grid):
        # Ensure values are tensors
        values = tf.convert_to_tensor(values, dtype=tf.float32)
        # Interpolate using tf.searchsorted to find positions
        indices = tf.searchsorted(X, new_grid, side='left')
        indices = tf.clip_by_value(indices, 1, tf.size(X) - 1)
        
        # Gather values at indices
        x0 = tf.gather(X, indices - 1)
        x1 = tf.gather(X, indices)
        y0 = tf.gather(values, indices - 1)
        y1 = tf.gather(values, indices)
        
        # Calculate weights for interpolation
        weight = (new_grid - x0) / (x1 - x0)
        interpolated_values = y0 + weight * (y1 - y0)
        
        return interpolated_values

    # Perform interpolation
    Z_interp = interpolate(Z, X, new_grid)
    skew_interp = interpolate(skew, X, new_grid)
    asy_interp = interpolate(asy, X, new_grid)
    
    return new_grid, Z_interp, skew_interp, asy_interp