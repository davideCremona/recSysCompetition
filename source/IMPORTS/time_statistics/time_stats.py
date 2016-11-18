import time
from datetime import datetime

time_start = 0
now = 0

def startTask(task):
    print "-------------------------"
    print "Start "+str(task)
    now = datetime.now()
    time_start = time.mktime(now.timetuple())

def finishTask(task):
    now = datetime.now()
    time_finish = time.mktime(now.timetuple())
    print "Finish "+str(task)+" in "+str(time_finish-time_start)