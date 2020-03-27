import subprocess
import time
import os
import exhibit

filename = exhibit.read_tag()
print(filename)

filename = os.getcwd() + '/videos/' + filename
print(filename)

omxprocess = subprocess.Popen(['omxplayer',filename], stdin = subprocess.PIPE, stdout = None, stderr = None, bufsize = 0)

time.sleep(5)

omxprocess.stdin.write(b' ')

time.sleep(5)

exhibit.close_process(omxprocess.pid)
