import subprocess
import os
import re
import sys
import funwave_ds.fw_ba as fba

# Directories
fba.set_env_vars({
    "WORK_DIR": "/work/thsu/rschanta/RTS-PY",
    "DATA_DIR": "/work/thsu/rschanta/DATA",
    "TEMP_DIR": "/lustre/scratch/rschanta",
    "FW_MODEL": "Dune3c",
    "RUN_NAME": "Val_2"})

d = fba.get_directories()

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


# Other variables
FW_ex = "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG"

# Initialize the pipeline
pipeline = fba.SlurmPipeline2(slurm_vars = slurm_defaults)

# Import parts of the pipeline
from pipeline import generate_files, run_condense_outputs, condense_outputs

# Define the steps with their respective arguments and optional SLURM edits
#        
steps = {
    generate_files: {"file": "p01_generate_files.py"}, 
    run_condense_outputs: {"FW_ex": FW_ex, "file": "p02_run_condense.py", "slurm_edit": {"array": "1-20"}},
}

# Run the pipeline
pipeline.run_pipeline(steps)
