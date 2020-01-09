'''
This script contains a bunch of functions used to help specify phases to plot:

gen_phase_dict(depth_earthquake=0, extra_phases=None, overwrite_phase_defaults=False):
    Create a dictionary of phases, arrival times and ray parameters for distances 1-180deg.
    Specify earthquake depth and additional phases to add to Taup defaults.
    If overwrite_phase_defaults: only extra_phases are calculated for dictionary.

check_dict_present(depth_earthquake=0):
    Check whether dictionary for given EQ depth is present

load_phase_dict(depth_earthquake=0):
    Loads phase dictionary in current directory

find_first_arrival(depth_earthquake=0, epi_dist=90):
    Returns name, time of first arrival for given distance

def find_arrival_time(depth_earthquake=0, epi_dist=90, phase_name='P'):
    Returns time of phase arrival at given distance

find_min_ray_dist(depth_earthquake=0, phase_name='P'):
    Returns minimum epicentral distance for given phase

find_max_ray_dist(depth_earthquake=0, phase_name='P'):
    Returns maximum epicentral distance for given phase

find_phases_at_dist(depth_earthquake=0, epi_dist=90):
    Returns a list of phases arriving at a given distance

'''

import json

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    

# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt
# Obspy is a seismic toolkit
import obspy
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths

import os.path
import time
import glob
import shutil
import numpy as np
import scipy
import time
import sys

model = TauPyModel(model='ak135')


##################################################################################
    
