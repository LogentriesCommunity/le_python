""" This file contains some utils for connecting to Logentries
    as well as storing logs in a queue and sending them."""

VERSION = '2.0.7'

from logentries import helpers as le_helpers

import logging
import threading
import socket
import random
import time
import sys

lock = threading.Lock()

import certifi

# Size of the internal event queue
QUEUE_SIZE = 32768
# Logentries API server address
LE_API = "data.logentries.com"
# Port number for token logging to Logentries API server
LE_PORT = 80
LE_TLS_PORT = 443
# Minimal delay between attempts to reconnect in seconds
MIN_DELAY = 0.1
# Maximal delay between attempts to recconect in seconds
MAX_DELAY = 10
# LE appender signature - used for debugging messages
LE = "LE: "
# Error message displayed when an incorrect Token has been detected
INVALID_TOKEN = ("\n\nIt appears the LOGENTRIES_TOKEN "
                 "parameter you entered is incorrect!\n\n")
# Unicode Line separator character   \u2028
LINE_SEP = le_helpers.to_unicode('\u2028')


def dbg(msg):
    print(LE + msg)


class PlainTextSocketAppender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self._conn = None
        self._queue = le_helpers.create_queue(QUEUE_SIZE)

    def empty(self):
        return self._queue.empty()

    def open_connection(self):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.connect((LE_API, LE_PORT))

    def reopen_connection(self):
        self.close_connection()

        root_delay = MIN_DELAY
        while True:
            try:
                self.open_connection()
                return
            except Exception:
                dbg("Unable to connect to Logentries")

            root_delay *= 2
            if(root_delay > MAX_DELAY):
                root_delay = MAX_DELAY

            wait_for = root_delay + random.uniform(0, root_delay)

            try:
                time.sleep(wait_for)
            except KeyboardInterrupt:
                raise

    def close_connection(self):
        if self._conn is not None:
            self._conn.close()

    def run(self):
        try:
            # Open connection
            self.reopen_connection()

            # Send data in queue
            while True:
                # Take data from queue
                data = self._queue.get(block=True)

                # Replace newlines with Unicode line separator
                # for multi-line events
                if not le_helpers.is_unicode(data):
                    multiline = le_helpers.create_unicode(data).replace(
                        '\n', LINE_SEP)
                else:
                    multiline = data.replace('\n', LINE_SEP)
                multiline += "\n"
                # Send data, reconnect if needed
                while True:
                    try:
                        self._conn.send(multiline.encode('utf-8'))
                    except socket.error:
                        self.reopen_connection()
                        continue
                    break
        except KeyboardInterrupt:
            dbg("Logentries asynchronous socket client interrupted")

        self.close_connection()

try:
    import ssl
except ImportError:  # for systems without TLS support.
    SocketAppender = PlainTextSocketAppender
    dbg("Unable to import ssl module. Will send over port 80.")
else:
    class TLSSocketAppender(PlainTextSocketAppender):

        def open_connection(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = ssl.wrap_socket(
                sock=sock,
                keyfile=None,
                certfile=None,
                server_side=False,
                cert_reqs=ssl.CERT_REQUIRED,
                ssl_version=getattr(
                    ssl,
                    'PROTOCOL_TLSv1_2',
                    ssl.PROTOCOL_TLSv1
                ),
                ca_certs=certifi.where(),
                do_handshake_on_connect=True,
                suppress_ragged_eofs=True,
            )
            sock.connect((LE_API, LE_TLS_PORT))
            self._conn = sock

    SocketAppender = TLSSocketAppender


class LogentriesHandler(logging.Handler):
    def __init__(self, token, force_tls=False):
        logging.Handler.__init__(self)
        self.token = token
        self.good_config = True
        # give the socket 10 seconds to flush,
        # otherwise drop logs
        self.timeout = 10
        if not le_helpers.check_token(token):
            dbg(INVALID_TOKEN)
            self.good_config = False
        format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
                                   '%a %b %d %H:%M:%S %Z %Y')
        self.setFormatter(format)
        self.setLevel(logging.DEBUG)
        if force_tls:
            self._thread = TLSSocketAppender()
        else:
            self._thread = SocketAppender()

    @property
    def _started(self):
        return self._thread.is_alive()

    def flush(self):
        # wait for all queued logs to be send
        now = time.time()
        while not self._thread.empty():
            time.sleep(0.2)
            if time.time() - now > self.timeout:
                break

    def emit(self, record):
        # Reset stdout. See: http://docs.python.org/2/library/sys.html#sys.__stdout__
        sys.stdout = sys.__stdout__
        lock.acquire()
        try:
            if not self._started and self.good_config:
                dbg("Starting Logentries Asynchronous Socket Appender")
                self._thread.start()

            msg = self.format(record).rstrip('\n')
            msg = self.token + msg

            self._thread._queue.put(msg)
        finally:
            lock.release()

    def close(self):
        logging.Handler.close(self)
