import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import inv

np.random.seed(0)

plt.style.use('seaborn')
error = 0.10 #10 percent


minx, maxx = -2, 2
miny, maxy = -3, 3
# stn_locs = [[-2,3,0],[1,3,0],[-2,-1,0],[0,-3,0],[2,-2,0]]
numstations = 30
stn_locs=[]
xvals = minx+(maxx-minx)*np.random.rand(numstations)
yvals = miny+(maxy-miny)*np.random.rand(numstations)

for num in range(numstations):
    stn_locs.append([xvals[num],yvals[num],0])



eq_loc = [2,2,-2]
vel = 6 #kmps
origintime = 0

def calc_arrival_time(eq_loc, stnx, stny, stnz, vel, origintime):
    eqx, eqy, eqz = eq_loc
    dist = np.sqrt((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)
    arr = dist/vel + origintime
    return arr

def G_matrix_cols(eq_loc, stnx, stny, stnz, vel, origintime):
    eqx, eqy, eqz = eq_loc
    G_col1 = (eqx-stnx)/vel * ((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)**(-1/2)
    G_col2 = (eqy-stny)/vel * ((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)**(-1/2)
    G_col3 = (eqz-stnz)/vel * ((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)**(-1/2)
    G_col4 = -1/vel**2 * ((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)**(1/2)
    G_col5 = 1
    return [G_col1,G_col2,G_col3,G_col4,G_col5]


eq_initial_guess = [eq_loc[0]+error*eq_loc[0],eq_loc[1]+error*eq_loc[1],eq_loc[2]+error*eq_loc[2]]
m_intial = [eq_initial_guess[0],eq_initial_guess[1],eq_initial_guess[2],vel+error*vel,origintime+error*origintime]


G_matrix = []
d_obs = []
d_pre = []
noise_level_data = 0.1
# noise_level_data = 0.001
for stnx, stny, stnz in stn_locs:
    # print("{:.2f} {:.2f} {:d}".format(stnx, stny, stnz))
    arr = calc_arrival_time(eq_loc, stnx, stny, stnz, vel, origintime)
    G_matrix.append(G_matrix_cols(eq_initial_guess, stnx, stny, stnz, m_intial[3], m_intial[4]))
    sign = np.random.choice([-1,1])
    d_obs.append(arr+sign*noise_level_data*arr)
    print("Arrival time at ({},{},{}) is {}".format(stnx, stny, stnz, arr+sign*noise_level_data*arr))
    # print("{:.2f}".format(arr+0.05*arr))
    d_pre.append(calc_arrival_time(eq_initial_guess, stnx, stny, stnz, m_intial[3], m_intial[4]))

d_obs = np.array(d_obs)
d_pre = np.array(d_pre)
G_matrix = np.array(G_matrix)


delm = inv(np.transpose(G_matrix).dot(G_matrix)).dot(np.transpose(G_matrix)).dot(d_obs-d_pre)
inv_model = m_intial+delm


print("Actual model EQ loc: ({:.2f},{:.2f},{:.2f}), vel: {:.2f} and origin time: {:.2f}".format(eq_loc[0],eq_loc[1],eq_loc[2],vel,origintime))
print("Initial model EQ loc: ({:.2f},{:.2f},{:.2f}), vel: {:.2f} and origin time: {:.2f}".format(m_intial[0],m_intial[1],m_intial[2],m_intial[3],m_intial[4]))
print("Inverted model EQ loc: ({:.2f},{:.2f},{:.2f}), vel: {:.2f} and origin time: {:.2f}".format(inv_model[0],inv_model[1],inv_model[2],inv_model[3],inv_model[4]))

squared_error = np.sum((inv_model-m_intial)**2)


## to create the surface
X = np.linspace(-3, 3, 200)
Y = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(X, Y)
Z = (X**2 + Y**2)*0

fig = plt.figure()
ax = plt.axes(projection='3d')
# plot stations
ax.scatter([x[0] for x in stn_locs],[x[1] for x in stn_locs],[x[2] for x in stn_locs],c='b',marker='^',s=50)
# plot surface
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,linewidth=0, antialiased=False,alpha=0.1)
# plot actual EQ
ax.scatter(eq_loc[0],eq_loc[1],eq_loc[2],c='r',marker='*',s=100,label='Actual EQ location')
ax.scatter(eq_initial_guess[0],eq_initial_guess[1],eq_initial_guess[2],c='gray',marker='*',s=100,label='Initial Guess EQ location')
ax.scatter(inv_model[0],inv_model[1],inv_model[2],c='k',marker='*',s=100,label='Inverted EQ location')
plt.title("Inverted model EQ loc: ({:.2f},{:.2f},{:.2f}),\nvel: {:.2f} and origin time: {:.2f}\nsq_error: {:.2f}".format(inv_model[0],inv_model[1],inv_model[2],inv_model[3],inv_model[4],squared_error),fontsize=8)
ax.set_xlim([-3,3])
ax.set_ylim([-4,4])
ax.set_zlim(-3,0.1)
plt.legend()

plt.savefig('Earthquake_loc_{:.0f}stn_{:.0f}percent_error.png'.format(numstations,error*100),bbox_inches='tight',dpi=300)
# plt.savefig('Earthquake_loc_5stn_30percent_error.png',bbox_inches='tight',dpi=300)
plt.close('all')
