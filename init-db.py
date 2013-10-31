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

def add_dates(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.dates` (
  dateid int not null auto_increment,
  date datetime not null,
  primary key (dateid)
)
""")

    print dbc.execute("""
insert into `rmm`.`ucas.dates`
  (date)
values
  ("2014-01-29 14:00"),
  ("2014-02-05 14:00"),
  ("2014-02-12 14:00"),
  ("2014-02-15 14:00"),
  ("2014-02-19 14:00"),
  ("2014-02-26 14:00"),
  ("2014-03-12 14:00"),
  ("2014-03-15 14:00"),
  ("2014-03-19 14:00"),
  ("2014-03-26 14:00"),
  ("2014-04-02 14:00")
""")

def add_modules(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.modules` (
  code varchar(6) not null,
  crsid varchar(6) not null,
  primary key (code)
)
""")

    print dbc.execute("""
insert into `rmm`.`ucas.modules`
  (code, crsid)
values
  ( "G50PRO", "018563" ),
  ( "G50WEB", "018561" ),
  ( "G51APS", "016658" ),
  ( "G51CSA", "002235" ),
  ( "G51DBS", "016949" ),
  ( "G51FSE", "021236" ),
  ( "G51FUN", "007252" ),
  ( "G51IAI", "016973" ),
  ( "G51MCS", "010233" ),
  ( "G51OOP", "021233" ),
  ( "G51PRG", "012192" ),
  ( "G51REQ", "021185" ),
  ( "G51TUT", "019438" ),
  ( "G51UST", "017010" ),
  ( "G51WPS", "017011" ),
  ( "G52ADS", "007255" ),
  ( "G52AFP", "018180" ),
  ( "G52APR", "021311" ),
  ( "G52APT", "021245" ),
  ( "G52CCN", "002252" ),
  ( "G52CON", "002253" ),
  ( "G52CPP", "022258" ),
  ( "G52GRP", "008415" ),
  ( "G52GUI", "018177" ),
  ( "G52HCI", "018255" ),
  ( "G52IFR", "021216" ),
  ( "G52IMO", "021246" ),
  ( "G52MAL", "018194" ),
  ( "G52PAS", "021232" ),
  ( "G52SEM", "021243" ),
  ( "G52TUT", "019439" ),
  ( "G53ARS", "023421" ),
  ( "G53ASD", "010236" ),
  ( "G53BIO", "015709" ),
  ( "G53CCT", "021220" ),
  ( "G53CMP", "021224" ),
  ( "G53COM", "002268" ),
  ( "G53CWO", "023374" ),
  ( "G53DOC", "021231" ),
  ( "G53ELC", "010238" ),
  ( "G53FUZ", "023393" ),
  ( "G53GRA", "021221" ),
  ( "G53IDA", "002272" ),
  ( "G53IDE", "004962" ),
  ( "G53IDJ", "008416" ),
  ( "G53IDS", "008462" ),
  ( "G53IDY", "019309" ),
  ( "G53KRR", "018195" ),
  ( "G53NMD", "021217" ),
  ( "G53OPS", "002276" ),
  ( "G53ORO", "018252" ),
  ( "G53SEC", "018176" ),
  ( "G53SQM", "022254" ),
  ( "G54999", "022992" ),
  ( "G54ACC", "021237" ),
  ( "G54ADM", "021235" ),
  ( "G54ALG", "021249" ),
  ( "G54ARC", "021250" ),
  ( "G54CCS", "022256" ),
  ( "G54CON", "021816" ),
  ( "G54DIA", "021226" ),
  ( "G54DMT", "021183" ),
  ( "G54FOP", "018385" ),
  ( "G54FPP", "021251" ),
  ( "G54GRP", "021788" ),
  ( "G54IHC", "021190" ),
  ( "G54INT", "021787" ),
  ( "G54MDP", "021255" ),
  ( "G54MET", "021188" ),
  ( "G54MGA", "023468" ),
  ( "G54MGP", "021253" ),
  ( "G54MIA", "023470" ),
  ( "G54MIP", "021254" ),
  ( "G54MXR", "021189" ),
  ( "G54ORM", "021489" ),
  ( "G54PDC", "021257" ),
  ( "G54PLP", "020241" ),
  ( "G54PRG", "021227" ),
  ( "G54PRO", "019348" ),
  ( "G54RP2", "022041" ),
  ( "G54RPS", "020837" ),
  ( "G54SAI", "022270" ),
  ( "G54SIM", "021202" ),
  ( "G54SUM", "021817" ),
  ( "G54UBI", "019275" ),
  ( "G54URP", "020240" ),
  ( "G64ADS", "018384" ),
  ( "G64DBS", "012353" ),
  ( "G64DEC", "023529" ),
  ( "G64HCI", "022388" ),
  ( "G64ICP", "006637" ),
  ( "G64INC", "013184" ),
  ( "G64MIT", "006640" ),
  ( "G64OOS", "009759" ),
  ( "G64PIT", "013747" ),
  ( "G64PMI", "013746" ),
  ( "G64PRE", "018518" ),
  ( "G64SPM", "013183" ),
  ( "G64SWE", "009760" )
""")

def add_staff(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.staff` (
  staffid varchar(5) not null,
  staffname varchar(32) not null,
  research varchar(128),
  primary key (staffid)
)
""")

    print dbc.execute("""
insert into `rmm`.`ucas.staff`
  (staffid, staffname, research)
values
  ("bsl", "Brian Logan", "artificial intelligence in general"),
  ("nhn", "Henrik Nilsson", "programming languages and second year group projects"),
  ("srb", "Steve Bagley", "how computers manipulate and process documents, and eBook technology"),
  ("bnk", "Boriana Koleva", "human computer interaction and third year projects")
""")

