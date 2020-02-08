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
        
    key_phase=key_phase                               # Key phase to plot raypath = e.g., ['P']
    
    output_location=output_location                 # String to locate waveform outputs
    
    mov_name_str=mov_name_str                        # String to name movie = e.g., 'CMB1'

    title=title                                     # Movie title = e.g., 'Inside the Deep Earth'

    load_image=load_image                          # Descriptive image to be plotted at lower middle when text labels show.

    LL_L1_text='Label for waves L1'                # Layer 1 text for LHS wavefront plot

    LL_L2_text='Label for waves L2'                # Layer 2 text for LHS wavefront plot

    LR_L1_text='Label for seismogram L1'           # Layer 1 text for RHS seismogram plot

    LR_L2_text='Label for seismogram L2'           # Layer 2 text for RHS seismogram plot
    
    mov_pause_times=mov_pause_times             # Times at which to pause movie for 5 seconds

    mov_fps=mov_fps                                 # frames per second for the mov
    
    mov_dpi=mov_dpi                                 # Dots per inch for mov. DOESNT seem to work!


'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
sys.path.append('../')
from pathlib import Path
home = str(Path.home())

# Function used to test the input parameters to movie making function:
import input_params as ip


# Funciton called to make the explaing waves movies.
epi_dist=50
theta_earthquake=0
depth_earthquake=0
propagation_time=600
seis_channel='BXZ'
filter_params=[0.02, 0.5] # []
extra_phases=None
overwrite_phase_defaults=False,
phases_to_plot=['P']
key_phase=['P']
output_location = '../wavefront_movie_outputs/'
mov_name_str=''
title='Inside the Earthsss'
LL_L1_text='Label for waves L1'
LL_L2_text='Label for waves L2'
LR_L1_text='Label for seismogram L1'
LR_L2_text='Label for seismogram L2'
load_image='Oldham.png'
mov_pause_times=[50, 100]
mov_fps=30
mov_dpi=150


    ############## Test these input params are suitable ######################

Filename_MOV= ip.test_input_params(epi_dist=epi_dist, theta_earthquake=theta_earthquake, depth_earthquake=depth_earthquake, 
                    propagation_time=propagation_time, seis_channel=seis_channel, filter_params=filter_params,
                    extra_phases=extra_phases, 
                    phases_to_plot=phases_to_plot, key_phase=key_phase, 
                    output_location=output_location, mov_name_str=mov_name_str, title=title, load_image=load_image, 
                    LL_L1_text=LL_L1_text, LL_L2_text=LL_L2_text, LR_L1_text=LR_L1_text, LR_L2_text=LR_L2_text,
                    mov_pause_times=mov_pause_times, mov_fps=mov_fps, mov_dpi=mov_dpi)

print(Filename_MOV)