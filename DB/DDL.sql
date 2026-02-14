-- Таблицы
create table quest
(
	id bigserial primary key,
	quest text,
	answer text
);
-- select * from quest
-- select * from information_schema.tables