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




# Other testing runs

# P-wave imaging
ewm.mk_mov(epi_dist=70, theta_earthquake=50, depth_earthquake=0, propagation_time=1200, seis_channel='BXZ', filter_params=[0.4, 2.0],
            extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PKP', 'PKiKP', 'PP', 'PKIKP'], key_phase=['P'], mirror_key_rp=False,
            output_location='../wavefront_movie_outputs/', mov_name_str='P_Tomo_test', title='Imaging the mantle', load_image='Al.png',
            LL_L1_text='Earthquake waves travel outwards in all\n directions from where an earthquake happens',
            LL_L2_text='These waves can tell us about the material\n they travel through on their journey',
            LR_L1_text='\"I look at the time it takes for P waves to\n arrive back at the Earth’s surface\"',
            LR_L2_text='\"I image where the mantle is hotter or colder\n by measuring the variable speeds of the waves\"',
            LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
            mov_pause_times=[], mov_fps=45, mov_dpi=150)
            
### Diffraction
ewm.mk_mov(epi_dist=145, theta_earthquake=-18, depth_earthquake=0, propagation_time=1400, seis_channel='BXZ', filter_params=[],
            extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP'], key_phase=['Pdiff'],  mirror_key_rp=False,
            output_location='../wavefront_movie_outputs/', mov_name_str='Core_Diff_test', title='Core diffracted waves', load_image='Li.png',
            LL_L1_text='Some S-wave energy leaves the earthquake\n and arrives at the core at a special angle',
            LL_L2_text='At this specific angle the wave \'hugs\' the\n edge of the core - this is called wave diffraction',
            LR_L1_text='\"I search for core \'hugging\' waves\n in the seismogram\"',
            LR_L2_text='\"I locate the mantle plume anchors that cause\n these waves to arrive from unexpected directions\"',
            LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.15, LR_L2_time=1.3,
            mov_pause_times=[], mov_fps=45, mov_dpi=150)
# #






# Corrected labels

# # P-wave imaging
# ewm.mk_mov(epi_dist=70, theta_earthquake=50, depth_earthquake=0, propagation_time=1200, seis_channel='BXZ', filter_params=[0.4, 2.0],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PKP', 'PKiKP', 'PP', 'PKIKP'], key_phase=['P'], mirror_key_rp=False,
#             output_location='../wavefront_movie_outputs/', mov_name_str='P_Tomo', title='Imaging the mantle', load_image='Al.png',
#             LL_L1_text='Earthquake waves travel outwards in all\n directions from where an earthquake happens',
#             LL_L2_text='These waves can tell us about the material\n they travel through on their journey',
#             LR_L1_text='\"I look at the time it takes for P waves to\n arrive back at the Earth’s surface\"',
#             LR_L2_text='\"I image where the mantle is hotter or colder\n by measuring the variable speeds of the waves\"',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)
#
# ### ScS CMB imaging
# ewm.mk_mov(epi_dist=60, theta_earthquake=-32, depth_earthquake=0, propagation_time=1800, seis_channel='BXT', filter_params=[],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['S', 'ScS', 'SS'], key_phase=['ScS'], mirror_key_rp=False,
#             output_location='../wavefront_movie_outputs/', mov_name_str='ScS_CMB', title='Investigating the Core-Mantle Boundary', load_image='Jenny.png',
#             LL_L1_text='S-waves are one type of wave that travel\n outwards in all directions from an earthquake',
#             LL_L2_text='They bounce off the core-mantle boundary,\n and are sensitive to the structure in the deep mantle',
#             LR_L1_text='\"I look for these core-bouncing waves\n in the seismogram\"',
#             LR_L2_text='\"I use the shape of the waves to investigate\n deep mysterious structures like mantle plume anchors\"',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)
#
# ### Diffraction
# ewm.mk_mov(epi_dist=145, theta_earthquake=-18, depth_earthquake=0, propagation_time=1400, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PcP', 'PP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP'], key_phase=['Pdiff'],  mirror_key_rp=False,
#             output_location='../wavefront_movie_outputs/', mov_name_str='Core_Diff', title='Core diffracted waves', load_image='Li.png',
#             LL_L1_text='Some S-wave energy leaves the earthquake\n and arrives at the core at a special angle',
#             LL_L2_text='At this specific angle the wave \'hugs\' the\n edge of the core - this is called wave diffraction',
#             LR_L1_text='\"I search for core \'hugging\' waves\n in the seismogram\"',
#             LR_L2_text='\"I locate the mantle plume anchors that cause\n these waves to arrive from unexpected directions\"',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.15, LR_L2_time=1.3,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)
# #
# ### Liquid Outer Core
# ewm.mk_mov(epi_dist=100, theta_earthquake=0, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False,
#             phases_to_plot=['P', 'PP', 'PcP', 'PKP', 'Pdiff', 'PKIKP', 'PKiKP', 'S', 'ScS', 'SS'], key_phase=['S'],  mirror_key_rp=True,
#             output_location='../wavefront_movie_outputs/', mov_name_str='Disc_OC', title='Discovery of the liquid outer core', load_image='Oldham.png',
#             LL_L1_text='S or transverse waves can only travel\n through a solid and not a liquid',
#             LL_L2_text='In 1906, British geologist Richard Oldham\n first noticed that there were no S waves beyond\n a certain distance from earthquakes – called a \'shadow zone\'',
#             LR_L1_text='This was the first clue to the\n existence of a liquid core!',
#             LR_L2_text='',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)
#
# ### Discovery of the Inner Core
# ewm.mk_mov(epi_dist=120, theta_earthquake=10, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False, phases_to_plot=['P', 'PP', 'PcP', 'PKP', 'PKIKP', 'PKiKP'], key_phase=['PKiKP'], mirror_key_rp=False,
#             output_location='../wavefront_movie_outputs/', mov_name_str='Disc_IC', title='Detecting the Inner Core', load_image='Lehmann.png',
#             LL_L1_text='P waves traveling through the Earth\n bounce off interior boundaries',
#             LL_L2_text='In the 1930s Danish scientist Inge Lehmann\n first recorded an unexpected P-wave arrival\n that came from the inner-core boundary',
#             LR_L1_text='She argued the core might be\n changing from a liquid to a solid\n close to the centre of the Earth!',
#             LR_L2_text='',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)
#
# ### Full wavefield
# ewm.mk_mov(epi_dist=179, theta_earthquake=78, depth_earthquake=0, propagation_time=1800, seis_channel='BXZ', filter_params=[],
#             extra_phases=['PP', 'SS'], overwrite_phase_defaults=False,
#             phases_to_plot=['P', 'PcP', 'PP', 'Pdiff', 'PKP', 'PKIKP', 'PKiKP','S', 'ScS', 'SS'], key_phase=['PKIKP'],  mirror_key_rp=False,
#             output_location='../wavefront_movie_outputs/', mov_name_str='Full_Wavefield', title='Complex P and S waves', load_image='vault.jpg',
#             LL_L1_text='P waves and S waves are caused\n by all natural earthquakes',
#             LL_L2_text='The faster traveling P waves take only 20 minutes\n to travel to the opposite side of the Earth!',
#             LR_L1_text='Sensitive instruments called seismometers\n are used to measure the shaking of the ground\n caused by the earthquake waves at the surface',
#             LR_L2_text='Waves lose lots of energy as they travel,\n so when they return to the surface\n the movements they cause are less than a millimeter!',
#             LL_L1_time=0.5, LL_L2_time=0.75, LR_L1_time=1.1, LR_L2_time=1.2,
#             mov_pause_times=[], mov_fps=45, mov_dpi=150)







