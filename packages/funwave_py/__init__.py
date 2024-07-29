# Import submodules

from .directories import *
from .templates import *
from .print_files import *
from .input_processing import *
from .hydro import *
from .spectra import *
from .plots import *

__all__ = ['directories', 'templates', 'print_files','hydro','input_processing','spectra','plots']


import importlib

# List of modules and submodules to import from
modules_to_import = [
    'directories',
    'templates',
    'print_files',
    'hydro',
    'input_processing',
    'spectra',
    'plots'
    
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


