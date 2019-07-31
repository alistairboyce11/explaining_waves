'''
REQUIRED:
conda install -c conda-forge instaseis

 PDE 2004 12 26  0 58 50.00   3.3000   95.7800  10.0 8.9 8.9 OFF W COAST OF NORTHERN                 
event name:     122604A        
time shift:    138.9600
half duration:  95.0000
latitude:        3.0900
longitude:      94.2600
depth:          28.6100
Mrr:       1.040000e+29
Mtt:      -4.270000e+28
Mpp:      -6.100000e+28
Mrt:       2.980000e+29
Mrp:      -2.400000e+29
Mtp:       4.260000e+28

check here for DB: http://ds.iris.edu/ds/products/syngine/



# TO DO LIST:
# Add predicted traveltimes...?
# write function to normalise the waveform
# Move source to pole - test
# Define representative source time function



'''
import instaseis
import obspy
from obspy import read
import matplotlib.pyplot as plt
import sys,glob
import obspy.signal.rotate
from obspy import UTCDateTime
import obspy.geodetics.base
import numpy as np
import obspy.geodetics

print(instaseis.__path__)

clean = True
    
# Load database with Green Functions
# db = instaseis.open_db("syngine://prem_a_2s")
# db = instaseis.open_db("syngine://ak135f_1s")
db = instaseis.open_db("syngine://ak135f_2s ")


# Read in source
evtlatitude=3.0900
evtlongitude=94.2600
evtdepth=28.610
source = instaseis.Source(latitude=evtlatitude, longitude=evtlongitude, depth_in_m=evtdepth,
                          m_rr = 1.040000e+29,
                          m_tt = -4.270000e+28,
                          m_pp = -6.100000e+28,
                          m_rt = 2.980000e+29,
                          m_rp = -2.400000e+29,
                          m_tp = 4.260000e+28,
                          origin_time=UTCDateTime('2004-12-26 00:58:50'))

# Other option for source definition
# source = instaseis.Source.from_strike_dip_rake(latitude=10.0, longitude=12.0, depth_in_m=1000, strike=79,dip=10, rake=20, M0=1E17)

# Station parameters
stlatitude=12.34
stlongitude=56.78
receiver = instaseis.Receiver(latitude=stlatitude, longitude=stlongitude, network="AB",station="CDE", location="SY")

# compute raypath statistics
distm, az, baz = obspy.geodetics.base.gps2dist_azimuth(evtlatitude, evtlongitude, stlatitude, stlongitude)
distdg = distm / (6371.e3 * np.pi / 180.)

start =UTCDateTime('2004-12-26 00:58:50')
end   =UTCDateTime('2004-12-26 00:58:50')+3600  

# Run function to get waveforms
st = db.get_seismograms(source=source, receiver=receiver,kind='displacement', dt=0.1)
# Add headers to Pickle in .stats
st[0].stats['evla'] = evtlatitude
st[0].stats['evlo'] = evtlongitude
st[0].stats['evdp'] = evtdepth
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
# st+=stZ
#print(streamnew)
for x in st:
   print(x.stats['channel'])
#OVERWRITES previous PICKLE with synthetics included
st.write('../wavefrom_movie_outputs/seis_synth.PICKLE',format='PICKLE')  
#plt.show()



To view:

# Quick plot -  all components
st1=read('../wavefrom_movie_outputs/seis_synth.PICKLE',format='PICKLE')
st1.plot()  
st1.plot(outfile='../wavefrom_movie_outputs/seis_synth_quick.png')

# Matplotlib plot of vertical component
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
st1Z=st1.select(channel='BXZ')
ax.plot(st1Z[0].times("matplotlib"), st1Z[0].data, "r-")
ax.xaxis_date()
fig.autofmt_xdate()
plt.show()
plt.savefig('../wavefrom_movie_outputs/seis_synth_mpl_BXZ.png')







# Some useful plotting code.

#
# plt.figure(1)
# plt.subplot(1, 3, 1)
# plt.plot(amp_rel,time,'k',linewidth=1)
#
# plt.fill_betweenx(time, 0, amp_rel, where=amp_rel >= 0, facecolor=[1, 0.4, 0.4])
# plt.fill_betweenx(time, 0, amp_rel, where=amp_rel <= 0, facecolor=[0.4, 0.4, 1])
#
# # Plot the predicted arrivals for a given epi_dist
# phases = phases_to_plot
#
# # Loop through each of the phases to plot
# for t in range(len(phases)):
# print (phases[t])
#
# # Read in the predicted travel time differences from the appropriate file
# data = np.genfromtxt('../Input/Moveout_with_epicentral_distance/TT_'+str(phases[t])+'.dat')
# TT_curve_poly = np.polyfit(data[:,0], data[:,1],3)
# TT_curve = np.poly1d(TT_curve_poly)
# TT=TT_curve(dist)
# # Get the epicentral distance, set as x, and the travel time
# # differences, set as y
# y = TT
#
# # Plot the curves on the stack, annotating each with the name of thephase
# plt.plot(0, y, "x")
# plt.annotate(str(phases[t]),xy=(0,y),xytext=(10,-10),textcoords='offset points')
#
# plt.ylim([-150,150])
# plt.xlim([-1,1])
# plt.gca().invert_yaxis()
#
# plt.xlabel('Norm Amplitude')
# plt.ylabel('Time (Max amplitude = ' + str(P_time) + ' s)')
#
#
#
#
# #----------------PLOT VERTICAL--------------------------------
# # 1 of 3 subplots (grid 1 row 3 columns)
# plt.subplot(1, 3,2)
#
# trace_time=UTCDateTime(seis[0].stats['starttime'])
# event_time=UTCDateTime(seis[0].stats['event'].origins[0].time)
# P_TT=seis[0].stats.traveltimes['P']
# tshift=trace_time-event_time
#
# vertical = seis.select(channel='*HZ')[0]
# vertical.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
# windowed=vertical[np.where(vertical.times()+tshift>P_TT-150) and np.where(vertical.times()+tshift<P_TT+150)]
# norm=np.max(np.abs(windowed))
# plt.plot(vertical.data/norm,vertical.times()+tshift-P_TT, 'k')
# plt.plot(0,0,'g^')
# plt.ylim([-150,150])
# plt.xlim([-1,1])
# plt.gca().invert_yaxis()
# plt.xlabel('Vertical')
# plt.ylabel('Time (s)')
# bbox_props = dict(boxstyle="square,pad=0.1", fc="white", ec="r", lw=1)
# plt.annotate(str(SNR_V),xy=(-0.8, 140), xytext=(-0.8, 140), color='red', fontsize=10, va='center', bbox=bbox_props)
#
#
# #----------------PLOT RADIAL--------------------------------
# # 3 of 3 subplots
# plt.subplot(1, 3, 3)
#
# radial = seis.select(channel='*HR')[0]
# radial.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
# windowed=radial[np.where(radial.times()+tshift>P_TT-150) and np.where(radial.times()+tshift<P_TT+150)]
# norm=np.max(np.abs(windowed))
# plt.plot(radial.data/norm, radial.times()+tshift-P_TT, 'k')
# plt.plot(0,0, 'g^')
# plt.ylim([-150,150])
# plt.xlim([-1,1])
# plt.gca().invert_yaxis()
# plt.xlabel('Radial')
# plt.ylabel('Time (s)')




