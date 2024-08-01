# This __init__ file is meant for this package, which in general will
# be aliased as "fw"

# Specify the Core Packages
from .core_packages import tf
from .core_packages import py

# This is such that I can specify fw.ml
from . import ML_Models as ml

# This is such that I can specify 
from . import model_runs as mr

# This is such that I can specify 
from . import post_processing as pp

__all__ = ['tf', 'py','ml','mr','pp']