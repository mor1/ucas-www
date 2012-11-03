-- as root

create user 'user'@'localhost' IDENTIFIED BY 'password';
grant all privileges on ucas.* to 'user'@'localhost';

create database if not exists `rmm` 
  character set "utf8" 
  collate "utf8_unicode_ci";

-- as user

create table if not exists `rmm`.`ucas.applicants` (
  ucasid varchar(32),
  name varchar(64),
  email varchar(128)
);

create table if not exists `rmm`.`ucas.staff` (
  staffid varchar(5)
  
);

-- create table if not exists `rmm`.`ucas.slots` (
-- );
