import subprocess
import os
import re
tasks_per_node = 32
email = "rschanta@udel.edu"
work_dir = "."
run_name = "test_matrix2"

def create_sbatch_dict(nodes=1, 
                       tasks_per_node=32, 
                       job_name="Funwave_Job", 
                       partition="standard", 
                       time="7-00:00:00", 
                       output="out.out", 
                       error="error.out", 
                       email="email@email.edu", 
                       mail_type="BEGIN,END,FAIL", 
                       export="ALL"):
    # Standard Tags
    sbatch_tags = {
        "nodes": str(nodes),
        "tasks-per-node": str(tasks_per_node),
        "job-name": job_name,
        "partition": partition,
        "time": time,
        "output": output,
        "error": error,
        "mail-user": email,
        "mail-type": mail_type,
        "export": export
    }

    return sbatch_tags

def add_features(sbatch_tags, new_tags):
    updated_sbatch_tags = sbatch_tags.copy()  # Create a copy to avoid modifying the original dictionary
    updated_sbatch_tags.update(new_tags)  # Merge new_tags into updated_sbatch_tags
    return updated_sbatch_tags

def set_logs(sbatch_tags,work_dir,run_name,process_name,array = False):
    updated_sbatch_tags = sbatch_tags.copy()
    
    
    # Just one dir for both outputs/errors
    if array == False:
        out_err_dir = os.path.join(work_dir, 'runs',run_name, 'logs',process_name)
        os.makedirs(out_err_dir, exist_ok=True)
        updated_sbatch_tags['output'] =  os.path.join(out_err_dir,'out.out')
        updated_sbatch_tags['error'] =  os.path.join(out_err_dir, 'err.out') 
    # Separate dir for outputs and errors if an array
    else:
        out_dir = os.path.join(work_dir, 'runs',run_name, 'logs',process_name,'out')
        err_dir = os.path.join(work_dir, 'runs',run_name, 'logs',process_name,'err')
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(err_dir, exist_ok=True)
        updated_sbatch_tags['output'] =  os.path.join(out_dir,'out%a.out')
        updated_sbatch_tags['error'] =  os.path.join(err_dir, 'err%a.out') 
    
    return updated_sbatch_tags



def write_slurm_script(tags,work_dir,run_name,process_name,text_content):
    
    # Make folder if it doesn't exist for batch scripts
    batch_dir = os.path.join(work_dir, 'runs',run_name, 'batch_scripts',process_name)
    os.makedirs(batch_dir, exist_ok=True)
    
    # Name of batch script (based on process)
    batch_name = os.path.join(batch_dir,f'batch_dir{process_name}.qs')
    
    with open(batch_name, 'w') as file:
        # Write the shebang line
        file.write("#!/bin/bash -l\n")
        file.write("#\n")  
        
        # Write the SLURM directives
        for key, value in tags.items():
            file.write(f"#SBATCH --{key}={value}\n")
        file.write("#\n")  
        if text_content:
                file.write(text_content)
                
                
def submit_slurm_job(script_path):
    """
    Submits a SLURM job using the sbatch command and extracts the job ID.

    Args:
        script_path (str): The path to the SLURM script to be submitted.

    Returns:
        str: The job ID extracted from the sbatch command output, or an error message.
    """
    try:
        # Run the sbatch command
        result = subprocess.run(
            ['sbatch', script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract the job ID using a regular expression
        output = result.stdout
        job_id_match = re.search(r'Submitted batch job (\d+)', output)
        
        if job_id_match:
            job_id = job_id_match.group(1)
            return job_id
        else:
            return "Job ID not found in sbatch output."
    
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess call
        return f"Error occurred: {e.stderr}"

#%% Generation File
tags = create_sbatch_dict(email=email)
tags = set_logs(tags,work_dir,run_name,'gen')

text_content = """
## Activate conda environment and compress
conda activate tf_env
python /work/thsu/rschanta/RTS-PY/mains/generate_inputs.py "/lustre/scratch/rschanta" "FSPY2" 
"""

write_slurm_script(tags,work_dir,run_name,'gen',text_content)

#%% Run File
tags = create_sbatch_dict(email=email)
tags = add_features(tags, {'array':"1-500","dependency":"yes"})

text_content = """
. /opt/shared/slurm/templates/libexec/openmpi.sh
## Construct name of file
    input_dir="/lustre/scratch/rschanta/test_matrix/inputs/"
    task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
    input_file="${input_dir}input_${task_id}.txt"
## Run FUNWAVE
    ${UD_MPIRUN} "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG" "$input_file"

## COMPRESS
conda activate tf_env
python "/work/thsu/rschanta/RTS-PY/mains/m02_condense.py" "/lustre/scratch/rschanta" "test_matrix" $SLURM_ARRAY_TASK_ID
"""
write_slurm_script(tags,work_dir,run_name,'run',text_content)