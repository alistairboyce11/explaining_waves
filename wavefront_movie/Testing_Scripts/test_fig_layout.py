
### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt



import matplotlib
from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
# import matplotlib.patches as patches

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
          'figure.figsize': (12.8, 7.2),
         'xtick.labelsize':'14',
         'ytick.labelsize':'14'}
pylab.rcParams.update(params)
from matplotlib.collections import PatchCollection
import matplotlib.patches as patches

import sys
sys.path.append('../')

# Function used to setup ploting area.
import setup_plot_area as spa

########################## SET PARAMETERS HERE #############################

# depth of earthquake in km
depth_earthquake = 0

radius = 6371                                       # radius of Earth in km

title = 'Movie title'


# epi_dist=70
# theta_earthquake=50
# LL_L1_text='Earthquake waves travel outwards in all\n directions from where an earthquake happens'
# LL_L2_text='These waves can tell us about the material\n they travel through on their journey'
# LR_L1_text='\"I look at the time it takes for P waves to\n arrive back at the Earth’s surface\"'
# LR_L2_text='\"I image where the mantle is hotter or colder\n by measuring the variable speeds of the waves\"'
# load_image='Cartoons/Al_from_group_name.png'

# epi_dist=60
# theta_earthquake=-32
# LL_L1_text='S-waves are one type of wave that travel\n outwards in all directions from an earthquake'
# LL_L2_text='They bounce off the core-mantle boundary,\n and are sensitive to the structure\n in the deep mantle'
# LR_L1_text='\"I look for these core-bouncing waves\n in the seismogram\"'
# LR_L2_text='\"I use the shape of the waves to investigate\n deep mysterious structures\n like mantle plume anchors\"'
# load_image='Cartoons/Jenny_from_group_name.png'

# epi_dist=145
# theta_earthquake=-18
# LL_L1_text='Some energy leaves the earthquake\n and arrives at the core at a special angle'
# LL_L2_text='At this specific angle the wave \'hugs\' the\n edge of the core - this is called wave diffraction'
# LR_L1_text='\"I search for core \'hugging\' waves\n in the seismogram\"'
# LR_L2_text='\"I locate the mantle plume anchors that cause\n these waves to arrive from unexpected directions\"'
# load_image='Cartoons/Zhi_from_group_name.png'

# epi_dist=100
# theta_earthquake=0
# LL_L1_text='S or transverse waves can only travel\n through a solid and not a liquid'
# LL_L2_text='In 1906, British geologist Richard Oldham\n first noticed that there were no S waves\n beyond a certain distance from earthquakes'
# LR_L1_text='This is called a \'shadow zone\''
# LR_L2_text='This was the first clue to the\n existence of a liquid core!'
# load_image='Oldham.png'

# epi_dist=120
# theta_earthquake=10
# LL_L1_text='P waves traveling through the Earth\n bounce off interior boundaries'
# LL_L2_text='In the 1930s Danish scientist Inge Lehmann\n first recorded an unexpected P-wave arrival\n that came from the inner-core boundary'
# LR_L1_text='She argued the core might be\n changing from a liquid to a solid\n close to the centre of the Earth!'
# LR_L2_text=''
# load_image='Lehmann.png'

epi_dist=179
theta_earthquake=78
LL_L1_text='P waves and S waves are caused\n by all natural earthquakes'
LL_L2_text='The faster traveling P waves take only 20 minutes\n to travel to the opposite side of the Earth!'
LR_L1_text='Sensitive instruments called seismometers\n are used to measure the shaking of the ground\n caused by the earthquake waves at the surface'
LR_L2_text='Waves lose lots of energy as they travel,\n so when they return to the surface\n the movements they cause are less than a millimeter!'
load_image=''


# ##################### SET UP THE PLOTTING AREA HERE #######################

# Use this function to setup the intial plto area!
fig,ax0,axgl,axgm,axgr,axll,axlr,axdi,di_figure,ax1,ax2,ax3,ax4 = spa.setup_plot(title=title,load_image=load_image,image_loc='../../wavefront_movie_images/', background_image_loc='../../wavefront_movie_home_screen/',plot_width=12.8,plot_height=7.2, epi_dist=epi_dist, depth_earthquake=depth_earthquake, polar_plot_offset=theta_earthquake, radius=radius, mirror_key_rp=False)

