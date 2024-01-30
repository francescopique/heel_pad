import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos

#import csv
x_data = np.genfromtxt('displacement.csv',delimiter='\t')   # ms , mm
decel_data = np.genfromtxt('deceleration.csv',delimiter='\t') # ms , G

# convert to SI units
x_data[:,0] = x_data[:,0] / 1000 # s
x_data[:,1] = x_data[:,1] / 1000 # m
decel_data[:,0] = decel_data[:,0] / 1000 # s
decel_data[:,1] = decel_data[:,1] * 9.81 # m/s^2

#plot
#sub plots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
ax1.plot(x_data[:,0], x_data[:,1], 'k.', label='displacement')
ax2.plot(decel_data[:,0], decel_data[:,1], 'r.',label='deceleration')

t = np.linspace(0, 0.04, 1000)
x = np.interp(t, x_data[:,0], x_data[:,1])
xddot = np.interp(t, decel_data[:,0], decel_data[:,1])
xdot = np.gradient(x,t)
mass = 5 * 9.81

print(xddot.shape)

fN_truth = mass*xddot
ax1.plot(t, x, 'k', label='fit')
ax2.plot(t, xddot, 'r',label='fit')
ax3.plot(t, xdot, 'b',label='velocity')
ax4.plot(x,fN_truth, label = 'normal force')
fig.legend()



#incognite
E = 1e6
c = 2
R = 0.032

fHz = (4/3)*sqrt(R)*E*x**(1.5)
fHc = 1.5*fHz*c*xdot

fdiss = np.zeros(len(fHc))
for i in range(len(fHc)):
    fdiss[i] = max(fHc[i],-fHz[i]) 

fN = fHz + fdiss

ax4.plot(x, fN, label='HC model')
plt.show()



