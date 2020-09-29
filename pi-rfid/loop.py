#Import all modules
import exhibit
import sys

#Define videos to play
filenames = ['Core_Diff.mp4',
             'Disc_IC.mp4',
             'Disc_OC.mp4',
             'Full_Wavefield.mp4',
             'P_Tomo.mp4',
             'ScS_CMB.mp4']

#Continually loop through the video playing
#Press ctrl + c to terminate script
while True:

	#Loop through and play videos
	try:
		for filename in filenames:

			#Define the homescreen video
			home_screen = '_home.'.join(filename.split('.'))

			#Display the wait screens
			exhibit.play_vid_loop(home_screen,1)

			#Play video and pause for 3 seconds at end
			exhibit.play_vid_loop(filename, 3)
	except KeyboardInterrupt:
		print('Terminating script')		
		sys.exit()
