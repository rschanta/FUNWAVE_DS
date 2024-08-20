import os
import funwave_ds.fw_ba as fba
# Get environment variables
d = fba.get_directories()


## GENERATE FILES
def generate_files(file=None):
    d = fba.get_directories()
    text_content = f"""
    ## Activate conda environment
    conda activate tf_env

    ## Export environment variables
    export WORK_DIR={d['WORK_DIR']} 
    export DATA_DIR={d['DATA_DIR']}
    export TEMP_DIR={d['TEMP_DIR']}
    export FW_MODEL={d['FW_MODEL']}
    export RUN_NAME={d['RUN_NAME']}

    ## Generate Inputs
    python "{d['WORK_DIR']}/fw_models/{d['FW_MODEL']}/model_pipelines/{d['RUN_NAME']}/{file}"
    """
    return text_content

## RUN AND CONDENSE
def run_files(file=None,FW_ex=None):
    d = fba.get_directories()
    text_content = f"""
    . /opt/shared/slurm/templates/libexec/openmpi.sh
    ## Construct name of file
        input_dir="{d['TEMP_DIR']}/{d['FW_MODEL']}/{d['RUN_NAME']}/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}input_${{task_id}}.txt"
    ## Run FUNWAVE
        ${{UD_MPIRUN}} {FW_ex} "$input_file"

    ## COMPRESS
    conda activate tf_env
    export WORK_DIR={d['WORK_DIR']} 
    export DATA_DIR={d['DATA_DIR']}
    export TEMP_DIR={d['TEMP_DIR']}
    export FW_MODEL={d['FW_MODEL']}
    export RUN_NAME={d['RUN_NAME']}
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "{d['WORK_DIR']}/fw_models/{d['FW_MODEL']}/model_pipelines/{d['RUN_NAME']}/{file}"

    ## Remove Raw Folder

    """
    return text_content