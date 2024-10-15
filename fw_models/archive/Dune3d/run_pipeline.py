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
env = 'RTS-PY/fw_models/Dune3d/envs/T1.env'

# Initialize the pipeline
pipeline = fba.SlurmPipeline(slurm_vars = slurm_defaults,env=env)

# Files in the pipeline  
generate_file = "/work/thsu/rschanta/RTS-PY/fw_models/Dune3d/model_pipelines/T1/generate.py"
run_condense = "/work/thsu/rschanta/RTS-PY/fw_models/Dune3d/model_pipelines/common/run_condense.py"  

# Steps of the pipeline
steps = {
    pipe.generate_files: {"file": generate_file},
    pipe.run_condense_outputs: {"file": run_condense,"slurm_edit": {"array": "1-5"}}
}

# Run the pipeline
pipeline.run_pipeline(steps)
