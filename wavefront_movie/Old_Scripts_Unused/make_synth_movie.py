'''
REQUIRED:
conda install -c conda-forge instaseis


check here for DB: http://ds.iris.edu/ds/products/syngine/

# TO DO LIST:
# Add predicted traveltimes...?
# Improve source time function
# Write as callable functions rather than if statements.

'''
import instaseis
import obspy
from obspy import read
import matplotlib.pyplot as plt

import sys, glob
import obspy.signal.rotate
from obspy import UTCDateTime
import obspy.geodetics.base
import numpy as np
import obspy.geodetics

# print(instaseis.__path__)

if len(sys.argv) <2 or len(sys.argv) > 2:
    print('python make_synth_movie.py DIST')
    print('e.g. -> python make_synth_movie.py 120\n')
    exit()
else:
    dist=int(sys.argv[1])
    print('Calculating seismogram at ' + str(dist) + ' Degrees epi. dist.')

Quick_plot=False                                    # Quick plot of all components
Vertical_plot=True                                  # Matplotlib formatted plot of vertical comp.
Normalise_waveform=True                             # Normalise waveform amplitude
Filter_waveform=False                               # Filter waveform with bandpass filter; params below
fmin=0.02
fmax=0.5
EQ_time=UTCDateTime('2004-12-26 00:58:50')
Time_window=3600                                    # Length of seismogram time window (s)
Animate_Trace=True                                  # Variable to initate Animation

# Load database with Green's Functions

# db = instaseis.open_db("syngine://prem_a_2s")
# db = instaseis.open_db("syngine://ak135f_1s")
db = instaseis.open_db("syngine://ak135f_2s ")


# Read in source
# evtlatitude=3.0900
# evtlongitude=94.2600
# evtdepth=28.610
# source = instaseis.Source(latitude=evtlatitude, longitude=evtlongitude, depth_in_m=evtdepth,
#                           m_rr = 1.040000e+29,
#                           m_tt = -4.270000e+28,
#                           m_pp = -6.100000e+28,
#                           m_rt = 2.980000e+29,
#                           m_rp = -2.400000e+29,
#                           m_tp = 4.260000e+28,
#                           origin_time=UTCDateTime('2004-12-26 00:58:50'))

# Other option for source definition
# Earthquake defined at the equator at zero longitude.
evtlatitude=0
evtlongitude=0
evtdepth=10000
source = instaseis.Source.from_strike_dip_rake(latitude=evtlatitude, longitude=evtlongitude, depth_in_m=evtdepth, strike=60,dip=30, rake=90, M0=1E12, sliprate=1, dt=0.1, origin_time=EQ_time)

# Station parameters
# stlongitude increases to represent increasing epicentral distance.
stlatitude=0
stlongitude=dist
receiver = instaseis.Receiver(latitude=stlatitude, longitude=stlongitude, network="AB",station="CDE", location="SY")

# compute raypath statistics
distm, az, baz = obspy.geodetics.base.gps2dist_azimuth(evtlatitude, evtlongitude, stlatitude, stlongitude)
distdg = distm / (6371.e3 * np.pi / 180.)


start = EQ_time
end   = EQ_time+Time_window

# Run function to get waveforms
st = db.get_seismograms(source=source, receiver=receiver,kind='displacement', dt=0.1)
# Add headers to Pickle in .stats
st[0].stats['evla'] = evtlatitude
st[0].stats['evlo'] = evtlongitude

st[0].stats['evdp'] = evtdepth/1000 # want EQ depth in km in PICKLE

st[0].stats['stla'] = stlatitude
st[0].stats['stlo'] = stlongitude
st[0].stats['dist'] = distdg
st[0].stats['az'] = az
st[0].stats['baz'] = baz

# Rotate synthetics to radial and transverse
stE = st.select(channel='BXE')
stN = st.select(channel='BXN')
stZ = st.select(channel='BXZ')
[stRtmp,stTtmp]=obspy.signal.rotate.rotate_ne_rt(stN[0].data,stE[0].data,st[0].stats['baz'])
stR=stN[0].copy()
stR.stats['channel']='BXR'
stR.data = stRtmp
stT=stN[0].copy()
stT.stats['channel']='BXT'
stT.data = stTtmp

st+=stR
st+=stT

# Normalize waveform amplitude for each trace
if Normalise_waveform:
    for channel in st:
        print(channel.stats['channel'])
        print(channel.stats['starttime'], channel.stats['endtime'])
        windowed=channel[np.where(channel.times() >= 0) and np.where(channel.times() <= Time_window )]
        norm=np.max(np.abs(windowed))
        channel.data=channel.data/norm


#OVERWRITES previous PICKLE with new synthetics

filename_PICKLE = '../wavefront_movie_outputs/' + str(dist) + '_seis_synth.PICKLE'
filename_plot_string = '../wavefront_movie_outputs/' + str(dist) + '_seis_synth'

if Filter_waveform: 
    st.filter('bandpass', freqmin=fmin,freqmax=fmax, corners=2, zerophase=True)
    st.taper(max_length=5, max_percentage=0.02, type='cosine')

st.write(filename_PICKLE,format='PICKLE')  


# To view:
if Quick_plot:
    # Quick plot -  all components
    st1=read(filename_PICKLE,format='PICKLE')
    # st1.plot() 
    st1.plot(outfile=filename_plot_string + '_quick.png')

if Vertical_plot:
    # Matplotlib plot of vertical component
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    st1=read(filename_PICKLE,format='PICKLE')
    st1Z=st1.select(channel='BXZ')
    ax.plot(st1Z[0].times("matplotlib"), st1Z[0].data, "r-",linewidth=0.5)
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.xlabel('Time')
    plt.ylabel('Norm Amplitude')
    # plt.show()
    plt.savefig(filename_plot_string + '_BXZ.png')

# if Animate_Trace:
    