'''
This script contains a function that sets up the plotting area:

setup_plot(plot_width=16,plot_height=10, video_name='new video'):
    Returns:    fig = the figure handler required for animate function.
                ax0  = background plot area
                ax1 = cartesian plot that holds the homescreen background
                ax2 = overlying polar plot that will hold the text


'''#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
import os.path

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
          'figure.figsize': (12.8, 7.2),
         'xtick.labelsize':'14',
         'ytick.labelsize':'14'}
pylab.rcParams.update(params)
matplotlib.font_manager._rebuild()
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Lato'


def setup_plot(plot_width=12.8, plot_height=7.2):
    
    fig = plt.figure(figsize =(plot_width,plot_height))
    
    # Add an axes at position rect [left, bottom, width, height] where all quantities are in fractions of figure width and height.

    # ax0 is the background plot that is the area inwhich to plot
    ax0 = fig.add_axes([0, 0, 1, 1], projection=None, polar=False,facecolor='white',frame_on=False)
    # ax0.text(0.01, 0.95, "ax1", size=12) # Add some labels if you wish
    ax0.set_xticks([])
    ax0.set_yticks([])
    
    ################ First plot the model in the background. #################

    # #create axes in the background to show cartesian image
    ax1 = fig.add_axes([0.05, 0.05, 0.95, 0.95], projection=None, polar=False,facecolor='none',frame_on=False)
    # # ax1.text(0.01, 0.95, "ax1", size=12) # Add some labels if you wish
    ax1.set_xticks([])
    ax1.set_yticks([])
    im = 'Explaining_waves_homescreen_COVID_update_2.png'
    background_figure = plt.imread(im)
    ax1.imshow(background_figure, alpha=1)

    ##########################################################################

    # define overlying polar plot that will hold the text
    ax2 = fig.add_axes([0.63, 0.10, 0.25, 0.2], projection=None, polar=False,facecolor='white',frame_on=False)
    ax2.set_xticks([])
    ax2.set_yticks([])
    # ax2.annotate('Next video: '+video_name+' in:', # this is the text
    #              (0, 0), # this is the point to label
    #              textcoords="offset points", # how to position the text
    #              xytext=(0,0), # distance from text to points (x,y)
    #              ha='left;',
    #              va='bottom',
    #              fontsize=12) # horizontal alignment can be left, right or center

    return(fig,ax0,ax1,ax2)
    