from scipy.optimize import least_squares

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos

def residuals(X,data_load):

    x_peak = 0.0063
    x_init = 0
    f= 1.1
    R = 0.032
    E = X[0]
    c = X[1]
    x = data_load[:,0]/1000
    t = 1-2*(x-x_init)/(x_peak-x_init)

    for i in range(len(t)):
        t[i] = acos(t[i])/(2*pi*f)

    xdot = 2*pi*f*t
    for i in range(len(xdot)):
        xdot[i] = f*x_peak*pi*sin(2*pi*f*t[i])
    
    fHz = (4/3)*sqrt(R)*E*x**(1.5)
    fHc = 1.5*fHz*c*xdot

    fN= fHz + fHc


    return fN - data_load[:,1]

def func(X,data_load):

    x_peak = 0.0063
    x_init = 0
    f= 1.1
    R = 0.032
    E = X[0]
    c = X[1]
    x = data_load[:,0]/1000
    t = 1-2*(x-x_init)/(x_peak-x_init)

    for i in range(len(t)):
        t[i] = acos(t[i])/(2*pi*f)

    xdot = 2*pi*f*t
    for i in range(len(xdot)):
        xdot[i] = f*x_peak*pi*sin(2*pi*f*t[i])
    
    fHz = (4/3)*sqrt(R)*E*x**(1.5)
    fHc = 1.5*fHz*c*xdot

    fN= fHz + fHc
    

    return fN

data_path = 'aertz_asc_vitro.csv'
data = np.genfromtxt(data_path,delimiter='\t')

x0 = np.array([1e6,2])
res = least_squares(residuals, x0, args=(data,),bounds=([1e1,0], [1e10,1e2]))
print(res)

#try optimized function

fN = func(res.x,data)
plt.plot(data[:,0],fN)
plt.plot(data[:,0],data[:,1])
plt.legend(['model E=%d c=%d' %tuple((res.x[0],res.x[1])),'aertz'])


plt.show()
