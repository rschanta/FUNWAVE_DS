import copy
import os
import re
import subprocess
import sys
from dotenv import load_dotenv
from .slurm_utils import *

###############################################################

###############################################################
class SlurmPipeline:
    ## INITIALIZE THE PIPELINE
    def __init__(self,
                 slurm_vars = None,
                 env=None):
        
        # Dictionary of default slurm variables
        self.slurm_vars = slurm_vars

        # Load necessary environments
        load_dotenv(dotenv_path=env)
        self.env = env
        self.log_dir = os.getenv('logs')
        self.batch_dir = os.getenv('batch')
        
        # Dictionary of Job IDs
        self.job_id = None


    ## ADD A JOB TO THE PIPELINE
    def add_job(self, dep_flags, script_content_func, **kwargs):

        # Slurm edit parameters
        slurm_edit = kwargs.pop('slurm_edit', {})
        
        # Slurm Flags
        all_slurm_flags = {**self.slurm_vars, # Default flags
                           **slurm_edit,      # Edited flags
                           **dep_flags}       # Dependency flags

        # Make log folders, set/edit slurm flags as needed
        all_slurm_flags = make_log_folders(self.log_dir,
                                           all_slurm_flags)

        ## Body of Script
        script_body = script_content_func(**kwargs)
        
        # Write the slurm script
        script = write_slurm_script(self.batch_dir,
                                        all_slurm_flags,
                                        script_body)
        
        # Run the slurm script
        job_id = submit_slurm_job(script)

        # Add the IDs to the job id list
        self.job_id = job_id
        return job_id

    ## RUN PIPELINE
    def run_pipeline(self, steps):
        # Track the job ID of the previous step to handle dependencies
        previous_job_id = self.job_id

        # Loop through all steps
        for step_func, kwargs in steps.items():
            # Set the job name using the function name
            job_name = step_func.__name__
            
            # All slurm bodies need the environment path
            kwargs['env'] = self.env

            # If this is the first job, just add job_name
            if previous_job_id is None:
                dep_flags = {'job-name': job_name}

            # If this is a dependent script, also need last job_id
            elif previous_job_id is not None:
                dep_flags = {'job-name': job_name,
                             'dependency': previous_job_id}

            # Add the job and submit
            job_id = self.add_job(dep_flags, step_func, **kwargs)

            # Update the last job_id
            previous_job_id = job_id