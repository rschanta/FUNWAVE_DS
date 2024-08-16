import argparse
from pathlib import Path
import os
import sys
import numpy as np

#%%
def main(super_path, run_name,tri_num):
    
    # Path Commands
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    
    # Import needed functions
    import python_code as pc

    # Get relevant paths
    p = pc.co.py.list_FW_dirs(super_path, run_name)
    ptr = pc.co.py.list_FW_tri_dirs(tri_num, p)

    # Get input dictionary
    In_d_i = pc.co.ke.load_input_dict(p['Id'], tri_num)

    # Compress/Serialize the outputs
    serialized_features = pc.co.ke.serialize_outputs2(ptr['RESULT_FOLDER'],In_d_i)
    
    # Compress/Serialize the inputs
    serialized_features = pc.co.ke.serialize_inputs2(In_d_i,feature_dict = serialized_features)
    
    # Compress/Serialize supplemental variables
    supplemental_vars = {'bathy': In_d_i['files']['bathy']['array'].astype(np.float32)}
    serialized_features = pc.co.ke.serialize_all2(supplemental_vars,feature_dict = serialized_features)

    
    # Save Out
    pc.co.ke.save_tfrecord(serialized_features,ptr['out_record'])
    
    print(f'\nSuccessfully saved out_{tri_num:05}.tfrecord')
    return

#%%
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
    