# -*- coding: utf-8 -*-
#############################################################################
### COMPUTES RAY PATHS AND TRAVEL TIMES FOR DIFFERENT BODY PHASES ##########
#############################################################################


### Importing various python libraries
# numpy is a useful toolkit for scientific computations
import numpy as np
# matplotlib is a plotting toolkit
import matplotlib.pyplot as plt
# Obspy is a seismic toolkit
import obspy
from obspy.taup import TauPyModel
from obspy.taup import plot_travel_times
from obspy.taup import plot_ray_paths

import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
# More about the obspy routines we are using can be found here:
# https://docs.obspy.org/packages/obspy.taup.html

# more imports
import instaseis
from obspy import read
import sys,glob
import os.path
import obspy.signal.rotate
from obspy import UTCDateTime
import obspy.geodetics.base
import numpy as np
import obspy.geodetics
from IPython.display import HTML, Image
matplotlib.rc('animation', html='html5')
import matplotlib.patches as patches

# velocity model as a function of depth.
model = TauPyModel(model='ak135')

########################## SET PARAMETERS HERE #############################

# See phase naming information below or on the link above.
phases_to_plot =['P','Pdiff','PKP','PKIKP', 'PcP', 'PKKP', 'PP']
# min and max distances for the different phases to consider
# these can be chosen broadly (could be set 0-180 for all), it just slows down the code a bit.
rays_dist_min=[0, 100,100, 130, 0, 60, 0]
rays_dist_max=[110, 150,  181, 181, 160,180, 180 ]

# darkness of grey (lower is lighter here)
# this should be adapted, colors should change at reflection points
color_attenuation=[1.0, 0.5, 0.8, 0.8, 0.3, 0.8, 1.0]

# Set epicentral distance from Earthquake to Station - use station longitude to increase this 0-180 allowed
epi_dist=45

<<<<<<< HEAD
stlatitude=25
stlongitude=56.78
=======
# EQ and Receiver station latitude and longitude
evtlatitude=0
evtlongitude=0
stlatitude=0
stlongitude=epi_dist
>>>>>>> 8c85c597b36d3336d7925876bc32c1ab81dfb0b1

# depth of earthquake in km
depth_earthquake = 10.

# Waveform characteristics
Normalise_Waveform=True                             # Normalise waveform amplitude
Filter_Waveform=False                               # Filter waveform with bandpass filter; params below
fmin=0.02
fmax=0.5
Time_window=3600                                    # Length of seismogram time window (s)

# Output handling
Output_Location     =   '../wavefront_movie_outputs/'
waveform_name_str   =   'seis_synth'
gif_name_str        =   'seis_movie'

Filename_PICKLE     =   Output_Location + str(epi_dist) + '_'+ waveform_name_str + '.PICKLE'
Filename_GIF        =   Output_Location + gif_name_str + '.gif'

if not os.path.exists(Output_Location):
    os.makedirs(Output_Location)


################ Wavefront movie #######################

# radius of Earth in km
radius = 6371.

# regular time array in s, 1 s resolution
time = np.arange(0., Time_window)

# calculate through and save ray paths in interpolated time domain
save_paths=[]
for p, phase  in enumerate(phases_to_plot):
    dists_collected=[]
    depths_collected=[]
    for r, dist in enumerate(np.arange(rays_dist_min[p], rays_dist_max[p], 1)): # resolution could be improved here
        # get raypaths
        rays = model.get_ray_paths(depth_earthquake, dist, phase_list=[phase])
        # Loop through rays found, some phases have multiple paths
        for ray in rays:
            # Interpolate to regulard time array
            dists = np.interp(time, ray.path['time'], ray.path['dist'], left = np.nan, right = np.nan)
            depths = np.interp(time, ray.path['time'], ray.path['depth'], left = np.nan, right = np.nan)
            # save paths
            dists_collected.append(dists)
            depths_collected.append(depths)
    save_paths.append([np.array(dists_collected),np.array(depths_collected)])

save_paths=np.array(save_paths)

#interpolater for plotter
intp = matplotlib.cbook.simple_linear_interpolation

# save wave fronts to the left and right
lines_left=[]
lines_right=[]

# start plot for t= 0
fig = plt.figure(figsize =(10,5))
# define polar subplot
ax = plt.subplot(1,2,1, polar = True)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])

