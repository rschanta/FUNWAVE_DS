import copy
import os
import re
import subprocess
import sys
from dotenv import load_dotenv

###############################################################

###############################################################
def make_log_folders(work_dir,run_name,matrix,all_slurm_flags):
    # Just one folder if no array
    if all_slurm_flags.get('array') is None:
        job_name = all_slurm_flags['job-name']
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





def get_directories():
    env_vars = {
        "WORK_DIR": os.getenv("WORK_DIR"),
        "DATA_DIR": os.getenv("DATA_DIR"),
        "TEMP_DIR": os.getenv("TEMP_DIR"),
        "FW_MODEL": os.getenv("FW_MODEL"),
        "RUN_NAME": os.getenv("RUN_NAME")
    }
    
    return env_vars

###############################################################

###############################################################
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