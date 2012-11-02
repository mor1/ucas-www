#!/usr/bin/env python
#
# Copyright (C) 2012 Richard Mortier <mort@cantab.net>.  All Rights
# Reserved.

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('ucas.ini')

import bottle
from bottle import Bottle, route, run, template
from bottle.ext import sqlite

app = Bottle()
plugin = sqlite.Plugin(dbfile=Config.get('database', 'dbfile'))
app.install(plugin)

@app.route('/hello/:name')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/dbtest/:item')
def dbtest(db, item):
    row = db.execute('SELECT * from items where name=?', item).fetchone()
    if row:
        return template('showitem', page=row)
    return HTTPError(404, "Page not found")

if __name__ == '__main__':
    bottle.debug(True)
    run(app, host='localhost', port=8080, reloader=True)
