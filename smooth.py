import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos, tanh
from smooth_utils import get_hertz_smooth, get_hertz

x = np.linspace(-0.01,0.01,100)
E = 1e7
cf = 1e-5
bd = 300


# hert force without if statement
fig, ax = plt.subplots()
fHz = get_hertz([E,cf],x)
ax.plot(x,fHz,'k',label='Hertz')
ax.set_xlabel('Indentation [m]')
ax.set_ylabel('Force [N]')
ax.legend()
#grid on
ax.grid(True)

# plot the tanh
y_plot = np.zeros(len(x))
for i in range(len(x)):
    y_plot[i] = 0.5 +0.5*(tanh(300*(x[i]-0.005)))
fig, ax = plt.subplots()
ax.plot(x,y_plot)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)

# plot the smoothed force
yres = y_plot * fHz
fig, ax = plt.subplots()
ax.plot(x,yres,label='translated')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [N]')
ax.grid(True)

#find previous bversion of hertz force
fHz = get_hertz_smooth([E,300,1e-5],x)
ax.plot(x,fHz,label='bd = 300 (default)')



# normal herz force
R = 0.03
k = 1/2 * E**(2./3.)
f = (4/3)*k*sqrt(R*k)*(x)**(3/2)
for i in range(len(f)):
    if x[i] < 0:
        f[i] = 0
ax.plot(x,f,label='Ideal Hertz',color='k')

ax.set_title('Normal E=1e7 c=2')
ax.legend()
plt.show()

#save
fig.savefig('smooth.png',dpi=300)
# fig, ax = plt.subplots()

# for i in range(10):
#     fHz = get_hertz_smooth([E,300,1e-5*i],x)
#     ax.plot(x,fHz,label='cf = '+str(1e-5*i))
# ax.set_xlabel('Indentation [m]')
# ax.set_ylabel('Force [N]')
# ax.set_title('Hertz vs. Smooth Hertz')
# ax.legend()



# fig, ax = plt.subplots()

# fHz = get_hertz([E],x)
# fHz_500 = get_hertz_smooth([E,500,1e-5],x)
# fHz_300 = get_hertz_smooth([E,300,1e-5],x)
# ax.plot(x,fHz,'k',label='Hertz')
# ax.plot(x,fHz_300,label='Smooth Hertz bd = 300 (default)')
# ax.plot(x,fHz_500,label='Smooth Hertz bd = 500')
# ax.set_xlabel('Indentation [m]')
# ax.set_ylabel('Force [N]')
# ax.set_title('Hertz vs. Smooth Hertz')
# ax.legend()


# fig, ax = plt.subplots()

# for i in (1e-4,5e-4,1e-5,5e-6,1e-6,5e-6):
#     fHz = get_hertz_smooth([E,300,i],x)
#     ax.plot(x,fHz,label='cf = '+str(i))
# ax.set_xlabel('Indentation [m]')
# ax.set_ylabel('Force [N]')
# ax.set_title('Hertz vs. Smooth Hertz')
# ax.legend()
# plt.show()
