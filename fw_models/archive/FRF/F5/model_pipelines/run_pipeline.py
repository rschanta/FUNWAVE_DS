import funwave_ds.fw_hpc as pipe

RUN_NAME = 'FRF'
TRI_NAME = 'F5'
# Inputs to Change
env = f'/work/thsu/rschanta/RTS-PY/fw_models/{RUN_NAME}/{TRI_NAME}/envs/{TRI_NAME}.env'

# Files in the pipeline  
generate_file = f"/work/thsu/rschanta/RTS-PY/fw_models/{RUN_NAME}/{TRI_NAME}/model_pipelines/gen.py"
condense_file = f"/work/thsu/rschanta/RTS-PY/fw_models/{RUN_NAME}/{TRI_NAME}/model_pipelines/pro.py"


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



# Initialize the pipeline
pipeline = pipe.SlurmPipeline(slurm_vars = slurm_defaults,env=env)

# Steps of the pipeline
steps = {
    pipe.generate_files: {"file": generate_file},
    pipe.RuCoDel: {"file": condense_file,"slurm_edit": {"array": "1-1001"}}
}


# Run the pipeline
pipeline.run_pipeline(steps)
