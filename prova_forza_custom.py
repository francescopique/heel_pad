import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, tanh
from opensim_sto_reader import readMotionFile
import os

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
        fHz[i] = (4/3)*k*sqrt(R*k)*(sqrt(x[i]*x[i] +cf)**(3))
    fHz_smooth = np.zeros(len(fHz))
    for i in range(len(x)):
        fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*(x[i]-0.005)))

    fHc = fHz_smooth*(1 +1.5*c*xdot)

    fHc_smooth = np.zeros(len(fHc))
    for i in range(len(xdot)):
        fHc_smooth[i] = fHc[i]*(0.5 + 0.5*tanh(bv*(xdot[i]+ (2./(3.*c)))))

    fN = fHc_smooth

    return  (fN, fHz_smooth)

# FORCE ON TOP OF DISPLAGEMENT
E = 5.62898958e9
c = 0.59582
t = np.linspace(0,100,100)
# load heel sphere center position data
path = '../bilevel_ocp/sphere_analysis/data/custom_newsmooth_l/new_model_scaled_FK_contacts_fra_s2_s2_pos.sto'
[header, labels, data] = readMotionFile(path)
data = np.array(data)
# get contact point position
R = 0.03
x = data[:,2]-R
xsav = x

# load heel sphere center velocity data
path = '../bilevel_ocp/sphere_analysis/data/custom_newsmooth_l/new_model_scaled_FK_contacts_fra_s2_s2_vel.sto'
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

# open figure
fig, ax = plt.subplots()

color = 'tab:red'
ax.set_xlabel('GC %\nc)')
ax.set_ylabel('Deformation [mm]', color=color)
ax.plot(t, xsav,label='s1',color=color,linewidth=1)
ax.tick_params(axis='y', labelcolor=color)
# horizontal line
ax.hlines(0, 0, 100, colors='k', linestyles='solid')
ax4 = ax.twinx()  # instantiate a second axes that shares the same x-axis


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
ax.plot(t[idx], xsav[idx], 'r*')



color = 'tab:blue'
ax4.set_ylabel('Force [N]', color=color)  
ax4.plot(t, fsav,label='s1',color=color,linewidth=1)
#ax2.plot(t,fhz_sav[0],label='s1',color='green',linewidth=1)
ax4.plot(t, fsav-fhz_sav,label='hc',color='green',linewidth=1)    
ax4.tick_params(axis='y', labelcolor=color)

# load resulting GRF
simulation ='20240418091532'
pathTraje = os.path.join('../bilevel_ocp/Results', simulation) 
pathResults = pathTraje
# load an npy
optimalTrajectories = np.load(pathTraje + '\optimalTrajectories.npy', allow_pickle=True).item()
optimalTrajectories = optimalTrajectories['1']
GRF= optimalTrajectories['GRF']
t = np.linspace(0,100,GRF.shape[1])
print(GRF.shape)
ax4.plot(t,GRF[4,:],label='GRF',color='k',linewidth=1)

fig.set_figwidth(7.16)
fig.set_figheight(3.)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# put zero at same
# save
#plt.savefig('custom_smooth_force.png',dpi=600)
plt.show()