######################## Additions to plot ax2 - wavefronts #################
# set polar subplot as current axes
plt.sca(ax2)

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


###################### Additions to Cartesian plot for the seismogram #######################################
plt.sca(ax4)

iter=0
delta=0.1
TW_duration=300                                             # Sesimogram window length (s)
tick_pointer_width=20                                       # drawing tick length (s)
time = np.arange(0, TW_duration, 1);
t_after_eq=time[0]
amplitude   = np.exp(-time/100) * np.sin(time/TW_duration/np.pi*180)

ax4.plot(time, amplitude,'r-', linewidth=1)
max_amp    = np.ceil(np.max(amplitude))
min_amp    = np.floor(np.min(amplitude))

ax4.set_xlim([-tick_pointer_width,TW_duration])
ax4.set_ylim([min_amp,max_amp])
# "Drawing tick" goes from left side of page up until 1s before start.
tick_x=[-tick_pointer_width, -1]
tick_y=[amplitude[0],amplitude[0]]
ax4.set_yticks([])                                               # Hides y-axis labels
# ax4.set_xticks([])                                               # Hides x-axis labels


x_label_pos = time[0::60]
x_label_val = [int(i) for i in time[0::60]/60 ]
ax4.set_xticks(x_label_pos)
ax4.set_xticklabels(x_label_val)
ax4.set_xlabel('Time after Earthquake (min)', fontsize=12)

ax4.plot(tick_x ,tick_y,'b-', linewidth=2)

# Puts triangle at end of drawing tick
ax4.plot(-5, amplitude[0], marker=(3, 0, (-90)), color='b', markersize=10, zorder=10,
        markeredgewidth=0.5, markeredgecolor="0.3", clip_on=False)

ax4.text(TW_duration-(TW_duration/40), max_amp-0.05, 'Time after Earthquake: '+str(t_after_eq)+'s', ha="right", va="top",
        fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='grey', pad=5.0))

wait_rem=3
wait_point='.'
waiting=wait_rem*wait_point

# # Adds label for waiting arriving earthquakes waves....
ax4.text(0, min_amp+0.05, 'Earthquake waves arriving '+str(waiting), ha="left", va="bottom",
                        fontsize=12, color='black')



# Set invisible text in place for the key phase labelling.
Key_phase_width=20
key_phase_seis_time_end = Key_phase_width
key_phase_seis_time_start = 0
key_phase_max_amp = 0.5 # np.max(np.abs(seis_data_new[len(time_buffer)+int(np.floor((key_phase_A_time/delta))):len(time_buffer)+int(np.floor((key_phase_A_time + Key_phase_width)/delta)):1]))

rect = patches.Rectangle((key_phase_seis_time_start , -key_phase_max_amp-0.05), Key_phase_width, 2*(key_phase_max_amp+0.05), fill=False,edgecolor='b', alpha=1, visible=False)
# Add collection to axes
phase_box = ax4.add_patch(rect)

phase_label = ax4.text(key_phase_seis_time_end+1, key_phase_max_amp+0.08, 'Wave of interest!', ha="left",va="top",fontsize=12, color='black', visible=False, clip_on=True, bbox=dict(facecolor='white',alpha=0.5,edgecolor='white', pad=0.0)) 

phase_label.set_visible(True)

phase_box.set_visible(True)











if len(LL_L1_text) > 0:
    # Layer 1 text - left label
    axll.text(0.5, 0.7, LL_L1_text, ha="center", va="center",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
if len(LL_L2_text) > 0:
    # Layer 2 text - left label
    axll.text(0.5, 0.1, LL_L2_text, ha="center", va="center",fontsize=12, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
if len(LR_L1_text) > 0:
    # Layer 1 text - right label
    axlr.text(0.5, 0.7, LR_L1_text, ha="center", va="center",fontsize=14, color='black',bbox=dict(facecolor='white',edgecolor='white', pad=1.0)) # Add some labels if you wish
if len(LR_L2_text) > 0:
    # Layer 2 text - right label
    axlr.text(0.5, 0.1, LR_L2_text, ha="center", va="center",fontsize=12, color='black',bbox=dict(facecolor='white',edgecolor='white', pad=1.0)) # Add some labels if you wish

# Plot descriptive image (di) between the labels.
if len(di_figure) > 0:
    axdi.imshow(di_figure, alpha=1)

plt.show()