# plot paths for t=0 (these are all at the earthquake
t=0
for p in range(len(save_paths)):
    dists_collected=save_paths[p,0]
    depths_collected=save_paths[p,1]
    front_dist= dists_collected[:,t] # Cut at single time across all paths
    front_depth = depths_collected[:, t] # Cut at single time across all paths
    # set colour
    col = ((1-(1.-float(0)/Time_window )*color_attenuation[p])+0.5)/1.5
    cols = [col, col,col]
    # plot line towards the right side
    line, = ax.plot(intp(front_dist, 100),radius - intp(front_depth, 100),color =cols )
    lines_right.append(line)
    # mirror line towards the left
    line, = ax.plot(intp(-1.*front_dist, 100),radius - intp(front_depth, 100),color =cols)
    lines_left.append(line)

# add discontinuities
discons = rays.model.s_mod.v_mod.get_discontinuity_depths()
ax.set_yticks(radius - discons)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())

# Pretty earthquake marker.
ax.plot([0], [radius - depth_earthquake],
        marker="*", color="#FEF215", markersize=20, zorder=10,
        markeredgewidth=1.5, markeredgecolor="0.3",
        clip_on=False)

ax.set_rmax(radius)
ax.set_rmin(0.0)

################ Generate seismogram. #######################

# Generating seismogram
def generate_seismogram(evtlatitude=0, evtlongitude=0, evtdepth=10, stlatitude=0,stlongitude=90,Norm_Wave=False,Filt_Wave=False,File_Wave='temp.PICKLE'):

        # Load database with Green Functions
        # db = instaseis.open_db("syngine://prem_a_2s")
        # db = instaseis.open_db("syngine://ak135f_1s")
        db = instaseis.open_db("syngine://ak135f_2s ")
        EQ_time=UTCDateTime('2004-12-26 00:00:00')
        
	# Other option for source definition
        source = instaseis.Source.from_strike_dip_rake(latitude=evtlatitude, longitude=evtlongitude, depth_in_m=evtdepth*1000, strike=60,dip=30, rake=90, M0=1E12, sliprate=1, dt=0.1, origin_time=EQ_time)

	# Station parameters
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
        st[0].stats['evdp'] = evtdepth # want EQ depth in km in PICKLE (do not x1000)
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
        
        # Make sure seismogram is correct length
        # st.trim(starttime=start, endtime=end, pad=True, nearest_sample=True, fill_value=0)

        # Normalize waveform amplitude for each trace
        if Norm_Wave:
            for channel in st:
                print(channel.stats['channel'])
                print(channel.stats['starttime'], channel.stats['endtime'])
                windowed=channel[np.where(channel.times() >= 0) and np.where(channel.times() <= Time_window )]
                norm=np.max(np.abs(windowed))
                channel.data=channel.data/norm


        #OVERWRITES previous PICKLE with new synthetics

        if Filt_Wave: 
            st.filter('bandpass', freqmin=fmin,freqmax=fmax, corners=2, zerophase=True)
            st.taper(max_length=5, max_percentage=0.02, type='cosine')

        st.write(File_Wave,format='PICKLE')  
        return

######################################################################

# Call above function
print('Calling synthetic seismogram generation')
generate_seismogram(evtlatitude=evtlatitude, 
                    evtlongitude=evtlongitude, 
                    evtdepth=depth_earthquake, 
                    stlatitude=stlatitude,
                    stlongitude=stlongitude,
                    Norm_Wave=Normalise_Waveform,
                    Filt_Wave=Filter_Waveform,
                    File_Wave=Filename_PICKLE)


# Read the generated seismogram in
try:
    st1=read(Filename_PICKLE,format='PICKLE')
    print(st1)
except:
    st1=read('temp.PICKLE',format='PICKLE')
ax1 = plt.subplot(1, 2, 2)
st1Z=st1.select(channel='BXZ')
seis_times = st1Z[0].times("matplotlib")
data = st1Z[0].data
seis, = ax1.plot(seis_times, data, "r-")
ax1.xaxis_date()
fig.autofmt_xdate()


#Add rectangle as reference frame
direct_P_travel_time = model.get_travel_times(source_depth_in_km=depth_earthquake, distance_in_degree=epi_dist, phase_list=['P'])[0].time # time for direct P wave to reach station
bottom, top = plt.ylim()
height  = top - bottom
start, end = plt.xlim()
duration = end - start
<<<<<<< HEAD
width = duration/5
start_time=(direct_P_travel_time/3600)*duration # converting direct-P travel time to seismogram time units
rect = patches.Rectangle((end-start_time-width,bottom), width, height, linewidth=1,facecolor='None', edgecolor='black', zorder=10)
=======
width = duration/10
start_time=(direct_P_travel_time/Time_window)*duration # converting direct-P travel time to seismogram time units
rect = patches.Rectangle((end-start_time-width,bottom), width, height, linewidth=0.5,facecolor='None', edgecolor='black', zorder=10)
>>>>>>> 8c85c597b36d3336d7925876bc32c1ab81dfb0b1
start_index = np.where(seis_times>=rect.xy[0])[0][0] # time index where rectangle starts
end_index = np.where(seis_times>=(rect.xy[0]+width))[0][0] # time index where rectangle finishes
ax1.add_patch(rect)

