=======================================
AIM Problem List Authentication (Proxy)
=======================================

Testing
-------

As couch.yinas.org is firewalled, to access port 8000 you need to use an SSH
tunnel e.g. as follows:

    ssh -L 8000:localhost:8000 couch.yinas.org

The proxy can then be accessed via:

    http://127.0.0.1:8000/pl/

I have set the backend host and port to 127.0.0.1 and 8888 respectively.  A
Tornado-based dummy backend is listening on this host and port.

Running the servers
-------------------

To run the Tornad+Django-based proxy, run the following:

    python /home/jason/aimauth/aimpl/proxy/run.py

To run the Tornado-based dummy backend, run the following:

    python /home/jason/aimauth/aimpl/dummy/run.py
