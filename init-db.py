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
Really_really = False
Add_for_Nov21 = False

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

    if Create_tables:
        ## as user

        if Really_really:
            print dbc.execute("drop table if exists `rmm`.`ucas.bookings`")
            db.commit()
            print dbc.execute("drop table if exists `rmm`.`ucas.slots`")
            db.commit()
            print dbc.execute("drop table if exists `rmm`.`ucas.staff`")
            db.commit()

        print dbc.execute("""
create table if not exists `rmm`.`ucas.staff` (
  staffid varchar(5) not null,
  staffname varchar(32) not null,
  research varchar(128),
  modules varchar(64),
  primary key (staffid)
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

    if Add_for_Nov21:
        print dbc.execute("""
insert into `rmm`.`ucas.staff` 
  (staffid, staffname, research, modules)
values
  ("bsl", "Brian Logan", "Artificial Intelligence", "G52APT, G54DIA"),
  ("nhn", "Henrik Nilsson", "Programming Languages", "G51FUN"),
  ("srb", "Steve Bagley", "Document Engineering", "G51PRG, G53DOC"),
  ("bnk", "Boriana Koleva", "Human Computer Interaction",
        "G51WPS")
""")

        print dbc.execute("""
insert into `rmm`.`ucas.slots`
  (slot, room, staffid, spaces)
values
  ("2012-11-21 11:00", "C1", "bsl", 8),
  ("2012-11-21 11:00", "C80", "nhn", 8),
  ("2012-11-21 11:00", "Exchange", "srb", 8),
  ("2012-11-21 11:00", "Atrium", "bnk", 8)
""")

    db.commit()

