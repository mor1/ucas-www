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

ROOT = Config.get("server", "root")
STATIC_FILES = ('favicon.ico', 'robots.txt', 'css/ucas.css',)

SLOTS_SQL = "SELECT `ucas.slots`.*, `ucas.staff`.* "\
    + "  FROM `ucas.slots` "\
    + "  INNER JOIN `ucas.staff` "\
    + "  ON `ucas.slots`.staffid = `ucas.staff`.staffid "\
    + "  WHERE `ucas.slots`.spaces > 0 "\
    + "  ORDER BY `ucas.slots`.slot, `ucas.slots`.spaces DESC"

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

@app.post('/')
@app.get('/')
def retrieve_booking(db, ucasid=None, name=None):
    '''Retrieve existing booking, indexed by <ucasid> and <name>.'''

    bcs = [{ 's': "Home", 'l': ROOT, }]
                                     
    booking = error = ucasid = None
    if request.method == "POST":
        ucasid = request.forms.ucasid
        name = request.forms.name
    else:
        ucasid = request.query.ucasid
        name = request.query.name
    
    if not ucasid: # Entry page, permitting booking retrieval
        return template('root', 
                        root=ROOT, breadcrumbs=bcs, error=None, booking=None)
    
    cmd = "SELECT `ucas.bookings`.*, `ucas.slots`.*, `ucas.staff`.* "\
        + "  FROM `ucas.bookings` "\
        + "  INNER JOIN `ucas.slots` "\
        + "    ON `ucas.bookings`.slotid = `ucas.slots`.slotid "\
        + "  INNER JOIN `ucas.staff` "\
        + "    ON `ucas.slots`.staffid = `ucas.staff`.staffid "\
        + "  WHERE `ucas.bookings`.ucasid = %s AND `ucas.bookings`.name = %s"
    n = db.execute(cmd, (ucasid, name))
    if n != 1: error = "booking-mismatch"
    else:
        booking = db.fetchone()
        if not booking: error = "booking-fetch"

    return template('root', 
                    root=ROOT, breadcrumbs=bcs, error=error, booking=booking)

@app.get('/<filename:path>')
def static(filename): 
    '''Retrieve static resource.'''

    if filename in STATIC_FILES:
        return bottle.static_file(filename, root='./static')
    return bottle.HTTPError(404, "Page not found")            

@app.get('/signup')
def signup(db):
    '''Display signup form.'''
    
    bcs = [{ 's': "Home", 'l': ROOT, },
           { 's': "Signup", 'l': "/signup" },
           ]

    db.execute(SLOTS_SQL)
    slots = db.fetchall()

    return template('signup', 
                    root=ROOT, breadcrumbs=bcs, error=None, slots=slots)

@app.post('/signup')
def do_signup(db):
    '''Create booking.'''

    booking = error = None
    
    ucasid = request.forms.ucasid
    name = request.forms.name
    email = request.forms.email
    slotid = request.forms.slotid

    cmd = "SELECT * FROM `ucas.bookings` WHERE `ucasid`=%s"
    n = db.execute(cmd, (ucasid, ))
    if n == 0:
        cmd = "UPDATE `ucas.slots` "\
            + "SET `spaces` = `spaces`-1 WHERE `slotid`=%s AND `spaces`>0"
        n = db.execute(cmd, (slotid,))
        if n != 1:
            db.execute(SLOTS_SQL)
            slots = db.fetchall()
            return template(
                'signup', root=ROOT, error="booking-slot-death", slots=slots)

        cmd = "INSERT INTO `ucas.bookings` VALUES (%s, %s, %s, %s)"
        db.execute(cmd, (ucasid, name, email, slotid,))
        
    else:
        booking = db.fetchone()
        if (booking
            and ((len(name) > 0 and booking['name'] == name)
                 or (len(email) > 0 and booking['email'] == email)
                 )):
            cmd = "UPDATE `ucas.slots` "\
                + "SET `spaces` = `spaces`+1 WHERE `slotid`=%s"
            db.execute(cmd, (booking['slotid'],))
            
            cmd = "UPDATE `ucas.slots` "\
                + "SET `spaces` = `spaces`-1 "\
                + "WHERE `slotid`=%s AND `spaces`>0"
            db.execute(cmd, (slotid,))

            cmd = "UPDATE `ucas.bookings` "\
                + "SET `name`=%s, `email`=%s, `slotid`=%s "\
                + "WHERE `ucasid`=%s AND (`name`=%s OR `email`=%s)"
            db.execute(cmd, (name, email, slotid, ucasid, name, email))

        else:
            db.execute(SLOTS_SQL)
            slots = db.fetchall()
            return template(
                'signup', root=ROOT, error="booking-update", slots=slots)

    from urllib import urlencode
    return redirect('%s?%s' % (
            ROOT, urlencode({'ucasid':ucasid, 'name':name }),))

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, reloader=True, debug=True)
