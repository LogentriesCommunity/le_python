Logentries Logger
=================

This is a plugin library to enable logging to Logentries from the Python
Logger. Logentries is a real-time log management service on the cloud.
More info at https://logentries.com. Note that this plugin is
**asynchronous**.

Setup
-----

To use this library, you must first create an account on Logentries.
This will only take a few moments.

Install
-------

To install this library, use the following command:

``pip install logentrieslogger``

Usage
-----

::

    #!/usr/bin/env python

    from logentries import LogentriesHandler
    import logging

    log = logging.getLogger('logentries')
    log.setLevel(logging.INFO)
    test = LogentriesHandler(LOGENTRIES_TOKEN)

    log.addHandler(test)

    log.warn("Warning message")
    log.info("Info message")

    sleep(10)

Configure
---------

The parameter ``LOGENTRIES_TOKEN`` needs to be filled in to point to a
file in your Logentries account.

In your Logentries account, create a new host, giving it a name that
represents your app. Then create a logfile, selecting ``Token TCP`` as
the source\_type. This will print a Token UUID beside the logfile. This
is the value to use for ``LOGENTRIES_TOKEN``.

You are now ready to start logging
