import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
plt.style.use('seaborn')


x = np.linspace(-10,10,100)
t = np.linspace(0,10,30)

[X,T]=np.meshgrid(x,t) 

def sech(X):
    return 1/np.cosh(X)

f=sech(X)*(1-0.5*np.cos(2*T))+(sech(X)*np.tanh(X))*(1-0.5*np.sin(2*T))

print("f shape",f.shape)

vmin = np.amin(f)
vmax = np.amax(f)
print(vmin,vmax)


from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure(figsize=plt.figaspect(0.8))
# ax = fig.gca(projection='3d')
# # Plot the surface.
# surf = ax.plot_surface(T, X, f, cmap='summer',linewidth=0, antialiased=True, rstride=1, cstride=1, alpha=None)
# ax.set_ylabel(r'$X$')
# ax.set_xlabel(r'$T$')
# surf.set_clim(vmin,vmax)
# plt.colorbar(surf)
# plt.tight_layout()
# plt.savefig('PCA_space_time_func.png',dpi=300,bbox_inches='tight')
# plt.close('all')


u,s,v = linalg.svd(f, full_matrices=False,check_finite=False)
eigen_values = s
s = np.diag(s)



pca_modes = []
for j in range(1,3):
    ff=u[:,0:j].dot(s[0:j,0:j]).dot(v[0:j,:])
    # print(u[:,0:j].shape,s[0:j,0:j].shape,v[:,0:j].T.shape)
    pca_modes.append(ff)


vmin = np.min([np.amin(pca_modes[0]),np.amin(pca_modes[1])])
vmax = np.max([np.amax(pca_modes[0]),np.amax(pca_modes[1])])


# fig = plt.figure(figsize=plt.figaspect(0.5))
# for jj in range(len(pca_modes)):
#     ax = fig.add_subplot(1, 2, jj+1, projection='3d')
#     surf = ax.plot_surface(T, X, pca_modes[jj], cmap='summer',linewidth=0, antialiased=True, rstride=1, cstride=1, alpha=None)
#     surf.set_clim(vmin,vmax)
#     ax.set_ylabel(r'$X$')
#     ax.set_xlabel(r'$T$')
#     ax.set_title('Var explained: {:.2f}%'.format(eigen_values[jj]/np.sum(eigen_values)*100))

# plt.colorbar(surf)
# plt.subplots_adjust(hspace=0.5,wspace=0.05)
# plt.tight_layout()
# plt.savefig('PCA_space_time_func_modes.png',dpi=300,bbox_inches='tight')
# plt.close('all')


## Spatial and temporal behaviour
fig, ax = plt.subplots(2,1,figsize=plt.figaspect(0.5))
ax[0].plot(x,v[0,:],'k-',label='mode 1')
ax[0].plot(x,v[1,:],'k--',label='mode 2')
ax[0].set_xlabel('x')
ax[0].set_ylabel('PCA modes')
ax[0].legend()


ax[1].plot(t,u[:,0],'k-',label='mode 1')
ax[1].plot(t,u[:,1],'k--',label='mode 2')
ax[1].set_xlabel('x')
ax[1].set_ylabel('PCA modes')
ax[1].legend()

plt.subplots_adjust(hspace=0.5,wspace=0.05)
plt.tight_layout()
plt.savefig('PCA_space_time_behaviour.png',dpi=300,bbox_inches='tight')
plt.close('all')

