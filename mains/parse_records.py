import argparse
import os 
import sys
import tensorflow as tf


def main(super_path, run_name,tri_num):
    ## Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    

    ## Construct path
    paths= [f'{super_path}/{run_name}/outputs-proc/out_{tri_num:05}.tfrecord']
    
    ## Inputs
    In_d = fp.tf.load_In_d(f'{super_path}/{run_name}/inputs-proc/In_d.pkl')
    
    ## Specify tensor shapes
    tensors_3d = ['eta','dep']
    tensors_2d = ['bathy','time_dt']
    
    ## Any other keys to add/modify?
    keys_to_add = {'TOTAL_TIME':tf.io.FixedLenFeature([], tf.int64)}

    ## Any other keys to ignore/remove?
    keys_to_ignore = []

    parsed_dict = fp.tf.get_tfrecord_as_dict(tensors_3d,
                                             tensors_2d,
                                             keys_to_add,
                                             In_d,
                                             keys_to_ignore,
                                             tri_num,
                                             paths)
    

    ## ML Preprocessing
    vars_required = ['AMP_WK','Tperiod','Xc_WK','DX','bathy','eta','time_dt']
    vars_requied_dict = fp.tf.filter_dict(parsed_dict,vars_required)
    bathyX, bathyZ, skew, asy =  fp.ml.ska_conv.preprocessing_pipeline(vars_requied_dict,0)
    
    
    ## Make sure that AMP_WK and Tperiod are also [1,1]
    AMP_WK = tf.reshape(vars_requied_dict['AMP_WK'], [1,1])
    Tperiod = tf.reshape(vars_requied_dict['Tperiod'], [1,1])
    
    
    # Save out

    feature_dict_ML = fp.tf.serialize_tensor({},'AMP_WK' ,AMP_WK)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'Tperiod',Tperiod)
    feature_dict_ML = fp.tf.serialize_tensor(feature_dict_ML,'bathyX' ,bathyX)
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