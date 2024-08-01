import argparse
import os 
import sys
import tensorflow as tf


def main(super_path, run_name,tri_num):
    ## Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    ## Inputs
    In_d = fp.tf.load_In_d(f'{super_path}/{run_name}/inputs-proc/In_d.pkl')
    tensors_3d = ['eta']
    tensors_2d = ['bathy','dep','time_dt']
    others = {'bathy':  tf.io.FixedLenFeature([], tf.string),
              'bathy_shape':  tf.io.FixedLenFeature([2], tf.int64)}
    
    ## Gather feature descriptions
    feature_description = {}
    feature_description = fp.tf.get_feature_desc_tensors(tensors_3d, 3,feature_description)
    feature_description = fp.tf.get_feature_desc_tensors(tensors_2d, 2,feature_description)
    feature_description = fp.tf.get_feature_desc_inputs(In_d[f'tri_{tri_num:05}'],feature_description)
    feature_description = fp.tf.add_features_manually(others,feature_description)
    
    ## Parse to both dataset and dictionary
    tf_record_files = fp.tf.get_all_filepaths(f'{super_path}/{run_name}/outputs-proc')
    tensors = tensors_3d + tensors_2d
    
    parsed_dataset = fp.tf.parse_function(tf_record_files,feature_description,tensors)
    parsed_dict = fp.tf.parse_function(tf_record_files,feature_description,tensors,out_type='dict')
    
    ## ML Preprocessing
    vars_required = ['AMP_WK','Tperiod','Xc_WK','DX','bathy','eta','time_dt']
    vars_requied_dict = fp.tf.filter_dict(parsed_dict,vars_required)
    bathyX, bathyZ, skew, asy =  fp.ml.ska_conv.preprocessing_pipeline(vars_requied_dict[0],0)
    
    
    ## Make sure that AMP_WK and Tperiod are also [1,1]
    AMP_WK = tf.reshape(vars_requied_dict[0]['AMP_WK'], [1,1])
    Tperiod = tf.reshape(vars_requied_dict[0]['Tperiod'], [1,1])
    
    
    # Save out
    feature_dict_ML = {}
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'AMP_WK' ,AMP_WK)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'Tperiod',Tperiod)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'bathyZ' ,bathyZ)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'skew' ,skew)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'asy' ,asy)
    
    fp.tf.save_tfrecord(feature_dict_ML,f'{super_path}/{run_name}/inputs-ML/MLin_{tri_num:05}.tfrecord')
    print(f'Successfully made: MLin_{tri_num:05}.tfrecord')
    return

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    parser.add_argument("super_path", type=str, help="Path to super directory")
    parser.add_argument("run_name", type=str, help="Name of the run")
    parser.add_argument("tri_num", type=int, help="Trial number")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.super_path, args.run_name,args.tri_num)