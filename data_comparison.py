import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import utils
# show the stress deformation loops of the three data sets we have

#kinoshita
# This data is from Kinoshita 1993, exported from graphs using onlline digitizer
# displacement.csv: time [ms], displacement [mm]. Is derived by the authors by integrating the acceleration signal that follows
# deceleration.csv: time [ms], deceleration [G]. Signal from accelerometer plced on pendulum impacting the heelpad

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Computer Modern Roman'
plt.rcParams['font.size'] = 14


x_data = np.genfromtxt('displacement.csv',delimiter='\t')   # ms , mm
decel_data = np.genfromtxt('deceleration.csv',delimiter='\t') # ms , G
# convert to SI units
x_data[:,0] = x_data[:,0] / 1000 # s
x_data[:,1] = x_data[:,1] / 1000 # m
decel_data[:,0] = decel_data[:,0] / 1000 # s
decel_data[:,1] = decel_data[:,1] * 9.81 # m/s^2


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
fN_kino = mass*xddot

# Aertz in vivo
# data by hand from aertz
# load np array from csv
data_path = 'barefoot_load.csv'
data_load = np.genfromtxt(data_path,delimiter='\t')
data_path = 'barefoot_unload.csv'
data_unload = np.genfromtxt(data_path,delimiter='\t')
# convert to SI
data_load[:,0] = data_load[:,0]/1000 # mm to m
data_unload[:,0] = data_unload[:,0]/1000 # mm to m
data = np.append(data_load,data_unload,axis=0) 

#plot
plt.plot(data[:,0], data[:,1],label='In vivo (Aerts 1993), vi = 0.96 m/s',color='black')
plt.plot(x,fN_kino,label ='In vivo (Kinoshita 1993),vi = 0.93 m/s ',color='red')
plt.xlabel('x [m]')
plt.ylabel('Normal force [N]')


# try ackermann 2010
a = 5e7
b = 1
fN = utils.get_fn_ackermann([a,b],x,xdot)
plt.plot(x,fN,label='Ackermann 2010 a=5e7,b=1',color='green')


# try miller 2015
a = 6e5
b = 1
fN = utils.get_fn_miller([a,b],x,xdot)
plt.plot(x,fN,label='Miller 2015 a=6e5,b=1',color='purple')


# lin and pandy 2017
a = 1e6
b = 1.5
fN = utils.get_fn_miller([a,b],x,xdot)
plt.plot(x,fN,label='Lin and Pandy 2017 a=1e6,b=1.5',color='blue')

plt.legend()
plt.savefig('data_comparison.png',dpi=600)
plt.show()