def gen_phase_dict(depth_earthquake=0, extra_phases=None, overwrite_phase_defaults=False):
    # input EQ depth, extra phases phases
    
    if ( extra_phases == None ) and ( overwrite_phase_defaults == True ):
        print('NO PHASES SELECTED FOR DICTIONARY......')
        print('Must specify extra_phases if overwrite_phase_defaults == True')
        print('exiting\n')
        sys.exit()

    print('Attempting to make phase dictionary')
    print('EQ depth = '+str(depth_earthquake)+'km\n')
    
    phase_dist=dict()
    
    for epi_dist in np.arange(1, 181, 1):
        phase_dist[str(epi_dist)]=dict()
        print('Calculating entries at ' +str(epi_dist)+'deg.')
        
        if overwrite_phase_defaults:
            # Calculate arrivals for extra_phases only
            print('Attempting to add '+str(extra_phases))
            try:
                arrivals = model.get_pierce_points(source_depth_in_km=depth_earthquake, distance_in_degree=epi_dist, phase_list=extra_phases )
            except:
                print('Extra phases could not be added for '+str(epi_dist)+'deg.')
        
        else:
            # Calculates arrivals for default phases.
            arrivals = model.get_pierce_points(source_depth_in_km=depth_earthquake, distance_in_degree=epi_dist)
            print('Taup initally uses ' + str(len(arrivals)) + ' phases')
            if extra_phases != None:
                # Adding extra arrivals for distance if possible
                # Will overrite if already calculated... Not an issue, only first arrival added.
                print('Attempting to add '+str(extra_phases))
                try:
                    extra_arrivals = model.get_pierce_points(source_depth_in_km=depth_earthquake, distance_in_degree=epi_dist, phase_list=extra_phases )
                    arrivals = arrivals + extra_arrivals
                except:
                    print('Extra phases could not be added for '+str(epi_dist)+'deg.')
        
        arr_count = len(arrivals)
        print('Recording first arrivals for '+str(arr_count)+' phases\n')
        # print(arrivals)

        for i in range(arr_count):
            # Check first arriving phase has not been added.
            if not arrivals[i].name in phase_dist[str(epi_dist)]:
                # print('Adding: ' +str(arrivals[i].name))
                phase_dist[str(epi_dist)][arrivals[i].name]=dict()
                # Record arrival time, ray param (s/deg), turning depth for each arrival
                phase_dist[str(epi_dist)][arrivals[i].name]['time']   = arrivals[i].time
                phase_dist[str(epi_dist)][arrivals[i].name]['rayp']   = arrivals[i].ray_param*np.pi/180
                
                # column index 3 is depth in pierce array
                depths=[]
                for j in range(len(arrivals[i].pierce)):
                    depths.append(arrivals[i].pierce[j][3])
                phase_dist[str(epi_dist)][arrivals[i].name]['tndp']   = np.max(depths)

                # phase_dist[str(epi_dist)][arrivals[i].name]['pnum']    = int(i)
                # phase_dist[str(epi_dist)][arrivals[i].name]['incang'] = arrivals[i].incident_angle
                # phase_dist[str(epi_dist)][arrivals[i].name]['takang'] = arrivals[i].takeoff_angle

    # Write dictionary to earthquake-depth specific file.
    with io.open('phase_dist_'+str(depth_earthquake)+'km_depth.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(phase_dist,indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))

    print('phase dictionary created...')
    
    return()
    
##################################################################################
    
def check_dict_present(depth_earthquake=0):
    # Checks if dictionary is present in current directory or needs generating
    
    if os.path.exists('./phase_dist_'+str(depth_earthquake)+'km_depth.json'):
        # print('phase_dist dictonary already present.')
        return True
    else:
        # print('run function to generate phase dictonary')
        # gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
        return False
    
##################################################################################
    
def load_phase_dict(depth_earthquake=0):
    # Loads phase dictinoary into memory.
    
    with open('./phase_dist_'+str(depth_earthquake)+'km_depth.json') as data_file:
        phase_dist = json.load(data_file)
        
    return(phase_dist)
    
##################################################################################
    

def find_first_arrival(depth_earthquake=0, epi_dist=90):
    # Return name, time of first arrival for given distance

    if not check_dict_present(depth_earthquake=depth_earthquake):
        gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
    phase_dist=load_phase_dict(depth_earthquake=depth_earthquake)
    
    # Get an iterable list of keys
    key_list=list(phase_dist[str(epi_dist)].keys())
    phase_keys=[]
    for i in range(len(key_list)):
        phase_keys.append(str(key_list[i]))
    
    # Make a 2 arrays of phases and times
    phases=[]
    times =[]
    for j in range(len(phase_keys)):
        phases.append(str(phase_keys[j]))
        times.append(float(phase_dist[str(epi_dist)][phase_keys[j]]['time']))
    
    # Find index of minimum time : first arrival
    first_arr_ind=np.argmin(times)
    phase_name=str(phases[first_arr_ind])
    arrival_time=float(times[first_arr_ind])
    
    return(phase_name, arrival_time)

##################################################################################

def find_arrival_time(depth_earthquake=0, epi_dist=90, phase_name='P'):
    # Return time of phase arrival at given distance

    if not check_dict_present(depth_earthquake=depth_earthquake):
        gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
    phase_dist=load_phase_dict(depth_earthquake=depth_earthquake)
    
    phase_list=find_phases_at_dist(depth_earthquake=depth_earthquake, epi_dist=epi_dist)
    
    if phase_name in phase_list:
        # print('Phase arrives at this distance.. :)\n')
        arrival_time = float(phase_dist[str(epi_dist)][phase_name]['time'])
    else:
        print('Something wrong.....')
        print(str(phase_name)+' not present at '+str(epi_dist)+'deg...')
        print('exiting...\n')
        sys.exit()
    
    return(arrival_time)

##################################################################################
    
    
def find_min_ray_dist(depth_earthquake=0, phase_name='P'):
    # Return minimum epicentral distance for given phase

    if not check_dict_present(depth_earthquake=depth_earthquake):
        gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
    phase_dist=load_phase_dict(depth_earthquake=depth_earthquake)

    # Get an iterable list of keys
    key_list=list(phase_dist.keys())
    dist_keys=[]
    for i in range(len(key_list)):
        dist_keys.append(int(key_list[i]))
    dist_keys=np.sort(dist_keys)
    
    dists=[]
    for j in range(len(dist_keys)):
        if phase_name in phase_dist[str(dist_keys[j])]:
            dists.append(dist_keys[j])
    
    min_ray_dist=np.min(dists)
    
    # Because Taup cannot handle eq_depth=0km, epi_dist=0km
    # Force min_ray_dist=0 if above calculcation yeilds 1.
    
    if min_ray_dist == 1:
        print('Forcing min_ray_dist = 0')
        min_ray_dist = 0
    
    return(min_ray_dist)
    
##################################################################################
    
def find_max_ray_dist(depth_earthquake=0, phase_name='P'):
    # Return maximum epicentral distance for given phase

    if not check_dict_present(depth_earthquake=depth_earthquake):
        gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
    phase_dist=load_phase_dict(depth_earthquake=depth_earthquake)

    # Get an iterable list of keys
    key_list=list(phase_dist.keys())
    dist_keys=[]
    for i in range(len(key_list)):
        dist_keys.append(int(key_list[i]))
    dist_keys=np.sort(dist_keys)
    
    dists=[]
    for j in range(len(dist_keys)):
        if phase_name in phase_dist[str(dist_keys[j])]:
            dists.append(dist_keys[j])
    
    max_ray_dist=np.max(dists)
    
    return(max_ray_dist)
    
##################################################################################
    
def find_phases_at_dist(depth_earthquake=0, epi_dist=90):
    # Return a list of phases arriving at a given distance
    
    if not check_dict_present(depth_earthquake=depth_earthquake):
        gen_phase_dict(depth_earthquake=depth_earthquake, extra_phases=None)
    phase_dist=load_phase_dict(depth_earthquake=depth_earthquake)

    phase_list = list(phase_dist[str(epi_dist)].keys())

    return(phase_list)
    
##################################################################################
    
def find_phase_attenuation(phase_name='P'):
    phase_attenuation=1


    return(phase_attenuation)

    
##################################################################################
