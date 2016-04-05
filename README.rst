Logentries Logger
=================

This is a plugin library to enable logging to Logentries from the Python Logger.
Additionally this plugin allows the user to get an overview of methods being executed,
their execution time, as well as CPU and Memory statistics.
Logentries is a real-time log management service on the cloud.
More info at https://logentries.com. Note that this plugin is
**asynchronous**.

Setup
-----

To use this library, you must first create an account on Logentries.
This will only take a few moments.

Install
-------

To install this library, use the following command:

``pip install logentries``

Usage
-----

.. code-block:: python

    #!/usr/bin/env python

    import logging
    from logentries import LogentriesHandler


    log = logging.getLogger('logentries')
    log.setLevel(logging.INFO)
    test = LogentriesHandler(LOGENTRIES_TOKEN)

    log.addHandler(test)

    log.warn("Warning message")
    log.info("Info message")

    sleep(10)


Usage with metric functionality
-------------------------------

.. code-block:: python

    import time
    import logging
    from logentries import LogentriesHandler, metrics


    TEST = metrics.Metric(LOGENTRIES_METRIC_TOKEN)

    @TEST.metric()
    def function_one(t):
        """A dummy function that takes some time."""
        time.sleep(t)

    if __name__ == '__main__':
            function_one(1)


Metric.Time()
-------------

This decorator function is used to log the execution time of given function. In the above example ``@TEST.time()`` will wrap ``function_one`` and send log message containing the name and execution time of this function.



Configure
---------

The parameter ``LOGENTRIES_TOKEN`` needs to be filled in to point to a
file in your Logentries account.

The parameter ``LOGENTRIES_METRIC_TOKEN`` needs to be filled in to point to a metric collection file in your Logentries account. However, please note that metric data can be send to LOGENTRIES_TOKEN and merged with other standard logs.

In your Logentries account, create a logfile, selecting ``Token TCP`` as
the source\_type. This will print a Token UUID. This
is the value to use for ``LOGENTRIES_TOKEN`` or ``LOGENTRIES_METRIC_TOKEN``.

The appender will attempt to send your log data over TLS over port 443,
otherwise it will send over port 80.

You are now ready to start logging
