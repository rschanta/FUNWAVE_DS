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

## RUN FUNWAVE
def run_FW(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$in"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}input_${{task_id}}.txt"
    
    ## Run FUNWAVE
        ${{UD_MPIRUN}} $FW_ex "$input_file"


    """
    return text_content


## RUN AND CONDENSE
def run_condense(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$in"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}/input_${{task_id}}.txt"
    
    ## Run FUNWAVE
        ${{UD_MPIRUN}} $FW_ex "$input_file"

    ## Activate Python Environment
    conda activate $conda

    ## Export out environment variables
    export $(xargs <{env})
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "{file}"

    """
    return text_content


## DELETE RAW DATA
def delete_raws(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}
    
    ## Construct name of file
        input_dir="$DATA_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}input_${{task_id}}.txt"

    echo "Deleting Raw Outputs from: ${{TEMP_DIR}}/${{FW_MODEL}}/${{RUN_NAME}}/outputs-raw/out_${{task_id}}"
    rm -rf "${{TEMP_DIR}}/${{FW_MODEL}}/${{RUN_NAME}}/outputs-raw/out_${{task_id}}"
    """
    return text_content


## CONDENSE OUTPUTS
def condense(file=None,env=None):

    text_content = f"""
    ## Access environment variables
    source {env}

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs <{env})
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "{file}"

    """
    return text_content


## RUN CONDENSE AND DELETE
def run_condense_delete(file=None,env=None):
    # Get function name and construct output file
    func_name = run_condense_delete.__name__ 

    text_content = f"""
    ## Access environment variables
    source {env}

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$in"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${{input_dir}}/input_${{task_id}}.txt"

    ## Run FUNWAVE
        ${{UD_MPIRUN}} $FW_ex "$input_file"

    ## Activate Python Environment
    conda activate $conda

    ## Export out environment variables
    export $(xargs <{env})
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    export FUNC_NAME={func_name}
    
    ## Run the Compression File
    python "{file}"

    ## Run the Raw Output Deletions
    
    echo "Deleting Raw Outputs from: ${{or}}/out_raw_${{task_id}}"
    rm -rf "${{or}}/out_raw_${{task_id}}"
  
    """
    return text_content


