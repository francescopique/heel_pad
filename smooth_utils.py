import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos, tanh

def get_myhertz_smooth(X,x):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """
    

    E = X[0]
    R = 0.03
    bd = X[1]
    cf = 1e-5
    k = 1/2 * E**(2./3.)
    #fHz = (4/3)*k*sqrt(R*k)*x**(3)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] +cf)**(3/2))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

    return fHz_smooth

def get_hertz_smooth(X,x):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """
    

    E = X[0]
    R = 0.03
    bd = X[1]
    cf = X[2]
    k = 1/2 * E**(2./3.)
    #fHz = (4/3)*k*sqrt(R*k)*x**(3)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] + cf )**(3/2))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

    return fHz_smooth


def get_hertz(X,x):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """

    E = X[0]
    R = 0.03
    cf =X[1]

    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i]+cf)**(3/2))

    # fHz = np.zeros(len(x))
    # for i in range(len(x)):
    #     if x[i] < 0:
    #         fHz[i] = 0
    #     else:
    #         fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i]+cf)**(3/2))

    
    return fHz