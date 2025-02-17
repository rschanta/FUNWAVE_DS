import funwave_ds.fw_hpc as pipe

# Inputs to Change
env = '/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/envs/Time_Sens.env'

# Files in the pipeline  
generate_file = "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/model_pipelines/gen.py"
condense_file = "/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/Time_Sens/model_pipelines/pro.py"


# Standard Slurm Flags
slurm_defaults = {
    "nodes": 1,
    "tasks-per-node": 32,
    "partition": "thsu",
    "time": "7-00:00:00",
    "mail-user": "rschanta@udel.edu",
    "mail-type": "BEGIN,END,FAIL",
    "export": "ALL"
}



# Initialize the pipeline
pipeline = pipe.SlurmPipeline(slurm_vars = slurm_defaults,
                              env=env)

# Steps of the pipeline
steps = {
    pipe.generate_files: {"file": generate_file},
    pipe.run_condense_delete: {"file": condense_file,"slurm_edit": {"array": "1-216"}}
}


# Run the pipeline
pipeline.run_pipeline(steps)
