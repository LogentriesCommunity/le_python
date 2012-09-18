=================
Logentries Logger
=================

This is a plugin library to enable logging to Logentries from the Python Logger. Logentries is a real-time log management service on the cloud. More info at https://logentries.com. Package source and instructions can also be found at https://github.com/logentries/le_python

Setup
-----

To use this library, you must first create an account on Logentries. This will only take a few moments.

Install
-------

To install this library, use the following command:

`easy_install https://github.com/downloads/MarkLC/le_python/LogentriesLogger-0.1.tar.gz`

Usage
-----

    #!/usr/bin/env python

    from logentries import LeHandler
    import logging

    log = logging.getLogger('')

    test = LeHandler(LOGENTRIES_ACCOUNT_KEY, LOGENTRIES_LOCATION)

    log.addHandler(test)

    log.info("Info message")
    log.warn("Warning message")`

Configure
---------

The two parameters `LOGENTRIES_ACCOUNT_KEY` and `LOGENTRIES_LOCATION` need to be filled in to sync with your Logentries account.

`LOGENTRIES_ACCOUNT_KEY` can be obtained by clicking Account in the Logentries UI and clicking Account Key on the right hand side. Simply copy and paste this value as a string.

`LOGENTRIES_LOCATION` is the name of your host followed by the name of your logfile on Logentries in the following format 'hostname/logname'.

To create the host, log into your Logentries account and click New on the top right corner. The name you give it is what you will use in the above parameter. For logname you do not need to create a log in the UI. Simply enter a name and it will be created when the first log events are received.

Example:  `'myapp/debug'` for a host named myapp and a logfile named debug

You are now ready to start logging
