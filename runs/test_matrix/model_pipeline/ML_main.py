import os 
import sys
import argparse

def main():
    #%% Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    
    #%% Feature descriptions
    tensors_2d = ['bathyZ','skew','asy','AMP_WK','Tperiod'] 
    feature_description = fp.tf.get_feature_desc_tensors(tensors_2d, 2,{})
    
    #%% Define the parsing
    tf_record_files = ['./local_lustre/FSPY2/inputs-ML/MLin_00001.tfrecord', 
                       './local_lustre/FSPY2/inputs-ML/MLin_00002.tfrecord']
    dataset = fp.ml.ska_conv.parse_function(tf_record_files,feature_description)
    
    #%% Create and fit the model
    model = fp.ml.ska_conv.create_model()
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    dataset = dataset.batch(1)  
    model.fit(dataset)
    
    
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