#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-8910
#SBATCH --job-name=run_files
#SBATCH --dependency=28267110
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/dep_flat_reg/logs/matrix_1/run_files/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/dep_flat_reg/logs/matrix_1/run_files/err/err%a.out
#

    . /opt/shared/slurm/templates/libexec/openmpi.sh
    ## Construct name of file
        input_dir="/lustre/scratch/rschanta/dep_flat_reg/inputs/"
        task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
        input_file="${input_dir}input_${task_id}.txt"
    ## Run FUNWAVE
        ${UD_MPIRUN} /work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG "$input_file"

    ## COMPRESS
    conda activate tf_env
    python "RTS-PY/runs/dep_flat_reg/model_pipelines/matrix_1/p02_run_condense.py" /lustre/scratch/rschanta dep_flat_reg $SLURM_ARRAY_TASK_ID

    ## Remove Raw Folder
    rm -rf "/lustre/scratch/rschanta/dep_flat_reg/outputs-raw/out_${task_id}"
    