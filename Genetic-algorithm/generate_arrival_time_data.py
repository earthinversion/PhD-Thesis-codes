import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
part1 = 0
part2 = 1

np.random.seed(0)

error = 0.10 #10 percent


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

if part1:

    def calc_arrival_time(eq_loc, stnx, stny, stnz, vel, origintime):
        eqx, eqy, eqz = eq_loc
        dist = np.sqrt((eqx - stnx)**2 + (eqy - stny)**2 + (eqz - stnz)**2)
        arr = dist/vel + origintime
        return arr



    eq_initial_guess = [eq_loc[0]+error*eq_loc[0],eq_loc[1]+error*eq_loc[1],eq_loc[2]+error*eq_loc[2]]
    m_intial = [eq_initial_guess[0],eq_initial_guess[1],eq_initial_guess[2],vel+error*vel,origintime+error*origintime]


    d_obs = []
    d_pre = []
    noise_level_data = 0.1
    # noise_level_data = 0.001
    for stnx, stny, stnz in stn_locs:
        # print("{:.2f} {:.2f} {:d}".format(stnx, stny, stnz))
        arr = calc_arrival_time(eq_loc, stnx, stny, stnz, vel, origintime)
        sign = np.random.choice([-1,1])
        d_obs.append(arr+sign*noise_level_data*arr)
        print("Arrival time at ({},{},{}) is {}".format(stnx, stny, stnz, arr+sign*noise_level_data*arr))
        # print("{:.2f}".format(arr+0.05*arr))
        d_pre.append(calc_arrival_time(eq_initial_guess, stnx, stny, stnz, m_intial[3], m_intial[4]))

    d_obs = np.array(d_obs)
    d_pre = np.array(d_pre)

    arr_df = pd.DataFrame()
    arr_df['dobs'] = d_obs
    arr_df['d_pre'] = d_pre

    arr_df.to_csv('arrival_times.csv',index=False)

    stn_locs = np.array(stn_locs)
    station_loc_df = pd.DataFrame()
    station_loc_df['xloc'] = stn_locs[:,0]
    station_loc_df['yloc'] = stn_locs[:,1]
    station_loc_df['zloc'] = stn_locs[:,2]

    station_loc_df.to_csv('station_locations.csv',index=False)




#####################
if part2:
    ## plotting ellipsoid
    import numpy.linalg as linalg
    
    def estimate_ellipsoid(center,coeffs=[1,2,2]):
        A = np.array([[coeffs[0],0,0],[0,coeffs[1],0],[0,0,coeffs[2]]])
        # center = [0,0,0]

        # find the rotation matrix and radii of the axes
        U, s, rotation = linalg.svd(A)
        radii = 1.0/np.sqrt(s)

        u = np.linspace(0.0, 2.0 * np.pi, 100)
        v = np.linspace(0.0, np.pi, 100)
        xx = radii[0] * np.outer(np.cos(u), np.sin(v))
        yy = radii[1] * np.outer(np.sin(u), np.sin(v))
        zz = radii[2] * np.outer(np.ones_like(u), np.cos(v))
        for i in range(len(xx)):
            for j in range(len(xx)):
                [xx[i,j],yy[i,j],zz[i,j]] = np.dot([xx[i,j],yy[i,j],zz[i,j]], rotation) + center
        return xx, yy, zz
    
    

    dff_eq_locs = pd.read_csv('eq_loc.txt',sep='\s+')
    mean_model_param = dff_eq_locs.mean().values
    print(mean_model_param)
    std_model_param = dff_eq_locs.std().values

    center = [mean_model_param[0],mean_model_param[1],mean_model_param[2]]
    xx, yy, zz = estimate_ellipsoid(center,coeffs=[std_model_param[0],std_model_param[1],std_model_param[2]])

    ## plot result
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
    # ax.scatter(eq_initial_guess[0],eq_initial_guess[1],eq_initial_guess[2],c='gray',marker='*',s=100,label='Initial Guess EQ location')
    ax.scatter(mean_model_param[0],mean_model_param[1],mean_model_param[2],c='k',marker='*',s=100,label='Inverted EQ location')
    ax.plot_surface(xx, yy, zz,  rstride=4, cstride=4, color='yellow',alpha=0.2)
    # plt.title("Inverted model EQ loc: ({:.2f},{:.2f},{:.2f}),\nvel: {:.2f} and origin time: {:.2f}\nsq_error: {:.2f}".format(inv_model[0],inv_model[1],inv_model[2],inv_model[3],inv_model[4],squared_error),fontsize=8)
    ax.set_xlim([-3,3])
    ax.set_ylim([-4,4])
    ax.set_zlim(-3,0.1)
    plt.legend()
    plt.tight_layout()
    plt.savefig('Earthquake_loc_ga.png',bbox_inches='tight',dpi=300)
    # plt.savefig('Earthquake_loc_5stn_30percent_error.png',bbox_inches='tight',dpi=300)
    plt.close('all')