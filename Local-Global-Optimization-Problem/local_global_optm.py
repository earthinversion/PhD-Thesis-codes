import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')



## Example 1
x = np.linspace(-3,3,100)
obj_fun = np.cos(14.5 * x - 0.3) + x*(x + 0.2) + 1.01

fig, ax = plt.subplots(1,1,figsize=(10,6))
ax.plot(x,obj_fun)
ax.axvline(x = x[np.argmin(obj_fun)],color='r',ls='--')
ax.set_ylabel(r'$f(x)$')
ax.set_xlabel(r'$x$')
plt.savefig('local_global_objective_function.png',dpi=300,bbox_inches='tight')
plt.close('all')


## Example 2 Surface plot
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


x2 = np.linspace(-6,6,100)
y2 = np.linspace(-6,6,100)
X,Y = np.meshgrid(x2,y2)

obj_fun2 = ((X+0.5)**4 - 30*X**2- 20*X + (Y+0.5)**4 - 30*Y**2- 20*Y)/100

fig = plt.figure(figsize=(5,5))
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(X, Y, obj_fun2, cmap=cm.jet,linewidth=0, antialiased=False)
ax.set_ylabel(r'$x$')
ax.set_xlabel(r'$y$')
plt.savefig('local_global_objective_function3D.png',dpi=300,bbox_inches='tight')
plt.close('all')


## Example 2 contour plot


fig, ax = plt.subplots(1,1,figsize=(6,5))
cp = ax.contourf(X, Y, obj_fun2, 20, cmap='jet')
plt.colorbar(cp)
# ax.clabel(cp, inline=True, fontsize=10)

ax.set_ylabel(r'$y$')
ax.set_xlabel(r'$x$')
plt.savefig('local_global_objective_function_contour.png',dpi=300,bbox_inches='tight')
plt.close('all')