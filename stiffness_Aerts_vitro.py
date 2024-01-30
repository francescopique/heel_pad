import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos
from utils import get_fn_indent_half
from scipy.optimize import least_squares


# data by hand from aertz
# load np array from csv
data_path = 'aertz_asc_vitro.csv'
data = np.genfromtxt(data_path,delimiter='\t')
# convert to SI
data[:,0] = data[:,0]/1000 # mm to m

plt.rcParams['text.usetex'] = True



# Compute normal foerce with HC model and default parms
x_peak = max(data[:,0])   # massima profondità di indentazione [m]
f = 1.1             # frequenza della sinusoide [Hz]
R = 0.032           # raggio sfera di contatto da osim [m]
x = np.linspace(0, x_peak, 100) 
E=1e6
c=2
fN = get_fn_indent_half([E,c],x,x_peak,f)


plt.plot(data[:,0],data[:,1],label='In vitro experimental (Aertz 1995)',color='black')
plt.plot(x,fN,label='model E=%f c=%f' %tuple((E,c)),linestyle='--',color='blue')
plt.xlabel('x [m]')
plt.ylabel('f [N]')

# optimise
def residuals(X,data):
    fN = get_fn_indent_half(X,data[:,0],x_peak,f)
    return fN - data[:,1]

x0 = np.array([1e6,2])
res = least_squares(residuals, x0, args=(data,),bounds=([1e1,0], [1e10,1e2]))
print(res)

#try optimized function

fN = get_fn_indent_half(res.x,data[:,0],x_peak,f)
plt.plot(data[:,0],fN,label='Best fit model E=%f c=%f' %tuple((res.x[0],res.x[1])),linestyle='-.',color='red')
plt.legend()
plt.show()

