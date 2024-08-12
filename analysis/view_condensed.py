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

AMP_WK, bathyZ, Tperiod, skew = get_inputs(0)

model = tf.keras.models.load_model('new_skew_model.keras')
lister = [AMP_WK, bathyZ.T, Tperiod]
z = model.predict(lister)


import matplotlib.pyplot as plt
plt.plot(z.reshape(-1))
plt.plot(skew.reshape(-1))
plt.show()
#%%
with open('postprocessed.pkl', 'rb') as f:
    nested_dict = pickle.load(f)
    
import tensorflow as tf
asy_model = tf.keras.models.load_model('new_asy_model.keras')
skew_model = tf.keras.models.load_model('new_skew_model.keras')


num = 0
lister = [ nested_dict[num]['AMP_WK'], nested_dict[num]['bathyZ'], nested_dict[num]['Tperiod']]

asy_pred = asy_model(lister).numpy()
skew_pred = skew_model(lister).numpy()

AMP_WK = nested_dict[num]['AMP_WK']
Tperiod = nested_dict[num]['Tperiod']
bathyX = nested_dict[num]['bathyX'].reshape(-1)
bathyZ = nested_dict[num]['bathyZ'].reshape(-1)
skew = nested_dict[num]['skew'].reshape(-1)
asy = nested_dict[num]['asy'].reshape(-1)


plt.plot(bathyX,skew,color='blue',label='FW Sk')
plt.plot(bathyX,asy,color='red',label='FW As')
plt.plot(bathyX,skew_pred.reshape(-1), linestyle='--',color='blue',label='ML Sk')
plt.plot(bathyX,asy_pred.reshape(-1), linestyle='--',color='red',label='ML As')
plt.plot(bathyX,-bathyZ, color='black', label='Bathymetry')  
plt.grid()
plt.xlabel('Position in the Cross-shore (m)')
legend = plt.legend(ncol=3)
plt.title(f'FUNWAVE outputs vs ML outputs')
plt.tight_layout()
plt.savefig('FW_vs_ML.png', dpi=300, bbox_extra_artists=[legend])
plt.show()
from sklearn.metrics import r2_score
r2_skew = r2_score(skew, skew_pred.reshape(-1))
r2_asy = r2_score(asy, asy_pred.reshape(-1))
