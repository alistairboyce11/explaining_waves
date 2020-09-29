# -*- coding: utf-8 -*-
#############################################################################
### COMPUTES RAY PATHS AND TRAVEL TIMES FOR DIFFERENT BODY PHASES ##########
#############################################################################
'''
    ########################## SET PARAMETERS HERE #############################

    propagation_time = propagation_time                  # Propagation time and seismogram length (s) - up to 3600s

    output_location=output_location                 # String to locate waveform outputs
    
    mov_name_str=mov_name_str                        # String to name movie = e.g., 'CMB1'

    mov_fps=mov_fps                                 # frames per second for the mov
    
    mov_dpi=mov_dpi                                 # Dots per inch for mov.
'''

### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt

import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.collections import PatchCollection
import matplotlib.patches as patches

# from matplotlib.animation import PillowWriter
# More about the obspy routines we are using can be found here:

import sys,glob
import os.path

from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
          'figure.figsize': (12.8, 7.2),
         'xtick.labelsize':'14',
         'ytick.labelsize':'14'}
pylab.rcParams.update(params)

matplotlib.font_manager._rebuild()
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Lato'



# Function used to setup ploting area.
import setup_plot_area as spa

    # Funciton called to make the explaing waves movies.
def mk_mov(propagation_time=20, output_location='./', mov_name_str='Core_Diff', mov_label='Core Diffraction',
           mov_fps=1, mov_dpi=150):
    Filename_MOV = output_location + mov_name_str + '.mp4'
    #################### Calculate the frames vector ####################################
    # This is a way to dictate when the movie pauses.
    
    # mov_pause_length = 30 # * mov_fps  # Define number of seconds pause for each mov_pause_time
    # Make the frames vector as integer intervals from zero to propagation_time -1
    # This must be a generator function that is passed to funcanimation below

    frames=np.arange(0, propagation_time , 1)
	
    # ##################### SET UP THE PLOTTING AREA HERE #######################

    # Use this function to setup the intial plot area!
    fig,ax0,ax1,ax2 = spa.setup_plot(plot_width=12.8, plot_height=7.2)

    # ##########################################################################
    # set polar subplot as current axes
    plt.sca(ax2)

    # plot paths for t=0 (these are all at the earthquake)
    t=0
    ax2.text(0.5,0.75, 'Next Video:', ha="center", va="bottom",fontsize=14, color='black',fontweight='semibold')
    ax2.text(0.5,0.5, '"'+str(mov_label)+'"', ha="center", va="bottom",fontsize=16, color='black',fontweight='bold')
	
    # Adds timing counter
    timing_counter = ax2.text(0.5,0.25, 'Time to video: '+str(int(20-t))+'s', ha="center", va="bottom",fontsize=14, color='black',fontweight='semibold')
    #
    #####################################################################

    frame_number    = propagation_time
    frame_rate      = mov_fps #30 fps
    mov_dpi         = mov_dpi # 150 Dots per inch of final mov. DOESNT seem to work!

    def animate(t):
        '''
            Function updates lines with time
        '''

        print('Time step calculated: '+str(t))

        # Adds timing counter
        timing_counter.set_text('Time to video: '+str(int(20-t))+'s')

        return()
            
    # Sets up animation
    animation = FuncAnimation(
                              # Your Matplotlib Figure object
                              fig,
                              # The function that does the updating of the Figure
                              animate,
                              # Vector containing frame numbers
                              frames,
                              # Frame information - generator function
                              # frames=gen_function(),
                              # Extra arguments to the animate function
                              # fargs=[lines_left, lines_right],
                              # The number of values from frames to cache:
                              save_count=propagation_time,
                              # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
                              interval=1000/frame_rate,
                              repeat=False,
                              )

    # to save as MP4 :
    Writer = matplotlib.animation.writers['ffmpeg']
    animation.save(Filename_MOV, writer=Writer(fps=frame_rate), dpi=mov_dpi)


    return()
