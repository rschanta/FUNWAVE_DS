#!/bin/bash -l
#
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=Parse
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/logs/parse/parse6_out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/logs/parse/parse6_err%a.out
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

## COMPRESS
conda activate tf_env
python "/work/thsu/rschanta/RTS-PY/mains/m03_postprocess_03.py" "/lustre/scratch/rschanta" "FSPY4" $SLURM_ARRAY_TASK_ID

