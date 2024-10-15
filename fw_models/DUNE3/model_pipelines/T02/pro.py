
## FUNWAVE_DS Modules
import funwave_ds.fw_tf as ftf
import funwave_ds.fw_fs as fwf


# Define internal postprocessing functions
function_set = [fwf.animate_1D_eta]

# Load in data, post-process, and serialize
serialized_features = ftf.postprocess(function_set)