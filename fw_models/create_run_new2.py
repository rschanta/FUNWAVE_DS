import os

################################################################
# INPUT HERE: directories
################################################################
WORK_DIR = r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\tutorials\work_dir'
DATA_DIR =  r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\tutorials\data_dir'
TEMP_DIR = r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS\tutorials\temp_dir'
FW_MODEL = "USACE_Empty_Tank"
RUN_NAME  = "A2"
FW_EX = "/work/thsu/rschanta/RTS-PY/funwave/FW_rts/exec/FW-REG"
CONDA_ENV = "tf_env"

################################################################
# SETUP
################################################################
# Define the subfolders to create
subfolders = ["design_matrices", 
              "logs", 
              "batch_scripts", 
              "model_code", 
              "model_pipelines",
              "envs"]

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the base folder in the script's directory
base_dir = os.path.join(script_dir, FW_MODEL,RUN_NAME)
os.makedirs(base_dir, 
            exist_ok=True)

# Create each subfolder within the base folder
for folder in subfolders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

print(f"Created {FW_MODEL} folder with subdirectories: {', '.join(subfolders)}")


################################################################
# Create the Environment File(s)
################################################################
# Path Name
env_file_path = os.path.join(base_dir, 'envs',f'{RUN_NAME}.env')

## Main DotEnv
dotenv_file = f"""WORK_DIR={WORK_DIR}
DATA_DIR={DATA_DIR}
TEMP_DIR={TEMP_DIR}
FW_MODEL={FW_MODEL}
RUN_NAME={RUN_NAME}
LOG_DIR={WORK_DIR}/fw_models/{FW_MODEL}/{RUN_NAME}/logs
ENV_FILE_PATH={env_file_path}
PYTHONPATH={WORK_DIR}:{WORK_DIR}/{FW_MODEL}/{RUN_NAME}
FW_EX={FW_EX}
CONDA_ENV={CONDA_ENV}
"""
with open(env_file_path, "w") as file:
    file.write(dotenv_file)

