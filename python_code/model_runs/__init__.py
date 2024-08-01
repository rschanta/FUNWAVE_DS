import pkgutil
import importlib

# Automatically import all submodules and subpackages
__all__ = []

# Discover and import subpackages
for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
    if is_pkg:
        # Import subpackage and add it to __all__
        module = importlib.import_module(f'.{module_name}', package=__name__)
        locals()[module_name] = module
        __all__.append(module_name)


