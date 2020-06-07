import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert

t=np.linspace(0.1,100,1000)
x=np.linspace(50,150,1000)

omega = np.linspace(10,100,1000)
kappa = np.linspace(10,100,1000)

deltaomega = np.linspace(0.1,1,1000)
deltakappa = np.linspace(0.1,1,1000)

u_xt = 2 * np.cos(omega*t - kappa *x)* np.cos(deltaomega*t - deltakappa *x)
envelope = np.abs(hilbert(u_xt))

fig, ax = plt.subplots(1,1,figsize=plt.figaspect(0.5))
ax.plot(t,u_xt,'k-',lw=0.5,label='Carrier')
ax.plot(t,envelope,'b-',lw=1,label='Envelope')
ax.plot(t,-envelope,'b-',lw=1)
plt.legend(fontsize=18)
plt.tight_layout()
plt.savefig('phase_group_vel.png',dpi=300,bbox_inches='tight')
plt.close('all')
