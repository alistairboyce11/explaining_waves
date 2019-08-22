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
from matplotlib import transforms as tf
from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
import matplotlib.patches as patches

# velocity model as a function of depth.
model = TauPyModel(model='ak135')

########################## SET PARAMETERS HERE #############################

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=20

# depth of earthquake in km
depth_earthquake = 0

radius = 6371                                       # radius of Earth in km

fig = plt.figure(figsize =(10,5))
# define polar subplot
ax = plt.subplot(1,2,1, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])

# add discontinuities
rays = model.get_ray_paths(depth_earthquake, epi_dist, phase_list='P')
discons = rays.model.s_mod.v_mod.get_discontinuity_depths()
ax.set_yticks(radius - discons)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())

# Pretty earthquake marker.
ax.plot([0], [radius - depth_earthquake],
        marker="*", color="#FEF215", markersize=20, zorder=10,
        markeredgewidth=1.5, markeredgecolor="0.3",
        clip_on=False)

# Label Earthquake
plt.annotate("Earthquake!", # this is the text
             (0, radius - depth_earthquake), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(-10,10), # distance from text to points (x,y)
             ha='right',
             fontsize=12) # horizontal alignment can be left, right or center

# Add seismometer location
ax.plot([epi_dist*np.pi/180], [radius+400],
        marker=(3, 0, (60-epi_dist)), color='r', markersize=15, zorder=10,
        markeredgewidth=1.5, markeredgecolor="0.3",
        clip_on=False)

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



TW_duration=300                                             # Sesimogram window length (s)
tick_pointer_width=20                                       # drawing tick length (s)

ax1 = plt.subplot(1, 2, 2)
time = np.arange(0, TW_duration, 1);

t_after_eq=time[0]

amplitude   = np.exp(-time/100) * np.sin(time/TW_duration/np.pi*180)
ax1.plot(time, amplitude,'r-', linewidth=1)

max_amp    = round(np.max(amplitude))
min_amp    = round(np.min(amplitude))


plt.gca().set_xlim([-tick_pointer_width,TW_duration])
plt.gca().set_ylim([min_amp,max_amp])

# "Drawing tick" goes rom left side of page up until 1s before start.
tick_x=[-tick_pointer_width, -1]
tick_y=[amplitude[0],amplitude[0]]


plt.xlabel('Time from present (s)', fontsize=10)
plt.yticks([])                                               # Hides y-axis labels
ax1.plot(tick_x ,tick_y,'b-', linewidth=2) 

# Puts triangle at end of drawing tick
ax1.plot(-5, amplitude[0], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
        markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)
        
ax1.text(TW_duration, max_amp, 'Time after Earthquake: '+str(t_after_eq)+'s', ha="right", va="bottom",
        fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))


plt.show()











