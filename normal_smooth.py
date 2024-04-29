import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, tanh
from smooth_utils import get_hertz_smooth, get_hertz


# here we show how bv influences the hertz force

x = np.linspace(-0.01,0.01,100)
E = 1e7
cf = 1e-5
bd = 300


# compute and plot the tanh smoother
y_plot = np.zeros(len(x))
for i in range(len(x)):
    y_plot[i] = 0.5 +0.5*(tanh(300*(x[i]-0.005))) # translation
fig, ax = plt.subplots()
ax.plot(x,y_plot)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('tanh smoother function')
ax.grid(True)


# hertz force without if statement
# but with cf !
fHz = get_hertz([E,cf],x)
# compute and plot the smoothed force
yres = y_plot * fHz
fig, ax = plt.subplots()
ax.plot(x,yres,label='translated')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [N]')
ax.grid(True)

#find defaoult version of hertz force
fHz = get_hertz_smooth([E,300,1e-5],x)
ax.plot(x,fHz,label='bd = 300 (default)')


# normal herz force, withuot smoothing AND without cf!
R = 0.03
k = 1/2 * E**(2./3.)
f = (4/3)*k*sqrt(R*k)*(x)**(3/2)
for i in range(len(f)):
    if x[i] < 0:
        f[i] = 0
ax.plot(x,f,label='Ideal Hertz',color='k')
ax.set_title('Normal E=1e7 ')

# try a harder tanh smoother
# compute and plot the tanh smoother
# y_plot = np.zeros(len(x))
# for i in range(len(x)):
#     y_plot[i] = 0.5 +0.5*(tanh(600*(x[i]-0.002))) # harder
# fHz = get_hertz([E,cf],x)
# # compute and plot the smoothed force
# yres = y_plot * fHz
# ax.plot(x,yres,label='600')


# # load fN_truth.csv
# data = np.genfromtxt('fN_truth.csv', delimiter=',')
# x = data[:,0]
# fN_truth = data[:,1]
# # plot
# ax.plot(x,fN_truth, label = 'Experimental',color = 'black')
# ax.legend()

plt.show()

#save
#fig.savefig('smooth.png',dpi=300)
