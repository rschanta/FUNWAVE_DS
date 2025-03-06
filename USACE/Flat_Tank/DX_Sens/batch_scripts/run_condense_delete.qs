#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --exclude=r03n56
#SBATCH --array=1-780
#SBATCH --job-name=run_condense_delete
#SBATCH --dependency=29804011
#SBATCH --output=/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Sens/logs/run_condense_delete/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Sens/logs/run_condense_delete/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Sens/envs/DX_Sens.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
        echo "Running ${input_file}"
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_EX "$input_file"

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/USACE/Flat_Tank/DX_Sens/envs/DX_Sens.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    export FUNC_NAME=run_condense_delete
    
    ## Run the Compression File
    python "RTS-PY/USACE/Flat_Tank/DX_Sens/model_pipelines/pro.py"

    ## Run the Raw Output Deletions
    #echo "Deleting Input File(s)"
    #rm -rf "${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/inputs/input_${task_id}.txt"
    #rm -rf "${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/inputs/input_${task_id}.txt"

    #echo "Deleting Raw Outputs from: ${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    rm -rf "${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
  
    