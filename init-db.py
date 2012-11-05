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

import MySQLdb

Create_user = False
Create_tables = False
Reset = True

if __name__ == '__main__':

    db = MySQLdb.connect(
        host=Config.get("database", "host"),
        user=Config.get("database", "user"), 
        passwd=Config.get("database", "pass"), 
        )
    dbc = db.cursor()

    if Create_user:
        ## as root
        dbc.execute("create user 'user'@'localhost' IDENTIFIED BY 'password'")
        dbc.execute("grant all privileges on ucas.* to 'user'@'localhost'")
        dbc.execute("""
create database if not exists `rmm`
  character set 'utf8'
  collate 'utf8_unicode_ci'
""")
        db.commit()

    if Create_tables:
        ## as user

        dbc.execute("""
create table if not exists `rmm`.`ucas.bookings` (
  ucasid varchar(32),
  name varchar(64),
  email varchar(128),
  slotid varchar(32)
)
""")

        dbc.execute("""
create table if not exists `rmm`.`ucas.staff` (
  staffid varchar(5),
  name varchar(32),
  email varchar(128),
  research varchar(128),
  modules varchar(64)
)
""")

        dbc.execute("""
create table if not exists `rmm`.`ucas.slots` (
  slotid varchar(32),
  slot datetime,
  room varchar(16),
  staffid varchar(5),
  spaces int default 6
)
""")

        db.commit()

    if Reset:
        print dbc.execute("""
insert into `rmm`.`ucas.staff` 
  (staffid, name, email, research, modules)
values
  ("bsl", "Brian Logan", "bsl@cs.nott.ac.uk", "Artificial intelligence", "G52APT, G54DIA"),
  ("nhn", "Henrik Nilsson", "nhn@cs.nott.ac.uk", "Programming languages", "G51FUN"),
  ("srb", "Steve Bagley", "srb@cs.nott.ac.uk", "Document engineering", "G51PRG, G53DOC"),
  ("bnk", "Boriana Koleva", "bnk@cs.nott.ac.uk", "Human computer interaction",
        "G51WPS")
""")

        db.commit()