#!/bin/bash -l
#
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32
#SBATCH --job-name=CorrectTime
#SBATCH --partition=standard
#SBATCH --time=7-00:00:00
#SBATCH --output=/work/thsu/rschanta/RTS-PY/logs/gen/corr_out.out
#SBATCH --error=/work/thsu/rschanta/RTS-PY/logs/gen/corre_out.out
#SBATCH --mail-user=rschanta@udel.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --export=ALL
#
#UD_QUIET_JOB_SETUP=YES
#UD_USE_SRUN_LAUNCHER=YES
#UD_DISABLE_CPU_AFFINITY=YES
#UD_MPI_RANK_DISTRIB_BY=CORE
#UD_DISABLE_IB_INTERFACES=YES
#UD_SHOW_MPI_DEBUGGING=YES



# Define the directory containing the files
DIRECTORY="/lustre/scratch/rschanta/FSPY4/inputs"

# Define the old and new text
OLD_TEXT="TOTAL_TIME = 400"
NEW_TEXT="TOTAL_TIME = 400.0"

# Loop through each file in the directory
for file in "$DIRECTORY"/*; do
  # Check if it's a file (not a directory)
  if [ -f "$file" ]; then
    echo "Processing $file"
    # Use sed to replace the old text with the new text
    sed -i "s/$OLD_TEXT/$NEW_TEXT/" "$file"
  fi
done

echo "Replacement completed."