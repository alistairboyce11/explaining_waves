# -*- coding: utf-8 -*-
#############################################################################
### COMPUTES RAY PATHS AND TRAVEL TIMES FOR DIFFERENT BODY PHASES ##########
#############################################################################
'''
    ########################## SET PARAMETERS HERE #############################

    epi_dist = epi_dist                             # Epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed

    theta_earthquake = theta_earthquake             # Angular anticlockwise rotation of earthquake and rest of plot from North

    depth_earthquake = depth_earthquake                    # depth of earthquake in km

    propagation_time = propagation_time                  # Propagation time and seismogram length (s) - up to 3600s

    seis_channel=seis_channel                      # Seismogram channel to use for seismograph, BXZ, BXR, BXT, Use BXT to remove P waves.

    filter_params=filter_params                     # filter parameters for synthetic seismogram [fmin, fmax]. e.g., [0.02, 0.5]
    
    extra_phases=extra_phases                       # Extra phases to add to the phase dictionary = e.g., ['SKS', 'ScS', 'SKiKS', 'SS', 'SKKS']
    
    overwrite_phase_defaults=overwrite_phase_defaults # Overwrite the default phases in the created dictionary = True/False
    
    phases_to_plot=phases_to_plot                     # List of phases wavefronts to plot = e.g., ['P', 'PcP']
    
    color_attenuation=color_attenuation               # List of attentuation factors for phases = e.g., [1.0, 0.4]
    
    key_phase=key_phase                               # Key phase to plot raypath = e.g., ['P']
    
    output_location=output_location                 # String to locate waveform outputs
    
    gif_name_str=gif_name_str                        # String to name movie = e.g., 'CMB1'

    title=title                                     # Movie title = e.g., 'Inside the Deep Earth'

    load_image=load_image                          # Descriptive image to be plotted at lower middle when text labels show.

    LL_L1_text='Label for waves L1'                # Layer 1 text for LHS wavefront plot

    LL_L2_text='Label for waves L2'                # Layer 2 text for LHS wavefront plot

    LR_L1_text='Label for seismogram L1'           # Layer 1 text for RHS seismogram plot

    LR_L2_text='Label for seismogram L2'           # Layer 2 text for RHS seismogram plot
    
    mov_pause_times=mov_pause_times             # Times at which to pause movie for 5 seconds
    
    mov_fps=mov_fps                                 # frames per second for the gif
    
    mov_dpi=mov_dpi                                 # Dots per inch for gif. DOESNT seem to work!

'''

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

import sys,glob
import os.path

from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (16, 10),
         'xtick.labelsize':'16',
         'ytick.labelsize':'16'}
pylab.rcParams.update(params)

from pathlib import Path
home = str(Path.home())

# Function used to test the input parameters to movie making function:
import input_params as ip

# Function below used to define input phases.
import phase_finder as pf

# Function used to generate seismogram
import gen_seis as gs

# Function used to setup ploting area.
import setup_plot_area as spa

# velocity model as a function of depth.
model = TauPyModel(model='ak135')

    # Funciton called to make the explaing waves movies.
