# -*- coding: utf-8 -*-
#############################################################################
### COMPUTES RAY PATHS AND TRAVEL TIMES FOR DIFFERENT BODY PHASES ##########
#############################################################################


### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt
# Obspy is a seismic toolkit
import obspy
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths

import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
# More about the obspy routines we are using can be found here:
# https://docs.obspy.org/packages/obspy.taup.html

# more imports
# import instaseis
# from obspy import read
import sys,glob
import os.path
# import obspy.signal.rotate
# from obspy import UTCDateTime
# import obspy.geodetics.base
# import obspy.geodetics
from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
import matplotlib.patches as patches

# Function below used to define input phases.
import phase_finder as pf

# Function used to generate seismogram
import gen_seis as gs

# velocity model as a function of depth.
model = TauPyModel(model='ak135')

########################## SET PARAMETERS HERE #############################

epi_dist = 35                             # Epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed

depth_earthquake = 0                    # depth of earthquake in km

Propagation_time = 900                  # Propagation time and seismogram length (s) - up to 3600s

Seismometer_shake_duration = 10         # Duration of shaking at the seismometer after the arrival of a plotted phase.

# phases_to_plot = ['P', 'PKiKP', 'PKP', 'PcP', 'Pn']
# color_attenuation=[1.0,  0.5,    0.8 ,  0.3,   0.3]

# phases_to_plot = ['P', 'PcP']
# color_attenuation=[1.0, 0.4]


#### ++++++++ Using phase finder.py +++++++++++ #############
# Use phase_finder.py toolbox to calculate phases to plot, min ray dist, max ray dist and attentuation (not yet working)

# pf.gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=[ 'P', 'PKiKP', 'PKP', 'PcP', 'PP', 'PKIKP', 'Pdiff', 'S', 'SKiKS', 'SKS', 'ScS', 'SS', 'SKIKS', 'Sdiff' ], overwrite_phase_defaults=True)
phases_to_plot=pf.find_phases_at_dist(depth_earthquake=depth_earthquake, epi_dist=epi_dist)

color_attenuation = 1 - (np.arange(0,len(phases_to_plot),1)/len(phases_to_plot))

# This gives the most accurate ray propagation but is slow and memory hungry!!!!

rays_dist_min=[]
rays_dist_max=[]
shake_arr_times=[]
for i in range(len(phases_to_plot)):
    print(phases_to_plot[i])
    min_rd=pf.find_min_ray_dist(depth_earthquake=depth_earthquake, phase_name=phases_to_plot[i])
    max_rd=pf.find_max_ray_dist(depth_earthquake=depth_earthquake, phase_name=phases_to_plot[i])
    rays_dist_min.append(min_rd)
    rays_dist_max.append(max_rd)
    arr1=pf.find_arrival_time(depth_earthquake=depth_earthquake, epi_dist=epi_dist, phase_name=phases_to_plot[i])
    shake_arr_times.append(arr1)

# Find the times to shake the seismometer.
shake_arr_times_sort=np.floor(np.sort(shake_arr_times))

shake_seis=[]
for i in range(len(shake_arr_times_sort)):
    shake_seis.append(np.arange(shake_arr_times_sort[i],shake_arr_times_sort[i]+Seismometer_shake_duration,1))

shake_seis=np.unique(shake_seis)


# Check that propagation time is greater that first arrival time.
F_A_name, F_A_time = pf.find_first_arrival(depth_earthquake=depth_earthquake, epi_dist=epi_dist)

if F_A_time > (Propagation_time-10):
    print('No phases arriving ......')
    print('Must allow more wave prop. time at '+str(epi_dist)+'deg distance.')
    print('exiting\n')
    sys.exit()
    


#-------------------# NOT READY FOR USE #-------------------#

# Need to work on amplitude attentuation factor......

##### +++++++++++++++++++++++++++++++++++++++++ #################
#-------------------# NOT READY FOR USE #-------------------#


# # min and max distances for the different phases to consider
# # these can be chosen broadly (could be set 0-180 for all), it just slows down the code a bit.
# rays_dist_min=[0, 100,100, 130, 0, 60, 0]
# rays_dist_max=[110, 150,  181, 181, 160,180, 180 ]

# darkness of grey (lower is lighter here)
# this should be adapted, colors should change at reflection points
# color_attenuation=[1.0, 0.5, 0.8, 0.8, 0.3, 0.8, 1.0]

# Waveform characteristics
Normalise_Waveform=True                             # Normalise waveform amplitude
Filter_Waveform=False                               # Filter waveform with bandpass filter; params below

