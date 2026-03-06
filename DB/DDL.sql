-- Таблицы
--- Пользователи
create table users
(
	id bigserial primary key, 
	email text not null,
	login text unique,
	insert_ts timestamp default current_timestamp
);
comment on table users is 'Пользователи';
comment on column users.id is 'Первичный ключ';
comment on column users.email is 'Адрес электронной почты';
comment on column users.login is 'Логин пользователя';
comment on column users.insert_ts is 'Дата-время добавления записи';
--- Пространства
create table quest_space
(
	id bigserial primary key,
	space text unique not null,
	user_id bigint,
	insert_ts timestamp default current_timestamp,
	constraint space_user_id foreign key (user_id) references users(id) on delete set null
);
comment on table quest_space is 'Пространство вопроса (тематика)';
comment on column quest_space.id is 'Первичный ключ';
comment on column quest_space.space is 'Название пространства';
comment on column quest_space.user_id is 'ID пользователя';
comment on column quest_space.insert_ts is 'Дата-время добавления записи';
--- Вопросы
create table quest
(
	id bigserial primary key,
	quest text,
	answer text,
	user_id bigint,
	insert_ts timestamp default current_timestamp,
	constraint quest_user_id foreign key (user_id) references users(id) on delete set null 
);

comment on table quest is 'Таблица вопросов';
comment on column quest.id is 'Первичный ключ';
comment on column quest.quest is 'Вопрос';
comment on column quest.answer is 'Ответ';
comment on column quest.user_id is 'ID пользователя';
comment on column quest.insert_ts is 'Дата-время добавления';
-- Соединение Пространства - Вопрос
create table conn_space_quest
(
	id bigserial primary key,
	space_id bigint not null,
	quest_id bigint not null,
	user_id bigint,
	insert_ts timestamp default current_timestamp,
	constraint conn_space foreign key (space_id) references quest_space(id) on delete cascade,
	constraint conn_quest foreign key (quest_id) references quest(id) on delete cascade,
	constraint space_quest_user_id foreign key (user_id) references users(id) on delete set null,
	constraint un_space_quest unique (space_id, quest_id)
);
comment on table conn_space_quest is 'Соединение Пространства - Вопросы';
comment on column conn_space_quest.space_id is 'Соединение с пространствами';
comment on column conn_space_quest.quest_id is 'Соединение с вопросами';
comment on column conn_space_quest.user_id is 'ID пользователя';
comment on column conn_space_quest.insert_ts is 'Дата-время добавления записи';
-- Словарь терминов
create table term_dict
(
	id bigserial primary key,
	term text,
	def text,
	comm text,
	user_id bigint,
	insert_ts timestamp default current_timestamp,
	constraint term_dict_user_id foreign key (user_id) references users(id) on delete set null
);

comment on table term_dict is 'Таблица терминов';
comment on column term_dict.id is 'Первичный ключ';
comment on column term_dict.term is 'Термин';
comment on column term_dict.def is 'Определение';
comment on column term_dict.comm is 'Комментарий';
comment on column term_dict.user_id is 'ID пользователя';
comment on column term_dict.insert_ts is 'Дата-время добавления';

-- Связь Вопрос - Термины
create table conn_quest_term
(
	id bigserial primary key,
	quest_id bigint not null,
	term_id bigint not null,
	user_id bigint,
	insert_ts timestamp default current_timestamp,
	constraint conn_quest foreign key (quest_id) references quest(id),
	constraint conn_term foreign key (term_id) references term_dict(id),
	constraint un_quest_term unique (quest_id, term_id)
);

comment on table conn_quest_term is 'Соединение Вопрос - Термины';
comment on column conn_quest_term.quest_id is 'ID вопроса';
comment on column conn_quest_term.term_id is 'ID термина';
comment on column conn_quest_term.user_id is 'ID пользователя';
comment on column conn_quest_term.insert_ts is 'Дата-время добавления записи';


