import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos, tanh

def get_fn_miller(X,x,xdot):
    a = X[0]
    b = X[1]

    fN = (a*x**2)*(1+b*xdot)

    return fN


def get_fn_ackermann(X,x,xdot):
    a = X[0]
    b = X[1]

    fN = (a*x**3)*(1+b*xdot)

    return fN

def get_fn_falisse_smooth(X,x,xdot):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """

    E = X[0]
    c = X[1]
    R = 0.02
    bd = 300
    bv = 50
    cf = 1e-5
    k = 1/2 * E**(2./3.)
    #fHz = (4/3)*k*sqrt(R*k)*x**(3)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] +cf)**(3/2))
    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*(x[i])))

    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return fN


def get_fn_custom_smooth(X,x,xdot):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """

    E = X[0]
    c = X[1]
    R = 0.032
    bd = 300
    bv = 50
    cf = 1e-5


    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*E*sqrt(R)*(sqrt(x[i]*x[i] +cf)**(3))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*(x[i])))

    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return fN

def get_fn_falisse_smooth_3parms(X,x,xdot):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    fN = (a*x**2)*(1+b*xdot)
    """
    E = X[0]
    c = X[1]
    p = X[2]
    cf = 1e-5
    R = 0.02
    bd = 300
    bv = 50
    k = 1/2 * E**(2./3.)
    k = 1/2 * E**(2./3.)
    #fHz = (4/3)*k*sqrt(R*k)*x**(3)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] +cf)**(p))
    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*(x[i])))


    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return fN


def get_fn_falisse_smooth_6parms(X,x,xdot):
    """
    function to get the smoothed hertz hunt crossley normal force
    with six optimizable parameters
    E = X[0]
    c = X[1]
    p = X[2]
    bd = X[3]
    bv = X[4]
    cf = X[5]
    """
    E = X[0]
    c = X[1]
    p = X[2]
    R = 0.03
    bd = X[3]
    bv = X[4]
    cf = X[5]
    k = 1/2 * E**(2./3.)
      
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] + cf )**(p))

    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))
        
    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return fN