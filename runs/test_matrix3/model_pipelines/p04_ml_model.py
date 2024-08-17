import os 
import sys
import argparse
import random
import tensorflow as tf

def main(super_path, run_name,model_name):
    # Add to system path
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    # Get modules
    import funwave_ds.fw_py as fpy
    import funwave_ds.fw_tf as ftf
    import funwave_ds.fw_ml as fml
    import ml_models.ska_conv_1 as mod

    # Get feature description needed (note: all are 2D for this model)
    tensors_2D = ['bathyZ','skew','asy','AMP_WK','Tperiod']
    feature_description = ftf.construct_feature_descr(tensors_2D = tensors_2D, strings = [])

    # Get path to all files
    directory = "/work/thsu/rschanta/RTS-PY/runs/test_matrix3/processed_outputs/ML_inputs"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Split file paths into train/test/validation sets
    train_set, val_set = fml.split_paths(0.8,files)
    
    # Parse both sets
    train_set = mod.parse_function_asy(train_set,feature_description)
    val_set = mod.parse_function_asy(val_set,feature_description)
    
    # Shuffle the set
    train_set = train_set.shuffle(buffer_size=1000)
    val_set = val_set.shuffle(buffer_size=1000)
    
    # Batching 
    train_set = train_set.batch(32)
    val_set = val_set.batch(32)
    
    # Prebatch
    train_set = train_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    val_set = val_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    # Create the model
    model = mod.create_model()
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    
    # Fit the model
    history = model.fit(train_set, epochs = 100,validation_data=val_set)
    
    # Save the model
    model.save(f'{super_path}/{run_name}/ML-models/{model_name}.keras')
    model.save(f'{super_path}/{run_name}/ML-models/{model_name}.h5')
    
    return model

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    parser.add_argument("super_path", type=str, help="Path to super directory")
    parser.add_argument("run_name", type=str, help="Name of the run")
    parser.add_argument("model_name", type=str, help="Name to save the ML model as")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.super_path, args.run_name, args.model_name)