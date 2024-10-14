import os

# Directories
WORK_DIR = "/work/thsu/rschanta/RTS-PY"
DATA_DIR =  "/work/thsu/rschanta/DATA"
DEBUG_DATA_DIR = "/work/thsu/rschanta/DATA/DEBUG"
TEMP_DIR = "/lustre/scratch/rschanta"
DEBUG_TEMP_DIR = "/lustre/scratch/rschanta/DEBUG"
FW_MODEL = "DUNE3"
RUN_NAME  = "T01"
FW_EX = "/work/thsu/rschanta/RTS/funwave/v3.6H/exec/FW-REG"
CONDA_ENV = "tf_env"

# Define the subfolders to create
subfolders = ["design_matrices", f"logs/{RUN_NAME}", f"batch_scripts/{RUN_NAME}", "model_code", f"model_pipelines/{RUN_NAME}","envs"]

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the base folder in the script's directory
base_dir = os.path.join(script_dir, FW_MODEL)
os.makedirs(base_dir, exist_ok=True)

# Create each subfolder within the base folder
for folder in subfolders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

print(f"Created {FW_MODEL} folder with subdirectories: {', '.join(subfolders)}")

################################################################
# Create the Environment File(s)
#################################################################
# Path Name
env_file_path = os.path.join(WORK_DIR, 'fw_models', FW_MODEL, 'envs', f'{RUN_NAME}.env')

## Main DotEnv
dotenv_file = f"""WORK_DIR={WORK_DIR}
DATA_DIR={DATA_DIR}
TEMP_DIR={TEMP_DIR}
FW_MODEL={FW_MODEL}
RUN_NAME={RUN_NAME}
ENV_FILE_PATH={env_file_path}
PYTHONPATH={WORK_DIR}:{WORK_DIR}/fw_models/{FW_MODEL}
FW_EX={FW_EX}
CONDA_ENV={CONDA_ENV}
"""
with open(env_file_path, "w") as file:
    file.write(dotenv_file)

## Debugging Environment
# Path Name
env_file_path = os.path.join(WORK_DIR, 'fw_models', FW_MODEL, 'envs', f'{RUN_NAME}_debug.env')

## Main DotEnv
dotenv_file = f"""WORK_DIR={WORK_DIR}
DATA_DIR={DEBUG_DATA_DIR}
TEMP_DIR={DEBUG_TEMP_DIR}
FW_MODEL={FW_MODEL}
RUN_NAME={RUN_NAME}
ENV_FILE_PATH={env_file_path}
PYTHONPATH={WORK_DIR}:{WORK_DIR}/fw_models/{FW_MODEL}
FW_EX={FW_EX}
CONDA_ENV={CONDA_ENV}
"""
with open(env_file_path, "w") as file:
    file.write(dotenv_file)