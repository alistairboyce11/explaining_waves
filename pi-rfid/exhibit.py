#!/usr/bin/env python







def open_screensaver():
	'''
	This function opens an image and keeps it open in the background
	It also returns a pid so that it can be closed later
	'''
	
	#Import relevant modules
	import subprocess
	import os

	#Define image location
	im_path = os.getcwd() + '/screens/home_screen.png'

	#Display image with Eye of Gnome
	proc = subprocess.Popen('eog -f ' + im_path, shell = True)

	#Obtain pid number
	pid = proc.pid

	return pid





def close_process(pid):
	'''
	This function closes a process, detailed by the pid number
	'''

	#import modules
	import psutil

	#Kill process AND close window
	pobj = psutil.Process(pid)
	for c in pobj.children(recursive = True):
		c.kill()
	pobj.kill()
	






def read_tag():
	'''
	This function continually reads the tag and returns the data on the tag
	'''

	#Import relevant modules
	import RPi.GPIO as GPIO
	from mfrc522 import SimpleMFRC522

	#Define reader
	reader = SimpleMFRC522()

	#Try to read
	try:
		id, text = reader.read()

	#Cleanup GPIO - MUST BE DONE
	finally:
		GPIO.cleanup()

	#Remove whitespace
	return text.strip()






def play_vid(filename, end_delay):
	'''
	This function plays a video as specified by the filename.
	It will also pause at the end for a time given by end_delay in seconds
	'''

	#Import relevant modules
	import subprocess
	import time
	import os

	#Modify filename
	filename = os.getcwd() + '/videos/' + filename

	try:
		#Get length of video
		x = subprocess.check_output('mediainfo ' + filename, shell = True)
		x = x.decode('utf-8')
		x = x.split('\n')
		for i in range(len(x)):
			if 'Duration' in x[i]:
				duration = x[i].split(':')[1]
				break

		duration = duration.strip()
		duration = duration.split('s')
		seconds = duration[0].strip()
		milliseconds = duration[1][0:-1].strip()
		duration = float(seconds + '.' + milliseconds)
		
		#Call totem to play video
		proc = subprocess.Popen(['omxplayer',filename], stdin = subprocess.PIPE, stdout = None, stderr = None, bufsize = 0)
		
		#Wait till end of video and pause
		time.sleep(duration - 1)
		proc.stdin.write(b' ')
		time.sleep(end_delay)

		#Kill process AND close window
		close_process(proc.pid)

	except:
		#Raise error screen to retry
		error_screen()





def error_screen():
	'''
	This function presents an error screen should an error occur
	It will simply ask the user to present the tag again
	'''
	
	#Import relevant modules
	import subprocess
	import time
	import os

	#Define path to error screen
	im_path = os.getcwd() + '/screens/error_screen.png'

	#Display image with Eye of Gnome
	proc = subprocess.Popen('eog -f -n ' + im_path, shell = True)

	#Wait for a number of seconds
	time.sleep(3.)
	read_tag()

	#Close error sceen
	close_process(proc.pid)
	



def wait_screen(filename, time):
	'''
	This function displays a temporary screen for a time
	'''
	
	#Import relevant modules
	import subprocess
	import time
	import os

	#Define path to screen
	im_path = os.getcwd() + '/screens/' + filename

	#Display image with Eye of Gnome
	proc = subprocess.Popen('eog -f -n ' + im_path, shell = True)

	#Wait for a number of seconds
	time.sleep(time)

	#Close sceen
	close_process(proc.pid)


