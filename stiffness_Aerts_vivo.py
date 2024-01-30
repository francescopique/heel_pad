import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos
from scipy.optimize import least_squares
from scipy.signal import resample
from utils import get_fn_indent_half, get_fn_standard, get_fn_indent_full

plt.rcParams['text.usetex'] = True

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

x_init = 0        # non c'è contatto iniziale, e la velocità iniziale è nulla
x_peak = 0.01222   #[m] massima profondità di indentazione (in questo caso di deformazione perchè l'esperimento non è deformaz.)
f = 1.1           # frequenza della sinusoide
R = 0.032         # raggio sfera di contatto da osim

x = np.linspace(x_init, x_peak, 100) 

# conti da verificare, sapendo che l'indentatore impone uno spostamento sinusoidale
# tipo x = [1-cos(2*pi*f*t)]*xp/2, possiamo ricavare la velocità:
t = 1-2*(x)/(x_peak)

for i in range(len(t)):
    t[i] = acos(t[i])/(2*pi*f)

xdot = pi*f*t
for i in range(len(xdot)):
    xdot[i] = f*x_peak*pi*sin(2*pi*f*t[i])

# parte per avere un ciclo completo
x = np.append(x,np.flip(x))
xdot = np.append(xdot,-xdot)
t = np.append(t, t+t[-1])

# plt position and velocity
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_title('Indentation test. ($\mathrm{x_{max}}$=%f m, f=%f Hz)' %tuple((x_peak,f)), fontsize=14)
ax1.set_xlabel('t [s]')
ax1.set_ylabel('x [m]', color=color)
ax1.plot(t, x, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx() 
color = 'tab:blue'
ax2.set_ylabel('$\mathrm{\dot{x}}$ [m/s]', color=color)  
ax2.plot(t, xdot, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  
plt.show()



#incognite
E = 1e6
c = 2

fHz = (4/3)*sqrt(R)*E*x**(1.5)
fHc = 1.5*fHz*c*xdot

fdiss = np.zeros(len(fHc))
for i in range(len(fHc)):
    fdiss[i] = max(fHc[i],-fHz[i]) 

fN = fHz + fdiss
plt.plot(data[:,0], data[:,1],label='In vivo (Aerts 1993)',color='black')
plt.plot(x, fN, '-.',label='HC model E=%d c=%d' %tuple((E,c)),color='blue',linestyle='--')

plt.xlabel('x [m]')
plt.ylabel('Normal force [N]')




# optimization
def residuals(X,data_load,data_unload):
    fN =  get_fn_indent_full(X,data_load[:,0],data_unload[:,0],x_peak,f)
    fN_truth = np.append(data_load[:,1],data_unload[:,1])
    return fN - fN_truth

x0 = np.array([1e6,2])
bounds=([1e1,0], [1e11,1e2]) # 100 Pa<E<100 GPa, 0<c<100
res = least_squares(residuals, x0, args=(data_load,data_unload),bounds=bounds)
print(res)

#try optimized function
fN = get_fn_indent_full(res.x,data_load[:,0],data_unload[:,0],x_peak,f)


#plot
plt.plot(np.append(data_load[:,0],data_unload[:,0]),fN, '--',label='Best fit: E=%5.3f, c=%5.3f' % tuple(res.x),color='red',linestyle='-.')
plt.legend()
plt.show()
