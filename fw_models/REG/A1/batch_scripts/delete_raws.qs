#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-16
#SBATCH --job-name=delete_raws
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/REG/A1/logs/delete_raws/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/REG/A1/logs/delete_raws/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/REG/A1/envs/A1.env
    
    ## Construct name of file
        input_dir="$DATA_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"

    echo "Deleting Raw Outputs from: ${DATA_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    rm -rf "${DATA_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    