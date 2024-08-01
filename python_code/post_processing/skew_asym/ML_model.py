from tensorflow.keras import layers, models, Input
'''
MOVED TO CREATE_MODEL
def create_model():
    # Tensor input branch (shape: 100 timesteps, 1 feature)
    bathyZ = Input(shape=(100, 1), name='bathyZ')
    x = layers.Conv1D(32, 3, activation='relu', padding='same')(bathyZ)
    x = layers.Conv1D(64, 3, activation='relu', padding='same')(x)
    x = layers.Flatten()(x)

    # Scalar inputs
    AMP_WK = Input(shape=(1,), name='AMP_WK')
    Tperiod = Input(shape=(1,), name='Tperiod')
    
    # Combine all branches
    combined = layers.concatenate([x, AMP_WK, Tperiod])

    # Fully connected layer
    z = layers.Dense(64, activation='relu')(combined)
    z = layers.Dense(128, activation='relu')(z)

    # Output layer (tensor output, same shape as input tensor)
    skew = layers.Dense(100, activation='linear', name='skew')(z)

    # Create the model
    model = models.Model(inputs=[AMP_WK, bathyZ, Tperiod], outputs=skew)
    return model
'''