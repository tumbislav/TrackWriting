-- Just a helper file for developing SQL statements. It is never
-- accessed directly, statements have to be copied into appropriate python strings

create table meta (
  id integer primary key,
  database_version text,
  system_version text,
  upgraded_on text,
  last_saved text,
  is_current text
);

insert into meta (database_version, system_version) values ('0.0');

create table works (
  id integer primary key,
  name text not null,
  work_level text not null,   -- collection, work, version or part
  parent integer,        -- when the work has a parent
  json text not null
);

create table history (
  id integer primary key,
  history_work integer not null,
  history_type text,
  history_value text,
  valid_from timestamp,
  foreign key(history_work) references works(id)
);

create table collections (
  id integer primary key,
  collection_name text not null,
  json text not null
);

create table i18n (
  id integer primary key,
  language text,
  json text not null
)