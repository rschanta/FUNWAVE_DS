# Import submodules
import importlib
from .ML_cutting import *
from .ML_parse import *
from .ML_model import *
__all__ = ['ML_cutting', 'ML_parse','ML_model']



# List of modules and submodules to import from
modules_to_import = [
    'ML_cutting','ML_parse', 'ML_model'
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