def mk_mov(epi_dist=30, theta_earthquake=0, depth_earthquake=0, propagation_time=600, seis_channel='BXZ', filter_params=[],
            extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P'], color_attenuation=[1.0], key_phase=['P'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='', title='Inside the Deep Earth', load_image='',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150):

    global save_paths

    ############## Test these input params are suitable ######################

    Filename_GIF= ip.test_input_params(epi_dist=epi_dist, theta_earthquake=theta_earthquake, depth_earthquake=depth_earthquake, 
                        propagation_time=propagation_time, seis_channel=seis_channel, 
                        extra_phases=extra_phases, 
                        phases_to_plot=phases_to_plot, color_attenuation=color_attenuation, key_phase=key_phase, 
                        output_location=output_location, gif_name_str=gif_name_str, title=title, load_image=load_image,
                        LL_L1_text=LL_L1_text, LL_L2_text=LL_L2_text, LR_L1_text=LR_L1_text, LR_L2_text=LR_L2_text,
                        mov_fps=mov_fps,mov_dpi=mov_dpi)

    ############## Plot which phases: ######################


    if not pf.check_dict_present(depth_earthquake=depth_earthquake):
        pf.gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=extra_phases, overwrite_phase_defaults=overwrite_phase_defaults)

    ############### Raypath to plot ######################

    key_phase_A_time=pf.find_arrival_time(depth_earthquake=depth_earthquake, epi_dist=epi_dist, phase_name=key_phase[0])

    ########################## Fixed Parameters #############################

    radius = 6371                                       # radius of Earth in km
    seismometer_shake_duration = 10         # Duration of shaking at the seismometer after the arrival of a plotted phase.

    #######################################################################################

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
        shake_seis.append(np.arange(shake_arr_times_sort[i],shake_arr_times_sort[i]+seismometer_shake_duration,1))
    shake_seis=np.unique(shake_seis)

    ### Show the array containing time steps to shake seismometer.
    # print(shake_seis)

    # Check that propagation time is greater that first arrival time.
    F_A_name, F_A_time = pf.find_first_arrival(depth_earthquake=depth_earthquake, epi_dist=epi_dist)

    if F_A_time > (propagation_time-10):
        print('No phases arriving ......')
        print('Must allow more wave prop. time at '+str(epi_dist)+'deg distance.')
        print('exiting\n')
        sys.exit()
    
    
    #################### Calculate the frames vector ####################################
    # This is a way to dictate when the movie pauses.
    
    mov_pause_length = 5  # Define number of seconds pause for each mov_pause_time
    # Make the frames vector as integer intervals from zero to propagation_time -1
    frames=np.arange(0, propagation_time , 1)
    
    if len(mov_pause_times) > 0:
        # Make frames vector by looping through and adding pauses (repeated frames)
        for i in range(len(mov_pause_times)):
            frames_start=list(frames[0:mov_pause_times[i]])
            frames_pause=[mov_pause_times[i] for j in range(mov_pause_length)]
            frames_end=list(frames[mov_pause_times[i]+1:])
            frames=frames_start+frames_pause+frames_end
        if frames[0] != 0 or frames[-1] != propagation_time-1:
            print('Something wrong with calculation of frames vector')
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


    ################ Wavefront movie #######################
    
    # regular time array in s, 1 s resolution
    time = np.arange(0., propagation_time)
    
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

    # Repeat the above but just calculate for the key phase and the epicentral distance required.
    key_path=[]
    key_dists_collected=[]
    key_depths_collected=[]
    key_ray = model.get_ray_paths(depth_earthquake, epi_dist, phase_list=key_phase)
    # Interpolate to regulard time array
    key_dists = np.interp(time, key_ray[0].path['time'], key_ray[0].path['dist']) #, left = np.nan, right = np.nan
    key_depths = np.interp(time, key_ray[0].path['time'], key_ray[0].path['depth']) #, left = np.nan, right = np.nan
    key_path=np.array([key_dists,key_depths])


    ############################## Start the plotting routine ################################
    #interpolater for plotter
    intp = matplotlib.cbook.simple_linear_interpolation

    # save wave fronts to the left and right
    lines_left=[]
    lines_right=[]

    # ##################### SET UP THE PLOTTING AREA HERE #######################

    # Use this function to setup the intial plot area!
    fig,ax0,axgl,axgm,axgr,axll,axlr,axdi,di_figure,ax1,ax2,ax3 = spa.setup_plot(title=title,load_image=load_image,plot_width=16,plot_height=10, epi_dist=epi_dist, depth_earthquake=depth_earthquake, polar_plot_offset=theta_earthquake, radius=radius)

    # ##########################################################################
    # set polar subplot as current axes
    plt.sca(ax2)

    # plot paths for t=0 (these are all at the earthquake
    t=0
    for p in range(len(save_paths)):
        dists_collected=save_paths[p,0]
        depths_collected=save_paths[p,1]
        front_dist= dists_collected[:,t] # Cut at single time across all paths
        front_depth = depths_collected[:, t] # Cut at single time across all paths
        # set colour
        col = color_attenuation[p] # ((1-(1.-float(0)/propagation_time )*color_attenuation[p])+0.5)/1.5
        cols = [col, col,col]
        # Set alphas - intrinsic amplitude decay : can be scaled:
        alpha_atten=1*np.exp((-1*t)/(2*650))
        # plot line towards the right side
        line, = ax2.plot(intp(front_dist, 100),radius - intp(front_depth, 100),color=cols, alpha=alpha_atten)
        lines_right.append(line)
        # mirror line towards the left
        line, = ax2.plot(intp(-1.*front_dist, 100),radius - intp(front_depth, 100),color=cols, alpha=alpha_atten)
        lines_left.append(line)

    ############################ add discontinuities - not used ##############################
    # discons = rays.model.s_mod.v_mod.get_discontinuity_depths()
    # discons = np.array([   0.  ,  35. ,  210. , 2891.5, 5153.5, 6371. ])
    # discons = np.array([   0., 2891.5, 5153.5, 6371. ])
    # ax2.set_yticks(radius - discons)
    # ax2.xaxis.set_major_formatter(plt.NullFormatter())
    # ax2.yaxis.set_major_formatter(plt.NullFormatter())

    # # Fill in Earth colors:
    # theta = np.arange(0, 2, (1./6000))*np.pi
    # discons_plot=np.full((len(theta),len(discons)),radius-discons)
    #
    # # Lith:
    # plt.fill_between(theta, discons_plot[:,0],discons_plot[:,2], color=(.4, .35, .34), alpha=0.4, lw=0)
    # # Mantle
    # plt.fill_between(theta, discons_plot[:,2],discons_plot[:,3], color=(.64, .11, .12), alpha=0.4, lw=0)
    # # Outer core:
    # plt.fill_between(theta, discons_plot[:,3],discons_plot[:,4], color=(.91, .49, .27), alpha=0.4, lw=0)
    # # Inner core:
    # plt.fill_between(theta, discons_plot[:,4],discons_plot[:,5], color=(.96, .91, .56), alpha=0.4, lw=0)
    #


    # Add the first point of the key ray path
    key_ray_path, = ax2.plot(key_path[0,0:t],radius - key_path[1,0:t],'b-', linewidth=1)

    # Pretty earthquake marker.
    eq_symbol, = ax2.plot([0], [radius - depth_earthquake],
                        marker="*", color="#FEF215", markersize=20, zorder=10,
                        markeredgewidth=1.5, markeredgecolor="0.3",
                        clip_on=False)

    # Add seismometer location
    seismom_symbol, = ax2.plot([epi_dist*np.pi/180], [radius+250],
                            marker=(3, 0, (60-epi_dist+theta_earthquake)), color='r', markersize=15, zorder=10,
                            markeredgewidth=1.5, markeredgecolor="0.3",
                            clip_on=False)

    ax2.set_rmax(radius)
    ax2.set_rmin(0.0)

    ######################################################################

    # Waveform characteristics
    normalise_waveform=True                             # Normalise waveform amplitude

    # Check if synthetic seismogram is present
    synthetic_present=gs.check_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time, out_loc=output_location)

    if synthetic_present:
        # Just go ahead and read it in
        synth=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,out_loc=output_location)
        synth_channel=synth.select(channel=seis_channel)
    else:
        # Call gen_seis function
        print('Calling synthetic seismogram generation')
        gs.generate_seismogram(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time,norm_wave=normalise_waveform,filter_params=filter_params,out_loc=output_location)

        # Now read it in
        synth=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,out_loc=output_location)
        synth_channel=synth.select(channel=seis_channel)

    ######################################################################

    # Collect info about seismogram
    seis_times = synth_channel[0].times()
    seis_data  = synth_channel[0].data
    delta      = synth_channel[0].stats['delta']
    npts       = synth_channel[0].stats['npts']
    max_amp    = np.ceil(np.max(seis_data))  + 0.1
    min_amp    = np.floor(np.min(seis_data)) - 0.1

    # Specific details of seismogram window - set ax3 as current axes
    plt.sca(ax3)

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

    # Set seismogram axes as tick pointer width plus TW duration. min->max amp.
    ax3.set_xlim([-tick_pointer_width,TW_duration])
    ax3.set_ylim([min_amp,max_amp])
    ax3.set_yticks([])                                               # Hides y-axis labels

    # Static minute labelling of x-ticks
    # ax3.set_xlabel('Time before present (min)', fontsize=10)
    # ax3.set_xticks(seis_plot_time[0::60/delta])
    # ax3.set_xticklabels([int(i) for i in seis_plot_time[0::60/delta]/60 ] )

    # No x-ticks
    # ax3.set_xticks([])                                               # Hides x-axis labels

    # Things below here are those that change with time.
    # These will need to be in the animate function.

    # Dynamic x-tick labelling.
    ax3.set_xlabel('Time after Earthquake (min)', fontsize=14)
    x_label_pos = seis_plot_time[round((divmod(iter,60)[1])/delta)::round(60/delta)]
    x_label_val = [ int(np.floor(i)) for i in seis_times_new[round((60+iter)/delta):round((TW_duration/delta)+(iter/delta))+1:round(60/delta)]/60 ][::-1]
    ax3.set_xticks(x_label_pos)
    ax3.set_xticklabels(x_label_val)

    # Cut the seismogram up into the correct length
    seis_data_cut       = seis_data_new[0+round(iter/delta):round((TW_duration/delta)+(iter/delta)):1]

    # "Drawing tick" goes from left side of page up until 1s before start.
    tick_x=[-tick_pointer_width, -1]
    tick_y=[seis_data_cut[-1],seis_data_cut[-1]]

    drawing_tick, = ax3.plot(tick_x ,tick_y,'b-', linewidth=2)

    # Puts triangle at end of drawing tick
    triangle_tick, = ax3.plot(-5, seis_data_cut[-1], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
                            markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)

    # Think the seismogram need to be flipped, and then plotted
    seis, = ax3.plot(seis_plot_time, seis_data_cut[::-1],'r-', linewidth=1)

    # Adds timing counter
    ax3.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Minutes after Earthquake: '+str(int(np.floor(iter))), ha="right", va="top",
                            fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

    # Adds label for waiting arriving earthquakes waves....
    ax3.text(0, min_amp+0.05, 'Earthquake waves arriving', ha="left", va="bottom",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))

    #####################################################################

    frame_number    = propagation_time
    frame_rate      = mov_fps #30 fps
    gif_dpi         = mov_dpi # 150 Dots per inch of final gif. DOESNT seem to work!
    count           = 0 # counter to track how long a text box should appear for
    shake_ampl      = 20 # Ampltiude of shaking in kilometers radius.

    def animate(t, lines_left, lines_right):
        '''
            Function updates lines with time
        '''
        global count

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
            col = color_attenuation[l] # ((1-(1.-float(t)/propagation_time )*color_attenuation[l])+0.5)/1.5
            cols = [col, col,col]
            line.set_color(cols)
            lines_left[l].set_color(cols)
            # Set alphas - intrinsic amplitude decay : can be scaled:
            alpha_atten=1*np.exp((-1*t)/(2*650))
            line.set_alpha(alpha_atten)
            lines_left[l].set_alpha(alpha_atten)
            
            
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

        # if t > F_A_time and t < propagation_time:
        if t in shake_seis:
            seis_shake_mod = shake_mod #/2
            # print('shaking: '+str(seis_shake_mod))
        else:
            seis_shake_mod = 0

        # Pretty earthquake marker.
        eq_symbol.set_data([0], [radius - depth_earthquake + quake_shake_mod])

        # Add seismometer location
        seismom_symbol.set_data([epi_dist*np.pi/180], [radius + 250 + seis_shake_mod])
        if t < key_phase_A_time:
            seismom_symbol.set_color('r')
        else:
            seismom_symbol.set_color('lime')

        # Constant drawing of ray path
        key_ray_path.set_data(key_path[0,0:t],radius - key_path[1,0:t])

        # Think the seismogram need to be flipped, and then plotted
        # seis, = ax3.plot(seis_plot_time, seis_data_cut[::-1],'r-', linewidth=1)

        seis_data_cut       = seis_data_new[0+round(t/delta):round((TW_duration/delta)+(t/delta)):1]
        seis.set_data(seis_plot_time, seis_data_cut[::-1]) # updating seismogram

        # "Drawing tick" goes from left side of page up until 1s before start.
        tick_x=[-tick_pointer_width, -1]
        tick_y=[seis_data_cut[-1],seis_data_cut[-1]]
        drawing_tick.set_data(tick_x, tick_y)

        # Puts triangle at end of drawing tick
        triangle_tick.set_data(-5, seis_data_cut[-1])

        # Adds timing counter
        ax3.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Minutes after Earthquake: '+str(int(np.floor(t/60))), ha="right", va="top",
                                fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

        # Adds label for waiting arriving earthquakes waves....
        if t < F_A_time:
            # Must use bbox to plot so that it overwrites previous text.
            # Text in else condition must be at least as long as longest string in if condition.
            wait_rem=((t - (t//20)*20 ) //5 )+1 # This just slows down the "dot-dot-dot" part when waiting for waves to arrive.
            rem_diff=4-wait_rem
            wait_space=' '
            waiting_gap=wait_space*rem_diff
            wait_point='.'
            waiting=wait_rem*wait_point
            ax3.text(0, min_amp+0.05, 'Earthquake waves arriving '+str(waiting)+str(waiting_gap), ha="left", va="bottom",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
        else:
            ax3.text(0, min_amp+0.05, 'Waves arrived!                               ', ha="left", va="bottom",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))

        # Dynamic x-tick labelling.
        ax3.set_xlabel('Time after Earthquake (min)', fontsize=14)
        x_label_pos = seis_plot_time[round((divmod(t,60)[1])/delta)::round(60/delta)]
        x_label_val = [ int(np.floor(i)) for i in seis_times_new[round((60+t)/delta):round((TW_duration/delta)+(t/delta))+1:round(60/delta)]/60 ][::-1]
        ax3.set_xticks(x_label_pos)
        ax3.set_xticklabels(x_label_val)
        
        
        # This part plots the time dependent appearance of labels and the lower image
        # Layer 1 text - left label
        if len(LL_L1_text) > 0: 
            if t > 0.5*F_A_time:
                axll.text(0.5, 0.5, LL_L1_text, ha="center", va="center",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
        # Layer 2 text - left label
        if len(LL_L2_text) > 0: 
            if t > 0.75*F_A_time:
                axll.text(0.5, 0.0, LL_L2_text, ha="center", va="center",fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
        # Layer 1 text - right label
        if len(LR_L1_text) > 0: 
            if t > 1.25*F_A_time:
                axlr.text(0.5, 0.5, LR_L1_text, ha="center", va="center",fontsize=14, color='black',bbox=dict(facecolor='white',edgecolor='white', pad=1.0)) # Add some labels if you wish
        # Layer 2 text - right label
        if len(LR_L2_text) > 0: 
            if t > 1.25*F_A_time:
                axlr.text(0.5, 0.0, LR_L2_text, ha="center", va="center",fontsize=12, color='black',bbox=dict(facecolor='white',edgecolor='white', pad=1.0)) # Add some labels if you wish

        # Plot descriptive image (di) between the labels.
        if len(di_figure) > 0: 
            if t >= 1*F_A_time:
                axdi.imshow(di_figure, alpha=1)

        return(line,eq_symbol,seismom_symbol,key_ray_path,seis,drawing_tick,triangle_tick)

    # Sets up animation
    animation = FuncAnimation(
                              # Your Matplotlib Figure object
                              fig,
                              # The function that does the updating of the Figure
                              animate,
                              # Vector containing frame numbers
                              # frames=frames,
                              # # Frame information (here just frame number)
                              frame_number,
                              # Extra arguments to the animate function
                              fargs=[lines_left, lines_right],
                              # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
                              interval=1000/frame_rate
                              )

    # to save as GIF :
    animation.save(Filename_GIF, writer=PillowWriter(fps=frame_rate), dpi=gif_dpi)


    return()
