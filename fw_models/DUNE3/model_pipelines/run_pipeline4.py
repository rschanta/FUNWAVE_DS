import funwave_ds.fw_hpc as pipe

# Inputs to Change
env = '/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/T04_d.env'

# Files in the pipeline  
generate_file = "/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/model_pipelines/T04_d/gen.py"
condense_file = "/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/model_pipelines/T04_d/pro.py"  

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
    pipe.run_condense_outputs: {"file": condense_file,"slurm_edit": {"array": "1-3"}}
}


# Run the pipeline
pipeline.run_pipeline(steps)
