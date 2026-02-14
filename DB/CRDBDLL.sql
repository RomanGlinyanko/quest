create database quest encoding utf8;

-- Переключиться на БД Quest
create user quest with password 'RX777ngS';
-- drop user quest
create schema quest authorization quest;

-- select * from information_schema.schemata;


/* select 
	* 
from 
	pg_roles r
join
	pg_user u
on
	r.rolname = u.usename;
*/