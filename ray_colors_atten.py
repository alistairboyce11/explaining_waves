'''
Script to calculate colours/amplitudes for each ray path over given propagation time.
Colour to vary between P and S 
Intrinsic attenuation to vary form P-to-S - different Q factor.
Reflection transmission factors to be same for P and S.

'''
### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
import matplotlib.pyplot as plt

# Obspy is a seismic toolkit
import obspy
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths
# velocity model as a function of depth.
model = TauPyModel(model='ak135')

import math
from pathlib import Path
home = str(Path.home())

# Function below used to define input phases.
import phase_finder as pf

# Function below used to find zoeppritz relfection transmission coefficients for each boundary crossing.
import zoeppritz_coeff as zpc


# Get velocities and densities for Reflection transmission coefficients (convert to m/s, kg/m3)
def get_vp_a(depth):
    if depth != 0:
        vp_a=model.model.s_mod.v_mod.evaluate_above(depth,'p')
        return vp_a*1000
    else:
        return 330

def get_vp_b(depth):
    vp_b=model.model.s_mod.v_mod.evaluate_below(depth,'p')
    return vp_b*1000

def get_vs_a(depth):
    if depth != 0:
        vs_a=model.model.s_mod.v_mod.evaluate_above(depth,'s')
        return vs_a*1000
    else:
        return 0
    
def get_vs_b(depth):
    vs_b=model.model.s_mod.v_mod.evaluate_below(depth,'s')
    return vs_b*1000
    
def get_rho_a(depth):
    if depth != 0:
        rho_a=model.model.s_mod.v_mod.evaluate_above(depth,'r')
        return rho_a*1000
    else:
        return 0
    
def get_rho_b(depth):
    rho_b=model.model.s_mod.v_mod.evaluate_below(depth,'r')
    return rho_b*1000

def get_ray_color(phase,dist,time,dists,depths,ray_param):
    # Want to determine the colour somehow
    # Set P and S equal to something perhaps.
    # Must return arrays of length time.
    
    cols=np.ones(len(time))
    
    if 'P' in str(phase):
        val=1
    if 'S' in str(phase):
        val=0.9
    # Set cols - P-different to S
    cols=cols*val
        
    return cols

