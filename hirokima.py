import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from utils import get_fn_standard
#import csv
x_data = np.genfromtxt('displacement.csv',delimiter='\t')   # ms , mm
decel_data = np.genfromtxt('deceleration.csv',delimiter='\t') # ms , G

plt.rcParams['text.usetex'] = True

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

t = np.linspace(0, 0.04, 100)
x = np.interp(t, x_data[:,0], x_data[:,1])
xddot = np.interp(t, decel_data[:,0], decel_data[:,1])
xdot = np.gradient(x,t)
mass = 5 * 9.81

print(xddot.shape)

fN_truth = mass*xddot
ax1.plot(t, x, 'k', label='fit')
ax2.plot(t, xddot, 'r',label='fit')
ax3.plot(t, xdot, 'b',label='velocity (derived)')
ax4.plot(x,fN_truth, label = 'normal force')
ax1.set_title('Experimental data')
fig.legend()



#incognite
E = 1e6
c = 2
R = 0.032
fig, ax = plt.subplots()

fN = get_fn_standard([E,c],x,xdot)
ax.plot(x,fN_truth, label = 'Experimental Hirokima 1993',color = 'black')
ax.plot(x, fN, label='HC model (E =%f, c = %f)'%(E,c), linestyle='--',color='blue')

# optimize


def residuals(X,x,xdot,fN_truth): 
    fN = get_fn_standard(X,x,xdot)
    return fN - fN_truth

x0 = np.array([1e6,2])
res = least_squares(residuals, x0, args=(x,xdot,fN_truth),bounds=([1e1,0], [1e10,1e2]))
print(res)

fN = get_fn_standard([res.x[0],res.x[1]],x,xdot)
plt.plot(x,fN, '-.',label = 'model best fit E = %f, c = %f' % (res.x[0],res.x[1]), color = 'red',linestyle='-.')
plt.legend()
plt.show()




