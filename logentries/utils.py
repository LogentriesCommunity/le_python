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

import certifi

# LE appender signature - used for debugging messages
LE = "LE: "
# Error message displayed when an incorrect Token has been detected
INVALID_TOKEN = ("\n\nIt appears the LOGENTRIES_TOKEN "
                 "parameter you entered is incorrect!\n\n")


def dbg(msg):
    print(LE + msg)


class PlainTextSocketAppender(threading.Thread):
    def __init__(self, verbose=True, LE_API='data.logentries.com', LE_PORT=80, LE_TLS_PORT=443):
        threading.Thread.__init__(self)

        # Logentries API server address
        self.LE_API = LE_API

        # Port number for token logging to Logentries API server
        self.LE_PORT = LE_PORT
        self.LE_TLS_PORT = LE_TLS_PORT

        # Size of the internal event queue
        self.QUEUE_SIZE = 32768
        # Minimal delay between attempts to reconnect in seconds
        self.MIN_DELAY = 0.1
        # Maximal delay between attempts to recconect in seconds
        self.MAX_DELAY = 10
        # Unicode Line separator character   \u2028
        self.LINE_SEP = le_helpers.to_unicode('\u2028')

        self.daemon = True
        self.verbose = verbose
        self._conn = None
        self._queue = le_helpers.create_queue(self.QUEUE_SIZE)

    def empty(self):
        return self._queue.empty()

    def open_connection(self):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.connect((self.LE_API, self.LE_PORT))

    def reopen_connection(self):
        self.close_connection()

        root_delay = self.MIN_DELAY
        while True:
            try:
                self.open_connection()
                return
            except Exception:
                if self.verbose:
                    dbg("Unable to connect to Logentries")

            root_delay *= 2
            if(root_delay > self.MAX_DELAY):
                root_delay = self.MAX_DELAY

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
                        '\n', self.LINE_SEP)
                else:
                    multiline = data.replace('\n', self.LINE_SEP)
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
            if self.verbose:
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
            sock.connect((self.LE_API, self.LE_TLS_PORT))
            self._conn = sock

    SocketAppender = TLSSocketAppender


class LogentriesHandler(logging.Handler):
    def __init__(self, token, force_tls=False, verbose=True, format=None, LE_API="data.logentries.com", LE_PORT=80, LE_TLS_PORT=443):
        logging.Handler.__init__(self)
        self.token = token
        self.good_config = True
        self.verbose = verbose
        # give the socket 10 seconds to flush,
        # otherwise drop logs
        self.timeout = 10
        if not le_helpers.check_token(token):
            if self.verbose:
                dbg(INVALID_TOKEN)
            self.good_config = False
        if format is None:
            format = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
                                       '%a %b %d %H:%M:%S %Z %Y')
        self.setFormatter(format)
        self.setLevel(logging.DEBUG)
        if force_tls:
            self._thread = TLSSocketAppender(verbose=verbose, LE_API=LE_API, LE_PORT=LE_PORT, LE_TLS_PORT=LE_TLS_PORT)
        else:
            self._thread = SocketAppender(verbose=verbose, LE_API=LE_API, LE_PORT=LE_PORT, LE_TLS_PORT=LE_TLS_PORT)

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
        if self.good_config and not self._thread.is_alive():
            try:
                self._thread.start()
                if self.verbose:
                    dbg("Starting Logentries Asynchronous Socket Appender")
            except RuntimeError: # It's already started.
                if not self._thread.is_alive():
                    raise

        msg = self.format(record).rstrip('\n')
        msg = self.token + msg

        self._thread._queue.put(msg)

    def close(self):
        logging.Handler.close(self)
