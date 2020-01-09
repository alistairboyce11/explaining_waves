'''
This script contains a function that sets up the plotting area:

setup_plot(title='title',plot_width=16,plot_height=10, polar_plot_offset=0):
    Returns:    fig = the figure handler required for animate function.
                ax0  = background plot area
                axgl = Plot axes for left gap between plots - gives space for moving labels.
                axgm = Plot axes for mid gap between plots - gives space for moving labels.
                axgr = Plot axes for right gap between plots - gives space for moving labels.
                axll = Plot axes for label below left plot (wavefronts)
                axlr = Plot axes for label below right plot (seismogram)
                axdi = Plot axes for descriptive image in the lower plot centre
                di_figure = Loaded image for bottom of the plot - usually a png
                ax1 = cartesian plot that holds the background model
                ax2 = overlying polar plot that will hold the wavefronts
                ax3 = Cartesian plot for the seismogram 

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
from pathlib import Path
home = str(Path.home())

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (16, 10),
         'xtick.labelsize':'16',
         'ytick.labelsize':'16'}
pylab.rcParams.update(params)

def setup_plot(title='', load_image='', plot_width=16, plot_height=10, epi_dist=30, depth_earthquake = 0, polar_plot_offset=0, radius=6371):
    
    fig = plt.figure(figsize =(plot_width,plot_height))
    if len(title) > 0:
        st = fig.suptitle(title, fontsize=20)
    
    # Add an axes at position rect [left, bottom, width, height] where all quantities are in fractions of figure width and height.

    # ax0 is the background plot that is the area inwhich to plot
    ax0 = fig.add_axes([0.05, 0.1, 0.9, 0.8], projection=None, polar=False,facecolor='white',frame_on=False)
    # ax0.text(0.01, 0.95, "ax1", size=12) # Add some labels if you wish
    ax0.set_xticks([])
    ax0.set_yticks([])

    # Plot axes for gaps between plots.
    axgl = fig.add_axes([0.05, 0.1, 0.05, 0.8], projection=None, polar=False,facecolor='red',frame_on=False)
    axgl.set_xticks([])
    axgl.set_yticks([])
    axgm = fig.add_axes([0.45, 0.1, 0.10, 0.8], projection=None, polar=False,facecolor='red',frame_on=False)
    axgm.set_xticks([])
    axgm.set_yticks([])
    axgr = fig.add_axes([0.90, 0.1, 0.05, 0.8], projection=None, polar=False,facecolor='red',frame_on=False)
    axgr.set_xticks([])
    axgr.set_yticks([])

    # Plot axes for labels below plots.
    axll = fig.add_axes([0.10, 0.1, 0.35, 0.15], projection=None, polar=False, facecolor='blue',frame_on=False)
     # Add some labels if you wish
    # axll.text(0.5, 0.5, 'Label for waves', ha="center", va="center",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0))
    axll.set_xticks([])
    axll.set_yticks([])
    axlr = fig.add_axes([0.55, 0.1, 0.35, 0.15], projection=None, polar=False, facecolor='blue',frame_on=False)
    # axlr.text(0.5, 0.5, 'Label for seismogram', ha="center", va="center",fontsize=14, color='black', bbox=dict(facecolor='white', edgecolor='white', pad=1.0)) # Add some labels if you wish
    axlr.set_xticks([])
    axlr.set_yticks([])
    
    # Add small axes for the descriptive image in the plot centre - axdi
    axdi = fig.add_axes([0.45, 0.125, 0.10, 0.1], projection=None, polar=False, facecolor='green',frame_on=False)
    axdi.set_xticks([])
    axdi.set_yticks([])
    
    # Load the image that is going in the small axes at the bottom of the plot - usually a png
    if len(load_image) > 0:
        di_loc = home + '/Dropbox/File_Sharing/GITHUB_AB/wavefront_movie_images/' + load_image
        di_figure = plt.imread(di_loc)
    else:
        di_figure=np.array([])
    
    
    ################ First plot the model in the background. #################

    # #create axes in the background to show cartesian image
    ax1 = fig.add_axes([0.10, 0.3, 0.35, 0.6], projection=None, polar=False,facecolor='none',frame_on=False)
    # ax1.text(0.01, 0.95, "ax1", size=12) # Add some labels if you wish
    ax1.set_xticks([])
    ax1.set_yticks([])
    im = home + '/Dropbox/File_Sharing/GITHUB_AB/wavefront_movie_home_screen/Model_graphics_vector_final_V2.png'
    background_figure = plt.imread(im)
    ax1.imshow(background_figure, alpha=1)

    ##########################################################################

    # define overlying polar plot that will hold the wavefronts
    ax2 = fig.add_axes([0.10, 0.3, 0.35, 0.6], projection=None, polar=True,facecolor='none',frame_on=True)
    ax2.set_theta_zero_location('N', offset=polar_plot_offset)
    ax2.set_theta_direction(-1)
    ax2.set_xticks([])
    ax2.set_yticks([])
    

    # Label Earthquake
    
    # Bunch of if statements to get the alignment of Earthquake label correct:
    if polar_plot_offset >= 0:
        # This is anticlockwise rotation of axes.
        horiz_a = 'right'
        offset_text = (-10,10)
    else:
        horiz_a = 'left'
        offset_text = (10,10)
    
    ax2.annotate("Earthquake!", # this is the text
                 (0, radius - depth_earthquake), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=offset_text, # distance from text to points (x,y)
                 ha=horiz_a,
                 va='bottom',
                 fontsize=12) # horizontal alignment can be left, right or center

    # Bunch of if statements to get the alignment of Seismometer label correct:

    if epi_dist-polar_plot_offset < 0:
        # Between -90 and 0
        horiz_a = 'right'
        vert_a = 'bottom'
        offset_text = (-10,10)

    elif epi_dist-polar_plot_offset >= 0 and epi_dist-polar_plot_offset < 90:
        # Between 0 and 90
        horiz_a = 'left'
        vert_a = 'bottom'
        offset_text = (10,10)
    elif epi_dist-polar_plot_offset >= 90 and epi_dist-polar_plot_offset < 180:
        # Between 90 and 180
        horiz_a = 'left'
        vert_a = 'top'
        offset_text = (10,-10)

    # Label Seismometer
    ax2.annotate("Seismometer", # this is the text
                 (epi_dist*np.pi/180, radius), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=offset_text, # distance from text to points (x,y)
                 ha=horiz_a,
                 va=vert_a,
                 fontsize=12) # horizontal alignment can be left, right or center
    
    
    ##################################### Cartesian plot for the seismogram #######################################
    ax3 = fig.add_axes([0.55, 0.3, 0.35, 0.6], projection=None, polar=False,facecolor='white',frame_on=True)
    ax3.title.set_size(16)
    ax3.title.set_text('Seismograph')
    ax3.set_xticks([])
    
    return(fig,ax0,axgl,axgm,axgr,axll,axlr,axdi,di_figure,ax1,ax2,ax3)
    