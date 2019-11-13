'''
Script to test phase_finder.py

'''
import sys
sys.path.append('../')
import phase_finder as pf
# -*- coding: utf-8 -*-
import json

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    
Test_1 = False # Test production of phase dictionary
Test_2 = False # Test reading of phase dictionary
Test_3 = False # Test find phases at dist
Test_4 = True # Test find min phase dist
Test_5 = True # Test find max phase dist
Test_6 = False # Test find first arrival
Test_7 = False  # Test find arrival time

depth_earthquake = 0


if Test_1:
    pf.gen_phase_dict(depth_earthquake=0, extra_phases=[ 'SKiKS', 'PKiKP'], overwrite_phase_defaults=False)

if Test_2:
    phase_dist=pf.load_phase_dict(depth_earthquake=0)
    print('SS' in phase_dist['92'])
    print('PKKP' in phase_dist['91'])
    print(phase_dist['93'].keys())
    

if Test_3:
    epi_dist=20
    phase_list=pf.find_phases_at_dist(depth_earthquake=depth_earthquake, epi_dist=epi_dist)
    print(phase_list)
    
if Test_4:
    phase_name='SKiKS'
    mrd=pf.find_min_ray_dist(depth_earthquake=depth_earthquake, phase_name=phase_name)
    print('Min ray dist for '+str(phase_name)+' is: ' + str(mrd)+'\n')


if Test_5:
    phase_name='SKiKS'
    mrd=pf.find_max_ray_dist(depth_earthquake=depth_earthquake, phase_name=phase_name)
    print('Max ray dist for '+str(phase_name)+' is: ' + str(mrd)+'\n')
    
    
if Test_6:
    epi_dist=20
    phase_name, arrival_time = pf.find_first_arrival(depth_earthquake=depth_earthquake, epi_dist=epi_dist)
    print('First arriving phase at '+str(epi_dist)+' is '+phase_name+' at '+str(arrival_time)+'s')
    
if Test_7:
    epi_dist=20
    phase_name='P'
    arrival_time=pf.find_arrival_time(depth_earthquake=0, epi_dist=20, phase_name=phase_name)
    print('At '+str(epi_dist)+'deg, '+phase_name+' arrives at '+str(arrival_time)+'s')
    
    
    
    
