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
    "FW_MODEL": "DFR_Pi",
    "RUN_NAME": "TMA2"})

d = fba.get_directories()

# Standard Slurm Flags
slurm_defaults = {
    "nodes": 1,
    "tasks-per-node": 16,
    "partition": "thsu",
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
from pipeline import generate_files, run_condense_outputs, condense_outputs, run_ML_preproc, run_ML_model

def run_ML_preproc2(file=None):
    d = fba.get_directories()
    text_content = f"""
    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR={d['WORK_DIR']} 
    export DATA_DIR={d['DATA_DIR']}
    export TEMP_DIR={d['TEMP_DIR']}
    export FW_MODEL={d['FW_MODEL']}
    export RUN_NAME={d['RUN_NAME']}
    export TRI_NUM=$SLURM_ARRAY_TASK_ID

    ## Generate Inputs
    python "{d['WORK_DIR']}/fw_models/{d['FW_MODEL']}/model_pipelines/{d['RUN_NAME']}/{file}"
    """
    return text_content


# Define the steps with their respective arguments and optional SLURM edits
    #generate_files: {"file": "p01_generate_files.py"},      generate_files: {"file": "p01_generate_files.py"},       
    #run_condense_outputs: {"FW_ex": FW_ex, "file": "p02_run_condense.py", "slurm_edit": {"array": "1-576"}},  
steps = {
    run_ML_model: {"file": "p04_machine_learning.py"},
    #run_ML_model: {"file": "p03_machine_learning.py.py"}
}
# Run the pipeline
pipeline.run_pipeline(steps)
