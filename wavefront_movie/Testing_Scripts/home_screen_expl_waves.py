# -*- coding: utf-8 -*-

#############################################################################
# Script to plot a homescreen that explains the Explaining Waves movie.
#############################################################################

### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt
# Obspy is a seismic toolkit
# import obspy
# from obspy.taup import TauPyModel
# from obspy.taup import plot_travel_times
# from obspy.taup import plot_ray_paths

import matplotlib
# from matplotlib.animation import FuncAnimation
# from matplotlib.animation import PillowWriter
# More about the obspy routines we are using can be found here:
# https://docs.obspy.org/packages/obspy.taup.html

import sys,glob
import os.path
# from IPython.display import HTML, Image
# matplotlib.rc('animation', html='html5')
# import matplotlib.patches as patches

# Function below used to define input phases.
# import phase_finder as pf

# Function used to generate seismogram
# import gen_seis as gs

# velocity model as a function of depth.
# model = TauPyModel(model='ak135')

########################## Fixed Parameters #############################

radius = 6371                                       # radius of Earth in km
depth_earthquake = 0                    # depth of earthquake in km
epi_dist = 25                             # Epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed

# https://docs.obspy.org/tutorial/code_snippets/travel_time.html


# start plot for t= 0
fig = plt.figure(figsize =(10,5))
# fig = plt.figure(figsize =(20,11)) # Probably want this for final graphics....?

# define polar subplot
ax = plt.subplot(1,2,1, polar = True)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)


# add discontinuities
# discons = rays.model.s_mod.v_mod.get_discontinuity_depths()
discons = np.array([   0.  ,  35. ,  210. , 2891.5, 5153.5, 6371. ])
ax.set_yticks(radius - discons)
ax.set_xticks(np.array([-35,35]))

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

######################################################################

# Pretty earthquake marker.
eq_symbol, = ax.plot([-epi_dist*np.pi/180], [radius - depth_earthquake],
                    marker="*", color="#FEF215", markersize=20, zorder=10,
                    markeredgewidth=1.5, markeredgecolor="0.3",
                    clip_on=False)


# Add seismometer location
seismom_symbol, = ax.plot([epi_dist*np.pi/180], [radius+100],
                        marker=(3, 0, (60-epi_dist)), color='r', markersize=15, zorder=10,
                        markeredgewidth=1.5, markeredgecolor="0.3",
                        clip_on=False)
# Label Earthquake
ax.annotate("Earthquake!", # this is the text
             (-epi_dist*np.pi/180, radius - depth_earthquake), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(-10,10), # distance from text to points (x,y)
             ha='right',
             fontsize=12) # horizontal alignment can be left, right or center


# Label Seismometer
ax.annotate("Seismometer", # this is the text
             (epi_dist*np.pi/180, radius), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(10,10), # distance from text to points (x,y)
             ha='left',
             # rotation=(-epi_dist),
             fontsize=12) # horizontal alignment can be left, right or center
             
             
ax.set_rmax(radius)
ax.set_rmin(0)
ax.set_thetamax(35)
ax.set_thetamin(-35)


######################################################################

# Specific details of seismogram window and initiate subplot
iter=0
TW_duration=300                                             # Seismogram plot window length (s)
tick_pointer_width=20                                       # drawing tick length (s)

# # Create buffer arrays - width of TW_duration to pad start of seismogram.
# time_buffer         = np.arange(-TW_duration,0,delta)
# seis_buffer         = np.zeros(len(time_buffer))
# # Add buffer to start of seismogram
# seis_times_new      = np.concatenate([time_buffer, seis_times])
# seis_data_new       = np.concatenate([seis_buffer, seis_data])
#
# seis_times_cut      = seis_times_new[0:round(TW_duration/delta):1]
# seis_plot_time      = np.arange(0,TW_duration,delta)

ax1 = plt.subplot(1, 2, 2)

# Set seismogram axes as tick pointer width plus TW duration. min->max amp.
plt.gca().set_xlim([-tick_pointer_width,TW_duration])
plt.gca().set_ylim([-1,1])
plt.yticks([])                                               # Hides y-axis labels

# Static minute labelling of x-ticks
# plt.xlabel('Time before present (min)', fontsize=10)
# plt.xticks(seis_plot_time[0::60/delta], [int(i) for i in seis_plot_time[0::60/delta]/60 ] )

# No x-ticks
# plt.xticks([])                                               # Hides x-axis labels

delta=0.1

# Dynamic x-tick labelling.
plt.xlabel('Time after Earthquake (min)', fontsize=10)
# x_label_pos = [round((divmod(iter,60)[1])/delta)::round(60/delta)]
# x_label_val = [ int(np.floor(i)) for i in seis_times_new[round((60+iter)/delta):round((TW_duration/delta)+(iter/delta))+1:round(60/delta)]/60 ][::-1]
# plt.xticks(x_label_pos, x_label_val )



# Cut the seismogram up into the correct length
# seis_data_cut       = seis_data_new[0+round(iter/delta):round((TW_duration/delta)+(iter/delta)):1]

# "Drawing tick" goes from left side of page up until 1s before start.
tick_x=[-tick_pointer_width, -1]
tick_y=[0,0]

drawing_tick, = ax1.plot(tick_x ,tick_y,'b-', linewidth=2) 

# Puts triangle at end of drawing tick
triangle_tick, = ax1.plot(-5, 0, marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
                        markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)

# Think the seismogram need to be flipped, and then plotted
# seis, = ax1.plot(seis_plot_time, seis_data_cut[::-1],'r-', linewidth=1)

# Adds timing counter
ax1.text(TW_duration, 1, 'Minutes after Earthquake: '+str(int(np.floor(0))), ha="right", va="bottom",
                        fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

plt.show()


