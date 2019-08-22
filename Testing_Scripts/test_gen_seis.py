'''
Script to test ../gen_seis.py

'''
import sys
sys.path.append('../')
import gen_seis as gs

##################################################################################

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=20

# depth of earthquake in km
depth_earthquake = 0

# Waveform characteristics
Normalise_Waveform=True                             # Normalise waveform amplitude
Filter_Waveform=False                               # Filter waveform with bandpass filter; params below

Propagation_time = 3600                                    # Propagation time and seismogram length (s)

# Output handling

Output_Location='./'

##################################################################################

Test_1 = False # Test production of synthetic seismogram
Test_2 = True # Test if synthetic seismogram is present
Test_3 = True # Test loading of synthetic seismogram

if Test_1:
    gs.generate_seismogram(epi_dist=epi_dist,evtdepth=depth_earthquake,Time_window=Propagation_time,Norm_Wave=Normalise_Waveform,Filt_Wave=Filter_Waveform,Out_loc=Output_Location)
    
if Test_2:
    fp=gs.check_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,Time_window=Propagation_time, Out_loc=Output_Location)
    print(fp)

if Test_3:
    synth_BXZ=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,Out_loc=Output_Location)
    print(synth_BXZ[0].stats)
    synth_BXZ[0].plot()
    
    