#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=run
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/run/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/run/err/err%a.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-40
#SBATCH --dependency=afterany:28255375
#

. /opt/shared/slurm/templates/libexec/openmpi.sh
## Construct name of file
    input_dir="/lustre/scratch/rschanta/test_matrix3/inputs/"
    task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
    input_file="${input_dir}input_${task_id}.txt"
## Run FUNWAVE
    ${UD_MPIRUN} /work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG "$input_file"

## COMPRESS
conda activate tf_env
python /work/thsu/rschanta/RTS-PY/runs/test_matrix3/model_pipeline/p02_condense.py /lustre/scratch/rschanta test_matrix3  $SLURM_ARRAY_TASK_ID
