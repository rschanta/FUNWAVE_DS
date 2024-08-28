from .ml_preprocess import *
tf.experimental.numpy.experimental_enable_numpy_behavior()
# Mapping Function
def process_fn(features):
    # Extract variables
    eta = features['eta']
    mask = features['mask']
    bathy = features['bathy']
    time_dt = features['time_dt']
    Hmo = features['Hmo']
    Tperiod = features['Tperiod']
    Xslp = features['Xslp']
   
    # Apply pipeline
    X, Z, eta = mask_eta(eta, mask,bathy)
    eta = cut_to_steady_time(eta, time_dt)
    skew, asy = calculate_ska_1D(eta)
    X, Z, skew, asy = cut_arrays_at_value_tf(X, Z, skew, asy, Xslp)
    bathyX, bathyZ, skew, asy = interpolate_to_grid(X, Z, skew, asy, num_points=100)
    
    # Reshape
    skew = tf.reshape(skew, [1,100])  # Adjust the second dimension to match expected size
    asy = tf.reshape(asy, (1, 100))
    Hmo = tf.reshape(Hmo, [1,1]) 
    Tperiod = tf.reshape(Tperiod, [1,1]) 
    
    #bathyX = bathyX.reshape(1,-1).astype(np.float32)
    #skew = skew.reshape(1,-1).astype(np.float32)
    #bathyZ = bathyZ.reshape(1,-1).astype(np.float32)
    #asy = asy.reshape(1, -1).astype(np.float32)
    
    inputs = (Hmo,Tperiod,bathyZ)
    outputs = skew
    
    print("Processed X shape:", bathyX.shape)
    print("Processed Z shape:", bathyZ.shape)
    print("Processed skew shape:", skew.shape)
    print("Processed asy shape:", asy.shape)
    
    return inputs, outputs
    
def map_fn(features):
    return process_fn(features)