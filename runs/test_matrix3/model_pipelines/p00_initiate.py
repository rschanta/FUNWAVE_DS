import subprocess
import os
import re
import sys
# Make sure workdir is on the path
sys.path.append("/work/thsu/rschanta/RTS-PY")

# Import needed functions
import funwave_ds.fw_ba as fba


#%% Key Input parameters
email = "rschanta@udel.edu"
work_dir = "/work/thsu/rschanta/RTS-PY"
run_name = "test_matrix3"
env_name = "tf_env"
super_path = "/lustre/scratch/rschanta"
FW_ex = "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG"

'''
##########################################################
#%% Generation File
##########################################################
# Set the slurm tags
tags2 = fba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="gen")

gen_file = "p01_gen_files.py"

# Set commands under the slurm tags
text_content = f"""
## Activate conda environment and compress
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipelines/{gen_file} {super_path} {run_name} 
"""

# Generate sbatch .qs script
gen_script = fba.write_slurm_script(tags2,work_dir,run_name,text_content)
# Run .qs script and get ID
gen_ID = fba.submit_slurm_job(gen_script)



##########################################################
#%% Run File
##########################################################
tags = fba.create_sbatch_dict(work_dir,run_name,
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
python {work_dir}/runs/{run_name}/model_pipelines/{compress_file} {super_path} {run_name}  $SLURM_ARRAY_TASK_ID
"""

# Generate sbatch .qs script
run_script = fba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
run_ID = fba.submit_slurm_job(run_script)


##########################################################
#%% Postprocessing
##########################################################
tags = fba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="posta",
                            array="1-40") #,
                            #dependency=f"afterany:{run_ID}")
postproc_file = "p03a_postprocess.py"

# Text to include under slurm tags
text_content = f"""
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipelines/{postproc_file} {super_path} {run_name}  $SLURM_ARRAY_TASK_ID
"""
# Generate sbatch .qs script
post_script_a = fba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
post_a_ID = fba.submit_slurm_job(post_script_a)


##########################################################
#%% Postprocessing b
##########################################################
tags = fba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="postb") #,
                            #dependency=f"afterany:{run_ID}")
postproc_file = "p03b_postprocess.py"

# Text to include under slurm tags
text_content = f"""
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipelines/{postproc_file} {super_path} {run_name} 
"""
# Generate sbatch .qs script
post_script_a = fba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
post_b_ID = fba.submit_slurm_job(post_script_a)
'''

##########################################################
#%% ML Model
##########################################################
tags = fba.create_sbatch_dict(work_dir,run_name,
                            email=email,
                            job_name="ml_model") #,
                            #dependency=f"afterany:{run_ID}")
ml_file = "p04_ml_model.py"

# Text to include under slurm tags
text_content = f"""
conda activate {env_name}
python {work_dir}/runs/{run_name}/model_pipelines/{ml_file} {super_path} {run_name} "test_model"
"""
# Generate sbatch .qs script
ml_script = fba.write_slurm_script(tags,work_dir,run_name,text_content)
# Run .qs script and get ID
ml_script_ID = fba.submit_slurm_job(ml_script)