<<<<<<< HEAD
#Generating text boxes and arrival times
boxes = np.array([])
arrival_times = np.array([])
for phase in phases_to_plot:
    arrival = model.get_travel_times(source_depth_in_km=depth_earthquake, distance_in_degree=stlatitude, phase_list=[phase])
    if len(arrival) > 0:
       textstr = 'Current phase: ' + phase
       boxes = np.append(boxes, textstr)
       arrival_times = np.append(arrival[0].time, arrival_times)
arrival_times = np.array([round(a) for a in arrival_times])
currenttextbox = None # current text box to display

frame_number = 250 # max 3600
=======
frame_number = Time_window
>>>>>>> 8c85c597b36d3336d7925876bc32c1ab81dfb0b1
frame_rate = 25 # fps
count = 0 # counter to track how long a text box should appear for

def animate(t, lines_left, lines_right):
    '''
        Function updates lines with time
    '''
    global save_paths
    global count, currenttextbox, boxes, arrival_times

    for l,line in enumerate(lines_right):
        dists_collected=save_paths[l,0]
        depths_collected=save_paths[l,1]
        front_dist= dists_collected[:,t]
        front_depth = depths_collected[:, t]
        # update line to the right
        line.set_xdata(intp(front_dist,100))
        line.set_ydata(radius - intp(front_depth,100))
        # mirror update for lines to left
        lines_left[l].set_xdata(intp(-1.*front_dist,100))
        lines_left[l].set_ydata(radius - intp(front_depth,100))
        # update colour
        col = ((1-(1.-float(t)/Time_window )*color_attenuation[l])+0.5)/1.5
        cols = [col, col,col]
        line.set_color(cols)
        lines_left[l].set_color(cols)

    new_data = np.zeros(data.shape)
    speed = len(data)/Time_window # pieces of data per frame
    if t < len(data)/speed: # seismogram moving into frame
        new_data = np.array(data[:round(speed*(t))]) # removing data off the edge of the frame
        new_data = np.pad(new_data, (len(data)-len(new_data),0), mode='constant') # padding out with zeros
        new_data = new_data[start_index:end_index] # removing data outisde of the reference zone
        new_data = np.pad(new_data, (start_index, len(data)-end_index), mode='constant') # padding out with zeros
    elif t < (2*len(data))/speed: # seismogram moving out of frame
        new_data = np.array(data[round(speed*(t)) - len(data):])
        new_data = np.pad(new_data, (0,len(data)-len(new_data)), mode='constant')
        new_data = new_data[start_index:end_index]
        new_data = np.pad(new_data, (start_index, len(data)-end_index), mode='constant')
    else:
        new_data = np.zeros(data.shape)

    # Checking to see if we should add a text box
    if np.isin(t, arrival_times):
        currenttextbox = boxes[0]
        print(currenttextbox)
        print(t)
        boxes = np.roll(boxes, 1)
        arrival_times = np.delete(arrival_times, np.where(arrival_times==t)[0])
        count = 75
    if count == 0:
        currenttextbox = None
        box.remove()
    else:
       count -= 1

    seis.set_data(seis_times, new_data) # updating seismogram
    ax1.add_patch(rect) # adding stationary rectangle
    if currenttextbox is not None:
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        box = ax1.text(1, 1, currenttextbox, transform=ax.transAxes, fontsize=14, bbox=props)
    
    return(line,seis)

# Sets up animation
animation = FuncAnimation(
                          # Your Matplotlib Figure object
                          fig,
                          # The function that does the updating of the Figure
                          animate,
                          # Frame information (here just frame number)
                          frame_number,
                          # Extra arguments to the animate function
                          fargs=[lines_left, lines_right],
                          # Frame-time in ms; i.e. for a given frame-rate x, 1000/x
                          interval=1000/frame_rate
                          )

# to save as GIF :
animation.save(Filename_GIF, writer=PillowWriter(fps=frame_rate))
# animation.save(Filename_GIF, writer='imagemagick')

