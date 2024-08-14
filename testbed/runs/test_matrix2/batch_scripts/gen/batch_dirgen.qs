#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=Funwave_Job
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=.\runs\test_matrix2\logs\gen\out.out
#SBATCH --error=.\runs\test_matrix2\logs\gen\err.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#

## Activate conda environment and compress
conda activate tf_env
python /work/thsu/rschanta/RTS-PY/mains/generate_inputs.py "/lustre/scratch/rschanta" "FSPY2" 