# Output handling
Output_Location     =   '../wavefront_movie_outputs/'
gif_name_str        =   'seis_movie_'+str(epi_dist)+'deg'
Filename_GIF        =   Output_Location + gif_name_str + '.gif'

if not os.path.exists(Output_Location):
    os.makedirs(Output_Location)

########################## Fixed Parameters #############################

radius = 6371                                       # radius of Earth in km

################ Wavefront movie #######################

# regular time array in s, 1 s resolution
time = np.arange(0., Propagation_time)

# calculate through and save ray paths in interpolated time domain
save_paths=[]
for p, phase  in enumerate(phases_to_plot):
    dists_collected=[]
    depths_collected=[]
    for r, dist in enumerate(np.arange(rays_dist_min[p], rays_dist_max[p] + 1 , 1)): # +1 required as arange excludes last value.
        # get raypaths
        rays = model.get_ray_paths(depth_earthquake, dist, phase_list=[phase])
        # Loop through rays found, some phases have multiple paths
        for ray in rays:
            # Interpolate to regulard time array
            dists = np.interp(time, ray.path['time'], ray.path['dist'], left = np.nan, right = np.nan)
            depths = np.interp(time, ray.path['time'], ray.path['depth'], left = np.nan, right = np.nan)
            # save paths
            dists_collected.append(dists)
            depths_collected.append(depths)
    save_paths.append([np.array(dists_collected),np.array(depths_collected)])

save_paths=np.array(save_paths)

#interpolater for plotter
intp = matplotlib.cbook.simple_linear_interpolation

# save wave fronts to the left and right
lines_left=[]
lines_right=[]

# start plot for t= 0
fig = plt.figure(figsize =(10,5))
# fig = plt.figure(figsize =(20,11)) # Probably want this for final graphics....?

# define polar subplot
ax = plt.subplot(1,2,1, polar = True)
# ax = plt.subplot2grid((10, 10), (0, 0), colspan=5, rowspan=10, projection='polar')

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])

# plot paths for t=0 (these are all at the earthquake
t=0
for p in range(len(save_paths)):
    dists_collected=save_paths[p,0]
    depths_collected=save_paths[p,1]
    front_dist= dists_collected[:,t] # Cut at single time across all paths
    front_depth = depths_collected[:, t] # Cut at single time across all paths
    # set colour
    col = ((1-(1.-float(0)/Propagation_time )*color_attenuation[p])+0.5)/1.5
    cols = [col, col,col]
    # plot line towards the right side
    line, = ax.plot(intp(front_dist, 100),radius - intp(front_depth, 100),color =cols )
    lines_right.append(line)
    # mirror line towards the left
    line, = ax.plot(intp(-1.*front_dist, 100),radius - intp(front_depth, 100),color =cols)
    lines_left.append(line)

# add discontinuities
# discons = rays.model.s_mod.v_mod.get_discontinuity_depths()
discons = np.array([   0.  ,  35. ,  210. , 2891.5, 5153.5, 6371. ])
ax.set_yticks(radius - discons)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())


# Fill in Earth colors:
theta = np.arange(0, 2, (1./6000))*np.pi
discons_plot=np.full((len(theta),len(discons)),radius-discons)

# Lith:
plt.fill_between(theta, discons_plot[:,0],discons_plot[:,2], color=(.4, .35, .34), alpha=0.4, lw=0)
# Mantle
plt.fill_between(theta, discons_plot[:,2],discons_plot[:,3], color=(.64, .11, .12), alpha=0.4, lw=0)
# Outer core:
plt.fill_between(theta, discons_plot[:,3],discons_plot[:,4], color=(.91, .49, .27), alpha=0.4, lw=0)
# Inner core:
plt.fill_between(theta, discons_plot[:,4],discons_plot[:,5], color=(.96, .91, .56), alpha=0.4, lw=0)



# Pretty earthquake marker.
eq_symbol, = ax.plot([0], [radius - depth_earthquake],
                    marker="*", color="#FEF215", markersize=20, zorder=10,
                    markeredgewidth=1.5, markeredgecolor="0.3",
                    clip_on=False)


# Add seismometer location
seismom_symbol, = ax.plot([epi_dist*np.pi/180], [radius+400],
                        marker=(3, 0, (60-epi_dist)), color='r', markersize=15, zorder=10,
                        markeredgewidth=1.5, markeredgecolor="0.3",
                        clip_on=False)
# Label Earthquake
plt.annotate("Earthquake!", # this is the text
             (0, radius - depth_earthquake), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(-10,10), # distance from text to points (x,y)
             ha='right',
             fontsize=12) # horizontal alignment can be left, right or center


