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

`easy_install https://github.com/downloads/logentries/le_python/LogentriesLogger-0.1.tar.gz`

Usage
-----

    #!/usr/bin/env python

    from logentries import LeHandler
    import logging

    log = logging.getLogger('')

    test = LeHandler(LOGENTRIES_ACCOUNT_KEY, LOGENTRIES_HOSTNAME, LOGENTRIES_LOGNAME)

    log.addHandler(test)

    log.info("Info message")
    log.warn("Warning message")`

Configure
---------

Three parameters `LOGENTRIES_ACCOUNT_KEY`, `LOGENTRIES_LOCATION` and `LOGENTRIES_LOGNAME` need to be filled in to sync with your Logentries account.

`LOGENTRIES_ACCOUNT_KEY` can be obtained by clicking Account in the Logentries UI and clicking Account Key on the right hand side. Simply copy and paste this value as a string.

`LOGENTRIES_HOSTNAME` is the name of the host which you created in the Logentries UI.

To create the host, log into your Logentries account and click New on the top right corner. The name you give it is what you will use in the above parameter. 

`LOGENTRIES_LOGNAME` is the name you wish to use for the logfile inside above host. A logfile of the name you choose will be automatically created in the Logentries UI when the first
events are received.

You are now ready to start logging
