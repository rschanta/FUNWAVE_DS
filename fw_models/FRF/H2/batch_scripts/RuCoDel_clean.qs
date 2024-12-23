#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-3500
#SBATCH --job-name=RuCoDelCLEAN
#SBATCH --output=/work/thsu/rschanta/RTS-PY/fw_models/FRF/H2/logs/RuCoDel2/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/fw_models/FRF/H2/logs/RuCoDel2/err/err%a.out
#

    ## Access environment variables
    source /work/thsu/rschanta/RTS-PY/fw_models/FRF/H2/envs/H2.env

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    
    ## Get File Name
    my_value=$(sed -n "$((SLURM_ARRAY_TASK_ID))p" /work/thsu/rschanta/MISC/values_UPDATE.txt)
    echo "Running task with value: $my_value"
    ## Construct name of file
        input_dir="$TEMP_DIR/$FW_MODEL/$RUN_NAME/inputs/"
        task_id=$(printf "%05d" $my_value)
        input_file="${input_dir}input_${task_id}.txt"
        echo "Running ${input_file}"
    ## Run FUNWAVE
        ${UD_MPIRUN} $FW_EX "$input_file"

    ## Activate Python Environment
    conda activate $CONDA_ENV

    ## Export out environment variables
    export $(xargs </work/thsu/rschanta/RTS-PY/fw_models/FRF/H2/envs/H2.env)
    export TRI_NUM=$task_id
    
    python "/work/thsu/rschanta/RTS-PY/fw_models/FRF/H2/model_pipelines/pro.py"

    echo "Deleting Raw Outputs from: ${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    rm -rf "${TEMP_DIR}/${FW_MODEL}/${RUN_NAME}/outputs-raw/out_${task_id}"
    