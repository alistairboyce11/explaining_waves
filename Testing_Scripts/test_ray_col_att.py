'''
Script to test ray_colors_atten.py

'''
import numpy as np
import sys
sys.path.append('../')
import ray_colors_atten as rca
import phase_finder as pf
# # Obspy is a seismic toolkit
import obspy
import matplotlib
intp = matplotlib.cbook.simple_linear_interpolation
from matplotlib.collections import LineCollection

from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths
# velocity model as a function of depth.
model = TauPyModel(model='ak135')

Test_1 = False # Test get ray color
Test_2 = False # Test get ray attenuation

# Set values
propagation_time=700
# phases_to_plot=['P', 'PP', 'PcP', 'PKP', 'PKiKP', 'PKIKP', 'PKKP']
phases_to_plot=['PcP']

depth_earthquake=0

seis_channel='BXZ'

rays_dist_min=[]
rays_dist_max=[]
for i in range(len(phases_to_plot)):
    print(phases_to_plot[i])
    min_rd=pf.find_min_ray_dist(depth_earthquake=depth_earthquake, phase_name=phases_to_plot[i])
    max_rd=pf.find_max_ray_dist(depth_earthquake=depth_earthquake, phase_name=phases_to_plot[i])
    rays_dist_min.append(min_rd)
    rays_dist_max.append(max_rd)


print('Plotting phases: '+str(phases_to_plot))
print('At min dists: '+str(rays_dist_min))
print('At max dists: '+str(rays_dist_max))



# regular time array in s, 1 s resolution
time = np.arange(0., propagation_time)
radius=6371

# calculate through and save ray paths in interpolated time domain
save_paths=[]
for p, phase  in enumerate(phases_to_plot):
    dists_collected=[]
    depths_collected=[]
    amps_collected=[]
    cols_collected=[]
    # for dist in np.arange(rays_dist_min[p], rays_dist_max[p] + 1 , 1): # +1 required as arange excludes last value.
    for dist in np.array([25,50]):
        # get raypaths
        rays = model.get_ray_paths(depth_earthquake, dist, phase_list=[phase])
        # Loop through rays found, some phases have multiple paths
        for ray in rays:
            # Interpolate to regulard time array
            dists = np.interp(time, ray.path['time'], ray.path['dist'], left = np.nan, right = np.nan)
            depths = np.interp(time, ray.path['time'], ray.path['depth'], left = np.nan, right = np.nan)
            ray_param=ray.ray_param/(radius*1000) # convert to s/km from s/radian.
            amps = rca.get_ray_atten(phase,dist,time,dists,depths,ray_param,seis_channel)
            cols = rca.get_ray_color(phase,dist,time,dists,depths,ray_param)
            # save paths
            dists_collected.append(dists)
            depths_collected.append(depths)
            amps_collected.append(amps)
            cols_collected.append(cols)
    save_paths.append([np.array(dists_collected),np.array(depths_collected),np.array(amps_collected),np.array(cols_collected)])
save_paths=np.array(save_paths)
print(np.shape(save_paths))


# save wave fronts to the left and right
lines_left=[]
lines_right=[]

print('dists:')
print(save_paths[0,0])
print('depths:')
print(save_paths[0,1])
print('amps:')
print(save_paths[0,2])
print('cols:')
print(save_paths[0,3])

#
# print(np.shape(save_paths))
#
# t=0
# for p in range(len(save_paths)):
#     dists_collected=save_paths[p,0]
#     depths_collected=save_paths[p,1]
#     amps_collected=save_paths[p,2]
#     cols_collected=save_paths[p,3]
#     front_dist= dists_collected[:,t] # Cut at single time across all paths
#     front_depth = depths_collected[:, t] # Cut at single time across all paths
#     front_amps = amps_collected[:, t] # Cut at single time across all paths
#     front_cols = cols_collected[:, t] # Cut at single time across all paths
#     print(front_amps)
#     print(front_cols)
#     # set colour and alphas.
#     # Make same length as interpolated values passed to line variable.
#     # Not sure why this isnt 100 but the work aroudn below works fine :)
#     rgba_colors = np.zeros((len(intp(front_cols, 20)),4))
#     print(np.shape(front_dist))
#     print(np.shape(front_depth))
#     print(np.shape(front_amps))
#     print(np.shape(front_cols))
#     print(np.shape(rgba_colors))
#     print(len(intp(front_depth, 20)))
#
#     rgba_colors[:,0] = intp(front_cols, 20)
#     rgba_colors[:,1] = intp(front_cols, 20)
#     rgba_colors[:,2] = intp(front_cols, 20)
#     rgba_colors[:,3] = intp(front_amps, 20)
#     print(front_amps)
#     print(rgba_colors[:,3])
#     # # plot line towards the right side
#     # line, = ax2.plot(intp(front_dist, 20),radius - intp(front_depth, 20),color=rgba_colors[0])
#     # lines_right.append(line)
#     # # mirror line towards the left
#     # line, = ax2.plot(intp(-1.*front_dist, 20),radius - intp(front_depth, 20),color=rgba_colors[0])
#     # lines_left.append(line)
#
#
#     interp_value=20
#     x_r = intp(front_dist, interp_value)
#     x_l = intp(-1.*front_dist, interp_value)
#     y   = radius - intp(front_depth, interp_value)
#
#     rgba_colors = np.zeros((len(x_r),4))
#     rgba_colors[:,0] = intp(front_cols, interp_value)
#     rgba_colors[:,1] = intp(front_cols, interp_value)
#     rgba_colors[:,2] = intp(front_cols, interp_value)
#     rgba_colors[:,3] = intp(front_amps, interp_value)
#
#     points_r=np.array([x_r, y]).T.reshape(-1, 1, 2)
#     points_l=np.array([x_l, y]).T.reshape(-1, 1, 2)
#
#     segs_r=np.concatenate([points_r[:-1], points_r[1:]], axis=1)
#     segs_l=np.concatenate([points_l[:-1], points_l[1:]], axis=1)
#
#     lc_r=LineCollection(segs_r,linewidth=2, linestyle='solid', colors=rgba_colors)
#     lc_l=LineCollection(segs_l,linewidth=2, linestyle='solid', colors=rgba_colors)
#
#     print('Finished....')
#
#




