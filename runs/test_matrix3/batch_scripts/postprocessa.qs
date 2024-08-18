#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#SBATCH --array=1-40
#SBATCH --job-name=postprocessa
#SBATCH --dependency=28263616
#SBATCH --output=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/postprocessa/out/out%a.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/runs/test_matrix3/logs/postprocessa/err/err%a.out
#

    conda activate tf_env
    python /work/thsu/rschanta/RTS-PY/runs/test_matrix3/model_pipelines/p03a_postprocess.py /lustre/scratch/rschanta test_matrix3  $SLURM_ARRAY_TASK_ID
    