import copy
import os
import re
import subprocess
import sys
from dotenv import load_dotenv


def write_slurm_script(work_dir,run_name,matrix,all_slurm_flags,script_body=None):
    # Make folder if it doesn't exist for batch scripts
    batch_dir = os.path.join(work_dir, 'fw_models',run_name, 'batch_scripts',matrix)
    os.makedirs(batch_dir, exist_ok=True)
    
    # Name of batch script (based on process)
    batch_name = os.path.join(batch_dir,f'{all_slurm_flags["job-name"]}.qs')

    with open(batch_name, 'w') as file:
        # Write the shebang line
        file.write("#!/bin/bash -l\n")
        file.write("#\n")  
        
        # Write the SLURM directives
        for key, value in all_slurm_flags.items():
            if value is not None:
                file.write(f"#SBATCH --{key}={value}\n")
        file.write("#\n")  
        if script_body:
                file.write(script_body)

    return batch_name



###############################################################

###############################################################
def make_log_folders(work_dir,run_name,matrix,all_slurm_flags):
    # Just one folder if no array
    if all_slurm_flags.get('array') is None:
        job_name = all_slurm_flags['job-name']
        print(work_dir)
        print(run_name)
        print(matrix)
        print(job_name)
        out_err_dir = os.path.join(work_dir, 'fw_models',run_name, 'logs',matrix,job_name)
        os.makedirs(out_err_dir, exist_ok=True)
        all_slurm_flags['output'] =  os.path.join(out_err_dir,'out.out')
        all_slurm_flags['error'] =  os.path.join(out_err_dir, 'err.out') 
    # Separate dir for outputs and errors if an array
    else:
        job_name = all_slurm_flags['job-name']
        out_dir = os.path.join(work_dir, 'fw_models',run_name, 'logs',matrix,job_name,'out')
        err_dir = os.path.join(work_dir, 'fw_models',run_name, 'logs',matrix,job_name,'err')
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(err_dir, exist_ok=True)
        all_slurm_flags['output'] = os.path.join(out_dir,'out%a.out')
        all_slurm_flags['error'] = os.path.join(err_dir, 'err%a.out') 
    return all_slurm_flags

def submit_slurm_job(script_path):
    
    # Try running the sbatch command
    try:
        # Subprocess command
        result = subprocess.run(
            ['sbatch', script_path],
            capture_output=True,    # To get jobID
            text=True,              # To get as text (not bytes)
            check=True              # To get errors
        )
        
        # Extract the job ID using a regular expression
        output = result.stdout
        job_id_match = re.search(r'Submitted batch job (\d+)', output)
        
        # Return job ID if found
        if job_id_match:
            job_id = job_id_match.group(1)
            return job_id
        else:
            return "Job ID not found in sbatch output."
    
    # Return error if any issues
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess call
        return f"Error occurred: {e.stderr}"


def get_directories():
    env_vars = {
        "WORK_DIR": os.getenv("WORK_DIR"),
        "DATA_DIR": os.getenv("DATA_DIR"),
        "TEMP_DIR": os.getenv("TEMP_DIR"),
        "FW_MODEL": os.getenv("FW_MODEL"),
        "RUN_NAME": os.getenv("RUN_NAME")
    }
    
    return env_vars


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