# Label Seismometer
plt.annotate("Seismometer", # this is the text
             (epi_dist*np.pi/180, radius), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(10,10), # distance from text to points (x,y)
             ha='left',
             # rotation=(-epi_dist),
             fontsize=12) # horizontal alignment can be left, right or center
             
             
ax.set_rmax(radius)
ax.set_rmin(0.0)

######################################################################

# Check if synthetic seismogram is present
synthetic_present=gs.check_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,Time_window=Propagation_time, Out_loc=Output_Location)

if synthetic_present:
    # Just go ahead and read it in
    synth_BXZ=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,Out_loc=Output_Location)
    
else:
    # Call gen_seis function
    print('Calling synthetic seismogram generation')
    gs.generate_seismogram(epi_dist=epi_dist,evtdepth=depth_earthquake,Time_window=Propagation_time,Norm_Wave=Normalise_Waveform,Filt_Wave=Filter_Waveform,Out_loc=Output_Location)
    
    # Now read it in
    synth_BXZ=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,Out_loc=Output_Location)


######################################################################

# Collect info about seismogram
seis_times = synth_BXZ[0].times()
seis_data  = synth_BXZ[0].data
delta      = synth_BXZ[0].stats['delta']
npts       = synth_BXZ[0].stats['npts']
max_amp    = np.ceil(np.max(seis_data))  + 0.1
min_amp    = np.floor(np.min(seis_data)) - 0.1


# Specific details of seismogram window and initiate subplot
iter=0
TW_duration=300                                             # Seismogram plot window length (s)
tick_pointer_width=20                                       # drawing tick length (s)

# Create buffer arrays - width of TW_duration to pad start of seismogram.
time_buffer         = np.arange(-TW_duration,0,delta)
seis_buffer         = np.zeros(len(time_buffer))
# Add buffer to start of seismogram
seis_times_new      = np.concatenate([time_buffer, seis_times])
seis_data_new       = np.concatenate([seis_buffer, seis_data])

seis_times_cut      = seis_times_new[0:round(TW_duration/delta):1]
seis_plot_time      = np.arange(0,TW_duration,delta)

ax1 = plt.subplot(1, 2, 2)
# ax1 = plt.subplot2grid((10, 10), (1, 6), colspan=5, rowspan=8)

ax1.title.set_size(16)
ax1.title.set_text('Seismograph')


# Set seismogram axes as tick pointer width plus TW duration. min->max amp.
plt.gca().set_xlim([-tick_pointer_width,TW_duration])
plt.gca().set_ylim([min_amp,max_amp])
plt.yticks([])                                               # Hides y-axis labels

# Static minute labelling of x-ticks
# plt.xlabel('Time before present (min)', fontsize=10)
# plt.xticks(seis_plot_time[0::60/delta], [int(i) for i in seis_plot_time[0::60/delta]/60 ] )

# No x-ticks
# plt.xticks([])                                               # Hides x-axis labels

# Things below here are those that change with time.
# These will need to be in the animate function.

# Dynamic x-tick labelling.
plt.xlabel('Time after Earthquake (min)', fontsize=12)
x_label_pos = seis_plot_time[round((divmod(iter,60)[1])/delta)::round(60/delta)] 
x_label_val = [ int(np.floor(i)) for i in seis_times_new[round((60+iter)/delta):round((TW_duration/delta)+(iter/delta))+1:round(60/delta)]/60 ][::-1]
plt.xticks(x_label_pos, x_label_val )

# Cut the seismogram up into the correct length
seis_data_cut       = seis_data_new[0+round(iter/delta):round((TW_duration/delta)+(iter/delta)):1]

# "Drawing tick" goes from left side of page up until 1s before start.
tick_x=[-tick_pointer_width, -1]
tick_y=[seis_data_cut[-1],seis_data_cut[-1]]

drawing_tick, = ax1.plot(tick_x ,tick_y,'b-', linewidth=2) 

# Puts triangle at end of drawing tick
triangle_tick, = ax1.plot(-5, seis_data_cut[-1], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
                        markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)

# Think the seismogram need to be flipped, and then plotted
seis, = ax1.plot(seis_plot_time, seis_data_cut[::-1],'r-', linewidth=1)

# Adds timing counter
ax1.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Minutes after Earthquake: '+str(int(np.floor(iter))), ha="right", va="top",
                        fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

# # Adds label for waiting arriving earthquakes waves....
# plt.annotate('Earthquake waves arriving ', (0, min_amp+0.05), ha="left", va="bottom",
#             fontsize=12, color='black')



#####################################################################

