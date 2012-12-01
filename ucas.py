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

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s\n  %(message)s',
    filename=Config.get("server", "logfile"), 
    level=logging.INFO
    )

ROOT = Config.get("server", "root")
STATIC_FILES = ('favicon.ico', 'robots.txt', 'css/ucas.css',
                'img/glyphicons-halflings.png', )

BASE_URL = "http://modulecatalogue.nottingham.ac.uk/nottingham/asp/moduledetails.asp"
SLOTS_SQL = (
    "SELECT "
    + " slots.slotid, slots.slot, slots.room, slots.spaces, "
    + " staff.staffid, staff.staffname, staff.research "
    + "  FROM `ucas.slots` AS `slots` "
    + "  INNER JOIN `ucas.staff` AS `staff` "
    + "  ON `slots`.staffid = `staff`.staffid "
    + "  WHERE `slots`.spaces > 0 "
    + "  ORDER BY `slots`.slot, `slots`.spaces DESC"
    )

MODULES_SQL = (
    "SELECT "
    + " modules.staffid, modules.code, modules.crsid "
    + "FROM `ucas.modules` AS `modules` "
    )

import bottle, bottle_mysql, hashlib
from bottle import request, response, template, redirect, error

app = bottle.Bottle()
plugin = bottle_mysql.Plugin(
    dbhost=Config.get('database', 'host'),
    dbuser=Config.get('database', 'user'),
    dbpass=Config.get('database', 'pass'), 
    dbname=Config.get('database', 'name')
    )
app.install(plugin)

def validate_ucasid(ucasid=None):
    '''Accept any separators or junk, return properly formatted version.'''
    
    if not ucasid: return None

    ds = ''.join([ s for s in ucasid if s.isdigit() ])
    if len(ds) != 10: return None

    return "%s-%s-%s" % (ds[0:3], ds[3:6], ds[6:10])

def validate_name(name=None):
    '''Accept anything that's not blank.'''

    if not name: return None
    return name

def get_slots(db):
    db.execute(SLOTS_SQL)
    slots = db.fetchall()
    db.execute(MODULES_SQL)
    modules = db.fetchall()

    for slot in slots:
        slot['modules'] = [ m
                            for m in modules
                            if m['staffid'] == slot['staffid'] ]
    return slots

class Data:
    def __init__(self): ## rendering data, with defaults
        self.root = ROOT
        self.breadcrumbs = [ ("Home", ROOT,) ]
        self.error = None

@error(404)
@error(500)
def error(error):
    data = Data()
    return template('error', data=data, error=error)

@app.post('/')
@app.post('')
@app.get('/')
@app.get('')
def retrieve_booking(db, ucasid=None, name=None):
    '''Retrieve existing booking, indexed by <ucasid> and <name>.'''

    data = Data()

    booking = ucasid = name = None
    if request.method == "POST":
        ucasid = request.forms.ucasid
        name = request.forms.name
    else:
        ucasid = request.query.ucasid
        name = request.query.name

    logging.info("+ retrieve: ucasid='%s' name='%s'" % (ucasid, name))

    if not ucasid: 
        ## entry page, permitting booking retrieval
        logging.info("- retrieve: root page")
        return template('root', data=data, booking=booking)
    
    ucasid = validate_ucasid(ucasid)
    if not ucasid:
        ## mash data.error
        data.error = "ucasid-validation"
        logging.info("- retrieve: ucasid failed validation")
        return template('root', data=data, booking=booking)
    
    cmd = "SELECT `ucas.bookings`.*, `ucas.slots`.*, `ucas.staff`.* "\
        + "  FROM `ucas.bookings` "\
        + "  INNER JOIN `ucas.slots` "\
        + "    ON `ucas.bookings`.slotid = `ucas.slots`.slotid "\
        + "  INNER JOIN `ucas.staff` "\
        + "    ON `ucas.slots`.staffid = `ucas.staff`.staffid "\
        + "  WHERE `ucas.bookings`.ucasid = %s AND `ucas.bookings`.name = %s"
    n = db.execute(cmd, (ucasid, name))
    if n != 1: data.error = "booking-mismatch"
    else:
        booking = db.fetchone()
        if not booking: data.error = "booking-fetch"

    if data.error: logging.info("- retrieve: %s" % (data.error,))
    else:
        logging.info('- retreive: booking="%s"' % (booking,))

    return template('root', data=data, booking=booking)

@app.get('/<filename:path>')
def static(filename): 
    '''Retrieve static resource.'''

    logging.info("+- static: filename='%s'" % (filename,))
    if filename in STATIC_FILES:
        return bottle.static_file(filename, root='./static')
    return bottle.HTTPError(404, "Page not found")            

