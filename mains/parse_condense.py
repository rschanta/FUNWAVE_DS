import argparse
import os 
import sys
import tensorflow as tf
import pickle

def main():
    ## Get modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.abspath(os.path.join(current_dir, os.pardir)))
    import python_code as fp
    

    directory = '/lustre/scratch/rschanta/FSPY4/inputs-ML'
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files = sorted(files)

    tensors_2d = ['bathyX','bathyZ','skew','AMP_WK','Tperiod','skew','asy']
    feature_descriptions = fp.tf.get_feature_desc_tensors(tensors_2d, 2,{})

    dataset = fp.ml.ska_conv.parse_function3(files,feature_descriptions)

    def dataset_to_nested_dict(dataset):
        nested_dict = {'inputs': {}, 'outputs': []}
        for inputs, output in dataset:
            for i, input_data in enumerate(inputs):
                if f'input_{i}' not in nested_dict['inputs']:
                    nested_dict['inputs'][f'input_{i}'] = []
                nested_dict['inputs'][f'input_{i}'].append(input_data.numpy())  # Convert tensors to numpy arrays
            nested_dict['outputs'].append(output.numpy())  # Assuming output is a single tensor
        return nested_dict

    nested_dict = dataset_to_nested_dict(dataset)

    with open('/lustre/scratch/rschanta/FSPY4/inputs-proc/nested_dict.pkl', 'wb') as f:
        pickle.dump(nested_dict, f)
    return

if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Process variables for compression")
    
    # Add arguments and descriptions
    
    # Call the parser
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main()