VERSION = '0.1'

import logging
import Queue
import threading
import socket
import random
import time

# Size of the internal event queue
QUEUE_SIZE = 32768;
# Logentries API server address
LE_API = "api.logentries.com"
# Default port number for Logentries API server
LE_PORT = 80
# Default SSL port number for Logentries API server
LE_SSL_PORT = 443
# Minimal delay between attempts to reconnect in seconds
MIN_DELAY = 0.1
# Maximal delay between attempts to recconect in seconds
MAX_DELAY = 10
# LE appender signature - used for debugging messages
LE = "LE: "
# Error message displayed when wrong configuration has been detected
WRONG_CONFIG = "\n\nIt appears you forgot to customize your config file!\n\n"

def dbg(msg):
    print LE + msg

class SocketAppender(threading.Thread):
    def __init__(self, key, location):
	    threading.Thread.__init__(self)
	    self.daemon = True
	    self._conn = None
	    self._queue = Queue.Queue(QUEUE_SIZE)
	    self.key = key
	    self.location = location

    def openConnection(self):
	    log_header = "PUT /%s/hosts/%s/?realtime=1 HTTP/1.1\r\n\r\n" %(self.key, self.location)

	    self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	    self._conn.connect((LE_API, LE_PORT))
	    self._conn.send(log_header)

    def reopenConnection(self):
	    self.closeConnection()

	    root_delay = MIN_DELAY
	    while True:
		    try:
			    self.openConnection()
			    return
		    except Exception, e:
			    dbg("Unable to connect to Logentries")

		    root_delay *= 2
		    if(root_delay > MAX_DELAY):
			    root_delay = MAX_DELAY
		
		    wait_for = root_delay + random.uniform(0, root_delay)
		    
		    try:
			    time.sleep(wait_for)
		    except KeyboardInterrupt, e:
				raise KeyboardInterrupt
	
    def closeConnection(self):
	    if(self._conn != None):
		    self._conn.close()


    def run(self):
	    try:
		    # Open connection
		    self.reopenConnection()

		    # Send data in queue
		    while True:
			    # Take data from queue
				data = self._queue.get(block=True)

			    # Send data, reconnect if needed
				while True:
				    try:
					    self._conn.send(data)	
				    except socket.error, e:
					    self.reopenConnection()
					    continue
						
				    break
	    except KeyboardInterrupt, e:
		    dbg("Asynchronous socket client interrupted")

	    self.closeConnection()


class LeHandler(logging.Handler):
    def __init__(self, key, location):
	    logging.Handler.__init__(self)
	    self.key = key
	    self.location = location
	    format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s', '%a %b %d %H:%M:%S %Z %Y')
	    self.setFormatter(format)
	    self._thread = SocketAppender(key, location)
	    self._started = False

    def emit(self, record):

	    if not self._started:
		    dbg("Starting Asynchronous Socket Appender") 
		    self._thread.start()
		    self._started = True

	    msg = self.format(record).rstrip('\n')
	    msg += '\n'

	    self._thread._queue.put(msg)


    def close(self):
	    logging.Handler.close(self)
