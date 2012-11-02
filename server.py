#!/usr/bin/env python
#
# Copyright (C) 2012 Richard Mortier <mort@cantab.net>.  All Rights
# Reserved.

import ConfigParser
Config = ConfigParser.RawConfigParser()
Config.read('ucas.ini')

from flup.server.ajp import WSGIServer
import ucas

WSGIServer(ucas.app, 
           scriptName=Config.get('server', 'scriptname'),
           bindAddress=(Config.get('server', 'host'), 
                        Config.getint('server', 'port'))
           ).run()
