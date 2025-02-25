import funwave_ds as fwd
import os

base = r'/work/thsu/rschanta/RTS-PY/'
dbase = r'/work/thsu/rschanta/data'
lustre = r'/lustre/scratch/rschanta/'

d = {
     'WORK_DIR': os.path.join(base,'DUNE3'),
     'DATA_DIR': os.path.join(dbase,'DUNE3'),
     'TEMP_DIR': os.path.join(lustre,'DUNE3'),
     'FW_MODEL': 'Validation',
     'RUN_NAME': 'Try1',
     'FW_EX': "/work/thsu/rschanta/RTS-PY/funwave/FW_ds/executables/FW-STANDARD",
     'CONDA_ENV': "tf_env"}


fwd.setup_model_run(**d)