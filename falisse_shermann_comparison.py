import numpy as np
from math import sqrt, tanh
import matplotlib.pyplot as plt
# here we show that shermann and falisse are equivalent if the initial
# coefficient is sqrt(2)/3

# we use the same parameters aas falisse docs
# cf here is missing!


E = 1e6
c = 2
R = 0.8
bd = 300
x = np.linspace(0,0.03,100)

#falisse
k = 1/2 * E**(2./3.)
fHz = (4/3)*k*sqrt(R*k)*x**(3/2)
fHz_smooth = np.zeros(len(fHz))
for i in range(len(x)):
    fHz_smooth[i] = fHz[i]*(0.5 +0.5*tanh(bd*x[i]))

#shermann


fHz = (sqrt(2)/3)*sqrt(R)*E*x**(3/2)

#plots
plt.plot(x,fHz_smooth,'k',label='Falisse')
plt.plot(x,fHz,'r',label='Shermann')
plt.xlabel('Indentation [m]')
plt.ylabel('Normal force [N]')
plt.legend()
plt.show()