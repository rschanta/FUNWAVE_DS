import os
import importlib

def import_all_modules(package_dir):
    for filename in os.listdir(package_dir):
        # Check case of .py files
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            importlib.import_module(f'.{module_name}', package=__package__)
            globals()[module_name] = importlib.import_module(f'.{module_name}', package=__package__)
        # Check case of modules
        elif os.path.isdir(os.path.join(package_dir, filename)) and \
             '__init__.py' in os.listdir(os.path.join(package_dir, filename)):
            subpackage_name = filename
            importlib.import_module(f'.{subpackage_name}', package=__package__)
            globals()[subpackage_name] = importlib.import_module(f'.{subpackage_name}', package=__package__)

# Directory of the current package
current_dir = os.path.dirname(__file__)

# Import all modules and submodules
import_all_modules(current_dir)
