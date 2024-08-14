import os

# Access the RUN_NAME environment variable
run_name = os.getenv('RUN_NAME')

# Use the environment variable
if run_name:
    print(f"Running with RUN_NAME: {run_name}")
else:
    print("RUN_NAME environment variable is not set.")