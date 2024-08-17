import subprocess
import os
import re
import sys
# Make sure workdir is on the path
sys.path.append("/work/thsu/rschanta/RTS-PY")
import funwave_ds.fw_ba as fba

# Standard Slurm Flags
slurm_defaults = {
    "nodes": 1,
    "tasks-per-node": 32,
    "partition": "standard",
    "time": "7-00:00:00",
    "mail-user": "rschanta@udel.edu",
    "mail-type": "BEGIN,END,FAIL",
    "export": "ALL"
}

work_dir = "/work/thsu/rschanta/RTS-PY"
run_name = "test_matrix3"
env_name = "tf_env"
super_path = "/lustre/scratch/rschanta"

os.environ['WORK_DIR'] = "/work/thsu/rschanta/RTS-PY"
os.environ['RUN_NAME'] = "test_matrix3"
os.environ['SUPER_PATH'] = "/lustre/scratch/rschanta"
os.environ['ENV_NAME'] = "tf_env"

FW_ex = "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG"

# Initialize the pipeline
# TODO: Environment variable it!
pipeline = fba.SlurmPipeline(slurm_vars=slurm_defaults, 
                         work_dir=work_dir, run_name=run_name, env_name=env_name)

# Import parts of the pipeline
from pipeline1 import generate_files, run_files,postprocessa,postprocessb,ml_model

# Define the steps with their respective arguments and optional SLURM edits
steps = {
    generate_files: {"file": "p01_gen_files.py"},
    run_files: {"FW_ex": FW_ex, "file": "p02_condense.py", "slurm_edit": {"array": "1-40"}},
    postprocessa: {"file": "p03a_postprocess.py", "slurm_edit": {"array": "1-40"}},
    postprocessb: {"file": "p03b_postprocess.py"},
    ml_model: {"file": "p04_ml_model.py"}
}

# Run the pipeline
pipeline.run_pipeline(steps)
