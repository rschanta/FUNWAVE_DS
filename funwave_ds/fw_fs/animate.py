# Add to system path
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import funwave_ds.fw_py as fpy
import funwave_ds.fw_ba as fwb
from .animate_backgrounds import *

def animate_1D_eta(vars):
    animate_1D_Var(vars,'eta')
    return {}

def animate_1D_undertow(vars):
    animate_1D_Var(vars,'U_undertow')
    return {}

def animate_1D_roller(vars):
    animate_1D_Var(vars,'roller')
    return {}