@app.get('/signup')
def signup(db):
    '''Display signup form.'''

    logging.info("+- signup: display form")

    data = Data()
    data.breadcrumbs.append(("Signup", "/signup"))

    return template('signup', data=data, slots=get_slots(db), base_url=BASE_URL)

@app.post('/signup')
def do_signup(db):
    '''Create booking.'''

    data = Data()
    booking = error = None
    
    ucasid = request.forms.ucasid
    name   = request.forms.name
    slotid = request.forms.slotid
    
    logging.info('+ signup: ucasid="%s" name="%s" slotid="%s"' % (
            ucasid, name, slotid))

    ucasid = validate_ucasid(ucasid)
    if not ucasid:
        data.error = "ucasid-validation"
        slots = get_slots(db)
        logging.info("- signup: ucasid failed validation")
        return template("signup", data=data, booking=booking, slots=slots, base_url=BASE_URL)

    name = validate_name(name)
    if not name:
        data.error = "name-validation"
        slots = get_slots(db)
        logging.info("- signup: name failed validation")
        return template("signup", data=data, booking=booking, slots=slots, base_url=BASE_URL)

    cmd = "SELECT * FROM `ucas.bookings` WHERE `ucasid`=%s"
    n = db.execute(cmd, (ucasid, ))
    if n == 0:
        cmd = "UPDATE `ucas.slots` "\
            + "SET `spaces` = `spaces`-1 WHERE `slotid`=%s AND `spaces`>0"
        n = db.execute(cmd, (slotid,))
        if n != 1:
            slots = get_slots(db)
            data.error = "booking-slot-death"
            logging.info("- signup: %s" % (data.error,))
            return template('signup', data=data, slots=slots, base_url=BASE_URL)

        cmd = "INSERT INTO `ucas.bookings` VALUES (%s, %s, %s)"
        db.execute(cmd, (ucasid, name, slotid,))
        
    else:
        booking = db.fetchone()
        if (booking and (len(name) > 0 and booking['name'] == name)):
            cmd = "UPDATE `ucas.slots` "\
                + "SET `spaces` = `spaces`+1 WHERE `slotid`=%s"
            db.execute(cmd, (booking['slotid'],))
            
            cmd = "UPDATE `ucas.slots` "\
                + "SET `spaces` = `spaces`-1 "\
                + "WHERE `slotid`=%s AND `spaces`>0"
            db.execute(cmd, (slotid,))

            cmd = "UPDATE `ucas.bookings` "\
                + "SET `slotid`=%s "\
                + "WHERE `ucasid`=%s AND `name`=%s)"
            db.execute(cmd, (slotid, ucasid, name))

        else:
            slots = get_slots(db)
            if not booking: data.error = "booking-fetch"
            else:
                data.error = "booking-mismatch"
            logging.info("- signup: %s" % (data.error,))
            return template('signup', data=data, slots=slots, base_url=BASE_URL)

    from urllib import urlencode
    params = urlencode({'ucasid':ucasid, 'name':name })
    logging.info("- signup: params='%s'" % (params,))
    return redirect('%s?%s' % (ROOT, params))

@app.get('/staff/login')
def staff_login(db):
    return '''<p>login</p>
              <form method="POST" action="/staff/login">
                <input name="password" type="password" />
                <input type="submit" />
              </form>'''

    # data = Data()
    # data.breadcrumbs.append(("Staff Signup", "/staff-signup"))
    # return template('signup', data=data, slots=get_slots(db), base_url=BASE_URL)

@app.post('/staff/login')
def staff_login_submit():
    
    def check_login(u, p):
        sha = hashlib.sha1(p).hexdigest()
        logging.info("P:'%s' SHA: %s" % (p,sha))
        return (sha == Config.get('www', 'pass'))

    name = request.forms.get('name')
    password = request.forms.get('password')
    if check_login(name, password):
        response.set_cookie("staff-signed-in", "True", 
                            httponly=True,
                            secret=Config.get('www', 'key'))
        return '''<p>Welcome! You are now logged in.</p>
                  <a href="/staff/signup">sign up</a>
                  <a href="/staff/logout">logout</a>
               '''
    else:
        return '''<p>Login failed</p><a href="/staff/login">login</a>'''

@app.get('/staff/logout')
def staff_logout():
    response.delete_cookie('staff-signed-in')
    return '''<p>logged out</p><a href="/staff/login">login</a>'''

@app.get('/staff/signup')
def staff_signup(db):
    signedin = bool(request.get_cookie(
        "staff-signed-in", secret=Config.get('www', 'key')))
    
    if signedin:
        return '''<p>welcome back</p>
                  <form method="POST" action="/staff/signup">
                    <input type="submit" />
                  </form>'''
    else:
        return '''You are not logged in. Access denied. <a href="/staff/login">login</a>'''

@app.post('/staff/signup')
def staff_signup_submit(db):
    return '''<p>Submitted!</p>'''

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080, reloader=True, debug=True)
