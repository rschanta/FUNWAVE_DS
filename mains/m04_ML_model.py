import os 
import sys
import argparse
import random
import tensorflow as tf
def main(super_path, run_name,model_name):

    #%% Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    # Get feature description needed (note: all are 2D for this model)
    tensors_2D = ['bathyZ','skew','asy','AMP_WK','Tperiod']
    feature_description = construct_feature_descr(tensors_2D = tensors_2D)

    
    # Get path to all files
    files = fp.py.get_all_paths_in_dir(f'{super_path}/{run_name}/inputs-ML')

    # Split file paths into train/test/validation sets
    train_set, val_set = split_paths(0.8,files)
    
    # Parse both sets
    train_set = fp.ml.ska_conv.parse_function3(tf_record_files_train,feature_description)
    val_set = fp.ml.ska_conv.parse_function3(tf_record_files_val,feature_description)
    
    # Shuffle the set
    train_set = training_set.shuffle(buffer_size=1000)
    val_set = val_set.shuffle(buffer_size=1000)
    
    # Batching 
    train_set = training_set.batch(32)
    val_set = val_set.batch(32)
    
    # Prebatch
    training_set = training_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    val_set = val_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    # Create the model
    model = fp.ml.ska_conv.create_model()
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    
    # Fit the model
    history = model.fit(training_set, epochs = 100,validation_data=val_set)
    
    # Save the model
    model.save('f{super_path}/{run_name}/{model_names}.keras')
    model.save('f{super_path}/{run_name}/{model_names}.h5')
    
    return model

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    parser.add_argument("super_path", type=str, help="Path to super directory")
    parser.add_argument("run_name", type=str, help="Name of the run")
    parser.add_argument("model_name", type=int, help="Name to save the ML model as")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(super_path, run_name, model_name )