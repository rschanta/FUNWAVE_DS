import copy
import os
import re
import subprocess
import sys
from dotenv import load_dotenv

#%%
def make_log_folders(log_dir,all_slurm_flags):
    '''
    Make the folders for the log files from slurm outputs, and
    adjust flags as needed to work with this.
    '''

    # Just one folder if no array
    if all_slurm_flags.get('array') is None:
        # Get the job name from the slurm flags
        job_name = all_slurm_flags['job-name']
        # Construct/make the directory for the logs `log_dir/job_name`
        out_err_dir = os.path.join(log_dir,job_name)
        os.makedirs(out_err_dir, exist_ok=True)
        # Construct the actual name of the path to an error/out file
        all_slurm_flags['output'] =  os.path.join(out_err_dir,'out.out')
        all_slurm_flags['error'] =  os.path.join(out_err_dir, 'err.out') 
        print(f'Slurm output log folder created: {out_dir}')
        print(f'Slurm error log folder created: {err_dir}')

    # If array, need to do slurm flags with %- add an extra folder layer for clarity
    else:
        # Get the job name from the slurm flags
        job_name = all_slurm_flags['job-name']
        # Construct/make the directory for the out logs `log_dir/job_name/out`
        out_dir = os.path.join(log_dir,job_name,'out')
        os.makedirs(out_dir, exist_ok=True)
        # Construct/make the directory for the error logs `log_dir/job_name/out`
        err_dir = os.path.join(log_dir, job_name,'err')
        os.makedirs(err_dir, exist_ok=True)
        # Construct the actual name of the path to an error/out file, using array syntax
        all_slurm_flags['output'] = os.path.join(out_dir,'out%a.out')
        all_slurm_flags['error'] = os.path.join(err_dir, 'err%a.out') 
        # Echo results
        print(f'Slurm output log folder created: {out_dir}')
        print(f'Slurm error log folder created: {err_dir}')
    return all_slurm_flags




#%%
def get_directories():
    env_vars = {
        "WORK_DIR": os.getenv("WORK_DIR"),
        "DATA_DIR": os.getenv("DATA_DIR"),
        "TEMP_DIR": os.getenv("TEMP_DIR"),
        "FW_MODEL": os.getenv("FW_MODEL"),
        "RUN_NAME": os.getenv("RUN_NAME")
    }
    
    return env_vars

#%%
def write_slurm_script(batch_dir,
                       all_slurm_flags,
                       script_body=None):
    '''
    Write the slurm script, with the required flags 
    and the input body
    '''


    # Get name/path of batch script based on job-name
    job_name = all_slurm_flags["job-name"]
    file_name = f'{job_name}.qs'
    script_path = os.path.join(batch_dir,file_name)

    # Open the file to write to
    with open(script_path, 'w') as file:
        # Write the shebang line
        file.write("#!/bin/bash -l\n")
        file.write("#\n")  
        
        # Write the SLURM directives
        for slurm_flag, flag_value in all_slurm_flags.items():
            if flag_value is not None:
                file.write(f"#SBATCH --{slurm_flag}={flag_value}\n")
        file.write("#\n")  

        # Write the slurm body defined
        if script_body:
                file.write(script_body)

    print(f'Batch script created: {script_path}')
    return script_path

#%%
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