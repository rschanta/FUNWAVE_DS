
import funwave_keras as fk
import tensorflow as tf
import preprocessing as pp
#%% Parsing all the data

## Inputs
In_d = fk.load_In_d('./local_lustre/FSPY2/inputs-proc/In_d.pkl')
tensors_3d = ['eta']
tensors_2d = ['dep','bathy','time_dt']
others = {'bathy':  tf.io.FixedLenFeature([], tf.string),'bathy_shape':  tf.io.FixedLenFeature([2], tf.int64)}

## Gather feature descriptions
feature_description = {}
feature_description = fk.get_feature_desc_tensors(tensors_3d, 3,feature_description)
feature_description = fk.get_feature_desc_tensors(tensors_2d, 2,feature_description)
feature_description = fk.get_feature_desc_inputs(In_d['tri_00001'],feature_description)
feature_description = fk.add_features_manually(others,feature_description)

## Parse to both dataset and dictionary
tf_record_files = fk.get_all_filepaths('./local_lustre/FSPY2/outputs-proc')
tensors = tensors_3d + tensors_2d

parsed_dataset = fk.parse_function(tf_record_files,feature_description,tensors)
parsed_dict = fk.parse_function(tf_record_files,feature_description,tensors,out_type='dict')

#%% ML Preprocessing
vars_required = ['AMP_WK','Tperiod','Xc_WK','DX','bathy','eta','time_dt']
vars_requied_dict = fk.filter_dict(parsed_dict,vars_required)
# Get cut values
bathyX,bathyZ,skew,asy = pp.preprocessing_pipeline(vars_requied_dict[0],0)
# Make sure that AMP_WK and Tperiod are also [1,1]
AMP_WK = tf.reshape(vars_requied_dict[0]['AMP_WK'], [1,1])
Tperiod = tf.reshape(vars_requied_dict[0]['Tperiod'], [1,1])


# Save out
feature_dict_ML = {}
feature_dict_ML = fk.serialize_tensor(feature_dict_ML,'AMP_WK' ,AMP_WK)
feature_dict_ML = fk.serialize_tensor(feature_dict_ML,'Tperiod',Tperiod)
feature_dict_ML = fk.serialize_tensor(feature_dict_ML,'bathyZ' ,bathyZ)
feature_dict_ML = fk.serialize_tensor(feature_dict_ML,'skew' ,skew)
feature_dict_ML = fk.serialize_tensor(feature_dict_ML,'asy' ,asy)

fk.save_tfrecord(feature_dict_ML,'./d3reg_py/inputs_ML/MLin_00001.tfrecord')
