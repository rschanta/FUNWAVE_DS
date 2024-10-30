
## FUNWAVE_DS Modules
import funwave_ds.fw_tf as ftf
import funwave_ds.fw_fs as fs
import model_code3 as mod         # Model specific code


# Define internal postprocessing functions
function_set = [fs.animate_1D_eta,
                mod.compare_D3]

# Load in data, post-process, and serialize
serialized_features = ftf.postprocess(function_set)