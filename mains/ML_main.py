import os 
import sys
import argparse
import random
import tensorflow as tf
def main():
    #%% Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    print('ENTERED SCRIPT: Checkpoint 1')
    tensors_2d = ['bathyZ','skew','asy','AMP_WK','Tperiod'] 
    feature_description = fp.tf.get_feature_desc_tensors(tensors_2d, 2,{})
    
    print('GETTING FILES TO PARSE: Checkpoint 2')
    directory = '/lustre/scratch/rschanta/FSPY4/inputs-ML'
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    print('SHUFFLING ENTIRE SET: Checkpoint 3')
    random.shuffle(files)
    split_ratio = 0.8
    split_index = int(len(files) * split_ratio)

    
    print('SPLITTING: Checkpoint 5')
    tf_record_files_train = files[:split_index]
    tf_record_files_val = files[split_index:]
    
    print('PARSING: Checkpoint 5')
    training_set = fp.ml.ska_conv.parse_function3(tf_record_files_train,feature_description)
    val_set = fp.ml.ska_conv.parse_function3(tf_record_files_val,feature_description)
    
    
    print('SHUFFLING SPLIT SETS: Checkpoint 6')
    training_set = training_set.shuffle(buffer_size=1000)
    val_set = val_set.shuffle(buffer_size=1000)
    
    print('BATCHING: Checkpoint 7')
    training_set = training_set.batch(32)
    val_set = val_set.batch(32)
    
    print('PREFETCH: Checkpoint 8')
    training_set = training_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    val_set = val_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    
    print('Checkpoint 9')
    model = fp.ml.ska_conv.create_model()
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    
    #%% Create and fit the model
    print('Checkpoint 10')
    history = model.fit(training_set, epochs = 100,validation_data=val_set)
    
    print('Checkpoint 11')
    model.save('/work/thsu/rschanta/RTS-PY/analysis/dummy_model.keras')
    model.save('/work/thsu/rschanta/RTS-PY/analysis/dummy_model.h5')
    
    return model

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    #parser.add_argument("super_path", type=str, help="Path to super directory")
    #parser.add_argument("run_name", type=str, help="Name of the run")
    #parser.add_argument("tri_num", type=int, help="Trial number")
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main()