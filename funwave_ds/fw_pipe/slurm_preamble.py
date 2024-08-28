import os
import funwave_ds.fw_ba as fba

## GENERATE FILES
def generate_files(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}
    
    ## Activate Python Environment
    conda activate $CONDA_ENV
    
    ## Export out environment variables
    export $(xargs <{env})
    
    ## Run File
    python "{file}"
    """
    return text_content

## RUN AND CONDENSE
def run_condense_outputs(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}input_${{task_id}}.txt"
    
    ## Run FUNWAVE
        ${{UD_MPIRUN}} $FW_EX "$input_file"

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs <{env})
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "{file}"

    """
    return text_content


