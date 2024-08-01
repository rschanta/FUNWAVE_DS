# Import all submodules here
import importlib
from .condense import *
from .save_tensors import *
from .utils import *
from .serialize import *
from .serialize_type import *
from .serialize_type import *
from .save_tf_record import *
from .feature_descriptions import *
from .parsing import *
__all__ = ['condense', 'save_tensors', 'utils', 'serialize', 'serialize_type', 'feature_descriptions', 'parsing']



# List of modules and submodules to import from
modules_to_import = [
    'condense',
    'save_tensors',
    'utils',
    'serialize',
    'serialize_type',
    'save_tf_record',
    'feature_descriptions',
    'parsing'
]

# Initialize the prefix namespace
pre = type('', (), {})()

# Import all functions dynamically
for module_name in modules_to_import:
    module = importlib.import_module(f'.{module_name}', package=__package__)
    for func_name in dir(module):
        if callable(getattr(module, func_name)):
            setattr(pre, func_name, getattr(module, func_name))

# Optional: Define __all__ to control what gets imported when using from package import *
__all__ = list(set(dir(pre)) - {'__dict__', '__doc__', '__module__', '__weakref__'})
