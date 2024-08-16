import subprocess
import os
import re
import sys
# Path Commands
sys.path.append("/work/thsu/rschanta/RTS-PY")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))

# Import needed functions
import python_code.core_packages.bash as ba


#%% Key slurm parameters
email = "rschanta@udel.edu"
work_dir = "/work/thsu/rschanta/RTS-PY"
run_name = "test_matrix3"
env_name = "tf_env"
super_path = "/lustre/scratch/rschanta"
FW_ex = "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG"

##########################################################
#%% Generation File
##########################################################
# Set the slurm tags
tags2 = ba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="gen")

gen_file = "p01_gen_files.py"

# Set commands under the slurm tags
text_content = f"""
## Activate conda environment and compress
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipeline/{gen_file} {super_path} {run_name} 
"""

# Generate sbatch .qs script
gen_script = ba.write_slurm_script(tags2,work_dir,run_name,text_content)
# Run .qs script and get ID
gen_ID = ba.submit_slurm_job(gen_script)



##########################################################
#%% Run File
##########################################################
tags = ba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="run",
                            array="1-40",
                            dependency=f"afterany:{gen_ID}")


compress_file = "p02_condense.py"

# Text to include under slurm tags
text_content = f"""
. /opt/shared/slurm/templates/libexec/openmpi.sh
## Construct name of file
    input_dir="{super_path}/{run_name}/inputs/"
    task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
    input_file="${{input_dir}}input_${{task_id}}.txt"
## Run FUNWAVE
    ${{UD_MPIRUN}} {FW_ex} "$input_file"

## COMPRESS
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipeline/{compress_file} {super_path} {run_name}  $SLURM_ARRAY_TASK_ID
"""

# Generate sbatch .qs script
run_script = ba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
run_ID = ba.submit_slurm_job(run_script)



##########################################################
#%% Postprocessing
##########################################################
tags = ba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="posta",
                            array="1-40",
                            dependency=f"afterany:{run_ID}")
postproc_file = "p03a_postprocess.py"

# Text to include under slurm tags
text_content = f"""
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipeline/{postproc_file} {super_path} {run_name}  $SLURM_ARRAY_TASK_ID
"""
# Generate sbatch .qs script
post_script_a = ba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
post_a_ID = ba.submit_slurm_job(post_script_a)
