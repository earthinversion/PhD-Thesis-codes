import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

np.random.seed(0)

plt.style.use('seaborn')


minx, maxx = -2, 2
miny, maxy = -3, 3
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



d_obs = []
noise_level_data = 0.001
for stnx, stny, stnz in stn_locs:
    arr = calc_arrival_time(eq_loc, stnx, stny, stnz, vel, origintime)
    sign = np.random.choice([-1,1])
    d_obs.append(arr+sign*noise_level_data*arr)

d_obs = np.array(d_obs)

def get_rand_number(min_value, max_value):
    range_vals = max_value - min_value
    choice = np.random.uniform(0,1)
    return min_value + range_vals*choice

## Monte Carlo

num_iterations = 100000
inv_model = []
squared_error0 = 100000 

mineqx, maxeqx = -3, 3
mineqy, maxeqy = -3, 3
mineqz, maxeqz = 0, -3
gen_num = []
lse = []
for i in range(num_iterations):
    eqx0 = get_rand_number(mineqx, maxeqx)
    eqy0 = get_rand_number(mineqy, maxeqy)
    eqz0 = get_rand_number(mineqz, maxeqz)
    vel0 = get_rand_number(5, 7)
    origintime0 = get_rand_number(-1, 1)
    d_pre = []
    for stnx, stny, stnz in stn_locs:
        d_pre.append(calc_arrival_time([eqx0, eqy0, eqz0], stnx, stny, stnz, vel0, origintime0))
    d_pre = np.array(d_pre)

    squared_error = np.sum((d_obs-d_pre)**2)
    if squared_error < squared_error0:
        print(i,squared_error)
        gen_num.append(i)
        lse.append(squared_error)
        m0 =  np.array([eqx0, eqy0, eqz0, vel0, origintime0])
        if np.abs(squared_error-squared_error0)<0.001:
            print("Terminated based on tol. value",np.abs(squared_error-squared_error0))
            break
        squared_error0 = squared_error
        inv_model = m0

print("{:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(inv_model[0],inv_model[1],inv_model[2],inv_model[3],inv_model[4]))


fig, ax = plt.subplots(1,1,figsize=(5,5))
ax.loglog(gen_num,lse, 'ko--')
ax.set_xlabel('Generations')
ax.set_ylabel('Least-squares error')
plt.savefig('iterations.png',bbox_inches='tight',dpi=300)
plt.close('all')



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
ax.scatter(inv_model[0],inv_model[1],inv_model[2],c='k',marker='*',s=100,label='Inverted EQ location')
plt.title("Inverted model EQ loc: ({:.2f},{:.2f},{:.2f}),\nvel: {:.2f} and origin time: {:.2f}\nsq_error: {:.2f}".format(inv_model[0],inv_model[1],inv_model[2],inv_model[3],inv_model[4],squared_error),fontsize=8)
ax.set_xlim([-3,3])
ax.set_ylim([-3,3])
ax.set_zlim(-3,0.1)
plt.legend()

plt.savefig('Earthquake_loc_monte_carlo.png',bbox_inches='tight',dpi=300)
plt.close('all')
