# Simple web app

### UNDER DEVELOPMENT. INCOMPLETE.

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

