#!/bin/bash -l
#
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=Trial4
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/logs/run/run6_out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/logs/run/err6__out%a.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-1260
#UD_QUIET_JOB_SETUP=YES
#UD_USE_SRUN_LAUNCHER=YES
#UD_DISABLE_CPU_AFFINITY=YES
#UD_MPI_RANK_DISTRIB_BY=CORE
#UD_DISABLE_IB_INTERFACES=YES
#UD_SHOW_MPI_DEBUGGING=YES
. /opt/shared/slurm/templates/libexec/openmpi.sh
## Construct name of file
    input_dir="/lustre/scratch/rschanta/FSPY4/inputs/"
    task_id=$(printf "%05d" $SLURM_ARRAY_TASK_ID)
    input_file="${input_dir}input_${task_id}.txt"
## Run FUNWAVE
    ${UD_MPIRUN} "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG" "$input_file"

## COMPRESS
conda activate tf_env
python "/work/thsu/rschanta/RTS-PY/mains/condense_outputs.py" "/lustre/scratch/rschanta" "FSPY4" $SLURM_ARRAY_TASK_ID

