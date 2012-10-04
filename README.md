=================
Logentries Logger
=================

This is a plugin library to enable logging to Logentries from the Python Logger. Logentries is a real-time log management service on the cloud. More info at https://logentries.com.

Setup
-----

To use this library, you must first create an account on Logentries. This will only take a few moments.

Install
-------

To install this library, use the following command:

`easy_install https://github.com/downloads/logentries/le_python/LogentriesLogger-0.2.tar.gz`

Usage
-----

    #!/usr/bin/env python

    from logentries import LeHandler
    import logging

    log = logging.getLogger('logentries')

    test = LeHandler(LOGENTRIES_TOKEN)

    log.addHandler(test)

    log.warn("Warning message")

Configure
---------

The parameter `LOGENTRIES_TOKEN` needs to be filled in to point to a file in your Logentries account.

In your Logentries account, create a new host, giving it a name that represents your app. Then create a logfile, selecting `Token TCP` as the source_type. This will print a Token UUID
beside the logfile. This is the value to use for `LOGENTRIES_TOKEN`.

You are now ready to start logging
