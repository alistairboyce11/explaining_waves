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
    
    mov_dpi=mov_dpi                                 # Dots per inch for mov. DOESN'T seem to work!

'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
# Function used to make movie
import expl_waves_movie as ewm




# Other testing runs

# evm.mk_mov(epi_dist=30, theta_earthquake=0, depth_earthquake=0, propagation_time=600, seis_channel='BXZ', filter_params=[],
#             extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P'], key_phase=['P'],
#             output_location = '../wavefront_movie_outputs/', mov_name_str=[], mov_fps=30,mov_dpi=150)

#
ewm.mk_mov(epi_dist=25, theta_earthquake=0, depth_earthquake=0, propagation_time=700, seis_channel='BXZ', filter_params=[],
            extra_phases=None, overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'S', 'ScS'], key_phase=['P'],
            output_location='../wavefront_movie_outputs/', mov_name_str='Test_atten_func', title='Upper Mantle atten', load_image='Al.png',
            LL_L1_text='Hi', LL_L2_text='There', LR_L1_text='Welcome', LR_L2_text='Back',
            LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.25, LR_L2_time=1.5,
            mov_pause_times=[0.5, 0.75, 1.25, 1.5], mov_fps=30, mov_dpi=150)













## P-wave imaging
# ewm.mk_mov(epi_dist=70, theta_earthquake=50, depth_earthquake=0, propagation_time=1200, seis_channel='BXZ', filter_params=[0.4, 2.0],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PKiKP', 'PP'], key_phase=['P'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='P_Tomo', title='Imaging the mantle', load_image='Al.png',
#             LL_L1_text='Faster traveling P-waves travel away from the Earthquake',
#             LL_L2_text='Waves are reflected off the surface and core',
#             LR_L1_text='The direct P-wave arrives first',
#             LR_L2_text='Al times these arrivals to find fast and\n slow areas in the Earth\'s mantle',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.25, LR_L2_time=1.5,
#             mov_pause_times=[0.5, 0.75, 1.25, 1.5], mov_fps=30, mov_dpi=150)
#
# ### ScS CMB imaging
# ewm.mk_mov(epi_dist=80, theta_earthquake=-32, depth_earthquake=0, propagation_time=1800, seis_channel='BXT', filter_params=[],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False, phases_to_plot=['S', 'ScS', 'SKS', 'SKKS', 'SS', 'SKiKS'], key_phase=['ScS'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='ScS_CMB', title='Investigating the Core-Mantle Boundary', load_image='Jenny.png',
#             LL_L1_text='Slower traveling S-waves travel away from the Earthquake',
#             LL_L2_text='Waves bounce of the surface and core but\n convert to P-waves in the outer core',
#             LR_L1_text='Jenny looks for these core-bouncing phases in the seismogram',
#             LR_L2_text='Delayed bouncing phases may have traveled\n through a mantle plume anchor',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[0.5, 0.75, 1.1, 1.2], mov_fps=30, mov_dpi=150)
#
# ### Diffraction
# ewm.mk_mov(epi_dist=145, theta_earthquake=-18, depth_earthquake=0, propagation_time=1400, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False, phases_to_plot=['PP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP'], key_phase=['Pdiff'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='Core_Diff', title='Core diffracted waves', load_image='Li.png',
#             LL_L1_text='Some P-wave energy leaves the surface and\n arrives at the core at a special angle',
#             LL_L2_text='This allows it to \'Hug\' the boundary of\n the core, known as wave refraction!',
#             LR_L1_text='Li searches for this energy on the seismogram\n as it arrives back at the surface',
#             LR_L2_text='These waves arriving from unpredictable\n locations can help locate mantle plume anchors',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.15, LR_L2_time=1.3,
#             mov_pause_times=[0.5, 0.75, 1.15, 1.3], mov_fps=45, mov_dpi=150)
#
# ### Liquid Outer Core
# ewm.mk_mov(epi_dist=130, theta_earthquake=-18, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False,
#             phases_to_plot=['PP', 'Pdiff', 'PKIKP', 'PKiKP', 'Sdiff', 'SKS', 'SKiKS', 'SKIKS', 'SS', 'SKKS'], key_phase=['PKIKP'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='Disc_OC', title='Discovery of the liquid outer core', load_image='Oldham.png',
#             LL_L1_text='P and S-waves travel in the mantle',
#             LL_L2_text='But only P-waves are found to travel\n in the outer core',
#             LR_L1_text='This led Richard Oldham to discover\n the liquid outer core',
#             LR_L2_text='S waves are converted to P-waves in the\n core and then convert back to S-waves as they leave the core',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[0.5, 0.75, 1.1, 1.2], mov_fps=45, mov_dpi=150)
#
# ### Discovery of the Inner Core
# ewm.mk_mov(epi_dist=152, theta_earthquake=10, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False, phases_to_plot=['PP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP'], key_phase=['PKiKP'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='Disc_IC', title='Detecting the Inner Core', load_image='Lehmann.png',
#             LL_L1_text='Waves travel faster as travel into the Earth\n so bend back towards the surface',
#             LL_L2_text='Bending of P-waves in the outer core causes\n P-waves to be invisible at some distances from the earthquake',
#             LR_L1_text='However Danish scientist Inge Lehmann recorded\n P-waves that arrive all around the globe',
#             LR_L2_text='She argued that some small P-waves bounce\n off a solid sphere within the Earth\'s core - the inner core was discovered!',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[0.5, 0.75, 1.1, 1.2], mov_fps=45, mov_dpi=150)
#
# ### Full wavefield
# ewm.mk_mov(epi_dist=179, theta_earthquake=78, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'PKKP', 'SS', 'SKKS', 'SKiKS'], overwrite_phase_defaults=False,
#             phases_to_plot=['PP', 'PKKP', 'PKIKP', 'SS', 'SKIKS', 'SKKS'], key_phase=['PKIKP'],
#             output_location='../wavefront_movie_outputs/', mov_name_str='Full_Wavefield', title='Complex P and S waves', load_image='vault.jpg',
#             LL_L1_text='Faster-P and slower S-wave energy is\n released by all natural earthquakes',
#             LL_L2_text='The fastest waves take over 20 minutes\n to travel through Earth',
#             LR_L1_text='Sensitive seismometers are needed to\n record energy at the other-side of the Earth',
#             LR_L2_text='Ground movements are fractions of a millimeter\n as the vibrations loose energy as they travel',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[0.5, 0.75, 1.1, 1.2], mov_fps=45, mov_dpi=150)
#
#





