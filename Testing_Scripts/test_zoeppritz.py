'''
Script to test zoeppritz_coeff.py

'''
import numpy as np
import sys
sys.path.append('../')
import ray_colors_atten as rca
import zoeppritz_coeff as zpc
import phase_finder as pf
# # Obspy is a seismic toolkit
import obspy
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths
# velocity model as a function of depth.
model = TauPyModel(model='ak135')


disconts = [0, 2891.5, 5153.5 ]
depth=disconts[1]


print(rca.get_vp_a(depth))
print(rca.get_vp_b(depth))

print(rca.get_vs_a(depth))
print(rca.get_vs_b(depth))

print(rca.get_rho_a(depth))
print(rca.get_rho_b(depth))

layer1= [rca.get_vp_a(depth), rca.get_vs_a(depth), rca.get_rho_a(depth)]
layer2= [rca.get_vp_b(depth), rca.get_vs_b(depth), rca.get_rho_b(depth)]

#Define layer parameters
#[p velocity, s velocity, density]
# layer1 = [13717, 7265, 5566]
# layer2 = [8065, 0, 9903]

#Define ray parameter this example is for 50 deg PcP
p = (2.225*np.pi/180)/6371000

#Collate layers
# layers = [layer1, layer2]

#Call Zoeppritz function
Rmatrix = zpc.zoeppritz(p,layer1,layer2)

print(Rmatrix)