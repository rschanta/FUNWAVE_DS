import subprocess
import os
import re
import sys
import funwave_ds.fw_ba as fba
import funwave_ds.fw_pipe as pipe

# Standard Slurm Flags
slurm_defaults = {
    "nodes": 1,
    "tasks-per-node": 16,
    "partition": "standard",
    "time": "7-00:00:00",
    "mail-user": "rschanta@udel.edu",
    "mail-type": "BEGIN,END,FAIL",
    "export": "ALL"
}

# Path to .env file
env = '/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/SW1.env'

# Initialize the pipeline
pipeline = fba.SlurmPipeline(slurm_vars = slurm_defaults,env=env)

# Files in the pipeline  
generate_file = "/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/model_pipelines/SW1/gen_SW.py"
condense_file = "RTS-PY/fw_models/DUNE3/model_pipelines/SW1/cond_SW.py"  

# Steps of the pipeline
steps = {
    #pipe.generate_files: {"file": generate_file},
    pipe.RuCoDel: {"file": condense_file,"slurm_edit": {"array": "1-1620"}}
}


# Run the pipeline
pipeline.run_pipeline(steps)
