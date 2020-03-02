# robots

Please use Python3.6 or above as code uses f strings for logging.

You can run this program like this:

python3 robots.py instructions.txt 


Optional mode parameter:

python3 roboys.py instructions.txt 3d

This will mean that if the robot goes past the end of the map, it returns to origin for that axis (this is calculated at the end of execution).


Program also runs a log file to log.txt so you can follow each robot step by step. Log file is wiped at each execution start.