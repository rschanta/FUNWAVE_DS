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
    def __init__(self,slurm_vars = None,env=None):
        # Dictionary of defauly slurm variables
        self.slurm_vars = slurm_vars

        # Load environment variables
        load_dotenv(dotenv_path=env)
        self.work_dir = os.getenv('WORK_DIR')
        self.fw_model = os.getenv('FW_MODEL')
        self.run_name = os.getenv('RUN_NAME')
        self.temp_dir = os.getenv('TEMP_DIR')
        self.data_dir = os.getenv('DATA_DIR')
        self.env = os.getenv('ENV_FILE_PATH')
        
        # Dictionary of Job IDs
        self.job_id = None

    # Add a job to the pipeline
    def add_job(self, dep_flags, script_content_func, **kwargs):

        ## Slurm Flags
        # Extract SLURM edits and other parameters from kwargs
        slurm_edit = kwargs.pop('slurm_edit', {})
        
        # Slurm Flags
        all_slurm_flags = {**self.slurm_vars, **slurm_edit, **dep_flags}

        # Make log folders, set in slurm flags
        all_slurm_flags = make_log_folders(self.work_dir, self.fw_model,self.run_name,all_slurm_flags)

        ## Body of Script
        script_body = script_content_func(**kwargs)
        
        # Write the slurm script
        script = write_slurm_script(self.work_dir,
                                        self.fw_model,
                                        self.run_name,
                                        all_slurm_flags,
                                        script_body)
        
        # Run the slurm script
        job_id = submit_slurm_job(script)

        # Add the IDs to the job id list
        self.job_id = job_id
        return job_id

    def run_pipeline(self, steps):
        # Track the job ID of the previous step to handle dependencies
        previous_job_id = self.job_id

        # Loop through all steps
        for step_func, kwargs in steps.items():
            # Name the job using the function name
            job_name = step_func.__name__
            
            # Add environment variables 
            kwargs['env'] = self.env

            # Add job name and dependency (not 1st)
            if previous_job_id is not None:
                dep_flags = {'job-name': job_name,
                             'dependency': previous_job_id}
            # Add job name (if it is first)
            elif previous_job_id is None:
                dep_flags = {'job-name': job_name}
            
            # Run the job, get ID
            job_id = self.add_job(dep_flags, step_func, **kwargs)

            # Update the last job_id
            previous_job_id = job_id