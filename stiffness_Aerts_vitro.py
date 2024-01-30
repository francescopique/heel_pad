import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, sin, cos, acos
from utils import get_fn_indent_half
from scipy.optimize import least_squares


# data by hand from aertz
# load np array from csv
data_path = 'aertz_asc_vitro.csv'
data = np.genfromtxt(data_path,delimiter='\t')
mm = data[:,0]
N = data[:,1]




x_init = 0          # non c'è contatto iniziale, e la velocità iniziale è nulla
x_peak = 0.0063    # massima profondità di indentazione
f = 1.1             # frequenza della sinusoide
R = 0.032           # raggio sfera di contatto da osim

x = np.linspace(x_init, x_peak, 100) 

E=1e6
c=2
fN = get_fn_indent_half([E,c],x_peak,f)


plt.plot(1000*x, fN, )
# plt.plot(x*1000, fHz)
# plt.plot(x*1000, fdiss)
plt.plot(mm, N,'-.')
#plt.legend(['fN', 'fHz', 'fdiss','aertz'])
plt.legend(['model E=%d c=%d' %tuple((E,c)),'aertz'])
plt.xlabel('x [mm]')
plt.ylabel('f [N]')
plt.show()

# optimise
def residuals(X,data):
    fN = get_fn_indent_half(X,x_peak,f)
    return fN - data[:,1]

x0 = np.array([1e6,2])
res = least_squares(residuals, x0, args=(data,),bounds=([1e1,0], [1e10,1e2]))
print(res)

#try optimized function

fN = get_fn_indent_half(res.x,x_peak,f)
plt.plot(data[:,0],fN)
plt.plot(data[:,0],data[:,1])
plt.legend(['model E=%d c=%d' %tuple((res.x[0],res.x[1])),'aertz'])


plt.show()

