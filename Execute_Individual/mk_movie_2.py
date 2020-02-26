'''
This script calls the function to make explaining waves movie:

    ########################## SET PARAMETERS HERE #############################

    epi_dist = epi_dist                             # Epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed

    theta_earthquake = theta_earthquake             # Angular anticlockwise rotation of earthquake and rest of plot from North

    depth_earthquake = depth_earthquake                    # depth of earthquake in km

    propagation_time = propagation_time                  # Propagation time and seismogram length (s) - up to 3600s

    seis_channel=seis_channel                      # Seismogram channel to use for seismograph, BXZ, BXR, BXT, Use BXT to remove P waves.

    filter_params=filter_params                     # filter parameters for synthetic seismogram [fmin, fmax]. e.g., [0.02, 0.5]

    extra_phases=extra_phases                       # Extra phases to add to the phase dictionary = e.g., ['SKKS']
    
    overwrite_phase_defaults=overwrite_phase_defaults # Overwrite the default phases in the created dictionary = True/False
    
    phases_to_plot=phases_to_plot                     # List of phases wavefronts to plot = e.g., ['P', 'PcP']
        
    key_phase=key_phase                               # Key phase to plot raypath = e.g., ['P']
    
    mirror_key_rp=mirror_key_rp                      # Mirror the key phase onto opposite hemisphere -  show shadow zone.
    
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
    
    mov_dpi=mov_dpi                                 # Dots per inch for mov

'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
# Function used to make movie
import expl_waves_movie as ewm


### ScS CMB imaging
ewm.mk_mov(epi_dist=60, theta_earthquake=-32, depth_earthquake=0, propagation_time=1800, seis_channel='BXT', filter_params=[],
            extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['S', 'ScS', 'SS'], key_phase=['ScS'], mirror_key_rp=False,
            output_location='../wavefront_movie_outputs/', mov_name_str='ScS_CMB', title='Investigating the Core-Mantle Boundary', load_image='Cartoons/Jenny_from_group_name.png',
            LL_L1_text='S-waves are one type of wave that travel\n outwards in all directions from an earthquake',
            LL_L2_text='They bounce off the core-mantle boundary,\n and are sensitive to the structure\n in the deep mantle',
            LR_L1_text='\"I look for these core-bouncing waves\n in the seismogram\"',
            LR_L2_text='\"I use the shape of the waves to investigate\n deep mysterious structures\n like mantle plume anchors\"',
            LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
            mov_pause_times=[], mov_fps=45, mov_dpi=150)
