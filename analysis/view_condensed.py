import tensorflow as tf
import pickle
with open('nested_dict.pkl', 'rb') as f:
    nested_dict = pickle.load(f)
    
def get_inputs(k):
    AMP_WK = nested_dict['inputs']['input_0'][k]
    bathyZ = nested_dict['inputs']['input_1'][k]
    Tperiod = nested_dict['inputs']['input_2'][k]
    skew = nested_dict['outputs'][k]
    
    return AMP_WK, bathyZ, Tperiod, skew

AMP_WK, bathyZ, Tperiod, skew = get_inputs(750)

model = tf.keras.models.load_model('first_model.keras')
lister = [AMP_WK, bathyZ.T, Tperiod]
z = model.predict(lister)


import matplotlib.pyplot as plt
plt.plot(z.reshape(-1))
plt.plot(skew.reshape(-1))