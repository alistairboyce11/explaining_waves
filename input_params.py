'''
This script contains the function that tests input parameters to explaining waves movie:


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

    LL_L1_time = 1                                  # Layer 1 text time for LHS wavefront plot as a function of First arrival time

    LL_L2_time = 1                                  # Layer 2 text time for LHS wavefront plot as a function of First arrival time

    LR_L1_time = 1                                  # Layer 1 text time for RHS seismogram plot as a function of First arrival time

    LR_L2_time = 1                                  # Layer 2 text time for RHS seismogram plot as a function of First arrival time

    mov_pause_times=mov_pause_times             # Times at which to pause movie for 5 seconds

    mov_fps=mov_fps                                 # frames per second for the gif
    
    mov_dpi=mov_dpi                                 # Dots per inch for gif. DOESNT seem to work!

'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
from pathlib import Path
home = str(Path.home())

def test_input_params(epi_dist=30, theta_earthquake=0, depth_earthquake=0, propagation_time=600, seis_channel='BXZ', filter_params=[],
            extra_phases=None, phases_to_plot=['P'], color_attenuation=[1.0], key_phase='P', 
            output_location = '../wavefront_movie_outputs/', gif_name_str='',  title='title', load_image='Lehmann.png',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            LL_L1_time=1.0, LL_L2_time=1.0, LR_L1_time=1.0, LR_L2_time=1.0,
            mov_pause_times=[], mov_fps=30,mov_dpi=150):



    # Tests for input parameters:
    
    if epi_dist < 0 or epi_dist > 180:
        print('Bad epicentral distance for Seismometer')
        sys.exit()
    
    if theta_earthquake > 90 or theta_earthquake < -90:
        print('Bad plot rotation factor - theta_earthquake')
        sys.exit()

    if depth_earthquake < 0 or depth_earthquake > 700:
        print('Bad eq depth - depth_earthquake')
        sys.exit()
        
    if propagation_time < 150 or propagation_time > 3600:
        print('Bad time length for movie - propagation_time')
        sys.exit()

    if not isinstance(seis_channel, str):
        print('Bad seismometer channel, must be a string - seis_channel')
        sys.exit()

    if not seis_channel == 'BXZ' and not seis_channel == 'BXR' and not seis_channel == 'BXT':
        print('Bad seismometer channel selected - seis_channel')
        sys.exit()

    if len(filter_params) > 0:
        if not isinstance(filter_params, list) or len(filter_params) != 2:
            print('Bad specification of filter_params - must be 2 parameter list')
            sys.exit()

    if not extra_phases == None:
        if not isinstance(extra_phases, list):
            print('Bad specification of extra_phases')
            sys.exit()

    if not isinstance(phases_to_plot, list):
        print('Bad specification of phases_to_plot')
        sys.exit()

    if not isinstance(color_attenuation, list) or len(color_attenuation) != len(phases_to_plot):
        print('Bad specification of color_attenuation')
        sys.exit()

    if not isinstance(key_phase, list)  or len(key_phase) != 1:
        print('Bad specification of key_phase - must be list length 1')
        sys.exit()

    if not isinstance(output_location, str):
        print('Bad specification of output_location - must be string')
        sys.exit()
    else:
        if not os.path.exists(output_location):
            os.makedirs(output_location)

    if len(gif_name_str) > 0:
        if not isinstance(gif_name_str, str):
            print('Bad specification of gif_name_str - must be string')            
            sys.exit()
    else:
        gif_name_str='seis_movie_'+str(epi_dist)+'deg'

    Filename_GIF = output_location + gif_name_str + '.gif'
    
    if len(title) > 0:
        if not isinstance(title, str):
            print('Bad specification of title - must be string')
            sys.exit()
    
    if len(load_image) > 0:
        if not isinstance(load_image, str):
            print('Bad specification of load_image - must be string')
            sys.exit()
        if not os.path.exists(home + '/Google_Drive/GITHUB_AB/wavefront_movie_images/' + load_image):
            print('Bad specification of load_image - path does NOT exist')
            sys.exit()

    if len(LL_L1_text) > 0:
        if not isinstance(LL_L1_text, str):
            print('Bad specification of LL_L1_text - must be string')
            sys.exit()
    if len(LL_L2_text) > 0:
        if not isinstance(LL_L2_text, str):
            print('Bad specification of LL_L2_text - must be string')
            sys.exit()
    if len(LR_L1_text) > 0:
        if not isinstance(LR_L1_text, str):
            print('Bad specification of LR_L1_text - must be string')
            sys.exit()
    if len(LR_L2_text) > 0:
        if not isinstance(LR_L2_text, str):
            print('Bad specification of LR_L2_text - must be string')
            sys.exit()

    if not isinstance(LL_L1_time, float):
        print('Bad specification of LL_L1_time - must be float')
        sys.exit()
    if not isinstance(LL_L2_time, float):
        print('Bad specification of LL_L2_time - must be float')
        sys.exit()
    if not isinstance(LR_L1_time, float):
        print('Bad specification of LR_L1_time - must be float')
        sys.exit()
    if not isinstance(LR_L2_time, float):
        print('Bad specification of LR_L2_time - must be float')
        sys.exit()

    if len(mov_pause_times) > 0:
        if not isinstance(mov_pause_times, list):
            print('Bad specification of mov_pause_times - must be list')
            sys.exit()

    if not isinstance(mov_fps, int):
        print('Bad specification of mov_fps - must be int')
        sys.exit()

    if not isinstance(mov_dpi, int):
        print('Bad specification of mov_dpi - must be int')
        sys.exit()

    print('Input parameters passed testing.....')

    return(Filename_GIF)

