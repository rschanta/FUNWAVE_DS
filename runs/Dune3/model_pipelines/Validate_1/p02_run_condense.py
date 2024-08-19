import argparse
from pathlib import Path
import os
import sys
import numpy as np

#%%
def main(super_path, run_name,tri_num):
    # Add to system path
    sys.path.append("/work/thsu/rschanta/RTS-PY")
    # Get modules
    import funwave_ds.fw_py as fpy
    import funwave_ds.fw_tf as ftf

    # Get relevant paths
    p = fpy.get_FW_paths(super_path, run_name)
    ptr = fpy.get_FW_tri_paths(tri_num, p)

    # Get input dictionary
    In_d_i = fpy.load_input_dict(p['Id'], tri_num)

    # Compress/Serialize the outputs
    serialized_features = ftf.serialize_outputs(ptr['RESULT_FOLDER'],In_d_i)
    
    # Compress/Serialize the inputs
    serialized_features = ftf.serialize_inputs(In_d_i,feature_dict = serialized_features)
    
    # Compress/Serialize supplemental variables
    #supplemental_vars = {'bathy': In_d_i['files']['bathy']['array'].astype(np.float32)}
    #serialized_features = ftf.serialize_dictionary(supplemental_vars,feature_dict = serialized_features)

    
    # Save Out
    name = f"RTS-PY/runs/Dune3/funwave_data/Validate_1/Out_{tri_num:05}.tfrecord"
    ftf.save_tfrecord(serialized_features,name)
    
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
    