'''
Script to test ../gen_seis.py

'''
import sys
sys.path.append('../')
import gen_seis as gs
import numpy as np


##################################################################################

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=70

# depth of earthquake in km
depth_earthquake = 0

# Waveform characteristics
normalise_waveform=True                             # Normalise waveform amplitude
filter_params=[]                               # Filter waveform with bandpass filter; params below

propagation_time = 1800                                    # Propagation time and seismogram length (s)

seis_channel = 'BXZ'

# Output handling

output_Location='./'

##################################################################################

Test_1 = False # Test production of synthetic seismogram
Test_2 = False # Test if synthetic seismogram is present
Test_3 = True # Test loading of synthetic seismogram

if Test_1:
    gs.generate_seismogram(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time,norm_wave=normalise_waveform,filter_params=filter_params,out_loc=output_Location)
    
if Test_2:
    fp=gs.check_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,time_window=propagation_time, out_loc=output_Location)
    print(fp)

if Test_3:
    synth=gs.load_synth_seis(epi_dist=epi_dist,evtdepth=depth_earthquake,out_loc=output_Location)


    synth_channel=synth.select(channel=seis_channel)
    print(synth_channel[0].stats)
    # synth_channel[0].plot()

    seis_times = synth_channel[0].times()
    seis_data  = synth_channel[0].data
    delta      = synth_channel[0].stats['delta']
    npts       = synth_channel[0].stats['npts']
    max_amp    = np.ceil(np.max(seis_data))  + 0.1
    min_amp    = np.floor(np.min(seis_data)) - 0.1

    iter=0
    TW_duration=300                                             # Seismogram plot window length (s)
    tick_pointer_width=20                                       # drawing tick length (s)

    # Create buffer arrays - width of TW_duration to pad start of seismogram.
    time_buffer         = np.arange(-TW_duration,0,delta)
    seis_buffer         = np.zeros(len(time_buffer))
    # Add buffer to start of seismogram
    seis_times_new      = np.concatenate([time_buffer, seis_times])
    seis_data_new       = np.concatenate([seis_buffer, seis_data])

    print(len(seis_times_new))
    print(delta)
    t=693
    Key_phase_label_time=3.0*60     # Length of time for key-phase to be labelled
    Key_phase_width = 20            # Cycle time for incoming key phase....
    key_phase_A_time = 673.34

    
    
    print(round((key_phase_A_time/delta)))
    print(round((key_phase_A_time + Key_phase_width)/delta))
    
    print(np.max(np.abs(seis_data_new[len(time_buffer)+round((key_phase_A_time/delta)):len(time_buffer)+round((key_phase_A_time + Key_phase_width)/delta):1])))
    synth_channel[0].plot()
    
    
    
    