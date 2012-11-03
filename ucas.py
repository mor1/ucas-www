#!/usr/bin/env python
#
# Copyright (c) 2012, Richard Mortier <mort@cantab.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('ucas.ini')

import bottle, bottle_mysql
from bottle import request, template, redirect

app = bottle.Bottle()
plugin = bottle_mysql.Plugin(
    dbhost=Config.get('database', 'host'),
    dbuser=Config.get('database', 'user'),
    dbpass=Config.get('database', 'pass'), 
    dbname=Config.get('database', 'name')
    )
app.install(plugin)

@app.get('/')
def root(): 
    '''Entry page, permitting booking retrieval.'''

    return template('root', error=None, booking=None, ucasid=None)

@app.post('/')
@app.get('/signup/<ucasid:re:[0-9]{3}-[0-9]{3}-[0-9]{4}>')
def retrieve_booking(db, ucasid=None):
    '''Retrieve existing booking, indexed by UCAS ID.'''

    booking = error = None
    if not ucasid:
        ucasid = request.forms.ucasid
    name = request.forms.name
    email = request.forms.email
        
    cmd = "SELECT * FROM `ucas.applicants` WHERE `ucasid`=%s"
    n = db.execute(cmd, (ucasid,))
    if n == 1: 
        booking = db.fetchone()
        if not booking: 
            error = "booking"
        print booking
        if booking['name'] != name and booking['email'] != email:
            error = "booking-mismatch"
            booking = None
    
    else:
        error = "unknown-ucasid"

    return template('root', error=error, booking=booking, ucasid=ucasid)

@app.get('/<filename:path>')
def static(filename): 
    '''Retrieve static resource.'''

    if filename in ('favicon.ico', 'robots.txt', 'css/ucas.css', ):
        return bottle.static_file(filename, root='./static')
    return bottle.HTTPError(404, "Page not found")            

@app.get('/signup')
def signup(db):
    '''Display signup form.'''
    
    slots = [ { 'value':'v', 'display':'d', },
              ]
    return template('signup', error=None, slots=slots)

@app.post('/signup')
def do_signup(db):
    '''Create booking.'''

    error = None
    slots = [ { 'value':'v', 'display':'d', },
              ]

    ucasid = request.forms.ucasid
    name = request.forms.name
    email = request.forms.email
    print ucasid, name, email

    cmd = "SELECT * FROM `ucas.applicants` WHERE `ucasid`=%s"
    n = db.execute(cmd, (ucasid,))
    if n == 0:
        cmd = "INSERT INTO `ucas.applicants` VALUES (%s, %s, %s)"
        db.execute(cmd, (ucasid, name, email,))
    else:
        booking = db.fetchone()
        if (email == booking['email']
            or name == booking['name']
            ):
            cmd = "UPDATE `ucas.applicants`" \
                + "SET `name`=%s, `email`=%s WHERE `ucasid`=%s"
            db.execute(cmd, (name, email, ucasid,))
        else:
            return template('signup', 
                            error="edit-booking-nomatch", slots=slots)
                           
    return redirect('/signup/%s' % (ucasid,))

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, reloader=True, debug=True)