def get_ray_atten(phase,dist,time,dists,depths,ray_param,seis_channel):
    # Want to determine the amplitude attentuation 
    # Start with P and S intrinsic attenuation and then multiply by reflection - transmission part.
    
    amps=np.ones(len(time))

    # For intrinsic attenuation, use if for Q factor, omega(W) natural frequency
    if 'P' in str(phase):
        Q=650; W=1.0
    if 'S' in str(phase):
        Q=280; W=0.1
    # Set alphas - intrinsic amplitude decay:
    i_atten=amps*np.exp((-W*time)/(2*Q))

    #####################################################################
    # The next section defines the reflection and transmission coefficents to set wavefront alphas.

    disconts = [0, 2891.5, 5153.5]

    # Define number of reflection/transmission points
    RT_max_points=4
    RT_point_amps=np.ones((len(time),RT_max_points))

    # Easier to operate on arrays without nan values.
    # They only occur at end so remove from dists and depths arrays
    dists=dists[~np.isnan(dists)]
    depths=depths[~np.isnan(depths)]
    p=ray_param
    
    #####################################################################
    
    if phase == 'PcP' or phase == 'ScS':
        # Check phase reaches CMB
        if np.nanmax(depths) > disconts[1]-5:
            # Need to find first time point where depth is > 2891.5 -5
            ind_RT0=np.where(depths > disconts[1]-5)[0][0]
            
            # Do Zoeppritz calcualtions
            d0=disconts[1]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)
            
            if seis_channel == 'BHT':
                R_RT0=np.abs(Rmatrix_RT0[1,1]) # This will be ScS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'ScS':
                    R_RT0=np.abs(Rmatrix_RT0[0,0])  # This will be ScS on vertical
                elif phase == 'PcP':
                    R_RT0=np.abs(Rmatrix_RT0[2,2]) # This will be PcP on vertical
            # print(phase, dist, R_RT0)
            RT_point_amps[ind_RT0:,0]=R_RT0

     #####################################################################
    if phase == 'PP' or phase == 'SS':
        # Check phase reaches bounce point
        if dists[-1] >= (dist/180*np.pi)/2 or math.isnan(dists[-1]):
            # Need to find first time point where dpeth is < 5
            ind_RT0=np.where(depths < disconts[0]+5)[0][1]
            
            # Do Zoeppritz calcualtions
            d0=disconts[0]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)

            if seis_channel == 'BHT':
                R_RT0=np.abs(Rmatrix_RT0[4,4]) # This will be SS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'SS':
                    R_RT0=np.abs(Rmatrix_RT0[3,3])  # This will be SS on vertical
                elif phase == 'PP':
                    R_RT0=np.abs(Rmatrix_RT0[5,5]) # This will be PP on vertical
            # print(phase, dist, R_RT0)
            RT_point_amps[ind_RT0:,0]=R_RT0

    #####################################################################
    if phase == 'PKP' or phase == 'SKS':
        # Check downgoing phase reaches CMB
        if np.nanmax(depths) > disconts[1]-5:
            # The first value where depth is greater than CMB depth.
            ind_RT0=np.where(depths > disconts[1]-5)[0][0]
            
            # Do Zoeppritz calcualtions
            d0=disconts[1]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)
            
            if seis_channel == 'BHT':
                T_RT0=np.abs(Rmatrix_RT0[5,1]) # This will be SKS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'SKS':
                    T_RT0=np.abs(Rmatrix_RT0[5,0])  # This will be SKS on vertical
                elif phase == 'PKP':
                    T_RT0=np.abs(Rmatrix_RT0[5,2]) # This will be PKP on vertical
            # print(phase, dist, T_RT0)
            RT_point_amps[ind_RT0:,0]=T_RT0
            
            # Check upgoing phase reaches CMB
            if depths[-1] < disconts[1]-5 or math.isnan(depths[-1]):
                # The last value where depth is less than CMB depth.
                ind_RT1=np.where(depths > disconts[1]-5)[0][-1]
                
            
                # Do Zoeppritz calcualtions
                d1=disconts[1]
                layer1= [get_vp_a(d1), get_vs_a(d1), get_rho_a(d1)]
                layer2= [get_vp_b(d1), get_vs_b(d1), get_rho_b(d1)]
                Rmatrix_RT1 = zpc.zoeppritz(p,layer1,layer2)
                
                if seis_channel == 'BHT':
                    T_RT1=np.abs(Rmatrix_RT1[1,5]) # This will be SKS on transverse
                elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                    if phase == 'SKS':
                        T_RT1=np.abs(Rmatrix_RT1[0,5])  # This will be SKS on vertical
                    elif phase == 'PKP':
                        T_RT1=np.abs(Rmatrix_RT1[2,5]) # This will be PKP on vertical
                RT_point_amps[ind_RT1:,1]=T_RT1
                
    #####################################################################
    if phase == 'PKiKP' or phase == 'SKiKS':
        # Check downgoing phase reaches CMB
        if np.nanmax(depths) > disconts[1]-5:
            # The first value where depth is greater than CMB depth.
            ind_RT0=np.where(depths > disconts[1]-5)[0][0]
            
            # Do Zoeppritz calcualtions
            d0=disconts[1]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)
            
            if seis_channel == 'BHT':
                T_RT0=np.abs(Rmatrix_RT0[5,1]) # This will be SKiKS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'SKiKS':
                    T_RT0=np.abs(Rmatrix_RT0[5,0])  # This will be SKiKS on vertical
                elif phase == 'PKiKP':
                    T_RT0=np.abs(Rmatrix_RT0[5,2]) # This will be PKiKP on vertical
            # print(phase, dist, T_RT0)
            RT_point_amps[ind_RT0:,0]=T_RT0

            # Check phase reaches bounce point
            if dists[-1] >= (dist/180*np.pi)/2 or math.isnan(dists[-1]):
                ind_RT1=np.where(depths > disconts[2]-5)[0][0]

                # Do Zoeppritz calcualtions
                d1=disconts[2]
                layer1= [get_vp_a(d1), get_vs_a(d1), get_rho_a(d1)]
                layer2= [get_vp_b(d1), get_vs_b(d1), get_rho_b(d1)]
                Rmatrix_RT1 = zpc.zoeppritz(p,layer1,layer2)
                
                R_RT1=np.abs(Rmatrix_RT1[2,2]) # ICB reflection is the same for all phases.
                RT_point_amps[ind_RT1:,1]=R_RT1
                
                # Check upgoing phase reaches CMB
                if depths[-1] < disconts[1]-5 or math.isnan(depths[-1]):
                    # The last value where depth is less than CMB depth.
                    ind_RT2=np.where(depths > disconts[1]-5)[0][-1]
                    
                    # Do Zoeppritz calcualtions
                    d2=disconts[1]
                    layer1= [get_vp_a(d2), get_vs_a(d2), get_rho_a(d2)]
                    layer2= [get_vp_b(d2), get_vs_b(d2), get_rho_b(d2)]
                    Rmatrix_RT2 = zpc.zoeppritz(p,layer1,layer2)
                    
                    if seis_channel == 'BHT':
                        T_RT2=np.abs(Rmatrix_RT2[1,5]) # This will be SKiKS on transverse
                    elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                        if phase == 'SKiKS':
                            T_RT2=np.abs(Rmatrix_RT2[0,5])  # This will be SKiKS on vertical
                        elif phase == 'PKiKP':
                            T_RT2=np.abs(Rmatrix_RT2[2,5]) # This will be PKiKP on vertical
                    RT_point_amps[ind_RT2:,2]=T_RT2

    #####################################################################
    if phase == 'PKIKP' or phase == 'SKIKS':
        # Check downgoing phase reaches CMB
        if np.nanmax(depths) > disconts[1]-5:
            # The first value where depth is greater than CMB depth.
            ind_RT0=np.where(depths > disconts[1]-5)[0][0]
            
            # Do Zoeppritz calcualtions
            d0=disconts[1]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)
            
            if seis_channel == 'BHT':
                T_RT0=np.abs(Rmatrix_RT0[5,1]) # This will be SKIKS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'SKIKS':
                    T_RT0=np.abs(Rmatrix_RT0[5,0])  # This will be SKIKS on vertical
                elif phase == 'PKIKP':
                    T_RT0=np.abs(Rmatrix_RT0[5,2]) # This will be PKIKP on vertical
            # print(phase, dist, T_RT0)
            RT_point_amps[ind_RT0:,0]=T_RT0
            
            # Check downgoing phase reaches ICB
            if np.nanmax(depths) > disconts[2]-5:
                ind_RT1=np.where(depths > disconts[2]-5)[0][0]
                
                # Do Zoeppritz calcualtions
                d1=disconts[1]
                layer1= [get_vp_a(d1), get_vs_a(d1), get_rho_a(d1)]
                layer2= [get_vp_b(d1), get_vs_b(d1), get_rho_b(d1)]
                Rmatrix_RT1 = zpc.zoeppritz(p,layer1,layer2)

                T_RT1=np.abs(Rmatrix_RT1[5,2]) # ICB downgoing transmission - same for all phases.
                RT_point_amps[ind_RT1:,1]=T_RT1
            
                # Check upgoing phase reaches ICB
                if depths[-1] < disconts[2]-5 or math.isnan(depths[-1]):
                    ind_RT2=np.where(depths > disconts[2]-5)[0][-1]
            
                    # Do Zoeppritz calcualtions
                    d2=disconts[1]
                    layer1= [get_vp_a(d2), get_vs_a(d2), get_rho_a(d2)]
                    layer2= [get_vp_b(d2), get_vs_b(d2), get_rho_b(d2)]
                    Rmatrix_RT2 = zpc.zoeppritz(p,layer1,layer2)
                    
                    T_RT2=np.abs(Rmatrix_RT2[2,5]) # ICB upgoing transmission - same for all phases.
                    RT_point_amps[ind_RT2:,2]=T_RT2
            
                    # Check upgoing phase reaches CMB
                    if depths[-1] < disconts[1]-5 or math.isnan(depths[-1]):
                        # The last value where depth is greater than CMB depth.
                        ind_RT3=np.where(depths > disconts[1]-5)[0][-1]
                        
                        # Do Zoeppritz calcualtions
                        d3=disconts[1]
                        layer1= [get_vp_a(d3), get_vs_a(d3), get_rho_a(d3)]
                        layer2= [get_vp_b(d3), get_vs_b(d3), get_rho_b(d3)]
                        Rmatrix_RT3 = zpc.zoeppritz(p,layer1,layer2)
                        
                        if seis_channel == 'BHT':
                            T_RT3=np.abs(Rmatrix_RT3[1,5]) # This will be SKIKS on transverse
                        elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                            if phase == 'SKIKS':
                                T_RT3=np.abs(Rmatrix_RT3[0,5])  # This will be SKIKS on vertical
                            elif phase == 'PKIKP':
                                T_RT3=np.abs(Rmatrix_RT3[2,5]) # This will be PKIKP on vertical
                        RT_point_amps[ind_RT3:,3]=T_RT3

    #####################################################################
    if phase == 'PKKP' or phase == 'SKKS':
        # Check downgoing phase reaches CMB
        if np.nanmax(depths) > disconts[1]-5:
            # The first value where depth is greater than CMB depth.
            ind_RT0=np.where(depths > disconts[1]-1)[0][0]
            
            # Do Zoeppritz calcualtions
            d0=disconts[1]
            layer1= [get_vp_a(d0), get_vs_a(d0), get_rho_a(d0)]
            layer2= [get_vp_b(d0), get_vs_b(d0), get_rho_b(d0)]
            Rmatrix_RT0 = zpc.zoeppritz(p,layer1,layer2)
            
            if seis_channel == 'BHT':
                T_RT0=np.abs(Rmatrix_RT0[5,1]) # This will be SKKS on transverse
            elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                if phase == 'SKKS':
                    T_RT0=np.abs(Rmatrix_RT0[5,0])  # This will be SKKS on vertical
                elif phase == 'PKKP':
                    T_RT0=np.abs(Rmatrix_RT0[5,2]) # This will be PKKP on vertical
            # print(phase, dist, T_RT0)

            RT_point_amps[ind_RT0:,0]=T_RT0

            # Check phase reaches bounce point
            if dists[-1] >= (dist/180*np.pi)/2 or math.isnan(dists[-1]):

                CMB_shallow=np.where(depths > disconts[1]-5)[0]
                CMB_deep   =np.where(depths < disconts[1]+5)[0]
                CMB_intersect=np.intersect1d(CMB_shallow,CMB_deep)
        
                # First turning point:
                K_turn_1=np.where(depths >= np.nanmax(depths)-1)[0][0]
                # Find first index of CMB intersect > K_turn_1
                CMB_intersect_ind=next(k for k, value in enumerate(CMB_intersect) if value > K_turn_1)
                ind_RT1=CMB_intersect[CMB_intersect_ind]
                
            
                # Do Zoeppritz calcualtions
                d1=disconts[1]
                layer1= [get_vp_a(d1), get_vs_a(d1), get_rho_a(d1)]
                layer2= [get_vp_b(d1), get_vs_b(d1), get_rho_b(d1)]
                Rmatrix_RT1 = zpc.zoeppritz(p,layer1,layer2)
                
                R_RT1=np.abs(Rmatrix_RT1[5,5]) # The upgoing CMB reflection - same for all phases.
                RT_point_amps[ind_RT1:,1]=R_RT1

                # Check upgoing phase reaches CMB
                if depths[-1] < disconts[1]-5 or math.isnan(depths[-1]):
                    # The last value where depth is greater than CMB depth.
                    ind_RT2=np.where(depths > disconts[1]-5)[0][-1]
                    
                    # Do Zoeppritz calcualtions
                    d2=disconts[1]
                    layer1= [get_vp_a(d2), get_vs_a(d2), get_rho_a(d2)]
                    layer2= [get_vp_b(d2), get_vs_b(d2), get_rho_b(d2)]
                    Rmatrix_RT2 = zpc.zoeppritz(p,layer1,layer2)
                    
                    if seis_channel == 'BHT':
                        T_RT2=np.abs(Rmatrix_RT2[1,5]) # This will be SKKS on transverse
                    elif seis_channel == 'BHR' or seis_channel == 'BHZ':
                        if phase == 'SKKS':
                            T_RT2=np.abs(Rmatrix_RT2[0,5])  # This will be SKKS on vertical
                        elif phase == 'PKKP':
                            T_RT2=np.abs(Rmatrix_RT2[2,5]) # This will be PKKP on vertical
                    RT_point_amps[ind_RT2:,2]=T_RT2

    
    
    # Want to multiply all the RT amplitude array segments together.
    RT_amps=np.ones(np.shape(RT_point_amps)[0])
    for i in range(np.shape(RT_point_amps)[1]): 
        RT_amps=RT_amps*RT_point_amps[:,i]
    
    amps = i_atten * RT_amps
    
    return amps

    ########################## Some notes on phases accounted for above ##########

    #
    # 'P', 'PcP', 'PP', 'PKP', 'PKiKP', 'PKIKP','PKKP',  'Pdiff'
    # 'S', 'ScS', 'SS', 'SKS', 'SKiKS', 'SKIKS','SKKS',  'Sdiff'
    #

    # Phase types: direct, topside OC-ref, underside SF-ref, OC-P, underside OC-ref, topside IC-ref, IC-P, IC-S
    # Reflection types: topside OC-refl, underside SF-refl, underside OC-refl, topside IC-refl
    # transmission types: downgoing M-OC, downgoing OC-IC, upgoing IC-OC, upgoing OC-M.
    #
    # Legs:
    #
    # Mantle-P 'P'
    # Mantle-S 'S'
    # OC-ref   'c'
    # SF-ref   'PP'
    # IC-ref   'i'
    # OC-P     'K'
    # IC-P     'I'
