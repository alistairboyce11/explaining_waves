'''
This script calls the function to make explaining waves movie:
    ########################## SET PARAMETERS HERE #############################

    propagation_time = propagation_time                  # Propagation time and seismogram length (s) - up to 3600s

    output_location=output_location                 # String to locate waveform outputs
    
    mov_name_str=mov_name_str                        # String to name movie = e.g., 'CMB1'

    mov_fps=mov_fps                                 # frames per second for the mov
    
    mov_dpi=mov_dpi                                 # Dots per inch for mov.
'''

import numpy as np
import matplotlib.pyplot as plt
import sys,glob
import os.path
# Function used to make movie
import home_screen_movie as hsm

filenames = ['Core_Diff_home',
             'Disc_IC_home',
             'Disc_OC_home',
             'Full_Wavefield_home',
             'P_Tomo_home',
             'ScS_CMB_home']
mov_labels = ['Diffracted Waves', 
              'Detecting the Inner Core', 
              'Liquid Outer Core', 
              'Complex P and S Waves', 
              'Imaging the Mantle', 
              'Core-Mantle Boundary']
              

for i in range(len(filenames)):
    hsm.mk_mov(propagation_time=20, output_location='./home_screen_outputs/', mov_name_str=filenames[i], mov_label=mov_labels[i], mov_fps=1, mov_dpi=150)

# hsm.mk_mov(propagation_time=20, output_location='./', mov_name_str=filenames[1], mov_label=mov_labels[1], mov_fps=1, mov_dpi=150)