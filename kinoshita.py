import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from utils import get_fn_falisse_smooth_3parms
from scipy import integrate

# import experimental data from csv
# This data is from Kinoshita 1993, exported from graphs using onlline digitizer
# displacement.csv: time [ms], displacement [mm]. Is derived by the authors by integrating the acceleration signal that follows
# deceleration.csv: time [ms], deceleration [G]. Signal from accelerometer plced on pendulum impacting the heelpad

x_data = np.genfromtxt('displacement.csv',delimiter='\t')   # ms , mm
decel_data = np.genfromtxt('deceleration.csv',delimiter='\t') # ms , G

plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'serif'
# convert to SI units
x_data[:,0] = x_data[:,0] / 1000 # s
x_data[:,1] = x_data[:,1] / 1000 # m
decel_data[:,0] = decel_data[:,0] / 1000 # s
decel_data[:,1] = decel_data[:,1] * 9.81 # m/s^2

# #plots
# # experimental data
# fig, (ax1, ax2) = plt.subplots(2, 1)
# ax1.plot(x_data[:,0], x_data[:,1], 'k.', label='displacement')
# ax1.set_ylabel('[m]')
# ax2.plot(decel_data[:,0], decel_data[:,1], 'r.',label='deceleration')
# ax2.set_ylabel(' [m/s^2]')
# ax2.set_xlabel('time [s]')
# ax1.set_title('Experimental data')
# fig.legend()

# interpolate data to get evenly spaced samples
N = 100
t = np.linspace(0, 0.04, 400)
x = np.interp(t, x_data[:,0], x_data[:,1])
xddot = np.interp(t, decel_data[:,0], decel_data[:,1])
# integrate xddot to get velocity


# for these data the initial impact veloicty is given in the paper as 0.93 m/s
# To do : check velocity of impact range for walking


# xddot is deceleration, thus the minus sign in the integration
xdot_init = 0.93
xdot = integrate.cumulative_trapezoid(-xddot, t,initial=0) + xdot_init

# Normal force from the heel pad is calculated ass the product of pendulum mass (given) and deceleration
mass = 5 
fN_truth = mass*xddot

# fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
# ax1.plot(t,x,'k',label='displacement (interpolated)')
# ax1.set_ylabel('[m]')
# ax2.plot(t,xddot,'r',label='deceleration (interpolated)')
# ax2.set_ylabel('[m/s^2]')
# ax3.plot(t,xdot,'b',label='velocity (computed)')
# ax3.set_ylabel('[m/s]')
# ax3.set_xlabel('time [s]')
# ax1.set_title('Derived data')
# fig.legend()
# #grid on
# ax1.grid()
# ax2.grid()
# ax3.grid()


#incognite
E = 1e6
c = 2
R = 0.032
p = 1.5 # initial guess for exponent of x(deformation)
fig, ax = plt.subplots()

fN = get_fn_falisse_smooth_3parms([E,c,p],x,xdot)
ax.plot(x,fN_truth, label = 'Experimental',color = 'black')
ax.plot(x, fN, label='E = 1 MPa, c = 2, p = 1.5', linestyle='--',color='blue')
ax.set_xlabel('deformation [m]')
ax.set_ylabel('Force [N]')
ax.set_title('model predictions vs. ground truth')


## optimize

def residuals(X,x,xdot,fN_truth): 
    fN = get_fn_falisse_smooth_3parms(X,x,xdot)
    return (fN - fN_truth)

x0 = np.array([1e6,2,1.5]) # initial guess
res = least_squares(residuals, x0, args=(x,xdot,fN_truth),bounds=([1e1,0,1], [1e10,1e2,5]))
print(res)

fN = get_fn_falisse_smooth_3parms([res.x[0],res.x[1],res.x[2]],x,xdot)
plt.plot(x,fN, '-.',label = 'Best fit\n E = %f\n c = %f\n p = %f' % (res.x[0],res.x[1],res.x[2]), color = 'red',linestyle='-.')
plt.legend(loc='upper left')
plt.savefig('fit_custom.png',dpi=600)

# fig, ax = plt.subplots()
# ax.plot(t,fN_truth, label = 'Experimental Ground Truth (Kinoshita 1993)',color = 'black')
# ax.plot(t, fN, label='model best fit (E =%f, c = %f, p = %f)'% (res.x[0],res.x[1],res.x[2]), linestyle='-.',color='red')
# ax.set_xlabel('time [s]')
# ax.set_ylabel('Force [N]')
# ax.set_title('model predictions vs. ground truth')
# plt.legend()
plt.show()

