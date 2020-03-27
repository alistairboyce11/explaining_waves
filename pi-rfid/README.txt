README file for Raspberry Pi museum video player
Created 20/02/20 S. Russell





########## Online Resources ##########
The following sites were used in the making of this project.

https://pimylifeup.com/raspberry-pi-rfid-rc522/
This site is a tutorial on how to set up the RFID RC522 chip, it is highly recommended to work through this while setting up this project.
This page crucially talks you through how to wire the reader and how to write and read the tags.





########## Requirements ##########
This project was done using a Raspberry Pi 4, although it should work on all Raspberry Pis

The following programs are used and should be installed beforehand:
	Eye of Gnome		Image display software
	Omxplayer		Video playing software - this is easily changed in the script if you know what you are doing
	Python3			Well, its python isn't it
	mediainfo		Used to get details about the media

The following non-standard python module is needed, this is discussed in the link in Online Resources
	MFRC522			Functions to interact with the RFID RC522 chip






########## Folder structure ##########
The basic folder structure is as follows
	./original_scripts/	A folder containing the original scripts, explained later
	./screens/		Contains any still images which are needed, also explained later
	./videos/		Contains the videos which are to be played, also explained later

Within the . directory are two scripts, exhibit.py and script.py. There is also this README file.






######### Scripts ##########
All scripts are .py files that can be run from the command line using the python3 command.

exhibit.py
Contained within the . directory. This file contains the basic functions needed.
Individual functions are described in this file

script.py
This is the main script that does all the work. This script calls its functions from exhibit.py.
It will continue looping until ctrl+c is pressed in the terminal.


original_scripts
Within this directory are three more scripts.

Write.py
This script is used to write data onto the tags, data is a string.

Read.py
This script reads data off of a tag and is the basis for the main script, script.py.

cleanup.py
This script cleans up. This must always occur after reading the tags. 
Usually it is run as part of the functions in exhibit.py, however in the case of major failure
or user termination then please run this script to be safe.






########## Media ##########
Images
These are within the ./screens/ directory and there are two images that are needed.
They are as named below and in png format, but again for anyone with a shred of coding know how these are easily changed.

home_screen.png
The image that is constantly in the background and that the screen displays when not playing a video.

error_screen.png
The image that is displayed when an error occurs to inform the user.


Videos
These are the videos which are played and are in the ./videos/ directory, the names of the videos are the strings of data stored on the tags.
We used mp4 although any format should be able to be used (provided it is compatible with the video player of course).
There is no limit to the number of videos you can have, depends how many tags you can afford really (and memory space on the Pi).






