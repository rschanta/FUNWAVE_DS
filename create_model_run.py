import funwave_ds as fwd
import os

base = r'C:\Users\rschanta\OneDrive - University of Delaware - o365\Desktop\Research\FUNWAVE_DS\FUNWAVE_DS'
lbase = r'C:/Users/rschanta/HPC_Pretend/'

d = {
     'WORK_DIR': os.path.join(base,'DUNE3'),
     'DATA_DIR': os.path.join(lbase,'DUNE3_Data'),
     'TEMP_DIR': os.path.join(lbase,'DUNE3_Temp'),
     'FW_MODEL': 'Validation',
     'RUN_NAME': 'Try1',
     'FW_EX': "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
     'CONDA_ENV': "tf_env"}


fwd.setup_model_run(**d)