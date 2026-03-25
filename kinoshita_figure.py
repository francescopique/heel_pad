import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import utils

from scipy import integrate

# This data is from Kinoshita 1993, exported from
# graphs using online digitizer
# displacement.csv: time [ms], displacement [mm]. 
# Is derived by the authors by integrating the acceleration
# signal that follows
# deceleration.csv: time [ms], deceleration [G]. 
# Signal from accelerometer plced on pendulum impacting the heelpad

x_data = np.genfromtxt('displacement.csv', delimiter='\t')  # ms , mm
decel_data = np.genfromtxt('deceleration.csv', delimiter='\t')  # ms , G

#plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'times new roman'
#plt.rcParams['font.size'] = 14

# Converting to SI units
x_data[:, 0] = x_data[:, 0] / 1000  # s
x_data[:,1] = x_data[:, 1] / 1000  # m
decel_data[:, 0] = decel_data[:, 0] / 1000  # s
decel_data[:, 1] = decel_data[:, 1] * 9.81  # m/s^2

# Interpolate data to get evenly spaced samples
# We impose a 40 ms time window
N = 100
t = np.linspace(0, 0.04, 400)
x = np.interp(t, x_data[:, 0], x_data[:, 1])
xddot = np.interp(t, decel_data[:,0], decel_data[:, 1])

# For these data the initial impact veloicty is given in the paper as 0.93 m/s
# To do : check velocity of impact range for walking.
# Integrate xddot to get velocity
# xddot is deceleration, thus the minus sign in the integration
xdot_init = 0.93
xdot = integrate.cumulative_trapezoid(-xddot, t, initial=0) + xdot_init

# Normal force from the heel pad is calculated as the product
# of pendulum mass (5 kg) and deceleration
mass = 5 
fN_truth = mass*xddot

fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fsize = 8

ax1.plot(t,x,'k',label='x')
ax1.set_ylabel('Deformation\n [m]',fontsize=fsize)
ax1.tick_params(axis='both', labelsize=8)
ax2.plot(t,xddot,'k')
ax2.set_ylabel('Deceleration\n [m/$\mathdefault{s^2}$]',fontsize=fsize)
ax2.tick_params(axis='both', labelsize=8)
ax3.plot(t,xdot,'k',label='$\mathrm{\dot{x}}$')
ax3.set_ylabel('Velocity\n [m/s]',fontsize=fsize)
ax3.set_xlabel('Time [s]',fontsize=fsize)
ax3.tick_params(axis='both', labelsize=8)

# Experimental data
ax1.plot(x_data[:, 0], x_data[:, 1], 'ro', label='Experimental')
ax2.plot(decel_data[:, 0], decel_data[:, 1], 'ro', label='Experimental')

#grid on
ax1.grid()
ax2.grid()
ax3.grid()
fig.set_figwidth(3.5)
fig.set_figheight(3.)
fig.tight_layout()
plt.show()
fig.savefig('fig/data.png', format='png', dpi=600)

fig, (ax1, ax2, ax3) = plt.subplots(1,3)
# Subplot 1
# Get default model results
E = 5e6
c = 2
fN = utils.get_fn_falisse_smooth([E, c], x, xdot)

# Plot default vs. ground truth
ax1.plot(x, fN_truth, label = 'Experimental', color = 'black')
ax1.set_xlabel('\na)')
ax1.set_ylabel('Force [N]')

# Function to optimize 
def residuals(X, x, xdot, fN_truth): 
    fN = utils.get_fn_falisse_smooth(X, x, xdot)
    return (fN - fN_truth)

# Initial guess
x0 = np.array([1e5,5])
# Bounds
E_lower = 1e1
E_upper = 1e11
c_lower = 0
c_upper = 1e2
bounds=([E_lower, c_lower], [E_upper, c_upper])
res = least_squares(residuals, x0, args=(x, xdot, fN_truth), bounds=bounds)
print(res)
print('E = %f, c = %f' % (res.x[0], res.x[1]))
fN = utils.get_fn_falisse_smooth([res.x[0],res.x[1]],x,xdot)
ax1.plot(x, fN, '-.',
        label = 'Best fit E = %d, c = %f' % (int(res.x[0]),res.x[1]),
        color = 'red',linestyle='-.')
# Plot what would be the default loop
fN_def = utils.get_fn_falisse_smooth([E,c],x,xdot)
ax1.plot(x, fN_def, label = 'Best fit E = 1 MPa, c = 2',
        color = 'b',linestyle='--')
ax1.grid()

#SUBPLOT 2
ax2.plot(x, fN_truth, label = 'Experimental', color = 'black')
ax2.set_xlabel('Deformation [m]\nb)')
ax2.grid()

# Function to optimize
def residuals(X, x, xdot, fN_truth): 
    fN = utils.get_fn_custom_smooth(X, x, xdot)
    return (fN - fN_truth)

# Initial guess
x0 = np.array([1e5, 5])
#Bounds
E_lower = 1e1
E_upper = 1e11
c_lower = 0
c_upper = 1e2
bounds=([E_lower, c_lower], [E_upper, c_upper])
res = least_squares(residuals, x0, args=(x, xdot, fN_truth), bounds=bounds)
print(res)
print('E = %f, c = %f' % (res.x[0], res.x[1]))
fN = utils.get_fn_custom_smooth([res.x[0], res.x[1]], x, xdot)
ax2.plot(x, fN, '-.',
        label = 'Best fit E = %d, c = %f' % (int(res.x[0]), res.x[1]),
        color = 'red', linestyle='-.')

#SUBPLOT 3

ax3.plot(x,fN_truth, label = 'Experimental',color = 'black')
ax3.set_xlabel('\nc)')
ax3.grid() 

## function to optimize
def residuals(X,x,xdot,fN_truth): 
    fN = utils.get_fn_custom_newsmooth(X,x,xdot)
    return (fN - fN_truth)

# Initial guess
x0 = np.array([1e5,5])
# bounds
E_lower = 1e1
E_upper = 1e11
c_lower = 0
c_upper = 1e2
bounds=([E_lower, c_lower], [E_upper, c_upper])
res = least_squares(residuals, x0, args=(x, xdot, fN_truth), bounds=bounds)
print(res)
print('E = %f, c = %f' % (res.x[0], res.x[1]))
fN = utils.get_fn_custom_newsmooth([res.x[0], res.x[1]], x, xdot)
ax3.plot(x, fN, '-.',
        label = 'Best fit E = %d, c = %f' % (int(res.x[0]), res.x[1]),
        color = 'red', linestyle='-.')

fig.set_figwidth(7.16)
fig.set_figheight(3.)
fig.tight_layout()
plt.savefig('fig/fits.png',dpi=600)
plt.show()
