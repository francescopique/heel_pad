import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos, tanh


def get_hertz_smooth(X,x):
    """
    function to get the hertz force
    with smoothing parameters passed
    E = X[0]
    bd = X[1]
    cf = X[2]
    R = 0.03

    """
    
    E = X[0]
    R = 0.03
    bd = X[1]
    cf = X[2]
    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] + cf )**(3/2))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

    return fHz_smooth


def get_hertz_smooth_custom(X,x):
    """
    function to get the hertz force
    with smoothing parameters passed
    E = X[0]
    bd = X[1]
    cf = X[2]
    R = 0.03

    """
    
    E = X[0]
    R = 0.03
    bd = X[1]
    cf = X[2]
    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] + cf )**(3))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

    return fHz_smooth

def get_hertz(X,x):
    

    E = X[0]
    R = 0.03
    cf =X[1]

    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i]+cf)**(3/2))

    return fHz



def get_hertz_custom(X,x):
    

    E = X[0]
    R = 0.03
    cf =X[1]

    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i]+cf)**(3))

    return fHz