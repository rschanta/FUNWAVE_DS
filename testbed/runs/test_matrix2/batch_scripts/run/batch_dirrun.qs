#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=Funwave_Job
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=out.out
#SBATCH --error=error.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-500
#SBATCH --dependency=yes
#

. /opt/shared/slurm/templates/libexec/openmpi.sh
## Construct name of file
    input_dir="/lustre/scratch/rschanta/test_matrix/inputs/"
    task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
    input_file="${input_dir}input_${task_id}.txt"
## Run FUNWAVE
    ${UD_MPIRUN} "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG" "$input_file"

## COMPRESS
conda activate tf_env
python "/work/thsu/rschanta/RTS-PY/mains/m02_condense.py" "/lustre/scratch/rschanta" "test_matrix" $SLURM_ARRAY_TASK_ID
