# Simple UCAS Signups Web App

Implements a simple web app for signups to UCAS open day small group discussions. Built on Python2.7 using [bottle.py][], and connected to the School of Computer Science webserver using AJP via [flup][].

[bottle.py]: http://bottlepy.org/
[flup]: https://pypi.python.org/pypi/flup

## Dependencies

Python 2.7 and associated libraries:

    $ pip install flup mysql-python bottle bottle-mysql

Of course, [bottle.py][] is a single-file web framework so could simply be copied directly into the relevant directory.

## Password hash creation

`sha1` hash of password string. Create on OSX as

    $ echo -n "password-string" | shasum

or in Python as

    >>> import hashlib
    >>> hashlib.sha1("password-string").hexdigest()

## Execution

Runs via `virtualpy` execution environment:

    $ source ~/localpy/bin/activate
    (localpy)$ cd ~/src/ucas-www
    (localpy)$ ( ps aux | \grep "^rmm.*python ./server.py" | grep -v grep | tr -s ' ' | cut -d ' ' -f 2 | xargs kill -9 )
    (localpy)$ ./server.py 1>ucas.$(date +%Y%m%d-%H%M%S).log 2>&1

Or, more usefully, via `screen`:

    $ screen  /usr/bin/env bash -c '. ~/localpy/bin/activate && cd src/ucas-www && ./server.py 1>ucas.$(date +%Y%m%d-%H%M%S).log 2>&1'

## Some useful queries

Connect to database:

    $ mysql -h mysql.cs.nott.ac.uk -u rmm -p
    (enter password)

    mysql> use rmm;

Retrieve list of upcoming bookings:

    mysql> select b.ucasid, b.name, s.staffid, s.spaces, d.date from `ucas.slots` as s inner join `ucas.bookings` as b on b.slotid=s.slotid inner join `ucas.dates` as d on s.dateid=d.dateid  where d.date >= NOW() order by date;
