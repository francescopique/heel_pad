import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import utils
from decimal import Decimal
from scipy import integrate

# This data is from Kinoshita 1993, exported from
# graphs using online digitizer
# displacement.csv: time [ms], displacement [mm]. 
# Is derived by the authors by integrating the acceleration
# signal that follows
# deceleration.csv: time [ms], deceleration [G]. 
# Signal from accelerometer plced on pendulum impacting the heelpad

x_data = np.genfromtxt('data/displacement.csv', delimiter='\t')  # ms , mm
decel_data = np.genfromtxt('data/deceleration.csv', delimiter='\t')  # ms , G

plt.rcParams['text.usetex'] = True
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'DejaVu Sans'


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.sans-serif'] = 'Times'
#plt.rcParams['font.size'] = 14

# Converting to SI units
x_data[:, 0] = x_data[:, 0] / 1000  # s
x_data[:,1] = x_data[:, 1] / 1000  # m
decel_data[:, 0] = decel_data[:, 0] / 1000  # s
decel_data[:, 1] = decel_data[:, 1] * 9.81  # m/s^2

# Interpolate data to get evenly spaced samples
# We impose a 40 ms time window
N = 400
t = np.linspace(0, 0.04, N)
x = np.interp(t, x_data[:, 0], x_data[:, 1])
xddot = np.interp(t, decel_data[:,0], decel_data[:, 1])

# For these data the initial impact veloicty is given in the paper as 0.93 m/s
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
ax3.set_ylabel('Deformation rate\n [m/s]',fontsize=fsize)
ax3.set_xlabel('Time [s]',fontsize=fsize)
ax3.tick_params(axis='both', labelsize=8)

# Experimental data
# ax1.plot(x_data[:, 0], x_data[:, 1], 'ro', label='Experimental')
# ax2.plot(decel_data[:, 0], decel_data[:, 1], 'ro', label='Experimental')

#grid on
ax1.grid()
ax2.grid()
ax3.grid()
fig.set_figwidth(3.5)
fig.set_figheight(3.)
fig.tight_layout()
# fig.set_facecolor('#DDEAF7')

# plt.show()
# fig.savefig('fig/data.png', format='png', dpi=600)








plt.rcParams['font.size'] = 9
fig, (ax1, ax2) = plt.subplots(2,1)
# Subplot 1
# Get default model results
E = 5e6
c = 2
fN = utils.get_fn_falisse_smooth([E, c], x, xdot)

# Plot default vs. ground truth
ax1.plot(x, fN_truth, label = 'Kinoshita (1993), experimental', color = 'black')
ax1.set_ylabel('Force [N]')
ax1.set_xlabel('Deformation [m]')
ax1.set_title('a)')
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

# rmse
rmse = np.mean(res.fun**2)
rmse = np.sqrt(rmse)



print('RMSE: ', rmse)
print('RMSE %(peak force): ', rmse/ max(fN_truth))

fN = utils.get_fn_falisse_smooth([res.x[0],res.x[1]],x,xdot)


Edec = Decimal(int(res.x[0]))
Esci =  '{:.2E}'.format(Edec) 

ax1.plot(x, fN, '-.',
        label = 'Best fit E = %.2f MPa, c = %.2f s/m ' % (res.x[0]/1000000, res.x[1]),
        # label = 'Best fit E =' + Esci + ' Pa, c = %.2f s/m' % res.x[1],

        color = 'red',linestyle='-.')
# Plot what would be the default loop
fN_def = utils.get_fn_falisse_smooth([E,c],x,xdot)
ax1.plot(x, fN_def, label = 'Default E = 1 MPa, c = 2 s/m',
        color = 'b',linestyle='--')
ax1.grid()
ax1.legend()

#SUBPLOT 2
ax2.plot(x, fN_truth, label = 'Kinoshita (1993), experimental', color = 'black')
ax2.set_xlabel('Deformation [m]')
ax2.set_ylabel('Force [N]')
ax2.grid()
ax2.set_title('b)')

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

# rmse
rmse = np.mean(res.fun**2)
rmse = np.sqrt(rmse)



print('RMSE: ', rmse)
print('RMSE %(peak force): ', rmse/ max(fN_truth))

print('E = %f, c = %f' % (res.x[0], res.x[1]))
fN = utils.get_fn_custom_smooth([res.x[0], res.x[1]], x, xdot)

Edec = Decimal(int(res.x[0]))
Esci =  '{:.2E}'.format(Edec) 
ax2.plot(x, fN, '-.',
        label = 'Best fit K = %.2f $\mathrm{GPa m^{-3/2}}$, c = %.2f s/m' % (res.x[0]/(1e9),res.x[1]),
        # label = 'Best fit E =' + Esci + ' Pa, c = %.2f s/m' % res.x[1],

        color = 'red', linestyle='-.')
ax2.legend(loc='upper left')

fig.set_figwidth(3.58)
fig.set_figheight(6.)
fig.tight_layout()
# fig.set_facecolor('#DDEAF7')

plt.savefig('fig/fits.png',dpi=600)
plt.show()
