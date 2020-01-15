'''
This script calls the function to make explaining waves movie:

Movies to be made:

Name		Region		Phases		Distances                       Title:

CMB1		CMB			ScS			60-90                           Investigating the Core Mantle Boundary - 1
CMB2		CMB			P,Pdiff		30-90, 100-159                  Investigating the Core Mantle Boundary - 2
UpMan		Upper Man	P,S			30-95                           Imaging the Mantle 
InC			Inner Core	PKiKP,PKIKP	0-155,116-180                   Detecting the Inner Core
OutC		Outer Core	S,P,PKP,PKIKP	0-100,145-178,116-180       Proving the Outer Core is Liquid
FulWav      Whole Earth All basic   0-180                           Complex Seismic waves!

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
    
    mov_pause_times=mov_pause_times             # Times at which to pause movie for 5 seconds

    mov_fps=mov_fps                                 # frames per second for the gif
    
    mov_dpi=mov_dpi                                 # Dots per inch for gif. DOESN'T seem to work!

'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
# Function used to make movie
import expl_waves_movie as ewm

# P-wave imaging
ewm.mk_mov(epi_dist=70, theta_earthquake=50, depth_earthquake=0, propagation_time=1200, seis_channel='BXZ', filter_params=[],
            extra_phases=['PP', 'PKKP', 'SS', 'SKKS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PKP', 'PKiKP', 'PKIKP', 'PKKP', 'PP'], color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['P'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='P_Tomo', title='Imaging the mantle', load_image='Al.png',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)

# ScS CMB imaging
ewm.mk_mov(epi_dist=80, theta_earthquake=-32, depth_earthquake=0, propagation_time=1800, seis_channel='BXT', filter_params=[],
            extra_phases=['PP', 'PKKP', 'SS', 'SKKS'], overwrite_phase_defaults=False, phases_to_plot=['S', 'ScS', 'SKS', 'SKKS', 'SS', 'SKiKS', 'SKIKS'], color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['ScS'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='ScS_CMB', title='Investigating the Core-Mantle Boundary', load_image='',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)

# Diffraction
ewm.mk_mov(epi_dist=145, theta_earthquake=-18, depth_earthquake=0, propagation_time=1400, seis_channel='BXZ', filter_params=[],
            extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP'], color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['Pdiff'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='Core_Diff', title='Core diffracted waves', load_image='',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)

# Discovery of the Inner Core
ewm.mk_mov(epi_dist=152, theta_earthquake=10, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
            extra_phases=['PP', 'PKKP', 'SS', 'SKKS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PKP', 'PKiKP', 'PKIKP', 'PKKP', 'PP'], color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['PKIKP'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='Disc_IC', title='Detecting the Inner Core', load_image='Lehmann.png',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)

# Liquid Outer Core
ewm.mk_mov(epi_dist=130, theta_earthquake=-18, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
            extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P', 'PKP', 'PKIKP', 'PKiKP', 'S', 'SKS', 'SKIKS', 'SKiKS'], color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['P'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='Disc_OC', title='Proving the Outer Core is Liquid', load_image='Oldham.png',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)
# Full wavefield
ewm.mk_mov(epi_dist=179, theta_earthquake=78, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
            extra_phases=['PP', 'PKKP', 'SS', 'SKKS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'Pdiff', 'PKP', 'PKiKP', 'PKIKP', 'S', 'ScS', 'Sdiff', 'SKS', 'SKiKS', 'SKIKS'], 
            color_attenuation=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], key_phase=['PKIKP'], 
            output_location='../wavefront_movie_outputs/', gif_name_str='Full_Wavefield', title='Complex P and S waves', load_image='',
            LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
            mov_pause_times=[], mov_fps=30, mov_dpi=150)



# Other testing runs

# evm.mk_mov(epi_dist=30, theta_earthquake=0, depth_earthquake=0, propagation_time=600, seis_channel='BXZ', filter_params=[],
#             extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P'], color_attenuation=[1.0], key_phase=['P'],
#             output_location = '../wavefront_movie_outputs/', gif_name_str=[], mov_fps=30,mov_dpi=150)


# ewm.mk_mov(epi_dist=10, theta_earthquake=0, depth_earthquake=0, propagation_time=350, seis_channel='BXZ', filter_params=[],
#             extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['S', 'ScS'], color_attenuation=[1.0, 0.6], key_phase=['S'],
#             output_location='../wavefront_movie_outputs/', gif_name_str='Test_intrinsic_atten', title='Upper Mantle', load_image='Al.png',
#             LL_L1_text='', LL_L2_text='', LR_L1_text='', LR_L2_text='',
#             mov_fps=30, mov_dpi=150)









### TEST 2.0 Jennys CMB movie
# pf.gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=['S', 'SKS', 'ScS', 'SKiKS', 'SS', 'SKKS'], overwrite_phase_defaults=True)
# phases_to_plot=['S', 'SKS', 'ScS', 'SKiKS', 'SS', 'SKKS' ]
# color_attenuation=[1.0, 0.8, 0.6 ,  0.4,     0.6,   0.2  ]

### TEST 1.0
# if not pf.check_dict_present(depth_earthquake=depth_earthquake):
#     pf.gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None, overwrite_phase_defaults=False)
# phases_to_plot = ['P', 'PcP']
# color_attenuation=[1.0, 0.4]

### TEST 2.0
# phases_to_plot = ['P', 'PKiKP', 'PKP', 'PcP', 'Pn']
# color_attenuation=[1.0,  0.5,    0.8 ,  0.3,   0.3]

#### ++++++++ Using phase finder.py +++++++++++ #############
# This gives the most accurate ray propagation but is slow and memory hungry!!!!

# pf.gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=[ 'P', 'PKiKP', 'PKP', 'PcP', 'PP', 'PKIKP', 'Pdiff', 'S', 'SKiKS', 'SKS', 'ScS', 'SS', 'SKIKS', 'Sdiff' ], overwrite_phase_defaults=True)

# phases_to_plot=pf.find_phases_at_dist(depth_earthquake=depth_earthquake, epi_dist=epi_dist)
# color_attenuation = 1 - (np.arange(0,len(phases_to_plot),1)/len(phases_to_plot))
