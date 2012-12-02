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

import sys, ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('ucas.ini')

import MySQLdb

Create_user = False
Create_tables = True
Really_really = False
Add_staff = False
Add_slots = False
Add_dates = True
Add_modules = True

def create_user():
    ## as root
    host = Config.get("database", "host")
    user = Config.get("database", "user")
    passwd = Config.get("database", "pass")
    print """
mysql -h %s -u root -p <<__EOF
drop user rmm@localhost;
create user '%s'@'localhost' IDENTIFIED BY '%s';
grant all privileges on rmm.* to '%s'@'localhost';
create database if not exists rmm
  character set 'utf8'
  collate 'utf8_unicode_ci'
__EOF
""" % (host, user, passwd, user,)

def create_tables(dbc):
    if Really_really:
        print dbc.execute("drop table if exists `rmm`.`ucas.bookings`")
        db.commit()
        print dbc.execute("drop table if exists `rmm`.`ucas.slots`")
        db.commit()
        print dbc.execute("drop table if exists `rmm`.`ucas.staff`")
        db.commit()
        print dbc.execute("drop table if exists `rmm`.`ucas.modules`")
        db.commit()
        print dbc.execute("drop table if exists `rmm`.`ucas.dates`")
        db.commit()
        print dbc.execute("drop table if exists `rmm`.`ucas.signups`")
        db.commit()

    print dbc.execute("""
create table if not exists `rmm`.`ucas.dates` (
  dateid int not null auto_increment,
  date datetime not null,
  primary key (dateid)
)
""")
        
    print dbc.execute("""
create table if not exists `rmm`.`ucas.staff` (
  staffid varchar(5) not null,
  staffname varchar(32) not null,
  research varchar(128),
  primary key (staffid)
)
""")

    print dbc.execute("""
create table if not exists `rmm`.`ucas.signups` (
  dateid int not null,
  foreign key (dateid) references `ucas.dates`(dateid),
  staffid varchar(5) not null,
  foreign key (staffid) references `ucas.staff`(staffid)
)
""")
        
    print dbc.execute("""
create table if not exists `rmm`.`ucas.modules` (
  code varchar(6) not null,
  crsid varchar(6) not null,
  primary key (code),
  staffid varchar(5) not null,
  foreign key (staffid) references `ucas.staff`(staffid)
)
""")

    print dbc.execute("""
create table if not exists `rmm`.`ucas.slots` (
  slotid int not null auto_increment,
  slot datetime not null,
  room varchar(16) not null, 
  staffid varchar(5) not null,
  spaces int default 6, 
  primary key (slotid),
  foreign key (staffid) references `ucas.staff`(staffid)
)
""")

    print dbc.execute("""
create table if not exists `rmm`.`ucas.bookings` (
  ucasid varchar(32) not null,
  name varchar(64) not null,
  slotid int not null,
  foreign key (slotid) references `ucas.slots`(slotid)  
)
""")
    
def add_staff(dbc):
    print dbc.execute("""
insert into `rmm`.`ucas.staff` 
  (staffid, staffname, research)
values
  ("bsl", "Brian Logan", "artificial intelligence in general"),
  ("nhn", "Henrik Nilsson", "programming languages and second year group projects"),
  ("srb", "Steve Bagley", "how computers manipulate and process documents, and eBook technology"),
  ("bnk", "Boriana Koleva", "human computer interaction and third year projects")
""")

    print dbc.execute("""
insert into `rmm`.`ucas.modules`
  (staffid, code, crsid)
values
  ("bsl", "G52APT", "021245"),
  ("bsl", "G52DIA", "021226"),
  ("nhn", "G53CMP", "021224"),
  ("nhn", "G54FOP", "018385"),
  ("srb", "G53DOC", "021231"),
  ("srb", "G51PRG", "012192"),
  ("bnk", "G51WPS", "017011")
""") 

def add_slots(dbc):
    print dbc.execute("""
insert into `rmm`.`ucas.slots`
  (slot, room, staffid, spaces)
values
  ("2012-12-05 14:00", "Pod 1", "bnk", 7),
  ("2012-12-05 14:00", "Hub", "nhn", 7),
  ("2012-12-05 14:00", "Pod 3", "srb", 7),
  ("2012-12-05 14:00", "Pod 2", "bsl", 7)
""")

def add_dates(dbc):
    print dbc.execute("""
insert into `rmm`.`ucas.dates`
  (date)
values
  ("2012-11-21 14:00"),
  ("2012-12-05 14:00"),
  ("2013-01-23 14:00"),
  ("2013-01-30 14:00"),
  ("2013-02-06 14:00"),
  ("2013-02-13 14:00"),
  ("2013-02-16 14:00"),
  ("2013-02-20 14:00"),
  ("2013-02-27 14:00"),
  ("2013-03-06 14:00"),
  ("2013-03-13 14:00"),
  ("2013-03-16 14:00"),
  ("2013-03-20 14:00"),
  ("2013-03-27 14:00"),
  ("2013-04-03 14:00")
""")

if __name__ == '__main__':

    if Create_user: 
        create_user()
        sys.exit(0)

    db = MySQLdb.connect(
        host=Config.get("database", "host"),
        user=Config.get("database", "user"), 
        passwd=Config.get("database", "pass"), 
        )
    dbc = db.cursor()

    if Create_tables: create_tables(dbc)
    if Add_staff: add_staff(dbc)
    if Add_slots: add_slots(dbc)
    if Add_dates: add_dates(dbc)
    if Add_modules: add_modules(dbc)

    db.commit()
