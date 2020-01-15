'''
Script to test ../gen_seis.py

'''
import sys
sys.path.append('../')
import gen_seis as gs

##################################################################################

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=130

# depth of earthquake in km
depth_earthquake = 0

# Waveform characteristics
normalise_waveform=True                             # Normalise waveform amplitude
filter_params=[]                               # Filter waveform with bandpass filter; params below

propagation_time = 1800                                    # Propagation time and seismogram length (s)

# Output handling

output_Location='./'

##################################################################################

Test_1 = True # Test production of synthetic seismogram
Test_2 = True # Test if synthetic seismogram is present
Test_3 = True # Test loading of synthetic seismogram

if Test_1:
    gs.generate_seismogram(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time,norm_wave=normalise_waveform,filter_params=filter_params,out_loc=output_Location)
    
if Test_2:
    fp=gs.check_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time, out_loc=output_Location)
    print(fp)

if Test_3:
    synth_BXZ=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,out_loc=output_Location)
    print(synth_BXZ[0].stats)
    synth_BXZ[0].plot()
    
    