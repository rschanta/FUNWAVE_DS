import numpy as np
from scipy.optimize import fsolve


def dispersion(T, h):
    sigma = 2 * np.pi / T
    g = 9.81

    # Define the function for fsolve
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)

    # Find the root of the equation numerically
    k = fsolve(disp_relation, 0)[0]
    L = 2 * np.pi / k

    return k, L