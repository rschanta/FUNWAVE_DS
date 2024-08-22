from tensorflow.keras import layers, models, Input

def create_model():
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

def create_model_asy():
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
    asy = layers.Dense(100, activation='linear', name='asy')(z)

    # Create the model
    model = models.Model(inputs=[AMP_WK, bathyZ, Tperiod], outputs=asy)
    return model


def create_model_dummy2():
    # Read in Vector
    bathyZ = Input(shape=(100, 1), name='bathyZ')
    x = layers.Flatten()(bathyZ)

    # Read in Scalar
    AMP_WK = Input(shape=(1,), name='AMP_WK')
    Tperiod = Input(shape=(1,), name='Tperiod')
    
    # Combine
    dummy_output = layers.concatenate([AMP_WK,x, Tperiod])
    # Output without modifying
    model = models.Model(inputs=[AMP_WK, bathyZ, Tperiod], outputs=dummy_output)
    return model



def create_model_asy2():
    bathyZ = Input(shape=(100, 1), name='bathyZ')
    x = layers.Conv1D(32, 3, activation='relu', padding='same')(bathyZ)
    x = layers.Conv1D(64, 3, activation='relu', padding='same')(x)
    x = layers.Flatten()(x)

    # Scalar inputs
    Hmo = Input(shape=(1,), name='Hmo')
    Tperiod = Input(shape=(1,), name='Tperiod')
    
    # Combine all branches
    combined = layers.concatenate([x, Hmo, Tperiod])
    # Fully connected layer
    z = layers.Dense(64, activation='relu')(combined)
    z = layers.Dense(128, activation='relu')(z)

    # Output layer (tensor output, same shape as input tensor)
    asy = layers.Dense(100, activation='linear', name='asy')(z)

    # Create the model
    model = models.Model(inputs=[Hmo, bathyZ, Tperiod], outputs=asy)
    return model

def create_model_skew2():
    bathyZ = Input(shape=(100, 1), name='bathyZ')
    x = layers.Conv1D(32, 3, activation='relu', padding='same')(bathyZ)
    x = layers.Conv1D(64, 3, activation='relu', padding='same')(x)
    x = layers.Flatten()(x)

    # Scalar inputs
    Hmo = Input(shape=(1,), name='Hmo')
    Tperiod = Input(shape=(1,), name='Tperiod')
    
    # Combine all branches
    combined = layers.concatenate([x, Hmo, Tperiod])
    # Fully connected layer
    z = layers.Dense(64, activation='relu')(combined)
    z = layers.Dense(128, activation='relu')(z)

    # Output layer (tensor output, same shape as input tensor)
    skew = layers.Dense(100, activation='linear', name='skew')(z)

    # Create the model
    model = models.Model(inputs=[Hmo, bathyZ, Tperiod], outputs=skew)
    return model
