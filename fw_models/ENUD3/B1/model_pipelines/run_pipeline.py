import funwave_ds.fw_hpc as pipe

# Inputs to Change
env = '/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/B1/envs/B1.env'

# Files in the pipeline  
generate_file = "/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/B1/model_pipelines/gen.py"
condense_file = "/work/thsu/rschanta/RTS-PY/fw_models/ENUD3/B1/model_pipelines/pro.py"


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
    #pipe.generate_files: {"file": generate_file},
    pipe.condense_outputs: {"file": condense_file,"slurm_edit": {"array": "1-20"}}
}


# Run the pipeline
pipeline.run_pipeline(steps)
