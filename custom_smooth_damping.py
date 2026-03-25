import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, tanh
from smooth_utils import get_hertz_smooth_custom, get_hertz_custom
from opensim_sto_reader import readMotionFile
from smooth_utils import get_hertz_smooth, get_hertz


def get_force(X,x,xdot):
    """
    function to get the hunt crossley normal force, for impact experiments
    
    X = [E,c] parameters to be optimized
    x = indentation or deformation over time
    xdot = deformation velocity over time (must be known)

    """

    E = X[0]
    c = X[1]
    R = X[2]
    cf = 1e-5
    bd = 300
    bv = 50
    k = 1/2 * E**(2./3.)
    fHz = np.zeros(len(x))
    for i in range(len(x)):
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] +cf)**(3./2.))
    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return  (fN, fHz_smooth)


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'times new roman'
plt.rcParams['font.size'] = 10

fig, (ax1,ax2,ax3) =  plt.subplots(1,3)
# here we show how bv influences the hertz force


# here we show how bv influences the hertz force

x = np.linspace(-0.01,0.01,100)
E = 1e7
cf = 1e-5
bd = 300


# compute and plot the tanh smoother
y_plot = np.zeros(len(x))
for i in range(len(x)):
    y_plot[i] = 0.5 +0.5*(tanh(300*(x[i]-0.005))) # translation

# hertz force without if statement
# but with cf !
fHz = get_hertz([E,cf],x)
# compute and plot the smoothed force
yres = y_plot * fHz
ax1.plot(x,yres,label='Custom\nsmoothing')
ax1.set_xlabel('Deformation [m]\na)')
ax1.set_ylabel('Force [N]')
ax1.grid(True)

#find defaoult version of hertz force
fHz = get_hertz_smooth([E,300,1e-5],x)
ax1.plot(x,fHz,label='Default')


# normal herz force, withuot smoothing AND without cf!
R = 0.03
k = 1/2 * E**(2./3.)
f = (4/3)*k*sqrt(R*k)*(x)**(3/2)
for i in range(len(f)):
    if x[i] < 0:
        f[i] = 0
ax1.plot(x,f,label='Ideal Hertz',color='k')

ax1.legend(framealpha=1.0, loc='upper left', fontsize=8)

# CUSTOM
x = np.linspace(-0.01,0.01,100)
E = 6e9
cf = 1e-5
bd = 300


# compute and plot the tanh smoother
y_plot = np.zeros(len(x))
for i in range(len(x)):
    y_plot[i] = 0.5 +0.5*(tanh(300*(x[i]-0.005))) # translation


# hertz force without if statement
# but with cf !
fHz = get_hertz_custom([E,cf],x)
# compute and plot the smoothed force
yres = y_plot * fHz
ax2.plot(x,yres,label='translated')
ax2.set_xlabel('Deformation [m]\nb)')
ax2.grid(True)

#find defaoult version of hertz force
fHz = get_hertz_smooth_custom([E,300,1e-5],x)
ax2.plot(x,fHz,label='bd = 300 (default)')


# normal herz force, withuot smoothing AND without cf!
R = 0.03
k = 1/2 * E**(2./3.)
f = (4/3)*k*sqrt(R*k)*(x)**(3)
for i in range(len(f)):
    if x[i] < 0:
        f[i] = 0
ax2.plot(x,f,label='Custom Hertz',color='k')

# FORCE ON TOP OF DISPLAGEMENT
E = 1e7
c = 2
t = np.linspace(0,100,100)
# load heel sphere center position data
path = '../bilevel_ocp/sphere_analysis/data/E_10Mpa_2c/s1/new_model_scaled_FK_contacts_fra_PointKinematics_s1_pos.sto'
[header, labels, data] = readMotionFile(path)
data = np.array(data)
# get contact point position
R = 0.03
x = data[:,2]-R
xsav = x

# load heel sphere center velocity data
path = '../bilevel_ocp/sphere_analysis/data/E_10Mpa_2c/s1/new_model_scaled_FK_contacts_fra_PointKinematics_s1_vel.sto'
[header, labels, data] = readMotionFile(path)
data = np.array(data)
xdotsav= data[:,2]
# impose positive towards ground
xdot = -data[:,2]
x = -x
# impose zero if no contact. Not needed since falisse uses tanh
# for j in range(0,len(x)):
#     if x[j] < 0:
#         x[j] = 0
#         xdot[j] = 0
(f,fhz) = get_force([E,c,R],x,xdot)

fsav= f
fhz_sav = fhz

color = 'tab:red'
ax3.set_xlabel('GC %\nc)')
ax3.set_ylabel('Deformation [mm]', color=color)
ax3.plot(t, xsav,label='s1',color=color,linewidth=1)
ax3.tick_params(axis='y', labelcolor=color)
# horizontal line
ax3.hlines(0, 0, 100, colors='k', linestyles='solid')
ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis


#Fill under the curve
plt.fill_between(
        x= t, 
        y1= fsav[:len(t)], 
        where= (0 < fsav[:len(t)])&(xsav[:len(t)] > 0),
        color= "b",
        alpha= 0.2)
        
# find value of x where force is zero
# find index where force is zero
idx = np.where((fsav < 1 ) & (xsav > 0))[0][0]
ax3.plot(t[idx], xsav[idx], 'r*')



color = 'tab:blue'
ax4.set_ylabel('Force [N]', color=color)  
ax4.plot(t, fsav,label='s1',color=color,linewidth=1)
#ax2.plot(t,fhz_sav[0],label='s1',color='green',linewidth=1)
#ax2.plot(t, fsav[0]-fhz_sav[0])
ax4.tick_params(axis='y', labelcolor=color)

fig.set_figwidth(7.16)
fig.set_figheight(3.)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# put zero at same
# save
# plt.savefig('custom_smooth_force.png',dpi=600)
plt.show()

