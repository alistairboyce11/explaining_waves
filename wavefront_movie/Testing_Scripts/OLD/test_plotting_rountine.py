# -*- coding: utf-8 -*-
#############################################################################
### COMPUTES RAY PATHS AND TRAVEL TIMES FOR DIFFERENT BODY PHASES ##########
#############################################################################


### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec

# Obspy is a seismic toolkit
# import obspy
# from obspy.taup import TauPyModel
# from obspy.taup import plot_travel_times
# from obspy.taup import plot_ray_paths

import matplotlib
from matplotlib import transforms as tf
from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')

# velocity model as a function of depth.
# model = TauPyModel(model='ak135')

########################## SET PARAMETERS HERE #############################

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist = 60

# Angular anticlockwise rotation of earthquake and rest of plot from North
theta_earthquake = -30

# depth of earthquake in km
depth_earthquake = 0

radius = 6371                                       # radius of Earth in km

fig = plt.figure(figsize =(16,10))
st = fig.suptitle("Inside the Deep Earth", fontsize=20)

################ First plot the model in the background. #################

# #create axes in the background to show cartesian image
ax0 = fig.add_subplot(121, label="Background Figure")
im='../../wavefront_movie_home_screen/Model_graphics_vector_final_V2.png'
background_figure = plt.imread(im)
# ax0 = plt.subplot2grid((10, 16), (1, 1), colspan=6, rowspan=7)
# ax0.set_facecolor('none')
ax0.imshow(background_figure, alpha=0.5)
ax0.axis("off")

##########################################################################

# define polar subplot
# ax1 = plt.subplot2grid((10, 16), (1, 1), colspan=6, rowspan=7, polar=True)
ax1 = fig.add_subplot(121, polar=True, label="Polar axes", alpha=0.5)
ax1.set_theta_zero_location('N', offset=theta_earthquake)
ax1.set_facecolor('none')
ax1.set_theta_direction(-1)
ax1.set_xticks([])
ax1.set_yticks([])


# add discontinuities
discons = np.array([   0.  ,  35. ,  210. , 2891.5, 5153.5, 6371. ])
# ax.set_yticks(radius - discons)
# ax.xaxis.set_major_formatter(plt.NullFormatter())
# ax.yaxis.set_major_formatter(plt.NullFormatter())

#
# # Fill in Earth colors:
# theta = np.arange(0, 2, (1./6000))*np.pi
#
# discons_plot=np.full((len(theta),len(discons)),radius-discons)
#
# # Lith:
# plt.fill_between(theta, discons_plot[:,0],discons_plot[:,2], color=matplotlib.colors.to_hex((.4, .35, .34)), alpha=0.4, lw=0)
# # Mantle
# plt.fill_between(theta, discons_plot[:,2],discons_plot[:,3], color=matplotlib.colors.to_hex((.64, .11, .12)), alpha=0.4, lw=0)
# # Outer core:
# plt.fill_between(theta, discons_plot[:,3],discons_plot[:,4], color=matplotlib.colors.to_hex((.91, .49, .27)), alpha=0.4, lw=0)
# # Inner core:
# plt.fill_between(theta, discons_plot[:,4],discons_plot[:,5], color=matplotlib.colors.to_hex((.96, .91, .56)), alpha=0.4, lw=0)
#

# Pretty earthquake marker.
eq_symbol, = ax1.plot([0], [radius - depth_earthquake],
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
seismom_symbol, = ax1.plot([epi_dist*np.pi/180], [radius+400],
                        marker=(3, 0, (60-epi_dist+theta_earthquake)), color='r', markersize=15, zorder=10,
                        markeredgewidth=1.5, markeredgecolor="0.3",
                        clip_on=False)

# Label Seismometer
plt.annotate("Seismometer", # this is the text
             (epi_dist*np.pi/180, radius), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(10,-10), # distance from text to points (x,y)
             ha='left',
             # rotation=(-epi_dist),
             fontsize=12) # horizontal alignment can be left, right or center


ax1.set_rmax(radius)
ax1.set_rmin(0.0)

TW_duration=300                                             # Sesimogram window length (s)
tick_pointer_width=20                                       # drawing tick length (s)

ax2 = fig.add_subplot(122, label="Seismograph")
# ax2 = plt.subplot2grid((10, 16), (1, 9), colspan=8, rowspan=7)
ax2.title.set_size(16)
ax2.title.set_text('Seismograph')
time = np.arange(0, TW_duration, 1);

t_after_eq=time[0]

amplitude   = np.exp(-time/100) * np.sin(time/TW_duration/np.pi*180)
ax2.plot(time, amplitude,'r-', linewidth=1)

max_amp    = np.ceil(np.max(amplitude))
min_amp    = np.floor(np.min(amplitude))

plt.gca().set_xlim([-tick_pointer_width,TW_duration])
plt.gca().set_ylim([min_amp,max_amp])

# "Drawing tick" goes from left side of page up until 1s before start.
tick_x=[-tick_pointer_width, -1]
tick_y=[amplitude[0],amplitude[0]]

plt.yticks([])                                               # Hides y-axis labels
# plt.xticks([])                                               # Hides x-axis labels

# plt.xticks(time[0::60], [int(i) for i in time[0::60]/60 ] )
# plt.xlabel('Time before present (min)', fontsize=10)


ax2.plot(tick_x ,tick_y,'b-', linewidth=2) 

# Puts triangle at end of drawing tick
ax2.plot(-5, amplitude[0], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
        markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)
        
ax2.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Time after Earthquake: '+str(t_after_eq)+'s', ha="right", va="top",
        fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

wait_rem=3
wait_point='.'
waiting=wait_rem*wait_point

# # Adds label for waiting arriving earthquakes waves....
ax2.text(0, min_amp+0.05, 'Earthquake waves arriving '+str(waiting), ha="left", va="bottom",
                        fontsize=12, color='black')
                        
                        
# # Place white space padding around the plots
# # Axes to add labels below plot #2
# ax2b = plt.subplot2grid((10, 16), (8, 9), colspan=8, rowspan=2)
# ax2b.set_facecolor('red')
# ax2b.set_xticks([])
# ax2b.set_yticks([])
# # ax2b.axis("off")

# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=1)
# plt.tight_layout()

plt.show()