def add_teaching(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.teaching` (
  code varchar(6) not null,
  foreign key (code) references `ucas.modules`(code),
  staffid varchar(5) not null,
  foreign key (staffid) references `ucas.staff`(staffid)
)
""")

    print dbc.execute("""
insert into `rmm`.`ucas.teaching`
  (staffid, code)
values
  ("bsl", "G52APT"),
  ("bsl", "G54DIA"),
  ("nhn", "G53CMP"),
  ("nhn", "G54FOP"),
  ("srb", "G53DOC"),
  ("srb", "G51PRG"),
  ("bnk", "G51WPS")
""")

def add_slots(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.slots` (
  slotid int not null auto_increment,
  primary key (slotid),

  dateid int not null,
  foreign key (dateid) references `ucas.dates`(dateid),
  staffid varchar(5) not null,
  foreign key (staffid) references `ucas.staff`(staffid),

  room varchar(16),
  spaces int default 6
)
""")

    print dbc.execute("""
insert into `rmm`.`ucas.slots`
  (dateid, staffid, room)
values
  (2, "bnk", "Pod 1"),
  (2, "nhn", "Hub"),
  (2, "srb", "Pod 3"),
  (2, "bsl", "Pod 2")
""")

def add_bookings(dbc):
    print dbc.execute("""
create table if not exists `rmm`.`ucas.bookings` (
  ucasid varchar(32) not null,
  name varchar(64) not null,
  slotid int not null,
  foreign key (slotid) references `ucas.slots`(slotid)
)
""")

if __name__ == '__main__':

    if False:
        create_user()
        sys.exit(0)

    db = MySQLdb.connect(
        host=Config.get("database", "host"),
        user=Config.get("database", "user"),
        passwd=Config.get("database", "pass"),
        )
    dbc = db.cursor()

    if True: add_dates(dbc)
    if False: add_modules(dbc)
    if False: add_staff(dbc)
    if False: add_teaching(dbc)
    if False: add_slots(dbc)
    if False: add_bookings(dbc)

    db.commit()