frame_number    = Propagation_time
frame_rate      = 25 # fps
gif_dpi         = 100 # Dots per inch of final gif. DOESNT seem to work!
count           = 0 # counter to track how long a text box should appear for
shake_ampl      = 8 # Ampltiude of shaking in kilometers radius.

def animate(t, lines_left, lines_right):
    '''
        Function updates lines with time
    '''
    global save_paths
    global count, currenttextbox, boxes, arrival_times

    for l,line in enumerate(lines_right):
        dists_collected=save_paths[l,0]
        depths_collected=save_paths[l,1]
        front_dist= dists_collected[:,t]
        front_depth = depths_collected[:, t]
        # update line to the right
        line.set_xdata(intp(front_dist,100))
        line.set_ydata(radius - intp(front_depth,100))
        # mirror update for lines to left
        lines_left[l].set_xdata(intp(-1.*front_dist,100))
        lines_left[l].set_ydata(radius - intp(front_depth,100))
        # update colour
        col = ((1-(1.-float(t)/Propagation_time )*color_attenuation[l])+0.5)/1.5
        cols = [col, col,col]
        line.set_color(cols)
        lines_left[l].set_color(cols)

    print('Time step calculated: '+str(t))

    # For each step we want to check if t is odd or even so that we can shake the eartquake and labels
    if t % 2 == 0:
        shake_mod = shake_ampl        # t is even
    else:
        shake_mod = -shake_ampl        # t is odd

    # We only want the earthquake to shake for a minute and the seismometer to begin shaking after the first arrival.

    if t < 60:
        quake_shake_mod = shake_mod
    else:
        quake_shake_mod = 0

    # if t > F_A_time and t < Propagation_time:
    if t in shake_seis:
        seis_shake_mod = shake_mod/2
    else:
        seis_shake_mod = 0
        

    # Pretty earthquake marker.
    eq_symbol.set_data([0], [radius - depth_earthquake + quake_shake_mod])

    # Add seismometer location
    seismom_symbol.set_data([epi_dist*np.pi/180], [radius + 400 + seis_shake_mod])
    

    # Think the seismogram need to be flipped, and then plotted
    # seis, = ax1.plot(seis_plot_time, seis_data_cut[::-1],'r-', linewidth=1)

    seis_data_cut       = seis_data_new[0+round(t/delta):round((TW_duration/delta)+(t/delta)):1]
    seis.set_data(seis_plot_time, seis_data_cut[::-1]) # updating seismogram

    # "Drawing tick" goes from left side of page up until 1s before start.
    tick_x=[-tick_pointer_width, -1]
    tick_y=[seis_data_cut[-1],seis_data_cut[-1]]

    # drawing_tick, = ax1.plot(tick_x ,tick_y,'b-', linewidth=2)
    drawing_tick.set_data(tick_x, tick_y)

    triangle_tick.set_data(-5, seis_data_cut[-1])
    # Puts triangle at end of drawing tick
    # triangle_tick, = ax1.plot(-5, seis_data_cut[-1], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
    #                         markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)

    # Adds timing counter
    ax1.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Minutes after Earthquake: '+str(int(np.floor(t/60))), ha="right", va="top",
                            fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

    # # Adds label for waiting arriving earthquakes waves....
    # # if t < F_A_time:
    # wait_rem=t % 4
    # wait_point='.'
    # waiting=wait_rem*wait_point
    # # print('Earthquake waves arriving '+str(waiting))
    # ax1.text(0, min_amp+0.05, 'Earthquake waves arriving '+str(waiting), ha="left", va="bottom",fontsize=12, color='black')

    # Dynamic x-tick labelling.
    plt.xlabel('Time after Earthquake (min)', fontsize=12)
    x_label_pos = seis_plot_time[round((divmod(t,60)[1])/delta)::round(60/delta)] 
    x_label_val = [ int(np.floor(i)) for i in seis_times_new[round((60+t)/delta):round((TW_duration/delta)+(t/delta))+1:round(60/delta)]/60 ][::-1]
    plt.xticks(x_label_pos, x_label_val )


    return(line,eq_symbol,seismom_symbol,seis,drawing_tick,triangle_tick)

    
# plt.tight_layout()

# Sets up animation
animation = FuncAnimation(
                          # Your Matplotlib Figure object
                          fig,
                          # The function that does the updating of the Figure
                          animate,
                          # Frame information (here just frame number)
                          frame_number,
                          # Extra arguments to the animate function
                          fargs=[lines_left, lines_right],
                          # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
                          interval=1000/frame_rate
                          )

# to save as GIF :
animation.save(Filename_GIF, writer=PillowWriter(fps=frame_rate), dpi=gif_dpi)

