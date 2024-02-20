import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos



def get_fn_standard(X,x,xdot):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """

    E = X[0]
    c = X[1]
    p = X[2]
    R = 0.032

    fHz = (4/3)*sqrt(R)*E*x**(p)
    fHc = 1.5*fHz*c*xdot

    fdiss = np.zeros(len(fHc))
    for i in range(len(fHc)):
        fdiss[i] = max(fHc[i],-fHz[i])

    fN = fHz + fdiss

    return fN

def get_fn_indent_half(X,x,x_peak,f):
    """
    function to get the hunt crossley normal force, for half sinusoidal identation experiments
    Includes the computation of the velocity:

    Knowing that the indentator imposes a sinusoidal deformation:
    x = [1-cos(2*pi*f*t)]*xp/2 we can get the velocity:

    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    f = frequency of the sinusoidal deformation

    """
    # x = np.linspace(0, x_peak, 100) 
    R = 0.032
    E = X[0]
    c = X[1]
    t = 1-2*x/x_peak

    for i in range(len(t)):
        t[i] = acos(t[i])/(2*pi*f)

    xdot = 2*pi*f*t
    for i in range(len(xdot)):
        xdot[i] = f*x_peak*pi*sin(2*pi*f*t[i])
    
    fHz = (4/3)*sqrt(R)*E*x**(1.5)
    fHc = 1.5*fHz*c*xdot

    fN_load = fHz + fHc
    return fN_load

def get_fn_indent_full(X,x_load,x_unload,x_peak,f):
    """
    function to get the hunt crossley normal force, for full sinusoidal identation experiments
    Includes the computation of the velocity:

    Knowing that the indentator imposes a sinusoidal deformation:
    x = [1-cos(2*pi*f*t)]*xp/2 we can get the velocity:

    X = [E,c] parameters to be optimized
    x_load = indentation or deformation over time until load
    x_unload = indentation or deformation over time after load until end
    f = frequency of the sinusoidal deformation

    """
    fN_load = get_fn_indent_half(X,x_load,x_peak,f)
    
    R = 0.032
    E = X[0]
    c = X[1]
    x = x_unload
    t = 1-2*(x)/(x_peak)

    for i in range(len(t)):
        t[i] = acos(t[i])/(2*pi*f)
    
    t = -t

    xdot = 2*pi*f*t

    for i in range(len(xdot)):
        xdot[i] = f*x_peak*pi*sin(2*pi*f*t[i])

    fHz = (4/3)*sqrt(R)*E*x**(1.5)
    fHc = 1.5*fHz*c*xdot

    fN_unload = fHz + fHc

    fN = np.append(fN_load,fN_unload)

    return fN
