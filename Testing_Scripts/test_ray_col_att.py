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
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths
# velocity model as a function of depth.
model = TauPyModel(model='ak135')

Test_1 = False # Test get ray color
Test_2 = False # Test get ray attenuation

# Set values
propagation_time=600
phases_to_plot=['P','PcP', 'S','ScS']
depth_earthquake=0


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


# calculate through and save ray paths in interpolated time domain
save_paths=[]
for p, phase  in enumerate(phases_to_plot):
    dists_collected=[]
    depths_collected=[]
    amps_collected=[]
    cols_collected=[]
    for dist in np.arange(rays_dist_min[p], rays_dist_max[p] + 1 , 1): # +1 required as arange excludes last value.
        # get raypaths
        rays = model.get_ray_paths(depth_earthquake, dist, phase_list=[phase])
        # Loop through rays found, some phases have multiple paths
        for ray in rays:
            # Interpolate to regulard time array
            dists = np.interp(time, ray.path['time'], ray.path['dist'], left = np.nan, right = np.nan)
            depths = np.interp(time, ray.path['time'], ray.path['depth'], left = np.nan, right = np.nan)
            amps = rca.get_ray_atten(phase,dist,time,dists,depths)
            cols = rca.get_ray_color(phase,dist,time,dists,depths)
            # save paths
            dists_collected.append(dists)
            depths_collected.append(depths)
            amps_collected.append(amps)
            cols_collected.append(cols)
    save_paths.append([np.array(dists_collected),np.array(depths_collected),np.array(amps_collected),np.array(cols_collected)])
save_paths=np.array(save_paths)
print(np.shape(save_paths))

# if Test_1:
#     rca.get_ray_color()
#
# if Test_2:
#     rca.get_ray_atten()

