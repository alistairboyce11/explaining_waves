'''
Script to calculate colours/amplitudes for each ray path over given propagation time.
Colour to vary between P and S 
Intrinsic attenuation to vary form P-to-S - different Q factor.
Reflection refraction factors to be same for P and S.

'''
### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
import matplotlib.pyplot as plt

# # Obspy is a seismic toolkit
# import obspy
# from obspy.taup import TauPyModel
# from obspy.taup import plot_travel_times
# from obspy.taup import plot_ray_paths
## velocity model as a function of depth.
# model = TauPyModel(model='ak135')

# import sys,glob
# import os.path

from pathlib import Path
home = str(Path.home())

# Function below used to define input phases.
import phase_finder as pf


def get_ray_color(phase,dist,time,dists,depths):
    # Want to determine the colour somehow
    # Set P and S equal to something perhaps.
    # Must return arrays of length time.
    
    cols=np.ones(len(time))
    
    # For intrinsic attenuation, use if for Q factor
    if 'P' in str(phase):
        val=1
    if 'S' in str(phase):
        val=0.7
    # Set cols - P-different to S
    cols=cols*val
    
    # cols = [float(col) for col in cols]
    
    return cols


def get_ray_atten(phase,dist,time,dists,depths):
    # Want to determine the amplitude attentuation 
    # Start with P and S intrinsic attenuation and then multiply by reflection refraction part.
    
    
    amps=np.ones(len(time))
    
    # For intrinsic attenuation, use if for Q factor, omega(W) natural frequency
    if 'P' in str(phase):
        Q=650; W=1.0
    if 'S' in str(phase):
        Q=380; W=0.1
    # print('Q: '+str(Q)+', W: '+str(W))
    # Set alphas - intrinsic amplitude decay:
    i_atten=amps*np.exp((-W*time)/(2*Q))
    
    
    amps = i_atten
    # amps = [float(amp) for amp in amps]

    return amps