#Import all modules
import exhibit

#Display screensaver
screen_pid = exhibit.open_screensaver()

#Continually loop through the video playing
#Press ctrl + c to terminate script
while True:
	
	try:
		#Read the tag
		filename = exhibit.read_tag()

		#Play video and pause for 3 seconds at end
		exhibit.play_vid(filename, 3)

	except KeyboardInterrupt:
		print('Terminating script')		
		break

#Close screensaver
exhibit.close_process(screen_pid)
