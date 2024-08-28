import os

# Define the base folder name
FW_MODEL = "Test4"  # Replace with your desired folder name

# Define the subfolders to create
subfolders = ["design_matrices", "logs", "batch_scripts", "model_code", "model_pipelines"]

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the base folder in the script's directory
base_dir = os.path.join(script_dir, FW_MODEL)
os.makedirs(base_dir, exist_ok=True)

# Create each subfolder within the base folder
for folder in subfolders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

print(f"Created {FW_MODEL} folder with subdirectories: {', '.join(subfolders)}")
