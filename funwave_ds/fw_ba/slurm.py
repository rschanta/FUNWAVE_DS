import subprocess
import os
import re

'''

def create_sbatch_dict(work_dir,run_name,
                       nodes=1, 
                       tasks_per_node=32, 
                       job_name="Funwave_Job", 
                       partition="standard", 
                       time="7-00:00:00", 
                       output="out.out", 
                       error="error.out", 
                       email="email@email.edu", 
                       mail_type="BEGIN,END,FAIL", 
                       export="ALL",
                       array=None,
                       dependency=None):
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
        "export": export,
        "array": array,
        "dependency": dependency
    }

    ## Create folder for logs
    # Just one dir for both outputs/errors
    if array == None:
        out_err_dir = os.path.join(work_dir, 'runs',run_name, 'logs',job_name)
        os.makedirs(out_err_dir, exist_ok=True)
        sbatch_tags['output'] =  os.path.join(out_err_dir,'out.out')
        sbatch_tags['error'] =  os.path.join(out_err_dir, 'err.out') 
    # Separate dir for outputs and errors if an array
    else:
        out_dir = os.path.join(work_dir, 'runs',run_name, 'logs',job_name,'out')
        err_dir = os.path.join(work_dir, 'runs',run_name, 'logs',job_name,'err')
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(err_dir, exist_ok=True)
        sbatch_tags['output'] =  os.path.join(out_dir,'out%a.out')
        sbatch_tags['error'] =  os.path.join(err_dir, 'err%a.out') 

    return sbatch_tags

def add_features(sbatch_tags, new_tags):
    updated_sbatch_tags = sbatch_tags.copy()  # Create a copy to avoid modifying the original dictionary
    updated_sbatch_tags.update(new_tags)  # Merge new_tags into updated_sbatch_tags
    return updated_sbatch_tags

def set_logs(sbatch_tags,work_dir,run_name,process_name,array = False):
    '''
        Create and set the log directories for the slurm script
    '''
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



def write_slurm_script(tags,work_dir,run_name,text_content):
    
    # Make folder if it doesn't exist for batch scripts
    batch_dir = os.path.join(work_dir, 'runs',run_name, 'batch_scripts')
    os.makedirs(batch_dir, exist_ok=True)
    
    # Name of batch script (based on process)
    batch_name = os.path.join(batch_dir,f'{tags["job-name"]}.qs')
    
    with open(batch_name, 'w') as file:
        # Write the shebang line
        file.write("#!/bin/bash -l\n")
        file.write("#\n")  
        
        # Write the SLURM directives
        for key, value in tags.items():
            if value is not None:
                file.write(f"#SBATCH --{key}={value}\n")
        file.write("#\n")  
        if text_content:
                file.write(text_content)
    return batch_name
                
'''