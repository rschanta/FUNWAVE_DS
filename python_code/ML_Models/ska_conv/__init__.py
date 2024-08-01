# Give access to the packages indicated
import importlib
from .create_model import *
from .parse import *
from .preprocessing import *
from .utils import *
__all__ = ['create_model', 'parse','preprocessing', 'utils']


modules_to_import = [
    'create_model',
    'parse',
    'preprocessing',
    'utils'
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
