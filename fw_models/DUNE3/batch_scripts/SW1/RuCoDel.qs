#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-1620
#SBATCH --job-name=RuCoDel
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/SW1/RuCoDel/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/DUNE3/logs/SW1/RuCoDel/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/SW1.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
    
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_EX "$input_file"

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/DUNE3/envs/SW1.env)
    export TRI_NUM=$SLURM_ARRAY_TASK_ID
    
    python "RTS-PY/fw_models/DUNE3/model_pipelines/SW1/cond_SW.py"

    echo "Deleting Raw Outputs from: ${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    rm -rf "${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    