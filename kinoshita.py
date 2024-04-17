import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from utils import get_fn_standard, get_fn_falisse, get_fn_falisse_smooth
from scipy import integrate

# import experimental data from csv
# This data is from Kinoshita 1993, exported from graphs using onlline digitizer
# displacement.csv: time [ms], displacement [mm]. Is derived by the authors by integrating the acceleration signal that follows
# deceleration.csv: time [ms], deceleration [G]. Signal from accelerometer plced on pendulum impacting the heelpad

x_data = np.genfromtxt('displacement.csv',delimiter='\t')   # ms , mm
decel_data = np.genfromtxt('deceleration.csv',delimiter='\t') # ms , G

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Computer Modern Roman'
plt.rcParams['font.size'] = 14


# convert to SI units
x_data[:,0] = x_data[:,0] / 1000 # s
x_data[:,1] = x_data[:,1] / 1000 # m
decel_data[:,0] = decel_data[:,0] / 1000 # s
decel_data[:,1] = decel_data[:,1] * 9.81 # m/s^2

#plots
# experimental data
# fig, (ax1, ax2) = plt.subplots(2, 1)
# ax1.plot(x_data[:,0], x_data[:,1], 'k.', label='displacement')
# ax1.set_ylabel('[m]')
# ax2.plot(decel_data[:,0], decel_data[:,1], 'r.',label='deceleration')
# ax2.set_ylabel(' $\mathrm{[m/s^2]$}')
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

fig, (ax1, ax2, ax3) = plt.subplots(3, 1,layout='constrained')
ax1.plot(t,x,'k',label='x')
ax1.set_ylabel('[m]')
ax2.plot(t,xddot,'r',label='$\mathrm{\ddot{x}}$')
ax2.set_ylabel('$\mathrm{[m/s^2]}$')
ax3.plot(t,xdot,'b',label='$\mathrm{\dot{x}}$')
ax3.set_ylabel('[m/s]')
ax3.set_xlabel('time [s]')
ax1.set_title('')
# legend
fig.legend(loc='outside lower center',ncol=3)

#grid on
ax1.grid()
ax2.grid()
ax3.grid()
plt.show()

# save images
fig.savefig('fig/data.png', format='png',dpi=600)
# get default model results
E = 1e6
c = 2
R = 0.032
fN = get_fn_falisse_smooth([E,c],x,xdot)

# plot default vs. ground truth
fig, ax = plt.subplots()
ax.plot(x,fN_truth, label = 'Experimental',color = 'black')
ax.plot(x, fN, label='E = 1 MPa, c = 2', linestyle='--',color='blue')
ax.set_xlabel('deformation $[x]$')
ax.set_ylabel('Force $[N]$')
ax.set_title('model predictions vs. ground truth')


## function to optimize
def residuals(X,x,xdot,fN_truth): 
    #fN = get_fn_standard(X,x,xdot)
    fN = get_fn_falisse_smooth(X,x,xdot)
    return (fN - fN_truth)


# least squares problem and plot

# initial guess
x0 = np.array([1e5,5])
# bounds
E_lower = 1e1
E_upper = 1e10
c_lower = 0
c_upper = 1e2
bounds=([E_lower,c_lower], [E_upper,c_upper])

res = least_squares(residuals, x0, args=(x,xdot,fN_truth),bounds=bounds)
print(res)
print('E = %f, c = %f' % (res.x[0],res.x[1]))
fN = get_fn_falisse_smooth([res.x[0],res.x[1]],x,xdot)
plt.plot(x,fN, '-.',label = 'Best fit E = %d, c = %f' % (int(res.x[0]),res.x[1]), color = 'red',linestyle='-.')
# # add trials with different c
Etr = 100000
ctr = 2
fN_trial = get_fn_falisse_smooth([Etr,ctr],x,xdot)
plt.plot(x,fN_trial, '-.',label = 'model trial E = %f, c = %f' % (Etr,ctr), color = 'green',linestyle='-.')
plt.legend(loc='upper left',bbox_to_anchor=(0,0.99))
fig.savefig('fig/fit.png', format='png', dpi=600)


# # plot over time
# fig, ax = plt.subplots()
# ax.plot(t,fN_truth, label = 'Experimental',color = 'black')
# ax.plot(t, fN, label='Best fit $(E =%f, c = %f)$'% (res.x[0],res.x[1]), linestyle='-.',color='red')
# ax.set_xlabel('time $[s]$')
# ax.set_ylabel('Force $[N]$')
# ax.set_title('model predictions vs. ground truth')
# plt.legend()
plt.show()

